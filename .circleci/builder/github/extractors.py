import enum
import logging
import os
import requests
import time
import typing
import types

from requests.auth import HTTPBasicAuth
from requests.models import Response

from urllib.parse import urlencode, urlparse

HEADERS = {}
PWN = typing.TypeVar('PWN')
ENCODING = 'utf-8'
DELAY = 0.5
GITHUB_BASE_URL = 'https://api.github.com'
logger = logging.getLogger(__name__)

class PRState(enum.Enum):
    OPEN = 'open'

def validate_response(response: Response, accepted_codes: typing.List[int] = [200]) -> bool:
    if response.status_code in accepted_codes:
        return True

    elif response.status_code == 403:
        logger.error(f'Rate Limited URL: {response.request.url}')
        return False

    if 'Must have push access to view repository collaborators' in response.json()['message']:
        path = urlparse(response.request.url).path
        logger.info(f'Unable to view Repo collaborators: {path}')

    else:
        logger.exception(f'Unabled Github API Error[{response.status_code}: {response.request.url}]: {response.content}')

    return False

def extract_github_data_from_api(
        base_url: str,
        headers: typing.Dict[str, str] = {},
        params: typing.Dict[str, str] = {}) -> None:
    base_headers = HEADERS.copy()
    base_headers.update(headers)
    SYNC_DATA = True
    page = 1
    limit = 100
    request_params: typing.Dict[str, str] = {
        'state': 'all',
        'sort': 'created'
    }
    request_params.update(params)
    while SYNC_DATA:
        request_params['page'] = page
        request_params['limit'] = limit
        url = '?'.join([base_url, urlencode(request_params)])
        logger.info(f'Pulling URL[{url}]')
        response = requests.get(url, headers=headers, auth=github_auth())
        time.sleep(DELAY)
        if validate_response(response) is False:
            SYNC_DATA = False
            break

        dataset = response.json()
        if len(dataset) == 0:
            SYNC_DATA = False
            break

        for entry in dataset:
            yield entry

        page += 1

def github_auth() -> HTTPBasicAuth:
    username = os.environ.get('GITHUB_USERNAME', None)
    password = os.environ.get('GITHUB_PASSWORD', None)
    if username and password:
        return HTTPBasicAuth(username, password)

    return None

def github_commit_status(owner: str, name: str, ref: str) -> types.GeneratorType:
    url = f'{GITHUB_BASE_URL}/repos/{owner}/{name}/commits/{ref}/status'
    response = requests.get(url, headers=HEADERS, auth=github_auth())
    time.sleep(DELAY)
    validate_response(response)
    for status in response.json()['statuses']:
        yield status

def github_pull_requests(owner: str, name: str, state: PRState) -> types.GeneratorType:
    base_url = f'{GITHUB_BASE_URL}/repos/{owner}/{name}/pulls'
    params = urlencode({
        'state': state.value,
        'sort': 'created',
        # 'direction': 'desc',
    })
    url = '?'.join([base_url, params])
    for entry in extract_github_data_from_api(url, HEADERS):
        yield entry
