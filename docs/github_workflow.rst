.. _GitHub Workflow:

#######################
Git and GitHub Workflow
#######################

This section outlines the Git and GitHub workflow.
Each time you update your notebook, follow the instructions below to "save" your changes.
The workflow outlined in the sub-sections below can be summarized with the following set of commands:

.. code:: bash

    # cd into directory
    cd notebooks<name_of_your_folder>

    # Check status
    git status

    # Add files to commit
    # For each file, run:
    git add <file_name>

    # Check status (files added should be in green)
    git status

    # Commit with comments
    git commit -m "short description of changes"

    # When ready to upload, Push to your fork
    git push <your_github_username> <branch_name>


**Step 1: Prepare Files Locally**

Next step is to create or update your files to your local repository before uploading them to GitHub.
As mentioned `above <GitHub Submissions>`_, create a new folder with your project name in the
`notebooks` directory. Add your :ref:`Science Notebooks <Jupyter Notebooks>` and
:ref:`requirements files <Requirements File>` into the new folder. Please make sure to
:ref:`clear cell ouputs <Clearing Notebook Outputs>` in your notebooks before continuing.

.. note::

    Remember to clear all cell outputs in your notebooks.
    See the :ref:`Clearing Notebook Outputs` for instructions.

**Step 2: Add**

Using your terminal, you must first ``cd`` into the folder you created:

.. code:: bash

    cd jdat_notebooks/notebooks/<name_of_your_folder>

Check Status: First step is to check what changes are available to be added and committed to the repository history.
To get a list of changes and their status, run:

.. code:: bash

    git status

This will return a list of files that have been added to the local repository. Files that are not staged for commit, are
highlighted in red. Files staged for commit are listed in green. To select file to be staged for commit, you must first
"add" them. Thing of "adding" as selecting which files you want to include in your commit.

Add Files to Upload: To add files to commit, run the following command for each file:

.. code:: bash

    git add <file_name>

Check Status Again: After adding the files, you should check one more time if the files you intend to commit are
staged. To do this, run:

.. code:: bash

    git status

This time the files you selected should be in green font under `Changes to be committed`.

**Step 3: Commit**

Now you may commit the files to your local git history. When you commit changes, you should leave short
comments describing the changes being introduced in the commit. To add a comment, you can append ``-m "comments"`` at
the end of the commit command. To commit changes with a comment, run the following command:

.. code:: bash

    git commit -m "short description of changes"


**Step 4: Push**

You can now push (upload) the changes to your GitHub fork. To do this, run the following command:

.. code:: bash

    git push <your_github_username> <branch_name>

.. tip::

    If you are not sure what branch you are working on, run ``git branch``

You will be prompted for your GitHub user name and password. After entering your credentials, your changes will be
uploaded to your GitHub fork (online copy).