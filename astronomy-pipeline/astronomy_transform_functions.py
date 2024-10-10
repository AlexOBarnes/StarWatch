"""Functions for the astronomy API transform script."""

import json
from datetime import datetime

import pandas as pd

from astronomy_extract_functions import get_db_connection


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


def clean_position_data(df: pd.DataFrame) -> list:
    """Removes unnecessary dataframe entries and converts data 
    to more appropriate data types."""

    # Get rid of earth entries
    df = df[df["body_name"] != "earth"]

    # Gets body_IDs from database
    body_mapping = get_body_mapping()
    df["body_id"] = df["body_name"].map(body_mapping)

    # distance_km to float
    # azimuth to float
    # altitude to float
    for col in ["distance_km", "azimuth", "altitude"]:
        df[col] = df[col].astype(float)

    print(df.head())

    return df.values.tolist()


def get_moon_df(phase_data: list["dict"]) -> list:
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
