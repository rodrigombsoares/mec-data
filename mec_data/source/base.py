from abc import ABC, abstractmethod
from mec_data.utils.download_manager import download as download_file


class BaseSource(ABC):
    def _run_download(self, url, path):
        download_file(url, path, 10)

    @abstractmethod
    def download(self, year):
        """Download files"""

    @abstractmethod
    def get_file_name(self, year):
        """Get file name for each class"""
