# pylint: skip-file
"""
Testing dummy data generation
"""

from unittest.mock import patch, MagicMock
from generate_dummy_data import connect


@patch('generate_dummy_data.load_dotenv')
@patch('psycopg2.connect')
def test_connection(mock_connect, mock_load_dotenv):
    '''Tests the connection'''

    mock_connection = MagicMock()
    mock_connect.return_value = mock_connection
    connection = connect()
    mock_load_dotenv.assert_called_once()
    mock_connect.assert_called_once()
    assert connection == mock_connection
