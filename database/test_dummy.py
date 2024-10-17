# pylint: skip-file

"""
Testing dummy data generation
"""

from unittest import TestCase
from unittest.mock import patch, MagicMock
from generate_dummy_data import connect, generate_article_topic_assignment


@patch('psycopg2.connect')
def test_connection(mock_connect):
    """Tests the connection"""

    mock_connection = MagicMock()
    mock_connect.return_value = mock_connection

    # Provide mock parameters for the connection
    connection = connect(dbname="test_db", host="localhost",
                         user="test_user", port="5432", password="test_pass")

    mock_connect.assert_called_once()
    assert connection == mock_connection


class TestGenerateArticleTopicAssignment(TestCase):

    def test_empty_headlines(self):
        """Test with an empty headlines dictionary."""
        result = generate_article_topic_assignment({}, ["Topic1", "Topic2"])
        self.assertEqual(result, [])

    def test_single_article_no_topics(self):
        """Test with a single article with no topics."""
        headlines = {"Article1": []}
        ordered_topics = ["Topic1", "Topic2"]
        result = generate_article_topic_assignment(headlines, ordered_topics)
        self.assertEqual(result, [])

    def test_single_article_with_topics(self):
        """Test with a single article with multiple topics."""
        headlines = {"Article1": ["Topic1", "Topic2"]}

        ordered_topics = ["Topic1", "Topic2", "Topic3"]

        result = generate_article_topic_assignment(headlines, ordered_topics)

        self.assertEqual(result, [(1, 1), (2, 1)])

    def test_multiple_articles(self):
        """Test with multiple articles and multiple topics."""
        headlines = {
            "Article1": ["Topic1"],
            "Article2": ["Topic2", "Topic3"]
        }
        ordered_topics = ["Topic1", "Topic2", "Topic3"]
        result = generate_article_topic_assignment(headlines, ordered_topics)

        self.assertEqual(result, [(1, 1), (2, 2), (3, 2)])

    def test_topic_not_found(self):
        """Test with a topic that is not found in ordered_topics."""
        headlines = {"Article1": ["Topic1", "UnknownTopic"]}
        ordered_topics = ["Topic1", "Topic2"]
        with self.assertRaises(ValueError):
            generate_article_topic_assignment(headlines, ordered_topics)
