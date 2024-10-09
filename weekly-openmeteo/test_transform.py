'''Contains tests for transform.py'''
import pytest
from datetime import datetime as dt
from transform import format_time, clean_data, format_data, transform

class TestFormatTime:
    '''Contains tests for format time function'''
    def test_valid_time_string(self):
        '''Tests that a valid input returns the expected object'''
        assert format_time('2024-10-09T15:30') == dt(2024, 10, 9, 15, 30)

    def test_invalid_time_string(self):
        '''Tests that invalid inputs cause errors'''
        with pytest.raises(ValueError):
            format_time('Invalid Time')

    def test_incomplete_time_string(self):
        '''Tests that missing values cause an error'''
        with pytest.raises(ValueError):
            format_time('2024-10-09T15')


class TestCleanData:
    '''Contains tests for clean data function'''
    def test_clean_data(self,valid_unclean_data,valid_cleaned_data):
        '''Tests that a valid input returns the expected result'''

        assert clean_data(valid_unclean_data) == valid_cleaned_data

    def test_missing_keys(self):
        '''Tests that missing keys cause error'''
        county_data = {'daily': {}}
        with pytest.raises(KeyError):
            clean_data(county_data)

    def test_empty_data(self):
        '''Tests that an empty set of values does not raise an error'''
        county_data = {'daily': {'sunrise': [],'sunset': []}}
        expected_result = {'sunrise': [],'sunset': []}
        assert clean_data(county_data) == expected_result


class TestFormatData:
    '''Contains tests for format data function'''
    def test_format_data(self, valid_times,expected_valid_times):
        '''Tests that a valid input returns the expected result'''
        assert format_data(valid_times, 1) == expected_valid_times


    def test_format_data_invalid_date(self,invalid_times):
        '''Tests that an invalid set of data will raise a index error'''
        with pytest.raises(IndexError):
            format_data(invalid_times, 1)

    def test_format_data_mismatched_times(self, valid_times):
        '''Tests that an invalid set of data will raise a index error'''
        invalid_times = valid_times
        invalid_times['sunrise'].pop()
        with pytest.raises(IndexError):
            format_data(invalid_times, 1)


class TestTransform:
    '''Contains tests for the transform function'''

    def test_transform(self, valid_openmeteo_data):
        '''Tests for an expected output from the transform function'''
        data = transform(valid_openmeteo_data)
        assert len(data) == 700
        assert data[-1][0] == 100

    def test_transform_empty_data(self):
        '''Tests that empty data raises an error'''
        with pytest.raises(ValueError):
            transform([])
    
    def test_transform_invalid_data(self,invalid_openmeteo_data):
        with pytest.raises(IndexError):
            transform(invalid_openmeteo_data)