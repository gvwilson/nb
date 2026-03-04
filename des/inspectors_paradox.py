"""Inspector's Paradox: a random observer almost always arrives during a long gap."""

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
    # Inspector's Paradox

    A random observer almost always arrives during a long gap between buses.

    The Inspector's Paradox (also called the waiting-time paradox or length-biased sampling)
    states that the expected wait time exceeds the naive estimate of half the mean headway
    whenever the headway has variance > 0.

    Formula: E[wait] = E[headway]/2 + Var[headway] / (2 × E[headway])
    """)
    return


@app.cell
def _():
    import random
    import statistics
    import altair as alt
    import polars as pl
    from asimpy import Environment, Process

    SIM_TIME = 100_000
    MEAN_HEADWAY = 10.0
    N_PASSENGERS = 20_000
    SEED = 42
    return (
        Environment, MEAN_HEADWAY, N_PASSENGERS, Process,
        SEED, SIM_TIME, alt, pl, random, statistics,
    )


@app.cell
def _(Environment, MEAN_HEADWAY, N_PASSENGERS, Process, SEED, SIM_TIME, random, statistics):
    class BusService(Process):
        def init(self, mode, bus_arrivals):
            self.mode = mode
            self.bus_arrivals = bus_arrivals

        async def run(self):
            while True:
                if self.mode == "regular":
                    headway = MEAN_HEADWAY
                elif self.mode == "exponential":
                    headway = random.expovariate(1.0 / MEAN_HEADWAY)
                elif self.mode == "clustered":
                    headway = 2.0 if random.random() < 0.5 else 18.0
                else:
                    raise ValueError(f"Unknown mode: {self.mode}")
                await self.timeout(headway)
                self.bus_arrivals.append(self.now)

    def collect_buses(mode, seed=SEED):
        random.seed(seed)
        bus_arrivals = []
        env = Environment()
        BusService(env, mode, bus_arrivals)
        env.run(until=SIM_TIME)
        return bus_arrivals

    def expected_wait(bus_arrivals, n=N_PASSENGERS, seed=SEED):
        rng = random.Random(seed + 1)
        max_t = bus_arrivals[-1]
        waits = []
        for _ in range(n):
            t = rng.uniform(0.0, max_t * 0.95)
            for b in bus_arrivals:
                if b > t:
                    waits.append(b - t)
                    break
        return statistics.mean(waits) if waits else 0.0

    def headway_variance(bus_arrivals):
        headways = [b - a for a, b in zip(bus_arrivals, bus_arrivals[1:])]
        return statistics.variance(headways) if len(headways) > 1 else 0.0

    return (collect_buses, expected_wait, headway_variance)


@app.cell
def _(MEAN_HEADWAY, collect_buses, expected_wait, headway_variance, pl):
    rows = []
    naive = MEAN_HEADWAY / 2.0
    for mode in ["regular", "exponential", "clustered"]:
        buses = collect_buses(mode)
        var_h = headway_variance(buses)
        mean_w = expected_wait(buses)
        rows.append({
            "mode": mode,
            "var_headway": var_h,
            "mean_wait": mean_w,
            "ratio": mean_w / naive,
        })
    df = pl.DataFrame(rows)
    return df, naive, rows


@app.cell(hide_code=True)
def _(MEAN_HEADWAY, mo, naive):
    mu = MEAN_HEADWAY
    var_clustered = 0.5 * (2 - mu) ** 2 + 0.5 * (18 - mu) ** 2
    mo.md(f"""
    ## Results

    Mean headway: {MEAN_HEADWAY} → naive expected wait = {naive:.1f}

    - **Exponential** (Var = E² = {mu**2:.1f}): predicted = {mu:.1f} (= full mean headway!)
    - **Clustered** (Var = {var_clustered:.1f}): predicted = {mu / 2 + var_clustered / (2 * mu):.1f}
    """)
    return (mu, var_clustered)


@app.cell
def _(df):
    df


@app.cell
def _(alt, df, naive, pl):
    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("mode:N", title="Bus schedule type"),
            y=alt.Y("mean_wait:Q", title="Mean passenger wait"),
            color=alt.Color("mode:N", legend=None),
            tooltip=["mode:N", "mean_wait:Q", "ratio:Q"],
        )
        .properties(title="Inspector's Paradox: Mean Wait by Schedule Type")
    )
    naive_line = (
        alt.Chart(pl.DataFrame({"naive": [naive]}))
        .mark_rule(strokeDash=[4, 4], color="gray")
        .encode(y="naive:Q")
    )
    (chart + naive_line)
    return (chart,)


if __name__ == "__main__":
    app.run()
