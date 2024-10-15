"""Full ETL pipeline lambda for the astronomy API data."""

# pylint: disable=W0613

import time
import logging
import asyncio

from astronomy_extract import extract_weekly_astronomy_data
from astronomy_transform import transform_astronomy_data
from astronomy_load import upload_astronomy_data


def lambda_handler(event=None, context=None) -> None:
    '''Runs the notification pipeline'''

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    logging.info("Astronomy API pipeline.")

    start_time = time.time()

    extract_data = asyncio.run(extract_weekly_astronomy_data())
    logging.info("Astronomy API data extraction complete.")

    # transform_astronomy_data returns dictionary as follows:
    # {
    #   "positions_list": body_position_list,
    #   "moon_phase_list": moon_phase_list
    # }
    transformed_data = transform_astronomy_data(extract_data)
    logging.info("Astronomy data transformation complete.")

    upload_astronomy_data(transformed_data)
    logging.info("Astronomy data upload complete.")
    logging.info("Astronomy execution time: %s seconds" %
                 round((time.time() - start_time), 2))


if __name__ == '__main__':
    lambda_handler()
