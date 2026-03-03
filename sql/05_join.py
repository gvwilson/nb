import marimo

__generated_with = "0.20.2"
app = marimo.App(width="medium")

with app.setup:
    import marimo as mo
    import sqlalchemy

    DATABASE_URL = "sqlite:///lab.db"
    engine = sqlalchemy.create_engine(DATABASE_URL)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Combining Tables

    Relational databases get their name from the fact that they store the relations between tables. This tutorial shows how to connect and combine information from multiple tables; along the way, it also shows how to represent a database schema as a diagram.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Basic Joins

    The `jobs` database has two tables. The first, called `job`, shows the credits that students can earn doing different kinds of jobs, and has just two rows and two columns:

    | name | credits |
    | :--- | ------: |
    | calibrate | 1.5 |
    | clean | 0.5 |

    The other table, `work`, keeps track of who has done which jobs:

    | person | job |
    | :----- | :-- |
    | Amal | calibrate |
    | Amal | clean |
    | Amal | complain |
    | Gita | clean |
    | Gita | clean |
    | Gita | complain |
    | Madhi | complain |

    Our first question is, "How many credits has each student earned?" The first step in answering this is to join the two tables together.
    """)
    return


@app.cell
def _():
    _df = mo.sql(
        f"""
        select *
        from job join work;
        """,
        engine=engine
    )
    return


if __name__ == "__main__":
    app.run()
