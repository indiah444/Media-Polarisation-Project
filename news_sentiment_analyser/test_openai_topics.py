# pylint: skip-file

"""Tests for the openai_topics.py file."""

import unittest
from unittest.mock import patch, MagicMock
import json

import pandas as pd
from openai import OpenAI

from openai_topics import (add_topics_to_dataframe, find_article_topics,
                           chunk_list, create_message, OpenAIError)


class TestAddTopicsToDataFrame(unittest.TestCase):
    """Tests for add_topics_to_dataframe function."""

    @patch('openai_topics.get_topic_names')
    @patch('openai_topics.OpenAI')
    @patch('openai_topics.ENV', {"OPENAI_API_KEY": "fake_api_key"})
    def test_add_topics_to_dataframe(self, fake_OpenAI, fake_get_topic_names):
        """Tests works with valid input al all rows with topics."""
        fake_get_topic_names.return_value = ["Technology", "Health", "Sports"]
        fake_ai_client = MagicMock(spec=OpenAI)
        fake_OpenAI.return_value = fake_ai_client
        fake_chat = MagicMock()
        fake_ai_client.chat = fake_chat
        fake_response = MagicMock()
        fake_response.choices = [MagicMock()]
        fake_response.choices[0].message.content = json.dumps([
            {"title": "Article 1", "topics": ["Technology"]},
            {"title": "Article 2", "topics": ["Health"]}
        ])
        fake_chat.completions.create.return_value = fake_response
        articles = pd.DataFrame({"title": ["Article 1", "Article 2"]})
        result_df = add_topics_to_dataframe(articles)

        fake_chat.completions.create.assert_called_once()
        self.assertEqual(result_df['topics'].iloc[0], ["Technology"])
        self.assertEqual(result_df['topics'].iloc[1], ["Health"])
        self.assertTrue(len(result_df) == 2)

    @patch('openai_topics.get_topic_names')
    @patch('openai_topics.OpenAI')
    @patch('openai_topics.ENV', {"OPENAI_API_KEY": "fake_api_key"})
    def test_empty_topics_rows_are_dropped(self, fake_OpenAI, fake_get_topic_names):
        """Test that rows with empty topics are dropped from the DataFrame."""
        fake_get_topic_names.return_value = ["Technology", "Health", "Sports"]
        fake_ai_client = MagicMock(spec=OpenAI)
        fake_OpenAI.return_value = fake_ai_client
        fake_chat = MagicMock()
        fake_ai_client.chat = fake_chat
        fake_response = MagicMock()
        fake_response.choices = [MagicMock()]
        fake_response.choices[0].message.content = json.dumps([
            {"title": "Article 1", "topics": ["Technology"]},
            {"title": "Article 2", "topics": []}
        ])
        fake_chat.completions.create.return_value = fake_response
        articles = pd.DataFrame({"title": ["Article 1", "Article 2"]})
        result_df = add_topics_to_dataframe(articles)

        self.assertEqual(len(result_df), 1)
        self.assertEqual(result_df['title'].iloc[0], "Article 1")

    @patch('openai_topics.get_topic_names')
    @patch('openai_topics.OpenAI')
    @patch('openai_topics.ENV', {"OPENAI_API_KEY": "fake_api_key"})
    def test_no_topics_returned(self, fake_OpenAI, fake_get_topic_names):
        """Test behavior when no topics are returned by the API."""
        fake_get_topic_names.return_value = ["Technology", "Health", "Sports"]
        fake_ai_client = MagicMock(spec=OpenAI)
        fake_OpenAI.return_value = fake_ai_client
        fake_chat = MagicMock()
        fake_ai_client.chat = fake_chat
        fake_response = MagicMock()
        fake_response.choices = [MagicMock()]
        fake_response.choices[0].message.content = json.dumps([
            {"title": "Article 1", "topics": []},
            {"title": "Article 2", "topics": []}
        ])
        fake_chat.completions.create.return_value = fake_response
        articles = pd.DataFrame({"title": ["Article 1", "Article 2"]})
        result_df = add_topics_to_dataframe(articles)

        self.assertEqual(len(result_df), 0)

    def test_missing_title_column(self):
        """Test if a ValueError is raised when 'title' column is missing."""
        articles = pd.DataFrame({"not_title": ["Article 1", "Article 2"]})

        with self.assertRaises(ValueError) as context:
            add_topics_to_dataframe(articles)
        self.assertEqual(str(context.exception),
                         "DataFrame must contain a 'title' column")

    def test_empty_dataframe(self):
        """Test if a ValueError is raised when the DataFrame is empty."""
        articles = pd.DataFrame(columns=["title"])

        with self.assertRaises(ValueError) as context:
            add_topics_to_dataframe(articles)
        self.assertEqual(str(context.exception), "DataFrame is empty")


class TestFindArticleTopics(unittest.TestCase):
    """Tests for find_article_topics function."""

    @patch('openai_topics.OpenAI')
    def test_find_article_topics(self, fake_OpenAI):
        """Test valid calls are processed correctly."""
        fake_ai_client = MagicMock(spec=OpenAI)
        fake_OpenAI.return_value = fake_ai_client
        fake_chat = MagicMock()
        fake_ai_client.chat = fake_chat
        fake_response = MagicMock()
        fake_response.choices = [MagicMock()]
        fake_response.choices[0].message.content = json.dumps([
            {"title": "Article 1", "topics": ["Technology"]},
            {"title": "Article 2", "topics": ["Health"]}
        ])
        fake_chat.completions.create.return_value = fake_response
        article_titles = ["Article 1", "Article 2"]
        topics = ["Technology", "Health", "Sports"]
        result = find_article_topics(
            article_titles, topics, fake_ai_client)

        fake_chat.completions.create.assert_called_once()
        expected_result = {
            "Article 1": ["Technology"],
            "Article 2": ["Health"]
        }
        self.assertEqual(result, expected_result)

    @patch('openai_topics.OpenAI')
    def test_openai_api_error(self, fake_OpenAI):
        """Test handling of OpenAI API errors."""
        fake_ai_client = MagicMock(spec=OpenAI)
        fake_OpenAI.return_value = fake_ai_client
        fake_chat = MagicMock()
        fake_ai_client.chat = fake_chat
        fake_chat.completions.create.side_effect = OpenAIError(
            "API error")
        article_titles = ["Article 1", "Article 2"]
        topics = ["Technology", "Health", "Sports"]
        result = find_article_topics(article_titles, topics, fake_ai_client)

        expected_result = {
            "Article 1": [],
            "Article 2": []
        }
        self.assertEqual(result, expected_result)

    @patch('openai_topics.OpenAI')
    def test_json_parsing_error(self, fake_OpenAI):
        """Test handling of JSON parsing errors in OpenAI response."""
        fake_ai_client = MagicMock(spec=OpenAI)
        fake_OpenAI.return_value = fake_ai_client
        fake_chat = MagicMock()
        fake_ai_client.chat = fake_chat
        fake_response = MagicMock()
        fake_response.choices = [MagicMock()]
        fake_response.choices[0].message.content = "Invalid JSON"
        fake_chat.completions.create.return_value = fake_response
        article_titles = ["Article 1", "Article 2"]
        topics = ["Technology", "Health", "Sports"]
        result = find_article_topics(article_titles, topics, fake_ai_client)

        expected_result = {
            "Article 1": [],
            "Article 2": []
        }
        self.assertEqual(result, expected_result)

    @patch('openai_topics.OpenAI')
    def test_json_with_code_block(self, fake_OpenAI):
        """Test handling of OpenAI response wrapped in ```json code block."""
        fake_ai_client = MagicMock(spec=OpenAI)
        fake_OpenAI.return_value = fake_ai_client
        fake_chat = MagicMock()
        fake_ai_client.chat = fake_chat
        fake_response = MagicMock()
        fake_response.choices = [MagicMock()]
        fake_response.choices[0].message.content = "```json\n" + json.dumps([
            {"title": "Article 1", "topics": ["Technology"]},
            {"title": "Article 2", "topics": ["Health"]}
        ]) + "\n```"
        fake_chat.completions.create.return_value = fake_response
        article_titles = ["Article 1", "Article 2"]
        topics = ["Technology", "Health", "Sports"]
        result = find_article_topics(article_titles, topics, fake_ai_client)

        expected_result = {
            "Article 1": ["Technology"],
            "Article 2": ["Health"]
        }
        fake_chat.completions.create.assert_called_once()
        self.assertEqual(result, expected_result)


class TestChunkList(unittest.TestCase):
    """Tests chuck_list function."""

    def test_chunk_list(self):
        """Tests the expected outcome."""
        lst = ["A", "B", "C", "D", "E"]
        chunks = list(chunk_list(lst, 2))

        expected_chunks = [["A", "B"], ["C", "D"], ["E"]]
        self.assertEqual(chunks, expected_chunks)


class TestCreateMessage(unittest.TestCase):
    """Tests create_message function."""

    def test_create_message(self):
        """Tests topics are in message."""
        topics = ["Technology", "Health", "Sports"]

        result_message = create_message(topics)
        for topic in topics:
            self.assertIn(topic, result_message)
