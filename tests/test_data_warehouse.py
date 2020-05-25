import os
from unittest import TestCase
from unittest.mock import patch
from mec_data.manage.app import create_app
from mec_data.model.databases import data_warehouse


class TestDataWarehouse(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_app = create_app()
        # Config Mocked DW
        # This sets up an empty sqlite database for tests
        cls.test_app.config[
            "SQLALCHEMY_DATABASE_URI"
        ] = f"sqlite:///{os.getcwd()}/tests/dw_mec_data.db"
        data_warehouse.init_app(cls.test_app)
        with cls.test_app.app_context():
            data_warehouse.create_all()

    @classmethod
    def tearDownClass(cls):
        os.remove("tests/dw_mec_data.db")

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
