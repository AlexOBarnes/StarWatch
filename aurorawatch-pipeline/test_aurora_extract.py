'''Test file for the AuroraWatch extract script.'''

from unittest.mock import patch
import pytest

# from aurora_extract import make_request, get_status, extract


class TestMakeRequest():
    '''Tests for the make request function.'''

    def test_make_request_success_returns_bytes(self):
        '''Tests that the a bytes object is returned when the
        request is successful.'''

    def test_make_request_fail(self):
        '''Tests that an error is raised if the request fails.'''


class TestGetStatus():
    '''Tests for the get status function.'''

    def test_get_status_success(self):
        '''Tests that get status runs correctly and returns a string
        given a valid XML as bytes input.'''

    @mark.par
    def test_get_status_invalid_input(self):
        '''Tests that a non-bytes object results in a TypeError.'''

    def test_get_status_no_root(self):
        '''Tests that get status raises a ParseError if no root is found
        in the XML.'''

    def test_get_status_no_site_status(self):
        '''Tests that get status raise a KeyError if no site status
        is found in the root.'''

    def test_get_status_no_status_id(self):
        '''Tests that get status raise a KeyError if no status id
        attribute is found in the site status tag.'''


class TestExtract():
    '''Tests for the extract function.'''

    def test_extract_correct_functions(self):
        '''Tests that the extract function calls the other functions correctly.'''

    def test_extract_returns_string(self):
        '''Tests that the extract function returns a string.'''
