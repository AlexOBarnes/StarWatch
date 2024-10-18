'''Contains tests for map generator functions.'''
# pylint: disable=R0903

from unittest.mock import patch, MagicMock
import matplotlib.pyplot as plt

from aurora_map import (get_aurora_data, get_cloud_data,
                        map_cloud_coverage, map_region_colours, create_aurora_map,
                        get_average_cloud_data, get_body_visible_regions,
                        map_body_visibility_regions_colours, create_body_visibility_map,
                        map_average_cloud_coverage, get_average_visibility_data,
                        map_average_visibility_colour, create_visibility_map)


class TestGetAuroraData():
    '''Tests for the get_aurora_data function.'''

    @patch('aurora_map.get_connection')
    def test_get_aurora_data(self, mock_get_connection):
        '''Tests that the function returns the expected result when successful.'''
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = ['Yellow']
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_connection.return_value.__enter__.return_value = mock_conn

        result = get_aurora_data()

        assert result == 'Yellow'
