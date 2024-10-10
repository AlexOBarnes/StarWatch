'''Script to extract data from the AuroraWatch UK API.'''

import xml.etree.ElementTree as ET
import logging

import requests

AURORA_WATCH_URL = 'http://aurorawatch-api.lancs.ac.uk/0.2/status/current-status.xml'


def make_request() -> bytes:
    '''Returns the result xml as a string from the
    get request made to the AuroraWatchUK API.'''
    response = requests.get(url=AURORA_WATCH_URL, timeout=10)
    logging.info('AuroraWatchUK request sent')

    if response.status_code == 200:
        logging.info('AuroraWatchUK request successful')
        return response.content

    err_msg = f'''AuroraWatchUK request unsuccessful: Error code {
        response.status_code}'''
    logging.error(err_msg)
    raise ConnectionError(err_msg)


def get_status(xml_string: bytes) -> str:
    '''Returns the current status from the XML passed in.'''
    if not isinstance(xml_string, bytes):
        raise TypeError('XML data must be in bytes format')

    try:
        current_status_root = ET.fromstring(xml_string)
    except ET.ParseError as pe:
        err_msg = 'Invalid XML, no root found.'
        logging.error(err_msg)
        raise ValueError(err_msg) from pe

    site_status = current_status_root.find('site_status')

    if site_status is not None:
        status_colour = site_status.get('status_id')

        if status_colour is not None:
            logging.info('Aurora status colour extracted')
            return status_colour

        err_msg = 'No status id attribute found in site status.'
        logging.error(err_msg)
        raise KeyError(err_msg)

    err_msg = 'No site status found in current status root.'
    logging.error(err_msg)
    raise KeyError(err_msg)


def extract() -> str:
    '''Runs the functions to make the request, get the status
    colour and returns it.'''
    request_response = make_request()
    aurora_status_colour = get_status(request_response)

    return aurora_status_colour


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    print(extract())
