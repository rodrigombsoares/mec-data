from flask import request
from flask_restplus import Namespace, Resource

# from mec_data.dto.store import StoreDto
from mec_data import dal
from mec_data import service

api = Namespace("DataWarehouse",)


@api.route("/stores/load/<company_id>/<date>/")
class DWResource(Resource):
    def post(self, company_id, date):
        """Load stores to DW."""
        company = dal.company.get(company_id)
        dw_service = service.data_warehouse.DataWarehouseService(company)
        return dw_service.load_stores(date)
