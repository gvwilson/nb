"""Dagster implementation of the four-stage parallel pipeline.

Launch with:
    dagster dev -f using_dagster.py        # open the web UI, then click Materialize
    dagster job execute -f using_dagster.py -j parallel_pipeline_job   # CLI

Topology
--------
generate_params_op  ──DynamicOut──>  process_group_op  ──>  transform_stats_op  ──collect──>  aggregate_results_op
(Stage 1)                            (Stage 2, N tasks)      (Stage 3, N tasks)                (Stage 4)

The key primitives:
- `DynamicOut` / `DynamicOutput`  — yield one output per group from Stage 1.
- `.map(op)`                      — apply an op to each dynamic output independently.
- `.collect()`                    — gather all dynamic outputs into a list for Stage 4.
"""

from dagster import DynamicOut, DynamicOutput, OpExecutionContext, job, op

from parallel import (
    aggregate_results,
    generate_params,
    process_group,
    transform_stats,
)


@op(out=DynamicOut())
def generate_params_op(context: OpExecutionContext):
    """Stage 1 — generate parameter sets and fan out via DynamicOutput.

    Yielding a DynamicOutput for each group tells Dagster to create one
    independent execution of any downstream op that consumes this output.
    The mapping_key must be a valid Python identifier; it appears in the
    run UI to identify each dynamic branch.
    """
    for params in generate_params():
        gid = params["group_id"]
        context.log.info(f"Emitting params for group {gid}")
        yield DynamicOutput(params, mapping_key=f"group_{gid}")


@op
def process_group_op(context: OpExecutionContext, params: dict) -> dict:
    """Stage 2 — compute raw statistics for one group."""
    stats = process_group(params)
    context.log.info(f"Processed group {stats['group_id']}: mean={stats['mean']:.3f}")
    return stats


@op
def transform_stats_op(context: OpExecutionContext, stats: dict) -> dict:
    """Stage 3 — derive normalized metrics for one group."""
    transformed = transform_stats(stats)
    context.log.info(
        f"Transformed group {transformed['group_id']}: cv={transformed['cv']:.3f}"
    )
    return transformed


@op
def aggregate_results_op(context: OpExecutionContext, transformed_list: list) -> dict:
    """Stage 4 — fan all Stage 3 results into a single summary.

    `transformed_list` is populated by calling `.collect()` on the dynamic
    output of transform_stats_op in the job definition below.  Dagster
    guarantees that every dynamic branch has completed before this op runs.
    """
    summary = aggregate_results(transformed_list)
    context.log.info(f"Summary: {summary}")
    return summary


@job
def parallel_pipeline_job():
    """Wire the four ops together using Dagster's dynamic graph API.

    `.map(op)` applies an op to each DynamicOutput independently.
    `.collect()` collapses the resulting dynamic outputs into a plain list
    that can be passed to a non-dynamic op.
    """
    # Stage 1 → fan out
    params = generate_params_op()

    # Stage 2 — one execution per group
    stats = params.map(process_group_op)

    # Stage 3 — one execution per Stage 2 result (chained .map keeps the
    # same set of dynamic keys; no extra fan-out or fan-in occurs here)
    transformed = stats.map(transform_stats_op)

    # Stage 4 — fan in: .collect() waits for all branches and returns a list
    aggregate_results_op(transformed.collect())


if __name__ == "__main__":
    result = parallel_pipeline_job.execute_in_process()
    print("Success:", result.success)
