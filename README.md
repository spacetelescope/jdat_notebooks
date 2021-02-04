# James Webb Space Telescope Data Analysis Tool Notebooks


 ``jdat_notebooks`` are one component of STScI's larger [Data Analysis Tools Ecosystem](https://jwst-docs.stsci.edu/jwst-post-pipeline-data-analysis).

 ``jdat_notebooks`` are intended for the broader science community.  If you wish to contribute notebooks or technical expertise, we refer you to [dat_pyinthesky](https://github.com/spacetelescope/dat_pyinthesky/tree/master/jdat_notebooks).  If you wish to contribute notebooks, please follow [contributing instructions](https://github.com/spacetelescope/jdat_notebooks/blob/master/contributing.md).


 This repository contains Jupyter notebooks intended for the developer community wishing to contribute notebooks or technical expertise.  The notebooks illustrate workflows for post-pipeline analysis of JWST data. The notebooks are likely to be useful for analyzing data from other observatories as well.

 The notebooks attempt to utilize a number of software packages supported by STScI, including [Astropy](https://www.astropy.org), [glue](http://docs.glueviz.org/en/stable/index.html), [ginga](https://ginga.readthedocs.io/en/latest/), [photutils](https://photutils.readthedocs.io), [specutils](https://specutils.readthedocs.io/en/stable/), [astroimtools](http://astroimtools.readthedocs.io), [imexam](http://imexam.readthedocs.io), [jdaviz](https://jdaviz.readthedocs.io/en/latest/), [asdf](http://asdf.readthedocs.io/en/latest/), [gwcs](https://gwcs.readthedocs.io/en/latest/), and [synphot](http://synphot.readthedocs.io/en/latest/index.html).  Note jdaviz is STScI's JWST Data Analysis Visualization Tool, designed to be used with spectra, IFU cubes, and multi-object spectroscopy (MOS).

You can view rendered versions of the notebooks at https://spacetelescope.github.io/jdat_notebooks/.

To download and execute the notebooks, clone this repository to your local computer. Most of the notebooks
rely on packages that are available in [astroconda](https://astroconda.readthedocs.io/en/latest/), although
a few rely on packages that should be installed using [pip](https://pip.pypa.io/en/stable/). The version
dependencies are listed in the `environment.yaml` and in the `requirements` file in each notebook folder.


## If you locally cloned this repo before 5 Feb 2021

The primary branch for this repo has been transitioned from ``master`` to ``main``.  If you have a local clone of this repository and want to keep your local branch in sync with this repo, you'll need to do the following:
```
% git branch -m master main
% git fetch origin
% git branch -u origin/main main
```
If you are using a GUI to manage your repos you'll have to find the equivalent commands as it's different for different programs. Alternatively, you can just delete your local clone and re-clone!