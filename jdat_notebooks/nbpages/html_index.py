import os
import jinja2


def make_html_index(converted_files, html_template, outfn='index.html',
                    relpaths=True):
    """
    Generates an html index page for a set of notebooks

    Parameters
    ----------
    converted_files : list
        The list of paths to the notebooks
    html_template : str
        A path to the template file to be used for generating the index. The
        template should be in jinja2 format and have a loop over
        ``notebook_html_paths`` to populate with the links
    outfn : str or None
        the output file name, or None to not write the file
    relpaths : bool
        If True, the paths are all passed in as relative paths with respect to
        ``outfn`` if given or the current directory (if ``outfn`` is None)

    Returns
    -------
    content : str
        The content of the index file
    """
    path, fn = os.path.split(html_template)
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(path),
                             autoescape=jinja2.select_autoescape(['html', 'xml']))
    templ = env.get_template(fn)

    if relpaths:
        outdir = os.path.realpath(os.path.dirname(outfn) if outfn else os.path.curdir)
        converted_files = [os.path.relpath(os.path.realpath(pth), outdir)
                           for pth in converted_files]

    content = templ.render(notebook_html_paths=converted_files)
    if outfn:
        with open(outfn, 'w') as f:
            f.write(content)
    return content
