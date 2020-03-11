from flask import request
from flask_accepts import accepts, responds
from flask_restplus import Namespace, Resource

from retail_stores.dto.store import StoreDto
from retail_stores import dal
from retail_stores import service

api = Namespace(
    'DataWarehouse',
)


@api.route('/stores/load/<company_id>/<date>/')
class DWResource(Resource):
    def post(self, company_id, date):
        """Load stores to DW."""
        company = dal.company.get(company_id)
        dw_service = service.data_warehouse.DataWarehouseService(company)
        return dw_service.load_stores(date)


#TODO: implement update store
# @api.route('/stores/')
# class DWStoreResource(Resource):
#     @accepts(schema=StoreDto, api=api)
#     def update(self):
#         """Update single store on DW"""
#     return request.parsed_obj
