# Development Procedure for JDAT Notebooks

This document is a description of the JWST Data Analysis Tools Approach to
"Notebook-Driven Development".  The procedures here outline the process for
getting a notebook through sucessive development stages to become something
that can be "live" on the spacetelescope notebooks repository.

These notebooks can have many varied science cases, but follow a relatively
standard workflow:

1. Notebook Concept
2. Notebook Draft
3. XXX Notebook
4. Public/Released Notebook
5. Revised based on Community feedback
6. (Repeat 5 into infinity)

These stages and the process for moving from one to the other are described below.

## Notebook Concept

This stage is generally done by a scientist. The primary purpose of this stage is to record a scientific workflow, but not in actual code. Reasonably often, notebooks can skip this stage if they are simpler or if the underlying tools are already well-enough developed to be immediately implemented.

To begin a notebook at this stage, the notebook author should start with either the notebook template from the [notebook style guide](https://github.com/spacetelescope/style-guides/blob/master/guides/jupyter-notebooks.md) or a blank Jupyter notebook.  They then write out their workflow in words.  Where possible, they put  *example* code of the sort they would *like* to see, even if it's not implemented yet.  For example,  an author might write ``spectral_line = find_line(jwst_miri_spectrum)`` and explain what they expect ``spectral_line`` to be even if the ``find_line`` function doesn't yet exist anywhere.  Once they have the concept ready, they create a pull request with the concept notebook's content.

### New Notebook Pull Request

Submission of a new notebook follows the git Pull Request workflow.  This is not described in detail here because more details are in the [STScI git workflow style guide](https://github.com/spacetelescope/style-guides/blob/master/guides/git-workflow.md).  But don't hesitate to reach out for help from other members of the team if you are stuck or aren't sure how it's supposed to work! 

To submit a concept notebook, the author should first fork and clone the notebooks working space repository: https://github.com/spacetelescope/dat_pyinthesky . Then for a add the new notebook in a sub-directory of the ``jdat_notebooks`` directory with the name of the notebook (see the repo itself for examples).  IMPORTANT: for a concept notebook, also be sure to add the name of the notebook to the ``exclude_notebooks`` file, to prevent the tests from running on the notebook (since it isn't intended to be functional yet anyway).  Once you've added the notebook to git, push it up to your fork and create a Pull Request (see the procedures document linked above for more detail).

One of the team members can then merge your Pull Request.  For concept notebook, nothing more than a cursory review (ensuring just that the notebook is readable and perhaps asking for clarification in a few areas) is necessary for merging.


## Notebook Draft
