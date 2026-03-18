# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo",
#     "wigglystuff",
# ]
# ///
import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from wigglystuff import ColorPicker
    return ColorPicker, mo


@app.cell
def _(mo):
    mo.md("""
    # CSS Styling Explorer

    Adjust the controls in each tab to change how common HTML elements appear.
    Changes take effect immediately.
    """)
    return


@app.cell
def _(ColorPicker, mo):
    # Typography
    font_family = mo.ui.dropdown(
        options=[
            "sans-serif", "serif", "monospace",
            "Georgia, serif", "Arial, sans-serif",
            "Courier New, monospace", "Palatino, serif",
        ],
        value="sans-serif",
        label="Font family",
    )
    font_size = mo.ui.slider(10, 32, value=16, label="Font size (px)", show_value=True)
    line_height = mo.ui.slider(1.0, 3.0, step=0.1, value=1.5, label="Line height", show_value=True)
    text_color = mo.ui.anywidget(ColorPicker(color="#222222"))
    bg_color = mo.ui.anywidget(ColorPicker(color="#f8f8f8"))
    container_padding = mo.ui.slider(8, 48, value=24, label="Padding (px)", show_value=True)
    para_margin_top = mo.ui.slider(0, 32, value=0, label="¶ margin-top (px)", show_value=True)
    para_margin_bottom = mo.ui.slider(0, 32, value=12, label="¶ margin-bottom (px)", show_value=True)

    # Headings
    heading_color = mo.ui.anywidget(ColorPicker(color="#1a1a2e"))
    heading_weight = mo.ui.dropdown(
        options=["400", "500", "600", "700", "800", "900"],
        value="700",
        label="Weight",
    )
    h1_size = mo.ui.slider(18, 56, value=36, label="H1 (px)", show_value=True)
    h2_size = mo.ui.slider(14, 44, value=28, label="H2 (px)", show_value=True)
    h3_size = mo.ui.slider(12, 36, value=22, label="H3 (px)", show_value=True)
    heading_margin_top = mo.ui.slider(0, 48, value=16, label="Margin-top (px)", show_value=True)
    heading_margin_bottom = mo.ui.slider(0, 32, value=12, label="Margin-bottom (px)", show_value=True)
    heading_line_height = mo.ui.slider(0.8, 2.5, step=0.1, value=1.2, label="Line height", show_value=True)
    letter_spacing = mo.ui.slider(-2, 8, step=0.5, value=0, label="Letter spacing (px)", show_value=True)

    # Lists
    ul_style = mo.ui.dropdown(
        options=["disc", "circle", "square", "none"],
        value="disc",
        label="Bullet style",
    )
    ol_style = mo.ui.dropdown(
        options=["decimal", "lower-alpha", "upper-alpha", "lower-roman", "upper-roman"],
        value="decimal",
        label="Numbered style",
    )
    list_indent = mo.ui.slider(10, 60, value=32, label="Indent (px)", show_value=True)
    list_gap = mo.ui.slider(0, 16, value=4, label="Item spacing (px)", show_value=True)
    list_margin_top = mo.ui.slider(0, 32, value=0, label="List margin-top (px)", show_value=True)

    # Table
    border_width = mo.ui.slider(0, 4, value=1, label="Border width (px)", show_value=True)
    border_style_sel = mo.ui.dropdown(
        options=["solid", "dashed", "dotted", "double", "none"],
        value="solid",
        label="Border style",
    )
    border_color = mo.ui.anywidget(ColorPicker(color="#cccccc"))
    cell_padding = mo.ui.slider(2, 24, value=8, label="Cell padding (px)", show_value=True)
    header_bg = mo.ui.anywidget(ColorPicker(color="#1a1a2e"))
    header_text_color = mo.ui.anywidget(ColorPicker(color="#ffffff"))
    header_text_align = mo.ui.dropdown(
        options=["left", "center", "right"],
        value="left",
        label="Header align",
    )
    table_layout = mo.ui.dropdown(
        options=["auto", "fixed"],
        value="auto",
        label="Table layout",
    )
    cell_valign = mo.ui.dropdown(
        options=["top", "middle", "bottom", "baseline"],
        value="middle",
        label="Vertical align",
    )
    row_separators = mo.ui.switch(label="Row separators only", value=False)
    zebra_stripe = mo.ui.switch(label="Zebra stripes", value=False)
    zebra_color = mo.ui.anywidget(ColorPicker(color="#efefef"))

    mo.ui.tabs({
        "Typography": mo.vstack([
            mo.hstack([font_family, font_size, line_height, container_padding]),
            mo.hstack([text_color, bg_color, para_margin_top, para_margin_bottom]),
        ]),
        "Headings": mo.vstack([
            mo.hstack([heading_color, heading_weight, h1_size, h2_size, h3_size]),
            mo.hstack([heading_margin_top, heading_margin_bottom, heading_line_height, letter_spacing]),
        ]),
        "Lists": mo.hstack([ul_style, ol_style, list_indent, list_gap, list_margin_top]),
        "Table": mo.vstack([
            mo.hstack([border_width, border_style_sel, border_color, cell_padding]),
            mo.hstack([header_bg, header_text_color, header_text_align]),
            mo.hstack([table_layout, cell_valign, row_separators, zebra_stripe, zebra_color]),
        ]),
    })
    return (
        bg_color, border_color, border_style_sel, border_width, cell_padding,
        cell_valign, container_padding, font_family, font_size,
        h1_size, h2_size, h3_size, header_bg, header_text_align, header_text_color,
        heading_color, heading_line_height, heading_margin_bottom, heading_margin_top,
        heading_weight, letter_spacing, line_height, list_gap, list_indent,
        list_margin_top, ol_style, para_margin_bottom, para_margin_top,
        row_separators, table_layout, text_color, ul_style, zebra_color, zebra_stripe,
    )


@app.cell
def _(
    mo,
    font_family, font_size, line_height, text_color, bg_color, container_padding,
    para_margin_top, para_margin_bottom,
    heading_color, heading_weight, h1_size, h2_size, h3_size,
    heading_margin_top, heading_margin_bottom, heading_line_height, letter_spacing,
    ul_style, ol_style, list_indent, list_gap, list_margin_top,
    border_width, border_style_sel, border_color, cell_padding,
    header_bg, header_text_color, header_text_align,
    table_layout, cell_valign, row_separators, zebra_stripe, zebra_color,
):
    if row_separators.value:
        _cell_border = "none"
        _row_border = f"border-bottom: {border_width.value}px {border_style_sel.value} {border_color.color};"
    else:
        _cell_border = f"{border_width.value}px {border_style_sel.value} {border_color.color}"
        _row_border = ""

    _zebra_rule = (
        f"\ntr:nth-child(even) td {{ background-color: {zebra_color.color}; }}"
        if zebra_stripe.value else ""
    )

    _heading_props = f"""\
    color: {heading_color.color};
    font-weight: {heading_weight.value};
    line-height: {heading_line_height.value};
    letter-spacing: {letter_spacing.value}px;
    margin-top: {heading_margin_top.value}px;
    margin-bottom: {heading_margin_bottom.value}px;"""

    styles_css = f"""\
body {{
    font-family: {font_family.value};
    font-size: {font_size.value}px;
    line-height: {line_height.value};
    color: {text_color.color};
    background-color: {bg_color.color};
    padding: {container_padding.value}px;
}}

p {{
    margin-top: {para_margin_top.value}px;
    margin-bottom: {para_margin_bottom.value}px;
}}

h1 {{
{_heading_props}
    font-size: {h1_size.value}px;
}}

h2 {{
{_heading_props}
    font-size: {h2_size.value}px;
}}

h3 {{
{_heading_props}
    font-size: {h3_size.value}px;
}}

ul {{
    list-style-type: {ul_style.value};
    padding-left: {list_indent.value}px;
    margin-top: {list_margin_top.value}px;
}}

ol {{
    list-style-type: {ol_style.value};
    padding-left: {list_indent.value}px;
    margin-top: {list_margin_top.value}px;
}}

li {{
    margin-bottom: {list_gap.value}px;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    table-layout: {table_layout.value};
}}

th, td {{
    border: {_cell_border};
    padding: {cell_padding.value}px;
    vertical-align: {cell_valign.value};
}}

{"tr { " + _row_border + " }" if _row_border else ""}

th {{
    background-color: {header_bg.color};
    color: {header_text_color.color};
    font-weight: 600;
    text-align: {header_text_align.value};
}}{_zebra_rule}
"""

    mo.download(
        data=styles_css.encode(),
        filename="styles.css",
        mimetype="text/css",
        label="Download CSS",
    )
    return (styles_css,)


@app.cell
def _(mo, styles_css):
    _scoped = styles_css \
        .replace("body {",               "#demo-content {") \
        .replace("\nh1 {",               "\n#demo-content h1 {") \
        .replace("\nh2 {",               "\n#demo-content h2 {") \
        .replace("\nh3 {",               "\n#demo-content h3 {") \
        .replace("\np {",                "\n#demo-content p {") \
        .replace("\nul {",               "\n#demo-content ul {") \
        .replace("\nol {",               "\n#demo-content ol {") \
        .replace("\nli {",               "\n#demo-content li {") \
        .replace("\ntable {",            "\n#demo-content table {") \
        .replace("\nth, td {",           "\n#demo-content th, #demo-content td {") \
        .replace("\nth {",               "\n#demo-content th {") \
        .replace("\ntr {",               "\n#demo-content tr {") \
        .replace("tr:nth-child",         "#demo-content tr:nth-child")

    mo.Html(f"""
    <style>
    {_scoped}
    #demo-wrapper {{
        height: calc(100vh - 380px);
        min-height: 300px;
        overflow-y: auto;
        border: 1px solid #ddd;
        border-radius: 4px;
    }}
    </style>
    <div id="demo-wrapper">
    <div id="demo-content">
        <h1>Heading Level 1</h1>
        <p>This paragraph demonstrates body text. Adjust the typography controls to change the font,
        size, color, line height, and padding. All changes take effect immediately as you move the
        sliders or make selections.</p>

        <h2>Heading Level 2</h2>
        <p>A second paragraph showing text flow. Good line height and generous padding improve
        readability, especially for longer passages. Try increasing the line height to 1.8 or
        switching to a serif font.</p>

        <h3>Heading Level 3</h3>
        <p>Each heading level has its own independent size slider while sharing color, weight,
        line height, and letter spacing with the other headings.</p>

        <h2>Unordered List</h2>
        <ul>
            <li>First item in the bulleted list</li>
            <li>Second item with a bit more text to show how long lines wrap at different font sizes</li>
            <li>Third item containing a nested list
                <ul>
                    <li>Nested sub-item one</li>
                    <li>Nested sub-item two</li>
                </ul>
            </li>
            <li>Fourth item rounds out the list</li>
        </ul>

        <h2>Ordered List</h2>
        <ol>
            <li>First step in the sequence</li>
            <li>Second step follows naturally</li>
            <li>Third step containing a nested list
                <ol>
                    <li>Sub-step A</li>
                    <li>Sub-step B</li>
                </ol>
            </li>
            <li>Fourth step completes the process</li>
        </ol>

        <h2>Table</h2>
        <table>
            <thead>
                <tr>
                    <th>Element</th>
                    <th>HTML Tag</th>
                    <th>Purpose</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Heading</td>
                    <td>&lt;h1&gt;–&lt;h6&gt;</td>
                    <td>Section titles at six levels of hierarchy</td>
                </tr>
                <tr>
                    <td>Paragraph</td>
                    <td>&lt;p&gt;</td>
                    <td>Blocks of body text</td>
                </tr>
                <tr>
                    <td>Unordered list</td>
                    <td>&lt;ul&gt;</td>
                    <td>Bulleted items without implied order</td>
                </tr>
                <tr>
                    <td>Ordered list</td>
                    <td>&lt;ol&gt;</td>
                    <td>Numbered items with a specific sequence</td>
                </tr>
                <tr>
                    <td>Table</td>
                    <td>&lt;table&gt;</td>
                    <td>Tabular data in rows and columns</td>
                </tr>
            </tbody>
        </table>
    </div>
    </div>
    """)
    return


if __name__ == "__main__":
    app.run()
