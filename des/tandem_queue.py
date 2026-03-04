"""Tandem Queue Blocking: variability at Stage 1 starves Stage 2."""

import marimo

__generated_with = "0.20.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Tandem Queue Blocking

    Variability at Stage 1 starves Stage 2.

    In a two-stage pipeline, if Stage 1 has high variance (sometimes fast, sometimes
    very slow), it creates bursts that overflow the inter-stage buffer and cause Stage 2
    to sit idle waiting for work — even when the overall load is the same.

    As the buffer capacity between stages grows, Stage 2 idle time falls and throughput rises.
    """)
    return


@app.cell
def _():
    import random
    import altair as alt
    import polars as pl
    from asimpy import Environment, Process, Queue

    SIM_TIME = 50_000
    ARRIVAL_RATE = 0.8
    MEAN_SERVICE = 1.0
    SEED = 42
    return (
        ARRIVAL_RATE, Environment, MEAN_SERVICE, Process,
        Queue, SEED, SIM_TIME, alt, pl, random,
    )


@app.cell
def _(ARRIVAL_RATE, Environment, MEAN_SERVICE, Process, Queue, SEED, SIM_TIME, random):
    def high_variance_service():
        if random.random() < 0.80:
            return random.expovariate(5.0)
        return random.expovariate(1.0 / 4.5)

    def low_variance_service():
        return MEAN_SERVICE

    class Source(Process):
        def init(self, buffer):
            self.buffer = buffer

        async def run(self):
            jid = 0
            while True:
                await self.timeout(random.expovariate(ARRIVAL_RATE))
                await self.buffer.put(jid)
                jid += 1

    class Stage1(Process):
        def init(self, inp, out, idle_tally):
            self.inp = inp
            self.out = out
            self.idle_tally = idle_tally

        async def run(self):
            while True:
                idle_start = self.now
                job = await self.inp.get()
                self.idle_tally.append(self.now - idle_start)
                await self.timeout(high_variance_service())
                await self.out.put(job)

    class Stage2(Process):
        def init(self, inp, idle_tally, completions):
            self.inp = inp
            self.idle_tally = idle_tally
            self.completions = completions

        async def run(self):
            while True:
                idle_start = self.now
                await self.inp.get()
                idle = self.now - idle_start
                self.idle_tally.append(idle)
                await self.timeout(low_variance_service())
                self.completions.append(self.now)

    def simulate(buffer_capacity, seed=SEED):
        random.seed(seed)
        env = Environment()
        input_q = Queue(env)
        middle_q = Queue(env, max_capacity=buffer_capacity)
        s2_idle = []
        completions = []
        Source(env, input_q)
        Stage1(env, input_q, middle_q, [])
        Stage2(env, middle_q, s2_idle, completions)
        env.run(until=SIM_TIME)
        n = len(completions)
        idle_total = sum(s2_idle)
        return {
            "buffer_capacity": buffer_capacity,
            "throughput": n / SIM_TIME,
            "stage2_idle_frac": idle_total / SIM_TIME,
            "n_completed": n,
        }

    return (simulate,)


@app.cell
def _(pl, simulate):
    df = pl.DataFrame([simulate(buffer_capacity=k) for k in [1, 2, 3, 5, 8, 13, 21]])
    return (df,)


@app.cell(hide_code=True)
def _(ARRIVAL_RATE, MEAN_SERVICE, mo):
    mo.md(f"""
    ## Results

    Arrival rate: {ARRIVAL_RATE}, mean service per stage: {MEAN_SERVICE}

    - Stage 1: hyperexponential (high variance: 80% short mean=0.2, 20% long mean=4.5)
    - Stage 2: deterministic (zero variance)

    > As buffer capacity grows, Stage 2 idle fraction falls toward 0%.
    """)
    return


@app.cell
def _(df):
    df


@app.cell
def _(alt, df):
    throughput_line = (
        alt.Chart(df)
        .mark_line(point=True)
        .encode(
            x=alt.X("buffer_capacity:Q", title="Buffer capacity (K)"),
            y=alt.Y("throughput:Q", title="Throughput (jobs/time)"),
            tooltip=["buffer_capacity:Q", "throughput:Q"],
        )
        .properties(title="Tandem Queue: Throughput vs. Buffer Capacity")
    )
    idle_line = (
        alt.Chart(df)
        .mark_line(point=True, strokeDash=[4, 4], color="orange")
        .encode(
            x=alt.X("buffer_capacity:Q"),
            y=alt.Y("stage2_idle_frac:Q", title="Stage 2 idle fraction"),
        )
    )
    (throughput_line + idle_line).resolve_scale(y="independent")
    return (idle_line, throughput_line)


if __name__ == "__main__":
    app.run()
