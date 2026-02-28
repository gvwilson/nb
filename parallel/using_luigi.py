"""Luigi implementation of the four-stage parallel pipeline.

Run with:
    python using_luigi.py AggregateResults --n-groups 4 --local-scheduler

Or start the central scheduler first and drop --local-scheduler:
    luigid &
    python using_luigi.py AggregateResults --n-groups 4

Topology
--------
GenerateParams  ──>  ProcessGroup (×N)  ──>  TransformStats (×N)  ──>  AggregateResults
(Stage 1)            (Stage 2)                (Stage 3)                  (Stage 4)

Luigi expresses parallelism through requires(): when a task's requires() list
contains N independent tasks, Luigi's worker pool runs them concurrently.
The fan-out is implicit in the list comprehension inside AggregateResults and
TransformStats.  Targets on the local filesystem act as the data bus between
tasks, giving Luigi idempotent, resumable execution for free.

Intermediate files are written to a temporary directory and cleaned up when
AggregateResults completes.  To keep them for inspection, comment out the
cleanup block in AggregateResults.run().
"""

import json
import shutil
import tempfile
from pathlib import Path

import luigi

from parallel import (
    aggregate_results,
    generate_params,
    process_group,
    transform_stats,
)

# ---------------------------------------------------------------------------
# Shared scratch directory (all tasks in one run share this)
# ---------------------------------------------------------------------------

SCRATCH_DIR = Path(tempfile.mkdtemp(prefix="luigi_pipeline_"))


# ---------------------------------------------------------------------------
# Luigi tasks
# ---------------------------------------------------------------------------

class GenerateParams(luigi.Task):
    """Stage 1 — write the parameter list to a JSON file.

    This task has no upstream dependencies.  Its output acts as the data
    source for every Stage 2 task, but Luigi reads it lazily: each
    ProcessGroup instance opens only the slice it needs.
    """

    n_groups: int = luigi.IntParameter(default=4)

    def output(self) -> luigi.LocalTarget:
        return luigi.LocalTarget(SCRATCH_DIR / "params.json")

    def run(self) -> None:
        params = generate_params(self.n_groups)
        with self.output().open("w") as fh:
            json.dump(params, fh, indent=2)


class ProcessGroup(luigi.Task):
    """Stage 2 — compute raw statistics for one group.

    One instance of this task is created per group.  Luigi schedules all
    instances concurrently (up to --workers N) because they share the same
    upstream task (GenerateParams) but write to distinct output files.
    """

    group_id: int = luigi.IntParameter()
    n_groups: int = luigi.IntParameter(default=4)

    def requires(self) -> GenerateParams:
        return GenerateParams(n_groups=self.n_groups)

    def output(self) -> luigi.LocalTarget:
        return luigi.LocalTarget(SCRATCH_DIR / f"stats_{self.group_id}.json")

    def run(self) -> None:
        with self.input().open() as fh:
            all_params = json.load(fh)
        params = next(p for p in all_params if p["group_id"] == self.group_id)
        stats = process_group(params)
        with self.output().open("w") as fh:
            json.dump(stats, fh, indent=2)


class TransformStats(luigi.Task):
    """Stage 3 — derive normalized metrics for one group.

    Each instance depends on exactly one ProcessGroup instance.  Luigi
    parallelises all N instances the same way it did in Stage 2.
    """

    group_id: int = luigi.IntParameter()
    n_groups: int = luigi.IntParameter(default=4)

    def requires(self) -> ProcessGroup:
        return ProcessGroup(group_id=self.group_id, n_groups=self.n_groups)

    def output(self) -> luigi.LocalTarget:
        return luigi.LocalTarget(SCRATCH_DIR / f"transformed_{self.group_id}.json")

    def run(self) -> None:
        with self.input().open() as fh:
            stats = json.load(fh)
        transformed = transform_stats(stats)
        with self.output().open("w") as fh:
            json.dump(transformed, fh, indent=2)


class AggregateResults(luigi.Task):
    """Stage 4 — fan all Stage 3 results into a single summary.

    requires() returns a list of N TransformStats instances.  Luigi treats
    each element as an independent prerequisite and runs them in parallel.
    self.input() mirrors the structure of requires(), so it is also a list of
    N LocalTarget objects.

    This task does not start until every TransformStats instance has written
    its output file, giving us the fan-in guarantee.
    """

    n_groups: int = luigi.IntParameter(default=4)

    def requires(self) -> list[TransformStats]:
        return [
            TransformStats(group_id=i, n_groups=self.n_groups)
            for i in range(self.n_groups)
        ]

    def output(self) -> luigi.LocalTarget:
        return luigi.LocalTarget(SCRATCH_DIR / "summary.json")

    def run(self) -> None:
        transformed_list = []
        for target in self.input():
            with target.open() as fh:
                transformed_list.append(json.load(fh))

        summary = aggregate_results(transformed_list)

        with self.output().open("w") as fh:
            json.dump(summary, fh, indent=2)

        print("Pipeline complete.")
        for key, value in summary.items():
            print(f"  {key}: {value}")

        # Comment out the next line to keep intermediate files for inspection.
        shutil.rmtree(SCRATCH_DIR, ignore_errors=True)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # --workers controls how many tasks Luigi runs in parallel.
    # Set it to at least n_groups to get full Stage 2 / Stage 3 parallelism.
    luigi.build(
        [AggregateResults(n_groups=4)],
        workers=4,
        local_scheduler=True,
    )
