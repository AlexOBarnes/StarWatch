# Quadhoral OpenMeteo Pipeline
This folder contains the code for the [OpenMeteo API](https://open-meteo.com/en/docs) data pipeline. This includes `extract.py`, `transform.py`, `load.py` and `pipeline.py`. This pipeline uses the `requests` library to send HTML GET requests to the `OpenMeteo API` and the `psycopg2` library to load this data onto our database. The data requested includes `cloud cover`, `visibility` and `chance of precipitation`, this pipeline is therefore designed to run every four hours to ensure accurate data.

## Setup

## Usage

## How it works