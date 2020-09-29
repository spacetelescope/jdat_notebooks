import glob
import logging
import os
import shutil
import types
import typing

from builder.constants import BUILD_BASE_DIR, ARTIFACT_DEST_DIR, ENCODING
from builder.utils import filter_gitignore_entry__as_string, Collection, BuildJob, Category, Notebook, load_gitignore_data, run_command

logger = logging.getLogger(__name__)

def build_categories(start_path: str, rebuild: bool = True) -> types.GeneratorType:
    gitignore_data = load_gitignore_data(os.path.join(start_path, '.gitignore'))
    for root, dirnames, filenames in os.walk(start_path):
        for dirname in dirnames:
            dirpath = os.path.join(root, dirname)
            if filter_gitignore_entry__as_string(dirname, gitignore_data, dirpath):
                # Reassigning dirnames[:] removes the dir from being scaned
                dirnames[:] = [dname for dname in dirnames if dname == dirname]
                continue

            books = []
            for filepath in glob.glob(f'{dirpath}/*.ipynb'):
                name = os.path.basename(filepath).rsplit('.', 1)[0]
                rel_filepath = os.path.relpath(filepath)
                filename = os.path.basename(filepath)

                books.append([name, filename, rel_filepath])

            notebooks = []
            for idx, (name, filename, rel_filepath) in enumerate(sorted(books, key=lambda x: x[1])):
                notebooks.append(Notebook(name, filename, rel_filepath, idx))

            if notebooks:
                requirements_path = os.path.relpath(os.path.join(dirpath, 'requirements.txt'))
                if not os.path.exists(requirements_path):
                    raise NotImplementedError(f'Category missing Requirements File[{requirements_path}]')

                build_dir = os.path.join(BUILD_BASE_DIR, dirname)
                if os.path.exists(build_dir) and rebuild:
                    shutil.rmtree(build_dir)

                artifact_dir = os.path.join(ARTIFACT_DEST_DIR, dirname)
                if os.path.exists(artifact_dir) and rebuild:
                    shutil.rmtree(artifact_dir)

                yield Category(dirname, notebooks, dirpath, build_dir, artifact_dir)

            else:
                for category in build_categories(dirpath, rebuild):
                    yield category

def find_collections(notebook_collection_paths: typing.List[str], rebuild: bool = True) -> types.GeneratorType:
    for name in notebook_collection_paths:
        c_path = os.path.join(os.getcwd(), name)
        yield Collection(name, [cate for cate in build_categories(c_path, rebuild)])

def find_build_jobs(notebook_collection_paths: typing.List[str], rebuild: bool = True):
    for collection in find_collections(notebook_collection_paths, rebuild):
        for category in collection.categories:
            # if any([True for ex_notebook in find_excluded_notebooks() if ex_notebook.collection == collection.name and ex_notebook.category == category.name]):
            #     import pdb; pdb.set_trace()
            #     continue

            build_scripts = []
            for notebook in category.notebooks:
                build_scripts.append(os.path.join(category.build_dir, f'{notebook.filename}-builder.sh'))

            yield BuildJob(collection, category, build_scripts)

EXCLUDED_NOTEBOOKS = None
class ExcludedNotebook(typing.NamedTuple):
    collection: str
    category: str

def is_excluded(job: BuildJob) -> bool:
    return not any([True for ex_notebook in find_excluded_notebooks() if ex_notebook.collection == job.collection.name and ex_notebook.category == job.category.name])

def find_excluded_notebooks() -> typing.List[ExcludedNotebook]:
    entries = []
    global EXCLUDED_NOTEBOOKS
    if EXCLUDED_NOTEBOOKS is None:
        filepath = os.path.join(os.getcwd(), 'excluded_notebooks')
        if not os.path.exists(filepath):
            return []

        with open(filepath, 'rb') as stream:
            entries = [entry for entry in stream.read().decode(ENCODING).split('\n') if entry]

    if EXCLUDED_NOTEBOOKS:
        return EXCLUDED_NOTEBOOKS

    EXCLUDED_NOTEBOOKS = []
    for entry in entries:
        collection, category = entry.split(':')
        EXCLUDED_NOTEBOOKS.append(ExcludedNotebook(collection, category))

    return EXCLUDED_NOTEBOOKS 

def setup_build(job: BuildJob) -> None:
    job.category.setup_build_env()
    job.category.inject_extra_files()
    for notebook in job.category.notebooks:
        notebook.create_build_script([job.collection.name, job.category.name], job.category.build_dir, job.category.artifact_dir)

def run_build(job: BuildJob) -> None:
    for script in job.scripts:
        command = f'bash "{script}"'
        log_name = f'{job.collection.name}-{job.category.name}'
        run_command(command, log_name)
