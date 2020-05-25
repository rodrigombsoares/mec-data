import os
from mec_data.source.base import BaseSource
from mec_data.utils.download_manager import create_if_not_exists


class UniversitySource(BaseSource):
    # There are different URL formats for the same source depending on the year
    def __init__(self):
        self.urls = [
            "http://download.inep.gov.br/microdados/microdados_educacao_superior_<YEAR>.zip",
            "http://download.inep.gov.br/microdados/microdados_censo_superior_<YEAR>.zip",
        ]
        self.path = os.path.join(os.getcwd(), self.temp_folder, "university")
        self.match = "dm_aluno.csv"
        self.bucket = "university"

    def download(self, year):
        # Create tempfolder
        create_if_not_exists(self.path)
        # Define filepath
        file_path = os.path.join(self.path, f"university_{year}.zip")
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

    def get_file_name(self, year):
        return f"university_{year}.zip"
