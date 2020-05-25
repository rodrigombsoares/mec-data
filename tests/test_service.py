from unittest import TestCase
from unittest.mock import patch

from mec_data.manage.app import create_app
from mec_data import service
from mec_data.model.company import Company

from tests.mocks.mocked_ibge import *


class TestCompanyService(TestCase):

    def setUp(self):
        self.test_app = create_app()

    @patch('mec_data.service.company.dal')
    def test_create_get(self, mocked_dal):
        vivara = {
            'name': 'vivara',
            'department':  'jewelry'
        }
        with self.test_app.app_context():
            create = service.company.create(vivara)
            get_all = service.company.get_all()
        mocked_dal.company.create.assert_called_once
        mocked_dal.company.get_all.assert_called_once
        self.assertEqual(create.name, Company(**vivara).name)
        self.assertEqual(create.department, Company(**vivara).department)

    @patch('mec_data.service.company.ApiRunner')
    def test_api_crawl(self, MockedApiRunner):
        MockedApiRunner.return_value.run.return_value = 'Crawled 5 items'
        with self.test_app.app_context():
            crawled = service.company.crawl(1)
        self.assertEqual(crawled, ('Crawled 5 items', 200))
    
    @patch('mec_data.service.company.ScrapyRunner')
    @patch('mec_data.service.company.ApiRunner')
    def test_scrapy_crawl(self, MockedApiRunner, MockedScrapyRunner):
        MockedApiRunner.return_value.run.side_effect = AttributeError
        MockedScrapyRunner.return_value.run.return_value = 'Crawled 10 items'
        with self.test_app.app_context():
            crawled = service.company.crawl(1)
        self.assertEqual(crawled, ('Crawled 10 items', 200))
    
    @patch('mec_data.service.company.ScrapyRunner')
    @patch('mec_data.service.company.ApiRunner')
    def test_crawl_exception(self, MockedApiRunner, MockedScrapyRunner):
        MockedApiRunner.return_value.run.side_effect = TypeError('Fail')
        with self.test_app.app_context():
            crawled = service.company.crawl(1)
        self.assertEqual(crawled, ('Fail', 500))


class TestIBGEService(TestCase):

    def setUp(self):
        self.test_app = create_app()

    @patch('mec_data.service.ibge_data.dal')
    @patch('mec_data.service.ibge_data.requests')
    def test_load_age_level(self, mocked_requests, mocked_dal):
        mocked_requests.get.return_value.json.return_value = mocked_age_levels
        with self.test_app.app_context():
            load = service.ibge_data.load_age_level('2010')
        self.assertEqual(load, 'Loaded 39 for 3 cities')

    @patch('mec_data.service.ibge_data.dal')
    @patch('mec_data.service.ibge_data.requests')
    def test_load_education_level(self, mocked_requests, mocked_dal):
        mocked_requests.get.return_value.json.return_value = mocked_education_level
        with self.test_app.app_context():
            load = service.ibge_data.load_education_level('2010')
        self.assertEqual(load, 'Loaded 15 for 3 cities')

    @patch('mec_data.service.ibge_data.dal')
    @patch('mec_data.service.ibge_data.requests')
    def test_load_income_range(self, mocked_requests, mocked_dal):
        mocked_requests.get.return_value.json.return_value = mocked_income_range
        with self.test_app.app_context():
            load = service.ibge_data.load_income_range('2010')
        self.assertEqual(load, 'Loaded 24 for 3 cities')

    @patch('mec_data.service.ibge_data.dal')
    @patch('mec_data.service.ibge_data.requests')
    def test_load_cities(self, mocked_requests, mocked_dal):
        mocked_requests.get.return_value.json.return_value = mocked_cities
        with self.test_app.app_context():
            load = service.ibge_data.load_cities()
        self.assertEqual(
            load, 'Loaded 5 cities, 3 states and 1 regions from IBGE')


class TestClusterRegisterService(TestCase):

    def setUp(self):
        self.test_app = create_app()

    def _get_mocked_company(self, company_id):
        company_obj = Company(
                id = company_id,
                name = 'vivara-{}'.format(company_id),
                department = 'jewelry'
        )
        return company_obj

    @patch('mec_data.service.cluster_register.dal')
    def test_cluster_register(self, mocked_dal):
        register_req = {
            'distances': [0],
            'company_ids': [1, 2],
            'label': 'any',
            'department': 'multi'
        }
        mocked_dal.company.get.side_effect = self._get_mocked_company
        with self.test_app.app_context():
            register = service.cluster_register.register(register_req)
            self.assertEqual(register, {'distances': [0], 'label': 'any', 'department': 'multi'})

    @patch('mec_data.service.cluster_register.dal')
    def test_cluster_register_error(self, mocked_dal):
        register_req = {
            'distances': [0],
            'company_ids': [0],
            'label': 'any',
            'department': 'multi'
        }
        mocked_dal.company.get.return_value = None
        with self.assertRaises(ValueError):
            service.cluster_register.register(register_req)


class TestDwService(TestCase):
    
    def setUp(self):
        self.test_app = create_app()

    def update_se(self, store):
        from datetime import datetime
        store.deactivate_date = datetime.utcnow()
        return store

    @patch('mec_data.service.data_warehouse.dal')
    @patch('mec_data.service.data_warehouse.get_query_client')
    def test_load_stores(self, mget_query_client, mocked_dal):
        # Import
        from tests.mocks.athena_rows_test import mocked_rows
        from tests.mocks.dw_mocked_stores import get_stores
        from mec_data.model.company import Company
        from mec_data.service.data_warehouse import DataWarehouseService
        # Create mocks
        company = Company(id=1, name='test', department='test')
        mget_query_client.return_value.run_query.return_value = mocked_rows
        mocked_dal.store.get_by_name.return_value = None
        mocked_dal.store.get_by_company.return_value = get_stores()
        mocked_dal.store.update.side_effect = self.update_se
        mocked_dal.store.create.side_effect = self.update_se
        mocked_dal.city.get_by_code.return_value.id = 1
        # Start service and load stores
        with self.test_app.app_context():
            dw_service = DataWarehouseService(company)
            res = dw_service.load_stores('2020-01-16')
        # Assert    
        # TODO: implement closing
        # expected_closed = [
        #     'Test Macapá',
        #     'Test Manaus Grande Circular', 
        #     'Boa Vista'
        # ]
        # for closed_store in res['closed']:
        #     print(closed_store)
        #     self.assertIn(closed_store['name'], expected_closed)
        self.assertEqual(len(res['treated']), len(mocked_rows))


class TestClusterRegisterService(TestCase):

    def setUp(self):
        self.test_app = create_app()

    def _get_neighbors_se(self, neighbors_dict, stores, current_store):
        neighbors_names = neighbors_dict[current_store.name]
        neighbors = [s for s in stores if s.name in neighbors_names]
        return neighbors


    @patch('mec_data.service.cluster.dal')
    def test_cluster(self, mocked_dal):
        from mec_data.service.cluster import ClusterService
        from mec_data.model.cluster_register import ClusterRegister
        from mec_data.model.company import Company
        from tests.mocks.dw_mocked_stores import get_stores
        from tests.mocks.neighbors import neighbors_dict
        # Set mocks
        mocked_dal.cluster_register.get.return_value = ClusterRegister(
            id=1,
            department='jewelry',
            label='test x test',
            distances=[0, 1]
        )
        mocked_dal.cluster_register.get.return_value.associateds = [
            Company(
                id=1,
                name='test_company',
                department='jewelry'
            )
        ]
        stores = get_stores()
        mocked_dal.store.get_by_companies.return_value = stores
        mocked_dal.store.get_neighbors.side_effect = lambda \
            current_store, *args: self._get_neighbors_se(
                neighbors_dict, 
                stores, 
                current_store
            )
        # Run tests
        with self.test_app.app_context():
            cluster_service = service.cluster.ClusterService(1)
            res = cluster_service.cluster()
        self.assertEqual(
            res, 
            [
                'Clusterized 7 stores for test x test at 0km in 3 clusters',
                'Clusterized 7 stores for test x test at 1km in 3 clusters'
            ]
        )

