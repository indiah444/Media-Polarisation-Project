# pylint: skip-file

"""Tests for load_rds.py file."""

import unittest
from unittest.mock import patch, MagicMock

import pandas as pd

from load_rds import load, insert_into_articles, process_df_for_assignment_insert, insert_into_assignment


class TestLoad(unittest.TestCase):
    """Tests for the load function."""

    @patch('load_rds.insert_into_articles')
    @patch('load_rds.process_df_for_assignment_insert')
    @patch('load_rds.insert_into_assignment')
    def test_load(self, fake_insert_into_assignment, fake_process_df_for_assignment_insert, fake_insert_into_articles):
        """Test that the load function calls all the necessary methods."""
        articles = pd.DataFrame({
            "title": ["Article 1", "Article 2"],
            "content": ["Content 1", "Content 2"],
            "polarity_score": [0.1, -0.3],
            "source_id": [1, 2],
            "date_published": [pd.Timestamp('2023-01-01'), pd.Timestamp('2023-01-02')],
            "article_url": ["http://article1.com", "http://article2.com"],
            "topics": [["Technology"], ["Health"]]
        })
        fake_insert_into_articles.return_value = {
            "Article 1": 101,
            "Article 2": 102
        }
        processed_df = pd.DataFrame({
            "topic_id": [1, 2],
            "article_id": [101, 102]
        })
        fake_process_df_for_assignment_insert.return_value = processed_df
        load(articles)

        fake_insert_into_articles.assert_called_once_with(articles)
        fake_process_df_for_assignment_insert.assert_called_once_with(
            articles, {"Article 1": 101, "Article 2": 102})
        fake_insert_into_assignment.assert_called_once_with(processed_df)

    @patch('load_rds.insert_into_articles')
    @patch('load_rds.process_df_for_assignment_insert')
    @patch('load_rds.insert_into_assignment')
    def test_load_with_empty_dataframe(self, fake_insert_into_assignment, fake_process_df_for_assignment_insert, fake_insert_into_articles):
        """Test that no methods are called when the dataframe is empty."""
        empty_articles = pd.DataFrame()
        load(empty_articles)

        fake_insert_into_articles.assert_not_called()
        fake_process_df_for_assignment_insert.assert_not_called()
        fake_insert_into_assignment.assert_not_called()


class TestInsertIntoArticles(unittest.TestCase):
    """Tests for the insert_into_articles function."""

    @patch('load_rds.create_connection')
    @patch('load_rds.execute_values')
    def test_insert_into_articles(self, fake_execute_values, fake_create_connection):
        """Test inserting articles into the database and returning the article_id dictionary."""
        articles = pd.DataFrame({
            "title": ["Article 1", "Article 2"],
            "content": ["Content 1", "Content 2"],
            "title_polarity_score": [0.1, -0.3],
            "content_polarity_score": [0.2, -0.5],
            "source_id": [1, 2],
            "published": [pd.Timestamp('2023-01-01'), pd.Timestamp('2023-01-02')],
            "link": ["http://article1.com", "http://article2.com"]
        })
        fake_cursor = MagicMock()
        fake_cursor.fetchall.return_value = [
            {"article_id": 101, "article_title": "Article 1"},
            {"article_id": 102, "article_title": "Article 2"}
        ]
        fake_conn = MagicMock()
        fake_conn.cursor.return_value.__enter__.return_value = fake_cursor
        fake_create_connection.return_value.__enter__.return_value = fake_conn
        result = insert_into_articles(articles)

        expected_result = {
            "Article 1": 101,
            "Article 2": 102
        }
        self.assertEqual(result, expected_result)
        fake_execute_values.assert_called_once()
        fake_cursor.fetchall.assert_called_once()
        fake_conn.commit.assert_called_once()


class TestProcessDfForAssignmentInsert(unittest.TestCase):
    """Tests for the process_df_for_assignment_insert function."""

    @patch('load_rds.get_topic_dict')
    def test_process_df_for_assignment_insert(self, fake_get_topic_dict):
        """Test processing the DataFrame for assignment insertion."""
        fake_get_topic_dict.return_value = {
            "Technology": 1,
            "Health": 2
        }
        articles = pd.DataFrame({
            "title": ["Article 1", "Article 2"],
            "topics": [["Technology"], ["Health"]]
        })
        article_id_dict = {
            "Article 1": 101,
            "Article 2": 102
        }
        result_df = process_df_for_assignment_insert(articles, article_id_dict)

        expected_df = pd.DataFrame({
            "topic_id": [1, 2],
            "article_id": [101, 102]
        })
        pd.testing.assert_frame_equal(result_df, expected_df)


class TestInsertIntoAssignment(unittest.TestCase):
    """Tests for the insert_into_assignment function."""

    @patch('load_rds.create_connection')
    @patch('load_rds.execute_values')
    def test_insert_into_assignment(self, fake_execute_values, fake_create_connection):
        """Test bulk insert of article-topic assignments into the database."""
        articles = pd.DataFrame({
            "topic_id": [1, 2],
            "article_id": [101, 102]
        })
        fake_conn = MagicMock()
        fake_create_connection.return_value.__enter__.return_value = fake_conn
        insert_into_assignment(articles)

        params = [(1, 101), (2, 102)]
        fake_execute_values.assert_called_once()
        call_args = fake_execute_values.call_args[0]
        self.assertEqual(call_args[2], params)
        fake_conn.commit.assert_called_once()
