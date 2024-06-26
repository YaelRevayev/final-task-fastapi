import unittest
from httpx import WSGITransport, Client
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi_server import app, extract_files_in_order


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    async def test_extract_files_in_order_given_right_order_returns_same_order(self):
        files = [
            MagicMock(filename="file_a.txt", read=MagicMock(return_value=b"content_a")),
            MagicMock(filename="file_b.txt", read=MagicMock(return_value=b"content_b")),
        ]

        result = await extract_files_in_order(files)

        expected_result = (b"content_a", b"content_b")
        self.assertEqual(result, expected_result)

    async def test_extract_files_in_order_given_wrong_order_returns_opposite_order(
        self,
    ):
        files = [
            MagicMock(filename="file_b.txt", read=MagicMock(return_value=b"content_b")),
            MagicMock(filename="file_a.txt", read=MagicMock(return_value=b"content_a")),
        ]

        result = await extract_files_in_order(files)

        expected_result = (b"content_a", b"content_b")
        self.assertEqual(result, expected_result)

    async def test_merge_and_sign_api_mocking_valid_request_returns_code_200(self):
        with patch("fastapi_server.create_loggers") as mock_create_loggers:
            mock_merged_files_logger = MagicMock()
            mock_error_logger = MagicMock()
            mock_create_loggers.return_value = (
                mock_merged_files_logger,
                mock_error_logger,
            )

            files = []
            files.append(("files", ("test100_a.jpg", b"test_data1")))
            files.append(("files", ("test100_b", b"test_data2")))

            async with Client(app=app, transport=WSGITransport()) as client:
                response = await client.post("/merge_and_sign", files=files)

            self.assertEqual(response.status_code, 200)

            mock_merged_files_logger.info.assert_called_once_with(
                "Merged file saved: %s", "test100.jpg"
            )

    def test_merge_files_with_sending_empty_list_receiving_unprocessable_entity_code(
        self,
    ):
        response = self.client.post("/merge_and_sign", files=[])
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
