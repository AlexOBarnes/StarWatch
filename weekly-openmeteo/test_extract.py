'''Contains tests for extract.py'''
import json
from unittest.mock import patch
import pytest
from requests import Response
from extract import extract
from api_error import APIError


class TestExtractFunction():

    @patch('extract.get')
    def test_extract_success(self, mock_get, valid_response):
        '''Tests that a 200 status codes results in the return of the data'''
        mock_response = Response()
        mock_response.status_code = 200
        mock_response._content = json.dumps(valid_response).encode('utf-8')
        mock_get.return_value = mock_response

        data = extract()

        assert data == valid_response

    @pytest.mark.parametrize("status_code", [400,401,402,403,404,405,408,500])
    @patch('extract.get')
    def test_extract_unsuccessful_request(self,mock_get,status_code):
        """Parameterized test for various unsuccessful API requests."""
        mock_response = Response()
        mock_response.status_code = status_code
        mock_response._content = b''
        mock_get.return_value = mock_response

        with pytest.raises(APIError) as exc_info:
            extract()

    @patch('extract.get')
    def test_extract_value_error(self,mock_get,invalid_response_value):
        """Test for erroneous data structure returned by the API."""
        mock_response = Response()
        mock_response.status_code = 200
        mock_response._content = json.dumps(invalid_response_value).encode('utf-8')
        mock_get.return_value = mock_response

        with pytest.raises(ValueError):
            extract()
    
    @patch('extract.get')
    def test_extract_type_error(self,mock_get, invalid_response_type):
        """Test for erroneous data structure returned by the API."""
        mock_response = Response()
        mock_response.status_code = 200
        mock_response._content = json.dumps(invalid_response_type).encode('utf-8')
        mock_get.return_value = mock_response

        with pytest.raises(TypeError):
            extract()

    @patch('extract.get')
    def test_extract_no_data(self,mock_get):
        """Test for API response with no data returned."""
        mock_response = Response()
        mock_response.status_code = 200
        mock_response._content = json.dumps({}).encode('utf-8')
        mock_get.return_value = mock_response

        with pytest.raises(TypeError):
            extract()


    @patch('extract.get')
    def test_extract_no_status_code(self,mock_get):
        """Test for API response with no status code."""
        mock_response = Response()
        mock_response._content = json.dumps({"daily": {"sunrise": [], "sunset": []}}).encode('utf-8')
        mock_get.return_value = mock_response

        with pytest.raises(APIError) as exc_info:
            extract()
