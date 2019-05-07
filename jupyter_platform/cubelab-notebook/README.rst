cubelab_notebook
================

.. image:: https://img.shields.io/pypi/v/cubelab_notebook.svg
    :target: https://pypi.python.org/pypi/cubelab_notebook
    :alt: Latest PyPI version

.. image:: https://travis-ci.org/nmearl/cubelab-notebook.png
   :target: https://travis-ci.org/nmearl/cubelab-notebook
   :alt: Latest Travis CI build status

This example package attempts to mimick the structure of a desktop-based Qt
application by creating individual widget elements and exposing events as one
might expect in a desktop framework.

Usage
-----

Once installed launch a Jupyter Notebook (*not* Lab) environment. The included
notebook demonstrates importing the ``Application`` class and instantiating
it to render the ipywidgets collection.

Installation
------------

To use, install the package into your current environment via

.. code-block:: bash

    $ pip install .

Requirements
^^^^^^^^^^^^

- Numpy
- Jupyter
- Plotly

Authors
-------

`cubelab_notebook` was written by `Nicholas Earl <nearl@stsci.edu>`_.
