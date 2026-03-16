# Marimo Notebooks for Educators

## Introduction

-   what *is a notebook?
    -   *literate programming* mixes prose and software in a single "runnable paper"
    -   each *cell* is prose or software
    -   prose typically written in Markdown
    -   software written in whatever programming languages the notebook supports
    -   software's output displayed in the notebook as well
-   why notebooks for everyday work?
    -   easier to understand (think about the way textbooks present material)
    -   improves reproducibility
-   why notebooks for learning?
    -   more engaging than static material: learners can experiment with settings, alter code, etc.
    -   no installation required: notebooks can be hosted so learners don't have to struggle with the hard bits first
    -   less intimidating than jumping straight into scripting
    -   introduces a real-world tool
-   why notebooks for teaching?
    -   all of the above…
    -   create interactive lecture material in a single place
-   why the Marimo notebook?
    -   more than Notebook but not as intimidating as VS Code
    -   doesn't allow out-of-order execution of cells
    -   plays nicely with other Python tools (because a notebook is a Python file)
    -   plays nicely with version control (same reason)
    -   configurable interaction with AI tools
    -   open source
-   why *not* Marimo?
    -   not yet as widely known as Jupyter (i.e., your IT department may not already support it)
    -   not yet integrated with auto-grading tools (we're waiting to see what you want)
    -   limited set of embeddable formative assessment tools (ditto)
    -   doesn't yet support multi-notebook books
    -   some quirks that might not make it the right tool for a CS-101 course (discussed below)

## Ways to Use the Notebook

-   macro
    -   follow along with lesson (code already present)
    -   workbooks for assignments ("fill in these cells")
    -   keep your own lecture material in sync
    -   notebooks as apps (play with data rather than write code)
    -   notebooks as lab reports (models real-world use)
-   micro
    -   scroll through a notebook
    -   step through a notebook by executing the cells in order
    -   fill out details or values into a mostly complete notebook
    -   tweak or flesh out a notebook with some content
    -   add content to a completely blank notebook
    -   ask learners what to add *or* what's going to happen
    -   ask AI to do something and then explore/correct/improve its output

## Pedagogical Patterns

## Shift-enter

-   description
    -   learner starts with complete notebook, re-executes cells
    -   (possibly) fills in prose cells with analysis/description
-   use for
    -   introduce new topics
    -   check understanding (e.g., warmup exercise)
-   audience
    -   any
-   format
    -   synchronous (i.e., in class or in real time online)
-   pro
    -   gives learners a complete working example
-   con:
    -   low engagement

## Fill in the blanks

-   description
    -   some code cells filled in, learner must complete
-   example:
    -   fill in a function used by other cells
-   use for
    -   focus attention on a specific concept (e.g., filtering data)
-   audience
    -   any
-   format
    -   assignments and labs
-   con:
    -   "just get AI to do it"
    -   required work can be too easy or too hard

## Tweak and twiddle

-   description
    -   learner starts with a complete working notebook
    -   asked to alter parameters to achieve some goal
-   example:
    -   explore sensitivity of clustering algorithm to various parameters
-   use for
    -   compare-and-contrast
    -   acquiring domain knowledge
-   audience
    -   learners without programming experience
    -   usually requires domain knowledge
-   format
    -   fixed-time workshop exercise
    -   pair programming
-   pro
    -   helps learners overcome code anxiety
-   con:
    -   "where do I start?"
    -   going down a rabbit hole

## Notebook as app

-   description
    -   use notebook as interactive dashboard
    -   usually keep prose in a separate document (to make the notebook look like an app)
-   example
    -   load and explore datasets
-   use for
    -   acquiring domain-specific knowledge
-   audience
    -   non-programmers
-   format
    -   use instead of slides in lecture (but know where you're going)
    -   have learners suggest alternatives to explore
    -   data analysis after (physical) lab
-   pro
    -   less effort to build than custom UI
-   con
    -   requires testing
    -   does not develop programming skills

## First day / top-down delivery

-   description
    -   give learners just enough control to get an exciting answer on day one
-   example
    -   fluid flow notebook that hides details
-   use for
    -   follow-along lectures
-   audience
    -   any
-   format
    -   tutorials and workshops (synchronous)
-   pro
    -   student engagement
-   con
    -   hard to get the right level of detail

## Coding as translation

-   description
    -   convert mathemematics to code or vice versa
-   example
    -   given description of data cleanup steps, write the code
    -   given statistical code, explain what it's doing
-   use for
    -   connect concepts to math
-   audience
    -   learners who understand theory but struggle with programming
-   format
    -   notebook with (some) explanatory text and (some) scaffolded code
-   pro
    -   lower the barrier for students with low programming knowledge
-   con
    -   if the task is still too hard, students will be turned off

## Symbolic math

-   description
    -   use SymPy for symbolic math in notebook
-   example
    -   the Euler equations
-   use for
    -   connect symbolic math to software
-   audience
    -   STEM students interested in theory
-   format
    -   any of the previous formats (content is different)
-   pro
    -   introduce another way to interact with computers
-   con
    -   math in SymPy is yet another thing to learn
    -   and SymPy has a few rough edges in Marimo

## Numerical methods and simulation instead of calculation

-   description
    -   some concepts are easier to understand via simulation or numerical analysis
-   example
    -   queueing theory
-   use for
    -   make concepts tangible before introducing mathematical abstraction
-   audience
    -   learners must be able to program
-   format
    -   any
-   pro
    -   go from specific to general
-   con
    -   requires programming skill

## Learn an API

-   description
    -   introduce a key API example by example
-   example
    -   Polars
-   use for
    -   putting focus on tools to be used in other places
-   audience
    -   programmers
-   format
    -   examples in order of increasing complexity
-   pro
    -   guide learning in a sensible order (which AI still struggles with)
-   con
    -   can't see the forest for the trees
    -   learners may prefer just asking AI

## Choose your data

-   description
    -   replace the dataset used in a notebook with another one
    -   that may be different enough to require modifications to code
-   example
    -   replace one census with another
    -   or one genomic assay with another
    -   or one sport with another
-   audience
    -   learners with specific domain interest (e.g., sports analytics)
-   format
    -   common first half, learners explore on their own for second half
    -   create a presentation
-   pro
    -   students' feeling of self-efficacy
    -   engagement with real-world data
-   con
    -   can't find data
    -   or data is too messy

## Test driven development

-   description
    -   instructor provides a notebook full of tests
    -   learner must write code to make those tests pass
-   example
    -   build data cleanup code
-   use for
    -   learners who want firm goalposts
-   audience
    -   programmers
-   format
    -   works well for homework exercises
-   pro
    -   helps students stay focused on well-defined task
-   con
    -   very easy to have AI generate the code

## Bug hunt

-   description
    -   give learners a notebook with one or more bugs
    -   can use AI to generate different bugs for different learners
    -   note that misleading prose counts as a bug
-   example
    -   notebook uses wrong statistical test
-   use for
    -   developing critical reading skills
-   audience
    -   programmers
-   format
    -   suitable for homework
-   pro
    -   some learners enjoy tracking down bugs
    -   it's a useful skill to learn
-   con
    -   calibrating bug difficulty to learner level

## Adversarial programming

-   description
    -   given a notebook with code, write calls that break it
-   example
    -   naive analysis that trusts all CSV files to be correctly formatted
-   use for
    -   learn critical thinking (and how to write tests)
-   audience
    -   programmers
-   format
    -   provide code and prose
    -   to be extra evil, deliberate mis-match between code and description
-   pro
    -   helps learners appreciate how hard it is to write good code
-   con
    -   learners break code in the wrong ways (e.g., six different illegal strings instead of just one)
