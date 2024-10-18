"""Tests for the extract_s3.py file."""
from datetime import datetime, timedelta, timezone
import unittest
from unittest.mock import patch

import pandas as pd

from extract_s3 import get_object_names, create_dataframe, delete_object, extract


class TestGetObjectNames(unittest.TestCase):
    """Tests for get_object_names function."""

    @patch('extract_s3.client')
    def test_get_object_names_one_correct_time(self, fake_s3_client):
        """Testing only within the last hour."""
        fake_s3_client.list_objects.return_value = {
            "Contents": [
                {
                    "Key": "correct_article_data.csv",
                    "LastModified": datetime.now(timezone.utc) - timedelta(minutes=30)
                },
                {
                    "Key": "not_correct_article_data.csv",
                    "LastModified": datetime.now(timezone.utc) - timedelta(hours=50)
                },
                {
                    "Key": "another_not_correct_article_data.csv",
                    "LastModified": datetime.now(timezone.utc) - timedelta(hours=80)
                }
            ]
        }
        bucket_name = "test-bucket"
        result = get_object_names(fake_s3_client, bucket_name)

        self.assertEqual(result, ["correct_article_data.csv"])

    @patch('extract_s3.client')
    def test_get_object_names_one_correct_name(self, fake_s3_client):
        """Testing only the correct name format."""
        fake_s3_client.list_objects.return_value = {
            "Contents": [
                {
                    "Key": "correct_article_data.csv",
                    "LastModified": datetime.now(timezone.utc) - timedelta(minutes=30)
                },
                {
                    "Key": "not_correct_article_data_format.csv",
                    "LastModified": datetime.now(timezone.utc) - timedelta(minutes=30)
                },
                {
                    "Key": "not_correct_article_data",
                    "LastModified": datetime.now(timezone.utc) - timedelta(minutes=20)
                }
            ]
        }
        bucket_name = "test-bucket"
        result = get_object_names(fake_s3_client, bucket_name)

        self.assertEqual(result, ["correct_article_data.csv"])

    @patch('extract_s3.client')
    def test_get_object_names_multiple_correct(self, fake_s3_client):
        """Testing multiple correct filenames are returned."""
        fake_s3_client.list_objects.return_value = {
            "Contents": [
                {
                    "Key": "correct_article_data.csv",
                    "LastModified": datetime.now(timezone.utc) - timedelta(minutes=30)
                },
                {
                    "Key": "another_correct_article_data.csv",
                    "LastModified": datetime.now(timezone.utc) - timedelta(minutes=40)
                },
                {
                    "Key": "not_correct_article_data.csv",
                    "LastModified": datetime.now(timezone.utc) - timedelta(hours=50)
                }
            ]
        }
        bucket_name = "test-bucket"
        result = get_object_names(fake_s3_client, bucket_name)

        self.assertEqual(
            result, ["correct_article_data.csv", "another_correct_article_data.csv"])

    @patch('extract_s3.client')
    def test_get_object_names_none_raises_error(self, fake_s3_client):
        """Testing if no file names are returned, a value error is raised."""
        fake_s3_client.list_objects.return_value = {
            "Contents": [
                {
                    "Key": "not_correct_article_data.csv",
                    "LastModified": datetime.now(timezone.utc) - timedelta(hours=50)
                }
            ]
        }
        bucket_name = "test-bucket"

        with self.assertRaises(ValueError):
            get_object_names(fake_s3_client, bucket_name)


class TestCreateDataFrame(unittest.TestCase):
    """Tests for create_dataframe function."""

    @patch('extract_s3.client')
    def test_create_dataframe(self, fake_s3_client):
        """Tests that returns a dataframe with the expected values."""
        csv_data = b'col1,col2\nval1,val2\nval3,val4'
        fake_s3_client.download_fileobj.side_effect = lambda Bucket, Key, Fileobj: Fileobj.write(
            csv_data)
        bucket_name = "test-bucket"
        file_name = "test_file.csv"
        result_df = create_dataframe(
            fake_s3_client, bucket_name, file_name)
        expected_df = pd.DataFrame({
            "col1": ["val1", "val3"],
            "col2": ["val2", "val4"]
        })

        pd.testing.assert_frame_equal(result_df, expected_df)


class TestDeleteObject(unittest.TestCase):
    """Tests for delete_object function."""

    @patch('extract_s3.client')
    def test_delete_object(self, fake_s3_client):
        """Tests that delete_object is called once with correct parameters."""
        bucket_name = "test-bucket"
        file_name = "test_file.csv"
        delete_object(fake_s3_client, bucket_name, file_name)

        fake_s3_client.delete_object.assert_called_once_with(
            Bucket=bucket_name, Key=file_name)


class TestExtract(unittest.TestCase):
    """Tests for extract function."""

    @patch('extract_s3.get_object_names')
    @patch('extract_s3.create_dataframe')
    @patch('extract_s3.delete_object')
    @patch('extract_s3.client')
    @patch('extract_s3.ENV', {"BUCKET_NAME": "test-bucket",
                              "AWS_ACCESS_KEY": "test-access-key",
                              "AWS_SECRET_KEY": "test-secret-key"})
    def test_extract(self, fake_client, fake_delete_object,
                     fake_create_dataframe, fake_get_object_names):
        """Tests that extract returns a dataframe made from the create dataframe functions."""
        fake_get_object_names.return_value = [
            "test_file1.csv", "test_file2.csv"]
        df1 = pd.DataFrame(
            {"col1": ["val1", "val3"], "col2": ["val2", "val4"]})
        df2 = pd.DataFrame(
            {"col1": ["val5", "val7"], "col2": ["val6", "val8"]})
        fake_create_dataframe.side_effect = [df1, df2]
        result_df = extract()
        expected_df = pd.concat([df1, df2], ignore_index=True)

        pd.testing.assert_frame_equal(result_df, expected_df)
        fake_delete_object.assert_any_call(
            fake_client.return_value, "test-bucket", "test_file1.csv")
        fake_delete_object.assert_any_call(
            fake_client.return_value, "test-bucket", "test_file2.csv")
        self.assertEqual(fake_delete_object.call_count, 2)

    @patch('extract_s3.get_object_names')
    @patch('extract_s3.ENV', {"BUCKET_NAME": "test-bucket",
                              "AWS_ACCESS_KEY": "test-access-key",
                              "AWS_SECRET_KEY": "test-secret-key"})
    def test_extract_no_dfs_raise_error(self, fake_get_object_names):
        """Tests that is no dataframes are returned, a value error is raised."""
        fake_get_object_names.return_value = []

        with self.assertRaises(ValueError):
            extract()
