'''Contains tests for extract.py'''
#pylint: disable=W0212
import json
from unittest.mock import patch, MagicMock
import pytest
from requests import Response
from extract import request_solar_data,get_county_coordinates,\
                    convert_to_params,get_connection
from api_error import APIError

class TestExtractFunction():
    '''Contains tests for the extract function'''
    @patch('extract.get')
    def test_extract_success(self, mock_get, valid_response,valid_params):
        '''Tests that a 200 status codes results in the return of the data'''
        mock_response = Response()
        mock_response.status_code = 200
        mock_response._content = json.dumps(valid_response).encode('utf-8')
        mock_get.return_value = mock_response

        data = request_solar_data(valid_params)

        assert data == valid_response

    @pytest.mark.parametrize("status_code", [400,401,402,403,404,405,408,500])
    @patch('extract.get')
    def test_extract_unsuccessful_request(self, mock_get, status_code, valid_params):
        """Parameterized test for various unsuccessful API requests."""
        mock_response = Response()
        mock_response.status_code = status_code
        mock_response._content = b''
        mock_get.return_value = mock_response

        with pytest.raises(APIError):
            request_solar_data(valid_params)

    @patch('extract.get')
    def test_extract_value_error(self, mock_get, invalid_response_value, valid_params):
        """Test for erroneous data structure returned by the API."""
        mock_response = Response()
        mock_response.status_code = 200
        mock_response._content = json.dumps(invalid_response_value).encode('utf-8')
        mock_get.return_value = mock_response

        with pytest.raises(ValueError):
            request_solar_data(valid_params)

    @patch('extract.get')
    def test_extract_type_error(self, mock_get, invalid_response_type, valid_params):
        """Test for erroneous data structure returned by the API."""
        mock_response = Response()
        mock_response.status_code = 200
        mock_response._content = json.dumps(invalid_response_type).encode('utf-8')
        mock_get.return_value = mock_response

        with pytest.raises(TypeError):
            request_solar_data(valid_params)

    @patch('extract.get')
    def test_extract_no_data(self, mock_get, valid_params):
        """Test for API response with no data returned."""
        mock_response = Response()
        mock_response.status_code = 200
        mock_response._content = json.dumps({}).encode('utf-8')
        mock_get.return_value = mock_response

        with pytest.raises(TypeError):
            request_solar_data(valid_params)


    @patch('extract.get')
    def test_extract_no_status_code(self, mock_get, valid_params):
        """Test for API response with no status code."""
        mock_response = Response()
        mock_response._content = json.dumps({"daily":
                                {"sunrise": [], "sunset": []}}).encode('utf-8')
        mock_get.return_value = mock_response

        with pytest.raises(APIError):
            request_solar_data(valid_params)


class TestDatabaseFunctions:

    @patch.dict("os.environ", {
        "DB_HOST": "test_host",
        "DB_PORT": "1433",
        "DB_NAME": "test_db",
        "DB_USER": "test_user",
        "DB_PASSWORD": "test_password"
    })
    @patch("extract.get_connection")
    def test_get_county_coordinates(self,mock_get_connection):
        """Test that the get_county_coordinates function returns the correct coordinates."""

        # Mocking the connection and cursor
        mock_connection = MagicMock()
        mock_cursor = MagicMock()

        # Setup mock connection behavior
        mock_get_connection.return_value.__enter__.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        # Setting up the return value for the cursor's fetchall method
        mock_cursor.fetchall.return_value = [
            (0.1278, 51.5074),  # London
            (-3.7038, 40.4168),  # Madrid
            (0.1276, 51.5033)   # Another sample
        ]

        # Call the function being tested
        longitudes, latitudes = get_county_coordinates()

        # Expected output
        expected_longitudes = [0.1278, -3.7038, 0.1276]
        expected_latitudes = [51.5074, 40.4168, 51.5033]

        # Assertions to verify the returned coordinates
        assert longitudes == expected_longitudes
        assert latitudes == expected_latitudes

    def test_convert_to_params(self):
        """Test convert_to_params function"""
        longitudes = [0.1276, -0.1280]
        latitudes = [51.5074, 51.5072]

        expected_params = {
            'latitude': [51.5074, 51.5072],
            'longitude': [0.1276, -0.1280],
            'daily': ["sunrise", "sunset"],
            'timezone': "Europe/London"
        }
        params = convert_to_params(longitudes, latitudes)
        assert params == expected_params
