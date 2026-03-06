## Process Oriented Guided Inquiry Learning

## Tutorials written in the Socratic / question-interleaved-example style

- CS-POGIL activities (cspogil.github.io):
The CS-POGIL project has produced 58+ classroom-ready guided-inquiry activities for CS courses, spanning Python, data structures, software design, and related topics. The site contains activities and other resources to support using POGIL in Computer Science and related disciplines. Each activity presents a short model (code or output), then drives learners through a sequence of questions to extract a principle, before asking them to apply it. The structure is closely aligned with what you want: tiny examples, no exposition dump, questions before answers. Start at [cspogil.github.io](https://cspogil.github.io).

- SERC POGIL examples collection (serc.carleton.edu):
The Science Education Resource Center hosts a curated set of POGIL activities across disciplines. This pedagogical resource page offers a curated collection of POGIL classroom activities across disciplines such as biology, chemistry, geoscience, and physics, organized by subject and grade level. Although most are not CS-specific, the format — model, then directed questions, then application — is exactly the template you'd adapt for Altair. See [serc.carleton.edu/sp/library/pogil/examples.html](https://serc.carleton.edu/sp/library/pogil/examples.html).

- The UW/IDL Visualization Curriculum (idl.uw.edu):
The Interactive Data Lab at the University of Washington published a full Jupyter-notebook-based curriculum for data visualization with Altair. This notebook will guide you through the basic process of creating visualizations in Altair and is structured as a sequence of tiny working code cells with surrounding prose that raises one question at a time before revealing what adding an encoding does. While it is not explicitly Socratic, its rhythm of "here is one small snippet — now notice what changed" is very close to tldr.sh-style examples. See [idl.uw.edu/visualization-curriculum](https://idl.uw.edu/visualization-curriculum/altair_introduction.html).

- The Altair official tutorial (altair-viz.github.io/altair-tutorial):
The fundamental object in Altair is the Chart, which takes a dataframe as a single argument. The official getting-started tutorial is built entirely as a chain of "here is the minimal thing — what happens if we add one more encoding?" steps. Each cell is 3–5 lines. The tutorial notebooks are at [altair-viz.github.io/altair-tutorial](https://altair-viz.github.io/altair-tutorial) and the source notebooks at [github.com/altair-viz/altair-tutorial](https://github.com/altair-viz/altair-tutorial).

- Nicky Case's "How I Make an Explorable Explanation" (blog.ncase.me):
This is a practical design guide, not a programming tutorial, but it is one of the most explicit treatments of the Socratic principle in interactive learning materials. What makes traditional teaching so ineffective is that it answers questions the student hasn't thought to ask. You have to help them love the questions. Case describes the pattern of starting grounded → ascending by small steps → ending with a sandbox where learners form their own questions. The post is at [blog.ncase.me/how-i-make-an-explorable-explanation](https://blog.ncase.me/how-i-make-an-explorable-explanation/) and the companion design-patterns post is at [blog.ncase.me/explorable-explanations](https://blog.ncase.me/explorable-explanations/).

- freeCodeCamp: "How to Help Someone with Their Code Using the Socratic Method":
This article gives a concrete demonstration of Socratic question sequences applied to debugging, with short code vignettes at each step. Rather than telling the learner how they should think, you guide them to reach the conclusion through their own volition. It is a useful model for how to write question scaffolds around short examples without giving answers away. Available at [freecodecamp.org](https://www.freecodecamp.org/news/how-to-help-someone-with-their-code-using-the-socratic-method/).

## How-to guides for writing this kind of tutorial

- Writing POGIL activities: The main practical guide is Ruder, Brown & Stanford (2020), "Developing POGIL Materials: Writing and Refining Activities for a Spectrum of Content Areas," cited at the [USC Center for Excellence in Teaching](https://cet.usc.edu/incorporating-process-oriented-guided-inquiry-learning-pogil-into-your-teaching/). The POGIL Project's own instructor guide is at [pogil.org](https://pogil.org). The activities help students use experimental setups to discover and build understanding of concepts. Students are asked to use a setup to generate a particular result, then to come up with a rule that explains why the result occurred.

- Explorable Explanations design patterns: Nicky Case's two posts (linked above) are the best practical design guide in this space. Text is best at describing very abstract concepts; graphs are best at showing broad relationships at a glance; interactives are best at showing processes, systems, and models. Start with a hook that provides an overview and motivates the explorer, but doesn't require a lot of upfront knowledge.

- The explorabl.es hub: [explorabl.es](https://explorabl.es) aggregates dozens of examples and links to design resources by Bret Victor, Vi Hart, Amit Patel, and others. Browsing it gives you a feel for what "show a tiny thing, then ask a question" looks like across many domains.

- Bret Victor's "Learnable Programming": The essay at [worrydream.com/LearnableProgramming](http://worrydream.com/LearnableProgramming/) argues that the right question to ask about any programming environment or tutorial is "how does it support reading, following, seeing, and creating?" It is a design philosophy document that directly shapes how you'd structure each short example.

- Wikipedia on Inquiry-Based Learning: Guided inquiry is where the teacher provides only the research question for the students, who are responsible for designing and following their own procedures to test it. The four-level taxonomy (confirmation → structured → guided → open) at [en.wikipedia.org/wiki/Inquiry-based_learning](https://en.wikipedia.org/wiki/Inquiry-based_learning) is useful for calibrating how much scaffolding to provide at each step of your Altair tutorial.

## Practical advice for your specific project

The closest existing precedent for what you're describing (Socratic questions interleaved with 3–5 line runnable examples in a reactive notebook) is probably the POGIL-for-CS activities combined with the Altair tutorial's cell-by-cell rhythm. The key structural move in both POGIL and Nicky Case's explorables is that *the example comes before the question, not after*. You show a minimal working snippet, the learner runs it and sees output, and only *then* you ask "what would happen if you changed `mark_point` to `mark_bar`?" or "why do you think the x-axis label reads `Horsepower` and not `Q`?". This is different from traditional tutorials, which explain first and demonstrate second.
