"""Extracts astronomical data from the Astronomy API."""

from datetime import date, timedelta, datetime
import json
import logging

from astronomy_extract_functions import get_db_regions, get_position_data, get_moon_urls
from astronomy_extract_functions import fill_region_time_dict


def save_to_file(filename: str, data: list[dict]) -> None:
    """Save the data to a file called stories.json"""

    with open(filename, "w", encoding="utf-8") as f_obj:
        json.dump(data, f_obj, indent=4)


def extract_weekly_astronomy_data():
    """Main function for extracting astronomical for a week"""

    logging.info("Data extraction started.")

    start_date = date.today() + timedelta(days=7)

    end_date = start_date + timedelta(days=6)

    times = ["18:00:00", "21:00:00", "00:00:00", "03:00:00", "06:00:00"]

    regions = get_db_regions()

    output_dict = fill_region_time_dict(times, regions)

    position_data = get_position_data(
        output_dict, times, regions, start_date, end_date)
    logging.info("Body position data extracted and refined.")

    final_dict = {}
    final_dict["body_positions"] = position_data
    final_dict["moon_phase_urls"] = get_moon_urls(start_date)
    logging.info("Moon phase data extracted.")

    return final_dict


if __name__ == "__main__":

    time1 = datetime.now()
    result_data = extract_weekly_astronomy_data()
    save_to_file("test_extract_data.json", result_data)

    print(f"Time: {(datetime.now() - time1).seconds}")
