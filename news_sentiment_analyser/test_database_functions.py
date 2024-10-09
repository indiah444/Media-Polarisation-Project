"""Tests for the database_functions.py file."""
from unittest.mock import patch, MagicMock

from psycopg2.extensions import connection

from database_functions import create_connection, get_topic_names, RealDictCursor


@patch('database_functions.connect')
@patch('database_functions.ENV', {
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


@patch('database_functions.create_connection')
def test_get_topic_names(fake_create_connection):
    """Tests the get_topic_names function."""
    fake_conn = MagicMock()
    fake_cursor = MagicMock()
    fake_create_connection.return_value.__enter__.return_value = fake_conn
    fake_conn.cursor.return_value.__enter__.return_value = fake_cursor
    fake_cursor.fetchall.return_value = [
        {"topic_name": "Dogs"},
        {"topic_name": "Cats"}
    ]
    result = get_topic_names()

    fake_cursor.execute.assert_called_once_with(
        "SELECT topic_name FROM topic;")

    assert result == ["Dogs", "Cats"]
