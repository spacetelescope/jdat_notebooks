 # James Webb Space Telescope Data Analysis Tool Notebooks    
.. contents::
   :depth: 3
..

|JWST Data Analysis Notebooks| Filter Notebooks ## |image1|\ James Webb
Space Telescope Data Analysis Tool Notebooks The \`jdat_notebooks\`
repository contains notebooks illustrating workflows for post-pipeline
analysis of JWST data. Some of the notebooks also illustrate generic
analysis workflows that are applicable to data from other observatories
as well. This repository and the notebooks are one component of STScI's
larger `Data Analysis Tools
Ecosystem <https://jwst-docs.stsci.edu/jwst-post-pipeline-data-analysis>`__.
The following table summarizes the notebooks currently available. Most
links will take you to rendered versions of the notebooks, which require
no special tools beyond your web browser. To download and execute the
notebooks, [clone](https://github.com/git-guides/git-clone) this
[repository](https://github.com/spacetelescope/jdat_notebooks) to your
local computer. Most of the notebooks rely on packages that can be
installed using `pip <https://pip.pypa.io/en/stable/>`__. The version
dependencies are listed in the environment.yaml and in the requirements
file in each notebook folder.

+-----------------------------------+-----------------------------------+
| JWST Science Analysis Notebooks   |                                   |
+===================================+===================================+
| Notebook                          | Description                       |
+-----------------------------------+-----------------------------------+
| Cross-Instrument                  |                                   |
+-----------------------------------+-----------------------------------+
| `asdf <jdat_notebooks/a           | -  Use case: create ASDF          |
| sdf_example/asdf_example.html>`__ |    (Advanced Scientific Data      |
|                                   |    Format) file from FITS file.   |
|                                   | -  Data: CANDELS image of the     |
|                                   |    COSMOS field.                  |
|                                   | -  Tools: asdf, gwcs, astrocut.   |
|                                   | -  Cross-instrument: all          |
|                                   |    instruments.                   |
+-----------------------------------+-----------------------------------+
| `Background                       | -  Use case: estimate the sky     |
| Estima                            |    background in complex scenes.  |
| tion <jdat_notebooks/background_e | -  Data: images with pathological |
| stimation_imaging/Imaging%20Sky%2 |    background pattern created in  |
| 0Background%20Estimation.html>`__ |    the notebook.                  |
|                                   | -  Tools: photutils               |
|                                   | -  Cross-instrument: all          |
|                                   |    instruments.                   |
+-----------------------------------+-----------------------------------+
| Redshift Cross-Corr               | -  Use case: reproduce the        |
|                                   |    workflow of the IRAF task      |
|                                   |    XCORFIT to measure redshift.   |
|                                   | -  Data: LEGA-C spectra and       |
|                                   |    galaxy template spectra;       |
|                                   |    optical rest-frame.            |
|                                   | -  Tools: specutils.              |
|                                   | -  Cross-instrument: all          |
|                                   |    instruments.                   |
+-----------------------------------+-----------------------------------+
| `Querying                         | -  Use case: How to submit a      |
| M                                 |    NIRSpec MAST Query using       |
| AST <jdat_notebooks/NIRSpec_MAST_ |    python.                        |
| Query/NIRSpec_MAST_Query.html>`__ | -  Data:                          |
|                                   | -  Tools: mast, astroquery.       |
|                                   | -  Cross-instrument: all          |
|                                   |    instruments.                   |
+-----------------------------------+-----------------------------------+
| `Specviz                          | -  Use case: How to inspect and   |
| GUI                               |    export spectra in Specviz GUI. |
|  <jdat_notebooks/specviz_notebook | -  Data: NIRISS simulation        |
| GUI_interaction/specviz_notebook_ |    generated with the code        |
| gui_interaction_redshift.html>`__ |    MIRAGE.                        |
|                                   | -  Tools: specutils, jdaviz.      |
|                                   | -  Cross-instrument: all          |
|                                   |    instruments.                   |
+-----------------------------------+-----------------------------------+
| `IFU Cube                         | -  Use case: continuum and        |
| Fitting <jdat_n                   |    emission-line modeling of      |
| otebooks/IFU_cube_continuum_fit/N |    galaxy IFU spectra.            |
| GC4151_FeII_ContinuumFit.html>`__ | -  Data: Spitzer IRS on Messier   |
|                                   |    58.                            |
|                                   | -  Tools: specutils, custom       |
|                                   |    functions.                     |
|                                   | -  Cross-instrument: MIRI,        |
|                                   |    NIRSpec.                       |
+-----------------------------------+-----------------------------------+
| NIRCam                            |                                   |
+-----------------------------------+-----------------------------------+
| `Multiband Extended Aperture      | -  Use case: measure extended     |
| Photometry <jdat_no               |    galaxy photometry in a field.  |
| tebooks/NIRCam_photometry/NIRCam% | -  Data: Simulated NIRCam images  |
| 20multiband%20photometry.html>`__ |    from JADES GTO extragalactic   |
|                                   |    blank field.                   |
|                                   | -  Tools: photutils.              |
|                                   | -  Cross-instrument:              |
+-----------------------------------+-----------------------------------+
| `Crowded Field Aperture           | -  Use case: Crowded field        |
| Photometry <jdat_noteboo          |    imaging with Aperture-fitting  |
| ks/aperture_photometry/NIRCam_Ape |    photometry.                    |
| rture_Photometry_Example.html>`__ | -  Data: Simulated NIRCam images  |
|                                   |    of LMC astrometric calibration |
|                                   |    field.                         |
|                                   | -  Tools: jwst pipeline,          |
|                                   |    photutils.                     |
|                                   | -  Cross-instrument:              |
+-----------------------------------+-----------------------------------+
| `PSF                              | -  Use case: Crowded field        |
| Photometry <jd                    |    imaging with PSF-fitting       |
| at_notebooks/psf_photometry/NIRCa |    photometry.                    |
| m_PSF_Photometry_Example.html>`__ | -  Data: Simulated NIRCam images  |
|                                   |    of LMC astrometric calibration |
|                                   |    field.                         |
|                                   | -  Tools: webbpsf, photutils.     |
|                                   | -  Cross-instrument:              |
+-----------------------------------+-----------------------------------+
| `PSF Matching                     | -  Use case: Crowded field        |
| Photom                            |    imaging with PSF-fitting       |
| etry <jdat_notebooks/NIRCam_PSF-m |    photometry.                    |
| atched_photometry/NIRCam_PSF_matc | -  Data: Simulated NIRCam images  |
| hed_multiband_photometry.html>`__ |    of LMC astrometric calibration |
|                                   |    field.                         |
|                                   | -  Tools: webbpsf, photutils.     |
|                                   | -  Cross-instrument:              |
+-----------------------------------+-----------------------------------+
| NIRISS                            |                                   |
+-----------------------------------+-----------------------------------+
| WFSS Spectra `Notebook            | -  Use case: Optimal extraction   |
| 0 <jdat_note                      |    and analysis of grism spectra. |
| books/NIRISS_WFSS_postpipeline/00 | -  Data: Simulated NIRISS spectra |
| .%20Optimal%20extraction.html>`__ |    of a galaxy cluster            |
| `Notebook                         | -  Tools: specutils .             |
| 1 <jdat_notebooks/NIRISS_WFSS_po  | -  Cross-instrument: NIRSpec.     |
| stpipeline/01.%20Combine%20and%20 |                                   |
| normalize%201D%20spectra.html>`__ |                                   |
| `Notebook                         |                                   |
| 2 <jdat_notebooks/NIRI            |                                   |
| SS_WFSS_postpipeline/02.%20Cross% |                                   |
| 20correlation%20template.html>`__ |                                   |
| `Notebook                         |                                   |
| 3 <                               |                                   |
| jdat_notebooks/NIRISS_WFSS_postpi |                                   |
| peline/03.%20Spatially%20resolved |                                   |
| %20emission%20line%20map.html>`__ |                                   |
+-----------------------------------+-----------------------------------+
| `MOS                              | -  Use case: Emission-line        |
| spc                               |    measurements and template      |
| tra <jdat_notebooks/mos-spectrosc |    matching on 1D spectra.        |
| opy/MOSspec_sv06_revised.html>`__ | -  Data: LEGA-C spectra and       |
|                                   |    galaxy template spectra;       |
|                                   |    optical rest-frame.            |
|                                   | -  Tools: specutils.              |
|                                   | -  Cross-instrument: NIRSpec.     |
+-----------------------------------+-----------------------------------+
| `SOSS Transiting                  | -  Use case: Primary transit of   |
| Exoplanet <https://github.        |    an exoplanet.                  |
| com/spacetelescope/jdat_jdat_>`__ | -  Data: Simulated transit using  |
|                                   |    awesomesoss.                   |
|                                   | -  Tools: jwst pipeline, juliet.  |
|                                   | -  Cross-instrument:              |
+-----------------------------------+-----------------------------------+
| AMI Binary Star                   | -  Use case: Find the binary      |
|                                   |    parameters of AB Dor.          |
|                                   | -  Data: Simulated MIRAGE data    |
|                                   |    for a binary point source.     |
|                                   | -  Tools: jwst pipeline,          |
|                                   |    nrm_analysis.                  |
|                                   | -  Cross-instrument:              |
+-----------------------------------+-----------------------------------+
| NIRSpec                           |                                   |
+-----------------------------------+-----------------------------------+
| `IFU                              | -  Use case: Continuum and        |
| Analysis <jdat_n                  |    emission-line modeling of AGN; |
| otebooks/IFU_cube_continuum_fit/N |    1.47-1.87um.                   |
| GC4151_FeII_ContinuumFit.html>`__ | -  Data: NIFS on Gemini; NGC      |
|                                   |    4151.                          |
|                                   | -  Tools: specutils, cubeviz.     |
|                                   | -  Cross-instrument:              |
+-----------------------------------+-----------------------------------+
| `MOS Optimal                      | -  Use case: Optimal spectral     |
| Extraction <jdat_                 |    extraction.                    |
| notebooks/optimal_extraction/Spec | -  Data: Simulated NIRSpec MOS    |
| tral%20Extraction-static.html>`__ |    data; point sources.           |
|                                   | -  Tools: jwst pipeline           |
|                                   | -  Cross-instrument:              |
+-----------------------------------+-----------------------------------+
| `MOS                              | -  Use case: Simulation of NIRCam |
| Pre-Imaging <https://github.      |    pre-imaging for NIRSpec.       |
| com/spacetelescope/jdat_jdat_>`__ | -  Data: Simulated NIRCam images  |
|                                   |    of LMC astrometric calibration |
|                                   |    field.                         |
|                                   | -  Tools: jwst pipeline.          |
|                                   | -  Cross-instrument: NIRCam.      |
+-----------------------------------+-----------------------------------+
| `BOTS Transiting                  | -  Use case: Primary transit of   |
| E                                 |    an exoplanet.                  |
| xoplanet <jdat_notebooks/transit_ | -  Data: Simulated NIRSpec data   |
| spectroscopy_notebook/Exoplanet_T |    from ground-based campaign.    |
| ransmission_Spectra_JWST.html>`__ | -  Tools:                         |
|                                   | -  Cross-instrument:              |
+-----------------------------------+-----------------------------------+
| `IFU Optimal                      | -  Use case: Optimal spectral     |
| Extraction <jdat_notebooks        |    extraction.                    |
| /ifu_optimal/ifu_optimal.html>`__ | -  Data: Simulated data of faint  |
|                                   |    (quasar) point source.         |
|                                   | -  Tools: jwst, scipy, specutils, |
|                                   |    jdaviz, photutils, astropy.io, |
|                                   |    astropy.wcs                    |
|                                   | -  Cross-instrument:              |
+-----------------------------------+-----------------------------------+
| MIRI                              |                                   |
+-----------------------------------+-----------------------------------+
| `LRS Optimal                      | -  Use case: Optimal spectral     |
| Extraction <j                     |    extraction.                    |
| dat_notebooks/tree/main/notebooks | -  Data: MIRISim simulated        |
| /MIRI_LRS_spectral_extraction>`__ |    spectra.                       |
|                                   | -  Tools: jwst pipeline, gwcs.    |
|                                   | -  Cross-instrument:              |
+-----------------------------------+-----------------------------------+
| `IFU Cube                         | -  Use case: Extract              |
| 1 <jdat_not                       |    spatial-spectral features from |
| ebooks/MRS_Mstar_analysis/JWST_Ms |    IFU cube.                      |
| tar_dataAnalysis_usecase.html>`__ | -  Data: KMOS datacube of point   |
|                                   |    sources in the LMC.            |
|                                   | -  Tools: specutils,              |
|                                   |    spectral_cube, photutils.      |
|                                   | -  Cross-instrument:              |
+-----------------------------------+-----------------------------------+
| `IFU Cube                         | -  Use case: Photutils to         |
| 2 <jdat_note                      |    automatically detect point     |
| books/MIRI_IFU_YSOs_in_the_LMC/is |    sources and extract photometry |
| ha_nayak_ysos_in_the_lmc.html>`__ | -  Data: ALMA 13CO data cubes.    |
|                                   | -  Tools: specutils,              |
|                                   |    spectral_cube, photutils.      |
|                                   | -  Cross-instrument:              |
+-----------------------------------+-----------------------------------+

## |image2|\ Help If you uncover any issues or bugs, you can open a
GitHub ticket. For faster responses, however, we encourage you to submit
a JWST Help Desk Ticket: jwsthelp.stsci.edu ## |image3|\ Contributing
Contributions are welcome from both the scientist and developer
community. If you wish to contribute fixes or clarifications to existing
notebooks, feel free to do so directly to this repository. If you wish
to contribute new notebooks or major reworks of existing notebooks, we
refer you to
[dat\_pyinthesky](https://github.com/spacetelescope/dat_pyinthesky/tree/master/jdat_notebooks).
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

.. |JWST Data Analysis Notebooks| image:: images/Jspectra.svg
   :class: logo
.. |image1| image:: data:image/svg+xml;base64,PHN2ZyBjbGFzcz0ib2N0aWNvbiBvY3RpY29uLWxpbmsiIHZpZXdib3g9IjAgMCAxNiAxNiIgdmVyc2lvbj0iMS4xIiB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIGFyaWEtaGlkZGVuPSJ0cnVlIj48cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik03Ljc3NSAzLjI3NWEuNzUuNzUgMCAwMDEuMDYgMS4wNmwxLjI1LTEuMjVhMiAyIDAgMTEyLjgzIDIuODNsLTIuNSAyLjVhMiAyIDAgMDEtMi44MyAwIC43NS43NSAwIDAwLTEuMDYgMS4wNiAzLjUgMy41IDAgMDA0Ljk1IDBsMi41LTIuNWEzLjUgMy41IDAgMDAtNC45NS00Ljk1bC0xLjI1IDEuMjV6bS00LjY5IDkuNjRhMiAyIDAgMDEwLTIuODNsMi41LTIuNWEyIDIgMCAwMTIuODMgMCAuNzUuNzUgMCAwMDEuMDYtMS4wNiAzLjUgMy41IDAgMDAtNC45NSAwbC0yLjUgMi41YTMuNSAzLjUgMCAwMDQuOTUgNC45NWwxLjI1LTEuMjVhLjc1Ljc1IDAgMDAtMS4wNi0xLjA2bC0xLjI1IDEuMjVhMiAyIDAgMDEtMi44MyAweiI+PC9wYXRoPjwvc3ZnPg==
   :class: octicon octicon-link
   :target: #james-webb-space-telescope-data-analysis-tool-notebooks
.. |image2| image:: data:image/svg+xml;base64,PHN2ZyBjbGFzcz0ib2N0aWNvbiBvY3RpY29uLWxpbmsiIHZpZXdib3g9IjAgMCAxNiAxNiIgdmVyc2lvbj0iMS4xIiB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIGFyaWEtaGlkZGVuPSJ0cnVlIj48cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik03Ljc3NSAzLjI3NWEuNzUuNzUgMCAwMDEuMDYgMS4wNmwxLjI1LTEuMjVhMiAyIDAgMTEyLjgzIDIuODNsLTIuNSAyLjVhMiAyIDAgMDEtMi44MyAwIC43NS43NSAwIDAwLTEuMDYgMS4wNiAzLjUgMy41IDAgMDA0Ljk1IDBsMi41LTIuNWEzLjUgMy41IDAgMDAtNC45NS00Ljk1bC0xLjI1IDEuMjV6bS00LjY5IDkuNjRhMiAyIDAgMDEwLTIuODNsMi41LTIuNWEyIDIgMCAwMTIuODMgMCAuNzUuNzUgMCAwMDEuMDYtMS4wNiAzLjUgMy41IDAgMDAtNC45NSAwbC0yLjUgMi41YTMuNSAzLjUgMCAwMDQuOTUgNC45NWwxLjI1LTEuMjVhLjc1Ljc1IDAgMDAtMS4wNi0xLjA2bC0xLjI1IDEuMjVhMiAyIDAgMDEtMi44MyAweiI+PC9wYXRoPjwvc3ZnPg==
   :class: octicon octicon-link
   :target: #help
.. |image3| image:: data:image/svg+xml;base64,PHN2ZyBjbGFzcz0ib2N0aWNvbiBvY3RpY29uLWxpbmsiIHZpZXdib3g9IjAgMCAxNiAxNiIgdmVyc2lvbj0iMS4xIiB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIGFyaWEtaGlkZGVuPSJ0cnVlIj48cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik03Ljc3NSAzLjI3NWEuNzUuNzUgMCAwMDEuMDYgMS4wNmwxLjI1LTEuMjVhMiAyIDAgMTEyLjgzIDIuODNsLTIuNSAyLjVhMiAyIDAgMDEtMi44MyAwIC43NS43NSAwIDAwLTEuMDYgMS4wNiAzLjUgMy41IDAgMDA0Ljk1IDBsMi41LTIuNWEzLjUgMy41IDAgMDAtNC45NS00Ljk1bC0xLjI1IDEuMjV6bS00LjY5IDkuNjRhMiAyIDAgMDEwLTIuODNsMi41LTIuNWEyIDIgMCAwMTIuODMgMCAuNzUuNzUgMCAwMDEuMDYtMS4wNiAzLjUgMy41IDAgMDAtNC45NSAwbC0yLjUgMi41YTMuNSAzLjUgMCAwMDQuOTUgNC45NWwxLjI1LTEuMjVhLjc1Ljc1IDAgMDAtMS4wNi0xLjA2bC0xLjI1IDEuMjVhMiAyIDAgMDEtMi44MyAweiI+PC9wYXRoPjwvc3ZnPg==
   :class: octicon octicon-link
   :target: #contributing
