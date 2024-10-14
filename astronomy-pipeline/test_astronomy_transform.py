'''Tests for the astronomy transform script.'''
# pylint: disable=W0613,R0913,R0917,R0801

from unittest.mock import patch, MagicMock
from datetime import datetime, timezone

import pytest

from astronomy_transform import (transform_astronomy_data, load_from_file,
                                 get_data_into_dataframe, get_body_mapping,
                                 get_constellation_mapping, clean_position_data,
                                 get_moon_df, convert_positions_datetime,
                                 convert_moon_datetime)


class TestLoadFromFile():
    '''Tests for the load from file function.'''

    @patch('json.load')
    @patch('builtins.open')
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

    def test_get_data_into_dataframe_missing_body_positions(self):
        """Test get_data_into_dataframe with missing body positions."""
        with pytest.raises(KeyError):
            get_data_into_dataframe({})


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
    def test_clean_position_data_correct_functions(self, mock_get_constellation_mapping,
                                                   mock_get_body_mapping,
                                                   position_dataframe_example):
        '''Tests that the correct function are called within the function.'''
        clean_position_data(position_dataframe_example)

        assert mock_get_constellation_mapping.called
        assert mock_get_body_mapping.called

    @patch('astronomy_transform.get_body_mapping')
    @patch('astronomy_transform.get_constellation_mapping')
    def test_clean_position_data_returns_list(self, mock_get_constellation_mapping,
                                              mock_get_body_mapping, position_dataframe_example):
        '''Tests that a list object is returned from the function.'''
        result = clean_position_data(position_dataframe_example)

        assert isinstance(result, list)


class TestGetMoonDf():
    '''Tests for the get moon df function.'''

    def test_get_moon_df_returns_list(self):
        '''Tests that a list object is returned from the function.'''
        result = get_moon_df([{'test': 'test'}])

        assert isinstance(result, list)

    def test_get_moon_df_valid_data(self):
        '''Test that the function output matches the expected, 
        with valid phase data.'''
        moon_data = [{'date': '2024-10-10', 'image_url': 'https://example.com/image1.jpg'},
                     {'date': '2024-11-10', 'image_url': 'https://example.com/image2.jpg'}]

        expected_output = [['2024-10-10', 'https://example.com/image1.jpg'],
                           ['2024-11-10', 'https://example.com/image2.jpg']]

        result = get_moon_df(moon_data)

        assert result == expected_output


class TestConvertPositionsDatetime():
    '''Tests for the convert positions datetime function.'''

    def test_convert_positions_datetime_valid_datetime(self):
        '''Test converting valid datetime strings.'''
        position_list = [['2024-10-10T12:30:45.123456+0000', 'position1', 100.0],
                         ['2023-11-11T15:45:30.654321+0000', 'position2', 200.0]]

        expected_output = [[datetime(2024, 10, 10, 12, 30, 45, 123456,
                                     tzinfo=timezone.utc), 'position1', 100.0],
                           [datetime(2023, 11, 11, 15, 45, 30, 654321,
                                     tzinfo=timezone.utc), 'position2', 200.0]]

        result = convert_positions_datetime(position_list)
        assert result == expected_output

    def test_convert_positions_datetime_invalid_datetime_format(self):
        '''Test handling of invalid datetime format strings.'''
        position_list = [['10-10-2024 12:30:45', 'position1', 100.0]]

        with pytest.raises(ValueError):
            convert_positions_datetime(position_list)


class TestConvertMoonDatetime():
    '''Tests for the convert moon datetime function.'''

    def test_convert_moon_datetime_valid_datetime(self):
        '''Test converting valid datetime strings.'''
        position_list = [['2024-10-09', 'position1', 100.0],
                         ['2023-11-09', 'position2', 200.0]]

        expected_output = [[datetime(2024, 10, 9, 0, 0), 'position1', 100.0],
                           [datetime(2023, 11, 9, 0, 0), 'position2', 200.0]]

        result = convert_moon_datetime(position_list)
        assert result == expected_output

    def test_convert_moon_datetime_invalid_datetime_format(self):
        '''Test handling of invalid datetime format strings.'''
        position_list = [['10-10-2024 12:30:45', 'position1', 100.0]]

        with pytest.raises(ValueError):
            convert_moon_datetime(position_list)


class TestTransformAstronomyData():
    '''Tests for the transform astronomy data function.'''

    @patch('astronomy_transform.get_data_into_dataframe')
    @patch('astronomy_transform.clean_position_data')
    @patch('astronomy_transform.convert_positions_datetime')
    @patch('astronomy_transform.get_moon_df')
    @patch('astronomy_transform.convert_moon_datetime')
    def test_transform_astronomy_data_correct_functions(self, mock_convert_moon_datetime,
                                                        mock_get_moon_df,
                                                        mock_convert_positions_datetime,
                                                        mock_clean_position_data,
                                                        mock_get_data_into_dataframe):
        '''Tests that the correct functions are called within the function.'''
        transform_astronomy_data({'moon_phase_urls': 'test'})

        assert mock_clean_position_data.called
        assert mock_convert_moon_datetime.called
        assert mock_get_moon_df.called
        assert mock_convert_positions_datetime.called
        assert mock_get_data_into_dataframe.called

    @patch('astronomy_transform.get_data_into_dataframe')
    @patch('astronomy_transform.clean_position_data')
    @patch('astronomy_transform.convert_positions_datetime')
    @patch('astronomy_transform.get_moon_df')
    @patch('astronomy_transform.convert_moon_datetime')
    def test_transform_astronomy_data_returns_dict(self, mock_convert_moon_datetime,
                                                   mock_get_moon_df,
                                                   mock_convert_positions_datetime,
                                                   mock_clean_position_data,
                                                   mock_get_data_into_dataframe):
        '''Tests that a dict object is returned from the function.'''
        mock_clean_position_data.return_value = MagicMock()
        mock_convert_moon_datetime.return_value = MagicMock()
        mock_get_moon_df.return_value = MagicMock()
        mock_convert_positions_datetime.return_value = MagicMock()
        mock_get_data_into_dataframe.return_value = MagicMock()

        result = transform_astronomy_data({'moon_phase_urls': 'test'})

        assert isinstance(result, dict)

    @patch('astronomy_transform.get_data_into_dataframe')
    @patch('astronomy_transform.clean_position_data')
    @patch('astronomy_transform.convert_positions_datetime')
    @patch('astronomy_transform.get_moon_df')
    @patch('astronomy_transform.convert_moon_datetime')
    def test_transform_astronomy_data_correct_keys(self, mock_convert_moon_datetime,
                                                   mock_get_moon_df,
                                                   mock_convert_positions_datetime,
                                                   mock_clean_position_data,
                                                   mock_get_data_into_dataframe):
        '''Tests that the correct keys are returned from the function.'''
        mock_clean_position_data.return_value = MagicMock()
        mock_convert_moon_datetime.return_value = MagicMock()
        mock_get_moon_df.return_value = MagicMock()
        mock_convert_positions_datetime.return_value = MagicMock()
        mock_get_data_into_dataframe.return_value = MagicMock()

        result = transform_astronomy_data({'moon_phase_urls': 'test'})

        assert 'positions_list' in result
        assert 'moon_phase_list' in result
