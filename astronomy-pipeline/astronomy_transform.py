"""
astronomy_transform
Transform script to reshape Astronomy API data into a format
for upload to the RDS database.
"""
import logging

from astronomy_transform_functions import (get_data_into_dataframe, clean_position_data,
                                           get_moon_df, convert_positions_datetime,
                                           convert_moon_datetime)


def transform_astronomy_data(raw_data: dict) -> list:
    """Main function for converting the extracted astronomy data into flat dataframes."""

    logging.info("Data transformation started.")

    merged_df = get_data_into_dataframe(raw_data)

    position_list = clean_position_data(merged_df)
    position_list = convert_positions_datetime(position_list)
    logging.info("Body position data converted to 2D list.")

    moon_phase_data = raw_data["moon_phase_urls"]

    moon_phase_list = get_moon_df(moon_phase_data)
    moon_phase_list = convert_moon_datetime(moon_phase_list)
    logging.info("Moon phase data converted to 2D list.")

    return {
        "positions_list": position_list,
        "moon_phase_list": moon_phase_list
    }
