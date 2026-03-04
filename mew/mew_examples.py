"""
Example Marimo Notebook: Education Widgets Demo

This notebook demonstrates all three educational widgets.
Run with: marimo edit example_notebook.py
"""

import marimo

__generated_with = "0.19.9"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    from mew import (
        LabelingWidget,
        MatchingWidget,
        MultipleChoiceWidget,
        OrderingWidget,
    )

    return LabelingWidget, MatchingWidget, MultipleChoiceWidget, OrderingWidget


@app.cell
def _(mo):
    mo.md("""
    # Educational Widgets Demo

    This notebook demonstrates interactive self-test questions.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Labeling Question
    """)
    return


@app.cell
def _(LabelingWidget, mo):
    labeling_question = mo.ui.anywidget(LabelingWidget(
        question="Label the parts of this Python code:",
        labels=[
            "Variable declaration",
            "Function call",
            "String literal",
            "Arithmetic operation"
        ],
        text_lines=[
            "name = 'Alice'",
            "age = 25",
            "result = age + 5",
            "print(name)"
        ],
        correct_labels={
            0: [0, 2],      # Line 0: labels 0 and 2
            1: [0],         # Line 1: label 0
            2: [0, 3],      # Line 2: labels 0 and 3
            3: [1, 2]       # Line 3: labels 1 and 2
        }
    ))
    labeling_question
    return (labeling_question,)


@app.cell
def _(labeling_question, mo):
    _val = labeling_question.value.get('value')
    mo.md(f"""
    **Student Response:** {_val if _val else 'Not answered yet'}
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Matching Question
    """)
    return


@app.cell
def _(MatchingWidget, mo):
    matching_question = mo.ui.anywidget(MatchingWidget(
        question="Match the programming languages to their primary paradigms:",
        left=["Python", "Haskell", "C", "SQL"],
        right=["Functional", "Procedural", "Multi-paradigm", "Declarative"],
        correct_matches={0: 2, 1: 0, 2: 1, 3: 3}
    ))
    matching_question
    return (matching_question,)


@app.cell
def _(matching_question, mo):
    _val = matching_question.value.get('value')
    mo.md(f"""
    **Student Response:** {_val if _val else 'Not answered yet'}
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Multiple Choice Question
    """)
    return


@app.cell
def _(MultipleChoiceWidget, mo):
    multiple_choice_question = mo.ui.anywidget(MultipleChoiceWidget(
        question="What is the capital of France?",
        options=["London", "Berlin", "Paris", "Madrid"],
        correct_answer=2,
        explanation="Paris has been the capital of France since the 12th century."
    ))
    multiple_choice_question
    return (multiple_choice_question,)


@app.cell
def _(multiple_choice_question, mo):
    _val = multiple_choice_question.value.get('value')
    mo.md(f"""
    **Student Response:** {_val if _val else 'Not answered yet'}
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Ordering Question
    """)
    return


@app.cell
def _(OrderingWidget, mo):
    ordering_question = mo.ui.anywidget(OrderingWidget(
        question="Arrange these steps of the scientific method in the correct order:",
        items=[
            "Ask a question",
            "Do background research",
            "Construct a hypothesis",
            "Test with an experiment",
            "Analyze data",
            "Draw conclusions"
        ],
        shuffle=True
    ))
    ordering_question
    return (ordering_question,)


@app.cell
def _(mo, ordering_question):
    _val = ordering_question.value.get('value')
    mo.md(f"""
    **Student Response:** {_val if _val else 'Not answered yet'}
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ---

    ## Quiz Results Summary

    You can access the values from all widgets to create a summary or scoring system.
    """)
    return


@app.cell
def _(matching_question, multiple_choice_question, mo, ordering_question):
    def calculate_score():
        score = 0
        total = 0

        _matching_val = matching_question.value.get('value')
        if _matching_val and _matching_val.get('score') is not None:
            total += 1
            if _matching_val.get('correct'):
                score += 1

        _mc_val = multiple_choice_question.value.get('value')
        if _mc_val and _mc_val.get('answered'):
            total += 1
            if _mc_val.get('correct'):
                score += 1

        _order_val = ordering_question.value.get('value')
        if _order_val and _order_val.get('order'):
            total += 1
            if _order_val.get('correct'):
                score += 1

        return score, total

    score, total = calculate_score()
    mo.md(f"""
    ### Current Score: {score}/{total}

    {'🎉 Perfect score!' if score == total and total > 0 else 'Keep going!' if total > 0 else 'Answer the questions above to see your score.'}
    """)
    return


if __name__ == "__main__":
    app.run()
