"""Convoy Effect: one slow job behind a FIFO gate delays many fast jobs."""

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
    # Convoy Effect

    One slow job behind a FIFO gate delays many fast jobs.

    Compares FIFO (first-in, first-out) scheduling against Shortest Job First (SJF)
    using a hyperexponential service time distribution (mostly quick, occasionally very slow).
    """)
    return


@app.cell
def _():
    import random
    import statistics
    import altair as alt
    import polars as pl
    from asimpy import Environment, Process, Queue

    ARRIVAL_RATE = 0.7
    SIM_TIME = 50_000
    SEED = 42
    SHORT_RATE = 4.0
    LONG_RATE = 0.2
    LONG_PROB = 0.10
    return (
        ARRIVAL_RATE, Environment, LONG_PROB, LONG_RATE, Process,
        Queue, SEED, SHORT_RATE, SIM_TIME, alt, pl, random, statistics,
    )


@app.cell
def _(ARRIVAL_RATE, Environment, LONG_PROB, LONG_RATE, Process, Queue, SEED, SHORT_RATE, SIM_TIME, random, statistics):
    def service_time():
        if random.random() < LONG_PROB:
            return random.expovariate(LONG_RATE)
        return random.expovariate(SHORT_RATE)

    class JobSource(Process):
        def init(self, job_queue, arrivals, sjf):
            self.job_queue = job_queue
            self.arrivals = arrivals
            self.sjf = sjf
            self._jid = 0

        async def run(self):
            while True:
                await self.timeout(random.expovariate(ARRIVAL_RATE))
                jid = self._jid
                self._jid += 1
                svc = service_time()
                self.arrivals[jid] = (self.now, svc)
                if self.sjf:
                    await self.job_queue.put((svc, jid))
                else:
                    await self.job_queue.put((jid, svc))

    class Server(Process):
        def init(self, job_queue, arrivals, sojourn_times, sjf):
            self.job_queue = job_queue
            self.arrivals = arrivals
            self.sojourn_times = sojourn_times
            self.sjf = sjf

        async def run(self):
            while True:
                item = await self.job_queue.get()
                if self.sjf:
                    svc, jid = item
                else:
                    jid, svc = item
                await self.timeout(svc)
                arrival_time, _ = self.arrivals[jid]
                self.sojourn_times.append(self.now - arrival_time)

    def simulate(sjf, seed=SEED):
        random.seed(seed)
        arrivals = {}
        sojourn_times = []
        env = Environment()
        q = Queue(env, priority=sjf)
        JobSource(env, q, arrivals, sjf)
        Server(env, q, arrivals, sojourn_times, sjf)
        env.run(until=SIM_TIME)
        return {
            "mean": statistics.mean(sojourn_times),
            "median": statistics.median(sojourn_times),
            "p95": sorted(sojourn_times)[int(0.95 * len(sojourn_times))],
            "p99": sorted(sojourn_times)[int(0.99 * len(sojourn_times))],
            "n": len(sojourn_times),
        }

    return (simulate,)


@app.cell
def _(LONG_PROB, LONG_RATE, SHORT_RATE, pl, simulate):
    fifo = simulate(sjf=False)
    sjf_res = simulate(sjf=True)
    rows = [
        {
            "metric": m,
            "fifo": fifo[m],
            "sjf": sjf_res[m],
            "improvement": fifo[m] / sjf_res[m],
        }
        for m in ("mean", "median", "p95", "p99")
    ]
    df = pl.DataFrame(rows)
    mean_svc = (1 - LONG_PROB) / SHORT_RATE + LONG_PROB / LONG_RATE
    return df, fifo, mean_svc, sjf_res


@app.cell(hide_code=True)
def _(ARRIVAL_RATE, LONG_PROB, LONG_RATE, SHORT_RATE, mean_svc, mo):
    mo.md(f"""
    ## Summary Statistics

    Arrival rate: {ARRIVAL_RATE}, estimated mean service: {mean_svc:.3f}

    Short jobs: {100 * (1 - LONG_PROB):.0f}% (mean {1 / SHORT_RATE:.2f}),
    Long jobs: {100 * LONG_PROB:.0f}% (mean {1 / LONG_RATE:.1f})

    > **Note:** SJF is optimal for mean sojourn time but requires knowing job sizes in advance.
    """)
    return


@app.cell
def _(df):
    df


@app.cell
def _(alt, df, pl):
    df_plot = df.filter(pl.col("metric") != "n").unpivot(
        on=["fifo", "sjf"],
        index="metric",
        variable_name="policy",
        value_name="sojourn_time",
    )
    chart = (
        alt.Chart(df_plot)
        .mark_bar()
        .encode(
            x=alt.X("metric:N", title="Metric"),
            y=alt.Y("sojourn_time:Q", title="Sojourn time"),
            color=alt.Color("policy:N", title="Policy"),
            xOffset="policy:N",
            tooltip=["metric:N", "policy:N", "sojourn_time:Q"],
        )
        .properties(title="Convoy Effect: FIFO vs. Shortest Job First")
    )
    chart
    return (chart,)


if __name__ == "__main__":
    app.run()
