# Distributed Parallel Workflows from a Marimo Notebook

## How the Notebook Exports Its Functions

Marimo provides two mechanisms that together make notebook-defined functions
importable as ordinary Python:

**`with app.setup:`** — a special context block whose body runs at module level
(not wrapped in a cell function). Anything defined here — imports, constants —
is available to `@app.function` cells and is part of the module's public
namespace when the file is imported.

**`@app.function`** — a cell decorator for cells that define exactly one
function. Unlike `@app.cell`, it does not wrap the function in a closure; it
returns the function unchanged and registers it as a top-level symbol. The
function may only reference names from the setup cell or other
`@app.function` / `@app.class_definition` symbols.

Because both the setup body and the `@app.function` definitions are at module
level, a plain import works with no helper code:

```python
from parallel import N_GROUPS, generate_params, process_group, \
                     transform_stats, aggregate_results
```

---

## What This Directory Contains

| File | Purpose |
|------|---------|
| `parallel.py` | Marimo notebook — sequential reference implementation |
| `using_metaflow.py` | Same pipeline expressed as a Metaflow `FlowSpec` |
| `using_dagster.py` | Same pipeline expressed as a Dagster `@job` |
| `using_luigi.py` | Same pipeline expressed as a set of Luigi `Task` classes |
| `index.md` | This file |

---

## The Pipeline

The notebook implements a four-stage statistical pipeline over *N* independent
data groups.  Each group has a fixed seed and sample size; groups do not share
data.

```
Stage 1  generate_params()     →  [params_0, params_1, …, params_N-1]
              │
         ┌────┼────┐  ← fan-out: N independent branches
         ↓    ↓    ↓
Stage 2  process_group()  ×N   →  raw statistics (mean, std, min, max, count)
         ↓    ↓    ↓
Stage 3  transform_stats() ×N  →  derived metrics (CV, range, stderr)
         └────┼────┘  ← fan-in: all branches converge
              ↓
Stage 4  aggregate_results()   →  grand summary record
```

Stages 2 and 3 are **embarrassingly parallel**: each branch touches only its
own data and can run on any worker without coordination.  Stage 4 has a strict
data dependency on all Stage 3 outputs, so it cannot start until the slowest
branch finishes.

The four pure functions (`generate_params`, `process_group`, `transform_stats`,
`aggregate_results`) are copied verbatim into each framework file.  The only
thing that changes between files is the orchestration layer.

---

## Running the Notebook

```bash
marimo run parallel.py          # read-only, fastest
marimo edit parallel.py         # interactive
```

---

## Metaflow (`using_metaflow.py`)

```bash
python using_metaflow.py run
python using_metaflow.py run --with batch          # AWS Batch workers
python using_metaflow.py run --with kubernetes     # Kubernetes workers
```

### How it works

Metaflow expresses fan-out with a single `foreach` argument on `self.next()`:

```python
@step
def start(self):
    self.params_list = generate_params()
    self.next(self.process_group, foreach="params_list")  # fan-out

@step
def process_group(self):
    self.stats = process_group(self.input)   # self.input is one element
    self.next(self.transform_stats)

@step
def transform_stats(self):
    self.transformed = transform_stats(self.stats)
    self.next(self.join)

@step
def join(self, inputs):                      # fan-in
    self.summary = aggregate_results([inp.transformed for inp in inputs])
    self.next(self.end)
```

Each step decorated with `@step` is a unit of work.  Between `start` and
`join`, Metaflow forks the execution graph into N concurrent branches and
manages retries, artifact persistence, and (optionally) remote dispatch
automatically.  The `join` step receives an `inputs` iterable of completed
branch objects, each carrying the artifacts written by its branch.

### Trade-offs

- Minimal boilerplate — the `foreach` / `join` pattern requires almost no
  extra code compared with the sequential version.
- Artifact store baked in: every run's inputs and outputs are versisted and
  inspectable via `metaflow.get_metadata()`.
- Remote execution requires a configured AWS / Kubernetes environment; local
  execution is single-process by default.

---

## Dagster (`using_dagster.py`)

```bash
# CLI execution (no UI required)
python using_dagster.py

# Launch the web UI, then click "Materialize all"
dagster dev -f using_dagster.py
```

### How it works

Dagster's dynamic graph API uses `DynamicOut` / `DynamicOutput` to produce a
variable number of outputs from one op, and `.map()` / `.collect()` to
consume them:

```python
@op(out=DynamicOut())
def generate_params_op(context):
    for params in generate_params():
        yield DynamicOutput(params, mapping_key=f"group_{params['group_id']}")

@op
def process_group_op(context, params: dict) -> dict: ...

@op
def transform_stats_op(context, stats: dict) -> dict: ...

@op
def aggregate_results_op(context, transformed_list: list) -> dict: ...

@job
def parallel_pipeline_job():
    params     = generate_params_op()          # DynamicOut
    stats      = params.map(process_group_op)  # DynamicOut × N
    transformed = stats.map(transform_stats_op) # DynamicOut × N
    aggregate_results_op(transformed.collect()) # list → single op
```

Each `DynamicOutput` carries a `mapping_key` (a valid Python identifier) that
Dagster uses to label the branch in the UI and in logs.  `.map()` propagates
the dynamic structure; `.collect()` collapses it into an ordinary list.

### Trade-offs

- Rich first-party UI with per-op logs, asset lineage, and run history.
- `DynamicOut` / `.map()` / `.collect()` is slightly more verbose than
  Metaflow's `foreach`, but the job-definition code reads almost like a
  dataflow graph.
- Dagster's asset model (not used here) adds software-defined assets,
  freshness policies, and data cataloguing on top of the job model.

---

## Luigi (`using_luigi.py`)

```bash
# Local scheduler — no daemon required
python using_luigi.py AggregateResults --n-groups 4 --local-scheduler

# Central scheduler — shows dependency graph in the Luigi web UI
luigid &
python using_luigi.py AggregateResults --n-groups 4
```

### How it works

Luigi models each unit of work as a `Task` subclass with three methods:
`requires()` (upstream dependencies), `output()` (the file or target that
marks completion), and `run()` (the work itself).  Fan-out and fan-in are
expressed through list comprehensions inside `requires()`:

```python
class AggregateResults(luigi.Task):
    n_groups = luigi.IntParameter(default=4)

    def requires(self):
        # returning a list causes Luigi to run all elements in parallel
        return [TransformStats(group_id=i) for i in range(self.n_groups)]

    def output(self):
        return luigi.LocalTarget("summary.json")

    def run(self):
        transformed_list = [json.load(t.open()) for t in self.input()]
        summary = aggregate_results(transformed_list)
        with self.output().open("w") as fh:
            json.dump(summary, fh)
```

Because each `ProcessGroup` and `TransformStats` instance writes a distinct
output file, Luigi can check completion at any granularity and resume a
partially-finished pipeline run without re-executing completed tasks.  Pass
`--workers N` (N ≥ n_groups) to get full Stage 2 / Stage 3 parallelism.

### Trade-offs

- The target / output idiom gives you idempotent, resumable pipelines almost
  for free — a huge practical advantage for long-running or error-prone jobs.
- The fan-out is implicit (a list in `requires()`), not a first-class concept.
  The number of parallel branches must be known at scheduling time, unlike
  Metaflow and Dagster which can determine it at runtime.
- No built-in artifact store; the filesystem *is* the store.  This is simple
  but means you manage file naming and cleanup yourself.

---

## Framework Comparison

| Concern | Metaflow | Dagster | Luigi |
|---------|----------|---------|-------|
| Fan-out primitive | `foreach=` on `self.next()` | `DynamicOut` + `.map()` | list in `requires()` |
| Fan-in primitive | `join(self, inputs)` step | `.collect()` | list in `requires()` of downstream task |
| Dynamic branch count | Yes — determined at runtime | Yes — determined at runtime | No — must be fixed at scheduling time |
| Intermediate storage | Metaflow artifact store | In-memory (configurable) | Filesystem targets |
| Resumability | Yes — per-step checkpointing | Yes — re-execution from failure | Yes — target-based skipping |
| Remote execution | `--with batch` / `--with kubernetes` | Dagster Cloud / custom executors | Distributed workers via `luigid` |
| UI | `metaflow ui` (Metaflow Service) | `dagster dev` (built-in) | `luigid` (basic) |
