import os
import shutil

from builder.utils import BuildJob, extract_files_and_directories_from_folder

def move_notebook(job: BuildJob, destination_path: str) -> None:
    dest_path = os.path.join(destination_path, job.category.name)
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)

    for name, path in extract_files_and_directories_from_folder(job.category.source_dir):
        file_dest_path = os.path.join(dest_path, name)
        if os.path.exists(file_dest_path):
            if os.path.isdir(file_dest_path):
                shutil.rmtree(file_dest_path)

            elif os.path.isfile(file_dest_path):
                os.remove(file_dest_path)

        if os.path.isdir(path):
            shutil.copytree(path, file_dest_path)

        elif os.path.isfile(path):
            shutil.copyfile(path, file_dest_path)
