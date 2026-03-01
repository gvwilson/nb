import marimo

__generated_with = "0.20.2"
app = marimo.App(width="medium")

with app.setup:
    import marimo as mo
    import sqlalchemy

    DATABASE_URL = "sqlite:///penguins.db"
    engine = sqlalchemy.create_engine(DATABASE_URL)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Missing Data

    The biggest challenge people facing when using databases isn't remembering the order of various bits of queries. The biggest challenge is handling missing data. This tutorial builds on the filtering introduced in the previous one to show how to manage this in our queries.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Null

    Here are all of the distinct combinations of island, species, and sex in the `penguins` table.
    """)
    return


@app.cell
def _(penguins):
    _df = mo.sql(
        f"""
        select distinct island, species, sex from penguins;
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Notice the two blanks in the `sex` column, and the fact that its subtitle says there are 3 unique values. Those blanks show the special value `null`, which SQL uses to mean "I don't know". In this case, those values tell us that the scientists who collected the penguins didn't record the sex of some of the Adelie penguins on Dream and Torgersen islands.

    `null` is not the same thing as zero or an empty piece of text. The most important thing about it is that almost any question we can ask that involves a `null` produces `null` as answer. For example, we can use SQL as a very complicated desk calculator and ask, "What is 1 + 2?"
    """)
    return


@app.cell
def _():
    _df = mo.sql(
        f"""
        select 1 + 2 as result;
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    If we ask, "What is 1 + `null`", on the other hand, the answer is `null`, because one plus "I don't know" is "I don't know".
    """)
    return


@app.cell
def _():
    _df = mo.sql(
        f"""
        select 1 + null as result;
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    We get the same thing if we subtract null, multiply by it, and so on. We also get the same thing if we do comparisons. Is `null` equal to 3? Again, the answer is `null`.
    """)
    return


@app.cell
def _():
    _df = mo.sql(
        f"""
        select null = 3 as result;
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    We get the same thing if we ask if `null` is _not_ equal to 3, because if we don't know the value, we don't know if it _isn't_ 3.
    """)
    return


@app.cell
def _():
    _df = mo.sql(
        f"""
        select null != 3 as result;
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    What about `null = null`? If I have two numbers, and I don't know what either is, I don't know if they're the same, so the answer is (once again) `null`.
    """)
    return


@app.cell
def _():
    _df = mo.sql(
        f"""
        select null = null as result;
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Handling Nulls

    There are only two things we can do with `null` that don't produce `null` as a result: ask if a value is `null`, and ask if it isn't. If we're interested in the `sex` column, the first is written `sex is null`, while the second is written `sex is not null`. Note that `is null` and `is not null` are written as multiple words, but are a single test; it's confusing, but we're stuck with it.

    Let's have a look at some practical examples. If we select the distinct values of `sex` from the `penguins` table, we get `"FEMALE"`, `"MALE"`, and `null`. (The first line of output is blank, which is how Marimo shows null values.)
    """)
    return


@app.cell
def _(penguins):
    _df = mo.sql(
        f"""
        select distinct sex from penguins order by sex;
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    If we want to get all the rows that have a null value for `sex`, we _cannot_ do this:
    """)
    return


@app.cell
def _(penguins):
    _df = mo.sql(
        f"""
        select sex from penguins
        where (sex != 'MALE') and (sex != 'FEMALE');
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    That doesn't produce any output because the rows with null values for `sex` don't pass the test: `null` is not true. If we want the rows with missing sex, we have to ask for them explicitly. This query gives us 11 rows.
    """)
    return


@app.cell
def _(penguins):
    _df = mo.sql(
        f"""
        select sex from penguins
        where sex is null;
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    How many times did the scientists fail to record a penguin's mass or flipper length? The answer is "twice", and in both cases they didn't record _any_ of the physical measurements.
    """)
    return


@app.cell
def _(penguins):
    _df = mo.sql(
        f"""
        select * from penguins
        where (body_mass_g is null) or (flipper_length_mm is null);
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Some programmers find `null` very annoying. Instead of putting it in their tables, they use marker values like -1 or `"NA"` to signal missing data. Doing this almost always leads to problems. For example, if we are calculating the average age of people who are 17, 19, 21, and and unknown number of years old, the sensible thing to do is add the values we know (the 17, 19, and 21) and then divide by 3. As we will see in the next tutorial, SQL will do this for us automatically _if_ we have used `null` to represent the unknown age. If we use -1, on the other hand, it's all too easy to calculate (17 + 19 + 21 - 1) / 4 and get an average age of 14. We could use `where` to filter out the -1 ages before doing the sum, but (a) we'd have to know to do that and (b) we'd have to know that this programmer used -1 instead of -999999 or something else to mean "I don't know". While it takes a bit of getting used to, it's (almost) always better to use `null` when there are holes in our data.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Ternary Logic

    These tutorials avoid theory when they can, but a little bit will help understand how `null` works. In conventional logic, a statement is either true or false. If we have two statements `A` and `B`, then `A and B` is true when both are true, while `A or B` is true if either or both are true. We can show these rules using tables.

    /// note | Boolean tables for `and` and `or`
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    These rules are sometimes referred to as *binary logic* because there are only two possible values. SQL is unusual among programming languages in using *ternary logic*, in which any statement can be true, false, or null. The tables below show how `and` and `or` work in this case.

    /// note | three-valued logic tables for `and` and `or`.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    /// note | add exercises
    """)
    return


if __name__ == "__main__":
    app.run()
