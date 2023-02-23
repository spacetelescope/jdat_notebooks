#################
Requirements File
#################

A pip requirements file is a text file, named `requirements.txt`, that contains a list of Python packages needed to
run science notebooks. When users download a science notebook, they need this requirements file to install the necessary
Python packages. Therefore, Notebook Leads will need to provide a requirements file in addition to their notebooks.

**Listing Packages:** Each Python package should be listed in a new line in the requirements file.
You should only list packages imported into your notebook (used in your notebook).
You can make a list of packages by looking though import statements in your notebook.
Packages that are native to Python, such as ``os`` or ``math``, should **not** be listed in the requirements file.

.. tip::

    You can get a list of package versions by running ``conda list`` or ``pip list`` in your terminal.

To specify a version of the package, you can use the ``==`` operator (for example ``astropy==4.1``).
Please list all requirement versions to match the conda or pip environment you used to develop your notebooks.
If you need to add a Python package only available on GitHub, you can list the module as follows:

.. code:: bash

    # Package on GitHub:
    git+https://github.com/name_of_repo

    # If you need to specify a branch:
    git+https://github.com/name_of_repo#branch_name


**Example:** Here is an example requirements file (`requirements.txt`):

.. code-block:: text

    numpy==1.19.1
    jupyter==1.0.0
    aplpy==2.0.3
    astrodendro==0.2.0
    astropy==4.0.1.post1
    matplotlib==3.3.1
    photutils==0.7.2
    scipy==1.5.0
    specutils==1.0
    git+https://github.com/spacetelescope/jwst#0.16.2

.. tip::

    To install packages in a `requirements.txt` file, use ``pip install -r requirements.txt``

.. warning::

    Before installing a new set of packages from a requirements file, one should consider creating a new Conda
    environment. If you need to setup Conda, please see the Conda's
    `Getting Started <https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html>`_ documentation.

Sometimes, the dev team adds an extra requirement file named `pre-requirements.txt`. This file is used for the testing
infrastructure and should be installed before the `requirements.txt`. The notebook lead is not expected to
contribute the `pre-requirements.txt` file.