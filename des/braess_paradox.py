"""Braess's Paradox: adding a road can make everyone's commute longer."""

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
    # Braess's Paradox

    Adding a road can make everyone's commute longer.

    Uses a routing-game approach: cars depart in discrete waves and use logit
    (softmax) routing, which converges smoothly to a Nash equilibrium.
    The DES clock advances one unit per wave.
    """)
    return


@app.cell
def _():
    import math
    import random
    import altair as alt
    import polars as pl
    from asimpy import Environment, Process

    N_DRIVERS = 4000
    CAPACITY = 100.0
    CONST_DELAY = 45.0
    BETA = 0.5
    N_ROUNDS = 80
    SEED = 42
    return (
        BETA, CAPACITY, CONST_DELAY, Environment, N_DRIVERS, N_ROUNDS,
        Process, SEED, alt, math, pl, random,
    )


@app.cell
def _(BETA, CAPACITY, CONST_DELAY, Environment, N_DRIVERS, N_ROUNDS, Process, SEED, math, random):
    def route_times(n_top, n_bot, n_short):
        n_sa = n_top + n_short
        n_bt = n_bot + n_short
        t_top = n_sa / CAPACITY + CONST_DELAY
        t_bot = CONST_DELAY + n_bt / CAPACITY
        t_short = n_sa / CAPACITY + n_bt / CAPACITY
        return t_top, t_bot, t_short

    def logit_split(times):
        vals = [math.exp(-BETA * t) for t in times]
        total = sum(vals)
        return [v / total for v in vals]

    class RoutingGame(Process):
        def init(self, has_shortcut, history):
            self.has_shortcut = has_shortcut
            self.history = history
            self._n_top = N_DRIVERS // 2
            self._n_bot = N_DRIVERS - N_DRIVERS // 2
            self._n_short = 0

        async def run(self):
            for _ in range(N_ROUNDS):
                await self.timeout(1.0)
                t_top, t_bot, t_short = route_times(self._n_top, self._n_bot, self._n_short)
                if self.has_shortcut:
                    probs = logit_split([t_top, t_bot, t_short])
                    self._n_top = round(N_DRIVERS * probs[0])
                    self._n_bot = round(N_DRIVERS * probs[1])
                    self._n_short = N_DRIVERS - self._n_top - self._n_bot
                else:
                    probs = logit_split([t_top, t_bot])
                    self._n_top = round(N_DRIVERS * probs[0])
                    self._n_bot = N_DRIVERS - self._n_top
                    self._n_short = 0
                t_top2, t_bot2, t_short2 = route_times(self._n_top, self._n_bot, self._n_short)
                mean_t = (
                    self._n_top * t_top2 + self._n_bot * t_bot2 + self._n_short * t_short2
                ) / N_DRIVERS
                self.history.append({
                    "round": self.now,
                    "n_top": self._n_top,
                    "n_bot": self._n_bot,
                    "n_short": self._n_short,
                    "t_top": t_top2,
                    "t_bot": t_bot2,
                    "t_short": t_short2,
                    "mean": mean_t,
                })

    def simulate(has_shortcut):
        random.seed(SEED)
        history = []
        env = Environment()
        RoutingGame(env, has_shortcut, history)
        env.run()
        return history

    return (simulate,)


@app.cell
def _(N_DRIVERS, CAPACITY, CONST_DELAY, pl, simulate):
    hist_no = simulate(has_shortcut=False)
    hist_yes = simulate(has_shortcut=True)
    df_no = pl.DataFrame(hist_no)
    df_yes = pl.DataFrame(hist_yes)
    eq_no = hist_no[-1]["mean"]
    eq_yes = hist_yes[-1]["mean"]
    n_half = N_DRIVERS / 2
    t_theory_no = n_half / CAPACITY + CONST_DELAY
    t_theory_yes = N_DRIVERS / CAPACITY + N_DRIVERS / CAPACITY
    return df_no, df_yes, eq_no, eq_yes, t_theory_no, t_theory_yes


@app.cell(hide_code=True)
def _(mo):
    mo.md("## Without Shortcut")
    return


@app.cell
def _(df_no):
    df_no


@app.cell(hide_code=True)
def _(mo):
    mo.md("## With Shortcut")
    return


@app.cell
def _(df_yes):
    df_yes


@app.cell(hide_code=True)
def _(N_DRIVERS, CAPACITY, CONST_DELAY, eq_no, eq_yes, mo, t_theory_no, t_theory_yes):
    mo.md(f"""
    ## Results

    - Nash equilibrium **without** shortcut: **{eq_no:.2f}**
    - Nash equilibrium **with** shortcut: **{eq_yes:.2f}**
    - Adding the shortcut increased travel time by **{eq_yes - eq_no:.2f}** units
      ({100 * (eq_yes / eq_no - 1):.1f}% worse for every driver)

    Theory without shortcut (50/50 split): {t_theory_no:.2f}
    Theory with shortcut (all on SA→AB→BT): {t_theory_yes:.2f}

    Parameters: {N_DRIVERS} drivers, capacity={CAPACITY:.0f}, constant delay={CONST_DELAY}
    """)
    return


@app.cell
def _(alt, df_no, df_yes, pl):
    df_no_plot = df_no.select(["round", "mean"]).with_columns(
        pl.lit("without shortcut").alias("scenario")
    )
    df_yes_plot = df_yes.select(["round", "mean"]).with_columns(
        pl.lit("with shortcut").alias("scenario")
    )
    df_plot = pl.concat([df_no_plot, df_yes_plot])
    chart = (
        alt.Chart(df_plot)
        .mark_line()
        .encode(
            x=alt.X("round:Q", title="Round"),
            y=alt.Y("mean:Q", title="Mean travel time"),
            color=alt.Color("scenario:N", title="Network"),
            tooltip=["round:Q", "scenario:N", "mean:Q"],
        )
        .properties(title="Braess's Paradox: Convergence to Nash Equilibrium")
    )
    chart
    return (chart,)


if __name__ == "__main__":
    app.run()
