Josh Veitch-Michaelis <veitchmichaelisj@ufl.edu>

Here is the notebook I'd suggest converting: https://github.com/Restor-Foundation/tcd/blob/main/notebooks/tiling.ipynb (high level docs here https://restor-foundation.github.io/tcd/).

I think it's a good example because (a) it should work and the important data are self-contained in the repo, but as the outputs are plots and their propensity to change, I cleaned it before checking in. (b) it should work - but if not it's an opportunity to test the AI tools to fix it up (c) it's vintage hand-written code! and (d) you could easily add in some interactivity for some of the tiling settings for exposition. Nowadays it's the sort of thing I would have render as part of a doc CI, but wasn't a huge priority at the time.

Something I I've always liked about notebooks is experimenting with how a user would interact with the code and treating it as doc-driven development. I recently learned that Knuth coined literate programming and of course, now I check, it's actually mentioned in the intro to Jupyter. For context that was my aim when I wrote this notebook. I find that much more intuitive than running a test suite and I think students probably do as well.

You can ignore the last few cells which are a demo of this working on some enormous imagery. This is classic research code where you can't actually reproduce it without the (public, but heavy) data. If this were on Colab, I would include a download cell, but I don't want users to pull several GB just to prove my point that the library is memory efficient...
