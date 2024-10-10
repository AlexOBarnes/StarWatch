"""Conftest file for weekly astronomy data pipeline."""

import pytest


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
                    "degrees": "-23.43",
                    "string": "-24° 34' 12\""
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
        "constellation": "sgr"
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
                    {"cells": [1, 2, 3]},
                    {"cells": [1, 2, 3]}
                ]
            }
        }
    }
