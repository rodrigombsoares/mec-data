from flask import request
from flask_restplus import Namespace, Resource

# from mec_data.dto.store import StoreDto
from mec_data import dal
from mec_data import service

api = Namespace("DataWarehouse", description="Structure and Load data from DL to DW")


@api.route("/scholar_census/<year>/")
class DWScholarResource(Resource):
    def post(self, year):
        """Load scholar census to DW."""
        load = service.data_warehouse.load("SCHOLAR_CENSUS", year)
        return load


@api.route("/university_census/<year>/")
class DWUniversityResource(Resource):
    def post(self, year):
        """Load university census to DW."""
        load = service.data_warehouse.load("UNIVERSITY_CENSUS", year)
        return load
