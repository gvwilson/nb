import marimo

__generated_with = "0.20.2"
app = marimo.App(width="medium")

# The setup cell runs before all other cells.  Its body is at module level in
# the file, so anything defined here is available to @app.function cells and
# is also importable by external scripts (using_metaflow.py, etc.).
with app.setup:
    import numpy as np
    N_GROUPS = 4


@app.cell
def _(mo):
    mo.md(
        r"""
        # Reusable function cells

        Each cell defines exactly one function, decorated with `@app.function`.
        `@app.function` returns the function unchanged, so these names are ordinary
        module-level callables that any Python file can import:

        ```
        from parallel import N_GROUPS, generate_params, process_group, \
                       transform_stats, aggregate_results
        ```

        Functions may only reference names from the setup cell or other
        `@app.function` / `@app.class`_definition symbols.
        """
    )
    return


@app.function
def generate_params(n_groups: int = N_GROUPS) -> list[dict]:
    """Return one parameter dict per group.

    Each dict carries the random seed and sample size for that group,
    plus a numeric group_id that also serves as the true mean of the
    synthetic data generated in Stage 2.
    """
    return [
        {"group_id": i, "seed": i * 42, "size": 100 * (i + 1)}
        for i in range(n_groups)
    ]


@app.function
def process_group(params: dict) -> dict:
    """Draw *size* samples from N(group_id, 1) and return raw statistics.

    This function is stateless and side-effect free, making it safe to
    run in any order, on any worker.
    """
    rng = np.random.default_rng(params["seed"])
    data = rng.normal(loc=params["group_id"], scale=1.0, size=params["size"])
    return {
        "group_id": params["group_id"],
        "mean": float(np.mean(data)),
        "std": float(np.std(data)),
        "min": float(np.min(data)),
        "max": float(np.max(data)),
        "count": int(len(data)),
    }


@app.function
def transform_stats(stats: dict) -> dict:
    """Derive normalized metrics from a single group's raw statistics.

    The coefficient of variation (CV) and standard error (SE) are
    scale-independent, making cross-group comparison meaningful even
    when the groups have different true means.
    """
    mean = stats["mean"]
    std = stats["std"]
    count = stats["count"]
    return {
        "group_id": stats["group_id"],
        "mean": mean,
        "cv": std / abs(mean) if mean != 0 else float("inf"),
        "range": stats["max"] - stats["min"],
        "stderr": std / np.sqrt(count),
    }


@app.function
def aggregate_results(transformed_list: list[dict]) -> dict:
    """Fan all per-group results into a single summary record.

    This step has a data dependency on *every* Stage 3 output, so it
    cannot start until the last Stage 3 worker finishes.
    """
    means = [r["mean"] for r in transformed_list]
    cvs = [r["cv"] for r in transformed_list]
    ranges = [r["range"] for r in transformed_list]
    return {
        "n_groups": len(transformed_list),
        "grand_mean": float(np.mean(means)),
        "mean_cv": float(np.mean(cvs)),
        "mean_range": float(np.mean(ranges)),
        "best_group": int(transformed_list[int(np.argmin(cvs))]["group_id"]),
    }


@app.cell
def _():
    import marimo as mo
    import polars as pl
    return mo, pl


@app.cell
def _(mo):
    mo.md(
        r"""
        # Four-Stage Parallel Pipeline

        This notebook implements a simple statistical pipeline in four stages
        that can be parallelized across independent data groups:

        1. **Generate** — produce parameter sets (one per group)
        2. **Process** — compute raw statistics for each group
        3. **Transform** — derive normalized metrics for each group
        4. **Aggregate** — combine all groups into a final summary

        Stages 2 and 3 are embarrassingly parallel: each group's work is
        independent of every other group's. Stage 4 fans them all back in.

        The four functions that implement these stages are defined with
        `@app.function`, placing them at module level so that
        `using_metaflow.py`, `using_dagster.py`, and `using_luigi.py` can
        import them without duplicating any code.
        """
    )
    return


@app.cell
def _(mo):
    mo.md("## Stage 1 — Generate parameter sets")
    return


@app.cell
def _(pl):
    params_list = generate_params()
    pl.DataFrame(params_list)
    return (params_list,)


@app.cell
def _(mo):
    mo.md("## Stage 2 — Process each group")
    return


@app.cell
def _(params_list, pl):
    raw_stats = [process_group(p) for p in params_list]
    pl.DataFrame(raw_stats)
    return (raw_stats,)


@app.cell
def _(mo):
    mo.md("## Stage 3 — Transform each group's statistics")
    return


@app.cell
def _(pl, raw_stats):
    transformed = [transform_stats(s) for s in raw_stats]
    pl.DataFrame(transformed)
    return (transformed,)


@app.cell
def _(mo):
    mo.md("## Stage 4 — Aggregate all groups")
    return


@app.cell
def _(mo, transformed):
    summary = aggregate_results(transformed)
    mo.md(
        f"""
        | Metric | Value |
        |--------|-------|
        | Groups | {summary['n_groups']} |
        | Grand mean | {summary['grand_mean']:.4f} |
        | Mean CV | {summary['mean_cv']:.4f} |
        | Mean range | {summary['mean_range']:.4f} |
        | Most stable group | {summary['best_group']} |
        """
    )
    return (summary,)


if __name__ == "__main__":
    app.run()
