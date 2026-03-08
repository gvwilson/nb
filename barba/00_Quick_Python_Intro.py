import marimo

__generated_with = "0.20.4"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Python Crash Course
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Hello! This is a quick intro to programming in Python to help you hit the ground running with the _12 Steps to Navier–Stokes_.

    There are two ways to enjoy these lessons with Python:

    1. You can download and install a Python distribution on your computer. One option is the free [Anaconda Scientific Python](https://store.continuum.io/cshop/anaconda/) distribution. Another is [Canopy](https://www.enthought.com/products/canopy/academic/), which is free for academic use.  Our recommendation is Anaconda.

    2. You can run Python in the cloud using [Wakari](https://wakari.io/) web-based data analysis, for which you need to create a free account. (No software installation required!)

    In either case, you will probably want to download a copy of this notebook, or the whole AeroPython collection. We recommend that you then follow along each lesson, experimenting with the code in the notebooks, or typing the code into a separate Python interactive session.

    If you decided to work on your local Python installation, you will have to navigate in the terminal to the folder that contains the .ipynb files. Then, to launch the notebook server, just type:
    ipython notebook

    You will get a new browser window or tab with a list of the notebooks available in that folder. Click on one and start working!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Libraries
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Python is a high-level open-source language.  But the _Python world_ is inhabited by many packages or libraries that provide useful things like array operations, plotting functions, and much more. We can import libraries of functions to expand the capabilities of Python in our programs.

    OK! We'll start by importing a few libraries to help us out. First: our favorite library is **NumPy**, providing a bunch of useful array operations (similar to MATLAB). We will use it a lot! The second library we need is **Matplotlib**, a 2D plotting library which we will use to plot our results.
    The following code will be at the top of most of your programs, so execute this cell first:
    """)
    return


@app.cell
def _():
    # <-- comments in python are denoted by the pound sign, like this one

    import numpy                 # we import the array library
    from matplotlib import pyplot    # import plotting library

    return (numpy,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We are importing one library named `numpy` and we are importing a module called `pyplot` of a big library called `matplotlib`.
    To use a function belonging to one of these libraries, we have to tell Python where to look for it. For that, each function name is written following the library name, with a dot in between.
    So if we want to use the NumPy function [linspace()](http://docs.scipy.org/doc/numpy/reference/generated/numpy.linspace.html), which creates an array with equally spaced numbers between a start and end, we call it by writing:
    """)
    return


@app.cell
def _(numpy):
    _myarray = numpy.linspace(0, 5, 10)
    _myarray
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If we don't preface the `linspace()` function with `numpy`, Python will throw an error.
    """)
    return


@app.cell
def _(linspace):
    _myarray = linspace(0, 5, 10)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The function `linspace()` is very useful. Try it changing the input parameters!

    **Import style:**

    You will often see code snippets that use the following lines
    ```Python
    import numpy as np
    import matplotlib.pyplot as plt
    ```
    What's all of this import-as business? It's a way of creating a 'shortcut' to the NumPy library and the pyplot module. You will see it frequently as it is in common usage, but we prefer to keep out imports explicit. We think it helps with code readability.

    **Pro tip:**

    Sometimes, you'll see people importing a whole library without assigning a shortcut for it (like `from numpy import *`). This saves typing but is sloppy and can get you in trouble. Best to get into good habits from the beginning!


    To learn new functions available to you, visit the [NumPy Reference](http://docs.scipy.org/doc/numpy/reference/) page. If you are a proficient `Matlab` user, there is a wiki page that should prove helpful to you: [NumPy for Matlab Users](http://wiki.scipy.org/NumPy_for_Matlab_Users)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Variables
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Python doesn't require explicitly declared variable types like C and other languages.
    """)
    return


@app.cell
def _():
    a = 5        #a is an integer 5
    b = 'five'   #b is a string of the word 'five'
    c = 5.0      #c is a floating point 5
    return a, b, c


@app.cell
def _(a):
    type(a)
    return


@app.cell
def _(b):
    type(b)
    return


@app.cell
def _(c):
    type(c)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Note that if you divide an integer by an integer that yields a remainder, the result will be converted to a float.  (This is *different* from the behavior in Python 2.7, beware!)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Whitespace in Python
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Python uses indents and whitespace to group statements together.  To write a short loop in C, you might use:

        for (i = 0, i < 5, i++){
           printf("Hi! \n");
        }
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Python does not use curly braces like C, so the same program as above is written in Python as follows:
    """)
    return


@app.cell
def _():
    for _i in range(5):
        print('Hi \n')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If you have nested for-loops, there is a further indent for the inner loop.
    """)
    return


@app.cell
def _():
    for _i in range(3):
        for j in range(3):
            print(_i, j)
        print('This statement is within the i-loop, but not the j-loop')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Slicing Arrays
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In NumPy, you can look at portions of arrays in the same way as in `Matlab`, with a few extra tricks thrown in.  Let's take an array of values from 1 to 5.
    """)
    return


@app.cell
def _(numpy):
    myvals = numpy.array([1, 2, 3, 4, 5])
    myvals
    return (myvals,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Python uses a **zero-based index**, so let's look at the first and last element in the array `myvals`
    """)
    return


@app.cell
def _(myvals):
    myvals[0], myvals[4]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    There are 5 elements in the array `myvals`, but if we try to look at `myvals[5]`, Python will be unhappy, as `myvals[5]` is actually calling the non-existant 6th element of that array.
    """)
    return


@app.cell
def _(myvals):
    myvals[5]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Arrays can also be 'sliced', grabbing a range of values.  Let's look at the first three elements
    """)
    return


@app.cell
def _(myvals):
    myvals[0:3]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Note here, the slice is inclusive on the front end and exclusive on the back, so the above command gives us the values of `myvals[0]`, `myvals[1]` and `myvals[2]`, but not `myvals[3]`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Assigning Array Variables
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    One of the strange little quirks/features in Python that often confuses people comes up when assigning and comparing arrays of values.  Here is a quick example.  Let's start by defining a 1-D array called $a$:
    """)
    return


@app.cell
def _(numpy):
    a_1 = numpy.linspace(1, 5, 5)
    return (a_1,)


@app.cell
def _(a_1):
    a_1
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    OK, so we have an array $a$, with the values 1 through 5.  I want to make a copy of that array, called $b$, so I'll try the following:
    """)
    return


@app.cell
def _(a_1):
    b_1 = a_1
    return (b_1,)


@app.cell
def _(b_1):
    b_1
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Great.  So $a$ has the values 1 through 5 and now so does $b$.  Now that I have a backup of $a$, I can change its values without worrying about losing data (or so I may think!).
    """)
    return


@app.cell
def _(a_1):
    a_1[2] = 17
    return


@app.cell
def _(a_1):
    a_1
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here, the 3rd element of $a$ has been changed to 17.  Now let's check on $b$.
    """)
    return


@app.cell
def _(b_1):
    b_1
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And that's how things go wrong!  When you use a statement like $a = b$, rather than copying all the values of $a$ into a new array called $b$, Python just creates an alias (or a pointer) called $b$ and tells it to route us to $a$.  So if we change a value in $a$ then $b$ will reflect that change (technically, this is called *assignment by reference*).  If you want to make a true copy of the array, you have to tell Python to copy every element of $a$ into a new array.  Let's call it $c$.
    """)
    return


@app.cell
def _(a_1):
    c_1 = a_1.copy()
    return (c_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now, we can try again to change a value in $a$ and see if the changes are also seen in $c$.
    """)
    return


@app.cell
def _(a_1):
    a_1[2] = 3
    return


@app.cell
def _(a_1):
    a_1
    return


@app.cell
def _(c_1):
    c_1
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    OK, it worked!  If the difference between `a = b` and `a = b.copy()` is unclear, you should read through this again.  This issue will come back to haunt you otherwise.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Learn More
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    There are a lot of resources online to learn more about using NumPy and other libraries. Just for kicks, here we use Jupyter's feature for embedding videos to point you to a short video on YouTube on using NumPy arrays.
    """)
    return


@app.cell
def _():
    from IPython.display import YouTubeVideo
    # a short video about using NumPy arrays, from Enthought
    YouTubeVideo('vWkb7VahaXQ')
    return


@app.cell
def _():
    from IPython.core.display import HTML
    def css_styling():
        styles = open("../styles/custom.css", "r").read()
        return HTML(styles)
    css_styling()
    return


if __name__ == "__main__":
    app.run()
