# Miscellaneous Marimo Notebook Material

| directory | contents |
| :-------- | :------- |
| `altair` | University of Washington "Intro to Altair" tutorial notebooks |
| `barba` | Prof. Lorena Barba's "12 Steps to Navier-Stokes" notebooks |
| `bib` | material related to notebooks in education and getting educators to adopt new tools |
| `des` | unexpected results from queueing theory with discrete event simulations in notebooks |
| `dist` | local Python package directory |
| `docs` | miscellaneous documents (largely superseded by Notion pages) |
| `images` | experimenting with `/public` image paths |
| `jenkins` | converting one of David Jenkins' notebooks |
| `js` | JavaScript for Marimo Educational Widgets (MEW) |
| `kis` | converting one of Amanda Kis's meteorological notebooks |
| `mew` | Marimo Educational Widgets |
| `nederbragt` | converting some of Lex Nederbragt's bioinformatics notebooks |
| `parallel` | vibe-coded experiments connecting Marimo to Dagster, Luigi, and Metaflow |
| `pogil` | Process Oriented Guided Inquiry Learning material |
| `sql` | SQL tutorial in Marimo notebooks |
| `turtle` | animated turtle graphics in Marimo notebook |

## Installation

-   `uv venv` and activate and `uv sync --dev`
-   `brew install eccodes` or equivalent before trying to run `kis/*.py` notebook.

## Marimo Educational Widgets

Three interactive educational widgets for Marimo computational notebooks using AnyWidget.

### Widgets Overview

Multiple Choice Widget (`MultipleChoiceWidget`)
:   Presents a question with multiple answer options.
    Students select one answer and receive immediate feedback.

Matching Widget (`MatchingWidget`)
:   Requires students to match items from Column A with corresponding items from Column B.

Ordering Widget (`OrderingWidget`)
:   Students arrange text items in the correct sequence by moving them up and down.

### Installation

Requires:

-   Python 3.13+
-   Node.js 16+

```bash
cd mew

# Build JavaScript first
cd js
npm install
npm run build

# Then install Python package
cd ..
uv sync --dev
```

## Try the Example

```bash
marimo edit example_notebook.py
```

This will open an interactive notebook with all three widget types.

### Create Your First Question

Create a new file `my_quiz.py`:

```python
import marimo as mo
from marimo_education_widgets import MultipleChoiceWidget

app = mo.App()

@app.cell
def __():
    import marimo as mo
    from marimo_education_widgets import MultipleChoiceWidget
    return mo, MultipleChoiceWidget

@app.cell
def __(mo, MultipleChoiceWidget):
    question = mo.ui.anywidget(MultipleChoiceWidget(
        question="What is 2 + 2?",
        options=["3", "4", "5"],
        correct_answer=1
    ))
    question
    return question,

if __name__ == "__main__":
    app.run()
```

Run it:

```bash
marimo edit my_quiz.py
```
