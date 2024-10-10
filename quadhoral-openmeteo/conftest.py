'''Contains the configuration for the tests in this file'''
import pytest

@pytest.fixture
def valid_coords():
    '''Returns valid set of coordinates'''
    return [(1.0, 51.0),(-1.0, 52.0)]


@pytest.fixture
def clean_valid_coord():
    '''Returns valid list of coordinates'''
    return [1.0, 51.0]


@pytest.fixture
def valid_json_data():
    '''Returns an example data from API'''
    return [{'hourly': {'temperature_2m': [15], 
            'precipitation_probability': [20], 
            'precipitation': [1], 
            'cloud_cover': [30], 
            'visibility': [10]}}] * 106


@pytest.fixture
def invalid_json_data():
    '''Returns an example data from API that is invalid'''
    return [{'hourly': {'temperature_2m': [], 
            'precipitation_probability': [], 'precipitation': [],
              'cloud_cover': [], 'visibility': []}}] * 106
