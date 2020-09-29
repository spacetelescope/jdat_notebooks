#!/usr/bin/env python

import argparse
import enum
import logging
import os
import json
import shutil
import typing

from builder.constants import ARTIFACT_DEST_DIR, ENCODING, BUILD_LOG_DIR, CIRCLE_CI_CONFIG_PATH
from builder.github import scan_pull_requests_for_failures
from builder.service import find_build_jobs, run_build, setup_build, find_excluded_notebooks, is_excluded
from builder.notebook_sync import move_notebook

from nbpages import make_html_index

logger = logging.getLogger(__file__)
class Operation(enum.Enum):
    BuildNotebooks = 'build-notebooks'
    BuildWebsite = 'build-website'
    MultiBuild = 'multi-build'
    SyncNotebooks = 'sync-notebooks'
    ScanGithub = 'scan-github'
    MapNotebooks = 'map-notebooks'
    MergeArtifacts = 'merge-artifacts'

def obtain_options() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--operation', type=Operation, default=Operation.BuildNotebooks)
    # Build Notebooks
    parser.add_argument('-c', '--notebook-collection-paths', type=str, default='')
    parser.add_argument('-n', '--notebook-category', type=str, default=None)
    parser.add_argument('-r', '--remote-names', type=str, default='master')
    # Build Website

    # Sync Notebooks
    parser.add_argument('-d', '--destination-path', type=str, default=None)

    # Map Notebooks

    options = parser.parse_args()
    options.notebook_collection_paths = [nb_path for nb_path in options.notebook_collection_paths.split(',')]
    return options

def validate(options: argparse.Namespace) -> None:
    operation_members = [member.value for member in Operation.__members__.values()]
    if not options.operation.value in operation_members:
        raise NotImplementedError(f'Operation[{options.operation.value}] does not exist. Available Operations: {",".join(operation_members)}')

def main(options: argparse.Namespace) -> None:
    if options.operation is Operation.ScanGithub:
        if options.remote_names == '':
            raise NotImplementedError

        options.remote_names == [name for name in options.remote_names.split(',')]
        for failure in scan_pull_requests_for_failures(options.remote_names):
            print(failure)

    elif options.operation is Operation.SyncNotebooks:
        if options.destination_path is None:
            raise NotImplementedError('Missing --destination-path input')

        formatted_collection_paths = ','.join(options.notebook_collection_paths)
        logger.info(f'Syncing Notebooks Collections to[{formatted_collection_paths}] to Destination[{options.destination_path}]')
        for build_job in filter(is_excluded, find_build_jobs(options.notebook_collection_paths)):
            logger.info(f'Syncing Notebook: {build_job.category.name}')
            move_notebook(build_job, options.destination_path)

    elif options.operation is Operation.BuildNotebooks:
        if options.notebook_collection_paths == '':
            raise NotImplementedError

        if options.notebook_category is None:
            for build_job in filter(is_excluded, find_build_jobs(options.notebook_collection_paths)):
                logger.info(f'Building Notebook: {build_job.collection.name}: {build_job.category.name}')
                setup_build(build_job)
                run_build(build_job)
        else:
            for build_job in find_build_jobs(options.notebook_collection_paths):
                if options.notebook_category != build_job.category.name:
                    continue

                logger.info(f'Building Notebook: {build_job.collection.name}: {build_job.category.name}')
                setup_build(build_job)
                run_build(build_job)

    elif options.operation is Operation.MultiBuild:
        import multiprocessing, time

        if os.path.exists(BUILD_LOG_DIR):
            shutil.rmtree(BUILD_LOG_DIR)

        os.makedirs(BUILD_LOG_DIR)
        def _build_category(collection_name: str, category_name: str) -> None:
            os.environ['CHANNEL_BUILD'] = 'true'
            for build_job in filter(is_excluded, find_build_jobs(options.notebook_collection_paths, False)):
                if category_name != build_job.category.name:
                    continue

                setup_build(build_job)
                run_build(build_job)
            del os.environ['CHANNEL_BUILD']

        job_list = []
        for build_job in filter(is_excluded, find_build_jobs(options.notebook_collection_paths)):
            job_list.append([build_job.collection.name, build_job.category.name])

        processes = []
        max_workers = 10
        while len(job_list) > 0 or len(processes) > 0:
            for proc_idx, proc in enumerate([proc for proc in processes if not proc.is_alive()]):
                processes.remove(proc)

            if len(processes) >= max_workers:
                time.sleep(1)
                continue

            try:
                collection_name, category_name = job_list.pop(0)
            except IndexError:
                continue

            logger.info(f'Starting new Build[{collection_name}, {category_name}]')
            proc = multiprocessing.Process(target=_build_category, args=(collection_name, category_name))
            proc.daemon = True
            proc.start()
            processes.append(proc)

    elif options.operation is Operation.BuildWebsite:
        artifact_dest_dir = 'pages'
        if os.path.exists(artifact_dest_dir):
            shutil.rmtree(artifact_dest_dir)

        os.makedirs(artifact_dest_dir)

        # if options.notebook_category is None:
        converted_pages = []
        for job in filter(is_excluded, find_build_jobs(options.notebook_collection_paths, False)):
            if options.notebook_category and options.notebook_category != job.category.name:
                continue

            for notebook in job.category.notebooks:
                filename = notebook.filename.rsplit('.', 1)[0]
                html_filename = f'{filename}.html'
                html_filepath = os.path.join(ARTIFACT_DEST_DIR, job.collection.name, job.category.name, html_filename)
                meta_filename = f'{filename}.metadata.json'
                meta_filepath = os.path.join(ARTIFACT_DEST_DIR, job.collection.name, job.category.name, meta_filename)
                with open(meta_filepath, 'rb') as stream:
                    metadata = json.loads(stream.read())

                group_dirpath = f'{artifact_dest_dir}/{job.collection.name}/{job.category.name}'
                if not os.path.exists(group_dirpath):
                    os.makedirs(group_dirpath)

                rel_filepath = f'{group_dirpath}/{filename}.html'
                shutil.copyfile(html_filepath, rel_filepath)
                html_rel_filepath = f'{job.collection.name}/{job.category.name}/{filename}.html'
                rel_filepath_meta = f'{group_dirpath}/{filename}.metadata.json'
                shutil.copyfile(meta_filepath, rel_filepath_meta)
                meta_rel_filepath = f'{job.collection.name}/{job.category.name}/{filename}.metadata.json'
                converted_pages.append({
                    'output_file_path': html_rel_filepath,
                    'name': metadata['title'],
                    'title': metadata['title'],
                })

        if len(converted_pages) > 0:
            index_path = f'{artifact_dest_dir}/index.html'
            index_template_path = os.path.join(os.getcwd(), 'index.tpl')
            output = make_html_index(converted_pages, index_template_path, outfn=None, relpaths=True)
            with open(index_path, 'wb') as stream:
                stream.write(output.encode(ENCODING))

    elif options.operation is Operation.MapNotebooks:
        if options.notebook_collection_paths == '':
            raise NotImplementedError

        import copy
        import yaml
        config = {
            'version': 2.1,
            'executors': {
                'notebook-executor': {
                    'docker': [
                        {'image': 'continuumio/miniconda3'}
                    ],
                    'resource_class': 'medium',
                    'working_directory': '~/repo'
                }
            },
            'jobs': {},
            'workflows': {
                'version': '2.1',
                'Branch Build': {
                    'jobs': []
                },
                # 'Deploy Website': {
                #     'jobs': []
                # },
                # 'PR Build': {
                #     'jobs': []
                # }
            }

        }
        job_template = {
            'executor': 'notebook-executor',
            'environment': {
                'PYTHONPATH': '.circleci',
            },
            'steps': [
                'checkout',
                {
                    'run': {
                        'name': 'Setup Environment',
                        'command': 'bash ./.circleci/setup_env.sh'
                    },
                },
                {
                    'run': {
                        'name': 'Build Notebook',
                        'no_output_timeout': '60m',
                        'command': None,
                    }
                },
                {
                    'run': {
                        'name': 'Build Website',
                        'command': None,
                    }
                },
                {
                    'store_artifacts': {
                        'path': './pages'
                    }
                },
            ]
        }
        deploy_website_job = {
            'executor': 'notebook-executor',
            'environment': {
                'PYTHONPATH': '.circleci',
            },
            'steps': [
                'checkout',
                {
                    'run': {
                        'name': 'Collect Artifacts',
                        'command': 'python ./.circleci/builder/factory.py -o merge-artifacts -c jdat_notebooks',
                    }
                }
            ]
        }
        for build_job in filter(is_excluded, find_build_jobs(options.notebook_collection_paths)):
            formatted_cat_name = ' '.join(build_job.category.name.split('_'))
            formatted_cat_name = formatted_cat_name.title()
            formatted_col_name = ' '.join(build_job.collection.name.split('_'))
            formatted_col_name = formatted_col_name.title()

            job_name = '-'.join([formatted_col_name, formatted_cat_name])
            job = copy.deepcopy(job_template)
            job['steps'][2]['run']['command'] = f'python ./.circleci/builder/factory.py -o build-notebooks -c {build_job.collection.name} -n {build_job.category.name}'
            job['steps'][3]['run']['command'] = f'python ./.circleci/builder/factory.py -o build-website -c {build_job.collection.name} -n {build_job.category.name}'
            config['jobs'][job_name] = job
            config['workflows']['Branch Build']['jobs'].append(job_name)

        # depend_job_names = [k for k in config['jobs'].keys()]
        # deploy_job_name = 'Deploy JDAT Notebooks'
        # deploy_job = copy.deepcopy(deploy_website_job)
        # config['jobs'][deploy_job_name] = deploy_job
        # config['workflows']['Branch Build']['jobs'].append({deploy_job_name: {'requires': depend_job_names}})

        with open(CIRCLE_CI_CONFIG_PATH, 'wb') as stream:
            stream.write(yaml.dump(config).encode('utf-8'))

    elif options.operation is Operation.MergeArtifacts:
        if options.notebook_collection_paths == '':
            raise NotImplementedError

        import requests
        artifact_dest_dir = './pages'
        if os.path.exists(artifact_dest_dir):
            shutil.rmtree(artifact_dest_dir)

        os.makedirs(artifact_dest_dir)
        token = 'e0b5094a0f0d94b084d105f9cbbc452515f20223'
        base_url = 'https://circleci.com/api/v1.1'
        recent_builds = f'{base_url}/recent-builds'
        class CircleAuth(requests.auth.AuthBase):
            def __call__(self, request):
                request.headers['Circle-Token'] = token
                return request

        workspace_id = None
        ci_jobs = []
        artifact_urls = []
        for idx, recent_job in enumerate(requests.get(recent_builds, auth=CircleAuth()).json()):
            if idx == 0:
                workspace_id = recent_job['workflows']['workspace_id']
                ci_jobs.append(recent_job)
                continue

            if workspace_id == recent_job['workflows']['workspace_id']:
                ci_jobs.append(recent_job)

        for ci_job in ci_jobs:
            url = f'{base_url}/project/{ci_job["vcs_type"]}/{ci_job["username"]}/{ci_job["reponame"]}/{ci_job["build_num"]}/artifacts'
            resp = requests.get(url, auth=CircleAuth())
            artifact_urls.extend([a['url'] for a in resp.json() if not a['url'].endswith('index.html')])

        class NotebookSource(typing.NamedTuple):
            filename: str
            filepath: str
            category: str
            collection: str
            url: str
            meta_file: bool

        notebook_sources: typing.List[NotebookSource] = []
        for url in artifact_urls:
            filename = os.path.basename(url)
            filepath = os.path.join(artifact_dest_dir, filename)
            file_category = os.path.dirname(url).rsplit('/', 1)[-1]
            file_collection = os.path.dirname(url).rsplit('/', 2)[-2]
            meta_file = filename.endswith('metadata.json')
            resp = requests.get(url, auth=CircleAuth(), stream=True)
            logger.info(f'Storing File[{filepath}]')
            with open(filepath, 'wb') as stream:
                for content in resp.iter_content(chunk_size=1024):
                    stream.write(content)

            notebook_sources.append(NotebookSource(filename, filepath, file_category, file_collection, url, meta_file))

        # Find local-files
        existing_categories = [item for item in set(['.'.join([nb.collection, nb.category]) for nb in notebook_sources])]
        for job in filter(is_excluded, find_build_jobs(options.notebook_collection_paths, False)):
            namespace = '.'.join([job.collection.name, job.category.name])
            if namespace in existing_categories:
                continue

            import pdb; pdb.set_trace()
            import sys; sys.exit(1)

        collections = {}
        for notebook in notebook_sources:
            coll = collections.get(notebook.collection, [])
            collections[notebook.collection] = coll
            coll.append(notebook)

        collection_categories = {}
        for coll_name, coll_source in collections.items():
            coll = collection_categories.get(coll_name, {})
            for notebook in coll_source:
                cat = coll.get(notebook.category, [])
                coll[notebook.category] = cat
                cat.append(notebook)

            collection_categories[coll_name] = coll

        class ArtifactNotebook(typing.NamedTuple):
            title: str
            metadata: typing.Dict[str, typing.Any]
            filepath: str
            filename: str

        class ArtifactCategory(typing.NamedTuple):
            name: str
            notebooks: typing.List[ArtifactNotebook]

        class ArtifactCollection(typing.NamedTuple):
            name: str
            categories: typing.List[ArtifactCategory]


        artifact_collections = []
        for coll_name, coll_source in collection_categories.items():
            cats = []
            for cat_name, cat_source in coll_source.items():
                nbs = []
                for idx, notebook in enumerate(cat_source[::2]):
                    cat_source_idx = idx * 2 + 1
                    with open(cat_source[cat_source_idx].filepath, 'rb') as stream:
                        metadata = json.loads(stream.read().decode(ENCODING))

                    metadata['title'] = metadata['title'].replace('%20', ' ')
                    nbs.append(ArtifactNotebook(metadata['title'], metadata, notebook.filepath, notebook.filename))
                cats.append(ArtifactCategory(cat_name, sorted(nbs)))

            artifact_collections.append(ArtifactCollection(coll_name, sorted(cats)))

        # Render Website
        import jinja2
        import toml
        # import os

        from datetime import datetime

        from jinja2.environment import Template, Environment


        ASSETS_DIR = os.path.join(os.getcwd(), '.circleci/builder-assets')
        TEMPLATE_DIR = os.path.join(os.getcwd(), '.circleci/builder-template')
        ENVIRONMENT_PATH = os.path.join(f'{TEMPLATE_DIR}/environment.toml')
        SITE_DIR = os.path.join(os.getcwd(), 'site')
        if os.path.exists(SITE_DIR):
            shutil.rmtree(SITE_DIR)

        os.makedirs(SITE_DIR)
        def _add_jinja2_filters(environment: Environment) -> None:
            def _render_human_datetime(datetime: datetime) -> str:
                return datetime.strftime('%A, %d. %B %Y %I:%M%p')

            def _render_machine_datetime(datetime: datetime) -> str:
                return datetime.strftime('%Y-%m-%d')

            def _render_machine_datetime_with_time(datetime: datetime) -> str:
                return datetime.strftime('%Y-%m-%dT%H-%M-%S')

            environment.filters['human_date'] = _render_human_datetime
            environment.filters['machine_date'] = _render_machine_datetime
            environment.filters['machine_date_with_time'] = _render_machine_datetime_with_time

        def load_environment() -> typing.Dict[str, typing.Any]:
            environment = {}
            with open(ENVIRONMENT_PATH, 'r') as stream:
                environment = toml.loads(stream.read())

            environment['today'] = datetime.utcnow()
            return environment

        jinja2_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR), undefined=jinja2.StrictUndefined)
        _add_jinja2_filters(jinja2_environment)
        index: Template = jinja2_environment.get_template('index.html')
        environment = load_environment()
        template_context = {
            'page': {
                'title': environment['index_title'],
                'keywords': environment['keywords'],
                'description': environment['description'],
                'locale': environment['default_locale'],
                'author': environment['author'],
                'maintainer': environment['maintainer'],
                'url': f'{environment["website_base_url"]}/index.html',
            },
            'static_url': 'static/',
            'collections': artifact_collections,
        }
        index_filepath = os.path.join(SITE_DIR, 'index.html')
        with open(index_filepath, 'wb') as stream:
            stream.write(index.render(**template_context).encode(ENCODING))

        for coll in artifact_collections:
            for cat in coll.categories:
                for notebook in cat.notebooks:
                    dest_filepath = os.path.join(SITE_DIR, coll.name, cat.name, notebook.filename)
                    dest_dirpath = os.path.dirname(dest_filepath)
                    if not os.path.exists(dest_dirpath):
                        os.makedirs(dest_dirpath)

                    shutil.copyfile(notebook.filepath, dest_filepath)

    else:
        raise NotImplementedError

if __name__ == '__main__':
    options = obtain_options()
    validate(options)
    main(options)
