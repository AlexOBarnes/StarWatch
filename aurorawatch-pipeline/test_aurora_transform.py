'''Test file for the AuroraWatch extract script.'''
# pylint: disable=W0212

from unittest.mock import patch
from datetime import datetime as dt

import pytest

from aurora_transform import get_colour_id, get_current_datetime, transform


class TestGetColourID():
    '''Tests for the get colour id function.'''

    @pytest.mark.parametrize('colour', [('green'), ('   green  '),
                                        ('GREEN'), ('Green')])
    def test_get_colour_id_success(self, colour):
        '''Tests that a colour id int is returned successfully given a correct string,
        no matter the formatting.'''
        result = get_colour_id(colour)

        assert result == 1

    @pytest.mark.parametrize('colour', [(1), (['list', 'test']),
                                        ((1, 2)), ({}), (1.9)])
    def test_get_colour_id_invalid_input(self, colour):
        '''Tests that a non-string object results in a TypeError.'''
        with pytest.raises(TypeError) as err:
            get_colour_id(colour)

        assert err.value.args[0] == 'The colour must be given in string format.'

    @pytest.mark.parametrize('colour', [('gren'), ('blue'), ('test')])
    def test_get_colour_id_invalid_colour(self, colour):
        '''Tests that if a colour is not found in the available alert
        colours, an error is raised.'''
        with pytest.raises(KeyError) as err:
            get_colour_id(colour)

        assert err.value.args[0] == f'No colour ID found for colour: {colour}'


class TestGetCurrentDatetime():
    '''Tests for the get current datetime function.'''

    def test_get_current_datetime_success(self):
        '''Tests that a string is returned from get current datetime.'''
        result = get_current_datetime()

        assert isinstance(result, str)

    def test_get_current_datetime_correct_format(self):
        '''Tests that the sting returned is in the correct format by turning it back
        to a datetime object.'''
        result = get_current_datetime()

        converted_result = dt.strptime(result, "%Y-%m-%d %H:%M:%S")

        assert isinstance(converted_result, dt)


class TestTransform():
    '''Tests for the transform function.'''

    @patch('aurora_transform.get_colour_id')
    @patch('aurora_transform.get_current_datetime')
    def test_transform_calls_success(self, mock_get_current_datetime, mock_get_colour_id):
        '''Tests that transform returns a correct tuple.'''
        mock_get_colour_id.return_value = 1
        mock_get_current_datetime.return_value = '2024-10-07 08:15:30'

        result = transform('')

        assert result == ('2024-10-07 08:15:30', 1)

    @patch('aurora_transform.get_colour_id')
    @patch('aurora_transform.get_current_datetime')
    def test_transform_calls_functions(self, mock_get_current_datetime, mock_get_colour_id):
        '''Tests that the correct functions are called inside the transform.'''
        transform('')

        assert mock_get_current_datetime.called
        assert mock_get_colour_id.called
