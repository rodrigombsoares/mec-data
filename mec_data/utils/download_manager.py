import os
import json
import shutil
import urllib.request
from urllib.error import HTTPError
import logging


def create_if_not_exists(temp_folder):
    try:
        os.makedirs(temp_folder)
    except FileExistsError:
        pass


def request_chunks(url, path, pos):
    headers = {"Range": f"bytes={pos}-"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response, open(path, "ab") as out_file:
        shutil.copyfileobj(response, out_file)


def download(url, path, max_retry=0, pos=0, tries=0):
    """
    This is the main function for download manager module. It was created because
    some sources from "dados abertos" closes connection before the file download
    is complete.
    """
    try:
        if tries <= max_retry:
            request_chunks(url, path, pos)
    except HTTPError as e:
        if e.code == 404:
            raise e
        logging.warning(e)
        size_downloaded = os.path.getsize(path)
        download(url, path, max_retry, size_downloaded, tries + 1)
    except Exception as e:
        logging.warning(e)
        size_downloaded = os.path.getsize(path)
        download(url, path, max_retry, size_downloaded, tries + 1)
