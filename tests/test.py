import os.path
import unittest

import mock
import run_lambda

from functions.convert.main import handle


class MainTest(unittest.TestCase):

    def test_empty(self):
        here = os.path.abspath(os.path.dirname(__file__))

        cdn_bucket = "bucket"
        cdn_file = "file"
        event = {
            "job": {
                "source": "file:{}".format(os.path.join(here, "resources/test.zip"))
            },
            "upload": {
                "cdn_bucket": cdn_bucket,
                "cdn_file": cdn_file
            }
        }

        mock_client = mock.MagicMock()
        mock_client.upload_file = mock.MagicMock()
        patches = {"boto3.client": mock.MagicMock(return_value=mock_client)}

        result = run_lambda.run_lambda(handle, event, patches=patches)
        self.assertIsNone(result.exception)
        self.assertIsNotNone(mock_client.upload_file.call_args)
        args, kwargs = mock_client.upload_file.call_args
        self.assertEqual(len(args), 3)
        self.assertEqual(len(kwargs), 0)
        self.assertEqual(args[1], cdn_bucket)
        self.assertEqual(args[2], cdn_file)
        output_zip_filename = args[0]
        self.assertTrue(os.path.isfile(output_zip_filename))


if __name__ == "__main__":
    unittest.main()
