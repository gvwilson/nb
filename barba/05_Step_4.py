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
    We continue our journey to solve the Navier–Stokes equation with Step 4. But don't continue unless you have completed the previous steps! In fact, this next step will be a combination of the two previous ones. The wonders of *code reuse*!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Step 4: Burgers' Equation
    ----
    ***
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You can read about Burgers' Equation on its [wikipedia page](http://en.wikipedia.org/wiki/Burgers'_equation).

    Burgers' equation in one spatial dimension looks like this:

    $$\frac{\partial u}{\partial t} + u \frac{\partial u}{\partial x} = \nu \frac{\partial ^2u}{\partial x^2}$$

    As you can see, it is a combination of non-linear convection and diffusion. It is surprising how much you learn from this neat little equation!

    We can discretize it using the methods we've already detailed in Steps [1](./01_Step_1.ipynb) to [3](./04_Step_3.ipynb).  Using forward difference for time, backward difference for space and our 2nd-order method for the second derivatives yields:

    $$\frac{u_i^{n+1}-u_i^n}{\Delta t} + u_i^n \frac{u_i^n - u_{i-1}^n}{\Delta x} = \nu \frac{u_{i+1}^n - 2u_i^n + u_{i-1}^n}{\Delta x^2}$$

    As before, once we have an initial condition, the only unknown is $u_i^{n+1}$. We will step in time as follows:

    $$u_i^{n+1} = u_i^n - u_i^n \frac{\Delta t}{\Delta x} (u_i^n - u_{i-1}^n) + \nu \frac{\Delta t}{\Delta x^2}(u_{i+1}^n - 2u_i^n + u_{i-1}^n)$$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Initial and Boundary Conditions

    To examine some interesting properties of Burgers' equation, it is helpful to use different initial and boundary conditions than we've been using for previous steps.

    Our initial condition for this problem is going to be:

    \begin{eqnarray}
    u &=& -\frac{2 \nu}{\phi} \frac{\partial \phi}{\partial x} + 4 \\\
    \phi &=& \exp \bigg(\frac{-x^2}{4 \nu} \bigg) + \exp \bigg(\frac{-(x-2 \pi)^2}{4 \nu} \bigg)
    \end{eqnarray}

    This has an analytical solution, given by:

    \begin{eqnarray}
    u &=& -\frac{2 \nu}{\phi} \frac{\partial \phi}{\partial x} + 4 \\\
    \phi &=& \exp \bigg(\frac{-(x-4t)^2}{4 \nu (t+1)} \bigg) + \exp \bigg(\frac{-(x-4t -2 \pi)^2}{4 \nu(t+1)} \bigg)
    \end{eqnarray}

    Our boundary condition will be:

    $$u(0) = u(2\pi)$$

    This is called a *periodic* boundary condition. Pay attention! This will cause you a bit of headache if you don't tread carefully.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Saving Time with SymPy


    The initial condition we're using for Burgers' Equation can be a bit of a pain to evaluate by hand.  The derivative $\frac{\partial \phi}{\partial x}$ isn't too terribly difficult, but it would be easy to drop a sign or forget a factor of $x$ somewhere, so we're going to use SymPy to help us out.

    [SymPy](http://sympy.org/en/) is the symbolic math library for Python.  It has a lot of the same symbolic math functionality as Mathematica with the added benefit that we can easily translate its results back into our Python calculations (it is also free and open source).

    Start by loading the SymPy library, together with our favorite library, NumPy.
    """)
    return


@app.cell
def _():
    import numpy
    import sympy

    return numpy, sympy


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We're also going to tell SymPy that we want all of its output to be rendered using $\LaTeX$. This will make our Notebook beautiful!
    """)
    return


@app.cell
def _():
    from sympy import init_printing
    init_printing(use_latex=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Start by setting up symbolic variables for the three variables in our initial condition and then type out the full equation for $\phi$.  We should get a nicely rendered version of our $\phi$ equation.
    """)
    return


@app.cell
def _(sympy):
    x, nu, t = sympy.symbols('x nu t')
    phi = (sympy.exp(-(x - 4 * t)**2 / (4 * nu * (t + 1))) +
           sympy.exp(-(x - 4 * t - 2 * sympy.pi)**2 / (4 * nu * (t + 1))))
    phi
    return nu, phi, t, x


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    It's maybe a little small, but that looks right.  Now to evaluate our partial derivative $\frac{\partial \phi}{\partial x}$ is a trivial task.
    """)
    return


@app.cell
def _(phi, x):
    phiprime = phi.diff(x)
    phiprime
    return (phiprime,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If you want to see the unrendered version, just use the Python print command.
    """)
    return


@app.cell
def _(phiprime):
    print(phiprime)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Now what?


    Now that we have the Pythonic version of our derivative, we can finish writing out the full initial condition equation and then translate it into a usable Python expression.  For this, we'll use the *lambdify* function, which takes a SymPy symbolic equation and turns it into a callable function.
    """)
    return


@app.cell
def _(nu, phi, phiprime):
    from sympy.utilities.lambdify import lambdify

    u = -2 * nu * (phiprime / phi) + 4
    print(u)
    return lambdify, u


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Lambdify

    To lambdify this expression into a useable function, we tell lambdify which variables to request and the function we want to plug them in to.
    """)
    return


@app.cell
def _(lambdify, nu, t, u, x):
    ufunc = lambdify((t, x, nu), u)
    print(ufunc(1, 4, 3))
    return (ufunc,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Back to Burgers' Equation

    Now that we have the initial conditions set up, we can proceed and finish setting up the problem.  We can generate the plot of the initial condition using our lambdify-ed function.
    """)
    return


@app.cell
def _(numpy, ufunc):
    from matplotlib import pyplot
    # '%matplotlib inline' command supported automatically in marimo
    nx = 101
    ###variable declarations
    nt = 100
    dx = 2 * numpy.pi / (nx - 1)
    nu_1 = 0.07
    dt = dx * nu_1
    x_1 = numpy.linspace(0, 2 * numpy.pi, nx)
    un = numpy.empty(nx)
    t_1 = 0
    u_1 = numpy.asarray([ufunc(t_1, x0, nu_1) for x0 in x_1])
    u_1
    return dt, dx, nt, nu_1, nx, pyplot, u_1, x_1


@app.cell
def _(numpy, pyplot, u_1, x_1):
    pyplot.figure(figsize=(11, 7), dpi=100)
    pyplot.plot(x_1, u_1, marker='o', lw=2)
    pyplot.xlim([0, 2 * numpy.pi])
    pyplot.ylim([0, 10])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This is definitely not the hat function we've been dealing with until now. We call it a "saw-tooth function".  Let's proceed forward and see what happens.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Periodic Boundary Conditions

    One of the big differences between Step 4 and the previous lessons is the use of *periodic* boundary conditions.  If you experiment with Steps 1 and 2 and make the simulation run longer (by increasing `nt`) you will notice that the wave will keep moving to the right until it no longer even shows up in the plot.

    With periodic boundary conditions, when a point gets to the right-hand side of the frame, it *wraps around* back to the front of the frame.

    Recall the discretization that we worked out at the beginning of this notebook:

    $$u_i^{n+1} = u_i^n - u_i^n \frac{\Delta t}{\Delta x} (u_i^n - u_{i-1}^n) + \nu \frac{\Delta t}{\Delta x^2}(u_{i+1}^n - 2u_i^n + u_{i-1}^n)$$

    What does $u_{i+1}^n$ *mean* when $i$ is already at the end of the frame?

    Think about this for a minute before proceeding.
    """)
    return


@app.cell
def _(dt, dx, nt, nu_1, numpy, nx, u_1, ufunc, x_1):
    for n in range(nt):
        un_1 = u_1.copy()
        for i in range(1, nx - 1):
            u_1[i] = un_1[i] - un_1[i] * dt / dx * (un_1[i] - un_1[i - 1]) + nu_1 * dt / dx ** 2 * (un_1[i + 1] - 2 * un_1[i] + un_1[i - 1])
        u_1[0] = un_1[0] - un_1[0] * dt / dx * (un_1[0] - un_1[-2]) + nu_1 * dt / dx ** 2 * (un_1[1] - 2 * un_1[0] + un_1[-2])
        u_1[-1] = u_1[0]
    u_analytical = numpy.asarray([ufunc(nt * dt, xi, nu_1) for xi in x_1])
    return (u_analytical,)


@app.cell
def _(numpy, pyplot, u_1, u_analytical, x_1):
    pyplot.figure(figsize=(11, 7), dpi=100)
    pyplot.plot(x_1, u_1, marker='o', lw=2, label='Computational')
    pyplot.plot(x_1, u_analytical, label='Analytical')
    pyplot.xlim([0, 2 * numpy.pi])
    pyplot.ylim([0, 10])
    pyplot.legend()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ***

    What next?
    ----

    The subsequent steps, from 5 to 12, will be in two dimensions. But it is easy to extend the 1D finite-difference formulas to the partial derivatives in 2D or 3D. Just apply the definition — a partial derivative with respect to $x$ is the variation in the $x$ direction *while keeping $y$ constant*.

    Before moving on to [Step 5](./07_Step_5.ipynb), make sure you have completed your own code for steps 1 through 4 and you have experimented with the parameters and thought about what is happening. Also, we recommend that you take a slight break to learn about [array operations with NumPy](./06_Array_Operations_with_NumPy.ipynb).
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


if __name__ == "__main__":
    app.run()
