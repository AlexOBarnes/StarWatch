"""Full ETL pipeline lambda for the astronomy API data."""

import logging

from astronomy_extract import extract_weekly_astronomy_data
from astronomy_transform import transform_astronomy_data
from astronomy_load import upload_astronomy_data


def lambda_handler(event=None, context=None) -> None:
    '''Runs the notification pipeline'''
    print('Running Lambda')
    extract_data = extract_weekly_astronomy_data()

    # transform_astronomy_data returns dictionary as follows:
    # {
    #   "positions_list": body_position_list,
    #   "moon_phase_list": moon_phase_list
    # }
    transformed_data = transform_astronomy_data(extract_data)

    upload_astronomy_data(transformed_data)


if __name__ == '__main__':
    lambda_handler()