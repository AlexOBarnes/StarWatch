'''Tests for the astronomy transform script.'''

from unittest.mock import patch, mock_open, MagicMock

import pytest
import pandas as pd

from astronomy_transform import (transform_astronomy_data, load_from_file,
                                 get_data_into_dataframe, get_body_mapping,
                                 get_constellation_mapping, clean_position_data,
                                 get_moon_df, convert_positions_datetime,
                                 convert_moon_datetime)


class TestLoadFromFile():
    '''Tests for the load from file function.'''

    @patch('json.load')
    @patch("builtins.open")
    def test_load_from_file_correct_methods(self, mock_open, mock_load):
        '''Tests that the correct methods and functions are called 
        in the load from file function.'''
        mock_open.return_value.__enter__.return_value = MagicMock()
        mock_load.return_value = {}

        load_from_file('test')

        assert mock_load.called
        assert mock_open.called

    @patch('json.load')
    @patch('builtins.open')
    def test_load_from_file_uses_correct_calls(self, mock_open, mock_load):
        '''Tests that the open method is called with the correct
        values.'''
        mock_open.return_value.__enter__.return_value = MagicMock()
        mock_load.return_value = {}

        load_from_file('test')

        mock_open.assert_called_once_with('test', 'r', encoding='UTF-8')

    @patch('json.load')
    @patch('builtins.open')
    def test_load_from_file_returns_dict(self, mock_open, mock_load):
        '''Tests that a dictionary is returned from the load from file function.'''
        mock_open.return_value.__enter__.return_value = MagicMock()
        mock_load.return_value = {}

        result = load_from_file('test')

        assert isinstance(result, dict)


class TestGetDataIntoDataFrame():
    '''Tests for the get data into dataframe function.'''

    @patch('pandas.concat')
    @patch('pandas.DataFrame')
    def test_get_data_into_dataframe_correct_methods(self, mock_dataframe, mock_concat):
        '''Tests that the correct pandas methods are called when the function runs.'''
        get_data_into_dataframe({'body_positions': {1: {1: 'test'}}})

        assert mock_dataframe.called
        assert mock_concat.called


class TestGetBodyMapping():
    '''Tests for the get body mapping function.'''

    @patch('astronomy_transform.get_db_connection')
    def test_get_body_mapping_correct_methods(self, mock_get_db_connection):
        '''Tests that the correct function and methods are 
        called within the function.'''
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        get_body_mapping()

        assert mock_cursor.execute.called
        assert mock_get_db_connection.called
        assert mock_conn.cursor.called

    @patch('astronomy_transform.get_db_connection')
    def test_get_body_mapping_correct_call(self, mock_get_db_connection):
        '''Tests that the correct input is used for the execute method.'''
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        get_body_mapping()

        mock_cursor.execute.assert_called_once_with(
            'SELECT body_id, body_name from body;')

    @patch('astronomy_transform.get_db_connection')
    def test_get_body_mapping_returns_dict(self, mock_get_db_connection):
        '''Tests that a dict object is returned from the function.'''
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        result = get_body_mapping()

        assert isinstance(result, dict)


class TestGetConstellationMapping():
    '''Tests for the get constellation mapping function.'''

    @patch('astronomy_transform.get_db_connection')
    def test_get_constellation_mapping_correct_methods(self, mock_get_db_connection):
        '''Tests that the correct function and methods are 
        called within the function.'''
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        get_constellation_mapping()

        assert mock_cursor.execute.called
        assert mock_get_db_connection.called
        assert mock_conn.cursor.called

    @patch('astronomy_transform.get_db_connection')
    def test_get_constellation_mapping_correct_call(self, mock_get_db_connection):
        '''Tests that the correct input is used for the execute method.'''
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        get_constellation_mapping()

        mock_cursor.execute.assert_called_once_with(
            'SELECT constellation_id, constellation_short_name from constellation;')

    @patch('astronomy_transform.get_db_connection')
    def test_get_constellation_mapping_returns_dict(self, mock_get_db_connection):
        '''Tests that a dict object is returned from the function.'''
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        result = get_constellation_mapping()

        assert isinstance(result, dict)


class TestCleanPositionData():
    '''Tests for the clean position data function.'''

    @patch('astronomy_transform.get_body_mapping')
    @patch('astronomy_transform.get_constellation_mapping')
    def test_clean_position_data(self, mock_get_constellation_mapping,
                                 mock_get_body_mapping, position_dataframe_example):
        ''''''
        clean_position_data(position_dataframe_example)


class TestGetMoonDf():
    '''Tests for the get moon df function.'''

    def test_get_moon_df(self):
        ''''''
        pass


class TestConvertPositionsDatetime():
    '''Tests for the convert positions datetime function.'''

    def test_convert_positions_datetime(self):
        ''''''
        pass


class TestConvertMoonDatetime():
    '''Tests for the convert moon datetime function.'''

    def test_convert_moon_datetime(self):
        ''''''
        pass


class TestTransformAstronomyData():
    '''Tests for the transform astronomy data function.'''

    def test_transform_astronomy_data(self):
        ''''''
        pass
