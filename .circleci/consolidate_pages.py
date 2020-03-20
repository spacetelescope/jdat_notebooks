#!/usr/bin/env python3

import os
import logging
import json
import shutil
import sys
import typing

from nbpages import make_html_index

ARTIFACT_HTML_DIR: str = '/tmp/artifacts-html'
INDEX_TEMPLATE: str = os.path.join(os.getcwd(), 'index.tpl')
INDEX_PATH: str = f'{ARTIFACT_HTML_DIR}/index.html'
PAGE_HOME: str = 'pages'

if not os.path.exists(INDEX_TEMPLATE):
    sys.stderr.write(f'Unable to find Index Template[{INDEX_TEMPLATE}]')
    sys.exit(1)

def find_converted_pages():
    for root, dirnames, filenames in os.walk(ARTIFACT_HTML_DIR):
        for filename in filenames:
            if filename.endswith('.html'):
                filename_without_ext: str = filename.split('.', 1)[0]
                metadata_filepath: str = f'{root}/{filename_without_ext}.metadata.json'
                with open(metadata_filepath, 'r') as stream:
                    filepath_metadata: typing.Dict[str, typing.Any] = json.loads(stream.read())

                yield filepath_metadata['title'], f'{root}/{filename}'

if os.path.exists(INDEX_PATH):
    os.remove(INDEX_PATH)

converted_pages = [page for page in find_converted_pages()]
if len(converted_pages) == 0:
    sys.exit(0)

if not os.path.exists(PAGE_HOME):
    os.makedirs(PAGE_HOME)

relative_pages: typing.List[str] = []
for page_title, converted_page in converted_pages:
    filename: str = os.path.basename(converted_page)
    groups: str = '/'.join([group for group in converted_page.split(ARTIFACT_HTML_DIR)[1].split('/')[:-1] if group])
    group_dir_path: str = f'{PAGE_HOME}/{groups}'
    if not os.path.exists(group_dir_path):
        os.makedirs(group_dir_path)

    filepath: str = f'{group_dir_path}/{filename}'
    shutil.copyfile(converted_page, filepath)
    relative_pages.append({
        'output_file_path': filepath,
        'name': page_title,
        'title': page_title
    })

with open(INDEX_PATH, 'w') as stream:
    stream.write(make_html_index(relative_pages, INDEX_TEMPLATE, outfn=None, relpaths=True))

sys.exit(0)
