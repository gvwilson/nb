"""Priority Starvation: high-priority load can cause low-priority jobs to wait forever."""

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
    # Priority Starvation

    High-priority load can cause low-priority jobs to wait forever.

    Demonstrates two effects:
    1. **Static priority**: as hi-priority utilization grows, lo-priority waits diverge.
    2. **Aging**: the server promotes a lo-priority job once it has waited long enough,
       preventing starvation at the cost of occasional hi-priority delay bursts.
    """)
    return


@app.cell
def _():
    import random
    import statistics
    import altair as alt
    import polars as pl
    from asimpy import Environment, Process, Queue

    SIM_TIME = 30_000
    SERVICE_RATE_HI = 2.0
    SERVICE_RATE_LO = 1.0
    ARRIVAL_RATE_LO = 0.2
    AGING_THRESHOLD = 15.0
    SEED = 42
    return (
        AGING_THRESHOLD, ARRIVAL_RATE_LO, Environment, Process,
        Queue, SEED, SERVICE_RATE_HI, SERVICE_RATE_LO, SIM_TIME,
        alt, pl, random, statistics,
    )


@app.cell
def _(AGING_THRESHOLD, ARRIVAL_RATE_LO, Environment, Process, Queue, SEED, SERVICE_RATE_HI, SERVICE_RATE_LO, SIM_TIME, random, statistics):
    class StaticPriorityServer(Process):
        def init(self, hi_q, lo_q, sojourn_hi, sojourn_lo):
            self.hi_q = hi_q
            self.lo_q = lo_q
            self.sojourn_hi = sojourn_hi
            self.sojourn_lo = sojourn_lo

        async def _serve(self, arrival, svc, record):
            await self.timeout(svc)
            record.append(self.now - arrival)

        async def run(self):
            while True:
                if not self.hi_q.is_empty():
                    arrival, svc = await self.hi_q.get()
                    await self._serve(arrival, svc, self.sojourn_hi)
                elif not self.lo_q.is_empty():
                    arrival, svc = await self.lo_q.get()
                    await self._serve(arrival, svc, self.sojourn_lo)
                else:
                    await self.timeout(0.01)

    class AgingServer(Process):
        def init(self, hi_q, lo_q, sojourn_hi, sojourn_lo):
            self.hi_q = hi_q
            self.lo_q = lo_q
            self.sojourn_hi = sojourn_hi
            self.sojourn_lo = sojourn_lo

        async def run(self):
            while True:
                lo_aged = (
                    not self.lo_q.is_empty()
                    and self.now - self.lo_q._items[0][0] >= AGING_THRESHOLD
                )
                if lo_aged:
                    arrival, svc = await self.lo_q.get()
                    await self.timeout(svc)
                    self.sojourn_lo.append(self.now - arrival)
                elif not self.hi_q.is_empty():
                    arrival, svc = await self.hi_q.get()
                    await self.timeout(svc)
                    self.sojourn_hi.append(self.now - arrival)
                elif not self.lo_q.is_empty():
                    arrival, svc = await self.lo_q.get()
                    await self.timeout(svc)
                    self.sojourn_lo.append(self.now - arrival)
                else:
                    await self.timeout(0.01)

    class HiSource(Process):
        def init(self, rate, q):
            self.rate = rate
            self.q = q

        async def run(self):
            while True:
                await self.timeout(random.expovariate(self.rate))
                svc = random.expovariate(SERVICE_RATE_HI)
                await self.q.put((self.now, svc))

    class LoSource(Process):
        def init(self, q):
            self.q = q

        async def run(self):
            while True:
                await self.timeout(random.expovariate(ARRIVAL_RATE_LO))
                svc = random.expovariate(SERVICE_RATE_LO)
                await self.q.put((self.now, svc))

    def simulate(arrival_rate_hi, use_aging, seed=SEED):
        random.seed(seed)
        env = Environment()
        hi_q = Queue(env)
        lo_q = Queue(env)
        sojourn_hi = []
        sojourn_lo = []
        HiSource(env, arrival_rate_hi, hi_q)
        LoSource(env, lo_q)
        if use_aging:
            AgingServer(env, hi_q, lo_q, sojourn_hi, sojourn_lo)
        else:
            StaticPriorityServer(env, hi_q, lo_q, sojourn_hi, sojourn_lo)
        env.run(until=SIM_TIME)
        return sojourn_hi, sojourn_lo

    def mean_or_none(lst):
        return statistics.mean(lst) if lst else None

    def pct_or_none(lst, p):
        if not lst:
            return None
        return sorted(lst)[int(p * len(lst))]

    return (mean_or_none, pct_or_none, simulate)


@app.cell
def _(ARRIVAL_RATE_LO, SERVICE_RATE_HI, SERVICE_RATE_LO, mean_or_none, pl, simulate):
    sweep_rows = []
    for rho_hi in [0.10, 0.20, 0.40, 0.60, 0.70, 0.80]:
        rate_hi = rho_hi * SERVICE_RATE_HI
        hi, lo = simulate(rate_hi, use_aging=False)
        rho_total = rho_hi + ARRIVAL_RATE_LO / SERVICE_RATE_LO
        sweep_rows.append({
            "rho_hi": rho_hi,
            "rho_total": rho_total,
            "mean_W_hi": mean_or_none(hi),
            "mean_W_lo": mean_or_none(lo),
        })
    df_sweep = pl.DataFrame(sweep_rows)
    return df_sweep, rho_hi, sweep_rows


@app.cell
def _(ARRIVAL_RATE_LO, SERVICE_RATE_HI, SERVICE_RATE_LO, mean_or_none, pl, pct_or_none, simulate):
    FIXED_RHO_HI = 0.70
    _rate_hi = FIXED_RHO_HI * SERVICE_RATE_HI
    rho_total = FIXED_RHO_HI + ARRIVAL_RATE_LO / SERVICE_RATE_LO

    hi_static, lo_static = simulate(_rate_hi, use_aging=False)
    hi_aging, lo_aging = simulate(_rate_hi, use_aging=True)

    compare_rows = [
        {
            "policy": "static", "class": "hi", "n": len(hi_static),
            "mean_W": mean_or_none(hi_static),
            "p95": pct_or_none(hi_static, 0.95),
            "p99": pct_or_none(hi_static, 0.99),
        },
        {
            "policy": "static", "class": "lo", "n": len(lo_static),
            "mean_W": mean_or_none(lo_static),
            "p95": pct_or_none(lo_static, 0.95),
            "p99": pct_or_none(lo_static, 0.99),
        },
        {
            "policy": "aging", "class": "hi", "n": len(hi_aging),
            "mean_W": mean_or_none(hi_aging),
            "p95": pct_or_none(hi_aging, 0.95),
            "p99": pct_or_none(hi_aging, 0.99),
        },
        {
            "policy": "aging", "class": "lo", "n": len(lo_aging),
            "mean_W": mean_or_none(lo_aging),
            "p95": pct_or_none(lo_aging, 0.95),
            "p99": pct_or_none(lo_aging, 0.99),
        },
    ]
    df_compare = pl.DataFrame(compare_rows)
    return FIXED_RHO_HI, df_compare, rho_total


@app.cell(hide_code=True)
def _(AGING_THRESHOLD, ARRIVAL_RATE_LO, FIXED_RHO_HI, SERVICE_RATE_LO, mo, rho_total):
    mo.md(f"""
    ## Part 1 — Static Priority: Effect of Hi-Priority Load on Lo-Priority Wait

    Lo-priority: arrival rate {ARRIVAL_RATE_LO}, mean service {1 / SERVICE_RATE_LO:.1f},
    ρ_lo = {ARRIVAL_RATE_LO / SERVICE_RATE_LO:.2f}

    Aging threshold: {AGING_THRESHOLD} time units
    """)
    return


@app.cell
def _(df_sweep):
    df_sweep


@app.cell(hide_code=True)
def _(FIXED_RHO_HI, mo, rho_total):
    mo.md(f"## Part 2 — Static vs. Aging at ρ_hi = {FIXED_RHO_HI:.2f}, ρ_total = {rho_total:.2f}")
    return


@app.cell
def _(df_compare):
    df_compare


@app.cell
def _(alt, df_compare, df_sweep, pl):
    df_plot = df_sweep.unpivot(
        on=["mean_W_hi", "mean_W_lo"],
        index=["rho_hi", "rho_total"],
        variable_name="job_class",
        value_name="mean_W",
    )
    sweep_chart = (
        alt.Chart(df_plot)
        .mark_line(point=True)
        .encode(
            x=alt.X("rho_hi:Q", title="Hi-priority utilization (ρ_hi)"),
            y=alt.Y("mean_W:Q", title="Mean sojourn time (W)"),
            color=alt.Color("job_class:N", title="Job class"),
            tooltip=["rho_hi:Q", "job_class:N", "mean_W:Q"],
        )
        .properties(title="Priority Starvation: Effect of Hi-Priority Load")
    )
    compare_chart = (
        alt.Chart(df_compare)
        .mark_bar()
        .encode(
            x=alt.X("class:N", title="Job class"),
            y=alt.Y("mean_W:Q", title="Mean sojourn time (W)"),
            color=alt.Color("policy:N", title="Policy"),
            xOffset="policy:N",
            tooltip=["policy:N", "class:N", "mean_W:Q", "p99:Q"],
        )
        .properties(title="Static Priority vs. Aging")
    )
    (sweep_chart | compare_chart)
    return (compare_chart, sweep_chart)


if __name__ == "__main__":
    app.run()
