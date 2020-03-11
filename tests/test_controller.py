from unittest import TestCase
from unittest.mock import patch

from retail_stores.manage.app import create_app
from retail_stores.model.company import Company


class TestCompanyController(TestCase):

    def setUp(self):
        self.test_app = create_app()

    @patch('retail_stores.controller.company.service')    
    def test_company_post(self, mocked_service):
        mocked_service.company.create.return_value = Company(
            id=0, name='teste', department='clothing'
        )
        post_json = {'name': 'teste', 'department': 'clothing'}
        expected_json = {'id':0, 'name': 'teste', 'department': 'clothing'}
        with self.test_app.test_client() as client:
            response = client.post(
                '/company/',
                json=post_json,
                follow_redirects=True
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), expected_json)

    @patch('retail_stores.controller.company.service')    
    def test_company_get(self, mocked_service):
        mocked_service.company.get_all.return_value = [
            Company(id=1, name='teste', department='clothing'),
            Company(id=2, name='teste2', department='clothing')
        ]
        expected_json = [
            {'id': 1, 'name': 'teste', 'department': 'clothing'},
            {'id': 2, 'name': 'teste2', 'department': 'clothing'}
        ]
        with self.test_app.test_client() as client:
            response = client.get(
                '/company/',
                follow_redirects=True
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), expected_json)


class TestCrawlController(TestCase):

    def setUp(self):
        self.test_app = create_app()

    @patch('retail_stores.controller.crawl.service')
    def test_crawl_post(self, mocked_service):
        mocked_service.company.crawl.return_value = ('Crawled 1 item', 200)
        with self.test_app.test_client() as client:
            response = client.post(
                '/crawl/1/',
                follow_redirects=True
            )
        mocked_service.company.crawl.assert_called_once_with('1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), 'Crawled 1 item')


class TestClusterController(TestCase):

    def setUp(self):
        self.test_app = create_app()

    @patch('retail_stores.controller.cluster.service')
    def test_register_post(self, mocked_service):
        post_json = {
            'distances': [0, 1, 2.5],
            'company_ids': [1, 2, 3],
            'label': 'clothing',
            'department': 'depar'
        }
        response_json = {
            'distances': [0.0, 1.0, 2.5],
            'label': 'clothing',
            'department': 'depar'
        }
        mocked_service.cluster_register.register.return_value = post_json
        with self.test_app.test_client() as client:
            response = client.post(
                '/cluster/register/',
                json=post_json,
                follow_redirects=True
            )
        mocked_service.cluster_register.register.assert_called_once_with(
            post_json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), response_json)

    @patch('retail_stores.controller.cluster.service')
    def test_register_post_exception(self, mocked_service):
        post_json = {
            'distances': [0, 1, 2.5],
            'company_ids': [1, 2, 3],
            'label': 'clothing',
            'department': 'depar'
        }
        mocked_service.cluster_register.register.side_effect = AttributeError(
            'Fail')
        with self.test_app.test_client() as client:
            response = client.post(
                '/cluster/register/',
                json=post_json,
                follow_redirects=True
            )
        mocked_service.cluster_register.register.assert_called_once_with(post_json)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_data(as_text=True), 'Fail')

    @patch('retail_stores.controller.cluster.service.cluster.ClusterService')
    def test_cluster(self, MClusterService):
        MClusterService.return_value.cluster.return_value = 'cluster'
        with self.test_app.test_client() as client:
            response = client.post(
                '/cluster/1/',
                follow_redirects=True
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), 'cluster')


class TestIBGEController(TestCase):

    def setUp(self):
        self.test_app = create_app()

    @patch('retail_stores.controller.ibge_data.service')
    def test_cities_post(self, mocked_service):
        mocked_service.ibge_data.load_cities.return_value = 'Loaded 1 city'
        with self.test_app.test_client() as client:
            response = client.post(
                '/ibge_data/cities/',
                follow_redirects=True
            )
        mocked_service.ibge_data.load_cities.assert_called_once_with()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), 'Loaded 1 city')

    @patch('retail_stores.controller.ibge_data.service')
    def test_age_level_post(self, mocked_service):
        mocked_service.ibge_data.load_age_level.return_value = 'Loaded 1 for 1 cities'
        with self.test_app.test_client() as client:
            response = client.post(
                '/ibge_data/age_level/2010/',
                follow_redirects=True
            )
        mocked_service.ibge_data.load_age_level.assert_called_once_with('2010')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), 'Loaded 1 for 1 cities')

    @patch('retail_stores.controller.ibge_data.service')
    def test_education_level_post(self, mocked_service):
        mocked_service.ibge_data.load_education_level.return_value = 'Loaded 1 for 1 cities'
        with self.test_app.test_client() as client:
            response = client.post(
                '/ibge_data/education_level/2010/',
                follow_redirects=True
            )
        mocked_service.ibge_data.load_education_level.assert_called_once_with(
            '2010')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), 'Loaded 1 for 1 cities')

    @patch('retail_stores.controller.ibge_data.service')
    def test_load_income_range_post(self, mocked_service):
        mocked_service.ibge_data.load_income_range.return_value = 'Loaded 1 for 1 cities'
        with self.test_app.test_client() as client:
            response = client.post(
                '/ibge_data/income_range/2010/',
                follow_redirects=True
            )
        mocked_service.ibge_data.load_income_range.assert_called_once_with(
            '2010')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), 'Loaded 1 for 1 cities')
