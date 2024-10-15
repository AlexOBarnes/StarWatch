"""Transform script to reshape Astronomy API data into a format
for upload to the RDS database."""

import json
from datetime import datetime
import logging

import pandas as pd

from astronomy_extract import get_db_connection


def load_from_file(filename: str) -> dict:
    """Load the stories from a file called stories.json"""

    with open(filename, "r", encoding="UTF-8") as f_obj:
        return json.load(f_obj)


def get_data_into_dataframe(raw_data: dict) -> pd.DataFrame:
    """Converts a list of body position dictionaries into a dataframe."""

    regions = list(raw_data["body_positions"].keys())
    times = list(raw_data["body_positions"][1].keys())

    df_list = []
    for r in regions:
        for t in times:
            time_list = raw_data["body_positions"][r][t]
            df = pd.DataFrame(time_list)
            df["region_id"] = int(r)
            df_list.append(df)

    return pd.concat(df_list, ignore_index=True)


def get_body_mapping() -> dict:
    """Returns body name to ID mapping from the RDS database."""

    with get_db_connection() as conn:

        cur = conn.cursor()

        cur.execute("SELECT body_id, body_name from body;")

        results = cur.fetchall()

    b_mapping = {}

    for body in results:
        body_name = body["body_name"].lower()
        body_id = body["body_id"]
        b_mapping[body_name] = body_id

    return b_mapping


def get_constellation_mapping() -> dict:
    """Returns constellation name to ID mapping from the RDS database."""

    with get_db_connection() as conn:

        cur = conn.cursor()

        cur.execute(
            "SELECT constellation_id, constellation_short_name from constellation;")

        results = cur.fetchall()

    c_mapping = {}

    for body in results:
        const_name = body["constellation_short_name"].lower()
        const_id = body["constellation_id"]
        c_mapping[const_name] = const_id

    return c_mapping


def clean_position_data(df: pd.DataFrame) -> list:
    """Removes unnecessary dataframe entries and converts data 
    to more appropriate data types."""

    # Get rid of earth entries
    # Create a copy to avoid warnings
    df = df[df["body_name"] != "earth"].copy()

    # Gets body_IDs from database
    body_mapping = get_body_mapping()
    df.loc[:, "body_id"] = df["body_name"].map(body_mapping)

    # Gets constellation IDs from database
    constellation_mapping = get_constellation_mapping()
    df.loc[:, "constellation_id"] = df["constellation_name"].map(
        constellation_mapping)

    # Convert distance_km, azimuth, and altitude to float
    df.loc[:, "distance_km"] = df["distance_km"].astype(float)
    df.loc[:, "azimuth"] = df["azimuth"].astype(float)
    df.loc[:, "altitude"] = df["altitude"].astype(float)

    df = df.drop(columns=["body_name", "constellation_name"])

    return df.values.tolist()


def get_moon_list(phase_data: list["dict"]) -> list:
    """Returns a dataframe of moon phase dates and image URLs."""

    df = pd.DataFrame(phase_data)

    return df.values.tolist()


def convert_positions_datetime(position_list: list) -> list:
    """Converts body position time string to a datetime object."""

    for entry in position_list:

        entry[0] = datetime.strptime(entry[0], "%Y-%m-%dT%H:%M:%S.%f%z")

    return position_list


def convert_moon_datetime(moon_list: list) -> list:
    """Converts moon phase time string to a datetime object."""

    for entry in moon_list:

        entry[0] = datetime.strptime(entry[0], "%Y-%m-%d")

    return moon_list


def get_star_chart_df(star_chart_data: list["dict"]) -> pd.DataFrame:
    """Creates dataframe from star chart data."""

    return pd.DataFrame(star_chart_data)


def clean_star_chart_data(star_chart_df: pd.DataFrame) -> list:
    """Returns clean star chart data as a list."""

    cleaned_df = star_chart_df.dropna(subset=['url'])

    return cleaned_df.values.tolist()


def convert_star_chart_datetime(chart_list: list) -> list:
    """Converts moon phase time string to a datetime object."""

    for entry in chart_list:

        entry[0] = datetime.strptime(entry[0], "%Y-%m-%d")

    return chart_list


def transform_astronomy_data(raw_data: dict) -> list:
    """Main function for converting the extracted astronomy data into flat dataframes."""

    logging.info("Data cleaning started.")

    merged_df = get_data_into_dataframe(raw_data)
    position_list = clean_position_data(merged_df)
    position_list = convert_positions_datetime(position_list)
    logging.info("Body position data converted to 2D list.")

    moon_phase_data = raw_data["moon_phase_urls"]
    moon_phase_list = get_moon_list(moon_phase_data)
    moon_phase_list = convert_moon_datetime(moon_phase_list)
    logging.info("Moon phase data converted to 2D list.")

    star_chart_data = raw_data["star_chart_urls"]
    star_chart_df = get_star_chart_df(star_chart_data)
    star_chart_list = clean_star_chart_data(star_chart_df)
    star_chart_list = convert_star_chart_datetime(star_chart_list)
    logging.info("Star chart data converted to 2D list.")

    return {
        "positions_list": position_list,
        "moon_phase_list": moon_phase_list,
        "star_chart_list": star_chart_list
    }
