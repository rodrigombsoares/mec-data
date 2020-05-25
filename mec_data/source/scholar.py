import os
import csv
from flask import current_app
from mec_data import dal
from mec_data.source.base import BaseSource
from urllib.error import HTTPError
from mec_data.utils.download_manager import create_if_not_exists
from mec_data.model.scholar import ScholarStudent


class ScholarSource(BaseSource):
    def __init__(self):
        self.urls = [
            "http://download.inep.gov.br/microdados/microdados_educacao_basica_<YEAR>.zip",
            "http://download.inep.gov.br/microdados/micro_censo_escolar_<YEAR>.zip",
        ]
        self.temp_folder = current_app.config.get("MEC_DATA_STORAGE_TEMP_FOLDER")
        self.path = os.path.join(os.getcwd(), self.temp_folder, "scholar")
        self.match = "matricula*.csv"
        self.bucket = "scholar"

    def download(self, year):
        # Create tempfolder
        create_if_not_exists(self.path)
        # Define filepath
        file_path = os.path.join(self.path, f"scholar_,{year}.zip")
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
        return f"scholar_{year}.zip"

    def load_to_dw(self, csv_path):
        indexes = {
            "NU_ANO_CENSO": None,
            "NU_DIA": None,
            "NU_MES": None,
            "NU_ANO": None,
            "NU_IDADE": None,
            "TP_SEXO": None,
            "NU_DURACAO_TURMA": None,
            "NU_DIAS_ATIVIDADE": None,
            "TP_COR_RACA": None,
            "TP_NACIONALIDADE": None,
            "CO_UF_NASC": None,
            "CO_MUNICIPIO_NASC": None,
            "IN_TRANSPORTE_PUBLICO": None,
            "IN_NECESSIDADE_ESPECIAL": None,
            "TP_MEDIACAO_DIDATICO_PEDAGO": None,
            "TP_ETAPA_ENSINO": None,
            "CO_UF": None,
            "TP_DEPENDENCIA": None,
            "TP_LOCALIZACAO": None,
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
                if str(row[indexes["TP_ETAPA_ENSINO"]]) not in [
                    "26",
                    "27",
                    "28",
                    "29",
                    "31",
                    "32",
                    "33",
                    "34",
                ]:
                    continue
                student = ScholarStudent(
                    year=row[indexes["NU_ANO_CENSO"]],
                    day_birth=row[indexes["NU_DIA"]],
                    month_birth=row[indexes["NU_MES"]],
                    year_birth=row[indexes["NU_ANO"]],
                    age=row[indexes["NU_IDADE"]],
                    sex=row[indexes["TP_SEXO"]],
                    race=row[indexes["TP_COR_RACA"]],
                    nationality=row[indexes["TP_NACIONALIDADE"]],
                    uf_birth=row[indexes["CO_UF_NASC"]],
                    city_birth=row[indexes["CO_MUNICIPIO_NASC"]],
                    disability=row[indexes["IN_NECESSIDADE_ESPECIAL"]],
                    public_transp=row[indexes["IN_TRANSPORTE_PUBLICO"]],
                    school_uf=row[indexes["CO_UF"]],
                    school_dependency=row[indexes["TP_DEPENDENCIA"]],
                    school_location=row[indexes["TP_LOCALIZACAO"]],
                    class_type=row[indexes["TP_MEDIACAO_DIDATICO_PEDAGO"]],
                    class_duration=row[indexes["NU_DURACAO_TURMA"]],
                    class_days=row[indexes["NU_DIAS_ATIVIDADE"]],
                )
                students.append(student)
                if len(students) > 100000:
                    # Save students in batches
                    print("greater than 100000")
                    dal.scholar.create_many(students)
                    students = []
            # Save the rest of the students
            dal.scholar.create_many(students)
