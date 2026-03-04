"""Rush Hour Displacement: individual avoidance of congestion shifts but never ends it."""

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
    # Rush Hour Displacement

    Individual avoidance of congestion shifts but never ends it.

    When commuters independently try to avoid congestion by shifting their departure time,
    the peak moves rather than disappears — a classic tragedy of the commons.
    """)
    return


@app.cell
def _():
    import random
    import statistics
    import altair as alt
    import polars as pl

    N_COMMUTERS = 200
    N_SLOTS = 30
    PREFERRED_SLOT = 15
    ROAD_CAPACITY = 20
    OVERLOAD_DELAY = 3.0
    BASE_DELAY = 1.0
    N_DAYS = 40
    SHIFT_PROB = 0.3
    SEED = 42
    return (
        BASE_DELAY, N_COMMUTERS, N_DAYS, N_SLOTS,
        OVERLOAD_DELAY, PREFERRED_SLOT, ROAD_CAPACITY, SEED,
        SHIFT_PROB, alt, pl, random, statistics,
    )


@app.cell
def _(BASE_DELAY, N_SLOTS, OVERLOAD_DELAY, ROAD_CAPACITY, SHIFT_PROB, random):
    def simulate_day(departure_slots):
        counts = {}
        for s in departure_slots:
            counts[s] = counts.get(s, 0) + 1
        travel_time = {}
        for slot, count in counts.items():
            if count <= ROAD_CAPACITY:
                travel_time[slot] = BASE_DELAY
            else:
                overflow = count - ROAD_CAPACITY
                travel_time[slot] = BASE_DELAY + OVERLOAD_DELAY * overflow / ROAD_CAPACITY
        return travel_time

    def update_slots(departure_slots, travel_times, rng):
        new_slots = departure_slots[:]
        for i, s in enumerate(departure_slots):
            my_delay = travel_times.get(s, BASE_DELAY)
            candidates = []
            if s > 0:
                candidates.append(s - 1)
            if s < N_SLOTS - 1:
                candidates.append(s + 1)
            better = [c for c in candidates if travel_times.get(c, BASE_DELAY) < my_delay]
            if better and rng.random() < SHIFT_PROB:
                new_slots[i] = rng.choice(better)
        return new_slots

    def slot_distribution(slots):
        counts = [0] * N_SLOTS
        for s in slots:
            counts[s] += 1
        return counts

    return (simulate_day, slot_distribution, update_slots)


@app.cell
def _(BASE_DELAY, N_COMMUTERS, N_DAYS, PREFERRED_SLOT, N_SLOTS, SEED, pl, random, simulate_day, slot_distribution, statistics, update_slots):
    rng = random.Random(SEED)
    departure_slots = [
        max(0, min(N_SLOTS - 1, PREFERRED_SLOT + round(rng.gauss(0, 2))))
        for _ in range(N_COMMUTERS)
    ]

    rows = []
    for day in range(N_DAYS):
        travel_times = simulate_day(departure_slots)
        mean_delay = statistics.mean(
            travel_times.get(s, BASE_DELAY) for s in departure_slots
        )
        dist = slot_distribution(departure_slots)
        max_count = max(dist)
        rows.append({"day": day + 1, "mean_delay": mean_delay, "max_slot_count": max_count})
        departure_slots = update_slots(departure_slots, travel_times, rng)

    df = pl.DataFrame(rows)
    final_dist = slot_distribution(departure_slots)
    peak_slot = max(range(N_SLOTS), key=lambda s: final_dist[s])
    return df, departure_slots, final_dist, peak_slot, rows


@app.cell(hide_code=True)
def _(N_COMMUTERS, N_SLOTS, PREFERRED_SLOT, ROAD_CAPACITY, mo, peak_slot):
    mo.md(f"""
    ## Results

    {N_COMMUTERS} commuters, {N_SLOTS} slots, road capacity {ROAD_CAPACITY}/slot

    - Initial peak slot: {PREFERRED_SLOT}
    - Final peak slot: {peak_slot} ({'same' if peak_slot == PREFERRED_SLOT else 'shifted'})

    > **Observation:** the rush-hour peak flattens and shifts but does not disappear.
    """)
    return


@app.cell
def _(df):
    df


@app.cell
def _(alt, df):
    chart = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=alt.X("day:Q", title="Day"),
            y=alt.Y("mean_delay:Q", title="Mean travel delay"),
            tooltip=["day:Q", "mean_delay:Q", "max_slot_count:Q"],
        )
        .properties(title="Rush Hour Displacement: Mean Delay Over Time")
    )
    chart
    return (chart,)


if __name__ == "__main__":
    app.run()
