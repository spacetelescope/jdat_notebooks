import os
import shutil
import typing

CIRCLE_CI_CONFIG_PATH = os.path.join(os.getcwd(), '.circleci/config.yml')
BUILD_LOG_DIR = '/tmp/nbcollection-ci-build-logs'
BUILD_BASE_DIR = '/tmp/nbcollection-ci-build-base-dir'
ARTIFACT_DEST_DIR: str = '/tmp/artifacts'
PWN = typing.TypeVar('PWN')
IPYDB_REQUIRED_FILES: typing.List[str] = ['requirements.txt']
REQUIREMENTS_FILE_NAMES = ['requirements.txt', 'requirements']
ENCODING: str = 'utf-8'
FILTER_STRIP = '/'
