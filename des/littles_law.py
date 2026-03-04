"""Little's Law holds universally: L = lambda * W across any queue configuration."""

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
    # Little's Law

    Little's Law states that in a stable system, L = λW, where:
    - **L** = mean number of customers in the system
    - **λ** = mean arrival rate
    - **W** = mean time a customer spends in the system

    This notebook verifies Little's Law across three different queue configurations:
    M/M/1, M/D/1, and M/M/3.
    """)
    return


@app.cell
def _():
    import random
    import statistics
    import altair as alt
    import polars as pl
    from asimpy import Environment, Process, Resource

    SIM_TIME = 200_000
    SAMPLE_INTERVAL = 1.0
    SEED = 42
    return (
        Environment, Process, Resource, SAMPLE_INTERVAL,
        SEED, SIM_TIME, alt, pl, random, statistics,
    )


@app.cell
def _(Environment, Process, Resource, SAMPLE_INTERVAL, SEED, SIM_TIME, random, statistics):
    class Monitor(Process):
        def init(self, in_system, samples):
            self.in_system = in_system
            self.samples = samples

        async def run(self):
            while True:
                self.samples.append(self.in_system[0])
                await self.timeout(SAMPLE_INTERVAL)

    class MM1Customer(Process):
        def init(self, server, in_system, sojourn_times):
            self.server = server
            self.in_system = in_system
            self.sojourn_times = sojourn_times

        async def run(self):
            arrival = self.now
            self.in_system[0] += 1
            async with self.server:
                await self.timeout(random.expovariate(1.0))
            self.in_system[0] -= 1
            self.sojourn_times.append(self.now - arrival)

    class MM1Arrivals(Process):
        def init(self, rate, server, in_system, sojourn_times):
            self.rate = rate
            self.server = server
            self.in_system = in_system
            self.sojourn_times = sojourn_times

        async def run(self):
            while True:
                await self.timeout(random.expovariate(self.rate))
                MM1Customer(self._env, self.server, self.in_system, self.sojourn_times)

    class MD1Customer(Process):
        def init(self, server, service_time, in_system, sojourn_times):
            self.server = server
            self.service_time = service_time
            self.in_system = in_system
            self.sojourn_times = sojourn_times

        async def run(self):
            arrival = self.now
            self.in_system[0] += 1
            async with self.server:
                await self.timeout(self.service_time)
            self.in_system[0] -= 1
            self.sojourn_times.append(self.now - arrival)

    class MD1Arrivals(Process):
        def init(self, rate, service_time, server, in_system, sojourn_times):
            self.rate = rate
            self.service_time = service_time
            self.server = server
            self.in_system = in_system
            self.sojourn_times = sojourn_times

        async def run(self):
            while True:
                await self.timeout(random.expovariate(self.rate))
                MD1Customer(self._env, self.server, self.service_time, self.in_system, self.sojourn_times)

    class MM3Customer(Process):
        def init(self, server, in_system, sojourn_times):
            self.server = server
            self.in_system = in_system
            self.sojourn_times = sojourn_times

        async def run(self):
            arrival = self.now
            self.in_system[0] += 1
            async with self.server:
                await self.timeout(random.expovariate(1.0))
            self.in_system[0] -= 1
            self.sojourn_times.append(self.now - arrival)

    class MM3Arrivals(Process):
        def init(self, rate, server, in_system, sojourn_times):
            self.rate = rate
            self.server = server
            self.in_system = in_system
            self.sojourn_times = sojourn_times

        async def run(self):
            while True:
                await self.timeout(random.expovariate(self.rate))
                MM3Customer(self._env, self.server, self.in_system, self.sojourn_times)

    def verify(label, env, in_system, sojourn_times, samples, arrival_rate):
        Monitor(env, in_system, samples)
        env.run(until=SIM_TIME)
        L_direct = statistics.mean(samples)
        W = statistics.mean(sojourn_times)
        n = len(sojourn_times)
        lam = n / SIM_TIME
        L_little = lam * W
        error = 100.0 * (L_little - L_direct) / L_direct
        return {
            "label": label,
            "lambda_obs": lam,
            "mean_W": W,
            "L_direct": L_direct,
            "L_little": L_little,
            "error_pct": error,
        }

    return (
        MD1Arrivals, MM1Arrivals, MM3Arrivals, verify,
    )


@app.cell
def _(Environment, MD1Arrivals, MM1Arrivals, MM3Arrivals, Resource, SEED, pl, random, verify):
    rows = []

    random.seed(SEED)
    lam1, mu1 = 0.7, 1.0
    in_sys1 = [0]
    soj1 = []
    smp1 = []
    env1 = Environment()
    srv1 = Resource(env1, capacity=1)
    MM1Arrivals(env1, lam1, srv1, in_sys1, soj1)
    rows.append(verify("M/M/1 (rho=0.70, 1 server)", env1, in_sys1, soj1, smp1, lam1))

    random.seed(SEED)
    lam2, svc2 = 0.7, 1.0
    in_sys2 = [0]
    soj2 = []
    smp2 = []
    env2 = Environment()
    srv2 = Resource(env2, capacity=1)
    MD1Arrivals(env2, lam2, svc2, srv2, in_sys2, soj2)
    rows.append(verify("M/D/1 (rho=0.70, deterministic service)", env2, in_sys2, soj2, smp2, lam2))

    random.seed(SEED)
    lam3 = 2.4
    in_sys3 = [0]
    soj3 = []
    smp3 = []
    env3 = Environment()
    srv3 = Resource(env3, capacity=3)
    MM3Arrivals(env3, lam3, srv3, in_sys3, soj3)
    rows.append(verify("M/M/3 (rho=0.80 per server, 3 servers)", env3, in_sys3, soj3, smp3, lam3))

    df = pl.DataFrame(rows)
    return df, rows


@app.cell(hide_code=True)
def _(mo):
    mo.md("## Verification: L = λW")
    return


@app.cell
def _(df):
    df


@app.cell
def _(alt, df, pl):
    points = (
        alt.Chart(df)
        .mark_point(size=100, filled=True)
        .encode(
            x=alt.X("L_direct:Q", title="L (direct sample)"),
            y=alt.Y("L_little:Q", title="L = λW (Little's Law)"),
            color=alt.Color("label:N", title="Configuration"),
            tooltip=["label:N", "L_direct:Q", "L_little:Q", "error_pct:Q"],
        )
    )
    max_val = max(df["L_direct"].to_list()) * 1.1
    diagonal = (
        alt.Chart(pl.DataFrame({"x": [0.0, max_val], "y": [0.0, max_val]}))
        .mark_line(color="gray", strokeDash=[4, 4])
        .encode(x="x:Q", y="y:Q")
    )
    (diagonal + points).properties(title="Little's Law: Direct Sample vs. λW")
    return (points,)


if __name__ == "__main__":
    app.run()
