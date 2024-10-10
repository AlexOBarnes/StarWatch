'''Test file for the AuroraWatch extract script.'''
# pylint: disable=W0212

from unittest.mock import patch

import pytest
from requests import Response

from aurora_extract import make_request, get_status, extract


class TestMakeRequest():
    '''Tests for the make request function.'''

    @patch('aurora_extract.requests.get')
    def test_make_request_success_returns_bytes(self, mock_get, valid_xml):
        '''Tests that the a bytes object is returned when the
        request is successful.'''
        mock_response = Response()
        mock_response.status_code = 200
        mock_response._content = valid_xml
        mock_get.return_value = mock_response

        data = make_request()

        assert mock_get.called
        assert data == valid_xml

    @patch('aurora_extract.requests.get')
    def test_make_request_fail(self, mock_get):
        '''Tests that an error is raised if the request fails.'''
        mock_response = Response()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with pytest.raises(ConnectionError):
            make_request()


class TestGetStatus():
    '''Tests for the get status function.'''

    def test_get_status_success(self, valid_xml):
        '''Tests that get status runs correctly and returns a string
        given a valid xml as bytes input.'''
        result = get_status(valid_xml)

        assert result == 'green'

    @pytest.mark.parametrize('xml_input', [(1), (['list', 'test']),
                                           ('test'), ((1, 2)), ({})])
    def test_get_status_invalid_input(self, xml_input):
        '''Tests that a non-bytes object results in a TypeError.'''
        with pytest.raises(TypeError):
            get_status(xml_input)

    def test_get_status_no_root(self, invalid_xml):
        '''Tests that get status raises a ParseError if no root is found
        in the xml.'''
        with pytest.raises(ValueError) as err:
            get_status(invalid_xml)

        assert err.value.args[0] == 'Invalid XML, no root found.'

    def test_get_status_no_site_status(self, valid_xml_no_site_status):
        '''Tests that get status raise a KeyError if no site status
        is found in the root.'''
        with pytest.raises(KeyError) as err:
            get_status(valid_xml_no_site_status)

        assert err.value.args[0] == 'No site status found in current status root.'

    def test_get_status_no_status_id(self, valid_xml_no_status_id):
        '''Tests that get status raise a KeyError if no status id
        attribute is found in the site status tag.'''
        with pytest.raises(KeyError) as err:
            get_status(valid_xml_no_status_id)

        assert err.value.args[0] == 'No status id attribute found in site status.'


class TestExtract():
    '''Tests for the extract function.'''

    @patch('aurora_extract.get_status')
    @patch('aurora_extract.make_request')
    def test_extract_correct_functions(self, mock_make_request, mock_get_status):
        '''Tests that the extract function calls the other functions correctly.'''
        extract()

        assert mock_make_request.called
        assert mock_get_status.called

    @patch('aurora_extract.get_status')
    @patch('aurora_extract.make_request')
    def test_extract_returns_string(self, mock_make_request, mock_get_status, valid_xml):
        '''Tests that the extract function returns a string.'''
        mock_make_request.return_value = valid_xml
        mock_get_status.return_value = 'green'

        result = extract()

        assert result == 'green'
