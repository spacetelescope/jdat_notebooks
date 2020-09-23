# James Webb Space Telescope Data Analysis Tool Notebooks

.. note::

   ``jdat_notebooks`` are one component of STScI's larger `Data Analysis Tools Ecosystem <https://jwst-docs.stsci.edu/jwst-post-pipeline-data-analysis>`_.

   .. note::

   ``jdat_notebooks`` are intended for the broader science community.  If you wish to contribute notebooks or technical expertise, we refer you to `dat_pyinthesky <https://github.com/spacetelescope/dat_pyinthesky/tree/master/jdat_notebooks>`_.

This repository contains Jupyter notebooks intended for the broader science community to illustrate workflows for post-pipeline analysis of JWST data. The notebooks are likely to be useful for analyzing data from other observatories as well.

The notebooks attempt to utilize a number of software packages supported by STScI, including `Astropy <https://www.astropy.org>`_, `glue <http://docs.glueviz.org/en/stable/index.html>`_, `ginga <https://ginga.readthedocs.io/en/latest/>`_, `photutils <https://photutils.readthedocs.io>`_, `specutils <https://specutils.readthedocs.io/en/stable/>`_, `astroimtools <http://astroimtools.readthedocs.io>`_, `imexam <http://imexam.readthedocs.io>`_, `jdaviz <https://jdaviz.readthedocs.io/en/latest/>`_, `asdf <http://asdf.readthedocs.io/en/latest/>`_, `gwcs <https://gwcs.readthedocs.io/en/latest/>`_, and `synphot <http://synphot.readthedocs.io/en/latest/index.html>`_.  Note jdaviz is STScI's JWST Data Analysis Visualization Tool, designed to be used with spectra, IFU cubes, and multi-object spectroscopy (MOS).

You can view rendered versions of the notebooks at https://spacetelescope.github.io/jdat_notebooks/. 

To download and execute the notebooks, clone this repository to your local computer. Most of the notebooks
rely on packages that are available in [astroconda](https://astroconda.readthedocs.io/en/latest/), although
a few rely on packages that should be installed using [pip](https://pip.pypa.io/en/stable/). The version
dependencies are listed in the `environment.yaml` and in the `requirements` file in each notebook folder.

