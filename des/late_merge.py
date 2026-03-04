"""Late Merge (Zipper Merge): using both lanes until the pinch point beats early merging."""

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
    # Late Merge (Zipper Merge)

    Using both lanes until the pinch point beats early merging.

    **Key insight:** "polite" early merging halves the available pre-merge buffer,
    causing more cars to be turned away and reducing throughput.
    """)
    return


@app.cell
def _():
    import random
    import altair as alt
    import polars as pl
    from asimpy import Environment, Event, Process, Queue

    ARRIVAL_RATE = 1.85
    MERGE_RATE = 2.0
    LANE_CAPACITY = 10
    SIM_TIME = 30_000
    SEED = 42
    RHO = ARRIVAL_RATE / MERGE_RATE
    return (
        ARRIVAL_RATE, Environment, Event, LANE_CAPACITY, MERGE_RATE,
        Process, Queue, RHO, SEED, SIM_TIME, alt, pl, random,
    )


@app.cell
def _(ARRIVAL_RATE, Environment, Event, MERGE_RATE, Process, Queue, SEED, SIM_TIME, random):
    def run_scenario(zipper, k, seed=SEED):
        random.seed(seed)
        env = Environment()
        sojourn_times = []
        blocked = []

        class EarlyMergeCar(Process):
            def init(self, lane, sojourn_times, blocked):
                self.lane = lane
                self.sojourn_times = sojourn_times
                self.blocked = blocked

            async def run(self):
                arrival = self.now
                if self.lane.is_full():
                    self.blocked.append(1)
                    return
                done = Event(self._env)
                await self.lane.put((arrival, done))
                await done
                self.sojourn_times.append(self.now - arrival)

        class LateMergeCar(Process):
            def init(self, lane1, lane2, sojourn_times, blocked):
                self.lane1 = lane1
                self.lane2 = lane2
                self.sojourn_times = sojourn_times
                self.blocked = blocked

            async def run(self):
                arrival = self.now
                target = (
                    self.lane1
                    if len(self.lane1._items) <= len(self.lane2._items)
                    else self.lane2
                )
                if target.is_full():
                    self.blocked.append(1)
                    return
                done = Event(self._env)
                await target.put((arrival, done))
                await done
                self.sojourn_times.append(self.now - arrival)

        class MergeServer(Process):
            def init(self, lanes, zipper):
                self.lanes = lanes
                self.zipper = zipper
                self._turn = 0

            async def run(self):
                while True:
                    if self.zipper:
                        served = False
                        for _ in range(len(self.lanes)):
                            idx = self._turn % len(self.lanes)
                            self._turn += 1
                            if not self.lanes[idx].is_empty():
                                _, arrival, done = (self.now,) + (await self.lanes[idx].get())
                                await self.timeout(random.expovariate(MERGE_RATE))
                                done.succeed()
                                served = True
                                break
                        if not served:
                            await self.timeout(0.05)
                    else:
                        _, arrival, done = (self.now,) + (await self.lanes[0].get())
                        await self.timeout(random.expovariate(MERGE_RATE))
                        done.succeed()

        class ArrivalStream(Process):
            def init(self, lanes, sojourn_times, blocked, zipper):
                self.lanes = lanes
                self.sojourn_times = sojourn_times
                self.blocked = blocked
                self.zipper = zipper

            async def run(self):
                while True:
                    await self.timeout(random.expovariate(ARRIVAL_RATE))
                    if self.zipper:
                        LateMergeCar(self._env, self.lanes[0], self.lanes[1], self.sojourn_times, self.blocked)
                    else:
                        EarlyMergeCar(self._env, self.lanes[0], self.sojourn_times, self.blocked)

        if zipper:
            lanes = [Queue(env, max_capacity=k), Queue(env, max_capacity=k)]
        else:
            lanes = [Queue(env, max_capacity=k)]
        ArrivalStream(env, lanes, sojourn_times, blocked, zipper)
        MergeServer(env, lanes, zipper)
        env.run(until=SIM_TIME)
        total = len(sojourn_times) + len(blocked)
        blocked_pct = 100.0 * len(blocked) / total if total else 0.0
        throughput = len(sojourn_times) / SIM_TIME
        mean_sojourn = sum(sojourn_times) / len(sojourn_times) if sojourn_times else 0.0
        return {
            "throughput": throughput,
            "blocked_pct": blocked_pct,
            "mean_sojourn": mean_sojourn,
            "total_buffer": k * (2 if zipper else 1),
        }

    return (run_scenario,)


@app.cell
def _(LANE_CAPACITY, pl, run_scenario):
    early = run_scenario(zipper=False, k=LANE_CAPACITY)
    late = run_scenario(zipper=True, k=LANE_CAPACITY)
    df_main = pl.DataFrame([
        {"strategy": "early", **early},
        {"strategy": "late", **late},
    ])

    sweep_rows = []
    for _k in [5, 10, 15, 20, 30]:
        ep = run_scenario(zipper=False, k=_k)["blocked_pct"]
        lp = run_scenario(zipper=True, k=_k)["blocked_pct"]
        sweep_rows.append({"buffer_k": _k, "early_blocked_pct": ep, "late_blocked_pct": lp})
    df_sweep = pl.DataFrame(sweep_rows)
    return df_main, df_sweep, early, late


@app.cell(hide_code=True)
def _(ARRIVAL_RATE, MERGE_RATE, RHO, mo):
    mo.md(f"""
    ## Main Results

    Arrival rate: {ARRIVAL_RATE}/unit, merge service rate: {MERGE_RATE}/unit,
    utilisation ρ = {RHO:.3f}
    """)
    return


@app.cell
def _(df_main):
    df_main


@app.cell(hide_code=True)
def _(mo):
    mo.md("## Effect of Buffer Size on Blocking Rate")
    return


@app.cell
def _(df_sweep):
    df_sweep


@app.cell
def _(alt, df_sweep, pl):
    df_plot = df_sweep.unpivot(
        on=["early_blocked_pct", "late_blocked_pct"],
        index="buffer_k",
        variable_name="strategy",
        value_name="blocked_pct",
    )
    chart = (
        alt.Chart(df_plot)
        .mark_line(point=True)
        .encode(
            x=alt.X("buffer_k:Q", title="Buffer size per lane (K)"),
            y=alt.Y("blocked_pct:Q", title="Blocked cars (%)"),
            color=alt.Color("strategy:N", title="Merge strategy"),
            tooltip=["buffer_k:Q", "strategy:N", "blocked_pct:Q"],
        )
        .properties(title="Late Merge: Blocked Cars vs. Buffer Size")
    )
    chart
    return (chart,)


if __name__ == "__main__":
    app.run()
