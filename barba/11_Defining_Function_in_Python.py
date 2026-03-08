import marimo

__generated_with = "0.20.4"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


app._unparsable_cell(
    r"""
    Text provided under a Creative Commons Attribution license, CC-BY.  All code is made available under the FSF-approved BSD-3 license.  (c) Lorena A. Barba, Gilbert F. Forsyth 2017. Thanks to NSF for support via CAREER award #1149784.
    """,
    name="_"
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    [@LorenaABarba](https://twitter.com/LorenaABarba)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    12 steps to Navier–Stokes
    =====
    ***
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This lesson complements the first interactive module of the online [CFD Python](https://github.com/barbagroup/CFDPython) class, by Prof. Lorena A. Barba, called **12 Steps to Navier–Stokes.** The interactive module starts with simple exercises in 1D that at first use little of the power of Python. We now present some new ways of doing the same things that are more efficient and produce prettier code.

    This lesson was written with BU graduate student Gilbert Forsyth.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Defining Functions in Python
    ----
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In steps 1 through 8, we wrote Python code that is meant to run from top to bottom.  We were able to reuse code (to great effect!) by copying and pasting, to incrementally build a solver for the Burgers' equation. But moving forward there are more efficient ways to write our Python codes.  In this lesson, we are going to introduce *function definitions*, which will allow us more flexibility in reusing and also in organizing our code.

    We'll begin with a trivial example: a function which adds two numbers.

    To create a function in Python, we start with the following:

        def simpleadd(a,b):

    This statement creates a function called `simpleadd` which takes two inputs, `a` and `b`. Let's execute this definition code.
    """)
    return


@app.function
def simpleadd(a, b):
    return a+b


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The `return` statement tells Python what data to return in response to being called.  Now we can try calling our `simpleadd` function:
    """)
    return


@app.cell
def _():
    simpleadd(3, 4)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Of course, there can be much more happening between the `def` line and the `return` line.  In this way, one can build code in a *modular* way. Let's try a function which returns the `n`-th number in the Fibonacci sequence.
    """)
    return


@app.function
def fibonacci(n):
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
    return a


@app.cell
def _():
    fibonacci(7)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Once defined, the function `fibonacci` can be called like any of the built-in Python functions that we've already used. For exmaple, we might want to print out the Fibonacci sequence up through the `n`-th value:
    """)
    return


@app.cell
def _():
    for n in range(10):
        print(fibonacci(n))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We will use the capacity of defining our own functions in Python to help us build code that is easier to reuse, easier to maintain, easier to share!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##### Exercise
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    (Pending.)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Learn more
    -----
    ***
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Remember our short detour on using [array operations with NumPy](./07_Step_5.ipynb)?

    Well, there are a few more ways to make your scientific codes in Python run faster. We recommend the article on the Technical Discovery blog about [Speeding Up Python](http://technicaldiscovery.blogspot.com/2011/06/speeding-up-python-numpy-cython-and.html) (June 20, 2011), which talks about NumPy, Cython and Weave. It uses as example the Laplace equation (which we will solve in [Step 9](./12_Step_9.ipynb)) and makes neat use of defined functions.

    But a recent new way to get fast Python codes is [Numba](http://numba.pydata.org). We'll learn a bit about that after we finish the **12 steps to Navier–Stokes**.

    There are many exciting things happening in the world of high-performance Python right now!

    ***
    """)
    return


@app.cell
def _():
    from IPython.core.display import HTML
    def css_styling():
        styles = open("../styles/custom.css", "r").read()
        return HTML(styles)
    css_styling()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > (The cell above executes the style for this notebook.)
    """)
    return


if __name__ == "__main__":
    app.run()
