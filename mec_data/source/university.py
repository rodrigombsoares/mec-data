import os
import csv
from mec_data import dal
from flask import current_app
from mec_data.model.university import UniversityStudent
from mec_data.source.base import BaseSource
from urllib.error import HTTPError
from mec_data.utils.download_manager import create_if_not_exists


class UniversitySource(BaseSource):
    # There are different URL formats for the same source depending on the year
    def __init__(self):
        self.urls = [
            "http://download.inep.gov.br/microdados/microdados_educacao_superior_<YEAR>.zip",
            "http://download.inep.gov.br/microdados/microdados_censo_superior_<YEAR>.zip",
        ]
        self.temp_folder = current_app.config.get("MEC_DATA_STORAGE_TEMP_FOLDER")
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

    def load_to_dw(self, csv_path):
        indexes = {
            "NU_ANO_CENSO": None,
            "NU_ANO_NASCIMENTO": None,
            "NU_MES_NASCIMENTO": None,
            "NU_DIA_NASCIMENTO": None,
            "TP_COR_RACA": None,
            "TP_SEXO": None,
            "TP_NACIONALIDADE": None,
            "CO_UF_NASCIMENTO": None,
            "CO_MUNICIPIO_NASCIMENTO": None,
            "TP_DEFICIENCIA": None,
            "IN_DEFICIENCIA": None,
            "IN_INGRESSO_VAGA_NOVA": None,
            "NU_ANO_INGRESSO": None,
        }
        with open(csv_path, mode="r") as csv_file:
            readCSV = csv.reader(csv_file, delimiter="|")
            header = next(readCSV)
            # Set column number for each index we need
            for index, val in enumerate(header):
                if val in indexes:
                    indexes[val] = index
            students = []
            for row in readCSV:
                if row[indexes["NU_ANO_INGRESSO"]] != row[indexes["NU_ANO_CENSO"]]:
                    continue
                student = UniversityStudent(
                    year=row[indexes["NU_ANO_CENSO"]],
                    day_birth=row[indexes["NU_DIA_NASCIMENTO"]],
                    month_birth=row[indexes["NU_MES_NASCIMENTO"]],
                    year_birth=row[indexes["NU_ANO_NASCIMENTO"]],
                    sex=row[indexes["TP_SEXO"]],
                    race=row[indexes["TP_COR_RACA"]],
                    nationality=row[indexes["TP_NACIONALIDADE"]],
                    uf_birth=row[indexes["CO_UF_NASCIMENTO"]],
                    city_birth=row[indexes["CO_MUNICIPIO_NASCIMENTO"]],
                    disability=row[indexes["IN_DEFICIENCIA"]]
                    if indexes["IN_DEFICIENCIA"]
                    else row[indexes["TP_DEFICIENCIA"]],
                )
                students.append(student)
                if len(students) > 100000:
                    # Save students in batches
                    print("greater than 100000")
                    dal.university.create_many(students)
                    students = []
            # Save the rest of the students
            dal.university.create_many(students)
