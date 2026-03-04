"""Pooled vs. separate queues: one shared line beats multiple dedicated lines."""

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
    # Pooled vs. Separate Queues

    One shared queue beats multiple dedicated queues.

    When customers randomly pick one of several dedicated servers (as in many
    supermarket checkouts), they can get stuck behind slow customers while other
    servers sit idle. A single pooled queue eliminates this waste.
    """)
    return


@app.cell
def _():
    import random
    import statistics
    import altair as alt
    import polars as pl
    from asimpy import Environment, Process, Resource

    SIM_TIME = 100_000
    ARRIVAL_RATE = 1.8
    SERVICE_RATE = 1.0
    N_SERVERS = 2
    SEED = 42
    RHO = ARRIVAL_RATE / (N_SERVERS * SERVICE_RATE)
    return (
        ARRIVAL_RATE, Environment, N_SERVERS, Process,
        Resource, RHO, SEED, SERVICE_RATE, SIM_TIME, alt, pl, random, statistics,
    )


@app.cell
def _(ARRIVAL_RATE, Environment, N_SERVERS, Process, Resource, SEED, SERVICE_RATE, SIM_TIME, random, statistics):
    class Customer(Process):
        def init(self, server, sojourn_times):
            self.server = server
            self.sojourn_times = sojourn_times

        async def run(self):
            arrival = self.now
            async with self.server:
                await self.timeout(random.expovariate(SERVICE_RATE))
            self.sojourn_times.append(self.now - arrival)

    class PooledArrivals(Process):
        def init(self, arrival_rate, server, sojourn_times):
            self.arrival_rate = arrival_rate
            self.server = server
            self.sojourn_times = sojourn_times

        async def run(self):
            while True:
                await self.timeout(random.expovariate(self.arrival_rate))
                Customer(self._env, self.server, self.sojourn_times)

    class SeparateArrivals(Process):
        def init(self, arrival_rate, servers, sojourn_times):
            self.arrival_rate = arrival_rate
            self.servers = servers
            self.sojourn_times = sojourn_times

        async def run(self):
            while True:
                await self.timeout(random.expovariate(self.arrival_rate))
                server = random.choice(self.servers)
                Customer(self._env, server, self.sojourn_times)

    def run_pooled(arrival_rate=ARRIVAL_RATE, seed=SEED):
        random.seed(seed)
        sojourn_times = []
        env = Environment()
        shared_server = Resource(env, capacity=N_SERVERS)
        PooledArrivals(env, arrival_rate, shared_server, sojourn_times)
        env.run(until=SIM_TIME)
        return statistics.mean(sojourn_times)

    def run_separate(arrival_rate=ARRIVAL_RATE, seed=SEED):
        random.seed(seed)
        sojourn_times = []
        env = Environment()
        servers = [Resource(env, capacity=1) for _ in range(N_SERVERS)]
        SeparateArrivals(env, arrival_rate, servers, sojourn_times)
        env.run(until=SIM_TIME)
        return statistics.mean(sojourn_times)

    return (run_pooled, run_separate)


@app.cell
def _(ARRIVAL_RATE, N_SERVERS, RHO, SERVICE_RATE, pl, run_pooled, run_separate):
    sweep_rows = []
    for _rho in [0.5, 0.6, 0.7, 0.8, 0.9]:
        _rate = _rho * N_SERVERS * SERVICE_RATE
        _pw = run_pooled(arrival_rate=_rate)
        _sw = run_separate(arrival_rate=_rate)
        sweep_rows.append({"rho": _rho, "pooled_W": _pw, "separate_W": _sw, "ratio": _sw / _pw})
    df_sweep = pl.DataFrame(sweep_rows)

    pooled_W = run_pooled()
    separate_W = run_separate()
    return df_sweep, pooled_W, separate_W


@app.cell(hide_code=True)
def _(N_SERVERS, RHO, SERVICE_RATE, mo, pooled_W, separate_W):
    mo.md(f"""
    ## Results

    {N_SERVERS} servers, service rate {SERVICE_RATE}, utilisation ρ = {RHO:.2f}

    At ρ = {RHO:.2f}: pooled W = {pooled_W:.3f}, separate W = {separate_W:.3f}
    — separate queues are **{separate_W / pooled_W:.2f}×** slower
    """)
    return


@app.cell
def _(df_sweep):
    df_sweep


@app.cell
def _(alt, df_sweep, pl):
    df_plot = df_sweep.unpivot(
        on=["pooled_W", "separate_W"], index="rho", variable_name="system", value_name="W"
    )
    chart = (
        alt.Chart(df_plot)
        .mark_line(point=True)
        .encode(
            x=alt.X("rho:Q", title="Utilization per server (ρ)"),
            y=alt.Y("W:Q", title="Mean sojourn time (W)"),
            color=alt.Color("system:N", title="Queue type"),
            tooltip=["rho:Q", "system:N", "W:Q"],
        )
        .properties(title="Pooled vs. Separate Queues: Mean Sojourn Time")
    )
    chart
    return (chart,)


if __name__ == "__main__":
    app.run()
