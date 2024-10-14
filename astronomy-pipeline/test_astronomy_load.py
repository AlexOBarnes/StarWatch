'''Tests for the astronomy load script.'''
# pylint: disable=W0613

from unittest.mock import patch, MagicMock

from astronomy_load import upload_body_position_data, upload_astronomy_data, upload_moon_phase_data


class TestUploadBodyPositionData():
    '''Tests for the upload body position data function.'''

    @patch('astronomy_load.execute_values')
    @patch('astronomy_load.get_db_connection')
    def test_upload_body_position_data_success_functions(self, mock_get_db_connection,
                                                         mock_execute_values):
        '''Tests that the correct functions and methods are called.'''
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        upload_body_position_data([[]])

        assert mock_get_db_connection.called
        assert mock_execute_values.called
        assert mock_conn.cursor.called

    @patch('astronomy_load.execute_values')
    @patch('astronomy_load.get_db_connection')
    def test_upload_body_position_data_success_calls(self, mock_get_db_connection,
                                                     mock_execute_values, upload_body_data_query):
        '''Tests that the execute values method is called with the correct inputs.'''
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        upload_body_position_data([[]])

        mock_execute_values.assert_called_once_with(
            mock_cursor, upload_body_data_query, [[]])


class TestUploadMoonPhaseData():
    '''Tests for the upload moon phase data function.'''

    @patch('astronomy_load.execute_values')
    @patch('astronomy_load.get_db_connection')
    def test_upload_moon_phase_data_success_functions(self, mock_get_db_connection,
                                                      mock_execute_values):
        '''Tests that the correct functions and methods are called.'''
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        upload_moon_phase_data([[]])

        assert mock_get_db_connection.called
        assert mock_execute_values.called
        assert mock_conn.cursor.called

    @patch('astronomy_load.execute_values')
    @patch('astronomy_load.get_db_connection')
    def test_upload_moon_phase_data_success_calls(self, mock_get_db_connection,
                                                  mock_execute_values, upload_moon_data_query):
        '''Tests that the execute values method is called with the correct inputs.'''
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        upload_moon_phase_data([[]])

        mock_execute_values.assert_called_once_with(
            mock_cursor, upload_moon_data_query, [[None, None, 'moon_phase']])


class TestUploadAstronomyData():
    '''Tests for the upload astronomy data function.'''

    @patch('astronomy_load.upload_moon_phase_data')
    @patch('astronomy_load.upload_body_position_data')
    def test_upload_astronomy_data_success_functions(self, mock_upload_body_position_data,
                                                     mock_upload_moon_phase_data,
                                                     astronomy_data_dict):
        '''Tests that the correct functions are called.'''
        upload_astronomy_data(astronomy_data_dict)

        assert mock_upload_body_position_data.called
        assert mock_upload_moon_phase_data.called

    @patch('astronomy_load.upload_moon_phase_data')
    @patch('astronomy_load.upload_body_position_data')
    def test_upload_astronomy_data_success_calls_moon(self, mock_upload_body_position_data,
                                                      mock_upload_moon_phase_data,
                                                      astronomy_data_dict):
        '''Tests that upload moon phase data is called with the correct values.'''
        upload_astronomy_data(astronomy_data_dict)

        mock_upload_moon_phase_data.assert_called_once_with(['moon'])

    @patch('astronomy_load.upload_moon_phase_data')
    @patch('astronomy_load.upload_body_position_data')
    def test_upload_astronomy_data_success_calls_body(self, mock_upload_body_position_data,
                                                      mock_upload_moon_phase_data,
                                                      astronomy_data_dict):
        '''Tests that upload body position data is called with the correct values.'''
        upload_astronomy_data(astronomy_data_dict)

        mock_upload_body_position_data.assert_called_once_with(['positions'])
