from flask_restplus import Namespace, Resource
from mec_data import service
from flask import Response


api = Namespace("Data Source", description="Gather data from sources",)


@api.route("/scholar_census/<year>/")
class DownloadScholar(Resource):
    def post(self, year):
        """Make request to download data from source"""
        res, status = service.data_source.download("SCHOLAR_CENSUS", year)
        return Response(str(res), status=status)


@api.route("/university_census/<year>/")
class DownloadUniversity(Resource):
    def post(self, year):
        """Make request to download data from source"""
        res, status = service.data_source.download("UNIVERSITY_CENSUS", year)
        return Response(str(res), status=status)
