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
    # Aggregating and Grouping

    The queries we wrote in the previous two tutorials operated on each row separately. We often want to ask questions about groups of rows, such as "how heavy is the largest penguin we weighed?" or "how many Gentoo penguins did we see?" This tutorial looks first at how to write queries that *aggregate* data, and then at how to calculate aggregate values for several subsets of our data simultaneously.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Aggregation

    Let's start by finding out how heavy the heaviest penguin in our dataset is. To do this, we use a function called `max`, and give it the name of the column it is to get data from. To make the result more readable, we will call the result `heaviest`.
    """)
    return


@app.cell
def _(penguins):
    _df = mo.sql(
        f"""
        select max(body_mass_g) as heaviest from penguins;
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    The query below shows the six most commonly used aggregation functions in SQL applied to different columns of the penguins data.
    """)
    return


@app.cell
def _(penguins):
    _df = mo.sql(
        f"""
        select 
            avg(flipper_length_mm) as averagest,
            count(species) as num_penguins,
            max(body_mass_g) as heaviest,
            min(flipper_length_mm) as shortest,
            sum(body_mass_g) as total_mass
        from penguins;
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Grouping

    The query shown above applies the aggregation function to all of the rows in the table. If we want, we can apply it to just the first ten.
    """)
    return


@app.cell
def _(penguins):
    _df = mo.sql(
        f"""
        select avg(body_mass_g) as avg_mass
        from penguins
        limit 10;
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    The order of operations here is important. We aren't asking SQL to calculate an average and then give us the first ten rows of the result. Instead, we are asking it to get the first ten rows and _then_ calculate the average. This matters more when we use `where` to filter the data: the filtering happens before SQL applies the function. This lets us do things like calculate the average mass of all the Gentoo penguins.
    """)
    return


@app.cell
def _(penguins):
    _df = mo.sql(
        f"""
        select avg(body_mass_g) as avg_mass
        from penguins
        where species = 'Gentoo';
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    But what if we want to calculate the average mass for each species? We could write three queries, one for each species, but (a) that would be annoying and (b) if someone adds Emperor penguins to the data and we don't remember to update our query, we won't get the full picture.

    What we should do instead is tell SQL to group the data based on the values in one or more columns, and then calculate the aggregate value within each group.
    """)
    return


@app.cell
def _(penguins):
    _df = mo.sql(
        f"""
        select avg(body_mass_g) as avg_mass
        from penguins
        group by species;
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Since there are three species, we get three rows of output. Unfortunately, we don't know which average corresponds to which species. To get that, we just add the name of the `species` column to the `select` clause.
    """)
    return


@app.cell
def _(penguins):
    _df = mo.sql(
        f"""
        select species, avg(body_mass_g) as avg_mass
        from penguins
        group by species;
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    And just as we can order data by multiple columns at once, we can group by multiple columns. When we do, we get one bucket for each unique combination of grouping values.
    """)
    return


@app.cell
def _(penguins):
    _df = mo.sql(
        f"""
        select species, sex, avg(body_mass_g) as avg_mass
        from penguins
        group by species, sex;
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    We will explain what the blanks in the `sex` column mean in the next tutorial.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Arbitrary Choice in Aggregation

    The query shown below is legal SQL, but probably not what anyone would want.
    """)
    return


@app.cell
def _(penguins):
    _df = mo.sql(
        f"""
        select sex, species, body_mass_g
        from penguins
        group by species;
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    The rule that SQL follows is this: if we have created groups using `group by`, and we _don't_ specify how to combine the values in a group for a particular column, then the database picks one of the values for that column in that group however it wants. For example, since we only grouped by `species`, but we're asking to show `sex`, the result shows one of the values for `sex` for each species. Similarly, since we didn't specify how to combine the various body masses for each species, the three values shown each come from a penguin of that species, but we don't know (and can't control) which one.

    We used this behavior earlier when we selected `species` and `avg(body_mass_g)` after grouping by `species`. Since all of the penguins within a group are of the same species, it doesn't matter which `species` value the database shows us for that group: they're all the same. If we forget to choose an aggregation function by accident, though, the answer will be plausible (because it's an actual value) but wrong.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Filtering After Aggregation

    Just as we can use `where` to filter individual rows _before_ aggregating (or if we're not aggregating at all), we can use `having` to filter aggregated values. For example, the query below finds those combinations of sex and species whose average weight is 4kg or more.
    """)
    return


@app.cell
def _(penguins):
    _df = mo.sql(
        f"""
        select sex, species, avg(body_mass_g) as avg_mass
        from penguins
        group by sex, species
        having avg_mass >= 4000.0;
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    What we _can't_ do with the tools we've seen so far is compare individual values to aggregates. For example, we can't use a query like the one below to find penguins that are heavier than average.
    """)
    return


@app.cell
def _(penguins):
    _df = mo.sql(
        f"""
        select * from penguins
        where body_mass_g > avg(body_mass_g);
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    We will see how to write this query in a couple of tutorials.
    """)
    return


if __name__ == "__main__":
    app.run()
