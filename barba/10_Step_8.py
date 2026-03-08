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
    This will be a milestone! We now get to Step 8: Burgers' equation. We can learn so much more from this equation. It plays a very important role in fluid mechanics, because it contains the full convective nonlinearity of the flow equations, and at the same time there are many known analytical solutions.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Step 8: Burgers' Equation in 2D
    ----
    ***
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Remember, Burgers' equation can generate discontinuous solutions from an initial condition that is smooth, i.e., can develop "shocks." We want to see this in two dimensions now!

    Here is our coupled set of PDEs:

    $$
    \frac{\partial u}{\partial t} + u \frac{\partial u}{\partial x} + v \frac{\partial u}{\partial y} = \nu \; \left(\frac{\partial ^2 u}{\partial x^2} + \frac{\partial ^2 u}{\partial y^2}\right)$$

    $$
    \frac{\partial v}{\partial t} + u \frac{\partial v}{\partial x} + v \frac{\partial v}{\partial y} = \nu \; \left(\frac{\partial ^2 v}{\partial x^2} + \frac{\partial ^2 v}{\partial y^2}\right)$$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We know how to discretize each term: we've already done it before!

    $$
    \begin{split}
    & \frac{u_{i,j}^{n+1} - u_{i,j}^n}{\Delta t} + u_{i,j}^n \frac{u_{i,j}^n-u_{i-1,j}^n}{\Delta x} + v_{i,j}^n \frac{u_{i,j}^n - u_{i,j-1}^n}{\Delta y} = \\
    & \qquad \nu \left( \frac{u_{i+1,j}^n - 2u_{i,j}^n+u_{i-1,j}^n}{\Delta x^2} + \frac{u_{i,j+1}^n - 2u_{i,j}^n + u_{i,j-1}^n}{\Delta y^2} \right)
    \end{split}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $$
    \begin{split}
    & \frac{v_{i,j}^{n+1} - v_{i,j}^n}{\Delta t} + u_{i,j}^n \frac{v_{i,j}^n-v_{i-1,j}^n}{\Delta x} + v_{i,j}^n \frac{v_{i,j}^n - v_{i,j-1}^n}{\Delta y} = \\
    & \qquad \nu \left( \frac{v_{i+1,j}^n - 2v_{i,j}^n+v_{i-1,j}^n}{\Delta x^2} + \frac{v_{i,j+1}^n - 2v_{i,j}^n + v_{i,j-1}^n}{\Delta y^2} \right)
    \end{split}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And now, we will rearrange each of these equations for the only unknown: the two components $u,v$ of the solution at the next time step:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $$
    \begin{split}
    u_{i,j}^{n+1} = & u_{i,j}^n - \frac{\Delta t}{\Delta x} u_{i,j}^n (u_{i,j}^n - u_{i-1,j}^n)  - \frac{\Delta t}{\Delta y} v_{i,j}^n (u_{i,j}^n - u_{i,j-1}^n) \\
    &+ \frac{\nu \Delta t}{\Delta x^2}(u_{i+1,j}^n-2u_{i,j}^n+u_{i-1,j}^n) + \frac{\nu \Delta t}{\Delta y^2} (u_{i,j+1}^n - 2u_{i,j}^n + u_{i,j-1}^n)
    \end{split}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $$
    \begin{split}
    v_{i,j}^{n+1} = & v_{i,j}^n - \frac{\Delta t}{\Delta x} u_{i,j}^n (v_{i,j}^n - v_{i-1,j}^n) - \frac{\Delta t}{\Delta y} v_{i,j}^n (v_{i,j}^n - v_{i,j-1}^n) \\
    &+ \frac{\nu \Delta t}{\Delta x^2}(v_{i+1,j}^n-2v_{i,j}^n+v_{i-1,j}^n) + \frac{\nu \Delta t}{\Delta y^2} (v_{i,j+1}^n - 2v_{i,j}^n + v_{i,j-1}^n)
    \end{split}
    $$
    """)
    return


@app.cell
def _():
    import numpy
    from matplotlib import pyplot, cm
    from mpl_toolkits.mplot3d import Axes3D
    # '%matplotlib inline' command supported automatically in marimo
    return cm, numpy, pyplot


@app.cell
def _(numpy):
    ###variable declarations
    nx = 41
    ny = 41
    nt = 120
    c = 1
    dx = 2 / (nx - 1)
    dy = 2 / (ny - 1)
    sigma = .0009
    nu = 0.01
    dt = sigma * dx * dy / nu


    x = numpy.linspace(0, 2, nx)
    y = numpy.linspace(0, 2, ny)

    u = numpy.ones((ny, nx))  # create a 1xn vector of 1's
    v = numpy.ones((ny, nx))
    un = numpy.ones((ny, nx)) 
    vn = numpy.ones((ny, nx))
    comb = numpy.ones((ny, nx))

    ###Assign initial conditions

    ##set hat function I.C. : u(.5<=x<=1 && .5<=y<=1 ) is 2
    u[int(.5 / dy):int(1 / dy + 1),int(.5 / dx):int(1 / dx + 1)] = 2 
    ##set hat function I.C. : u(.5<=x<=1 && .5<=y<=1 ) is 2
    v[int(.5 / dy):int(1 / dy + 1),int(.5 / dx):int(1 / dx + 1)] = 2
    return dt, dx, dy, nt, nu, u, v, x, y


@app.cell
def _(cm, numpy, pyplot, u, v, x, y):
    ###(plot ICs)
    fig = pyplot.figure(figsize=(11, 7), dpi=100)
    ax = fig.gca(projection='3d')
    X, Y = numpy.meshgrid(x, y)
    ax.plot_surface(X, Y, u[:], cmap=cm.viridis, rstride=1, cstride=1)
    ax.plot_surface(X, Y, v[:], cmap=cm.viridis, rstride=1, cstride=1)
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$');
    return


@app.cell
def _(dt, dx, dy, nt, nu, u, v):
    for n in range(nt + 1):  ##loop across number of time steps
        un_1 = u.copy()
        vn_1 = v.copy()
        u[1:-1, 1:-1] = un_1[1:-1, 1:-1] - dt / dx * un_1[1:-1, 1:-1] * (un_1[1:-1, 1:-1] - un_1[1:-1, 0:-2]) - dt / dy * vn_1[1:-1, 1:-1] * (un_1[1:-1, 1:-1] - un_1[0:-2, 1:-1]) + nu * dt / dx ** 2 * (un_1[1:-1, 2:] - 2 * un_1[1:-1, 1:-1] + un_1[1:-1, 0:-2]) + nu * dt / dy ** 2 * (un_1[2:, 1:-1] - 2 * un_1[1:-1, 1:-1] + un_1[0:-2, 1:-1])
        v[1:-1, 1:-1] = vn_1[1:-1, 1:-1] - dt / dx * un_1[1:-1, 1:-1] * (vn_1[1:-1, 1:-1] - vn_1[1:-1, 0:-2]) - dt / dy * vn_1[1:-1, 1:-1] * (vn_1[1:-1, 1:-1] - vn_1[0:-2, 1:-1]) + nu * dt / dx ** 2 * (vn_1[1:-1, 2:] - 2 * vn_1[1:-1, 1:-1] + vn_1[1:-1, 0:-2]) + nu * dt / dy ** 2 * (vn_1[2:, 1:-1] - 2 * vn_1[1:-1, 1:-1] + vn_1[0:-2, 1:-1])
        u[0, :] = 1
        u[-1, :] = 1
        u[:, 0] = 1
        u[:, -1] = 1
        v[0, :] = 1
        v[-1, :] = 1
        v[:, 0] = 1
        v[:, -1] = 1
    return


@app.cell
def _(cm, numpy, pyplot, u, v, x, y):
    fig_1 = pyplot.figure(figsize=(11, 7), dpi=100)
    ax_1 = fig_1.gca(projection='3d')
    X_1, Y_1 = numpy.meshgrid(x, y)
    ax_1.plot_surface(X_1, Y_1, u, cmap=cm.viridis, rstride=1, cstride=1)
    ax_1.plot_surface(X_1, Y_1, v, cmap=cm.viridis, rstride=1, cstride=1)
    ax_1.set_xlabel('$x$')
    ax_1.set_ylabel('$y$')
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
    The video lesson that walks you through the details for Steps 5 to 8 is **Video Lesson 6** on You Tube:
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
