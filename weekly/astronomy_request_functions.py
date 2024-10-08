"""File to extract sample APi data for database experimentation"""

from os import environ as ENV
from datetime import datetime, date, timedelta
import base64
import json

from dotenv import load_dotenv
import requests

load_dotenv()

ASTRO_URL = "https://api.astronomyapi.com/api/v2"

start_date = date.today()
end_date = start_date + timedelta(days=7)
lat = 51.523350
long = -0.077440
elev = 32
eg_time = "08:00:00"


##### ASTRONOMY FUNCTIONS #####

def get_astronomy_all_body_positions(start_date=start_date, end_date=end_date,
                                     lat=lat, long=long, elev=elev, eg_time=eg_time):

    url = f"{ASTRO_URL}/bodies/positions?latitude={lat}&longitude={
        long}&elevation={elev}&from_date={start_date}&to_date={end_date}&time={eg_time}"

    user_pass = f"{ENV["ASTRONOMY_ID"]}:{ENV["ASTRONOMY_SECRET"]}"

    auth_string = base64.b64encode(user_pass.encode()).decode()

    headers = {"Authorization": f"Basic {auth_string}"}

    return (requests.get(url, headers=headers)).json()


def get_astronomy_one_body_position(body_name="moon", start_date=start_date, end_date=end_date,
                                    lat=lat, long=long, elev=elev, eg_time=eg_time):

    url = f"{ASTRO_URL}/bodies/positions/{body_name}?latitude={lat}&longitude={
        long}&elevation={elev}&from_date={start_date}&to_date={end_date}&time={eg_time}"

    user_pass = f"{ENV["ASTRONOMY_ID"]}:{ENV["ASTRONOMY_SECRET"]}"

    auth_string = base64.b64encode(user_pass.encode()).decode()

    headers = {"Authorization": f"Basic {auth_string}"}

    return (requests.get(url, headers=headers)).json()


def get_astronomy_body_events(body_name="moon", start_date=start_date, end_date=end_date,
                              lat=lat, long=long, elev=elev, eg_time=eg_time):

    url = f"{ASTRO_URL}/bodies/events/{body_name}?latitude={lat}&longitude={
        long}&elevation={elev}&from_date={start_date}&to_date={end_date}&time={eg_time}"

    user_pass = f"{ENV["ASTRONOMY_ID"]}:{ENV["ASTRONOMY_SECRET"]}"

    auth_string = base64.b64encode(user_pass.encode()).decode()

    headers = {"Authorization": f"Basic {auth_string}"}

    return (requests.get(url, headers=headers)).json()


def get_star_chart():

    example_body = {
        "style": "default",
        "observer": {
            "latitude": lat,
            "longitude": long,
            "date": f"{date.today()}"
        },
        "view": {
            "type": "constellation",
            "parameters": {
                "constellation": "ori"  # 3 letter constellation ID
            }
        }
    }

    url = f"{ASTRO_URL}/studio/star-chart"

    user_pass = f"{ENV["ASTRONOMY_ID"]}:{ENV["ASTRONOMY_SECRET"]}"

    auth_string = base64.b64encode(user_pass.encode()).decode()

    headers = {"Authorization": f"Basic {auth_string}"}

    return requests.post(url, headers=headers, json=example_body).json()["data"]["imageUrl"]


def get_moon_phase():

    example_body = {
        "format": "png",
        "style": {
            "moonStyle": "default",
            "backgroundStyle": "stars",
            "headingColor": "white",
            "textColor": "white"
        },
        "observer": {
            "latitude": lat,
            "longitude": long,
            "date": f"{date.today()}"
        },
        "view": {
            "type": "portrait-simple",
            "orientation": "north-up"
        }
    }

    url = f"{ASTRO_URL}/studio/moon-phase"

    user_pass = f"{ENV["ASTRONOMY_ID"]}:{ENV["ASTRONOMY_SECRET"]}"

    auth_string = base64.b64encode(user_pass.encode()).decode()

    headers = {"Authorization": f"Basic {auth_string}"}

    return requests.post(url, headers=headers, json=example_body).json()["data"]["imageUrl"]
