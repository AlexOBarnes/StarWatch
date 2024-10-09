"""File to obtain body positional data from the Astronomy API."""

# pylint: disable=E0401,R0913,R0917

from os import environ as ENV
from datetime import date, timedelta
import base64


from psycopg2 import connect, extensions, extras
from dotenv import load_dotenv
import requests

load_dotenv()

ASTRO_URL = "https://api.astronomyapi.com/api/v2"


def get_db_connection() -> extensions.connection:
    """Reusable function for getting a database connection."""

    return connect(cursor_factory=extras.RealDictCursor,
                   dbname=ENV["DB_NAME"],
                   host=ENV["DB_HOST"],
                   password=ENV["DB_PASSWORD"],
                   user=ENV["DB_USER"],
                   port=ENV["DB_PORT"])


def get_auth_string() -> str:
    """Generates AstronomyAPI authorization key from env values."""

    user_pass = f"{ENV["ASTRONOMY_ID"]}:{ENV["ASTRONOMY_SECRET"]}"

    auth_string = base64.b64encode(user_pass.encode()).decode()

    return auth_string


def get_db_regions() -> list:
    """Returns the regions data from an RDS instance"""
    with get_db_connection() as conn:
        cur = conn.cursor()

        cur.execute("SELECT * FROM region;")

        regions = cur.fetchall()

    return regions


def get_all_body_positions(start_date: date, end_date: date, lat: float,
                           long: float, time: str, elev: int = 50) -> dict:
    """Returns the inclusive body positional information from
    the Astronomy API for a given date range."""
    url = f"{ASTRO_URL}/bodies/positions?latitude={lat}&longitude={
        long}&elevation={elev}&from_date={start_date}&to_date={end_date}&time={time}"

    auth_string = get_auth_string()

    headers = {"Authorization": f"Basic {auth_string}"}

    return (requests.get(url, headers=headers)).json()


def make_clean_body_dict(entry: dict) -> dict:
    """Creates refined body data from astronomy API body data."""

    new_dict = {}
    new_dict["datetime"] = entry["date"]
    new_dict["body_name"] = entry["id"]
    new_dict["distance_km"] = entry["distance"]["fromEarth"]["km"]
    new_dict["azimuth"] = entry["position"]["horizontal"]["azimuth"]["degrees"]
    new_dict["altitude"] = entry["position"]["horizontal"]["altitude"]["degrees"]
    new_dict["constellation"] = entry["position"]["constellation"]["id"]

    return new_dict


def refine_bodies_data(bodies: dict) -> list:
    """Removes unnecessary data from the astronomy positions dict."""

    rows = bodies["data"]["table"]["rows"]

   # Each cell contains a list of dictionaries of an entry
   # key and a single body over a set number of days (7)
    output_list = []
    for obj in rows:
        for entry in obj["cells"]:
            clean_dict = make_clean_body_dict(entry)
            output_list.append(clean_dict)

    return output_list


def get_moon_phase(input_date: str) -> str:
    """Returns a url for an image of the moon phase for a given
    location and date."""

    example_body = {
        "format": "png",
        "style": {
            "moonStyle": "default",
            "backgroundStyle": "stars",
            "headingColor": "white",
            "textColor": "white"
        },
        "observer": {
            "latitude": 53.812207,
            "longitude": -2.917976,
            "date": f"{input_date}"
        },
        "view": {
            "type": "portrait-simple",
            "orientation": "north-up"
        }
    }

    url = f"{ASTRO_URL}/studio/moon-phase"

    auth_string = get_auth_string()

    headers = {"Authorization": f"Basic {auth_string}"}

    return requests.post(url, headers=headers, json=example_body).json()["data"]["imageUrl"]


def get_position_data(input_dict: dict, times: list[str], regions: list[dict],
                      start: date, end: date) -> dict:
    """Returns all positional data for astronomical bodies as dictionary."""

    for region in regions:

        region_id = region["region_id"]
        lat = region["latitude"]
        long = region["longitude"]

        for time in times:

            bodies_pos = get_all_body_positions(
                start, end, lat, long, time)

            refined_pos = refine_bodies_data(bodies_pos)

            input_dict[region_id][time[:2]] = refined_pos

    return input_dict


def get_moon_urls(start: date) -> list[dict]:
    """Returns list of moon phase URLs from the Astronomy API"""
    pass


def fill_region_time_dict(times_list: list[str], region_list: list[dict]):
    """Creates framework for body position dictionary."""
    pass


if __name__ == "__main__":
    ...
