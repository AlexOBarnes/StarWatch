'''Contains fixtures for this files tests'''
import pytest
from datetime import datetime as dt

@pytest.fixture
def valid_clean_data():
    '''Returns the expected data shape after cleaning'''
    return [{'user': 'davidjohnson', 'phone': None, 
             'email': 'davidjohnson@example.com',
             'body': 'Venus', 'time': dt(2024, 10, 1, 12, 30)},
            {'user': 'johndoe', 'phone': '+12345678901', 
             'email': 'johndoe@example.com',
             'body': 'Mars', 'time': dt(2024, 10, 1, 15, 30)}]


@pytest.fixture
def valid_queried_data():
    '''Returns the data stored in the database'''
    return [('davidjohnson', None, 'davidjohnson@example.com',
            'Venus', dt(2024, 10, 1, 12, 30)),
            ('johndoe', '+12345678901', 'johndoe@example.com',
            'Mars', dt(2024, 10, 1, 15, 30))]

@pytest.fixture
def invalid_clean_data():
    '''Returns the expected data shape after cleaning for invalid_queried data'''
    return [{'user': 'davidjohnson', 'phone': None,
            'email': None, 'body': 'Venus', 'time': None},
            {'user': 'johndoe', 'phone': '+12345678901',
            'email': None, 'body': 'Mars', 'time': None}]


@pytest.fixture
def invalid_queried_data():
    '''Returns the invalid data in the correct shape'''
    return [('davidjohnson', None, None, 'Venus', None),
        ('johndoe', '+12345678901', None, 'Mars', None)]
