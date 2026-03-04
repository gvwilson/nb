import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import random

    import altair as alt
    import polars as pl

    from asimpy import Environment, Process, Resource

    return Environment, Process, Resource, alt, mo, pl, random


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Server Utilization

    ## *The Most Important Number in Queueing Theory*

    The previous scenario introduced exponential arrival times and Poisson processes. This one introduces the other half of a queue: the server that does the work. To start, we also model service times as exponentially distributed with rate $\mu$ (mu), meaning that on average the server completes $\mu$ jobs per unit time, with a mean service time of $1/\mu$.

    With arrivals at rate $\lambda$ and service at rate $\mu$, we can define the *utilization* of the server as

    $$\rho = \frac{\lambda}{\mu}$$

    ## What Utilization Means

    The fraction of time the server is busy converges to $\rho$ in the long run, regardless of the variability of service times, which means that the server is idle $1 - \rho$ of the time.

    | Target $\rho$ | Busy fraction | Idle fraction |
    |:---:|:---:|:---:|
    | 0.50 | ≈ 0.50 | ≈ 0.50 |
    | 0.80 | ≈ 0.80 | ≈ 0.20 |
    | 0.95 | ≈ 0.95 | ≈ 0.05 |

    This seems obvious, but the implication is striking: a server running at $\rho = 0.95$ is idle only 5% of the time, yet customers still wait a significant amount of time.

    ### The Stability Condition

    The system is *stable* only when $\rho < 1$. When $\rho \geq 1$, arrivals come at least as fast as the server can handle them. The queue grows without bound: every customer waits longer than the last.

    When $\rho = 1$ (arrival rate exactly equals service rate), you might expect the server to keep up, but it can't. Randomness in both arrivals and service creates occasional bursts that the server falls behind on, and with no slack capacity to recover, the backlog accumulates forever.

    ### Why This Matters

    Utilization is the most important thing to calculate for any real system. A web server handling 800 requests per second with a mean response time of 1 ms has utilization $\rho = 800 \times 0.001 = 0.8$, leaving 20% slack. A printer that handles 50 jobs per hour but receives 55 jobs per hour has $\rho = 55/50 = 1.1 > 1$, and will fall further and further behind over time.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Simulation

    The `Customer` process acquires the shared `Resource`, randomly chooses an exponential service time, and accumulates it in a shared `total_service` list. `Arrivals` generates customers with Poisson inter-arrival gaps. After the simulation, the busy fraction is `total_service[0] / SIM_TIME`. The simulation sweeps $\rho$ from 0.1 to 0.95, confirming each time that the observed busy fraction matches the target $\lambda/\mu$.
    """)
    return


@app.cell
def _(mo):
    sim_time_slider = mo.ui.slider(
        start=0,
        stop=100_000,
        step=1_000,
        value=100_000,
        label="Simulation time",
    )

    service_rate_slider = mo.ui.slider(
        start=1.0,
        stop=5.0,
        step=0.01,
        value=2.0,
        label="Service rate",
    )

    seed_input = mo.ui.number(
        value=192_837_465,
        step=1,
        label="Random seed",
    )

    run_button = mo.ui.button(label="Run simulation")

    mo.vstack([
        sim_time_slider,
        service_rate_slider,
        seed_input,
        run_button,
    ])
    return seed_input, service_rate_slider, sim_time_slider


@app.cell
def _(seed_input, service_rate_slider, sim_time_slider):
    SIM_TIME = int(sim_time_slider.value)
    SERVICE_RATE = float(service_rate_slider.value)
    SEED = int(seed_input.value)
    return SEED, SERVICE_RATE, SIM_TIME


@app.cell
def _(Process, SERVICE_RATE, random):
    class Customer(Process):
        def init(self, server, total_service):
            self.server = server
            self.total_service = total_service

        async def run(self):
            async with self.server:
                svc = random.expovariate(SERVICE_RATE)
                await self.timeout(svc)
                self.total_service[0] += svc

    return (Customer,)


@app.cell
def _(Customer, Process, random):
    class Arrivals(Process):
        def init(self, rate, server, total_service):
            self.rate = rate
            self.server = server
            self.total_service = total_service

        async def run(self):
            while True:
                await self.timeout(random.expovariate(self.rate))
                Customer(self._env, self.server, self.total_service)

    return (Arrivals,)


@app.cell
def _(Arrivals, Environment, Resource, SERVICE_RATE, SIM_TIME):
    def simulate(rho):
        arrival_rate = rho * SERVICE_RATE
        env = Environment()
        server = Resource(env, capacity=1)
        total_service = [0.0]
        Arrivals(env, arrival_rate, server, total_service)
        env.run(until=SIM_TIME)
        busy_frac = total_service[0] / SIM_TIME
        return {
            "rho_target": rho,
            "rho_observed": round(busy_frac, 4),
            "idle_frac": round(1.0 - busy_frac, 4),
        }

    return (simulate,)


@app.cell
def _(SEED, pl, random, simulate):
    random.seed(SEED)
    rows = [simulate(rho) for rho in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95]]
    df_sim = pl.DataFrame(rows)
    df_sim
    return (df_sim,)


@app.cell
def _(alt, df_sim):
    def make_chart(df):
        df_plot = df.unpivot(
            on=["rho_observed", "idle_frac"],
            index="rho_target",
            variable_name="metric",
            value_name="fraction",
        )
        return (
            alt.Chart(df_plot)
            .mark_line(point=True)
            .encode(
                x=alt.X("rho_target:Q", title="Target utilization (ρ = λ/μ)"),
                y=alt.Y("fraction:Q", title="Fraction of time"),
                color=alt.Color("metric:N", title="Metric"),
                tooltip=["rho_target:Q", "metric:N", "fraction:Q"],
            )
            .properties(title="Server Utilization: Busy and Idle Fractions vs. ρ")
        )
    make_chart(df_sim)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Understanding the Math

    ### Why does the long-run busy fraction equal $\rho$?

    Suppose the simulation runs for a long time $T$ and $N$ customers are served. By definition, $\lambda \approx N/T$ (arrivals per unit time), so $N \approx \lambda T$. Each customer occupies the server for an average of $1/\mu$ time units. The total service time is approximately $N/\mu = \lambda T / \mu = \rho T$.  Dividing by $T$ gives:

    $$\text{fraction busy} = \frac{\rho T}{T} = \rho$$

    ### What does $\rho < 1$ mean geometrically?

    Think of a bank account.  Each arriving job makes a "deposit" of work (service time) into the server's backlog.  Each unit of clock time makes a "withdrawal" of $\mu$ units of work (service capacity).  When $\lambda/\mu < 1$, withdrawals outpace deposits in the long run and the balance (queue length) stays bounded.  When $\lambda/\mu \geq 1$, deposits outpace withdrawals and the balance grows without limit.

    ### The exponential service time and its coefficient of variation

    Recall from the arrival process scenario that the exponential distribution has mean equal to standard deviation.  Its *coefficient of variation* is its standard deviation divided by mean, and is therefore $\text{CV} = 1$.  A deterministic server (every job takes exactly $1/\mu$) has CV = 0.  A highly variable server (some jobs very short, some very long) has CV $> 1$.  The CV of service times matters enormously for queue length, as later lessons will show.

    ### Why randomness prevents $\rho = 1$ from being stable

    Suppose $\rho = 1$. Gaps between arrivals and service times are both exponential with the same mean.  The queue length after each service completion performs a random walk: it goes up by 1 when a new arrival joins while the server is busy, and down by 1 when service finishes.  A symmetric random walk (equal probability of going up or down) is known from probability theory to be null-recurrent: it returns to zero, but the expected return time is infinite.  This means the expected queue length is infinite even at exact balance.

    ### A rule of thumb

    Engineers routinely target $\rho \leq 0.7$–$0.8$ for interactive systems, because queue length and wait time grow sharply as $\rho$ approaches 1 — a fact the next two scenarios quantify precisely.
    """)
    return


if __name__ == "__main__":
    app.run()
