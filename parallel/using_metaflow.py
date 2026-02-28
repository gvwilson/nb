"""Metaflow implementation of the four-stage parallel pipeline.

Run with:
    python using_metaflow.py run

To run Stage 2 / Stage 3 on a remote compute backend (AWS Batch, Kubernetes,
etc.) add --with batch or --with kubernetes to the run command.  The foreach
fan-out is handled entirely by Metaflow; you do not need to change the step
code.

Topology
--------
start  ──foreach params_list──>  process_group  ──>  transform_stats  ──join──>  end
       (Stage 1)                 (Stage 2, N tasks)  (Stage 3, N tasks)           (Stage 4)
"""

from metaflow import FlowSpec, step

from parallel import (
    aggregate_results,
    generate_params,
    process_group,
    transform_stats,
)


class ParallelPipelineFlow(FlowSpec):
    """Four-stage statistical pipeline with Metaflow fan-out / fan-in.

    Metaflow's `foreach` parameter on `self.next()` triggers automatic
    parallelism: one clone of the target step is created for each element
    of the named list attribute.  Each clone receives its element via
    `self.input`.  The subsequent `join` step receives an `inputs` iterable
    that contains the completed clones.
    """

    @step
    def start(self):
        """Stage 1 — generate parameter sets and fan out."""
        # Storing the list on self makes it available to the foreach mechanism.
        self.params_list = generate_params()
        # foreach="params_list" creates one parallel branch per element.
        self.next(self.process_group, foreach="params_list")

    @step
    def process_group(self):
        """Stage 2 — compute raw statistics for one group.

        self.input is set by Metaflow to the current element of params_list.
        """
        self.stats = process_group(self.input)
        self.next(self.transform_stats)

    @step
    def transform_stats(self):
        """Stage 3 — derive normalized metrics for one group."""
        self.transformed = transform_stats(self.stats)
        self.next(self.join)

    @step
    def join(self, inputs):
        """Stage 4 — fan all Stage 3 results into a single summary.

        `inputs` is an iterable of completed branch objects.  Each has a
        `.transformed` attribute set by the transform_stats step above.
        """
        self.summary = aggregate_results([inp.transformed for inp in inputs])
        self.next(self.end)

    @step
    def end(self):
        """Print summary and finish."""
        print("Pipeline complete.")
        for key, value in self.summary.items():
            print(f"  {key}: {value}")


if __name__ == "__main__":
    ParallelPipelineFlow()
