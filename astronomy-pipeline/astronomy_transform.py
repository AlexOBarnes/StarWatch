"""Transform script to reshape Astronomy API data into a format
for upload to the RDS database."""

from astronomy_transform_functions import (get_data_into_database, clean_position_data,
                                           get_moon_df)


def transform_astronomy_data(raw_data: dict) -> list:
    """Main function for converting the extracted astronomy data into flat dataframes."""

    merged_df = get_data_into_database(raw_data)

    position_df = clean_position_data(merged_df)

    moon_phase_data = raw_data["moon_phase_urls"]

    moon_df = get_moon_df(moon_phase_data)

    return {
        "position_df": position_df,
        "moon_df": moon_df
    }
