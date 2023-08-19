import sys
from pathlib import Path


images_files = list()
video_files = list()
documents_files = list()
audio_files = list()
archives_files = list()
folders = list()
others = list()
unknown = list()
extensions = set()

registered_extensions = {
    "JPEG": images_files, "PNG": images_files, "JPG": images_files, "SVG": images_files,

    "AVI": video_files, "MP4": video_files, "MOV": video_files, "MKV": video_files,

    "DOC": documents_files, "DOCX": documents_files, "TXT": documents_files, "PDF": documents_files,
    "XLSX": documents_files, "PPTX": documents_files,

    "MP3": audio_files, "OGG": audio_files, "WAV": audio_files, "AMR": audio_files,

    "GZ": archives_files, "TAR": archives_files, "ZIP": archives_files,
    '': unknown

}

def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()

def scan(folder):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in("Images", "Documents", "Audio", "Video", "Archives", "Others", "Unknown"):
                folders.append(item)
                scan(item)
            continue

        extension = get_extensions(file_name=item.name)
        new_name = folder/item.name                                     #Link to item.name in folder what we give
        try:
            container = registered_extensions[extension]            #container = one item of dir
            extensions.add(extension)
            container.append(new_name)                              #where? and what?
        except KeyError:
            others.append(new_name)
            extensions.add(extension)

if __name__ == '__main__':
    path = sys.argv[1]
    print(f'Start in {path}')

    arg = Path(path)
    scan(arg)

    print(f"Images: {images_files}\n")
    print(f"Video: {video_files}\n")
    print(f"Documents: {documents_files}\n")
    print(f"Audio: {audio_files}\n")
    print(f"Archive: {archives_files}\n")
    print(f"Folders: {folders}\n")
    print(f"Others: {others}\n")
    print(f"Unknown extensions: {unknown}\n")
    print(f"All extensions: {extensions}\n")