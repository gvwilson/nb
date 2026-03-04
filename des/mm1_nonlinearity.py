"""M/M/1 queue: mean queue length grows nonlinearly with utilization."""

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
    # M/M/1 Queue Nonlinearity

    Mean queue length grows nonlinearly with utilization.

    For an M/M/1 queue the exact formula is:

    $$L = \frac{\rho}{1 - \rho}$$

    This grows without bound as ρ → 1, which means small increases in load near
    capacity cause disproportionately large increases in queue length.
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
    SERVICE_RATE = 1.0
    SEED = 42
    return (
        Environment, Process, Resource, SEED,
        SERVICE_RATE, SIM_TIME, alt, pl, random, statistics,
    )


@app.cell
def _(Environment, Process, Resource, SEED, SERVICE_RATE, SIM_TIME, random, statistics):
    class Customer(Process):
        def init(self, server, service_rate, sojourn_times):
            self.server = server
            self.service_rate = service_rate
            self.sojourn_times = sojourn_times

        async def run(self):
            arrival = self.now
            async with self.server:
                await self.timeout(random.expovariate(self.service_rate))
            self.sojourn_times.append(self.now - arrival)

    class ArrivalStream(Process):
        def init(self, arrival_rate, service_rate, server, sojourn_times):
            self.arrival_rate = arrival_rate
            self.service_rate = service_rate
            self.server = server
            self.sojourn_times = sojourn_times

        async def run(self):
            while True:
                await self.timeout(random.expovariate(self.arrival_rate))
                Customer(self._env, self.server, self.service_rate, self.sojourn_times)

    def simulate(rho, sim_time=SIM_TIME, seed=SEED):
        random.seed(seed)
        arrival_rate = rho * SERVICE_RATE
        sojourn_times = []
        env = Environment()
        server = Resource(env, capacity=1)
        ArrivalStream(env, arrival_rate, SERVICE_RATE, server, sojourn_times)
        env.run(until=sim_time)
        mean_W = statistics.mean(sojourn_times) if sojourn_times else 0.0
        sim_L = arrival_rate * mean_W
        theory_L = rho / (1.0 - rho)
        return sim_L, theory_L

    return (simulate,)


@app.cell
def _(pl, simulate):
    rhos = [0.1, 0.2, 0.3, 0.5, 0.7, 0.8, 0.9, 0.95]
    sweep_rows = []
    for rho in rhos:
        sim_L, theory_L = simulate(rho)
        pct = 100.0 * (sim_L - theory_L) / theory_L
        sweep_rows.append({"rho": rho, "theory_L": theory_L, "sim_L": sim_L, "pct_error": pct})
    df_sweep = pl.DataFrame(sweep_rows)

    marginal_rows = []
    prev_L, prev_rho = None, None
    for _rho in [0.5, 0.6, 0.7, 0.8, 0.9]:
        _theory_L = _rho / (1.0 - _rho)
        if prev_L is not None:
            marginal_rows.append({"rho_from": prev_rho, "rho_to": _rho, "delta_L": _theory_L - prev_L})
        prev_L, prev_rho = _theory_L, _rho
    df_marginal = pl.DataFrame(marginal_rows)
    return df_marginal, df_sweep


@app.cell(hide_code=True)
def _(mo):
    mo.md("## Simulated vs. Theoretical Queue Length")
    return


@app.cell
def _(df_sweep):
    df_sweep


@app.cell(hide_code=True)
def _(mo):
    mo.md("## Marginal Increase in L per 0.1 Step in ρ (Theory)")
    return


@app.cell
def _(df_marginal):
    df_marginal


@app.cell
def _(alt, df_sweep, pl):
    df_plot = df_sweep.unpivot(
        on=["theory_L", "sim_L"], index="rho", variable_name="source", value_name="L"
    )
    chart = (
        alt.Chart(df_plot)
        .mark_line(point=True)
        .encode(
            x=alt.X("rho:Q", title="Utilization (ρ)"),
            y=alt.Y("L:Q", title="Mean queue length (L)"),
            color=alt.Color("source:N", title="Source"),
            tooltip=["rho:Q", "source:N", "L:Q"],
        )
        .properties(title="M/M/1 Queue Length vs. Utilization")
    )
    chart
    return (chart,)


if __name__ == "__main__":
    app.run()
