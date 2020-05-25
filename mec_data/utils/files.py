import os
import zipfile
import fnmatch


def unzip_file(temp_folder, file_path, match):
    with zipfile.ZipFile(file_path) as archive_object:
        archive_object.extractall(temp_folder)
    matches = []
    for root, subdirs, files in os.walk(temp_folder):
        for file in files:
            if fnmatch.fnmatch(file.lower(), match.lower()):
                matches.append(os.path.join(root, file))

    return matches
