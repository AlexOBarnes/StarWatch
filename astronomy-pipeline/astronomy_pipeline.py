"""Full ETL pipeline for the astronomy API data."""

from astronomy_extract import extract_weekly_astronomy_data
from astronomy_transform import transform_astronomy_data

if __name__ == "__main__":

    extract_data = extract_weekly_astronomy_data()

    # transform_astronomy_data returns dictionary as follows:
    # {
    #   "position_df": body_position_dataframe,
    #   "moon_df": moon_phase_dataframe
    # }
    transformed_data = transform_astronomy_data(extract_data)
