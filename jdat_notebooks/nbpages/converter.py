# Standard library
from os import path, walk, remove, makedirs

import re
import time
import logging
import argparse
from urllib import request

from nbconvert.preprocessors import ExecutePreprocessor, CellExecutionError
from nbconvert.exporters import RSTExporter, HTMLExporter
from nbconvert.writers import FilesWriter
import nbformat

__all__ = ['NBPagesConverter', 'process_notebooks', 'make_parser', 'run_parsed']

logger = logging.getLogger('nbpages')
def init_logger():
    logger.setLevel(logging.INFO)
    logging.basicConfig()
    logging.captureWarnings(True)


class NBPagesConverter(object):
    def __init__(self, nb_path, output_path=None, template_file=None,
                 overwrite=False, kernel_name=None, output_type='rst',
                 nb_version=4, base_path=None):
        self.nb_path = path.abspath(nb_path)
        fn = path.basename(self.nb_path)
        self.path_only = path.dirname(self.nb_path)
        self.nb_name, _ = path.splitext(fn)
        self.nb_version = nb_version
        self.base_path = base_path

        if output_type.upper() not in ('HTML', 'RST'):
            raise ValueError('output_type has to be either html or rst')
        self._output_type = output_type.upper()

        if output_path is not None:
            self.output_path = output_path
            makedirs(self.output_path, exist_ok=True)
        else:
            self.output_path = self.path_only

        if template_file is not None:
            self.template_file = path.abspath(template_file)
        else:
            self.template_file = None

        self.overwrite = overwrite

        # the executed notebook
        self._executed_nb_path = path.join(self.output_path,
                                           'exec_{0}'.format(fn))

        logger.info('Processing notebook {0} (in {1})'.format(fn,
                                                              self.path_only))

        # the RST file
        self._output_path = path.join(self.output_path,
                                   '{0}.{1}'.format(self.nb_name, self._output_type.lower()))

        self._execute_kwargs = dict(timeout=900)
        if kernel_name:
            self._execute_kwargs['kernel_name'] = kernel_name

    def execute(self, write=True):
        """
        Execute the specified notebook file, and optionally write out the
        executed notebook to a new file.

        Parameters
        ----------
        write : bool, optional
            Write the executed notebook to a new file, or not.

        Returns
        -------
        executed_nb_path : str, ``None``
            The path to the executed notebook path, or ``None`` if
            ``write=False``.

        """

        if path.exists(self._executed_nb_path) and not self.overwrite:
            logger.debug("Executed notebook already exists at {0}. Use "
                         "overwrite=True or --overwrite (at cmd line) to re-run"
                         .format(self._executed_nb_path))
            return self._executed_nb_path

        # Execute the notebook
        logger.debug('Executing notebook using kwargs '
                     '"{}"...'.format(self._execute_kwargs))
        executor = ExecutePreprocessor(**self._execute_kwargs)

        with open(self.nb_path) as f:
            nb = nbformat.read(f, as_version=self.nb_version)

        st = time.time()
        try:
            executor.preprocess(nb, {'metadata': {'path': self.path_only}})
        except CellExecutionError:
            # TODO: should we fail fast and raies, or record all errors?
            raise
        et = time.time()
        logger.info('Execution of notebook {} took {} sec'.format(self.nb_name,
                    et - st))

        if write:
            logger.debug('Writing executed notebook to file {0}...'
                         .format(self._executed_nb_path))
            with open(self._executed_nb_path, 'w') as f:
                nbformat.write(nb, f)

            return self._executed_nb_path

    def convert(self, remove_executed=False):
        """
        Convert the executed notebook to a restructured text (RST) file or HTML.

        Parameters
        ----------
        delete_executed : bool, optional
            Controls whether to remove the executed notebook or not.

        """

        if not path.exists(self._executed_nb_path):
            raise IOError("Executed notebook file doesn't exist! Expected: {0}"
                          .format(self._executed_nb_path))

        if path.exists(self._output_path) and not self.overwrite:
            logger.debug("{0} version of notebook already exists at {1}. Use "
                         "overwrite=True or --overwrite (at cmd line) to re-run"
                         .format(self._output_type, self._output_path))
            return self._output_path

        # Initialize the resources dict - see:
        # https://github.com/jupyter/nbconvert/blob/master/nbconvert/nbconvertapp.py#L327
        resources = {}
        resources['config_dir'] = ''  # we don't need to specify config
        resources['unique_key'] = self.nb_name

        # path to store extra files, like plots generated
        resources['output_files_dir'] = 'nboutput'

        if self.base_path is None:
            path_to_root = ''
        else:
            path_to_root = path.relpath(self.base_path,
                                        start=path.split(self.nb_path)[0])
            path_to_root += path.sep
        resources['path_to_pages_root'] = request.pathname2url(path_to_root)

        # Exports the notebook to the output format
        logger.debug('Exporting notebook to {}...'.format(self._output_type))
        if self._output_type == 'RST':
            exporter = RSTExporter()
        elif self._output_type == 'HTML':
            exporter = HTMLExporter()
        else:
            raise ValueError('This should be impossible... output_type should '
                             'have been checked earlier, but it is '
                             'unrecognized')

        if self.template_file:
            exporter.template_file = self.template_file
        output, resources = exporter.from_filename(self._executed_nb_path,
                                                   resources=resources)

        # Write the output file
        writer = FilesWriter()
        output_file_path = writer.write(output, resources,
                                        notebook_name=self.nb_name)

        if self._output_type == 'RST':
            self._add_filter_keywords(output_file_path)

        if remove_executed:  # optionally, clean up the executed notebook file
            remove(self._executed_nb_path)

        return output_file_path

    def _add_filter_keywords(self, output_file_path):
        """
        read the executed notebook, grab the keywords from the header,
        add them in to the output as filter keywords
        """
        with open(self._executed_nb_path) as f:
            nb = nbformat.read(f, as_version=self.nb_version)

        top_cell_text = nb['cells'][0]['source']
        match = re.search('## [kK]eywords\s+(.*)', top_cell_text)

        if match:
            keywords = match.groups()[0].split(',')
            keywords = [clean_keyword(k) for k in keywords if k.strip()]
            keyword_filters = ['filter{0}'.format(k) for k in keywords]
        else:
            keyword_filters = []

        # Add metatags to top of RST files to get rendered into HTML, used for
        # the search and filter functionality in Learn Astropy
        meta_tutorials = '.. meta::\n    :keywords: {0}\n'
        filters = ['filterTutorials'] + keyword_filters
        meta_tutorials = meta_tutorials.format(', '.join(filters))
        with open(output_file_path, 'r') as f:
            rst_text = f.read()

        with open(output_file_path, 'w') as f:
            rst_text = '{0}\n{1}'.format(meta_tutorials, rst_text)
            f.write(rst_text)


def process_notebooks(nbfile_or_path, exec_only=False, exclude=[], include=[],
                      **kwargs):
    """
    Execute and optionally convert the specified notebook file or directory of
    notebook files.

    This is a wrapper around the ``NBPagesConverter`` class that does file
    handling.

    Parameters
    ----------
    nbfile_or_path : str
        Either a single notebook filename or a path containing notebook files.
    exec_only : bool, optional
        Just execute the notebooks, don't run them.
    exclude : list
        A list of notebook name patterns (*full path* regex's) to exclude.
    include : list
        A list of notebook name patterns (*full path* regex's) to include.
        Cannot be given at the same time as ``exclude``.
    **kwargs
        Any other keyword arguments are passed to the ``NBPagesConverter``
        init.

    """
    exclude_res = [re.compile(ex) for ex in exclude]
    include_res = [re.compile(ix) for ix in include]
    if include_res and exclude_res:
        raise ValueError('cannot give both include and exclude patterns at the '
                         'same time')

    converted = []
    if path.isdir(nbfile_or_path):
        kwargs.setdefault('base_path', nbfile_or_path)
        # It's a path, so we need to walk through recursively and find any
        # notebook files
        for root, dirs, files in walk(nbfile_or_path):
            for name in files:
                _, ext = path.splitext(name)
                full_path = path.join(root, name)

                if 'ipynb_checkpoints' in full_path:  # skip checkpoint saves
                    continue

                if name.startswith('exec'):  # notebook already executed
                    continue

                if ext == '.ipynb':
                    if any([rex.match(full_path) for rex in exclude_res]):
                        logger.info("Skipping {} because it is in the exclude list".format(full_path))
                        continue
                    if include_res and not any([rex.match(full_path) for rex in include_res]):
                        logger.info("Skipping {} because it is not in the include list".format(full_path))
                        continue

                    nbc = NBPagesConverter(full_path, **kwargs)
                    nbc.execute()

                    if not exec_only:
                        converted.append(nbc.convert())

    else:
        # It's a single file, so convert it
        nbc = NBPagesConverter(nbfile_or_path, **kwargs)
        nbc.execute()

        if not exec_only:
            converted.append(nbc.convert())

    return converted


def clean_keyword(kw):
    """Given a keyword parsed from the header of one of the tutorials, return
    a 'cleaned' keyword that can be used by the filtering machinery.

    - Replaces spaces with capital letters
    - Removes . / and space
    """
    return kw.strip().title().replace('.', '').replace('/', '').replace(' ', '')


def make_parser(parser=None):
    """
    Generate an `argparse.ArgumentParser` for nbpages
    """
    if parser is None:
        parser = argparse.ArgumentParser()
    parser.description = ('A command-line tool leveraging nbconvert to execute '
                          'a set of notebooks and convert then to html or rst.')

    vq_group = parser.add_mutually_exclusive_group()
    vq_group.add_argument('-v', '--verbose', action='count', default=0,
                          dest='verbosity')
    vq_group.add_argument('-q', '--quiet', action='count', default=0,
                          dest='quietness')

    parser.add_argument('--exec-only', default=False, action='store_true',
                        dest='exec_only', help='Just execute the notebooks, '
                                               'don\'t convert them as well. '
                                               'This is useful for testing that'
                                               ' the notebooks run.')

    parser.add_argument('-o', '--overwrite', action='store_true',
                        dest='overwrite', default=False,
                        help='Re-run and overwrite any existing executed '
                             'notebook or converted files.')

    parser.add_argument('--template', default=None, dest='template_file',
                        help='The path to a jinja2 template file for the '
                             'conversion.  The template operates in a context '
                             'determined by the exporter.')

    parser.add_argument('--output-path', default=None, dest='output_path',
                        help='The path to save all executed or converted '
                             'notebook files. If not specified, the executed/'
                             'converted files will be in the same path as the '
                             'source notebooks.')

    parser.add_argument('--kernel-name', default='python3', dest='kernel_name',
                        help='The name of the kernel to run the notebooks with.'
                             ' Must be an available kernel from "jupyter '
                             'kernelspec list".')

    parser.add_argument('--notebook-version', default=4, dest='nb_version',
                        help='The version of the notebook format to convert to'
                             ' for execution.')

    parser.add_argument('--exclude', default=None,
                        help='A comma-separated list of notebook names to '
                             'exclude.')

    parser.add_argument('--include', default=None,
                        help='A comma-separated list of notebook names to '
                             'include. Cannot be given at the same time as '
                             'exclude.')
    return parser


def run_parsed(nbfile_or_path, output_type, args, **kwargs):
    init_logger()
    # Set logger level based on verbose flags
    if args.verbosity != 0:
        if args.verbosity == 1:
            logger.setLevel(logging.DEBUG)
        else:  # anything >= 2
            logger.setLevel(1)

    elif args.quietness != 0:
        if args.quietness == 1:
            logger.setLevel(logging.WARNING)
        else:  # anything >= 2
            logger.setLevel(logging.ERROR)

    # make sure output path exists
    output_path = args.output_path
    if output_path is not None:
        output_path = path.abspath(output_path)
        makedirs(output_path, exist_ok=True)

    # make sure the template file exists
    template_file = args.template_file
    if template_file is not None and not path.exists(template_file):
        raise IOError("Couldn't find template file at {0}"
                      .format(template_file))

    if args.exclude is None:
        exclude_list = []
    else:
        exclude_list = [ex if ex.startswith('.*') else '.*?' + ex
                        for ex in args.exclude.split(',')]

    if args.include is None:
        include_list = []
    else:
        include_list = [inc if inc.startswith('.*') else '.*?' + inc
                        for inc in args.include.split(',')]

    return process_notebooks(nbfile_or_path, exec_only=args.exec_only,
                      output_path=output_path, template_file=template_file,
                      overwrite=args.overwrite, kernel_name=args.kernel_name,
                      output_type=output_type, nb_version=args.nb_version,
                      exclude=exclude_list, include=include_list, **kwargs)


if __name__ == "__main__":
    parser = make_parser()

    parser.add_argument('nbfile_or_path',
                        help='Path to a specific notebook file, or the '
                             'top-level path to a directory containing notebook'
                             ' files to process.')

    parser.add_argument('convertto', help='output type to convert to.  Must be '
                                          'one of "RST" or "HTML"')

    args = parser.parse_args()
    run_parsed(args.nbfile_or_path, args.convertto.upper(), args)
