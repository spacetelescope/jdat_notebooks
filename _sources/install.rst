.. _install:

=========================
Installation Instructions
=========================

You can view rendered versions of the notebooks here,
which require no special tools beyond your web browser.

To download and execute the notebooks, we recommend you clone
the `jdat_notebooks <https://github.com/spacetelescope/jdat_notebooks>`_
repository to your local computer. You can also click the "Download ZIP"
option for the entire repository listed under the green "Code" button at
the top of the repository landing page. You could download individual notebooks,
but it is not as straight forward or recommended, so we do not provide details here.

Most notebooks have additional associated files in their folder,
including a requirements document that lists packages necessary to run the notebooks.
These packages can be installed using `pip <https://pip.pypa.io/en/stable/>`_. The version dependencies are listed in the environment.yaml
and in the requirements file in each notebook folder. You will need Python version 3.9 or higher.

Create Your Local Environment and Clone the Repo
------------------------------------------------

Some of Jdaviz's dependencies require non-Python packages to work
(particularly the front-end stack that is part of the Jupyter ecosystem).
We recommend using `Miniconda <https://docs.conda.io/en/latest/miniconda.html>`_
to easily manage a compatible Python environment for ``jdaviz``; it should work
with most modern shells, except CSH/TCSH.

You may want to consider installing your notebooks in a new virtual or conda environment
to avoid version conflicts with other packages you may have installed, for example::

    conda create -n jdat-nb python=3.11
    conda activate jdat-nb
    git clone https://github.com/spacetelescope/jdat_notebooks.git

Pip Install Notebook Requirements
---------------------------------

Next, move into the directory of the notebook you want to install and set up the requirements::

    cd jdat_notebooks/notebooks/<whatever-notebook>
    pip install -r pre-requirements.txt (if necessary)
    pip install -r requirements.txt
    pip install jupyter
    jupyter notebook
    ## Alternatively, you can use jupyter lab
