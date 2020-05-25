import os
from unittest import TestCase
from unittest.mock import patch
from mec_data.manage.app import create_app


class TestDataWarehouse(TestCase):
    def setUp(self):
        self.test_app = create_app()

    @patch("mec_data.service.data_warehouse.get_dl_client")
    def test_scholar_data_lake(self, m_get_dl_client):
        m_get_dl_client.return_value.get_files.return_value = [
            os.path.join(os.getcwd(), "tests", "mock", "scholar_co_2017.csv")
        ]
        with self.test_app.test_client() as client:
            response = client.post(
                "mec-data/data_warehouse/scholar_census/2017/", follow_redirects=True
            )
        # Assert that download method has been called correctly
        m_get_dl_client.assert_called_once()
        # Assert route response status
        self.assertEqual(response.status_code, 200)

    @patch("mec_data.service.data_warehouse.get_dl_client")
    def test_uni_data_lake(self, m_get_dl_client):
        m_get_dl_client.return_value.get_files.return_value = [
            os.path.join(os.getcwd(), "tests", "mock", "university_2017.csv")
        ]
        with self.test_app.test_client() as client:
            response = client.post(
                "mec-data/data_warehouse/university_census/2017/", follow_redirects=True
            )
        # Assert that download method has been called correctly
        m_get_dl_client.assert_called_once()
        # Assert route response status
        self.assertEqual(response.status_code, 200)
