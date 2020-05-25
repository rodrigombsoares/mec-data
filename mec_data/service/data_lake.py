import os
from mec_data.source.factory import get_source
from mec_data.utils.files import unzip_file
from mec_data.data_lake import get_dl_client


def store(source_name, year):
    # Get source
    source = get_source(source_name)
    # Get datalake client
    dl_client = get_dl_client()

    # Create paths
    file_name = source.get_file_name(year)
    file_path = os.path.join(source.path, file_name)
    folder_name = file_name.split(".")[0]
    folder = os.path.join(source.path, folder_name)
    # Unzip and store files
    unziped_files = unzip_file(folder, file_path, source.match)
    for unziped in unziped_files:
        dl_client.store(source.bucket, folder_name, unziped)
    return True
