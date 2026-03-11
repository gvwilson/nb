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
        FlashcardWidget,
        LabelingWidget,
        MatchingWidget,
        MultipleChoiceWidget,
        OrderingWidget,
    )

    return FlashcardWidget, LabelingWidget, MatchingWidget, MultipleChoiceWidget, OrderingWidget


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
    ## Flashcard Deck
    """)
    return


@app.cell
def _(FlashcardWidget, mo):
    flashcard_deck = mo.ui.anywidget(FlashcardWidget(
        question="Python Concepts — rate yourself on each card:",
        cards=[
            {
                "front": "What does a list comprehension look like?",
                "back": "[expr for item in iterable if condition] — e.g., [x**2 for x in range(10) if x % 2 == 0]",
            },
            {
                "front": "What is the difference between a list and a tuple?",
                "back": "Lists are mutable (can be changed after creation); tuples are immutable (cannot be changed).",
            },
            {
                "front": "What does the `*args` parameter do in a function definition?",
                "back": "It collects any number of positional arguments into a tuple named `args`.",
            },
            {
                "front": "What is a Python generator?",
                "back": "A function that uses `yield` to produce values one at a time, pausing between each, without building the full sequence in memory.",
            },
            {
                "front": "What does `if __name__ == '__main__':` do?",
                "back": "It runs the indented code only when the file is executed directly, not when it is imported as a module.",
            },
            {
                "front": "What is the difference between `is` and `==` in Python?",
                "back": "`==` tests value equality; `is` tests identity (whether two names refer to the exact same object in memory).",
            },
        ],
        shuffle=True,
    ))
    flashcard_deck
    return (flashcard_deck,)


@app.cell
def _(flashcard_deck, mo):
    _val = flashcard_deck.value.get("value") or {}
    _results = _val.get("results", {})
    _complete = _val.get("complete", False)
    _counts = {"got_it": 0, "almost": 0, "no": 0}
    for _r in _results.values():
        _counts[_r["rating"]] = _counts.get(_r["rating"], 0) + 1
    mo.md(f"""
    **Progress:** {len(_results)} card(s) rated —
    ✓ Got it: {_counts['got_it']} &nbsp;
    ~ Almost: {_counts['almost']} &nbsp;
    ✗ No: {_counts['no']}
    {"&nbsp; 🎉 Deck complete!" if _complete else ""}
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
def _(flashcard_deck, matching_question, multiple_choice_question, mo, ordering_question):
    def calculate_score():
        score = 0
        total = 0

        _fc_val = flashcard_deck.value.get('value') or {}
        _fc_results = _fc_val.get('results', {})
        if _fc_results:
            total += 1
            if _fc_val.get('complete'):
                score += 1

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
