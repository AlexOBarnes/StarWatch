'''Script to transform the extracted data from the AuroraWatch UK API into a format
ready to be loaded.'''

import logging
from datetime import datetime as dt

from aurora_extract import extract


ALERT_COLOURS = {'Green': 1, 'Yellow': 2, 'Amber': 3, 'Red': 4}


def get_colour_id(colour: str) -> int:
    '''Returns the colour id for a given colour.'''
    if not isinstance(colour, str):
        raise TypeError('The colour must be given in string format.')

    colour_id = ALERT_COLOURS.get(colour.strip().title())

    if colour_id:
        logging.info('Colour ID found.')
        return colour_id

    err_msg = f'No colour ID found for colour: {colour}'
    logging.error(err_msg)
    raise KeyError(err_msg)


def get_current_datetime() -> str:
    '''Returns the current datetime in the format "YYYY-MM-DD HH:MM:SS".'''
    current_datetime = dt.now()

    return current_datetime.strftime("%Y-%m-%d %H:%M:%S")


def transform(colour: str) -> tuple:
    '''Returns a tuple of the colour id and timestamp, ready for loading.'''
    colour_id = get_colour_id(colour)
    timestamp = get_current_datetime()

    logging.info('AuroraWatch alert data transformed into tuple.')
    return (timestamp, colour_id)


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    extracted_data = extract()
    print(transform(extracted_data))
