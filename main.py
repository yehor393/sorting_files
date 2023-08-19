import shutil
import sys

import scan
import normalize
from pathlib import Path
def handle_file(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    new_path = target_folder / (normalize.normalize(path.name) + path.suffix)
    path.replace(new_path)
def handle_archive(path, root_folder):

    new_name = normalize.normalize(path.with_suffix('').name)

    archive_folder = root_folder / new_name
    archive_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(str(path.resolve()), str(archive_folder))
    except shutil.ReadError:
        archive_folder.rmdir()
    except FileNotFoundError:
        archive_folder.rmdir()
    except OSError:
        pass

    path.unlink()

def remove_empty_folders(path):
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass
def get_folder_object(root_path):
    for folder in root_path.iterdir():
        if folder.is_dir():
            remove_empty_folders(folder)
            try:
                folder.rmdir()
            except OSError:
                pass

def main(folder_path):
    scan.scan(folder_path)

    for file in scan.images_files:
        file = Path(file)
        handle_file(file, folder_path, "Images")

    for file in scan.documents_files:
        file = Path(file)
        handle_file(file, folder_path, "Documents")

    for file in scan.audio_files:
        file = Path(file)
        handle_file(file, folder_path, "Audio")

    for file in scan.video_files:
        file = Path(file)
        handle_file(file, folder_path, "Video")

    for file in scan.others:
        file = Path(file)
        handle_file(file, folder_path, "Others")

    for file in scan.unknown:
        file = Path(file)
        handle_file(file, folder_path, "Unknown")

    for file in scan.archives_files:
        file = Path(file)
        handle_archive(file, folder_path)

        get_folder_object(folder_path)

if __name__ == '__main__':
    path = sys.argv[1]
    print(f'Start in {path}')

    arg = Path(path)
    main(arg.resolve())
