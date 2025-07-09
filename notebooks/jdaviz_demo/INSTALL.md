# Setup and Installation Instructions for Jdaviz demo

To run all the demo notebooks on your own computer, you will need
a Python environment configured with the required packages (and data).
These instructions describe setup using `git` and `Miniconda`.

If you have any problems with any of these steps, please
feel free to [submit an issue](https://github.com/spacetelescope/jdaviz_demo/issues)
or send an email to Cami at cpacifici@stsci.edu.

For the commands shown, `%` (and anything to the left of it) represents
the terminal prompt. You do not need to copy it; instead only copy the
command to the right of `%`.


## 1. Install Miniconda (if needed)

*Miniconda is a free minimal installer for conda. It is a small,
bootstrap version of Anaconda that includes only conda, Python, the
packages they depend on, and a small number of other useful packages,
including pip, zlib, and a few others. If you have either Miniconda or
the full Anaconda already installed, you can skip to the next step.*

In a terminal window, check if Miniconda is already installed.

    % conda info

If Miniconda is not already installed, follow
these instructions for your operating system:
https://conda.io/projects/conda/en/latest/user-guide/install/index.html.
Please be sure to install a **64-bit version** of Miniconda to ensure
all packages work correctly.

(On native Windows, you might also need [additional
compilers](https://github.com/conda/conda-build/wiki/Windows-Compilers),
although this should not be necessary in WSL).


## 2. Check your conda installation

Open a terminal window and verify that conda is working:

    % conda info

If you are having trouble, check your shell in a terminal window:

    % echo $SHELL

then run the initialization if needed, in that same terminal window:

    % conda init `basename $SHELL`

You should open a new terminal window after `conda init` is run.

It is advisable to update your conda to the latest version. We recommend
a minimum version of 23.10.0. Check your conda version with:

    % conda --version

Update it with:

    % conda update conda

or

    % conda update -n base conda


## 3. Install git (if needed)

At the prompt opened in the previous step, enter this command to see
whether git is already installed and accessible to this shell:

    % git --version

If the output shows a git version, proceed to the next step. Otherwise
install git by entering the following command and following the prompts:

    % conda install git


## 4. Clone this repository, or download a ZIP file

If using `git`, clone the workshop repository using
[git](https://help.github.com/articles/set-up-git/):

    % git clone https://github.com/spacetelescope/jdaviz_demo.git

If you elect not to use `git`, you can download
the ZIP file by opening the green *Code* button at
https://github.com/spacetelescope/jdaviz_demo and selecting
*Download ZIP*.


## 5. Create a conda environment for the workshop

*Miniconda includes an environment manager called conda. Environments
allow you to have multiple sets of Python packages installed at the
same time, making reproducibility and upgrades easier. You can create,
export, list, remove, and update environments that have different
versions of Python and/or packages installed in them.*

Create and activate a new Python 3.12 environment for the workshop
called jdaviz:

    % conda create -n jdaviz python=3.12 -y
    % conda activate jdaviz

The name of the new conda environment created above should be displayed next
to the terminal prompt: `(jdaviz) %`


## 6. Install the required packages and data

Jdaviz comes with a series of packages like astropy, matplotlib, Jupyter,
and others.
To be able to work with instrument footprints we will need to install
pysiaf and for data sonification we will need strauss. **Here are three versions
of the same command (you do not have to run all three).** I would recommend using
the last one since there are a couple of interesting things we can look
at in the not-yet released version.

Here is the basic command:

    % pip install jdaviz pysiaf strauss

If (like me) you have a large number of conda environments with various
versions of the same packages, you might want to add `--no-cache-dir`
to be sure to get the latest versions of the required packages for the
latest jdaviz. The command will look like this:

    % pip install jdaviz pysiaf strauss --no-cache-dir

If you want to use the developer version of jdaviz, you can install
directly from github with the following commands:

    % pip install pysiaf strauss --no-cache-dir
    % pip install git+https://github.com/spacetelescope/jdaviz.git --no-cache-dir

## 7. Check Installation

To check your installation, run `jupyter lab` from your command line when
in the jdaviz environment. This should launch a Jupyter lab instance in
your default browser. Open a new notebook and in a code cell type:

    import jdaviz
    print(jdaviz.__version__)

Note that the first import is quite slow because of the dependencies that
need to be imported too. Thank you for being patient.

## 8. Download the Required Workshop Data

The script `download_data.py` will download the necessary data for this
demo from MAST. To download the data, run

    % python download_data.py
