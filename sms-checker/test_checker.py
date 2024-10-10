'''Contains tests for checker script'''
from unittest import mock
from checker import get_subscribers


class TestGetSubscribers:

    @mock.patch('checker.get_connection')
    def test_get_subscribers(self, mock_get_connection,valid_clean_data,valid_queried_data):
        '''Tests that a valid return produces the expected output'''
        mock_conn = mock.MagicMock()
        mock_cursor = mock.MagicMock()
        mock_get_connection.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = valid_queried_data
        result = get_subscribers()
        assert result == valid_clean_data
    
    @mock.patch('checker.get_connection')
    def test_get_subscribers_erroneous_data(self, mock_get_connection,invalid_queried_data,invalid_clean_data):
        '''Tests that an invalid return does not cause an error'''
        mock_conn = mock.MagicMock()
        mock_cursor = mock.MagicMock()
        mock_get_connection.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = invalid_queried_data
        result = get_subscribers()
        assert result == invalid_clean_data

    @mock.patch('checker.get_connection')
    def test_get_subscribers_no_data(self, mock_get_connection):
        '''Tests that an empty return does not cause an error'''
        mock_conn = mock.MagicMock()
        mock_cursor = mock.MagicMock()
        mock_get_connection.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []
        result = get_subscribers()
        expected_result = []
        assert result == expected_result
