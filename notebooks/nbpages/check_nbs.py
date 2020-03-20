
"""
This module contains functionality to check notebooks for possible problems like
executed cells that were erroneously checked in.
"""

import os
import sys
import nbformat
import logging
import argparse
import subprocess

log = logging.getLogger('check_nbs')


def is_executed(nb_path):
    nb = nbformat.read(nb_path, nbformat.NO_CONVERT)
    for cell in nb.cells:
        if cell.cell_type == 'code':
            if cell.outputs:
                return True
    return False


def execution_check(name, full_path):
    log.info('Checking notebook {}'.format(name))
    success = True
    if is_executed(full_path):
        log.error('Notebook {} has executed cells!'.format(name))
        success = False

    return success


def visit_content_nbs(nbpath, visitfunc):
    """
    Visits all the notebooks in the ``nbpath`` that are *not* "exec_*" or in
    ipynb_checkpoints, and calls the ``visitfunc`` on them. Signature of
    ``visitfunc`` should be ``visitfunc(name, nb_full_path)``.
    """
    success = True
    for root, dirs, files in os.walk(nbpath):
        for name in files:
            _, ext = os.path.splitext(name)
            full_path = os.path.join(root, name)
            if ext != '.ipynb':
                continue

            if name.startswith('exec_'):  # skip the executed ones
                continue

            if 'ipynb_checkpoints' in full_path:  # skip checkpoint saves
                continue

            success = visitfunc(name, full_path) and success
    return success


def main(max_commits_to_check_in_range=50):
    """
    Call this to programmatically use this as a command-line script
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--commit-range', default=None, dest='range',
                        help='A range of git commits to check. Must be a valid'
                             'argument for "git rev-list", and git must be '
                             'installed and accessible from the calling shell.')
    args = parser.parse_args()

    logging.basicConfig()
    log.setLevel(logging.INFO)
    if args.range is None:
        success = visit_content_nbs('.', execution_check)
    else:
        initial_branch = subprocess.check_output('git rev-parse --abbrev-ref HEAD', shell=True).decode().strip()
        if initial_branch == 'HEAD':
            # this is just the SHA - probably a detached head
            initial_branch = subprocess.check_output('git rev-parse HEAD', shell=True).decode().strip()
        stash = subprocess.check_output('git stash', shell=True).decode().strip()
        if stash == 'No local changes to save':
            stash = None

        try:
            listcmd = 'git rev-list {}'.format(args.range)
            shas = subprocess.check_output(listcmd, shell=True).decode().strip().split('\n')
            if len(shas) < max_commits_to_check_in_range:
                log.info('Checking {} revisions: '.format(len(shas)))
            else:
                log.info('Got {} revisions, which is too many.  Only doing the {} '
                         'most recent: '.format(len(shas), max_commits_to_check_in_range))
                shas = shas[:max_commits_to_check_in_range]

            success = True
            for sha in shas:
                log.info('Checking SHA "{}"'.format(sha))
                subprocess.check_output('git checkout -q -f {}'.format(sha), shell=True)
                if not visit_content_nbs('.', execution_check):
                    success = False
        finally:
            subprocess.check_output('git checkout ' + initial_branch, shell=True)
            if stash is not None:
                subprocess.check_output('git stash pop', shell=True)

    if success:
        sys.exit(0)
    else:
        log.info("At least one of the checks failed!  Look for ERROR's above")
        sys.exit(1)

if __name__ == '__main__':
    main()
