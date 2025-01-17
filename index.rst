=======================================================
JWST Data Analysis Tool Notebooks
=======================================================

The `jdat_notebooks repository <https://github.com/spacetelescope/jdat_notebooks>`_
contains notebooks illustrating workflows for post-pipeline analysis of JWST data.
Some of the notebooks also illustrate generic
analysis workflows that are applicable to data from other observatories
as well. This repository and the notebooks are one component of STScI's
larger `Data Analysis Tools
Ecosystem <https://jwst-docs.stsci.edu/jwst-post-pipeline-data-analysis>`_.

Summary Listing and Descriptions
================================

The sidebar on the left of this page provides a summery listing of the notebooks,
and clicking will take you to html-rendered
versions of the notebooks. These are easily readable, and
require no special tools beyond your web browser. The notebooks are
organized by JWST instrument, or are marked as
cross-instrument. At the top of each notebook you will find a brief
description of the specific science use case
that is demonstrated by the notebook, a description of the data that are used,
and a listing of the data analysis tools that
are demonstrated by the use case.

Installation Instructions
=========================

To download and execute the notebooks, we recommend that you
clone the `jdat_notebooks repository <https://github.com/spacetelescope/jdat_notebooks>`_
to your local computer as described
in the :ref:`installation instructions <install>`.

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
to contribute new notebooks or major reworks of existing notebooks, see the `contributing
instructions <https://github.com/spacetelescope/jdat_notebooks/blob/main/CONTRIBUTING.rst/>`__.
The notebooks attempt to utilize a number of software packages supported by
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
