"""Test file for the Astronomy API pipeline files."""

import base64
from unittest import mock
import json
from datetime import date

import pytest
from psycopg2 import extensions, extras

from extract_functions import get_db_connection, get_auth_string, get_db_regions, get_all_body_positions
from extract_functions import make_clean_body_dict, refine_bodies_data, get_position_data

ENV = {
    "DB_NAME": "test_db",
    "DB_HOST": "localhost",
    "DB_PASSWORD": "test_password",
    "DB_USER": "test_user",
    "DB_PORT": "5432",
    "ASTRONOMY_ID": "test_id",
    "ASTRONOMY_SECRET": "test_secret"
}


class TestExtractFunctions():
    """Tests for the extract_functions file."""

    @mock.patch("extract_functions.ENV", ENV)
    @mock.patch("extract_functions.connect")
    def test_get_db_connection_called_with_correct_parameters(self, mock_connect):
        """Tests get_db_connection successfully connects
        using the correct parameters."""

        mock_conn = object()
        mock_connect.return_value = mock_conn

        get_db_connection()

        mock_connect.assert_called_once_with(
            cursor_factory=extras.RealDictCursor,
            dbname=ENV["DB_NAME"],
            host=ENV["DB_HOST"],
            password=ENV["DB_PASSWORD"],
            user=ENV["DB_USER"],
            port=ENV["DB_PORT"]
        )

    @mock.patch("extract_functions.connect")
    def test_get_db_connection_expected_output(self, mock_connect):
        """Tests get_db_connection successfully connects
        using the correct parameters."""

        mock_conn = object()
        mock_connect.return_value = mock_conn

        conn = get_db_connection()

        assert conn == mock_conn

    @mock.patch("extract_functions.ENV", ENV)
    def test_get_auth_string_returns_string(self):
        """Tests auth string output is string data."""

        res = get_auth_string()

        assert isinstance(res, str)

    @mock.patch("extract_functions.ENV", ENV)
    def test_get_auth_string(self):
        """Tests expected output is provided by the
        get_auth_string function."""

        expected_user_pass = "test_id:test_secret"
        expected = base64.b64encode(expected_user_pass.encode()).decode()

        actual = get_auth_string()

        assert actual == expected

    @mock.patch("extract_functions.get_db_connection")
    def test_get_db_regions_returns_expected_result(self, mock_connection):
        """Tests that data is passed through into the output correctly."""

        mock_conn = mock.Mock()
        mock_cursor = mock.Mock()

        mock_cursor.fetchall.return_value = [{"key1": 1}, {"key2": 2}]
        mock_conn.cursor.return_value = mock_cursor
        mock_connection.return_value.__enter__.return_value = mock_conn

        res = get_db_regions()

        assert res == [{"key1": 1}, {"key2": 2}]

    @mock.patch("extract_functions.get_db_connection")
    def test_get_db_regions_returns_list(self, mock_connection):
        """Tests that data is passed through into the output correctly."""

        mock_conn = mock.Mock()
        mock_cursor = mock.Mock()

        mock_cursor.fetchall.return_value = [{"key1": 1}, {"key2": 2}]
        mock_conn.cursor.return_value = mock_cursor
        mock_connection.return_value.__enter__.return_value = mock_conn

        res = get_db_regions()

        assert isinstance(res, list)

    @mock.patch("extract_functions.get_auth_string")
    @mock.patch("extract_functions.requests.get")
    def test_get_all_bodies_returns_json_dict(self, mock_get, mock_auth_string):
        """Asserts that a dictionary is returned by the body function."""

        mock_auth_string.return_value = "fake_string"

        class MockResponse:
            """Simple mock class for creating object that returns a
            dict when .json() is used."""

            def __init__(self, data: dict):
                self._data = data

            def json(self):
                return self._data

        mock_data = {"key1": "value1", "key2": "value2"}

        mock_response = MockResponse(mock_data)

        mock_get.return_value = mock_response

        res = get_all_body_positions(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 10),
            lat=40.7128,
            long=-74.0060,
            time="12:00")

        assert res == mock_data

    def test_make_clean_body_dict_expected_outcome(self, sample_raw_body_data,
                                                   sample_filtered_body_data):
        """Test dictionary is filtered properly."""

        sample_dict = sample_raw_body_data

        expected = sample_filtered_body_data

        res = make_clean_body_dict(sample_dict)

        assert res == expected

    @mock.patch("extract_functions.make_clean_body_dict")
    def test_refine_bodies_data_creates_list_of_dicts(self, fake_clean):
        """Asserts that the function returns a list of dicts."""

        input_data = {
            "data": {
                "table": {
                    "rows": [
                        {"cells": [1, 2, 3]},
                        {"cells": [1, 2, 3]}
                    ]
                }
            }
        }

        fake_clean.return_value = {"key": "val"}

        res = refine_bodies_data(input_data)

        assert isinstance(res, list)

    @mock.patch("extract_functions.refine_bodies_data")
    @mock.patch("extract_functions.get_all_body_positions")
    def test_get_position_data_returns_dict(self, fake_body_pos, fake_refine):
        """Tests that the correct data types are returned by the
        named function."""

        fake_refine.return_value = [1, 2, 3]

        input_dict = {1: {}, 2: {}}

        regions = [{"region_id": 1, "latitude": 1.2, "longitude": 1.3},
                   {"region_id": 2, "latitude": 1.4, "longitude": 1.5}]

        times = ["18:00:00", "21:00:00", "00:00:00"]

        start_date, end_date = date.today(), date.today()

        res = get_position_data(input_dict, times, regions,
                                start_date, end_date)

        assert isinstance(res, dict)
        assert isinstance(res[1], dict)
        assert isinstance(res[1]["18"], list)

    @mock.patch("extract_functions.refine_bodies_data")
    @mock.patch("extract_functions.get_all_body_positions")
    def test_get_position_data_returns_correct_vals(self, fake_body_pos, fake_refine):
        """Tests that the correct data values are returned
        in the output of the named function"""

        fake_refine.return_value = [1, 2, 3]

        input_dict = {1: {}, 2: {}}

        regions = [{"region_id": 1, "latitude": 1.2, "longitude": 1.3},
                   {"region_id": 2, "latitude": 1.4, "longitude": 1.5}]

        times = ["18:00:00", "21:00:00", "00:00:00"]

        start_date, end_date = date.today(), date.today()

        res = get_position_data(input_dict, times, regions,
                                start_date, end_date)

        assert res[1]["18"][2] == 3
