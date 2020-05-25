from unittest import TestCase
from unittest.mock import patch
from mec_data.manage.app import create_app
from urllib.error import HTTPError


class TestDataSource(TestCase):
    def setUp(self):
        self.test_app = create_app()

    @patch("mec_data.source.base.download_file")
    def test_scholar_post(self, m_download_file):
        # Make post request to download data from SCHOLAR CENSUS
        with self.test_app.test_client() as client:
            response = client.post(
                "mec-data/download/scholar_census/2017/", follow_redirects=True
            )
        # Assert that download method has been called correctly
        m_download_file.assert_called_once()
        # Assert route response status
        self.assertEqual(response.status_code, 200)

    @patch("mec_data.source.base.download_file")
    def test_scholar_post_errors(self, m_download_file):
        m_download_file.side_effect = HTTPError(
            url="mocked", code=500, msg="mocked", hdrs="mocked", fp="mocked"
        )
        # Make post request to download data from SCHOLAR CENSUS
        # When raising error
        with self.test_app.test_client() as client:
            response = client.post(
                "mec-data/download/scholar_census/2017/", follow_redirects=True
            )
        # Assert that download method has been called correctly
        m_download_file.assert_called_once()
        # Assert route response status
        self.assertEqual(response.status_code, 500)

        # If download error is 404
        m_download_file.side_effect = HTTPError(
            url="mocked", code=404, msg="mocked", hdrs="mocked", fp="mocked"
        )
        with self.test_app.test_client() as client:
            response = client.post(
                "mec-data/download/scholar_census/2017/", follow_redirects=True
            )
        # Assert that download method has been called 2+1 times
        assert 3 == m_download_file.call_count
        # Assert route response status
        self.assertEqual(response.status_code, 500)

    @patch("mec_data.source.base.download_file")
    def test_university_post(self, m_download_file):
        with self.test_app.test_client() as client:
            response = client.post(
                "mec-data/download/university_census/2017/", follow_redirects=True
            )
        # Assert that download method has been called correctly
        m_download_file.assert_called_once()
        # Assert route response status
        self.assertEqual(response.status_code, 200)

    @patch("mec_data.source.base.download_file")
    def test_university_post_errors(self, m_download_file):
        m_download_file.side_effect = HTTPError(
            url="mocked", code=500, msg="mocked", hdrs="mocked", fp="mocked"
        )
        with self.test_app.test_client() as client:
            response = client.post(
                "mec-data/download/university_census/2017/", follow_redirects=True
            )
        # Assert that download method has been called correctly
        m_download_file.assert_called_once()
        # Assert route response status
        self.assertEqual(response.status_code, 500)

        m_download_file.side_effect = HTTPError(
            url="mocked", code=404, msg="mocked", hdrs="mocked", fp="mocked"
        )
        with self.test_app.test_client() as client:
            response = client.post(
                "mec-data/download/university_census/2017/", follow_redirects=True
            )
        # Assert that download method has been called correctly
        assert 3 == m_download_file.call_count
        # Assert route response status
        self.assertEqual(response.status_code, 500)
