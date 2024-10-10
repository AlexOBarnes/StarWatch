'''Contains the configurations for the tests in this folder.'''

import pytest


@pytest.fixture
def valid_xml() -> bytes:
    '''Valid xml example to use in testing.'''
    xml_string = '''<?xml version=\'1.0\' encoding=\'UTF-8\' standalone=\'yes\'?>\n
    <!DOCTYPE current_status PUBLIC "-//AuroraWatch-API//DTD REST 0.2.5//EN" 
    "http://aurorawatch-api.lancs.ac.uk/0.2.5/aurorawatch-api.dtd">\n
    <current_status api_version="0.2.5"><updated><datetime>2024-10-10T10:21:32+0000</datetime>
    </updated><site_status project_id="project:AWN" site_id="site:AWN:SUM" 
    site_url="http://aurorawatch-api.lancs.ac.uk/0.2.5/project/awn/sum.xml" 
    status_id="green"/></current_status>'''

    return xml_string.encode('utf-8')


@pytest.fixture
def invalid_xml() -> bytes:
    '''Invalid xml with no root for testing.'''
    xml_string = 'Invalid xml'

    return xml_string.encode('utf-8')


@pytest.fixture
def valid_xml_no_site_status() -> bytes:
    '''Valid xml example without site status to use in testing.'''
    xml_string = '''<?xml version=\'1.0\' encoding=\'UTF-8\' standalone=\'yes\'?>\n
    <!DOCTYPE current_status PUBLIC "-//AuroraWatch-API//DTD REST 0.2.5//EN" 
    "http://aurorawatch-api.lancs.ac.uk/0.2.5/aurorawatch-api.dtd">\n
    <current_status api_version="0.2.5"><updated><datetime>2024-10-10T10:21:32+0000</datetime>
    </updated></current_status>'''

    return xml_string.encode('utf-8')


@pytest.fixture
def valid_xml_no_status_id() -> bytes:
    '''Valid xml example without status id attribute to use in testing.'''
    xml_string = '''<?xml version=\'1.0\' encoding=\'UTF-8\' standalone=\'yes\'?>\n
    <!DOCTYPE current_status PUBLIC "-//AuroraWatch-API//DTD REST 0.2.5//EN" 
    "http://aurorawatch-api.lancs.ac.uk/0.2.5/aurorawatch-api.dtd">\n
    <current_status api_version="0.2.5"><updated><datetime>2024-10-10T10:21:32+0000</datetime>
    </updated><site_status project_id="project:AWN" site_id="site:AWN:SUM" 
    site_url="http://aurorawatch-api.lancs.ac.uk/0.2.5/project/awn/sum.xml"/></current_status>'''

    return xml_string.encode('utf-8')
