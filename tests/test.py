import os.path
import unittest
import zipfile

import mock
import run_lambda

from functions.convert.main import handle


class MainTest(unittest.TestCase):

    def setUp(self):
        self.cdn_bucket = "cdn_bucket"
        self.cdn_file = "cdn_file"

        # mock for boto3.client(..).upload_file(..)
        # self.mock_upload_file = mock.MagicMock()
        self.mock_client = mock.MagicMock()
        self.patches = {"boto3.client": mock.MagicMock(return_value=self.mock_client)}

    def test_empty(self):
        event = self.event("resources/empty.zip")
        result = run_lambda.run_lambda(handle, event, patches=self.patches)
        output_zip_filename = self.assert_success(result)
        with zipfile.ZipFile(output_zip_filename, "r") as output_zip:
            self.assertEqual(len(output_zip.infolist()), 0)

    def test_single(self):
        event = self.event("resources/genesis.zip")
        result = run_lambda.run_lambda(handle, event, patches=self.patches)
        output_zip_filename = self.assert_success(result)
        with zipfile.ZipFile(output_zip_filename, "r") as output_zip:
            names = set(output_zip.namelist())
            expected = {"default.css", "genesis.html"}
            self.assertEqual(names, expected)

    def test_multiple(self):
        event = self.event("resources/multiple.zip")
        result = run_lambda.run_lambda(handle, event, patches=self.patches)
        output_zip_filename = self.assert_success(result)
        with zipfile.ZipFile(output_zip_filename, "r") as output_zip:
            names = set(output_zip.namelist())
            expected = {"default.css", "genesis.html", "luke.html"}
            self.assertEqual(names, expected)

    def test_missing_file(self):
        event = self.event("resources/doesnotexist.zip")
        result = run_lambda.run_lambda(handle, event, patches=self.patches)
        self.assertIsInstance(result.exception, IOError)

    # helper methods
    def event(self, filename):
        here = os.path.abspath(os.path.dirname(__file__))
        return {
            "job": {
                "source": "file:{}".format(os.path.join(here, filename))
            },
            "upload": {
                "cdn_bucket": self.cdn_bucket,
                "cdn_file": self.cdn_file
            }
        }

    def assert_success(self, result):
        self.assertIsNone(result.exception)
        self.assertFalse(result.timed_out)
        self.assertIsNotNone(self.mock_client.upload_file.call_args)
        args, kwargs = self.mock_client.upload_file.call_args
        self.assertEqual(len(args), 3)
        self.assertEqual(len(kwargs), 0)
        self.assertEqual(args[1], self.cdn_bucket)
        self.assertEqual(args[2], self.cdn_file)
        output_zip = args[0]
        self.assertTrue(os.path.isfile(output_zip))
        return output_zip

if __name__ == "__main__":
    unittest.main()
