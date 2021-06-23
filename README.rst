James Webb Space Telescope Data Analysis Tool Notebooks
--------------

The ``jdat_notebooks`` repository contains notebooks illustrating workflows for post-pipeline analysis of JWST data. Some of the notebooks also illustrate generic analysis workflows that are applicable to data from other observatories as well. This repository and the notebooks are one component of STScI's larger `Data Analysis Tools Ecosystem <https://jwst-docs.stsci.edu/jwst-post-pipeline-data-analysis>`_.

The following table summarizes the notebooks currently available.

+-----------+-------------------------------------------------------------------------------------+
| JWST Science Analysis Notebooks                                                                 |
+-----------+-------------------------------------------------------------------------------------+
| Notebook  | Description                                                                         |
+-----------+-------------------------------------------------------------------------------------+
| Cross-Instrument                                                                                |
+===========+=====================================================================================+
| asdf      | * Use case: create ASDF (Advanced Scientific Data Format) file from FITS file.      |
|           | * Data: CANDELS image of the COSMOS field.                                          |
|           | * Tools: asdf, gwcs, astrocut.                                                      |
|           | * Cross-instrument: all instruments.                                                |
+-----------+-------------------------------------------------------------------------------------+
| Background| * Use case: estimate the sky background in complex scenes.                          |
| Estimation| * Data: images with pathological background pattern created in the notebook.        |
|           | * Tools: photutils                                                                  |
|           | * Cross-instrument: all instruments.                                                |
+-----------+-------------------------------------------------------------------------------------+
| Redshift  | * Use case: reproduce the workflow of the IRAF task XCORFIT to measure redshift.    |
| Cross-Corr| * Data: LEGA-C spectra and galaxy template spectra; optical rest-frame.             |
|           | * Tools: specutils.                                                                 |
|           | * Cross-instrument: all instruments.                                                |
+-----------+-------------------------------------------------------------------------------------+
| Querying  | * Use case: How to submit a NIRSpec MAST Query using python.                        |
| MAST      | * Data:                                                                             |
|           | * Tools: mast, astroquery.                                                          |
|           | * Cross-instrument: all instruments.                                                |
+-----------+-------------------------------------------------------------------------------------+
| Specviz   | * Use case: How to inspect and export spectra in Specviz GUI.                       |
| GUI       | * Data: NIRISS simulation  generated with the code MIRAGE.                          |
|           | * Tools: specutils, jdaviz.                                                         |
|           | * Cross-instrument: all instruments.                                                |
+-----------+-------------------------------------------------------------------------------------+
| IFU       | * Use case: continuum and emission-line modeling of galaxy IFU spectra.             |
| Cube      | * Data: Spitzer IRS on Messier 58.                                                  |
| Fitting   | * Tools: specutils, custom functions.                                               |
|           | * Cross-instrument: MIRI, NIRSpec.                                                  |
+-----------+-------------------------------------------------------------------------------------+
| NIRCam                                                                                          |
+-----------+-------------------------------------------------------------------------------------+
| Multiband | * Use case: measure extended galaxy photometry in a field.                          |
| Extended  | * Data: Simulated NIRCam images from JADES GTO extragalactic blank field.           |
| Aperture  | * Tools: photutils.                                                                 |
| Photometry| * Cross-instrument:                                                                 |
+-----------+-------------------------------------------------------------------------------------+
| Crowded   | * Use case: Crowded field imaging with Aperture-fitting photometry.                 |
| Field     | * Data: Simulated NIRCam images of LMC astrometric calibration field.               |
| Aperture  | * Tools: jwst pipeline, photutils.                                                  |
| Photometry| * Cross-instrument:                                                                 |
+-----------+-------------------------------------------------------------------------------------+
| PSF       | * Use case: Crowded field imaging with PSF-fitting photometry.                      |
| Photometry| * Data: Simulated NIRCam images of LMC astrometric calibration field.               |
|           | * Tools: webbpsf, photutils.                                                        |
|           | * Cross-instrument:                                                                 |
+-----------+-------------------------------------------------------------------------------------+
| PSF       | * Use case: Crowded field imaging with PSF-fitting photometry.                      |
| Matching  | * Data: Simulated NIRCam images of LMC astrometric calibration field.               |
| Photometry| * Tools: webbpsf, photutils.                                                        |
|           | * Cross-instrument:                                                                 |
+-----------+-------------------------------------------------------------------------------------+
| NIRISS                                                                                          |
+-----------+-------------------------------------------------------------------------------------+
| WFSS      | * Use case: Optimal extraction and analysis of grism spectra.                       |
| Spectra   | * Data: Simulated NIRISS spectra of a galaxy cluster                                |
|           | * Tools: specutils         .                                                        |
|           | * Cross-instrument: NIRSpec.                                                        |
+-----------+-------------------------------------------------------------------------------------+
| MOS       | * Use case: Emission-line measurements and template matching on 1D spectra.         |
| Spectra   | * Data: LEGA-C spectra and galaxy template spectra; optical rest-frame.             |
|           | * Tools: specutils.                                                                 |
|           | * Cross-instrument: NIRSpec.                                                        |
+-----------+-------------------------------------------------------------------------------------+
| SOSS      | * Use case: Primary transit of an exoplanet.                                        |
| Transiting| * Data: Simulated transit using awesomesoss.                                        |
| Exoplanet | * Tools: jwst pipeline, juliet.                                                     |
|           | * Cross-instrument:                                                                 |
+-----------+-------------------------------------------------------------------------------------+
| AMI       | * Use case: Find the binary parameters of AB Dor.                                   |
| Binary    | * Data: Simulated MIRAGE data for a binary point source.                            |
| Star      | * Tools: jwst pipeline, nrm_analysis.                                               |
|           | * Cross-instrument:                                                                 |
+-----------+-------------------------------------------------------------------------------------+
| NIRSpec                                                                                         |
+-----------+-------------------------------------------------------------------------------------+
| IFU       | * Use case: Continuum and emission-line modeling of AGN; 1.47-1.87um.               |
| Analysis  | * Data: NIFS on Gemini; NGC 4151.                                                   |
|           | * Tools: specutils, cubeviz.                                                        |
|           | * Cross-instrument:                                                                 |
+-----------+-------------------------------------------------------------------------------------+
| MOS       | * Use case: Optimal spectral extraction.                                            |
| Optimal   | * Data: Simulated NIRSpec MOS data; point sources.                                  |
| Extraction| * Tools: jwst pipeline                                                              |
|           | * Cross-instrument:                                                                 |
+-----------+-------------------------------------------------------------------------------------+
| MOS       | * Use case: Simulation of NIRCam pre-imaging for NIRSpec.                           |
| Pre-      | * Data: Simulated NIRCam images of LMC astrometric calibration field.               |
| Imaging   | * Tools: jwst pipeline.                                                             |
|           | * Cross-instrument: NIRCam.                                                         |
+-----------+-------------------------------------------------------------------------------------+
| BOTS      | * Use case: Primary transit of an exoplanet.                                        |
| Transiting| * Data: Simulated NIRSpec data from ground-based campaign.                          |
| Exoplanet | * Tools:                                                                            |
|           | * Cross-instrument:                                                                 |
+-----------+-------------------------------------------------------------------------------------+
| IFU       | * Use case: Optimal spectral extraction.                                            |
| Optimal   | * Data: Simulated data of faint (quasar) point source.                              |
| Extraction| * Tools:  jwst, scipy, specutils, jdaviz, photutils, astropy.io, astropy.wcs        |
|           | * Cross-instrument:                                                                 |
+-----------+-------------------------------------------------------------------------------------+
| MIRI                                                                                            |
+-----------+-------------------------------------------------------------------------------------+
| LRS       | * Use case: Optimal spectral extraction.                                            |
| Optimal   | * Data: MIRISim simulated spectra.                                                  |
| Extraction| * Tools: jwst pipeline, gwcs.                                                       |
|           | * Cross-instrument:                                                                 |
+-----------+-------------------------------------------------------------------------------------+
| IFU       | * Use case: Extract spatial-spectral features from IFU cube.                        |
| Cube      | * Data: KMOS datacube of point sources in the LMC.                                  |
| Analysis  | * Tools: specutils, spectral_cube, photutils.                                       |
| 1         | * Cross-instrument:                                                                 |
+-----------+-------------------------------------------------------------------------------------+
| IFU       | * Use case: Photutils to automatically detect point sources and extract photometry  |
| Cube      | * Data: ALMA 13CO data cubes.                                                       |
| Analysis  | * Tools: specutils, spectral_cube, photutils.                                       |
| 2         | * Cross-instrument:                                                                 |
+-----------+-------------------------------------------------------------------------------------+

Installation
--------------

You can view rendered versions of the notebooks at https://spacetelescope.github.io/jdat_notebooks/, which require no special tools beyond your web browser.

To download and execute the notebooks, `clone <https://github.com/git-guides/git-clone>`_ this repository to your local computer. Most of the notebooks
rely on packages that are available in `astroconda <https://astroconda.readthedocs.io/en/latest/>`_, although
a few rely on packages that should be installed using `pip <https://pip.pypa.io/en/stable/>`_. The version
dependencies are listed in the `environment.yaml` and in the `requirements` file in each notebook folder.

If you locally cloned this repo before 5 Feb 2021
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The primary branch for this repo has been transitioned from ``master`` to ``main``.  If you have a local clone of this repository and want to keep your local branch in sync with this repo, you'll need to do the following in your local clone from your terminal:

.. code-block::

   git branch -m master main
   git fetch origin
   git branch -u origin/main main

If you are using a GUI to manage your repos you'll have to find the equivalent commands as it's different for different programs. Alternatively, you can just delete your local clone and re-clone!


Help
----------

If you uncover any issues or bugs, you can open a GitHub ticket.  For faster responses, however, we encourage you to submit a JWST Help Desk Ticket: jwsthelp.stsci.edu

Contributing
----------

Contributions are welcome from both the scientist and developer community.  If you wish to contribute fixes or clarifications to existing notebooks, feel free to do so directly to this repository.  If you wish to contribute new notebooks or major reworks of existing notebooks, we refer you to `dat_pyinthesky <https://github.com/spacetelescope/dat_pyinthesky/tree/master/jdat_notebooks>`_.  For details on how to provide such contributions, see the `contributing instructions <https://github.com/spacetelescope/jdat_notebooks/blob/main/CONTRIBUTING.md>`_.

The notebooks attempt to utilize a number of software packages supported by STScI, including `Astropy <https://www.astropy.org>`_, `glue <http://docs.glueviz.org/en/stable/index.html>`_, `ginga <https://ginga.readthedocs.io/en/latest/>`_, `photutils <https://photutils.readthedocs.io>`_, `specutils <https://specutils.readthedocs.io/en/stable/>`_, `astroimtools <http://astroimtools.readthedocs.io>`_, `imexam <http://imexam.readthedocs.io>`_, `jdaviz <https://jdaviz.readthedocs.io/en/latest/>`_, `asdf <http://asdf.readthedocs.io/en/latest/>`_, `gwcs <https://gwcs.readthedocs.io/en/latest/>`_, and `synphot <http://synphot.readthedocs.io/en/latest/index.html>`_.  Note jdaviz is STScI's JWST Data Analysis Visualization Tool, designed to be used with spectra, IFU cubes, and multi-object spectroscopy (MOS).

