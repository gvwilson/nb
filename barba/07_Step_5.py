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
    Up to now, all of our work has been in one spatial dimension (Steps [1](./01_Step_1.ipynb) to [4](./05_Step_4.ipynb)). We can learn a lot in just 1D, but let's grow up to flatland: two dimensions.

    In the following exercises, you will extend the first four steps to 2D. To extend the 1D finite-difference formulas to partial derivatives in 2D or 3D, just apply the definition: a partial derivative with respect to $x$ is the variation in the $x$ direction *at constant* $y$.

    In 2D space, a rectangular (uniform) grid is defined by the points with coordinates:

    $$x_i = x_0 +i \Delta x$$

    $$y_i = y_0 +i \Delta y$$

    Now, define $u_{i,j} = u(x_i,y_j)$ and apply the finite-difference formulas on either variable $x,y$ *acting separately* on the $i$ and $j$ indices. All derivatives are based on the 2D Taylor expansion of a mesh point value around $u_{i,j}$.

    Hence, for a first-order partial derivative in the $x$-direction, a finite-difference formula is:

    $$ \frac{\partial u}{\partial x}\biggr\rvert_{i,j} = \frac{u_{i+1,j}-u_{i,j}}{\Delta x}+\mathcal{O}(\Delta x)$$

    and similarly in the $y$ direction. Thus, we can write backward-difference, forward-difference or central-difference formulas for Steps 5 to 12. Let's get started!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Step 5: 2-D Linear Convection
    ----
    ***
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The PDE governing 2-D Linear Convection is written as

    $$\frac{\partial u}{\partial t}+c\frac{\partial u}{\partial x} + c\frac{\partial u}{\partial y} = 0$$

    This is the exact same form as with 1-D Linear Convection, except that we now have two spatial dimensions to account for as we step forward in time.

    Again, the timestep will be discretized as a forward difference and both spatial steps will be discretized as backward differences.

    With 1-D implementations, we used $i$ subscripts to denote movement in space (e.g. $u_{i}^n-u_{i-1}^n$).  Now that we have two dimensions to account for, we need to add a second subscript, $j$, to account for all the information in the regime.

    Here, we'll again use $i$ as the index for our $x$ values, and we'll add the $j$ subscript to track our $y$ values.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    With that in mind, our discretization of the PDE should be relatively straightforward.

    $$\frac{u_{i,j}^{n+1}-u_{i,j}^n}{\Delta t} + c\frac{u_{i, j}^n-u_{i-1,j}^n}{\Delta x} + c\frac{u_{i,j}^n-u_{i,j-1}^n}{\Delta y}=0$$

    As before, solve for the only unknown:

    $$u_{i,j}^{n+1} = u_{i,j}^n-c \frac{\Delta t}{\Delta x}(u_{i,j}^n-u_{i-1,j}^n)-c \frac{\Delta t}{\Delta y}(u_{i,j}^n-u_{i,j-1}^n)$$

    We will solve this equation with the following initial conditions:

    $$u(x,y) = \begin{cases}
    \begin{matrix}
    2\ \text{for} & 0.5 \leq x, y \leq 1 \cr
    1\ \text{for} & \text{everywhere else}\end{matrix}\end{cases}$$

    and boundary conditions:

    $$u = 1\ \text{for } \begin{cases}
    \begin{matrix}
    x =  0,\ 2 \cr
    y =  0,\ 2 \end{matrix}\end{cases}$$
    """)
    return


@app.cell
def _():
    from mpl_toolkits.mplot3d import Axes3D    ##New Library required for projected 3d plots

    import numpy
    from matplotlib import pyplot, cm
    # '%matplotlib inline' command supported automatically in marimo

    ###variable declarations
    nx = 81
    ny = 81
    nt = 100
    c = 1
    dx = 2 / (nx - 1)
    dy = 2 / (ny - 1)
    sigma = .2
    dt = sigma * dx

    x = numpy.linspace(0, 2, nx)
    y = numpy.linspace(0, 2, ny)

    u = numpy.ones((ny, nx)) ##create a 1xn vector of 1's
    un = numpy.ones((ny, nx)) ##

    ###Assign initial conditions

    ##set hat function I.C. : u(.5<=x<=1 && .5<=y<=1 ) is 2
    u[int(.5 / dy):int(1 / dy + 1),int(.5 / dx):int(1 / dx + 1)] = 2 

    ###Plot Initial Condition
    ##the figsize parameter can be used to produce different sized images
    fig = pyplot.figure(figsize=(11, 7), dpi=100)
    ax = fig.gca(projection='3d')                      
    X, Y = numpy.meshgrid(x, y)                            
    surf = ax.plot_surface(X, Y, u[:], cmap=cm.viridis)
    return X, Y, c, cm, dt, dx, dy, nt, numpy, nx, ny, pyplot


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3D Plotting Notes
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To plot a projected 3D result, make sure that you have added the Axes3D library.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    from mpl_toolkits.mplot3d import Axes3D
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The actual plotting commands are a little more involved than with simple 2d plots.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```python
    fig = pyplot.figure(figsize=(11, 7), dpi=100)
    ax = fig.gca(projection='3d')
    surf2 = ax.plot_surface(X, Y, u[:])
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The first line here is initializing a figure window.  The **figsize** and **dpi** commands are optional and simply specify the size and resolution of the figure being produced.  You may omit them, but you will still require the

        fig = pyplot.figure()

    The next line assigns the plot window the axes label 'ax' and also specifies that it will be a 3d projection plot.  The final line uses the command

        plot_surface()

    which is equivalent to the regular plot command, but it takes a grid of X and Y values for the data point positions.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##### Note


    The `X` and `Y` values that you pass to `plot_surface` are not the 1-D vectors `x` and `y`.  In order to use matplotlibs 3D plotting functions, you need to generate a grid of `x, y` values which correspond to each coordinate in the plotting frame.  This coordinate grid is generated using the numpy function `meshgrid`.

        X, Y = numpy.meshgrid(x, y)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Iterating in two dimensions
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To evaluate the wave in two dimensions requires the use of several nested for-loops to cover all of the `i`'s and `j`'s.  Since Python is not a compiled language there can be noticeable slowdowns in the execution of code with multiple for-loops.  First try evaluating the 2D convection code and see what results it produces.
    """)
    return


@app.cell
def _(X, Y, c, cm, dt, dx, dy, nt, numpy, nx, ny, pyplot):
    u_1 = numpy.ones((ny, nx))
    u_1[int(0.5 / dy):int(1 / dy + 1), int(0.5 / dx):int(1 / dx + 1)] = 2
    for n in range(nt + 1):
        un_1 = u_1.copy()  ##loop across number of time steps
        row, col = u_1.shape
        for j in range(1, row):
            for i in range(1, col):
                u_1[j, i] = un_1[j, i] - c * dt / dx * (un_1[j, i] - un_1[j, i - 1]) - c * dt / dy * (un_1[j, i] - un_1[j - 1, i])
                u_1[0, :] = 1
                u_1[-1, :] = 1
                u_1[:, 0] = 1
                u_1[:, -1] = 1
    fig_1 = pyplot.figure(figsize=(11, 7), dpi=100)
    ax_1 = fig_1.gca(projection='3d')
    surf2 = ax_1.plot_surface(X, Y, u_1[:], cmap=cm.viridis)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Array Operations
    ----------------

    Here the same 2D convection code is implemented, but instead of using nested for-loops, the same calculations are evaluated using array operations.
    """)
    return


@app.cell
def _(X, Y, c, cm, dt, dx, dy, nt, numpy, nx, ny, pyplot):
    u_2 = numpy.ones((ny, nx))
    u_2[int(0.5 / dy):int(1 / dy + 1), int(0.5 / dx):int(1 / dx + 1)] = 2
    for n_1 in range(nt + 1):
        un_2 = u_2.copy()  ##loop across number of time steps
        u_2[1:, 1:] = un_2[1:, 1:] - c * dt / dx * (un_2[1:, 1:] - un_2[1:, :-1]) - c * dt / dy * (un_2[1:, 1:] - un_2[:-1, 1:])
        u_2[0, :] = 1
        u_2[-1, :] = 1
        u_2[:, 0] = 1
        u_2[:, -1] = 1
    fig_2 = pyplot.figure(figsize=(11, 7), dpi=100)
    ax_2 = fig_2.gca(projection='3d')
    surf2_1 = ax_2.plot_surface(X, Y, u_2[:], cmap=cm.viridis)
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
    The video lesson that walks you through the details for Step 5 (and onwards to Step 8) is **Video Lesson 6** on You Tube:
    """)
    return


@app.cell
def _():
    from IPython.display import YouTubeVideo
    YouTubeVideo('tUg_dE3NXoY')
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
