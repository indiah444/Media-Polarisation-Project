# pylint: skip-file

from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta

import pandas as pd

from w_db_funcs import get_avg_polarity_last_week, get_weekly_subscribers


class TestGetAvgPolarityLastWeek:

    @patch('w_db_funcs.get_cursor')
    @patch('w_db_funcs.create_connection')
    def test_correct_cursor_call_and_empty_dataframe(self, mock_create_conn, mock_get_cursor):

        last_week = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        today = datetime.now().strftime('%Y-%m-%d')

        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_create_conn.return_value.__enter__.return_value = mock_conn
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.fetchall.return_value = []

        query = """
        SELECT t.topic_name, s.source_name,
        AVG(a.content_polarity_score) AS avg_polarity_score,
        COUNT(a.article_id) AS article_count
        FROM article_topic_assignment ata
        JOIN article a ON ata.article_id = a.article_id
        JOIN topic t ON ata.topic_id = t.topic_id
        JOIN source s ON a.source_id = s.source_id
        WHERE a.date_published BETWEEN %s AND %s
        GROUP BY t.topic_name, s.source_name
        ORDER BY t.topic_name, s.source_name;
    """

        result_df = get_avg_polarity_last_week()

        mock_cursor.execute.assert_called_once_with(query, (last_week, today))
        assert result_df.empty

    @patch('w_db_funcs.get_cursor')
    @patch('w_db_funcs.create_connection')
    def test_output(self, mock_create_conn, mock_get_cursor):

        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_create_conn.return_value.__enter__.return_value = mock_conn
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor

        sample_data = [('Politics', 'Source A', 0.5),
                       ('Sports', 'Source B', 0.2)]
        mock_cursor.fetchall.return_value = sample_data

        result_df = get_avg_polarity_last_week()
        expected_df = pd.DataFrame(sample_data)

        pd.testing.assert_frame_equal(result_df, expected_df)


class TestGetWeeklySubscribers:

    @patch('w_db_funcs.get_cursor')
    @patch('w_db_funcs.create_connection')
    def test_correct_cursor_call_and_empty_data(self, mock_create_conn, mock_get_cursor):

        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_create_conn.return_value.__enter__.return_value = mock_conn
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.fetchall.return_value = []

        query = """
        SELECT subscriber_email 
        FROM subscriber
        WHERE weekly = TRUE
        """

        result = get_weekly_subscribers()

        mock_cursor.execute.assert_called_once_with(query)
        assert len(result) == 0

    @patch('w_db_funcs.get_cursor')
    @patch('w_db_funcs.create_connection')
    def test_with_data(self, mock_create_conn, mock_get_cursor):

        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_create_conn.return_value.__enter__.return_value = mock_conn
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor

        sample_data = [{'subscriber_email': 'user1@example.com'},
                       {'subscriber_email': 'user2@example.com'}]
        mock_cursor.fetchall.return_value = sample_data

        result = get_weekly_subscribers()
        expected_result = ['user1@example.com', 'user2@example.com']

        assert result == expected_result

    @patch('w_db_funcs.get_cursor')
    @patch('w_db_funcs.create_connection')
    def test_no_data(self, mock_create_conn, mock_get_cursor):

        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_create_conn.return_value.__enter__.return_value = mock_conn
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.fetchall.return_value = []
        result = get_weekly_subscribers()
        expected_result = []

        assert result == expected_result
