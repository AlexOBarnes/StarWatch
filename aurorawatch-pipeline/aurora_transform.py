'''Script to transform the extracted data from the AuroraWatch UK API into a format
ready to be loaded.'''

import logging
from datetime import datetime as dt

from aurora_extract import extract

ALERT_COLOURS = {'Green': 1, 'Yellow': 2, 'Amber': 3, 'Red': 4}


def get_colour_id(colour: str) -> int:
    ''''''


def get_current_datetime() -> str:
    ''''''


def transform(colour: str) -> tuple:
    ''''''


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    extracted_data = extract()
