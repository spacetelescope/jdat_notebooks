import enum
import configparser
import logging
import os
import types
import typing

from builder.constants import ENCODING
from builder.github.extractors import github_pull_requests, extract_github_data_from_api, github_commit_status, PRState

from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class TransportProtocol(enum.Enum):
    HTTPS = 'https'
    GIT = 'git'

class RepoParams(typing.NamedTuple):
    owner: str
    name: str
    host: str
    protocol: TransportProtocol

class GitRemote(typing.NamedTuple):
    name: str
    url: str
    fetch: str
    repo: RepoParams

def remote_to_params(remote: str) -> RepoParams:
    if remote.startswith('https'):
        url_parts = urlparse(remote)
        owner, name = [part for part in url_parts.path.split('/', 2) if part]
        try:
            name, extension = name.split('.', 1)
        except ValueError:
            extension = None

        return RepoParams(owner, name, url_parts.netloc, TransportProtocol.HTTPS)

    elif remote.startswith('git@'):
        username, hostpath = remote.split('@', 1)
        host, path = hostpath.split(':', 1)
        owner, name = path.split('/', 1)
        try:
            name, extension = name.split('.', 1)
        except ValueError:
            extension = None

        return RepoParams(owner, name, host, TransportProtocol.GIT)

    else:
        raise NotImplementedError

def load_github_remotes() -> types.GeneratorType:
    git_config_path = os.path.join(os.getcwd(), '.git/config')
    config_data = configparser.ConfigParser()
    with open(git_config_path, 'rb') as stream:
        config_data.read_string(stream.read().decode(ENCODING))

    for key in config_data.keys():
        if key.startswith('remote "'):
            url = config_data[key].get('url', None)
            fetch = config_data[key].get('fetch', None)
            name = key.split('remote "', 1)[1].strip('"')
            yield GitRemote(name, url, fetch, remote_to_params(url))

def scan_pull_requests_for_failures(remote_names: typing.List[str]) -> None:
    for remote in filter(lambda x: x.name in remote_names, load_github_remotes()):
        failed = []
        pending = []
        success = []
        for idx, entry in enumerate(github_pull_requests(remote.repo.owner, remote.repo.name, PRState.OPEN)):
            commit_hashes = []
            for commit_entry in extract_github_data_from_api(entry['commits_url'], params={
                'sort': 'created',
            }):
                commit_hashes.append(commit_entry['sha'])
            for status in github_commit_status(remote.repo.owner, remote.repo.name, commit_hashes[-1]):
                if status['state'] in ['error', 'failure']:
                    failed.append([entry, status])

                elif status['state'] in ['pending']:
                    pending.append([entry, status])

                elif status['state'] in ['success']:
                    success.append([entry, status])

                else:
                    pass

        def _print_pr_details(pr, status):
            number = pr['number']
            html_url = pr['html_url']
            name = pr['title']
            labels = ', '.join([label['name'] for label in pr['labels']])
            target_url = status['target_url']
            logging.info(f'Name: {name}')
            logging.info(f'PR No. {number} - {html_url}')
            logging.info(f'Labels: {labels}')
            logging.info(f'Details: {target_url}')

        logger.info(f'Pull Request Count: {idx + 1} (open)')
        logger.info('Pull Request States')
        if failed:
            logger.info('Failed')
            for pr, status in failed:
                _print_pr_details(pr, status)

        if pending:
            logger.info('Pending')
            for pr, status in pending:
                _print_pr_details(pr, status)

        if success:
            logger.info('Success')
            for pr, status in success:
                _print_pr_details(pr, status)

    return []
