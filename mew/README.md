# Marimo Education Widgets

Three interactive educational widgets for Marimo computational notebooks using AnyWidget.

## Widgets Overview

Multiple Choice Widget (`MultipleChoiceWidget`)
:   Presents a question with multiple answer options.
    Students select one answer and receive immediate feedback.

Matching Widget (`MatchingWidget`)
:   Requires students to match items from Column A with corresponding items from Column B.

Ordering Widget (`OrderingWidget`)
:   Students arrange text items in the correct sequence by moving them up and down.

## Installation

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

## Create Your First Question

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
