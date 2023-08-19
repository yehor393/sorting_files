import shutil
import sys

import scan
import normalize
from pathlib import Path


def handle_file(path, root_folder, dist):
    """
    Move and normalize a file to a specific directory.

    :param path: The path to the file.
    :param root_folder: The root folder where the target folder will be created.
    :param dist: The sub-folder where the file will be moved
    :return: None
    """
    # Creates the target folder if it doesn't exist
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)

    # Normalize the file name and combine this with origin extension
    new_path = target_folder / (normalize.normalize(path.name) + path.suffix)

    # Move the file to the new path
    path.replace(new_path)


def handle_archive(path, root_folder):
    """
    Handle the extraction and organization of an archive file.

    This function takes an archive file path and a root folder path as input. It creates a normalized sub-folder name
    using the base name of the archive file (without extension) and attempts to unpack the contents of the archive
    into the newly created sub-folder within the specified root folder. If the unpacking is successful, the original
    archive file is removed. If any errors occur during unpacking or folder creation, the function handles them
    gracefully by removing any newly created sub-folders and ignoring the error.

    :param path: The path to the file.
    :param root_folder: The root folder where the target folder will be created.
    :return: None
    """
    #
    new_name = normalize.normalize(path.with_suffix('').name)

    # Creates the archive folder if it doesn't exist
    archive_folder = root_folder / new_name
    archive_folder.mkdir(exist_ok=True)

    try:
        # Unpack the archive into the sub-folder
        shutil.unpack_archive(str(path.resolve()), str(archive_folder))

        # Handle any potential errors during unpacking or folder operations
        # by removing the sub-folder and ignoring the error
    except shutil.ReadError:
        archive_folder.rmdir()
    except FileNotFoundError:
        archive_folder.rmdir()
    except OSError:
        pass

    # Remove the original archive file
    path.unlink()


def remove_empty_folders(path):
    """
    Recursively remove empty folders within a given path.

    This function traverses the specified path and its subdirectories to identify and remove empty folders. It first
    recursively calls itself to ensure that all subdirectories are processed before their parent directories. If an
    empty folder is encountered, it attempts to remove it using the 'rmdir' method. If the folder is not empty or if
    an error occurs during removal, the function continues to the next iteration.

    :param path: The root path to start the search for empty folders.
    :return: None
    """
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass


def get_folder_object(root_path):
    """
    Recursively remove empty folders and specific folders within a given root path.

    This function traverses the specified root path to identify and remove specific folders that were created during
    the organization process but remain empty or no longer needed. It uses the 'remove_empty_folders' function to
    perform the removal of empty folders. If the folder is not empty or if an error occurs during removal, the
    function continues to the next iteration.

    :param root_path: The root path to start the search for empty folders.
    :return: None
    """
    for folder in root_path.iterdir():
        if folder.is_dir():
            remove_empty_folders(folder)
            try:
                folder.rmdir()
            except OSError:
                pass


def main(folder_path):
    """
    Organize files within a specified folder by categorizing and moving them to appropriate subfolders.

    This function orchestrates the entire organization process. It first uses the 'scan' module to identify different
    types of files and their extensions within the specified folder. Then, it iterates through each categorized list
    of files (images, documents, audio, video, others, unknown, archives).

    :param folder_path: The path to the folder containing the unorganized files.
    :return: None
    """
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
