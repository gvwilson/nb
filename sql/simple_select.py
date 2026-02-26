# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "polars",
# ]
# ///

import marimo

__generated_with = "0.19.9"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import sqlite3
    import textwrap

    return mo, sqlite3, textwrap


@app.cell
def _(sqlite3):
    conn = sqlite3.connect("penguins.db")
    return (conn,)


@app.cell
def _(mo, textwrap):
    def show_sql(query, conn):
        clean = textwrap.dedent(query).strip()
        df = mo.sql(f"{clean}", engine=conn, output=False)
        return mo.vstack([mo.md(f"```sql\n{clean}\n```"), df])

    return (show_sql,)


@app.cell
def _(mo):
    mo.md("""
# Core Features
""")
    return


@app.cell
def _(mo):
    mo.md("""
## Selecting Constant

- `select` is a keyword
- Normally used to select data from table...
- ...but if all we want is a constant value, we don't need to specify one
- Semi-colon terminator is required
""")
    return


@app.cell
def _(conn, show_sql):
    show_sql("""
        select 1;
    """, conn)
    return


@app.cell
def _(mo):
    mo.md("""
## Selecting All Values from Table

- An actual query
- Use `*` to mean "all columns"
- Use `from` *tablename* to specify table
- Output format is not particularly readable
""")
    return


@app.cell
def _(conn, show_sql):
    show_sql("""
        select * from penguins;
    """, conn)
    return


@app.cell
def _(mo):
    mo.md("""
## Specifying Columns

- Specify column names separated by commas
- In any order
- Duplicates allowed
- Line breaks encouraged for readability
""")
    return


@app.cell
def _(conn, show_sql):
    show_sql("""
        select
            species,
            island,
            sex
        from penguins;
    """, conn)
    return


@app.cell
def _(mo):
    mo.md("""
## Sorting

- `order by` must follow `from` (which must follow `select`)
- `asc` is ascending, `desc` is descending
    - Default is ascending, but please specify
""")
    return


@app.cell
def _(conn, show_sql):
    show_sql("""
        select
            species,
            sex,
            island
        from penguins
        order by island asc, sex desc;
    """, conn)
    return


@app.cell
def _(mo):
    mo.callout(mo.md("""
**Exercise**

Write a SQL query to select the sex and body mass columns from the `penguins` in that
order, sorted such that the largest body mass appears first.
"""), kind="info")
    return


@app.cell
def _(mo):
    mo.md("""
## Limiting Output

- Full dataset has 344 rows
- `limit N` specifies maximum number of rows returned by query
""")
    return


@app.cell
def _(conn, show_sql):
    show_sql("""
        select
            species,
            sex,
            island
        from penguins
        order by species, sex, island
        limit 10;
    """, conn)
    return


@app.cell
def _(mo):
    mo.md("""
## Paging Output

- `offset N` must follow `limit`
- Specifies number of rows to skip from the start of the selection
- So this query skips the first 3 and shows the next 10
""")
    return


@app.cell
def _(conn, show_sql):
    show_sql("""
        select
            species,
            sex,
            island
        from penguins
        order by species, sex, island
        limit 10 offset 3;
    """, conn)
    return


@app.cell
def _(mo):
    mo.md("""
## Removing Duplicates

- `distinct` keyword must appear right after `select`
    - SQL was supposed to read like English
- Shows distinct combinations
- Blanks in `sex` column show missing data
    - We'll talk about this in a bit
""")
    return


@app.cell
def _(conn, show_sql):
    show_sql("""
        select distinct
            species,
            sex,
            island
        from penguins;
    """, conn)
    return


@app.cell
def _(mo):
    mo.callout(mo.md("""
**Exercise**

1. Write a SQL query to select the islands and species from rows 50 to 60 inclusive
   of the `penguins` table. Your result should have 11 rows.

2. Modify your query to select distinct combinations of island and species from the
   same rows and compare the result to what you got in part 1.
"""), kind="info")
    return


@app.cell
def _(mo):
    mo.md("""
## Filtering Results

- `where` *condition* filters the rows produced by selection
- Condition is evaluated independently for each row
- Only rows that pass the test appear in results
- Use single quotes for `'text data'` and double quotes for `"weird column names"`
    - SQLite will accept double-quoted text data but SQLFluff will complain
""")
    return


@app.cell
def _(conn, show_sql):
    show_sql("""
        select distinct
            species,
            sex,
            island
        from penguins
        where island = 'Biscoe';
    """, conn)
    return


@app.cell
def _(mo):
    mo.callout(mo.md("""
**Exercise**

1. Write a query to select the body masses from `penguins` that are less than 3000.0 grams.

2. Write another query to select the species and sex of penguins that weight less than
   3000.0 grams. This shows that the columns displayed and those used in filtering are
   independent of each other.
"""), kind="info")
    return


@app.cell
def _(mo):
    mo.md("""
## Filtering with More Complex Conditions

- `and`: both sub-conditions must be true
- `or`: either or both part must be true
- Notice that the row for Gentoo penguins on Biscoe island with unknown (empty) sex
  didn't pass the test
    - We'll talk about this in a bit
""")
    return


@app.cell
def _(conn, show_sql):
    show_sql("""
        select distinct
            species,
            sex,
            island
        from penguins
        where island = 'Biscoe' and sex != 'MALE';
    """, conn)
    return


@app.cell
def _(mo):
    mo.callout(mo.md("""
**Exercise**

1. Use the `not` operator to select penguins that are *not* Gentoos.

2. SQL's `or` is an inclusive or: it succeeds if either *or both* conditions are true.
   SQL does not provide a specific operator for exclusive or, which is true if either
   *but not both* conditions are true, but the same effect can be achieved using `and`,
   `or`, and `not`. Write a query to select penguins that are female *or* on Torgersen
   Island *but not both*.
"""), kind="info")
    return


@app.cell
def _(mo):
    mo.md("""
## Doing Calculations

- Can do the usual kinds of arithmetic on individual values
    - Calculation done for each row independently
- Column name shows the calculation done
""")
    return


@app.cell
def _(conn, show_sql):
    show_sql("""
        select
            flipper_length_mm / 10.0,
            body_mass_g / 1000.0
        from penguins
        limit 3;
    """, conn)
    return


@app.cell
def _(mo):
    mo.md("""
## Renaming Columns

- Use *expression* `as` *name* to rename
- Give result of calculation a meaningful name
- Can also rename columns without modifying
""")
    return


@app.cell
def _(conn, show_sql):
    show_sql("""
        select
            flipper_length_mm / 10.0 as flipper_cm,
            body_mass_g / 1000.0 as weight_kg,
            island as where_found
        from penguins
        limit 3;
    """, conn)
    return


@app.cell
def _(mo):
    mo.callout(mo.md("""
**Exercise**

Write a single query that calculates and returns:

1. A column called `what_where` that has the species and island of each penguin
   separated by a single space.
2. A column called `bill_ratio` that has the ratio of bill length to bill depth.

You can use the `||` operator to concatenate text to solve part 1,
or look at the documentation for SQLite's `format()` function.
"""), kind="info")
    return


if __name__ == "__main__":
    app.run()
