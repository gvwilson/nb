# Learner Personas

## Anya Academic

1. **Background:** Biology professor at mid-sized state university; teaches undergrad microbiology and biostatistics classes, both of which emphasize data management and visualization.
2. **Relevant Experience:** Used R for 15 years, switched to Python three years ago, but has never done "a real computer science course". Frequently remixes teaching material she finds online, particularly examples.
3. **Goals:**
    1. Wants to equip her students with modern skills, especially AI-related, both because she thinks they're important and to increase student engagement.
    2. Wants more recognition at her university for her teaching work, which she believes is more likely to come from publishable innovation than from high student evaluations.
    3. Would like to get student engagement back to pre-COVID levels; she feels that today's cohorts don't know each other as well and aren't as excited about material because of the shift to online education.
4. **Complications:**
    1. Is concerned about tool setup and maintenance overheads. Doesn't have time to completely rewrite courses, so will only move over if there's an incremental migration path that allows her to back out if thing don't appear to be working.
    2. Anya's department has two overworked IT staff, and nothing at her university is allowed to go beyond the pilot phase if it doesn't integrate with the LMS somehow.

## Ellis Engineer

1. **Background:** Senior undergraduate in mechanical engineering who just returned to school from their third and final co-op placement with Oliver Overstory's company. They are very excited about drones…
2. **Relevant Experience:** Has been using Jupyter notebooks with Colab since their second semester. They are comfortable with NumPy and Altair and has bumped into Pandas, but has done as many classes with MATLAB and AutoCAD as with Python.
3. **Goals:**
    1. Ellis wants to create an impressive senior project to secure themself a place in a good graduate program (which they think is essential to doing interesting work with drones). They have seen custom widgets in notebooks, and are willing to invest some time to learn how to build one with AI support.
    2. They also want to explore small-craft aerodynamics, particularly feedback stability problems, out of personal interest and as a way to become part of the "serious" drone community.
4. **Complications:**
    1. Is already invested in Jupyter; will need to be convinced that Marimo is better in some tangible way.
    2. Doesn't find out-of-order execution or "plays nicely with version control" compelling: their computer is powerful enough that they can re-run notebooks when they need to, and they are used to single-author notebooks.

## Nang Newbie

1. **Background:** Undergraduate business student; decided not to bother minoring in CS because "AI is going to eat all those jobs". Nang chooses courses, tools, and interests based primarily on what the web tells him potential future employers are going to look for. He routinely uses ChatGPT for help with homework.
2. **Relevant Experience:** Used Scratch in middle school and did one CS class in high school that covered HTML and a bit of Python, and got far enough to build a Wordle clone that almost worked. He just finished an intro stats class that used Pandas and Altair in hosted Jupyter notebooks. Nang enjoyed his intro stats class enough to sign up for the sequel.
3. **Goals:**
    1. Nang wants to be able to do homework assignments more quickly and with less effort (hence his interest in ChatGPT).
    2. He wants to learn how to explore and analyze sports statistics for fun (he's a keen basketball fan), and to share what he finds with like-minded fans through online forums.
4. **Complications:**
    1. Nang is taking five courses and volunteering with two campus clubs (one for the sake of his CV, and one because of his passion for basketball), so he is chronically over-committed.

## Oliver Overstory

1. **Background:** Master's degree in geography, now a GIS expert at a 100-person company that builds models of forest cover using satellite and drone imagery.
2. **Relevant Experience:** Has been using Jupyter notebooks for several years for his own work and to build simple dashboards for other analysts at his company. Those analysts have to edit the cells in the notebook to change input files or parameters, which many are reluctant to do; Oliver finds this reluctance frustrating.
3. **Goals:**
    1. Wants his colleagues to make more use of the dashboards he builds, but doesn't want to have to learn anything about CSS or JavaScript. (Despite all the visualization he does, he doesn't think of himself as a graphical person.)
    2. Wants to turn what he's learned into a training course complete with an interactive textbook. Oliver realizes this is going to be a big investment, and wants to be sure he picks tomorrow's tools. (He recently migrated all his projects to uv, Pydantic, and DuckDB for this reason.)
4. **Complications:**
    1. Oliver wrote his thesis with LaTeX and won't use tools that don't provide equivalent support for math, bibliography management, cross-referencing figures and tables, etc.

## Yani Youtuber

1. **Background:** A nutritionist who became a minor YouTube celebrity thanks to a series of videos analyzing popular foods. Volunteering with food awareness programs at her local library led her to start blogging, which in turn led to making short videos.
2. **Relevant Experience:** Learned a bit of web design as a teenager through online courses and experimentation, but did a bachelor's degree in nutrition as a safe career option. Has a practical rather than theoretical understanding of statistics.
3. **Goals:**
    1. Yani enjoys the supplemental income she get from her YouTube channel, and would like to see it grow. She is therefore looking for tools that will allow her to make more engaging videos.
    2. She cares more about educating the public on food-related topics, especially the harm done by ultra-processed foods, so is also looking for tools that high schoolers and interested laypeople can use to play around with data on their own.
4. **Complications:** Is currently using R, ggplot2, and Quarto to create visuals rather than Python-based tools. Identifies more with the R community (especially R-Ladies) than with the tools themselves.

## Analysis

1. **Anya** is the gatekeeper for a large number of potential adopters
    1. Providing her with notebooks she can remix to fit into her existing course gives her a chance to try things out
    2. Particularly if those notebooks are versions of things she knows students are already interested in (e.g., Yani's nutrition examples)
    3. She will only care about auto-grading, integration with LMS, etc. *after* she is convinced that switch to Marimo will be low effort
2. **Ellis** is probably the easiest person to convince, but won't have wider impact
3. **Nang** is not a direct target
    1. Hard for us to get and keep his attention in a crowded, noisy world
    2. He won't commit unless/until he believes Marimo is a winner
        1. Note: "my prof says so" isn't going to convince him
    3. Best way to reach him is through the Yanis of his community
        1. If one of the sports data analysts he follows online gives Marimo a shot, Nang will try it out
4. **Oliver** is *not* initially a focus
    1. Even if he adopts Marimo, his work won't have an impact in the next 12-18 months
    2. But if we can convince him now, he can convince others on our behalf via his book
5. **Yani** is the highest value
    1. But it will be hard to persuade her to switch (R is not just a tool, it's a community)
    2. However, she would support someone else translating her work into Marimo notebooks, and would publicize their existence if she liked the result
