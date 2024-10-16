# pylint: skip-file

"""Tests for db_functions.py script."""

from unittest.mock import patch, MagicMock

import pandas as pd
from psycopg2.extensions import connection

from db_functions import (create_connection, get_topic_names, get_topic_dict, get_scores_topic,
                          get_average_score_per_source_for_a_topic, get_title_and_content_data_for_a_topic,
                          get_subscriber_emails, updates_subscriber, add_new_subscriber,
                          remove_subscription, get_avg_polarity_all_topics, RealDictCursor)


@patch('db_functions.connect')
@patch('db_functions.ENV', {
    "DB_NAME": "test_db",
    "DB_USER": "test_user",
    "DB_HOST": "test_host",
    "DB_PASSWORD": "test_password",
    "DB_PORT": "5432"
})
def test_create_connection(fake_connect):
    """Tests the create_connection function."""
    fake_conn = MagicMock(spec=connection)
    fake_connect.return_value = fake_conn
    conn = create_connection()

    fake_connect.assert_called_once_with(
        dbname="test_db",
        user="test_user",
        host="test_host",
        password="test_password",
        port="5432",
        cursor_factory=RealDictCursor
    )
    assert conn == fake_conn


@patch('db_functions.create_connection')
def test_get_topic_names(fake_create_connection):
    """Test get_topic_names function."""
    fake_conn = MagicMock()
    fake_cursor = MagicMock()
    fake_create_connection.return_value.__enter__.return_value = fake_conn
    fake_conn.cursor.return_value.__enter__.return_value = fake_cursor
    fake_cursor.fetchall.return_value = [
        {'topic_name': 'Technology'}, {'topic_name': 'Health'}]
    result = get_topic_names()

    fake_create_connection.assert_called_once()
    assert result == ['Technology', 'Health']


@patch('db_functions.create_connection')
def test_get_topic_dict(fake_create_connection):
    """Test get_topic_dict function."""
    fake_conn = MagicMock()
    fake_cursor = MagicMock()
    fake_create_connection.return_value.__enter__.return_value = fake_conn
    fake_conn.cursor.return_value.__enter__.return_value = fake_cursor
    fake_cursor.fetchall.return_value = [{'topic_name': 'Technology', 'topic_id': 1},
                                         {'topic_name': 'Health', 'topic_id': 2}]
    result = get_topic_dict()

    fake_create_connection.assert_called_once()
    assert result == {'Technology': 1, 'Health': 2}


@patch('db_functions.create_connection')
def test_get_scores_topic(fake_create_connection):
    """Test get_scores_topic function."""
    fake_conn = MagicMock()
    fake_cursor = MagicMock()
    fake_create_connection.return_value.__enter__.return_value = fake_conn
    fake_conn.cursor.return_value.__enter__.return_value = fake_cursor
    fake_cursor.fetchall.return_value = [
        {'topic_name': 'Technology', 'source_name': 'Source A', 'content_polarity_score': 0.5,
            'title_polarity_score': 0.3, 'date_published': '2023-01-01'}
    ]
    result = get_scores_topic('Technology')

    fake_create_connection.assert_called_once()
    assert result == [{'topic_name': 'Technology', 'source_name': 'Source A',
                       'content_polarity_score': 0.5, 'title_polarity_score': 0.3, 'date_published': '2023-01-01'}]


@patch('db_functions.create_connection')
def test_get_average_score_per_source_for_a_topic(fake_create_connection):
    """Test get_average_score_per_source_for_a_topic function."""
    fake_conn = MagicMock()
    fake_cursor = MagicMock()
    fake_create_connection.return_value.__enter__.return_value = fake_conn
    fake_conn.cursor.return_value.__enter__.return_value = fake_cursor
    fake_cursor.fetchall.return_value = [
        {'source_name': 'Source A', 'avg_polarity_score': 0.5, 'article_count': 10}
    ]
    result = get_average_score_per_source_for_a_topic(1)

    fake_create_connection.assert_called_once()
    expected_df = pd.DataFrame(
        [{'source_name': 'Source A', 'avg_polarity_score': 0.5, 'article_count': 10}])
    pd.testing.assert_frame_equal(result, expected_df)


@patch('db_functions.create_connection')
def test_get_title_and_content_data_for_a_topic(fake_create_connection):
    """Test get_title_and_content_data_for_a_topic function."""
    fake_conn = MagicMock()
    fake_cursor = MagicMock()
    fake_create_connection.return_value.__enter__.return_value = fake_conn
    fake_conn.cursor.return_value.__enter__.return_value = fake_cursor
    fake_cursor.fetchall.return_value = [
        {'article_title': 'Article 1', 'title_polarity_score': 0.2,
            'content_polarity_score': 0.5, 'source_name': 'Source A'}
    ]
    result = get_title_and_content_data_for_a_topic(1)

    fake_create_connection.assert_called_once()
    expected_df = pd.DataFrame([{'article_title': 'Article 1', 'title_polarity_score': 0.2,
                               'content_polarity_score': 0.5, 'source_name': 'Source A'}])
    pd.testing.assert_frame_equal(result, expected_df)


@patch('db_functions.create_connection')
def test_get_subscriber_emails(fake_create_connection):
    """Test get_subscriber_emails function."""
    fake_conn = MagicMock()
    fake_cursor = MagicMock()
    fake_create_connection.return_value.__enter__.return_value = fake_conn
    fake_conn.cursor.return_value.__enter__.return_value = fake_cursor
    fake_cursor.fetchall.return_value = [
        {'subscriber_email': 'test@example.com'}]
    result = get_subscriber_emails()

    fake_create_connection.assert_called_once()
    assert result == ['test@example.com']


@patch('db_functions.create_connection')
def test_updates_subscriber(fake_create_connection):
    """Test updates_subscriber function."""
    fake_conn = MagicMock()
    fake_cursor = MagicMock()
    fake_create_connection.return_value.__enter__.return_value = fake_conn
    fake_conn.cursor.return_value.__enter__.return_value = fake_cursor
    updates_subscriber('John', 'Doe', 'john@example.com', True, False)

    fake_create_connection.assert_called_once()
    fake_cursor.execute.assert_called_once()
    fake_conn.commit.assert_called_once()


@patch.dict('os.environ', {
    'DB_NAME': 'test_db',
    'DB_USER': 'test_user',
    'DB_HOST': 'localhost',
    'DB_PASSWORD': 'password',
    'DB_PORT': '5432'
})
@patch('db_functions.create_connection')
@patch('db_functions.check_and_verify_email')
def test_add_new_subscriber(fake_check_and_verify_email, fake_create_connection):
    """Test add_new_subscriber function."""
    fake_conn = MagicMock()
    fake_cursor = MagicMock()
    fake_create_connection.return_value.__enter__.return_value = fake_conn
    fake_conn.cursor.return_value.__enter__.return_value = fake_cursor
    add_new_subscriber('John', 'Doe', 'john@example.com', True, False)

    fake_check_and_verify_email.assert_called_once_with(
        'john@example.com')
    fake_cursor.execute.assert_called_once()
    fake_conn.commit.assert_called_once()


@patch('db_functions.create_connection')
def test_remove_subscription(fake_create_connection):
    """Test remove_subscription function."""
    fake_conn = MagicMock()
    fake_cursor = MagicMock()
    fake_create_connection.return_value.__enter__.return_value = fake_conn
    fake_conn.cursor.return_value.__enter__.return_value = fake_cursor
    remove_subscription('john@example.com')

    fake_create_connection.assert_called_once()
    fake_cursor.execute.assert_called_once()


@patch('db_functions.create_connection')
def test_get_avg_polarity_all_topics(fake_create_connection):
    """Test get_avg_polarity_all_topics function."""
    fake_conn = MagicMock()
    fake_cursor = MagicMock()
    fake_create_connection.return_value.__enter__.return_value = fake_conn
    fake_conn.cursor.return_value.__enter__.return_value = fake_cursor
    fake_cursor.fetchall.return_value = [
        {'topic_name': 'Technology', 'source_name': 'Source A',
            'avg_polarity_score': 0.5, 'article_count': 10}
    ]
    result = get_avg_polarity_all_topics()

    fake_create_connection.assert_called_once()
    expected_df = pd.DataFrame(
        [{'topic_name': 'Technology', 'source_name': 'Source A', 'avg_polarity_score': 0.5, 'article_count': 10}])
    pd.testing.assert_frame_equal(result, expected_df)
