import os
from unittest import TestCase
from unittest.mock import patch
from urllib.error import HTTPError
from mec_data.utils.files import unzip_file
from mec_data.utils.download_manager import create_if_not_exists, download


class TestUtils(TestCase):
    def test_unzip(self):
        mock_folder = os.path.join(os.getcwd(), "tests", "mock")
        mock_tmp = os.path.join(os.getcwd(), "tests", "mock", "temp")
        zip_file = os.path.join(mock_folder, "test.zip")
        create_if_not_exists(mock_tmp)
        unzip_file(mock_tmp, zip_file, "*.csv")

    @patch("mec_data.utils.download_manager.urllib.request")
    def test_download(self, m_request):
        download("test.com", "path")

    @patch("mec_data.utils.download_manager.urllib.request")
    def test_http_error(self, m_request):
        m_request.Request.side_effect = HTTPError(
            url="mocked", code=500, msg="mocked", hdrs="mocked", fp="mocked"
        )
        download("test.com", "path")

    @patch("mec_data.utils.download_manager.urllib.request")
    def test_http_error_404(self, m_request):
        # Raise error as side effect of mocked request
        m_request.Request.side_effect = HTTPError(
            url="mocked", code=404, msg="mocked", hdrs="mocked", fp="mocked"
        )
        with self.assertRaises(HTTPError) as cm:
            download("test.com", "path")
