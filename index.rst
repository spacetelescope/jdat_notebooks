<img src="images/Jspectra.svg" class="logo"
alt="JWST Data Analysis Notebooks" />

Filter Notebooks

<span
id="user-content-james-webb-space-telescope-data-analysis-tool-notebooks"></span>

## <a href="#james-webb-space-telescope-data-analysis-tool-notebooks"
id="user-content-james-webb-space-telescope-data-analysis-tool-notebooks"
class="anchor" aria-hidden="true"><img
src="data:image/svg+xml;base64,PHN2ZyBjbGFzcz0ib2N0aWNvbiBvY3RpY29uLWxpbmsiIHZpZXdib3g9IjAgMCAxNiAxNiIgdmVyc2lvbj0iMS4xIiB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIGFyaWEtaGlkZGVuPSJ0cnVlIj48cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik03Ljc3NSAzLjI3NWEuNzUuNzUgMCAwMDEuMDYgMS4wNmwxLjI1LTEuMjVhMiAyIDAgMTEyLjgzIDIuODNsLTIuNSAyLjVhMiAyIDAgMDEtMi44MyAwIC43NS43NSAwIDAwLTEuMDYgMS4wNiAzLjUgMy41IDAgMDA0Ljk1IDBsMi41LTIuNWEzLjUgMy41IDAgMDAtNC45NS00Ljk1bC0xLjI1IDEuMjV6bS00LjY5IDkuNjRhMiAyIDAgMDEwLTIuODNsMi41LTIuNWEyIDIgMCAwMTIuODMgMCAuNzUuNzUgMCAwMDEuMDYtMS4wNiAzLjUgMy41IDAgMDAtNC45NSAwbC0yLjUgMi41YTMuNSAzLjUgMCAwMDQuOTUgNC45NWwxLjI1LTEuMjVhLjc1Ljc1IDAgMDAtMS4wNi0xLjA2bC0xLjI1IDEuMjVhMiAyIDAgMDEtMi44MyAweiI+PC9wYXRoPjwvc3ZnPg=="
class="octicon octicon-link" /></a>James Webb Space Telescope Data Analysis Tool Notebooks

The `jdat_notebooks` repository contains notebooks illustrating
workflows for post-pipeline analysis of JWST data. Some of the notebooks
also illustrate generic analysis workflows that are applicable to data
from other observatories as well. This repository and the notebooks are
one component of STScI's larger
<a href="https://jwst-docs.stsci.edu/jwst-post-pipeline-data-analysis"
rel="nofollow">Data Analysis Tools Ecosystem</a>.

The following table summarizes the notebooks currently available. Most
links will take you to rendered versions of the notebooks, which require
no special tools beyond your web browser. To download and execute the
notebooks, [clone](https://github.com/git-guides/git-clone) this
[repository](https://github.com/spacetelescope/jdat_notebooks) to your
local computer. Most of the notebooks rely on packages that can be
installed using
<a href="https://pip.pypa.io/en/stable/" rel="nofollow">pip</a>. The
version dependencies are listed in the environment.yaml and in the
requirements file in each notebook folder.

<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<thead data-valign="bottom">
<tr class="header">
<th colspan="2">JWST Science Analysis Notebooks</th>
</tr>
<tr class="odd">
<th>Notebook</th>
<th>Description</th>
</tr>
<tr class="header">
<th colspan="2">Cross-Instrument</th>
</tr>
</thead>
<tbody data-valign="top">
<tr class="odd">
<td><a href="jdat_notebooks/asdf_example/asdf_example.html"
rel="nofollow">asdf</a></td>
<td><ul>
<li>Use case: create ASDF (Advanced Scientific Data Format) file from
FITS file.</li>
<li>Data: CANDELS image of the COSMOS field.</li>
<li>Tools: asdf, gwcs, astrocut.</li>
<li>Cross-instrument: all instruments.</li>
</ul></td>
</tr>
<tr class="even">
<td><a
href="jdat_notebooks/background_estimation_imaging/Imaging%20Sky%20Background%20Estimation.html"
rel="nofollow">Background Estimation</a></td>
<td><ul>
<li>Use case: estimate the sky background in complex scenes.</li>
<li>Data: images with pathological background pattern created in the
notebook.</li>
<li>Tools: photutils</li>
<li>Cross-instrument: all instruments.</li>
</ul></td>
</tr>
<tr class="odd">
<td>Redshift Cross-Corr</td>
<td><ul>
<li>Use case: reproduce the workflow of the IRAF task XCORFIT to measure
redshift.</li>
<li>Data: LEGA-C spectra and galaxy template spectra; optical
rest-frame.</li>
<li>Tools: specutils.</li>
<li>Cross-instrument: all instruments.</li>
</ul></td>
</tr>
<tr class="even">
<td><a href="jdat_notebooks/NIRSpec_MAST_Query/NIRSpec_MAST_Query.html"
rel="nofollow">Querying MAST</a></td>
<td><ul>
<li>Use case: How to submit a NIRSpec MAST Query using python.</li>
<li>Data:</li>
<li>Tools: mast, astroquery.</li>
<li>Cross-instrument: all instruments.</li>
</ul></td>
</tr>
<tr class="odd">
<td><a
href="jdat_notebooks/specviz_notebookGUI_interaction/specviz_notebook_gui_interaction_redshift.html"
rel="nofollow">Specviz GUI</a></td>
<td><ul>
<li>Use case: How to inspect and export spectra in Specviz GUI.</li>
<li>Data: NIRISS simulation generated with the code MIRAGE.</li>
<li>Tools: specutils, jdaviz.</li>
<li>Cross-instrument: all instruments.</li>
</ul></td>
</tr>
<tr class="even">
<td><a
href="jdat_notebooks/IFU_cube_continuum_fit/NGC4151_FeII_ContinuumFit.html"
rel="nofollow">IFU Cube Fitting</a></td>
<td><ul>
<li>Use case: continuum and emission-line modeling of galaxy IFU
spectra.</li>
<li>Data: Spitzer IRS on Messier 58.</li>
<li>Tools: specutils, custom functions.</li>
<li>Cross-instrument: MIRI, NIRSpec.</li>
</ul></td>
</tr>
<tr class="odd">
<td colspan="2">NIRCam</td>
</tr>
<tr class="even">
<td><a
href="jdat_notebooks/NIRCam_photometry/NIRCam%20multiband%20photometry.html"
rel="nofollow">Multiband Extended Aperture Photometry</a></td>
<td><ul>
<li>Use case: measure extended galaxy photometry in a field.</li>
<li>Data: Simulated NIRCam images from JADES GTO extragalactic blank
field.</li>
<li>Tools: photutils.</li>
<li>Cross-instrument:</li>
</ul></td>
</tr>
<tr class="odd">
<td><a
href="jdat_notebooks/aperture_photometry/NIRCam_Aperture_Photometry_Example.html"
rel="nofollow">Crowded Field Aperture Photometry</a></td>
<td><ul>
<li>Use case: Crowded field imaging with Aperture-fitting
photometry.</li>
<li>Data: Simulated NIRCam images of LMC astrometric calibration
field.</li>
<li>Tools: jwst pipeline, photutils.</li>
<li>Cross-instrument:</li>
</ul></td>
</tr>
<tr class="even">
<td><a
href="jdat_notebooks/psf_photometry/NIRCam_PSF_Photometry_Example.html"
rel="nofollow">PSF Photometry</a></td>
<td><ul>
<li>Use case: Crowded field imaging with PSF-fitting photometry.</li>
<li>Data: Simulated NIRCam images of LMC astrometric calibration
field.</li>
<li>Tools: webbpsf, photutils.</li>
<li>Cross-instrument:</li>
</ul></td>
</tr>
<tr class="odd">
<td><a
href="jdat_notebooks/NIRCam_PSF-matched_photometry/NIRCam_PSF_matched_multiband_photometry.html"
rel="nofollow">PSF Matching Photometry</a></td>
<td><ul>
<li>Use case: Crowded field imaging with PSF-fitting photometry.</li>
<li>Data: Simulated NIRCam images of LMC astrometric calibration
field.</li>
<li>Tools: webbpsf, photutils.</li>
<li>Cross-instrument:</li>
</ul></td>
</tr>
<tr class="even">
<td colspan="2">NIRISS</td>
</tr>
<tr class="odd">
<td>WFSS Spectra <a
href="jdat_notebooks/NIRISS_WFSS_postpipeline/00.%20Optimal%20extraction.html"
rel="nofollow">Notebook 0</a> <a
href="jdat_notebooks/NIRISS_WFSS_postpipeline/01.%20Combine%20and%20normalize%201D%20spectra.html"
rel="nofollow">Notebook 1</a> <a
href="jdat_notebooks/NIRISS_WFSS_postpipeline/02.%20Cross%20correlation%20template.html"
rel="nofollow">Notebook 2</a> <a
href="jdat_notebooks/NIRISS_WFSS_postpipeline/03.%20Spatially%20resolved%20emission%20line%20map.html"
rel="nofollow">Notebook 3</a></td>
<td><ul>
<li>Use case: Optimal extraction and analysis of grism spectra.</li>
<li>Data: Simulated NIRISS spectra of a galaxy cluster</li>
<li>Tools: specutils .</li>
<li>Cross-instrument: NIRSpec.</li>
</ul></td>
</tr>
<tr class="even">
<td><a href="jdat_notebooks/mos-spectroscopy/MOSspec_sv06_revised.html"
rel="nofollow">MOS spctra</a></td>
<td><ul>
<li>Use case: Emission-line measurements and template matching on 1D
spectra.</li>
<li>Data: LEGA-C spectra and galaxy template spectra; optical
rest-frame.</li>
<li>Tools: specutils.</li>
<li>Cross-instrument: NIRSpec.</li>
</ul></td>
</tr>
<tr class="odd">
<td><a href="https://github.com/spacetelescope/jdat_jdat_"
data-jdat_notebooks="" data-tree="" data-main="" data-notebooks=""
data-soss-transit-spectroscopy"="">SOSS Transiting Exoplanet</a></td>
<td><ul>
<li>Use case: Primary transit of an exoplanet.</li>
<li>Data: Simulated transit using awesomesoss.</li>
<li>Tools: jwst pipeline, juliet.</li>
<li>Cross-instrument:</li>
</ul></td>
</tr>
<tr class="even">
<td>AMI Binary Star</td>
<td><ul>
<li>Use case: Find the binary parameters of AB Dor.</li>
<li>Data: Simulated MIRAGE data for a binary point source.</li>
<li>Tools: jwst pipeline, nrm_analysis.</li>
<li>Cross-instrument:</li>
</ul></td>
</tr>
<tr class="odd">
<td colspan="2">NIRSpec</td>
</tr>
<tr class="even">
<td><a
href="jdat_notebooks/IFU_cube_continuum_fit/NGC4151_FeII_ContinuumFit.html"
rel="nofollow">IFU Analysis</a></td>
<td><ul>
<li>Use case: Continuum and emission-line modeling of AGN;
1.47-1.87um.</li>
<li>Data: NIFS on Gemini; NGC 4151.</li>
<li>Tools: specutils, cubeviz.</li>
<li>Cross-instrument:</li>
</ul></td>
</tr>
<tr class="odd">
<td><a
href="jdat_notebooks/optimal_extraction/Spectral%20Extraction-static.html"
rel="nofollow">MOS Optimal Extraction</a></td>
<td><ul>
<li>Use case: Optimal spectral extraction.</li>
<li>Data: Simulated NIRSpec MOS data; point sources.</li>
<li>Tools: jwst pipeline</li>
<li>Cross-instrument:</li>
</ul></td>
</tr>
<tr class="even">
<td><a href="https://github.com/spacetelescope/jdat_jdat_"
data-jdat_notebooks="" data-tree="" data-main="" data-notebooks=""
data-preimaging"="">MOS Pre-Imaging</a></td>
<td><ul>
<li>Use case: Simulation of NIRCam pre-imaging for NIRSpec.</li>
<li>Data: Simulated NIRCam images of LMC astrometric calibration
field.</li>
<li>Tools: jwst pipeline.</li>
<li>Cross-instrument: NIRCam.</li>
</ul></td>
</tr>
<tr class="odd">
<td><a
href="jdat_notebooks/transit_spectroscopy_notebook/Exoplanet_Transmission_Spectra_JWST.html"
rel="nofollow">BOTS Transiting Exoplanet</a></td>
<td><ul>
<li>Use case: Primary transit of an exoplanet.</li>
<li>Data: Simulated NIRSpec data from ground-based campaign.</li>
<li>Tools:</li>
<li>Cross-instrument:</li>
</ul></td>
</tr>
<tr class="even">
<td><a href="jdat_notebooks/ifu_optimal/ifu_optimal.html"
rel="nofollow">IFU Optimal Extraction</a></td>
<td><ul>
<li>Use case: Optimal spectral extraction.</li>
<li>Data: Simulated data of faint (quasar) point source.</li>
<li>Tools: jwst, scipy, specutils, jdaviz, photutils, astropy.io,
astropy.wcs</li>
<li>Cross-instrument:</li>
</ul></td>
</tr>
<tr class="odd">
<td colspan="2">MIRI</td>
</tr>
<tr class="even">
<td><a
href="jdat_notebooks/tree/main/notebooks/MIRI_LRS_spectral_extraction">LRS
Optimal Extraction</a></td>
<td><ul>
<li>Use case: Optimal spectral extraction.</li>
<li>Data: MIRISim simulated spectra.</li>
<li>Tools: jwst pipeline, gwcs.</li>
<li>Cross-instrument:</li>
</ul></td>
</tr>
<tr class="odd">
<td><a
href="jdat_notebooks/MRS_Mstar_analysis/JWST_Mstar_dataAnalysis_usecase.html"
rel="nofollow">IFU Cube 1</a></td>
<td><ul>
<li>Use case: Extract spatial-spectral features from IFU cube.</li>
<li>Data: KMOS datacube of point sources in the LMC.</li>
<li>Tools: specutils, spectral_cube, photutils.</li>
<li>Cross-instrument:</li>
</ul></td>
</tr>
<tr class="even">
<td><a
href="jdat_notebooks/MIRI_IFU_YSOs_in_the_LMC/isha_nayak_ysos_in_the_lmc.html"
rel="nofollow">IFU Cube 2</a></td>
<td><ul>
<li>Use case: Photutils to automatically detect point sources and
extract photometry</li>
<li>Data: ALMA 13CO data cubes.</li>
<li>Tools: specutils, spectral_cube, photutils.</li>
<li>Cross-instrument:</li>
</ul></td>
</tr>
</tbody>
</table>

<span id="user-content-help"></span>

## <a href="#help" id="user-content-help" class="anchor"
aria-hidden="true"><img
src="data:image/svg+xml;base64,PHN2ZyBjbGFzcz0ib2N0aWNvbiBvY3RpY29uLWxpbmsiIHZpZXdib3g9IjAgMCAxNiAxNiIgdmVyc2lvbj0iMS4xIiB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIGFyaWEtaGlkZGVuPSJ0cnVlIj48cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik03Ljc3NSAzLjI3NWEuNzUuNzUgMCAwMDEuMDYgMS4wNmwxLjI1LTEuMjVhMiAyIDAgMTEyLjgzIDIuODNsLTIuNSAyLjVhMiAyIDAgMDEtMi44MyAwIC43NS43NSAwIDAwLTEuMDYgMS4wNiAzLjUgMy41IDAgMDA0Ljk1IDBsMi41LTIuNWEzLjUgMy41IDAgMDAtNC45NS00Ljk1bC0xLjI1IDEuMjV6bS00LjY5IDkuNjRhMiAyIDAgMDEwLTIuODNsMi41LTIuNWEyIDIgMCAwMTIuODMgMCAuNzUuNzUgMCAwMDEuMDYtMS4wNiAzLjUgMy41IDAgMDAtNC45NSAwbC0yLjUgMi41YTMuNSAzLjUgMCAwMDQuOTUgNC45NWwxLjI1LTEuMjVhLjc1Ljc1IDAgMDAtMS4wNi0xLjA2bC0xLjI1IDEuMjVhMiAyIDAgMDEtMi44MyAweiI+PC9wYXRoPjwvc3ZnPg=="
class="octicon octicon-link" /></a>Help

If you uncover any issues or bugs, you can open a GitHub ticket. For
faster responses, however, we encourage you to submit a JWST Help Desk
Ticket: jwsthelp.stsci.edu

<span id="user-content-contributing"></span>

## <a href="#contributing" id="user-content-contributing" class="anchor"
aria-hidden="true"><img
src="data:image/svg+xml;base64,PHN2ZyBjbGFzcz0ib2N0aWNvbiBvY3RpY29uLWxpbmsiIHZpZXdib3g9IjAgMCAxNiAxNiIgdmVyc2lvbj0iMS4xIiB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIGFyaWEtaGlkZGVuPSJ0cnVlIj48cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik03Ljc3NSAzLjI3NWEuNzUuNzUgMCAwMDEuMDYgMS4wNmwxLjI1LTEuMjVhMiAyIDAgMTEyLjgzIDIuODNsLTIuNSAyLjVhMiAyIDAgMDEtMi44MyAwIC43NS43NSAwIDAwLTEuMDYgMS4wNiAzLjUgMy41IDAgMDA0Ljk1IDBsMi41LTIuNWEzLjUgMy41IDAgMDAtNC45NS00Ljk1bC0xLjI1IDEuMjV6bS00LjY5IDkuNjRhMiAyIDAgMDEwLTIuODNsMi41LTIuNWEyIDIgMCAwMTIuODMgMCAuNzUuNzUgMCAwMDEuMDYtMS4wNiAzLjUgMy41IDAgMDAtNC45NSAwbC0yLjUgMi41YTMuNSAzLjUgMCAwMDQuOTUgNC45NWwxLjI1LTEuMjVhLjc1Ljc1IDAgMDAtMS4wNi0xLjA2bC0xLjI1IDEuMjVhMiAyIDAgMDEtMi44MyAweiI+PC9wYXRoPjwvc3ZnPg=="
class="octicon octicon-link" /></a>Contributing

Contributions are welcome from both the scientist and developer
community. If you wish to contribute fixes or clarifications to existing
notebooks, feel free to do so directly to this repository. If you wish
to contribute new notebooks or major reworks of existing notebooks, we
refer you to
[dat\_pyinthesky](https://github.com/spacetelescope/dat_pyinthesky/tree/master/jdat_notebooks).
For details on how to provide such contributions, see the
<a href="https://github.com/spacetelescope/jdat_jdat_"
data-jdat_notebooks="" data-blob="" data-main=""
data-contributing.md"="">contributing instructions</a>.

The notebooks attempt to utilize a number of software packages supported
by STScI, including
<a href="https://www.astropy.org" rel="nofollow">Astropy</a>,
<a href="http://docs.glueviz.org/en/stable/index.html"
rel="nofollow">glue</a>,
<a href="https://ginga.readthedocs.io/en/latest/"
rel="nofollow">ginga</a>,
<a href="https://photutils.readthedocs.io" rel="nofollow">photutils</a>,
<a href="https://specutils.readthedocs.io/en/stable/"
rel="nofollow">specutils</a>,
<a href="http://astroimtools.readthedocs.io"
rel="nofollow">astroimtools</a>,
<a href="http://imexam.readthedocs.io" rel="nofollow">imexam</a>,
<a href="https://jdaviz.readthedocs.io/en/latest/"
rel="nofollow">jdaviz</a>,
<a href="http://asdf.readthedocs.io/en/latest/" rel="nofollow">asdf</a>,
<a href="https://gwcs.readthedocs.io/en/latest/" rel="nofollow">gwcs</a>,
and <a href="http://synphot.readthedocs.io/en/latest/index.html"
rel="nofollow">synphot</a>. Note jdaviz is STScI's JWST Data Analysis
Visualization Tool, designed to be used with spectra, IFU cubes, and
multi-object spectroscopy (MOS).
