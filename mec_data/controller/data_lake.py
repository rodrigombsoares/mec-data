from flask_restplus import Namespace, Resource
from mec_data import service
from flask import Response


api = Namespace("Data Lake", description="Treat and store downloaded files to datalake")


@api.route("/scholar_census/<year>/")
class StoreScholar(Resource):
    def post(self, year):
        """Unpack and store scholar census files"""
        res = service.data_lake.store("SCHOLAR_CENSUS", year)
        return res


@api.route("/university_census/<year>/")
class StoreUniversity(Resource):
    def post(self, year):
        """Unpack and store university census files"""
        res = service.data_lake.store("UNIVERSITY_CENSUS", year)
        return res
