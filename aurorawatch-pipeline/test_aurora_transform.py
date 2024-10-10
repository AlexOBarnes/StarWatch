'''Test file for the AuroraWatch extract script.'''
# pylint: disable=W0212


from unittest.mock import patch
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


class TestTransform():
    '''Tests for the transform function.'''
