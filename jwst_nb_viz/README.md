# JWST Notebook Viz Tools

## Hack Day

Feb 18, RW333 9a-5p:
```
9 - 930: breakfast (provided)
930 - 945: kickoff
945 - 1230: hack
1230 - 130: lunch (provided)
130 - 430: hack
430 - 5: wrap-up
```

### Goal

To produce Jupyter notebooks for JWST-relevant science use cases, to clarify which (if any) visualization tools are needed.

### Building notebooks

For the hack day, feel free to to fast development of notebooks on Box or similar if that's easier to share with team members.  But by the end of the day the notebooks should be at least in Pull Request form into this repo, inside a sub directory inside this directory (see the example).

There is an in-progress example notebook in this repo to show a simple example of the goal for these notebooks.  But bear in mind this is a guideline, and other notebook formats/layouts are still be useful as long as they help with the goal.

### Existing tools for building interactive notebooks

These tools may be useful for the hack day to develop experimental UIs for notebooks.

* Ipywidgets: https://ipywidgets.readthedocs.io/en/stable/ - Basic UI elements like buttons, sliders, etc.
* Glue-jupyter / Glupyter: https://github.com/glue-viz/glue-jupyter - a ipywidgets-based tool for doing data analysis/plotting across multiple datasets in the notebook.
* Astrowidgets: https://astrowidgets.readthedocs.io/en/latest/ - An alpha-level effort to develop astro-specific notebook tools using ipywidgets.  Currently the main functionality is a wrapper around the ginga notebook - essentially a basic "ds9 in the notebook".
* Ginga in "notebook mode": https://gist.github.com/ejeschke/6067409 - ginga is not just in the notebook, but it can be used as a "ds9 in the notebook".  Astrowidgets uses this as a backend so it might be easier to use that, depending on your needs.
* JupyterLab: https://github.com/jupyterlab/jupyterlab - a way to access notebooks that provides a multi-window interface.  E.g., you can "pop out" a view of one of the above tools and have it appear on the sidebar as a separate window.

### Potential tools needing development

The below are areas where STScI might develop tools that might make notebook interactions easier for JWST data.  Knowing which would help with your use cases would be extremely valuable! 

* `jwst_tools` : High-level "helper" functions specifically aimed at accessing JWST data.  E.g. ``spectrum = jwst_tools.get_my_data(proposalid)``
* notebook image viewer : "ds9 in the notebook"
* 1D spectrum viewer : "specviz in the notebook"
* 2D spectrum viewer : a combination of the above two that are linked together
* IFU viewer: "cubeviz in the notebook"
* Pipeline runner : an interactive tool to auto-run the pipeline stages in exactly the way 
* Ramp viewer : A tool to make it easier to look at ramp files in parallel with the image viewer
* Mosaic viewer: "Google maps for astronomical images"  - i.e., only show subsets of very large images that don't fit in the image viewer
* Glupyter: Additional features for the "linked data" element of Glue-jupyter
