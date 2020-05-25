from unittest import TestCase
from unittest.mock import patch
from mec_data.manage.app import create_app
from urllib.error import HTTPError


class TestDataSource(TestCase):
    """
    This tests cases take care of mec-data/download/ routes
    """

    def setUp(self):
        self.test_app = create_app()

    @patch("mec_data.source.base.download_file")
    def test_scholar_download(self, m_download_file):
        """
        Test a scholar census call that should return status 200
        """
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
    def test_scholar_download_error_not_404(self, m_download_file):
        """
        Test a scholar census call that should fail and return 500
        this test covers download from source response != 404 on
        source.scholar.download method
        """
        m_download_file.side_effect = HTTPError(
            url="mocked", code=500, msg="mocked", hdrs="mocked", fp="mocked"
        )
        # Make post request to download data from SCHOLAR CENSUS
        # When raising HTTP error != from 404
        with self.test_app.test_client() as client:
            response = client.post(
                "mec-data/download/scholar_census/2017/", follow_redirects=True
            )
        # Assert that download method has been called correctly
        m_download_file.assert_called_once()
        # Assert route response status
        self.assertEqual(response.status_code, 500)

    @patch("mec_data.source.base.download_file")
    def test_scholar_download_error_404(self, m_download_file):
        """
        Test a scholar census call that should fail and return 500
        this test covers download from source response is 404 on
        source.scholar.download method
        """
        # When download error is 404
        m_download_file.side_effect = HTTPError(
            url="mocked", code=404, msg="mocked", hdrs="mocked", fp="mocked"
        )
        with self.test_app.test_client() as client:
            response = client.post(
                "mec-data/download/scholar_census/2017/", follow_redirects=True
            )
        # Assert that download method has been called 2 times
        assert 2 == m_download_file.call_count
        # Assert route response status
        self.assertEqual(response.status_code, 500)

    @patch("mec_data.source.base.download_file")
    def test_university_download(self, m_download_file):
        """
        Test a university census call that should return status 200
        """
        with self.test_app.test_client() as client:
            response = client.post(
                "mec-data/download/university_census/2017/", follow_redirects=True
            )
        # Assert that download method has been called correctly
        m_download_file.assert_called_once()
        # Assert route response status
        self.assertEqual(response.status_code, 200)

    @patch("mec_data.source.base.download_file")
    def test_university_download_error_not_404(self, m_download_file):
        """
        Test a university census call that should fail and return 500
        this test covers download response != 404 on
        source.university.download method
        """
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

    @patch("mec_data.source.base.download_file")
    def test_university_download_error_404(self, m_download_file):
        """
        Test a university census call that should fail and return 500
        this test covers download from source response is 404 on
        source.university.download method
        """
        m_download_file.side_effect = HTTPError(
            url="mocked", code=404, msg="mocked", hdrs="mocked", fp="mocked"
        )
        with self.test_app.test_client() as client:
            response = client.post(
                "mec-data/download/university_census/2017/", follow_redirects=True
            )
        # Assert that download method has been called correctly
        assert 2 == m_download_file.call_count
        # Assert route response status
        self.assertEqual(response.status_code, 500)
