# James Webb Space Telescope Data Analysis Tool Notebooks

.. note::

   ``jdat_notebooks`` are one component of STScI's larger `Data Analysis Tools Ecosystem <https://jwst-docs.stsci.edu/jwst-post-pipeline-data-analysis>`_.

   .. note::

   ``jdat_notebooks`` are intended for the broader science community.  If you wish to contribute notebooks or technical expertise, we refer you to `dat_pyinthesky <https://github.com/spacetelescope/dat_pyinthesky/tree/master/jdat_notebooks>`_.


# Development Procedure for JDAT Notebooks

This document is a description of the JWST Data Analysis Tools (JDAT) Approach to
"Notebook-Driven Development".  The procedures here outline the process for
getting a notebook through successive development stages to become something
that can be "live" on the spacetelescope notebooks repository.

These notebooks can have many varied science cases, but follow a relatively
standard workflow:

1. Draft Stage
2. Baseline Stage
3. Notebook-driven development
4. Advanced Stage
5. Final Notebook - Maintenance Stage
6. Revision based on Community feedback

These stages and the process for moving from one to the other are described below.

**The procedure to submit the notebook via a Pull Request is described at the end of this document.
This is repeated for each of the 5 stages.**

Note that there is much more information on writing Jupyter notebooks at the
[STScI notebook style guide](https://github.com/spacetelescope/style-guides/blob/master/guides/jupyter-notebooks.md),
and similar guidance for Python code at the
[STScI Python style guide](https://github.com/spacetelescope/style-guides/blob/master/guides/python.md).
These guidelines are in place to make review steps easier.

## Draft Stage

The primary purpose of this stage is to record a scientific workflow, but without including actual code.
This stage is generally done primarily by a scientist. Reasonably often, notebooks can skip this stage
if they are simpler or if the underlying tools are already well-enough developed to be immediately implemented.

To begin a notebook at this stage, the notebook author should start with either the notebook template
from the [notebook style guide](https://github.com/spacetelescope/style-guides/blob/master/guides/jupyter-notebooks.md)
or a blank Jupyter notebook.  They then write out their workflow in words.  Where possible, they put
*example* code of the sort they would *like* to see, even if it is not implemented yet.
For example, an author might write this in such a notebook:
```
In [ ]: spectral_line = find_line(jwst_miri_spectrum)

`spectral_line` should be a list of line centers and names of lines indexed by spaxel,
found using a derivative-based line-finder.
```
even if the ``find_line`` function doesn't yet exist anywhere.

The top-level header of the notebook (i.e., the title) should have "Draft: " at the start
to make it clear this is a draft notebook.  The filename should *not* have `draft` in it,
however, as the filename will generally remain the same throughout the later stages.

Once they have the draft ready, the author should create a pull request with the draft notebook's content (see
instructions at the end of this document).


## Baseline Stage

The primary purpose of this stage is to get a functioning notebook to record a workflow.
This stage is also typically done by a scientist (although with developers available to ask questions).
It is also frequently the *first* step of development.  That is, if the workflow is already reasonable
to implement with existing tools, the draft notebook is not necessary.

In this stage the notebook should actually execute from beginning to end, but it is fine to be
"rough around the edges".  E.g., the notebook might have several cells that say things like:
```
...
In [ ]: spec = Spectrum(np.linspace(a, b, 1000)*u.angstrom, some_complex_function(...))
```

the scientist might think this is too complicated, and so to communicate their desire for an improved
workflow, they create a "Developer Note". A developer note should be a part of the notebook itself and should be a
single markdown cell (not code cell - code examples in a dev note can be done as literal markdown blocks - i.e.
surrounded by `\`\`\`` for blocks or \` for inline code). That cell should begin with the text ``*Developer Note:*``.
E.g., a markdown cell might be added below the above cell in a notebook, which would say:

```
*Developer Note:*
Creating the spectrum above is a bit complicated, and it would improve the workflow if there was a single
simple function that just did `spec = simulate_jwst_spectrum(a, b)`.
```
thereby providing guidance for where specific development would simplify the workflow.

If a notebook is freshly created in this form, the author can follow the "Procedure to submit a notebook as a Pull Request"
(found at the end of this document), skipping the Draft Stage step.

If the notebook was already created in the Draft Stage step and the "Procedure to submit a notebook as a Pull Request"
has already been followed, the author should just create a new branch to modify the existing code and then create
a new Pull Request with the changes once they are ready.

In either case, the title (but not filename) of the notebook should begin with
"Baseline:" to indicate the notebook is in the Baseline Stage.

Once the Pull Request has been created, the notebook will automatically be built in the repository
so that reviewers can view it. Reviewers can then comment on the notebook in Github.  At this stage
the bar is still relatively low for review - primarily things like ensuring the notebook does run from
beginning-to-end and that data files or the like were not accidentally committed to the repository.

Finally, there are three important technicalities for notebooks that become relevant at this stage
(and continue for future stages):

1. The output cells of a notebook should *always* be cleared before a git commit is made.
Notebook outputs can sometimes be quite large (in the megabytes for plots or the like), and git is intended
for source code, not data. Clearing the outputs also ensures the notebook can be run from beginning to end and
therefore be reproduced by others.
2. Any data files required for a notebook need to be accessible by others who may be reviewing or testing the notebook.
The [STScI guidelines on data storage for notebooks](https://github.com/spacetelescope/style-guides/blob/master/guides/where-to-put-your-data.md)
should be followed here.  The specific addition for the JWST Notebooks is that notebook data should be
in the `DMD_Managed_Data/JWST/jwst-data_analysis_tools` Box folder (or subfolders thereof).
If you do not have access to this box folder already, ask a Project Scientist and they should be able to get you added.
Note that if a baseline notebook is using data that should not yet be public, the easiest choice is probably central store,
but in that case it is critical that the notebook state prominently that it must be run inside the STScI network.
3. A notebook should state clearly what version of various dependencies were used to generate the notebook.
These versions should be placed in a `requirements` file in the same directory as the notebook itself. An example of this file
is in the``example_notebook`` folder.
That will ensure reviewers/testers can be sure that if they encounter problems, it is not due to software version mis-matches.

The notebook will undergo a scientific and a technical review, which might also yield additional developer notes.  It will then
be merged into the repository once the review comments have been addressed. This concludes the Baseline Stage.

## Notebook-driven development

Along and after the Draft and Baseline stages, there is potential for considerable development
to be necessary.  A baseline notebook may contain a large number of areas where more development is desired in data
analysis tools, or it may only require a few minor adjustments (or none at all!).  This stage is therefore the most
flexible and dependent on developer resources, etc.  In general the intent is for developers to be able to re-use
bits of code from the notebook as tests for development, while occasionally (if necessary) asking the notebook
author for guidance to ensure the implementation actually meets the notebook's needs.  There is not a formal
process for this step, but it is intended that the JDAT planning process (currently on Jira) keeps track of specific
steps needed before a given notebook can proceed on to the next stage.

## Advanced Stage

Once a baseline notebook has been completed, the next stage is to build the baseline into a notebook that uses the DAT's
or associated community-developed software as consistently as possible.  This is typically done via a developer
reviewing a baseline notebook and working with the scientist to develop
additional DAT code, particularly focused on resolving the "developer notes".  It is at the discretion of the notebook
author and developer together which of them actually modifies the notebook and sources the Pull Request, but it is
likely both will be involved to some degree. An example approach is for the developer to take the baseline notebook,
mark it up with comments like (using the example from above):
```
*Developer Note:*
...
In [ ]: spec = Spectrum(np.linspace(a, b, 1000)*u.angstrom, some_complex_function(...))

Creating the spectrum above is a bit complicated, and it would improve the workflow if there was a single simple function that just did ``spec = simulate_jwst_spectrum(a, b)``

*Development:*
This has now been implemented as JWSTSimulator.make_spectrum(a, b, anotherparameterthatturnsouttobeimportant).  Can you try that and ensure it works here?
```
and then create a git commit with these comments.  The original author would then address the comments in a
follow-on commit.  There might be multiple pull requests of this sort as the notebook driven development
continues.  But once all developer notes have been addressed, the developer and author can declare the notebook
ready to be called "Advanced".

Once the notebook authors (original author and developer/reviewer) have agreed it is ready, one of them follows
the Pull Request workflow as described above, but with the notebook title now changed to be just
the title itself (no "Draft:" or Baseline:"). The Pull Request is then reviewed by one of the project scientists, and merged when
everyone is satisfied with the notebook.

## Final Notebook - Maintenance Stage

The final stage for the notebook is release on the
[official STScI notebook repository](https://github.com/spacetelescope/notebooks).
Specific documentation for this last stage is given in the repository itself.  However, that repository and the
working repository here have very similar structure, so it is in principle simply a matter of copying the advanced
notebook over to a form of the release repository and doing one final Pull Request.  Note, however, that other
STScI reviewers may comment on this stage.  It is also important for the authors to do an additional check over
the notebook to ensure that it uses *released* (not developer) versions of requirements where possible. It is also
a good opportunity to fill in the scientific context of a given notebook - e.g. add a motivation section, or a final
plot at the bottom that shows the final science result.  Once this is done, and the Pull Request merged, the notebook
can be declared complete.

## Revision based on Community feedback

Of course, science does not stand still!  As time passes some of the completed notebooks may have enhancements
or changes necessary.  In general these follow the standard Pull Request workflow and can be submitted by anyone
once the notebook is public (both in and out of STScI).  While the repo maintainers manage this process, the notebook
authors may be called in from time to time to provide opinions or perspectives on any proposed changes.

# Procedure to submit a notebook as a Pull Request

Submission of a new notebook follows the Github Pull Request workflow.  All details are in the
[STScI git workflow style guide](https://github.com/spacetelescope/style-guides/blob/master/guides/git-workflow.md).
Here we give a "cookbook" procedure,
but do not hesitate to reach out for help from other members of the team if you are stuck or are not sure how
it is supposed to work!

Note also that these steps are slightly different for if you update a notebook after you've created the first pull request - you can skip steps 1-3 and 5.

1. Go to the github working space https://github.com/spacetelescope/dat_pyinthesky and fork the repository to your user account
(button "Fork" in the top right corner).

2. Clone the repository locally on your machine

``git clone git@github.com:username/dat_pyinthesky.git``

3. While this sets up ``origin`` to point to your fork, there is currently no connection to the main ``spacetelescope`` "upstream" repository.  So you can point your local clone to the right repository by doing:

``git remote add upstream https://github.com/spacetelescope/dat_pyinthesky.git``

4. Create a new branch where to start the development and move to that branch

``git branch new_notebook_branch_name``

``git checkout new_notebook_branch_name``

5. Create a new folder where to develop the notebook

``cd jdat_notebook``

``mkdir new_notebook_name``

6. Now start building your notebook (new_notebook_name.ipynb)!

7. At any point in the development, save your work and push it up to your forked repository. (Important: you must clear the outputs on your notebook using the Jupyter interface before doing an ``add/commit`` like this.)

``git add new_notebook_name.ipynb``

``git commit -m "Clear message to state the fix or improvement to the notebook"``

``git push origin new_notebook_branch_name``

(sometimes you have to reset the upstream, so in that case it is ``git push --set-upstream origin new_notebook_branch_name``)

8. When you are happy with your notebook, double check that you have satisfied the thecnical requirements of the specific status
of your notebook (see above).

9. Now you can create a Pull Request from the ``spacetelescope/dat_pyinthesky`` repository. You do that
by clicking on ``New pull request`` on the webpage, then the link ``compare across forks``. Then set the base repository
to ``spacetelescope/dat_pyinthesky`` and branch ``master`` and the head fork to
the branch on your personal fork, so repository ``username/dat_pyinthesky`` and branch ``new_notebook_branch_name``. You
set a title and you click on ``Create pull request``.

One of the team members can then merge your Pull Request.
