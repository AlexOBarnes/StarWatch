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
