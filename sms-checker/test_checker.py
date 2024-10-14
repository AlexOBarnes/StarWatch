'''Contains tests for checker script'''
from unittest import mock
import pytest
from checker import get_subscribers_bodies,get_subscribers_aurora,\
                    get_aurora_regions


class TestGetSubscribers:
    '''Tests for get subscriber function'''
    @mock.patch('checker.get_connection')
    def test_get_subscribers_bodies(self, mock_get_connection,valid_clean_data,valid_queried_data):
        '''Tests that a valid return produces the expected output'''
        mock_conn = mock.MagicMock()
        mock_cursor = mock.MagicMock()
        mock_get_connection.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = valid_queried_data
        result = get_subscribers_bodies()
        assert result == valid_clean_data

    @mock.patch('checker.get_connection')
    def test_get_subscribers_bodies_erroneous_data(self, mock_get_connection,
                                            invalid_queried_data,invalid_clean_data):
        '''Tests that an invalid return does not cause an error'''
        mock_conn = mock.MagicMock()
        mock_cursor = mock.MagicMock()
        mock_get_connection.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = invalid_queried_data
        result = get_subscribers_bodies()
        assert result == invalid_clean_data

    @mock.patch('checker.get_connection')
    def test_get_subscribers_bodies_no_data(self, mock_get_connection):
        '''Tests that an empty return does not cause an error'''
        mock_conn = mock.MagicMock()
        mock_cursor = mock.MagicMock()
        mock_get_connection.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []
        result = get_subscribers_bodies()
        expected_result = []
        assert result == expected_result


    @mock.patch('checker.get_aurora_regions')
    @mock.patch('checker.get_connection')
    def test_get_subscribers_aurora_green_alert(self, mock_get_connection, mock_get_aurora_regions):
        '''Test that green aurora alert returns None for subscribers'''
        mock_get_aurora_regions.return_value = ['Green', 'Safe']
        result = get_subscribers_aurora()
        assert result == (None, None)

    @mock.patch('checker.get_aurora_regions')
    @mock.patch('checker.get_connection')
    def test_get_subscribers_aurora_yellow_alert(self, mock_get_connection, mock_get_aurora_regions, valid_queried_data, valid_clean_aurora_data):
        '''Test that yellow aurora alert returns the expected subscriber list'''
        mock_get_aurora_regions.return_value = ['Yellow', 'Moderate alert']
        mock_conn = mock.MagicMock()
        mock_cursor = mock.MagicMock()
        mock_get_connection.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = valid_queried_data
        result = get_subscribers_aurora()
        assert result[0] == valid_clean_aurora_data
        assert result[1] == ['Yellow', 'Moderate alert']

    @mock.patch('checker.get_aurora_regions')
    @mock.patch('checker.get_connection')
    def test_get_subscribers_aurora_no_data(self, mock_get_connection, mock_get_aurora_regions):
        '''Tests that no data is handled correctly for aurora subscribers'''
        mock_get_aurora_regions.return_value = ['Yellow', 'Moderate alert']
        mock_conn = mock.MagicMock()
        mock_cursor = mock.MagicMock()
        mock_get_connection.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []
        result = get_subscribers_aurora()
        expected_result = ([], ['Yellow', 'Moderate alert'])
        assert result == expected_result


class TestGetAuroraRegions:
    '''Contains tests for the get aurora regions function'''
    @mock.patch('checker.get_connection')
    def test_get_aurora_regions_success(self, mock_get_connection):
        '''Tests that a successful call is handled correctly'''
        mock_conn = mock.MagicMock()
        mock_cursor = mock.MagicMock()
        mock_get_connection.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            ('Green', 'Moderate alert')]
        result = get_aurora_regions()
        mock_cursor.execute.assert_called_once()
        assert result == ('Green', 'Moderate alert')

    @mock.patch('checker.get_connection')
    def test_get_aurora_regions_no_data(self, mock_get_connection):
        '''Tests that an unsuccessful call raises an error'''
        mock_conn = mock.MagicMock()
        mock_cursor = mock.MagicMock()
        mock_get_connection.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []
        with pytest.raises(IndexError):
            get_aurora_regions()

    @mock.patch('checker.get_connection')
    def test_get_aurora_regions_exception(self, mock_get_connection):
        '''Tests that an unsuccessful call raises an error'''
        mock_conn = mock.MagicMock()
        mock_cursor = mock.MagicMock()
        mock_get_connection.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.execute.side_effect = Exception("Database error")
        with pytest.raises(Exception):
            get_aurora_regions()
