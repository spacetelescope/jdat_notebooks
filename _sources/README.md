[![ci_validation](https://img.shields.io/github/workflow/status/spacetelescope/jdat_notebooks/ci_validation?label=Notebook%20Validation)](https://github.com/spacetelescope/jdat_notebooks/actions?query=workflow%3Aci_validation)
[![ci_deployment](https://img.shields.io/github/workflow/status/spacetelescope/jdat_notebooks/Build%20and%20deploy%20notebooks?label=HTML%20Deployment&style=flat)](https://github.com/spacetelescope/jdat_notebooks/actions?query=workflow%3ABuild%20and%20deploy%20notebooks)


# James Webb Space Telescope Data Analysis Tool Notebooks


The ``jdat_notebooks`` repository contains notebooks illustrating workflows for post-pipeline analysis of JWST data. Some of the notebooks also illustrate generic analysis workflows that are applicable to data from other observatories as well. This repository and the notebooks are one component of STScI's larger [Data Analysis Tools Ecosystem](https://jwst-docs.stsci.edu/jwst-post-pipeline-data-analysis).

The following [table](https://spacetelescope.github.io/jdat_notebooks/) summarizes the notebooks currently available.

## Installation

You can view [rendered versions of the notebooks](https://spacetelescope.github.io/jdat_notebooks/), which require no special tools beyond your web browser.

To download and execute the notebooks, we recommend you [clone](https://github.com/git-guides/git-clone) this repository to your local computer. You can also click the "Download ZIP" option for the entire repository listed under the green "Code" button at the top of this page.

You can also download individual notebooks, but it is not as straight forward.  This is because Git doesn't directly support downloading parts of the repository. However, in some web browsers, you should be able to navigate to your desired notebook, right click on the "RAW" formatting button, and download.  There are also options to use wget or curl for advanced users. 

Note, however, most notebooks have additional associated files in their folder, including a `requirements` document that lists packages necessary to run the notebooks.  These packages can be installed using [pip](https://pip.pypa.io/en/stable/). The version dependencies are listed in the `environment.yaml` and in the `requirements` file in each notebook folder. 
You will need **python version 3.8.10**.  We recommend the following command sequence:

```   
% git clone https://github.com/spacetelescope/jdat_notebooks.git
% cd jdat_notebooks/notebooks/<whatever-notebook>
% conda create -n jdat-nb python=3.8.10
% conda activate jdat-nb
% pip install -r pre-requirements.txt (if necessary)
% pip install -r requirements.txt
% pip install jupyter
% jupyter notebook
```


### If you locally cloned this repo before 5 Feb 2021

The primary branch for this repo has been transitioned from ``master`` to ``main``.  If you have a local clone of this repository and want to keep your local branch in sync with this repo, you'll need to do the following in your local clone from your terminal:

```   
% git branch -m master main
% git fetch origin
% git branch -u origin/main main
```

If you are using a GUI to manage your repos you'll have to find the equivalent commands as it's different for different programs. Alternatively, you can just delete your local clone and re-clone!


## Help

If you uncover any issues or bugs, you can [open an issue on GitHub](https://github.com/spacetelescope/jdat_notebooks/issues/new).  For faster responses, however, we encourage you to submit a JWST Help Desk Ticket: jwsthelp.stsci.edu

## Contributing

Contributions are welcome from both the scientist and developer community.  If you wish to contribute fixes or clarifications to existing notebooks, feel free to do so directly to this repository.  If you wish to contribute new notebooks or major reworks of existing notebooks, we refer you to [dat_pyinthesky](https://github.com/spacetelescope/dat_pyinthesky/tree/master/jdat_notebooks).  For details on how to provide such contributions, see the [contributing instructions](https://github.com/spacetelescope/jdat_notebooks/blob/main/CONTRIBUTING.md).

The notebooks attempt to utilize a number of software packages supported by STScI, including [Astropy](https://www.astropy.org), [glue](http://docs.glueviz.org/en/stable/index.html), [ginga](https://ginga.readthedocs.io/en/latest/), [photutils](https://photutils.readthedocs.io), [specutils](https://specutils.readthedocs.io/en/stable/), [astroimtools](http://astroimtools.readthedocs.io), [imexam](http://imexam.readthedocs.io), [jdaviz](https://jdaviz.readthedocs.io/en/latest/), [asdf](http://asdf.readthedocs.io/en/latest/), [gwcs](https://gwcs.readthedocs.io/en/latest/), and [synphot](http://synphot.readthedocs.io/en/latest/index.html).  Note jdaviz is STScI's JWST Data Analysis Visualization Tool, designed to be used with spectra, IFU cubes, and multi-object spectroscopy (MOS).

