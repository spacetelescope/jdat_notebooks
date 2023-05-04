This notebook checklist has been made available to us by the [the Notebooks For All team](https://github.com/Iota-School/notebooks-for-all/blob/main/resources/event-hackathon/notebook-authoring-checklist.md).
Its purpose is to serve as a guide for both the notebook author and the technical reviewer highlighting critical aspects to consider when striving to develop an accessible and effective notebook.

### The First Cell

- [ ] The title of the notebook in a first-level heading (eg. `<h1>` or `# in markdown`).
- [ ] A brief description of the notebook.
- [ ] A table of contents in an [ordered list](https://www.markdownguide.org/basic-syntax/#ordered-lists) (`1., 2.,` etc. in Markdown).
- [ ] The author(s) and affiliation(s) (if relevant).
- [ ] The date first published.
- [ ] The date last edited (if relevant).
- [ ] A link to the notebook's source(s) (if relevant).

### The Rest of the Cells

- [ ] There is only one H1 (`#` in Markdown) used in the notebook.
- [ ] The notebook uses other [heading tags](https://www.markdownguide.org/basic-syntax/#headings) in order (meaning it does not skip numbers). 

## Text

- [ ] All link text is descriptive. It tells users where they will be taken if they open the link.
- [ ] All acronyms are defined at least the first time they are used. 
- [ ] Field-specific/specialized terms are used when needed, but not excessively.

## Code

- [ ] Code sections are introduced and explained before they appear in the notebook. This can be fulfilled with a heading in a prior Markdown cell, a sentence preceding it, or a code comment in the code section.
- [ ] Code has explanatory comments (if relevant). This is most important for long sections of code.
- [ ] If the author has control over the syntax highlighting theme in the notebook, that theme has enough color contrast to be legible.
- [ ] Code and code explanations focus on one task at a time. Unless comparison is the point of the notebook, only one method for completing the task is described at a time.

### Images

- [ ] All images (jpg, png, svgs) have an [image description](https://www.w3.org/WAI/tutorials/images/decision-tree/). This could be
    - [ ] [Alt text](https://developer.mozilla.org/en-US/docs/Web/API/HTMLImageElement/alt) (an `alt` property) 
    - [ ] [Empty alt text](https://developer.mozilla.org/en-US/docs/Web/API/HTMLImageElement/alt#decorative_images) for decorative images/images meant to be skipped (an `alt` attribute with no value)
    - [ ] Captions
    - [ ] If no other options will work, the image is decribed in surrounding paragraphs.

- [ ] Any [text present in images](https://www.w3.org/WAI/WCAG21/Understanding/images-of-text.html) exists in a text form outside of the image (this can be alt text, captions, or surrounding text.)

### Visualizations

- [ ] All visualizations have an image description. Review the previous section, Images, for more information on how to add it.
- [ ] [Visualization descriptions](http://diagramcenter.org/specific-guidelines-e.html) include
    - [ ] The type of visualization (like bar chart, scatter plot, etc.)
    - [ ] Title
    - [ ] Axis labels and range
    - [ ] Key or legend
    - [ ] An explanation of the visualization's significance to the notebook (like the trend, an outlier in the data, what the author learned from it, etc.)

- [ ] All visualizations and their parts have [enough color contrast](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html) ([color contrast checker](https://webaim.org/resources/contrastchecker/)) to be legible. Remember that transparent colors have lower contrast than their opaque versions.
- [ ] All visualizations [convey information with more visual cues than color coding](https://www.w3.org/WAI/WCAG21/Understanding/use-of-color.html). Use text labels, patterns, or icons alongside color to achieve this.
- [ ] All visualizations have an additional way for notebook readers to access the information. Linking to the original data, including a table of the data in the same notebook, or sonifying the plot are all options.