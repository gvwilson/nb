# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo",
# ]
# ///
import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import asyncio
    import math

    return asyncio, math, mo


@app.cell
def _(mo):
    mo.md(r"""
    # 🐢 Async Turtle Graphics in Marimo

    Each turtle method is an `async def` coroutine that `await`s a short
    `asyncio.sleep()` after drawing, yielding control back to the event
    loop so Marimo can push the updated SVG to the browser in real time.

    No threads, no locks — just cooperative multitasking.
    """)
    return


@app.cell
def _(math):
    WIDTH, HEIGHT = 520, 520

    def draw_svg(segments, tx=None, ty=None, tangle=0):
        lines = ""
        for (x1, y1), (x2, y2), color in segments:
            lines += (
                f'<line x1="{x1:.1f}" y1="{y1:.1f}" '
                f'x2="{x2:.1f}" y2="{y2:.1f}" '
                f'stroke="{color}" stroke-width="1.8" '
                f'stroke-linecap="round"/>'
            )
        marker = ""
        if tx is not None:
            r = math.radians(tangle)
            # Equilateral triangle: three vertices equally spaced at 120° (2π/3 rad)
            TURTLE_RADIUS = 9
            pts = " ".join(
                f"{tx + TURTLE_RADIUS*math.cos(r+a):.1f},{ty + TURTLE_RADIUS*math.sin(r+a):.1f}"
                for a in [0, 2*math.pi/3, -2*math.pi/3]
            )
            marker = f'<polygon points="{pts}" fill="#00ff88" opacity="0.9"/>'
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
            f'style="background:#1a1a2e;border-radius:8px;display:block">'
            f'{lines}{marker}</svg>'
        )


    return HEIGHT, WIDTH, draw_svg


@app.cell
def _(HEIGHT, WIDTH, asyncio, draw_svg, math, mo):
    class AsyncTurtle:
        """
        Each movement method is a coroutine.  Callers `await` it, so the
        event loop gets a chance to flush the updated SVG to the browser
        after every single line segment — no threads required.
        """
        PALETTE = [
            "#e63946", "#f4a261", "#2ec4b6",
            "#a8dadc", "#e9c46a", "#8ecae6", "#b5e48c",
        ]

        def __init__(self, delay: float = 0.05):
            self.x = WIDTH / 2
            self.y = HEIGHT / 2
            self.angle = -90.0      # facing upward
            self.pen = True
            self.segments: list = []
            self._ci = 0
            self._delay = delay     # seconds between frames

        # ── pen control ──────────────────────────────────────────────────────
        def penup(self):   self.pen = False
        def pendown(self): self.pen = True
        def goto(self, x, y): self.x, self.y = x, y
        def setheading(self, a): self.angle = a
        def next_color(self): self._ci += 1

        @property
        def color(self): return self.PALETTE[self._ci % len(self.PALETTE)]

        # ── private: push one SVG frame ──────────────────────────────────────
        async def _frame(self):
            mo.output.replace(
                mo.Html(draw_svg(self.segments, self.x, self.y, self.angle))
            )
            await asyncio.sleep(self._delay)   # ← yield to event loop here

        # ── movement coroutines ──────────────────────────────────────────────
        async def forward(self, dist: float):
            r = math.radians(self.angle)
            nx = self.x + dist * math.cos(r)
            ny = self.y + dist * math.sin(r)
            if self.pen:
                self.segments.append(((self.x, self.y), (nx, ny), self.color))
                self.x, self.y = nx, ny
                await self._frame()
            else:
                self.x, self.y = nx, ny

        async def backward(self, dist: float):
            await self.forward(-dist)

        def right(self, deg: float): self.angle += deg

        def left(self,  deg: float): self.angle -= deg

    return (AsyncTurtle,)


@app.function
async def spiral(t):
    for i in range(70):
        if i % 10 == 0:
            t.next_color()
        await t.forward(i * 2.8)
        t.right(91)


@app.function
async def star(t):
    for _ in range(5):
        await t.forward(200)
        t.right(144)
        t.next_color()


@app.cell
def _():
    async def branch(tt, length, depth):
        if depth == 0 or length < 3:
            await tt.forward(length)
            return
        await tt.forward(length / 3)
        tt.left(60)
        await branch(tt, length / 3, depth - 1)
        tt.right(120)
        await branch(tt, length / 3, depth - 1)
        tt.left(60)
        await tt.forward(length / 3)

    async def snowflake(t):
        for _ in range(3):
            await branch(t, 210, 3)
            t.right(120)
            t.next_color()

    return (snowflake,)


@app.function
async def square_spiral(t):
    for i in range(52):
        if i % 4 == 0:
            t.next_color()
        await t.forward(10 + i * 3.8)
        t.right(89)


@app.cell
def _(HEIGHT, WIDTH):
    async def koch(tt, length, depth):
        if depth == 0:
            await tt.forward(length)
            return
        await koch(tt, length / 3, depth - 1)
        tt.left(60)
        await koch(tt, length / 3, depth - 1)
        tt.right(120)
        await koch(tt, length / 3, depth - 1)
        tt.left(60)
        await koch(tt, length / 3, depth - 1)

    async def koch_curve(t):
        t.goto(WIDTH * 0.1, HEIGHT * 0.6)
        t.setheading(0)
        await koch(t, WIDTH * 0.8, 3)

    return (koch_curve,)


@app.cell
def _(koch_curve, mo, snowflake):
    shapes = {
        "spiral": spiral,
        "star": star,
        "snowflake": snowflake,
        "square spiral": square_spiral,
        "koch curve": koch_curve,
    }
    pattern = mo.ui.dropdown(
        options=list(shapes.keys()),
        value=list(shapes.keys())[0],
        label="Pattern",
    )
    speed = mo.ui.slider(1, 30, value=12, label="Speed (steps/sec)")
    draw_btn = mo.ui.run_button(label="▶ Draw")
    mo.hstack([pattern, speed, draw_btn], gap=2)
    return draw_btn, pattern, shapes, speed


@app.cell
async def _(AsyncTurtle, draw_btn, draw_svg, mo, pattern, shapes, speed):
    # ── cell is async: marimo runs it on its asyncio event loop ──────────────
    draw_btn  # reactive: re-run this cell whenever the button is clicked

    # Draw.
    turtle = AsyncTurtle(delay=1.0 / speed.value)
    await shapes[pattern.value](turtle)

    # Final frame: hide the turtle marker
    mo.output.replace(mo.Html(draw_svg(turtle.segments)))
    return


if __name__ == "__main__":
    app.run()
