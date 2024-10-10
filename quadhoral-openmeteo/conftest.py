'''Contains the configuration for the tests in this file'''
from datetime import datetime as dt
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


@pytest.fixture
def valid_clean_county_data():
    '''Returns valid clean county data'''
    return {
        'time': [f'2024-10-01T{i:02d}:00' for i in range(24)],
        'temp': [10 + i for i in range(24)],
        'prob': [20 + i for i in range(24)],
        'precip': [0.1 * i for i in range(24)],
        'clouds': [50 + i for i in range(24)],
        'visibility': [10000 - (i * 100) for i in range(24)]
    }

@pytest.fixture
def incomplete_clean_county_data():
    '''Returns incomplete clean county data'''
    return {
        'time': ['2024-10-01T00:00'],
        'temp': [10],
        'prob': [],
        'precip': [0.0],
        'clouds': [50],
        'visibility': [10000]
    }


@pytest.fixture
def empty_clean_county_data():
    '''Returns empty clean county data'''
    return {
        'time': [],
        'temp': [],
        'prob': [],
        'precip': [],
        'clouds': [],
        'visibility': []
    }


@pytest.fixture
def valid_input_data():
    '''Returns valid input data'''
    return [{
        'hourly': {
            'time': [f'2024-10-01T{i:02d}:00' for i in range(24)],
            'temperature_2m': [10 + i for i in range(24)],
            'precipitation_probability': [20 + i for i in range(24)],
            'precipitation': [0.1 * i for i in range(24)],
            'cloud_cover': [50 + i for i in range(24)],
            'visibility': [10000 - (i * 100) for i in range(24)]}}]

@pytest.fixture
def expected_clean_data():
    '''Returns clean data that matches previous fixtures'''
    return {'time': ['2024-10-01T00:00', '2024-10-01T01:00'],
        'temp': [10, 11],'prob': [20, 21],'precip': [0.0, 0.1],
        'clouds': [50, 51],'visibility': [10000, 9900]}

@pytest.fixture
def expected_formatted_data():
    '''Returns formatted data that matches previous fixtures'''
    return [[1, dt(2024, 10, 1, 0, 0), 10, 20, 0.0, 50, 10000],
            [1, dt(2024, 10, 1, 1, 0), 11, 21, 0.1, 51, 9900]]


@pytest.fixture
def valid_db_data():
    '''Returns a valid dataset for the database'''
    return [[1, '2024-10-01T10:00', 15.0, 20, 0.1, 30, 10000],
    [2, '2024-10-01T11:00', 16.0, 25, 0.2, 35, 9500]]
