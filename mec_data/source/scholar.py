import os
from mec_data.source.base import BaseSource
from urllib.error import HTTPError
from mec_data.utils.download_manager import create_if_not_exists


class ScholarSource(BaseSource):
    def __init__(self):0
        self.urls = [
            "http://download.inep.gov.br/microdados/microdados_educacao_basica_<YEAR>.zip",
            "http://download.inep.gov.br/microdados/micro_censo_escolar_<YEAR>.zip",
        ]
        self.path = os.path.join(os.getcwd(), self.temp_folder, "scholar")
        self.match = "matricula*.csv"
        self.bucket = "scholar"

    def download(self, year):
        # Create tempfolder
        create_if_not_exists(self.path)
        # Define filepath
        file_path = os.path.join(self.path, f"scholar_{year}.zip")
        # Try to download from any of the two URLs
        for url in self.urls:
            url = url.replace("<YEAR>", year)
            try:
                self._run_download(url, file_path)
                return True, 200
            except HTTPError as e:
                # If error different than 404 return
                # internal server error
                if e.code != 404:
                    return False, 500
                # If not found (404), tries second url
        return False, 500
