'''Contains tests for transform script'''
import pytest
from quadhoral_transform import format_time, clean_data, format_data, transform
from datetime import datetime


class TestFormatTime:
    def test_format_time_valid(self):
        '''Test format_time with a valid string'''
        event_time = "2024-10-01T15:30"
        output = datetime(2024, 10, 1, 15, 30)
        assert format_time(event_time) == output

    def test_format_time_invalid_format(self):
        '''Test format_time with an invalid string format'''
        with pytest.raises(ValueError):
            format_time("01-10-2024 15:30")

    def test_format_time_empty_string(self):
        '''Test format_time with an empty string'''
        with pytest.raises(ValueError):
            format_time("")


class TestCleanData:
    def test_clean_data_valid(self, valid_input_data,expected_clean_data):
        '''Test clean_data with valid county data'''
        county_data = valid_input_data[0]
        result = clean_data(county_data)
        result = {k: v[:2] for k, v in result.items()}

        assert result == expected_clean_data

    def test_clean_data_missing_fields(self):
        '''Test clean_data with missing fields in the county data'''
        county_data = {'hourly': {'time': ['2024-10-01T00:00'],
                'temperature_2m': [10]}}
        with pytest.raises(KeyError):
            clean_data(county_data)

    def test_clean_data_empty(self):
        '''Test clean_data with empty county data'''
        county_data = {'hourly': {}}
        with pytest.raises(KeyError):
            clean_data(county_data)


class TestFormatData:
    def test_format_data_valid(self, valid_clean_county_data,expected_formatted_data):
        '''Test format_data with valid clean county data'''
        county_id = 1
        result = format_data(valid_clean_county_data, county_id)
        assert result[:2] == expected_formatted_data

    def test_format_data_incomplete_data(self, incomplete_clean_county_data):
        '''Test format_data with incomplete clean county data'''
        county_id = 1
        with pytest.raises(IndexError):
            format_data(incomplete_clean_county_data, county_id)

    def test_format_data_empty(self, empty_clean_county_data):
        '''Test format_data with empty clean county data'''
        county_id = 1
        result = format_data(empty_clean_county_data, county_id)
        assert result == []


class TestTransform:
    def test_transform_valid(self, valid_input_data):
        '''Test transform with valid input data'''
        result = transform(valid_input_data)
        assert len(result) == 24

    def test_transform_no_data(self):
        '''Test transform with no input data'''
        with pytest.raises(ValueError, match="No data to transform"):
            transform([])

    def test_transform_incomplete_data(self, incomplete_clean_county_data):
        '''Test transform with incomplete input data'''
        input_data = [{'hourly': incomplete_clean_county_data}]
        with pytest.raises(KeyError):
            transform(input_data)
