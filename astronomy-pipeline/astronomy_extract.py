"""Extracts astronomical data from the Astronomy API.
File to obtain body positional data from the Astronomy API."""

# pylint: disable=E0401,R0913,R0917

from os import environ as ENV
from datetime import date, timedelta, datetime
import base64
import json
import logging
import asyncio

import aiohttp
import requests
from dotenv import load_dotenv
from psycopg2 import connect, extensions, extras
from requests import exceptions as ex

from api_error import APIError

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
    """Generates AstronomyAPI authorisation key from env values."""

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

    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code == 200:
        return response.json()

    logging.info('Body position get request unsuccessful.')
    return APIError("Unsuccessful request.", response.status_code)


def make_clean_body_dict(entry: dict) -> dict:
    """Creates refined body data from astronomy API body data."""

    clean_dict = {}
    clean_dict["timestamp"] = entry["date"]
    clean_dict["body_name"] = entry["id"]
    clean_dict["distance_km"] = entry["distance"]["fromEarth"]["km"]
    clean_dict["azimuth"] = entry["position"]["horizontal"]["azimuth"]["degrees"]
    clean_dict["altitude"] = entry["position"]["horizontal"]["altitude"]["degrees"]
    clean_dict["constellation_name"] = entry["position"]["constellation"]["id"]

    return clean_dict


def refine_bodies_data(bodies: dict) -> list:
    """Removes unnecessary data from the astronomy positions dict."""

    rows = bodies["data"]["table"]["rows"]

   # Each cell contains a list of dictionaries of an entry
   # key and a single body over a set number of days (7)
    output_list = []
    for obj in rows:
        for entry in obj["cells"]:
            altitude = entry["position"]["horizontal"]["altitude"]["degrees"]
            if float(altitude) > 5.0:
                clean_dict = make_clean_body_dict(entry)
                output_list.append(clean_dict)

    return output_list


def get_moon_phase(input_date: str) -> str:
    """Returns a url for an image of the moon phase for a given date."""

    request_body = {
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

    try:
        response = requests.post(url, headers=headers, json=request_body,
                                 timeout=10)

        if response.status_code == 200:
            return response.json()["data"]["imageUrl"]

        logging.info('Moon phase post request unsuccessful.')
        return APIError("Unsuccessful request.", response.status_code)

    except ex.ReadTimeout:
        logging.info("Star chart API request failed.")
        return None


# def get_star_chart(input_date: str, constellation: str) -> str:
#     """Returns a url for an image of the moon phase for a given date."""

#     print("Request started.")

#     request_body = {
#         "style": "default",
#         "observer": {
#             "latitude": 53.812207,
#             "longitude": -2.917976,
#             "date": f"{input_date}"
#         },
#         "view": {
#             "type": "constellation",
#             "parameters": {
#                 "constellation": constellation
#             }
#         }
#     }

#     url = f"{ASTRO_URL}/studio/star-chart"

#     auth_string = get_auth_string()

#     headers = {"Authorization": f"Basic {auth_string}"}

#     try:
#         response = requests.post(url, headers=headers, json=request_body,
#                                  timeout=7)
#         if response.status_code == 200:
#             return response.json()["data"]["imageUrl"]

#         logging.info('Moon phase post request unsuccessful.')
#         return APIError("Unsuccessful request.", response.status_code)

#     except ex.ReadTimeout:

#         logging.info("Star chart API request failed.")
#         return None


def get_const_list():

    with get_db_connection() as conn:
        cur = conn.cursor()

        cur.execute("SELECT constellation_short_name from constellation;")

        res = cur.fetchall()

    constellations = [c["constellation_short_name"].lower() for c in res]

    return constellations


# def get_star_chart_urls(start: date) -> list[dict]:
#     """Returns list of moon phase URLs from the Astronomy API"""
#     output_list = []

#     constellations = get_const_list()

#     for n in range(7):
#         for const in constellations:
#             star_chart_dict = {}
#             day = start + timedelta(days=n)
#             chart_url = get_star_chart(day, const)

#             star_chart_dict["day"] = str(day)
#             star_chart_dict["url"] = chart_url

#             output_list.append(star_chart_dict)

#     return output_list


async def get_star_chart(input_date: str, constellation: str) -> str:
    """Returns a URL for an image of the star chart for a given date asynchronously."""

    request_body = {
        "style": "default",
        "observer": {
            "latitude": 53.812207,
            "longitude": -2.917976,
            "date": input_date
        },
        "view": {
            "type": "constellation",
            "parameters": {
                "constellation": constellation
            }
        }
    }

    url = f"{ASTRO_URL}/studio/star-chart"

    auth_string = get_auth_string()
    headers = {"Authorization": f"Basic {auth_string}"}

    try:
        # Make the asynchronous request
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=request_body, timeout=50) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["data"]["imageUrl"]

                logging.info('Star chart post request unsuccessful.')
                return None

    except asyncio.TimeoutError:
        logging.info("Star chart API request failed due to timeout.")
        return None

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return None


async def get_star_chart_urls(start: date) -> list[dict]:
    """Returns list of star chart URLs from the Astronomy API asynchronously."""
    output_list = []
    constellations = get_const_list()

    tasks = []

    for n in range(7):
        for const in constellations:
            day = start + timedelta(days=n)
            task = get_star_chart(str(day), const)
            tasks.append(task)

    chart_urls = await asyncio.gather(*tasks)

    for i, url in enumerate(chart_urls):
        day = start + timedelta(days=i // len(constellations))
        output_list.append({
            "day": str(day),
            "url": url
        })

    return output_list


def get_position_data(input_dict: dict, times: list[str], regions: list[dict],
                      start_date: date, end_date: date) -> dict:
    """Returns all positional data for astronomical bodies as dictionary."""

    output_dict = input_dict.copy()

    for region in regions:

        region_id = region["region_id"]
        lat = region["latitude"]
        long = region["longitude"]

        for time in times:

            bodies_pos = get_all_body_positions(
                start_date, end_date, lat, long, time)

            refined_pos = refine_bodies_data(bodies_pos)

            output_dict[region_id][time[:2]] = refined_pos

    return output_dict


def get_moon_urls(start: date) -> list[dict]:
    """Returns list of moon phase URLs from the Astronomy API"""
    output_list = []

    for n in range(7):
        moon_day_dict = {}
        day = start + timedelta(days=n)
        phase_url = get_moon_phase(day)

        moon_day_dict["day"] = str(day)
        moon_day_dict["url"] = phase_url

        output_list.append(moon_day_dict)

    return output_list


def fill_region_time_dict(times_list: list[str],
                          region_list: list[dict]) -> dict:
    """Creates framework for body position dictionary."""
    region_ids = [region["region_id"] for region in region_list]
    time_ids = [time[:2] for time in times_list]

    output_dict = {}

    for num in region_ids:
        output_dict[num] = {}
        for time in time_ids:
            output_dict[num][time] = {}

    return output_dict


def save_to_file(filename: str, data: list[dict]) -> None:
    """Save the data to a file called stories.json"""

    with open(filename, "w", encoding="utf-8") as f_obj:
        json.dump(data, f_obj, indent=4)


async def extract_weekly_astronomy_data():
    """Main function for extracting astronomical data for a week"""

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

    # Await the asynchronous get_star_chart_urls function
    final_dict["star_chart_urls"] = await get_star_chart_urls(start_date)
    logging.info("Star chart data extracted.")

    return final_dict


if __name__ == "__main__":

    time1 = datetime.now()

    res = asyncio.run(extract_weekly_astronomy_data())

    print(f"Time: {(datetime.now() - time1).seconds}")
