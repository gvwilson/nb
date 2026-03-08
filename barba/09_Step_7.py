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
    You see where this is going ... we'll do 2D diffusion now and next we will combine steps 6 and 7 to solve Burgers' equation. So make sure your previous steps work well before continuing.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Step 7: 2D Diffusion
    ----
    ***
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And here is the 2D-diffusion equation:

    $$\frac{\partial u}{\partial t} = \nu \frac{\partial ^2 u}{\partial x^2} + \nu \frac{\partial ^2 u}{\partial y^2}$$

    You will recall that we came up with a method for discretizing second order derivatives in Step 3, when investigating 1-D diffusion.  We are going to use the same scheme here, with our forward difference in time and two second-order derivatives.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $$\frac{u_{i,j}^{n+1} - u_{i,j}^n}{\Delta t} = \nu \frac{u_{i+1,j}^n - 2 u_{i,j}^n + u_{i-1,j}^n}{\Delta x^2} + \nu \frac{u_{i,j+1}^n-2 u_{i,j}^n + u_{i,j-1}^n}{\Delta y^2}$$

    Once again, we reorganize the discretized equation and solve for $u_{i,j}^{n+1}$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $$
    \begin{split}
    u_{i,j}^{n+1} = u_{i,j}^n &+ \frac{\nu \Delta t}{\Delta x^2}(u_{i+1,j}^n - 2 u_{i,j}^n + u_{i-1,j}^n) \\
    &+ \frac{\nu \Delta t}{\Delta y^2}(u_{i,j+1}^n-2 u_{i,j}^n + u_{i,j-1}^n)
    \end{split}
    $$
    """)
    return


@app.cell
def _():
    import numpy
    from matplotlib import pyplot, cm
    from mpl_toolkits.mplot3d import Axes3D ##library for 3d projection plots
    # '%matplotlib inline' command supported automatically in marimo
    return cm, numpy, pyplot


@app.cell
def _(numpy):
    ###variable declarations
    nx = 31
    ny = 31
    nt = 17
    nu = .05
    dx = 2 / (nx - 1)
    dy = 2 / (ny - 1)
    sigma = .25
    dt = sigma * dx * dy / nu

    x = numpy.linspace(0, 2, nx)
    y = numpy.linspace(0, 2, ny)

    u = numpy.ones((ny, nx))  # create a 1xn vector of 1's
    un = numpy.ones((ny, nx))

    ###Assign initial conditions
    # set hat function I.C. : u(.5<=x<=1 && .5<=y<=1 ) is 2
    u[int(.5 / dy):int(1 / dy + 1),int(.5 / dx):int(1 / dx + 1)] = 2
    return dt, dx, dy, nu, u, x, y


@app.cell
def _(cm, numpy, pyplot, u, x, y):
    fig = pyplot.figure()
    ax = fig.gca(projection='3d')
    X, Y = numpy.meshgrid(x, y)
    surf = ax.plot_surface(X, Y, u, rstride=1, cstride=1, cmap=cm.viridis,
            linewidth=0, antialiased=False)

    ax.set_xlim(0, 2)
    ax.set_ylim(0, 2)
    ax.set_zlim(1, 2.5)

    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$');
    return X, Y


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $$
    \begin{split}
    u_{i,j}^{n+1} = u_{i,j}^n &+ \frac{\nu \Delta t}{\Delta x^2}(u_{i+1,j}^n - 2 u_{i,j}^n + u_{i-1,j}^n) \\
    &+ \frac{\nu \Delta t}{\Delta y^2}(u_{i,j+1}^n-2 u_{i,j}^n + u_{i,j-1}^n)
    \end{split}
    $$
    """)
    return


@app.cell
def _(X, Y, cm, dt, dx, dy, nu, pyplot, u):
    ###Run through nt timesteps
    def diffuse(nt):
        u[int(.5 / dy):int(1 / dy + 1),int(.5 / dx):int(1 / dx + 1)] = 2  
    
        for n in range(nt + 1): 
            un = u.copy()
            u[1:-1, 1:-1] = (un[1:-1,1:-1] + 
                            nu * dt / dx**2 * 
                            (un[1:-1, 2:] - 2 * un[1:-1, 1:-1] + un[1:-1, 0:-2]) +
                            nu * dt / dy**2 * 
                            (un[2:,1: -1] - 2 * un[1:-1, 1:-1] + un[0:-2, 1:-1]))
            u[0, :] = 1
            u[-1, :] = 1
            u[:, 0] = 1
            u[:, -1] = 1

    
        fig = pyplot.figure()
        ax = fig.gca(projection='3d')
        surf = ax.plot_surface(X, Y, u[:], rstride=1, cstride=1, cmap=cm.viridis,
            linewidth=0, antialiased=True)
        ax.set_zlim(1, 2.5)
        ax.set_xlabel('$x$')
        ax.set_ylabel('$y$');

    return (diffuse,)


@app.cell
def _(diffuse):
    diffuse(10)
    return


@app.cell
def _(diffuse):
    diffuse(14)
    return


@app.cell
def _(diffuse):
    diffuse(50)
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
