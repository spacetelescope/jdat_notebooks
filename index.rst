=======================================================
JWST Data Analysis Tool Notebooks
=======================================================

The `jdat_notebooks <https://github.com/spacetelescope/jdat_notebooks>`_
repository contains notebooks illustrating workflows for post-pipeline
analysis of JWST data. Some of the notebooks also illustrate generic
analysis workflows that are applicable to data from other observatories
as well. This repository and the notebooks are one component of STScI's
larger `Data Analysis Tools
Ecosystem <https://jwst-docs.stsci.edu/jwst-post-pipeline-data-analysis>`_.

Installation Instructions
=========================

Please see the :ref:`installation instructions <install>` for details on how to download,
install, and run your notebooks.

Summary of Notebooks
====================

The table below summarizes the notebooks currently available. The
Table of Contents on the left of this page will take you to rendered versions
of the notebooks, which require no special tools beyond your web browser. If you
do not see an expected notebook listed in the left-hand column, it is not
currently rendered. The links in the table will take you to the GitHub repository
location of the notebooks for you to :ref:`download <install>`.

.. list-table:: JWST Science Analysis Notebooks
   :widths: 25 25
   :header-rows: 1

   * - Notebook
     - Description
   * - Cross-Instrument
     -
   * - `asdf <https://github.com/spacetelescope/jdat_notebooks/tree/main/notebooks/asdf_example>`_
     - - **Use case:** create ASDF (Advanced Scientific Data) file from FITS file.
       - **Data:** CANDELS image of the COSMOS field.
       - **Tools:** asdf, gwcs, astrocut.
       - **Cross-instrument:** All.
   * - `Background Estimation <https://github.com/spacetelescope/jdat_notebooks/tree/main/notebooks/background_estimation_imaging>`_
     - - **Use case:** estimate the sky background in complex scenes.
       - **Data:** images with pathological background pattern created in the notebook.
       - **Tools:** photutils
       - **Cross-instrument:** All.
   * - `Querying MAST <https://github.com/spacetelescope/jdat_notebooks/tree/main/notebooks/NIRSpec_MAST_Query>`_
     - - **Use case:** How to submit NIRSpec MAST Query using python.
       - **Data:**
       - **Tools:** mast, astroquery
       - **Cross-instrument:** All.
   * - `Specviz GUI <https://github.com/spacetelescope/jdat_notebooks/tree/main/notebooks/specviz_notebookGUI_interaction>`_
     - - **Use case:** How to inspect and export spectra in Specviz GUI.
       - **Data:** NIRISS simulation generated with MIRAGE.
       - **Tools:** specutils, jdaviz.
       - **Cross-instrument:** All.
   * - `Composite Model Fitting <https://github.com/spacetelescope/jdat_notebooks/tree/main/notebooks/composite_model_fitting>`_
     - - **Use case:** Fitting the complex continuum around Lyman-alpha in the spectrum of an active galaxy NGC 5548.
       - **Data:** 3-column ECSV file with units for each column.
       - **Tools:** specutils, numpy.
       - **Cross-instrument:** All.
   * - `Redshift Cross-Correlation <https://github.com/spacetelescope/jdat_notebooks/tree/main/notebooks/redshift_crosscorr>`_
     - - **Use case:** Reproduce the workflow of the IRAF task XCORFIT to measure redshfit.
       - **Data:** LEGA-C spectra and galaxy template spectra; optical rest frame.
       - **Tools:** specutils
       - **Cross-instrument:** All.
   * - `IFU Cube Fitting <https://github.com/spacetelescope/jdat_notebooks/tree/main/notebooks/cube_fitting>`_
     - - **Use case:** Continuum and emission-line modeling of galaxy IFU spectra.
       - **Data:** Spitzer/IRS on M58.
       - **Tools:** specutils, custom functions
       - **Cross-instrument:** MIRI, NIRSpec
   * - MIRI
     -
   * - `MRS Cube Pipeline, Optimal Extraction, Analysis <https://github.com/spacetelescope/jdat_notebooks/tree/main/notebooks/MRS_Mstar_analysis>`_
     - - **Use case:** For MIRI MRS, run the JWST pipeline, optimal extraction of point source, and analysis in Cubeviz.
       - **Data:** Simulated MIRI MRS spectrum of AGB star.
       - **Tools:**  jdaviz, specutils, jwst, photutils, astropy, scipy
       - **Cross-instrument:**
   * - `IFU of YSO's in LMC <https://github.com/spacetelescope/jdat_notebooks/tree/main/notebooks/MIRI_IFU_YSOs_in_the_LMC>`_
     - - **Use case:**  Automatically detect point sources and extract photometry in a 3D cube. Analyze spectral lines.
       - **Data:** ALMA 13CO data cubes.
       - **Tools:** specutils, photutils, astropy.
       - **Cross-instrument:**
   * - `LRS Optimal Extraction <https://github.com/spacetelescope/jdat_notebooks/tree/main/notebooks/MIRI_LRS_spectral_extraction>`_
     - - **Use case:**Optimal spectral extraction.
       - **Data:** MIRISim simulated LRS spectrum.
       - **Tools:** jwst pipeline, gwcs.
       - **Cross-instrument:** NIRSpec, NIRISS, MIRI
   * - NIRCam
     -
   * - `Point Source Aperture Photometry <https://github.com/spacetelescope/jdat_notebooks/tree/main/notebooks/aperture_photometry>`_
     - - **Use case:** Crowded field imaging with Aperture-fitting photometry.
       - **Data:** Simulated NIRCam images of LMC astrometric calibration field.
       - **Tools:** jwst pipeline, photutils
       - **Cross-instrument:** MIRI, NIRCam
   * - `Multiband Extended Aperture Photometry <https://github.com/spacetelescope/jdat_notebooks/tree/main/notebooks/NIRCam_photometry>`_
     - - **Use case:** measure extended galaxy galaxy photomtery in a field.
       - **Data:** Simulated NIRCam images from JADES GTO extragalactic blank field.
       - **Tools:** photutils
       - **Cross-instrument:** MIRI, NIRCam
   * - `Cross-Filter PSF-Matched Aperture Photometry <https://github.com/spacetelescope/jdat_notebooks/tree/main/notebooks/NIRCam_PSF-matched_photometry>`_
     - - **Use case:** A more advanced version of the above notebook that uses PSF corrections, but still performs aperture photometry.
       - **Data:** Simulated NIRCam images from JADES GTO extragalactic blank field.
       - **Tools:** photutils
       - **Cross-instrument:** MIRI, NIRCam
   * - `PSF Photometry <https://github.com/spacetelescope/jdat_notebooks/tree/main/notebooks/psf_photometry>`_
     - - **Use case:** Crowded field imaging with PSF-fitting photomtery.
       - **Data:** Simulated NIRCam images of LMC astrometric calibration field.
       - **Tools:** webbpsf, photutils
       - **Cross-instrument:** MIRI, NIRCam
   * - `MIRAGE Simulations <https://github.com/spacetelescope/jdat_notebooks/tree/main/notebooks/preimaging>`_
     - - **Use case:** Putting together simulations and running the NIRCam Imaging JWST Calibration Pipeline.
       - **Data:** Simulated NIRCam images of LMC astrometric calibration field.
       - **Tools:** webbpsf, jwst
       - **Cross-instrument:**
   * - NIRISS
     -
   * - `WFSS Spectra <https://github.com/spacetelescope/jdat_notebooks/tree/main/notebooks/NIRISS_WFSS_postpipeline>`_
     - - **Use case:** Optimal Extraction and analysis of grism spectra.
       - **Data:** Simulated NIRISS spectra of galaxy center.
       - **Tools:** specutils
       - **Cross-instrument:** NIRSpec, NIRISS
   * - `WFSS MOS Spectra <https://github.com/spacetelescope/jdat_notebooks/tree/main/notebooks/mos-spectroscopy>`_
     - - **Use case:** Emission-line measurements and template matching on 1D spectra.
       - **Data:** LEGA-C spectra and agalxy template spectra; optical rest frame
       - **Tools:** specutils
       - **Cross-instrument:** NIRSpec, NIRISS
   * - `AMI Binary Star <https://github.com/spacetelescope/jdat_notebooks/tree/main/notebooks/niriss_ami_binary>`_
     - - **Use case:** Find the binary parameters of AB Dor.
       - **Data:** Simulated MIRAGE data for a binary point source.
       - **Tools:** jwst pipeline, nrm_analysis
       - **Cross-instrument:**
   * - `SOSS Transiting Exoplanet <https://github.com/spacetelescope/jdat_notebooks/tree/main/notebooks/soss-transit-spectroscopy>`_
     - - **Use case:** Primary transit of an exoplanet.
       - **Data:** Simulated transit using awesomesoss.
       - **Tools:** jwst pipeline, juliet
       - **Cross-instrument:**
   * - NIRSpec
     -
   * - `IFU Cube Modeling <https://github.com/spacetelescope/jdat_notebooks/tree/main/notebooks/IFU_cube_continuum_fit>`_
     - - **Use case:** Continuum and emission line modeling of AGN; 1.47-1.87um.
       - **Data:** NIFS on Gemini; NGC 4151
       - **Tools:** specutils, cubeviz
       - **Cross-instrument:** MIRI, NIRSpec
   * - `IFU Optimal Extraction <https://github.com/spacetelescope/jdat_notebooks/tree/main/notebooks/ifu_optimal>`_
     - - **Use case:** Optimal spectral extraction.
       - **Data:** Simulated data of a faint (quasar) point source.
       - **Tools:** jwst pipeline, scipy, specutils, jdaviz, photutils, astropy.io astropy.wcs
       - **Cross-instrument:**
   * - `MOS Optimal Extraction <https://github.com/spacetelescope/jdat_notebooks/tree/main/notebooks/optimal_extraction_dynamic>`_
     - - **Use case:** Optimal spectral extraction.
       - **Data:** Simulated NIRSpec MOS data; point sources.
       - **Tools:** jwst pipeline
       - **Cross-instrument:**
   * - `BOTS Transiting Exoplanet <https://github.com/spacetelescope/jdat_notebooks/tree/main/notebooks/transit_spectroscopy_notebook>`_
     - - **Use case:** Primary transit of an exoplanet.
       - **Data:** Simulated NIRSpec data from ground-based campaign.
       - **Tools:**
       - **Cross-instrument:**

Help
====

If you uncover any issues or bugs, you can open a
`GitHub issue <https://github.com/spacetelescope/jdat_notebooks/issues>`_.
For faster responses, however, we encourage you to submit
a `JWST Help Desk Ticket <https://stsci.service-now.com/jwst>`_.

Contributing
============

Contributions are welcome from both the scientist and developer
community. If you wish to contribute fixes or clarifications to existing
notebooks, feel free to do so directly to this repository. If you wish
to contribute new notebooks or major reworks of existing notebooks, we
refer you to
`dat\_pyinthesky <https://github.com/spacetelescope/dat_pyinthesky/tree/master/jdat_notebooks>`_.

For details on how to provide such contributions, see the `contributing
instructions <https://github.com/spacetelescope/jdat_jdat_>`__. The
notebooks attempt to utilize a number of software packages supported by
STScI, including `Astropy <https://www.astropy.org>`__,
`glue <http://docs.glueviz.org/en/stable/index.html>`__,
`ginga <https://ginga.readthedocs.io/en/latest/>`__,
`photutils <https://photutils.readthedocs.io>`__,
`specutils <https://specutils.readthedocs.io/en/stable/>`__,
`astroimtools <http://astroimtools.readthedocs.io>`__,
`imexam <http://imexam.readthedocs.io>`__,
`jdaviz <https://jdaviz.readthedocs.io/en/latest/>`__,
`asdf <http://asdf.readthedocs.io/en/latest/>`__,
`gwcs <https://gwcs.readthedocs.io/en/latest/>`__, and
`synphot <http://synphot.readthedocs.io/en/latest/index.html>`__. Note
jdaviz is STScI's JWST Data Analysis Visualization Tool, designed to be
used with spectra, IFU cubes, and multi-object spectroscopy (MOS).

.. |image1| image:: data:image/svg+xml;base64,PHN2ZyBjbGFzcz0ib2N0aWNvbiBvY3RpY29uLWxpbmsiIHZpZXdib3g9IjAgMCAxNiAxNiIgdmVyc2lvbj0iMS4xIiB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIGFyaWEtaGlkZGVuPSJ0cnVlIj48cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik03Ljc3NSAzLjI3NWEuNzUuNzUgMCAwMDEuMDYgMS4wNmwxLjI1LTEuMjVhMiAyIDAgMTEyLjgzIDIuODNsLTIuNSAyLjVhMiAyIDAgMDEtMi44MyAwIC43NS43NSAwIDAwLTEuMDYgMS4wNiAzLjUgMy41IDAgMDA0Ljk1IDBsMi41LTIuNWEzLjUgMy41IDAgMDAtNC45NS00Ljk1bC0xLjI1IDEuMjV6bS00LjY5IDkuNjRhMiAyIDAgMDEwLTIuODNsMi41LTIuNWEyIDIgMCAwMTIuODMgMCAuNzUuNzUgMCAwMDEuMDYtMS4wNiAzLjUgMy41IDAgMDAtNC45NSAwbC0yLjUgMi41YTMuNSAzLjUgMCAwMDQuOTUgNC45NWwxLjI1LTEuMjVhLjc1Ljc1IDAgMDAtMS4wNi0xLjA2bC0xLjI1IDEuMjVhMiAyIDAgMDEtMi44MyAweiI+PC9wYXRoPjwvc3ZnPg==
   :class: octicon octicon-link
   :target: #james-webb-space-telescope-data-analysis-tool-notebooks
.. |image2| image:: data:image/svg+xml;base64,PHN2ZyBjbGFzcz0ib2N0aWNvbiBvY3RpY29uLWxpbmsiIHZpZXdib3g9IjAgMCAxNiAxNiIgdmVyc2lvbj0iMS4xIiB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIGFyaWEtaGlkZGVuPSJ0cnVlIj48cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik03Ljc3NSAzLjI3NWEuNzUuNzUgMCAwMDEuMDYgMS4wNmwxLjI1LTEuMjVhMiAyIDAgMTEyLjgzIDIuODNsLTIuNSAyLjVhMiAyIDAgMDEtMi44MyAwIC43NS43NSAwIDAwLTEuMDYgMS4wNiAzLjUgMy41IDAgMDA0Ljk1IDBsMi41LTIuNWEzLjUgMy41IDAgMDAtNC45NS00Ljk1bC0xLjI1IDEuMjV6bS00LjY5IDkuNjRhMiAyIDAgMDEwLTIuODNsMi41LTIuNWEyIDIgMCAwMTIuODMgMCAuNzUuNzUgMCAwMDEuMDYtMS4wNiAzLjUgMy41IDAgMDAtNC45NSAwbC0yLjUgMi41YTMuNSAzLjUgMCAwMDQuOTUgNC45NWwxLjI1LTEuMjVhLjc1Ljc1IDAgMDAtMS4wNi0xLjA2bC0xLjI1IDEuMjVhMiAyIDAgMDEtMi44MyAweiI+PC9wYXRoPjwvc3ZnPg==
   :class: octicon octicon-link
   :target: #help
.. |image3| image:: data:image/svg+xml;base64,PHN2ZyBjbGFzcz0ib2N0aWNvbiBvY3RpY29uLWxpbmsiIHZpZXdib3g9IjAgMCAxNiAxNiIgdmVyc2lvbj0iMS4xIiB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIGFyaWEtaGlkZGVuPSJ0cnVlIj48cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik03Ljc3NSAzLjI3NWEuNzUuNzUgMCAwMDEuMDYgMS4wNmwxLjI1LTEuMjVhMiAyIDAgMTEyLjgzIDIuODNsLTIuNSAyLjVhMiAyIDAgMDEtMi44MyAwIC43NS43NSAwIDAwLTEuMDYgMS4wNiAzLjUgMy41IDAgMDA0Ljk1IDBsMi41LTIuNWEzLjUgMy41IDAgMDAtNC45NS00Ljk1bC0xLjI1IDEuMjV6bS00LjY5IDkuNjRhMiAyIDAgMDEwLTIuODNsMi41LTIuNWEyIDIgMCAwMTIuODMgMCAuNzUuNzUgMCAwMDEuMDYtMS4wNiAzLjUgMy41IDAgMDAtNC45NSAwbC0yLjUgMi41YTMuNSAzLjUgMCAwMDQuOTUgNC45NWwxLjI1LTEuMjVhLjc1Ljc1IDAgMDAtMS4wNi0xLjA2bC0xLjI1IDEuMjVhMiAyIDAgMDEtMi44MyAweiI+PC9wYXRoPjwvc3ZnPg==
   :class: octicon octicon-link
   :target: #contributing
