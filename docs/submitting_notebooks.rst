####################
Submitting Notebooks
####################

.. _jdat_notebooks: https://github.com/spacetelescope/jdat_notebooks

This section outlines how to submit notebooks.
New notebooks development occurs in the `jdat_notebooks`_ repository. As such, new notebooks should be submitted by
making a pull request (PR) in the ``STSCI jdat_notebooks`` repository
(this is the :ref:`Pre-Baseline Stage <draft stage>`). After the :ref:`Review process <review process>`, the notebooks will be merged
(this is the :ref:`Baseline Stage <baseline stage>`). 

**What to Submit**:

1. :ref:`Data Files` (Upload to :ref:`Box <Box Submissions>`).
2. :ref:`Jupyter Notebooks` (Upload to :ref:`GitHub <GitHub Submissions>`).
3. :ref:`Requirements File` (Upload to :ref:`GitHub <GitHub Submissions>`).

|
Check List
**********

Before and after submitting your notebook, requirement files and data, please make sure the following items are in order:

.. code:: text

    - [ ] Box:

        - [ ] Data has been uploaded to box.
        - [ ] The data is bing shared via link. Make sure the settings allow for anyone with a link to download.

    - [ ] GitHub:

        - [ ] Notebook has all cell outputs cleared out.
        - [ ] Notebook is written in `Python 3`
        - [ ] All imports occur at the beginning of the notebook.
        - [ ] All data is loaded into the notebook via a URL from box. (No local files being used).
        - [ ] Verify that the python code satisfies PEP 8.
        - [ ] Comments and unused lines of code are removed.
        - [ ] `requirements.txt` file is included.

.. tip::

    If you copy and paste this checklist into your PR as a comment or description, it will render as a checklist with
    radio buttons you can toggle any time.

.. _Box Submissions:

Box Submissions
***************

All data files should be uploaded to STScI's box folder and made sharable via URL.
All notebooks should use human readable URLs in the notebooks when loading/reading data.
For instructions on submitting data files, please visit the :ref:`Uploading Data to Box <Data Files>` section.

.. _Github Submissions:

GitHub Submissions
******************

:ref:`Science Notebooks <Jupyter Notebooks>` and :ref:`requirements files <Requirements File>` files should be submitted
by making a pull request against the `main` branch of the STScI `jdat_notebooks`_  repository. For instructions on
how to create a GitHub pull request, please see the :ref:`GitHub Guidelines <GitHub PR>`.

 important::

    New notebooks should be added to the `jdat_notebooks/notebooks` directory.

You must first create a new folder in the `jdat_notebooks/notebooks` directory and name the new folder something
relevant to the topic of the notebooks being submitted (think of this a short title).
For example, `jdat_notebooks/notebooks/spectral_fitting`.
This "title" will also be used to name the folder on Box containing the :ref:`data files <Data Files>` used by the
notebook. After creating a new folder and naming it, please place all notebooks and requirement files inside of it.

The folder name ("short title") should be:

- Related to the topic of the notebooks.
- Unique to avoid confusion/conflicts with existing notebooks.
- Reasonable in length (makes navigating in a terminal easy).
- All small letters.
- Using underscores instead of spaces. For example "spectral fitting" -> "spectral_fitting"

|
Review Process
**************

After creating a Pull Request (PR), your PR will undergo a science and technical review.
The automatic testing infrastructure will also attempt to render your notebook. Reviewers will leave comments in your
PR with suggested changes or give their approval. If changes are recommended or requested, you can
:ref:`update your PR <Updating Your PR>` via the steps described in the :ref:`Git and GitHub Workflow <GitHub Workflow>` section. Once the
all reviewers approve and the automated tests pass, the PR will be merged into the official STScI repo.


