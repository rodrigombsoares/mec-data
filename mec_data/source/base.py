from abc import ABC, abstractmethod
from flask import current_app
from mec_data.utils.download_manager import download as download_file


class BaseSource:
    temp_folder = current_app.config.get("MEC_DATA_STORAGE_TEMP_FOLDER")

    def _run_download(self, url, path):
        download_file(url, path, 10)

    @abstractmethod
    def download(self, year):
        pass

    @abstractmethod
    def get_file_name(self, year):
        pass
