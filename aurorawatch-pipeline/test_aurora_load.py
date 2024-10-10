'''Contains tests for the load script'''
from unittest import mock
from aurora_load import load_data


class TestLoadData:
    '''Tests for the load_data function'''
    @mock.patch('aurora_load.get_connection')
    def test_load_data_success(self, mock_get_connection, valid_insertion_data):
        '''Tests that valid data doesn't cause an error'''
        mock_conn = mock.MagicMock()
        mock_cursor = mock.MagicMock()
        mock_get_connection.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        load_data(valid_insertion_data)
        mock_conn.commit.assert_called_once()

    @mock.patch('aurora_load.get_connection')
    def test_load_data_empty_list(self, mock_get_connection):
        '''Tests that empty data doesn't result in an error'''
        mock_conn = mock.MagicMock()
        mock_cursor = mock.MagicMock()
        mock_get_connection.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        load_data(())
        mock_conn.commit.assert_called_once()
