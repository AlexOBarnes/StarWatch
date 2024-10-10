'''Contains the configurations for the tests in this folder'''
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
    """Fixture for invalid API response data."""
    return [51.5074, 51.5072], [0.1276, -0.1280]
