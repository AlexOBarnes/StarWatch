"""Conftest file for weekly astronomy data pipeline."""
# pylint: disable=R0801

import pytest
import pandas as pd


@pytest.fixture
def sample_raw_body_data():
    """Sample body result data."""

    output = {
        "date": "2020-12-20T09:00:00.000-05:00",
        "id": "sun",
        "name": "Sun",
        "distance": {
            "fromEarth": {
                "au": "0.98378",
                "km": "147171382.76144"
            }
        },
        "position": {
            "horizontal": {
                "altitude": {
                    "degrees": "10.04",
                    "string": "10° 2' 24\""
                },
                "azimuth": {
                    "degrees": "131.21",
                    "string": "131° 12' 36\""
                }
            },
            "horizonal": {
                "altitude": {
                    "degrees": "10.04",
                    "string": "10° 2' 24\""
                },
                "azimuth": {
                    "degrees": "131.21",
                    "string": "131° 12' 36\""
                }
            },
            "equatorial": {
                "rightAscension": {
                    "hours": "17.92",
                    "string": "17h 55m 12s"
                },
                "declination": {
                    "degrees": "23.43",
                    "string": "24° 34' 12\""
                }
            },
            "constellation": {
                "id": "sgr",
                "short": "Sgr",
                "name": "Sagittarius"
            }
        }
    }

    return output


@pytest.fixture
def sample_filtered_body_data():
    """Sample refined body position data."""

    data = {
        "timestamp": "2020-12-20T09:00:00.000-05:00",
        "body_name": "sun",
        "distance_km": "147171382.76144",
        "azimuth": "131.21",
        "altitude": "10.04",
        "constellation_name": "sgr"
    }

    return data


@pytest.fixture
def sample_moon_urls():
    """Example moon urls."""

    data = [
        {
            "day": "today",
            "url": "fake_url1"
        },
        {
            "day": "today",
            "url": "fake_url1"
        }
    ]

    return data


@pytest.fixture
def sample_raw_positions():
    """Fake sample of raw body position data."""

    return {
        "data": {
            "table": {
                "rows": [
                    {"cells": [
                        {"position": {
                            "horizontal": {
                                "altitude": {
                                    "degrees": "23.5"
                                }
                            }
                        }}
                    ]}
                ]
            }
        }
    }


@pytest.fixture
def upload_body_data_query():
    '''Body data sql query for testing.'''
    q_str = """
                INSERT INTO body_assignment
                (at, distance_km, azimuth, altitude, region_id, body_id, constellation_id)
                VALUES
                %s"""

    return q_str


@pytest.fixture
def upload_moon_data_query():
    '''Moon phase data sql query for testing.'''
    q_str = """
                INSERT INTO image
                (image_date, image_url, region_id, constellation_id, image_name)
                VALUES
                %s"""

    return q_str


@pytest.fixture
def astronomy_data_dict():
    '''Test dictionary for testing the upload astronomy data.'''
    astronomy_data = {'positions_list': [
        'positions'], 'moon_phase_list': ['moon'],
        'star_chart_list': ['24-03-03']}

    return astronomy_data


@pytest.fixture
def position_dataframe_example():
    '''Test dataframe for testing the cleaning of position data.'''
    data = {
        "body_name": ["mars", "earth", "jupiter"],
        "constellation_name": ["Orion", "Andromeda", "Cassiopeia"],
        "distance_km": ["50000", "100000", "200000"],
        "azimuth": ["30", "60", "90"],
        "altitude": ["10", "20", "30"]
    }

    return pd.DataFrame(data)
