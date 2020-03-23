#!/usr/bin/env python

import logging
import json
import os
import subprocess
import shutil
import sys
import tarfile
import tempfile
import time
import types
import typing

from datetime import datetime

from junitparser import TestCase, TestSuite, JUnitXml, Skipped, Error

from select import select

root = logging.getLogger()
root.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
root.addHandler(handler)

logger = logging.getLogger(__file__)

IPYDB_REQUIRED_FILES: typing.List[str] = ['requirements.txt']
ENCODING: str = 'utf-8'
ARTIFACT_DEST_DIR: str = '/tmp/artifacts'
ARTIFACT_HTML_DIR: str = '/tmp/artifacts-html'
TEST_OUTPUT_DIR: str = '/tmp/test-results'
if not os.path.exists(TEST_OUTPUT_DIR):
    os.makedirs(TEST_OUTPUT_DIR)
TEST_CASES: typing.List[TestCase] = []

if os.path.exists(ARTIFACT_HTML_DIR):
    shutil.rmtree(ARTIFACT_HTML_DIR)

os.makedirs(ARTIFACT_HTML_DIR)
class BuildError(Exception):
    pass

def run_command(cmd: typing.Union[str, typing.List[str]]) -> None:
    if isinstance(cmd, str):
        cmd = [cmd]

    buffer_size: int = 1024
    proc = subprocess.Popen(cmd, shell=True)
    while proc.poll() is None:
        time.sleep(.1)

    if proc.poll() > 0:
        raise BuildError(f'Process Exit Code[{proc.poll()}]')

def find_artifacts(start_dir: str) -> types.GeneratorType:
    for root, dirnames, filenames in os.walk(start_dir):
        for filename in filenames:
            if filename.endswith('.tar.gz'):
                yield os.path.join(start_dir, filename)

def main():
    for artifact_path in find_artifacts(ARTIFACT_DEST_DIR):
        logger.info(f'Found Artifact in path[{artifact_path}]. Building Artifact')
        notebook_name: str = os.path.basename(artifact_path).rsplit('.', 1)[0]
        extraction_path: str = tempfile.mkdtemp(prefix=notebook_name)
        build_script_path: str = None
        with tarfile.open(artifact_path, "r:gz") as tar:
            for member in tar.getmembers():
                if member.isdir():
                    dir_path: str = os.path.join(extraction_path, member.path)
                    os.makedirs(dir_path)
    
                elif member.isfile():
                    filepath: str = os.path.join(extraction_path, member.path)
                    with open(filepath, 'wb') as stream:
                        stream.write(tar.extractfile(member).read())
    
                    if os.path.basename(member.path) == 'build.sh':
                        build_script_path = filepath
    
                else:
                    raise NotImplementedError
    
    
        owd: str = os.getcwd()
        build_dir: str = os.path.dirname(build_script_path)
        logger.info(f'Changing to build_dir[{build_dir}]')
        os.chdir(build_dir)
        start = datetime.utcnow()
        logger.info(f'Running Build for Notebook[{notebook_name}]')
        try:
            run_command([f'bash build.sh {ARTIFACT_HTML_DIR}'])
        except BuildError:
            raise BuildError(f'Unable to execute notebook[{notebook_name}]')

        delta = datetime.utcnow() - start
        logger.info(f'Changing back to old working dir[{owd}]')
        os.chdir(owd)
        test_case = TestCase(f'{notebook_name} Test')
    
        TEST_CASES.append(test_case)
    
    test_suite = TestSuite(f'Notebooks Test Suite')
    [test_suite.add_testcase(case) for case in TEST_CASES]
    test_output_path: str = os.path.join(TEST_OUTPUT_DIR, f'results.xml')
    xml = JUnitXml()
    xml.add_testsuite(test_suite)
    xml.write(test_output_path)

if __name__ in ['__main__']:
    main()

