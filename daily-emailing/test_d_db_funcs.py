# pylint: skip-file

from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta

import pandas as pd

from d_db_funcs import get_avg_polarity_by_topic_and_source_yesterday, get_daily_subscribers, get_yesterday_links_and_titles


class TestGetAvgPolarityByTopicAndSourceYesterday:

    @patch('d_db_funcs.get_cursor')
    @patch('d_db_funcs.create_connection')
    @patch('d_db_funcs.get_yesterday_date')
    def test_correct_cursor_call_and_empty_dataframe(self, mock_get_yesterday_date, mock_create_conn, mock_get_cursor):

        mock_get_yesterday_date.return_value = '2024-01-01'
        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_create_conn.return_value.__enter__.return_value = mock_conn
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.fetchall.return_value = []

        query = """
        SELECT t.topic_name, s.source_name,
        AVG(a.content_polarity_score) AS avg_polarity_score
        FROM article_topic_assignment ata
        JOIN article a ON ata.article_id = a.article_id
        JOIN topic t ON ata.topic_id = t.topic_id
        JOIN source s ON a.source_id = s.source_id
        WHERE a.date_published = %s
        GROUP BY t.topic_name, s.source_name
        ORDER BY t.topic_name, s.source_name;
    """

        result = get_avg_polarity_by_topic_and_source_yesterday()

        mock_cursor.execute.assert_called_once_with(query, ('2024-01-01',))
        assert len(result.index) == 0

    @patch('d_db_funcs.get_cursor')
    @patch('d_db_funcs.create_connection')
    @patch('d_db_funcs.get_yesterday_date')
    def test_output(self, mock_get_yesterday_date, mock_create_conn, mock_get_cursor):

        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_create_conn.return_value.__enter__.return_value = mock_conn
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor

        sample_data = [('Politics', 'Source A', 0.5),
                       ('Sports', 'Source B', 0.2)]
        mock_cursor.fetchall.return_value = sample_data

        result_df = get_avg_polarity_by_topic_and_source_yesterday()

        expected_df = pd.DataFrame(sample_data)
        pd.testing.assert_frame_equal(result_df, expected_df)


class TestGetDailySubscribers:

    @patch('d_db_funcs.get_cursor')
    @patch('d_db_funcs.create_connection')
    @patch('d_db_funcs.get_yesterday_date')
    def test_correct_cursor_call_and_empty_data(self, mock_get_yesterday_date, mock_create_conn, mock_get_cursor):

        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_create_conn.return_value.__enter__.return_value = mock_conn
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.fetchall.return_value = []

        query = """
        SELECT subscriber_email 
        FROM subscriber
        WHERE daily = TRUE
    """

        result = get_daily_subscribers()

        mock_cursor.execute.assert_called_once_with(query)
        assert len(result) == 0

    @patch('d_db_funcs.get_cursor')
    @patch('d_db_funcs.create_connection')
    def test_with_data(self, mock_create_conn, mock_get_cursor):

        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_create_conn.return_value.__enter__.return_value = mock_conn
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor

        sample_data = [{'subscriber_email': 'user1@example.com'},
                       {'subscriber_email': 'user2@example.com'}]
        mock_cursor.fetchall.return_value = sample_data

        result = get_daily_subscribers()
        expected_result = ['user1@example.com', 'user2@example.com']

        assert result == expected_result

    @patch('d_db_funcs.get_cursor')
    @patch('d_db_funcs.create_connection')
    def test_no_data(self, mock_create_conn, mock_get_cursor):

        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_create_conn.return_value.__enter__.return_value = mock_conn
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.fetchall.return_value = []
        result = get_daily_subscribers()
        expected_result = []

        assert result == expected_result


class TestGetYesterdayLinks:

    @patch('d_db_funcs.get_cursor')
    @patch('d_db_funcs.create_connection')
    @patch('d_db_funcs.get_yesterday_date')
    def test_correct_cursor_call_and_empty_data(self, mock_get_yesterday_date, mock_create_conn, mock_get_cursor):

        mock_get_yesterday_date.return_value = '2024-01-01'
        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_create_conn.return_value.__enter__.return_value = mock_conn
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.fetchall.return_value = []

        query = """
        SELECT a.article_url, a.article_title, t.topic_name
        FROM article_topic_assignment ata
        JOIN article a ON ata.article_id = a.article_id
        JOIN topic t ON ata.topic_id = t.topic_id
        WHERE a.date_published = %s 
    """

        result = get_yesterday_links_and_titles()

        mock_cursor.execute.assert_called_once_with(query, ('2024-01-01',))
        assert len(result) == 0

    @patch('d_db_funcs.get_cursor')
    @patch('d_db_funcs.create_connection')
    @patch('d_db_funcs.get_yesterday_date')
    def test_with_data(self, mock_get_yesterday_date, mock_create_conn, mock_get_cursor):

        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_create_conn.return_value.__enter__.return_value = mock_conn
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor

        sample_data = [{'article_url': 'http://example.com/article1', 'article_title': 'article1', 'topic_name': 'topic1'},
                       {'article_url': 'http://example.com/article2', 'article_title': 'article2', 'topic_name': 'topic2'}]
        mock_cursor.fetchall.return_value = sample_data

        result = get_yesterday_links_and_titles()
        print(result)
        expected_result = [{'title': 'article1', 'link': 'http://example.com/article1', 'topic': 'topic1'},
                           {'title': 'article2', 'link': 'http://example.com/article2', 'topic': 'topic2'}]

        assert result == expected_result

    @patch('d_db_funcs.get_cursor')
    @patch('d_db_funcs.create_connection')
    @patch('d_db_funcs.get_yesterday_date')
    def test_no_data(self, mock_get_yesterday_date, mock_create_conn, mock_get_cursor):

        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_create_conn.return_value.__enter__.return_value = mock_conn
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []

        result = get_yesterday_links_and_titles()
        expected_result = []

        assert result == expected_result
