'''Contains tests for the image pipeline'''
#pylint: disable=C0121,R0903
from unittest.mock import patch, MagicMock
from datetime import datetime as dt
import pytest
from dashboard.nasa_pipeline import (has_nasa_image,extract_time,get_nasa_image,
    load_image,nasa_pipeline,APIError, get_iss_location)

NASA_API_URL = 'https://api.nasa.gov/planetary/apod?api_key=YOUR_API_KEY'
KEYS = ['data', 'title', 'url']


class TestHasNasaImage:
    '''Contains tests for has nasa image function'''
    @patch('image_pipeline.get_connection')
    def test_has_nasa_image_true(self, mock_get_connection):
        '''Tests that if 1 is returned from database a true value is returned'''
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = [1]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_connection.return_value.__enter__.return_value = mock_conn

        assert has_nasa_image() == True

    @patch('image_pipeline.get_connection')
    def test_has_nasa_image_false(self, mock_get_connection):
        '''Tests that if there are no images in the database a false value is returned'''
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = [0]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_connection.return_value.__enter__.return_value = mock_conn

        assert has_nasa_image() == False


class TestExtractTime:
    '''Contains tests for the extract time function'''
    def test_extract_time_valid(self):
        '''Asserts that a valid string is extracted'''
        time_str = "2024-10-14"
        expected_date = dt(2024, 10, 14)
        assert extract_time(time_str) == expected_date

    def test_extract_time_invalid(self):
        '''Tests that an invalid string causes an error'''
        with pytest.raises(ValueError):
            extract_time("14-10-2024")

class TestGetNasaImage:
    '''Tests for the get nasa image function'''
    @patch('image_pipeline.get')
    @patch.dict('image_pipeline.ENV', {'NASA_API_KEY': 'FAKE_API_KEY'})
    def test_get_nasa_image_successful(self, mock_get):
        '''Tests that the get image function returns the currect values'''
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'date': '2024-10-14',
                                           'title': 'Amazing NASA Image',
                                           'url': 'https://example.com/nasa_image.jpg'}
        mock_get.return_value = mock_response

        result = get_nasa_image()
        assert result == [dt(2024, 10, 14), 'NASA_Amazing NASA Image',
                          'https://example.com/nasa_image.jpg']

    @patch('image_pipeline.get')
    @patch.dict('image_pipeline.ENV', {'NASA_API_KEY': 'FAKE_API_KEY'})
    def test_get_nasa_image_incomplete_data(self, mock_get):
        '''tests that the get nasa image raises an error if there is missing data'''
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'date': '2024-10-14',
                                           'title': 'Amazing NASA Image',
                                           'url': None}
        mock_get.return_value = mock_response

        with pytest.raises(ValueError, match="Could not obtain url"):
            get_nasa_image()

    @patch('image_pipeline.get')
    @patch.dict('image_pipeline.ENV', {'NASA_API_KEY': 'FAKE_API_KEY'})
    def test_get_nasa_image_api_error(self, mock_get):
        '''tests that the get_nasa_image function raises an api error when a request fails'''
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with pytest.raises(APIError, match="Unsuccessful request."):
            get_nasa_image()


class TestLoadImage:
    '''Contains tests for load image function'''
    @patch('image_pipeline.get_connection')
    def test_load_image(self, mock_get_connection):
        '''Tests that the load image function calls the commit function'''
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_connection.return_value.__enter__.return_value = mock_conn
        image_data = [dt(2024, 10, 14), 'NASA_Amazing',
                      'https://example.com/nasa_image.jpg']

        load_image(image_data)
        mock_conn.commit.assert_called_once()


class TestNasaPipeline:
    '''Contains tests for the nasa pipeline function'''
    @patch('image_pipeline.load_image')
    @patch('image_pipeline.get_nasa_image')
    @patch('image_pipeline.has_nasa_image')
    def test_nasa_pipeline_no_image_found(self, mock_has_nasa_image,
                                        mock_get_nasa_image, mock_load_image):
        '''Tests that a valid request ends in the correct functions being called'''
        mock_has_nasa_image.return_value = False
        mock_get_nasa_image.return_value = [dt(2024, 10, 14),
                                            'NASA_Amazing', 'https://example.com/nasa_image.jpg']

        nasa_pipeline()

        mock_get_nasa_image.assert_called_once()
        mock_load_image.assert_called_once()

    @patch('image_pipeline.load_image')
    @patch('image_pipeline.get_nasa_image')
    @patch('image_pipeline.has_nasa_image')
    def test_nasa_pipeline_image_already_exists(self, mock_has_nasa_image,
                                                mock_get_nasa_image, mock_load_image):
        '''Tests that a true response does not call the ETL pipeline'''
        mock_has_nasa_image.return_value = True

        nasa_pipeline()

        mock_get_nasa_image.assert_not_called()
        mock_load_image.assert_not_called()


class TestGetIssLocation:
    '''Contains tests for get iss location'''
    @patch('image_pipeline.get')
    def test_get_iss_location_success(self, mock_get):
        '''Tests that the iss request function returns data in the correct format'''
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'message': 'success',
            'timestamp': 1728908772,
            'iss_position': {'latitude': '46.9566','longitude': '-3.7535'}}
        mock_get.return_value = mock_response
        result = get_iss_location()
        expected_result = {'timestamp': dt(2024,10,14,12,26,12),
            'latitude': '46.9566','longitude': '-3.7535'}

        assert result == expected_result

    @patch('image_pipeline.get')
    def test_get_iss_location_failure(self, mock_get):
        '''Tests whether a returned error triggers an API error in the script'''
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'message': 'error',
            'timestamp': 1728908772,
            'iss_position': {
                'latitude': '46.9566',
                'longitude': '-3.7535'}}
        mock_get.return_value = mock_response

        with pytest.raises(APIError, match='Unsuccessful request.'):
            get_iss_location()

    @patch('image_pipeline.get')
    def test_get_iss_location_http_error(self, mock_get):
        '''Tests that an error code triggers an API error'''
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with pytest.raises(APIError, match='Unsuccessful request.'):
            get_iss_location()
