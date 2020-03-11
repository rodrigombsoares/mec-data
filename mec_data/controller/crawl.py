from flask_restplus import Namespace, Resource
from retail_stores import service
from flask import Response


api = Namespace(
    'Crawl',
    description='Call crawler for registred companies',
)


@api.route('/<company_id>/')
class CrawlResource(Resource):
    def post(self, company_id):
        """Calls crawler for registered companies."""
        res, status = service.company.crawl(company_id)
        return Response(res, status=status)
