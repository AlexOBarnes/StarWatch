'''Contains tests for the load script in this folder'''
from unittest.mock import patch, MagicMock
from quadhoral_load import truncate_database, load_data


class TestDatabaseFunctions:
    '''Contains tests for database interacting functions'''
    @patch('quadhoral_load.get_connection')
    def test_truncate_database(self, mock_get_connection):
        '''Tests that the truncate database function makes the expected calls'''
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        truncate_database()
        mock_cursor.execute.assert_called_once_with(
            '''DELETE FROM forecast WHERE at >= CURRENT_TIMESTAMP''')
        mock_conn.commit.assert_called_once()

    @patch('quadhoral_load.get_connection')
    @patch('quadhoral_load.execute_values')
    def test_load_data(self, mock_execute_values, mock_get_connection, valid_db_data):
        '''Tests that the load data function calls the expected amount of times'''
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        load_data(valid_db_data)
        mock_conn.commit.assert_called_once()
