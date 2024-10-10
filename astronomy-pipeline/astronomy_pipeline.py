"""Full ETL pipeline for the astronomy API data."""

from astronomy_extract import extract_weekly_astronomy_data
from astronomy_transform import transform_astronomy_data

if __name__ == "__main__":

    extract_data = extract_weekly_astronomy_data()

    # transform_astronomy_data returns dictionary as follows:
    # {
    #   "positions_list": body_position_list,
    #   "moon_phase_list": moon_phase_list
    # }
    transformed_data = transform_astronomy_data(extract_data)

    print(transformed_data["positions_list"])
    print(transformed_data["moon_phase_list"])

    print(transformed_data["positions_list"][-1][0])
    print(type(transformed_data["positions_list"][-1][0]))
    print(transformed_data["positions_list"][-1][0])
    print(type(transformed_data["positions_list"][-1][0]))
