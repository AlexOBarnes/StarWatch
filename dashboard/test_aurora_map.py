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


class TestGetCloudData():
    '''Tests for the get_cloud_data function.'''

    @patch('aurora_map.get_connection')
    def test_get_cloud_data(self, mock_get_connection):
        '''Tests that the function returns the expected result when successful.'''
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [{'county_name': 'County1',
                                              'cloud_coverage_percent': 75},
                                             {'county_name': 'County2',
                                              'cloud_coverage_percent': 50}]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_connection.return_value.__enter__.return_value = mock_conn

        result = get_cloud_data()
        expected_result = {'County1': 75,
                           'County2': 50}

        assert result == expected_result


class TestMapCloudCoverage():
    '''Tests for the map_cloud_coverage function.'''

    @patch('aurora_map.get_cloud_data')
    def test_map_cloud_coverage(self, mock_get_cloud_data):
        '''Tests that the function returns the expected result when successful.'''
        mock_get_cloud_data.return_value = {'County Durham': 75,
                                            'North Yorkshire': 50}

        result = map_cloud_coverage()
        expected_result = {'County Durham': 0.75,
                           'Darlington': 0.75,
                           'Hartlepool': 0.75,
                           'Middlesbrough': 0.5,
                           'North Yorkshire': 0.5,
                           'Redcar and Cleveland': 0.5,
                           'Stockton-on-Tees': 0.75,
                           'York': 0.5}

        assert result == expected_result


class TestMapRegionColours():
    '''Tests for the map_region_colours function.'''

    @patch('aurora_map.get_aurora_data')
    def test_map_region_colours(self, mock_get_aurora_data):
        '''Tests that the function returns the expected result when successful.'''
        mock_get_aurora_data.return_value = 'Yellow'

        result = map_region_colours(['Test'])
        expected_result = {'North East (England)': 'blue',
                           'North West (England)': 'blue',
                           'Northern Ireland': 'blue',
                           'Scotland': 'blue',
                           'Yorkshire and The Humber': 'blue',
                           'Test': 'red'}

        assert result == expected_result


class TestCreateAuroraMap():
    '''Tests for the create_aurora_map function.'''

    @patch('geopandas.read_file')
    @patch('aurora_map.map_region_colours')
    @patch('aurora_map.map_cloud_coverage')
    def test_create_aurora_map(self, mock_map_cloud_coverage,
                               mock_map_region_colours, mock_read_file):
        '''Tests that the function returns the correct data type.'''
        mock_gdf1 = MagicMock()
        mock_gdf1.nuts118nm.tolist.return_value = ['Region1', 'Region2']
        mock_read_file.side_effect = [mock_gdf1, mock_gdf1]
        mock_map_region_colours.return_value = {'Region1': 'red',
                                                'Region2': 'green'}
        mock_map_cloud_coverage.return_value = {'Region1': 0.5,
                                                'Region2': 0.75}

        fig = create_aurora_map()

        assert isinstance(fig, plt.Figure)


class TestGetAverageCloudData():
    '''Tests for the get_average_cloud_data function.'''

    @patch('aurora_map.get_connection')
    def test_get_average_cloud_data(self, mock_get_connection):
        '''Tests that the function returns the expected result when successful.'''
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [{'county_name': 'County1',
                                              'avg_cloud_cov': 60.5},
                                             {'county_name': 'County2',
                                              'avg_cloud_cov': 40.0}]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_connection.return_value.__enter__.return_value = mock_conn

        result = get_average_cloud_data()
        expected_result = {'County1': 60.5,
                           'County2': 40.0}

        assert result == expected_result


class TestGetBodyVisibleRegions():
    '''Tests for the get_body_visible_regions function.'''

    @patch('aurora_map.get_connection')
    def test_get_body_visible_regions(self, mock_get_connection):
        '''Tests that the function returns the expected result when successful.'''
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [('Region1',), ('Region2',)]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_connection.return_value.__enter__.return_value = mock_conn

        result = get_body_visible_regions('Venus')
        expected_result = ['Region1', 'Region2']

        assert result == expected_result


class TestMapBodyVisibilityRegionsColours():
    '''Tests for the map_body_visibility_regions_colours function.'''

    @patch('aurora_map.get_body_visible_regions')
    def test_map_body_visibility_regions_colours(self, mock_get_body_visible_regions):
        '''Tests that the function returns the expected result when successful.'''
        mock_get_body_visible_regions.return_value = ['Region1', 'Region2']
        result = map_body_visibility_regions_colours('Venus',
                                                     ['Region1', 'Region3'])
        expected_result = {'Region1': 'green',
                           'Region3': 'red'}

        assert result == expected_result
