'''Contains tests for the extract script in this folder'''
import os
from unittest.mock import patch, MagicMock
import pytest
from quadhoral_extract import get_county_coordinates, convert_to_params,\
                              request_weather_data, extract
from api_error import APIError

class TestGetCountyCoordinates:
    '''Contains tests for get county coordinate functions'''
    @patch('quadhoral_extract.get_connection')
    def test_get_county_coordinates_valid(self,mock_get_connection,valid_coords):
        """Test getting valid county coordinates."""
        mock_cursor = MagicMock()
        mock_get_connection.return_value.__enter__.return_value.\
            cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = valid_coords
        longitudes, latitudes = get_county_coordinates()
        assert longitudes == [1.0, -1.0]
        assert latitudes == [51.0, 52.0]


    @patch('quadhoral_extract.get_connection')
    def test_get_county_coordinates_empty(self, mock_conn):
        """Test handling empty county coordinates."""
        mock_cursor = MagicMock()
        mock_conn.return_value.__enter__.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []
        longitudes, latitudes = get_county_coordinates()

        assert longitudes == []
        assert latitudes == []

    @patch('quadhoral_extract.get_connection')
    def test_get_county_coordinates_error(self, mock_conn):
        """Test database error when getting county coordinates."""
        mock_conn.side_effect = Exception("Database connection error")

        with pytest.raises(Exception, match="Database connection error"):
            get_county_coordinates()


class TestConvertToParams:
    '''Contains tests for convert to params function'''
    def test_convert_to_params_valid(self,clean_valid_coord):
        """Test valid parameter conversion."""
        params = convert_to_params(clean_valid_coord,clean_valid_coord)
        assert params['latitude'] == [1.0, 51.0]
        assert params['longitude'] == [1.0, 51.0]
        assert 'hourly' in params
        assert params['forecast_days'] == 1

    def test_convert_to_params_invalid(self):
        """Test invalid parameter conversion raises TypeError."""
        with pytest.raises(TypeError, match="Queried data is wrong datatype"):
            convert_to_params(1.0, 51.0)

    def test_convert_to_params_empty(self):
        """Test empty parameter conversion."""
        params = convert_to_params([], [])
        assert params['latitude'] == []
        assert params['longitude'] == []


class TestRequestWeatherData:
    '''Contains tests for request weather data'''
    @patch('quadhoral_extract.get')
    def test_request_weather_data_valid(self, mock_get,valid_json_data):
        """Test successful weather data request."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = valid_json_data
        mock_get.return_value = mock_response

        params = {'latitude': [1.0], 'longitude': [51.0]}
        data = request_weather_data(params)

        assert len(data) == 106

    @patch('quadhoral_extract.get')
    def test_request_weather_data_error(self, mock_get):
        """Test request returns unsuccessful status code."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        with pytest.raises(APIError, match="Unsuccessful request."):
            request_weather_data({})

    @patch('quadhoral_extract.get')
    def test_request_weather_data_missing_values(self, mock_get,invalid_json_data):
        """Test request returns data with missing values."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = invalid_json_data
        mock_get.return_value = mock_response

        with pytest.raises(ValueError, match="Missing Values in returned data"):
            request_weather_data({})


class TestExtract:
    '''Contains tests for extract function'''
    @patch('quadhoral_extract.get_county_coordinates')
    @patch('quadhoral_extract.convert_to_params')
    @patch('quadhoral_extract.request_weather_data')
    @patch.dict(os.environ, {"DB_NAME": "test_db", "DB_USER": "test_user", "DB_PASS": "test_pass"})
    def test_extract_valid(self, mock_weather_data, mock_params,
                                           mock_coords, valid_json_data):
        """Test successful data extraction pipeline."""
        mock_coords.return_value = ([1.0], [51.0])
        mock_params.return_value = {'latitude': [1.0], 'longitude': [51.0]}
        mock_weather_data.return_value = valid_json_data

        result = extract()
        assert len(result) == 106

    @patch('quadhoral_extract.get_county_coordinates')
    @patch.dict(os.environ, {"DB_NAME": "test_db", "DB_USER": "test_user", "DB_PASS": "test_pass"})
    def test_extract_db_error(self, mock_coords):
        """Test extraction pipeline fails due to DB connection."""
        mock_coords.side_effect = Exception("Database connection error")

        with pytest.raises(Exception, match="Database connection error"):
            extract()
