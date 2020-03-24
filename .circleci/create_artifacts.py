#!/usr/bin/env python

import logging
import glob
import os
import shutil
import sys
import tarfile
import tempfile
import types
import typing

root = logging.getLogger()
root.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
root.addHandler(handler)

logger = logging.getLogger(__file__)

IPYDB_REQUIRED_FILES: typing.List[str] = ['requirements.txt']
ENCODING: str = 'utf-8'
ARTIFACT_DEST_DIR: str = '/tmp/artifacts'
if os.path.exists(ARTIFACT_DEST_DIR):
    shutil.rmtree(ARTIFACT_DEST_DIR)

os.makedirs(ARTIFACT_DEST_DIR)

def find_ipynb_files(start_path: str) -> types.GeneratorType:
    for root, dirnames, filenames in os.walk(start_path):
        is_ipydb_directory: bool = False
        for filename in filenames:
            if filename.endswith('.ipynb'):
                is_ipydb_directory = True
                break

        if is_ipydb_directory:
            has_error: bool = False
            for filename in IPYDB_REQUIRED_FILES:
                if not filename in filenames:
                    logger.error(f'Missing file[{filename}] in dir[{os.path.relpath(root)}]')
                    has_error = True

            if has_error is False:
                yield os.path.abspath(root)

def main():
    for notebook_path in find_ipynb_files(os.getcwd()):
        logger.info(f'Found notebook in path[{os.path.relpath(notebook_path)}]. Building Artifact')
        notebook_name: str = os.path.basename(notebook_path)
        notebook_name_plain: str = notebook_name.rsplit('.', 1)[0]
        build_path = tempfile.mkdtemp(prefix=notebook_name)
        shutil.rmtree(build_path)
        build_script_path = os.path.join(build_path, 'build.sh')
        shutil.copytree(notebook_path, build_path)
        paths: typing.List[str] = glob.glob(f'{build_path}/*.ipynb')
        if len(paths) > 1:
            raise NotImplementedError('Support for building more than one .ipynb file at a time is not yet supported')

        notebook_filepath: str = paths[0]
        notebook_groups: str = os.path.relpath(notebook_path).split('notebooks')[1].strip('/')
        shutil.copyfile('.circleci/extract_metadata_from_notebook.py', f'{build_path}/extract_metadata_from_notebook.py')
        setup_script: str = f"""#!/usr/bin/env bash
set -e

if [ -z "$1" ]; then
    echo "Unable to build; Artifact DIR Required" >&2
    exit 1
fi
cd {build_path}
source activate notebooks_env
virtualenv -p $(which python3) env
conda deactivate
source env/bin/activate
if [ -f "pre-install.sh" ]; then
   bash pre-install.sh
fi
if [ -f "pre_requirements.txt" ]; then
    pip install -r pre_requirements.txt
fi
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi
pip install jupyter
mkdir -p $1/{notebook_groups}

if [ -f "environment.sh" ]; then
    source environment.sh
fi
python extract_metadata_from_notebook.py --input "{notebook_filepath}" --output "$1/{notebook_groups}/{notebook_name_plain}.metadata.json"
jupyter nbconvert --debug --to html --execute "{notebook_filepath}" --output "$1/{notebook_groups}/{notebook_name_plain}.html" --ExecutePreprocessor.timeout=600
cd -
"""
        with open(build_script_path, 'w') as stream:
            stream.write(setup_script)
    
        logger.info(f'Taring Notebook[{notebook_name}]')
        artifact_name: str = f'{notebook_name_plain}.tar.gz'
        artifact_dir_path: str = os.path.dirname(tempfile.NamedTemporaryFile().name)
        artifact_path: str = os.path.join(artifact_dir_path, artifact_name)
        with tarfile.open(artifact_path, "w:gz") as tar:
            tar.add(build_path, arcname=os.path.basename(build_path))
    
        if not os.path.exists(ARTIFACT_DEST_DIR):
            os.makedirs(ARTIFACT_DEST_DIR)
    
        artifact_dest: str = os.path.join(ARTIFACT_DEST_DIR, artifact_name)
        logger.info(f'Moving Notebook[{notebook_name_plain}]')
        shutil.move(artifact_path, artifact_dest)

if __name__ in ['__main__']:
    main()

