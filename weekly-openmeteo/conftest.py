'''Contains the configurations for the tests in this folder'''
from datetime import datetime as dt
import pytest

@pytest.fixture
def valid_params():
    '''Returns valid parameters'''
    return {'latitude': [],
            'longitude': [],
            "daily": ["sunrise", "sunset"], "timezone": "Europe/London"}

@pytest.fixture
def valid_response():
    """Fixture for valid API response data."""
    return [{
        "daily": {
            "sunrise": ["2024-10-09T07:45", "2024-10-10T07:46"],
            "sunset": ["2024-10-09T18:42", "2024-10-10T18:39"]
        }
    }] * 106

@pytest.fixture
def invalid_response_value():
    """Fixture for invalid API response data."""
    return [{'daily':{
        "sunrise": "not_a_list",
        "sunset": "not_a_list"
    }}]


@pytest.fixture
def invalid_response_type():
    """Fixture for invalid API response data."""
    return {
        "sunrise": "not_a_list",
        "sunset": "not_a_list"
    }


@pytest.fixture
def valid_coords():
    """Fixture for valid coords."""
    return [51.5074, 51.5072], [0.1276, -0.1280]

@pytest.fixture
def valid_unclean_data():
    '''Returns a valid dictionary with solar data'''
    return {'daily': {'sunrise': ['2024-10-09T06:00', '2024-10-10T06:01'],
            'sunset': ['2024-10-09T18:00', '2024-10-10T18:01']}}


@pytest.fixture
def valid_cleaned_data():
    '''Returns a valid dictionary with solar data'''
    return {'sunrise': ['2024-10-09T06:00', '2024-10-10T06:01'],
        'sunset': ['2024-10-09T18:00', '2024-10-10T18:01']}


@pytest.fixture
def valid_times():
    '''Returns valid solar data'''
    return {'sunrise': ['2024-10-09T06:00', '2024-10-10T06:01', '2024-10-11T06:02',
                        '2024-10-12T06:03', '2024-10-13T06:04', '2024-10-14T06:05',
                         '2024-10-15T06:06'],
            'sunset': ['2024-10-09T18:00', '2024-10-10T18:01', '2024-10-11T18:02',
                        '2024-10-12T18:03', '2024-10-13T18:04', '2024-10-14T18:05',
                          '2024-10-15T18:06']}


@pytest.fixture
def expected_valid_times():
    '''Returns valid solar data after it has been cleaned'''
    return [
        [1, dt(2024, 10, 9, 6, 0), dt(2024, 10, 9, 18, 0)],
        [1, dt(2024, 10, 10, 6, 1), dt(2024, 10, 10, 18, 1)],
        [1, dt(2024, 10, 11, 6, 2), dt(2024, 10, 11, 18, 2)],
        [1, dt(2024, 10, 12, 6, 3), dt(2024, 10, 12, 18, 3)],
        [1, dt(2024, 10, 13, 6, 4), dt(2024, 10, 13, 18, 4)],
        [1, dt(2024, 10, 14, 6, 5), dt(2024, 10, 14, 18, 5)],
        [1, dt(2024, 10, 15, 6, 6), dt(2024, 10, 15, 18, 6)]
    ]


@pytest.fixture
def invalid_times():
    '''Returns an invalid time set'''
    return {'sunrise': ['2024-10-09T06:00', '2024-10-10T18:01'],
        'sunset': ['2024-10-09T18:00', '2024-10-10T18:01']}

@pytest.fixture
def valid_openmeteo_data():
    '''Returns a sample dataset akin to openmeteo'''
    return [{'daily': {
            'sunrise': ['2024-10-09T06:00', '2024-10-10T06:01', '2024-10-11T06:02', 
                        '2024-10-12T06:03', '2024-10-13T06:04', '2024-10-14T06:05', 
                        '2024-10-15T06:06'],
            'sunset': ['2024-10-09T18:00', '2024-10-10T18:01', '2024-10-11T18:02', 
                       '2024-10-12T18:03', '2024-10-13T18:04', '2024-10-14T18:05', 
                       '2024-10-15T18:06']}}]*100


@pytest.fixture
def invalid_openmeteo_data():
    '''Returns a sample dataset akin to openmeteo'''
    return [{'daily': {
            'sunrise': ['2024-10-09T06:00', '2024-10-10T06:01', '2024-10-11T06:02',
                        '2024-10-12T06:03', '2024-10-13T06:04', '2024-10-14T06:05'],
            'sunset': ['2024-10-09T18:00', '2024-10-10T18:01', '2024-10-11T18:02',
                       '2024-10-12T18:03', '2024-10-13T18:04', '2024-10-14T18:05',
                       '2024-10-15T18:06']}}]*100
