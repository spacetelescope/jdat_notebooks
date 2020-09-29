#!/usr/bin/env python

import argparse
import json
import typing

def capture_options() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-i' ,'--input', type=str, required=True)
    parser.add_argument('-o', '--output', type=str, required=True)
    return parser.parse_args()

def extract_metadata(options: argparse.Namespace) -> typing.Dict[str, typing.Any]:
    metadata: typing.Dict[str, str] = {
        'title': None,
        'description': None
    }
    with open(options.input, 'r') as stream:
        notebook: typing.Dict[str, typing.Any] = json.loads(stream.read())
        for idx, cell in enumerate(notebook['cells']):
            if idx == 0:
                if not cell['cell_type'] in ['markdown']:
                    raise NotImplementedError('First cell must be a Markdown Cell')

                for line_item in cell['source']:
                    if line_item.strip().startswith('#'):
                        metadata['title'] = line_item.strip('# \n')
                        break

                continue

            if idx == 1 and cell['cell_type'] in ['markdown']:
                metadata['description'] = ''.join(cell['source'])

    with open(options.output, 'w') as stream:
        stream.write(json.dumps(metadata, indent=2))

if __name__ in ['__main__']:
    options = capture_options()
    extract_metadata(options)

