import marimo

__generated_with = "0.20.4"
app = marimo.App()


@app.cell
def _():
    return


@app.cell
def _():
    import marimo as mo
    import math
    import random
    import statistics

    import altair as alt
    import polars as pl

    from asimpy import Environment, Process

    return Environment, Process, alt, math, mo, pl, random, statistics


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Arrival Process

    ## *The Foundation of Queueing Theory*

    In order to understand queues, we need to understand how customers arrive. This tutorial asks a simple question: if customers arrive at random, i.e., no one coordinates with anyone else, and past events do not influence future ones, what pattern do those arrivals follow?

    The answer is the *Poisson process*, named after the French mathematician Siméon Denis Poisson.  It is parameterized by a single number $\lambda$ (lambda), called the *arrival rate*, which is the number of arrivals per unit time.

    The Poisson process has two equivalent descriptions:

    1. Gaps are exponentially distributed: the time between consecutive arrivals follows an exponential distribution with mean $1/\lambda$.
    2. Counts are Poisson-distributed: the number of arrivals in any window of width $t$ follows a Poisson distribution with mean $\lambda t$.

    These are not separate: if one holds, the other must hold automatically.

    ### The Exponential Distribution of Gaps

    If $X$ is the time until the next arrival, then:

    $$P(X > t) = e^{-\lambda t}$$

    The mean gap is $E[X] = 1/\lambda$ and the standard deviation is $\text{SD}[X] = 1/\lambda$.  The mean equaling the standard deviation is the defining property of the exponential distribution.

    A consequence of this is that the distribution is *memoryless*.  If you have already waited $s$ units for the next arrival, the remaining wait is still exponentially distributed with the same mean $1/\lambda$:

    $$P(X > s + t \mid X > s) = P(X > t)$$

    This means that the next arrival is never overdue; knowing that you have already waited a long time gives no information about when the next arrival will come.

    ## The Poisson Distribution of Counts

    If $K$ is the number of arrivals in a time window of duration $t$, then:

    $$P(K = k) = \frac{(\lambda t)^k \, e^{-\lambda t}}{k!}$$

    The mean and variance of $K$ are both equal to $\lambda t$.  Again, this is a direct consequence of the distribution being memoryless.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## When Is the This Model Appropriate?

    The Poisson process is a good model when:

    - Arrivals are independent: one customer's arrival does not influence another's.
    - The rate $\lambda$ is constant over the period of interest.
    - Simultaneous arrivals are essentially impossible.

    It fits customer arrivals at a supermarket during a quiet period, but is a poor fit when people arrive in groups (e.g., fans leaving a stadium), or on a fixed schedule (e.g., hourly buses).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Simulation

    Our simulation uses [asimpy](https://asimpy.readthedocs.io/), a discrete event simulation framework written in Python. An `ArrivalSource` process generates arrivals by drawing each inter-arrival gap from `random.expovariate(rate)`, then advancing the simulation clock by that gap.

    After the run, window counts are tallied by dividing the time axis into non-overlapping intervals of the same width and counting how many recorded arrivals land in each.  The observed distribution is compared against the theoretical Poisson probabilities computed directly from the formula.
    """)
    return


@app.cell
def _(mo):
    sim_time_slider = mo.ui.slider(
        start=0,
        stop=200_000,
        step=1_000,
        value=200_000,
        label="Simulation time",
    )

    arrival_rate_slider = mo.ui.slider(
        start=1.0,
        stop=5.0,
        step=0.01,
        value=2.0,
        label="Arrival rate",
    )

    window_slider = mo.ui.slider(
        start=1.0,
        stop=5.0,
        step=0.01,
        value=1.0,
        label="Counting window",
    )

    seed_input = mo.ui.number(
        value=192_837_465,
        step=1,
        label="Random seed",
    )

    run_button = mo.ui.button(label="Run simulation")

    mo.vstack([
        sim_time_slider,
        arrival_rate_slider,
        window_slider,
        seed_input,
        run_button,
    ])
    return arrival_rate_slider, seed_input, sim_time_slider, window_slider


@app.cell
def _(arrival_rate_slider, seed_input, sim_time_slider, window_slider):
    SIM_TIME = int(sim_time_slider.value)
    ARRIVAL_RATE = float(arrival_rate_slider.value)
    WINDOW = float(window_slider.value)
    SEED = int(seed_input.value)
    return ARRIVAL_RATE, SIM_TIME, WINDOW


@app.cell
def _(Process, random):
    class ArrivalSource(Process):
        """Generates arrivals at a Poisson rate and records inter-arrival gaps."""

        def init(self, rate, gaps):
            self.rate = rate
            self.gaps = gaps

        async def run(self):
            while True:
                gap = random.expovariate(self.rate)
                await self.timeout(gap)
                self.gaps.append(gap)

    return (ArrivalSource,)


@app.cell
def _(ARRIVAL_RATE, ArrivalSource, Environment, SIM_TIME):
    def simulate():
        gaps = []
        env = Environment()
        ArrivalSource(env, ARRIVAL_RATE, gaps)
        env.run(until=SIM_TIME)
        return gaps

    return (simulate,)


@app.cell
def _(ARRIVAL_RATE, pl, statistics):
    def summarize(gaps):
        mean_gap = statistics.mean(gaps)
        stdev_gap = statistics.stdev(gaps)
        return pl.DataFrame(
            [
                {"quantity": "target λ", "value": ARRIVAL_RATE},
                {"quantity": "measured λ (1/mean)", "value": round(1.0 / mean_gap, 5)},
                {"quantity": "mean inter-arrival", "value": round(mean_gap, 5)},
                {"quantity": "theory mean (1/λ)", "value": round(1.0 / ARRIVAL_RATE, 5)},
                {"quantity": "stdev inter-arrival", "value": round(stdev_gap, 5)},
                {"quantity": "theory stdev (1/λ)", "value": round(1.0 / ARRIVAL_RATE, 5)},
            ]
        )

    return (summarize,)


@app.cell
def _(ARRIVAL_RATE, SIM_TIME, WINDOW, math, pl):
    def empirical(gaps):
        n_windows = int(SIM_TIME / WINDOW)
        window_counts = [0] * n_windows
        t = 0.0
        for g in gaps:
            t += g
            w = int(t / WINDOW)
            if w < n_windows:
                window_counts[w] += 1
    
        max_k = max(window_counts)
        freq = {}
        for c in window_counts:
            freq[c] = freq.get(c, 0) + 1
    
        lam_w = ARRIVAL_RATE * WINDOW  # expected count per window
        dist_rows = []
        for k in range(max_k + 1):
            observed = freq.get(k, 0) / n_windows
            theory = (lam_w**k) * math.exp(-lam_w) / math.factorial(k)
            dist_rows.append(
                {"k": k, "observed": round(observed, 5), "theory": round(theory, 5)}
            )
    
        return pl.DataFrame(dist_rows)

    return (empirical,)


@app.cell
def _(simulate, summarize):
    gaps = simulate()
    summarize(gaps)
    return (gaps,)


@app.cell
def _(ARRIVAL_RATE, WINDOW, alt, empirical, gaps):
    df_plot = empirical(gaps).unpivot(
        on=["observed", "theory"],
        index="k",
        variable_name="source",
        value_name="probability",
    )
    chart = (
        alt.Chart(df_plot)
        .mark_bar(opacity=0.8)
        .encode(
            x=alt.X("k:O", title=f"Arrivals per window (width {WINDOW})"),
            y=alt.Y("probability:Q", title="Probability"),
            color=alt.Color("source:N", title="Series"),
            xOffset="source:N",
            tooltip=["k:O", "source:N", "probability:Q"],
        )
        .properties(title=f"Arrival Counts: Observed vs. Poisson(λ={ARRIVAL_RATE})")
    )
    chart
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Understanding the Math

    ### Where does $e^{-\lambda t}$ come from?

    Imagine dividing the interval $[0, t]$ into $n$ tiny slices of width $\Delta = t/n$.  The probability of an arrival in each slice is approximately $\lambda \Delta = \lambda t/n$ (arrival rate times slice width), and slices are independent. The probability of zero arrivals in all $n$ slices is approximately $(1 - \lambda t / n)^n$.  From introductory calculus you know that $\lim_{n \to \infty}(1 - x/n)^n = e^{-x}$, so the probability of no arrival in $[0,t]$ is $e^{-\lambda t}$.  This is exactly $P(X > t)$.

    ### Where does the factorial $k!$ come from?

    $P(K = k)$ is the probability of exactly $k$ arrivals and zero arrivals in the remaining time. The $k!$ in the denominator corrects for the fact that the $k$ arrivals are indistinguishable, i.e., we do not care about the order in which they occur, only that there are exactly $k$ of them. This is the same factorial that appears in the binomial coefficient $\binom{n}{k} = n!/(k!(n-k)!)$.

    ### Why does mean equal standard deviation for the exponential?

    The mean of $X \sim \text{Exp}(\lambda)$ requires integration by parts:

    $$E[X] = \int_0^\infty t \cdot \lambda e^{-\lambda t}\, dt = \frac{1}{\lambda}$$

    The second moment $E[X^2] = 2/\lambda^2$, so $\text{Var}(X) = E[X^2] - (E[X])^2 = 2/\lambda^2 - 1/\lambda^2 = 1/\lambda^2$, giving $\text{SD}(X) = 1/\lambda = E[X]$.  Equal mean and standard deviation means the distribution is highly variable: roughly one-third of gaps are longer than the mean.

    ### Why does mean equal variance for the Poisson?

    The count $K$ in a window is the sum of $n$ independent Bernoulli trials (one per slice), each with success probability $p = \lambda t / n$.  A Bernoulli trial has mean $p$ and variance $p(1-p)$.  Summing $n$ independent trials gives mean $np = \lambda t$ and variance $np(1-p) \approx np = \lambda t$ as $n \to \infty$ and $p \to 0$, so the mean and variance both equal $\lambda t$.

    ### What the simulation confirms.

    Running the simulation with $\lambda = 2$ and windows of width 1 should give an observed count distribution very close to Poisson(2): mostly 2 arrivals per window, rarely 0 or more than 5. The measured $1/\lambda$ from the gap data should also match 0.5, and the standard deviation of gaps should equal the mean.
    """)
    return


if __name__ == "__main__":
    app.run()
