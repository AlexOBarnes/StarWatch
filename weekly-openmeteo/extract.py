'''Extracts weekly sunset and sunrise data for the 12 UK regions'''
import logging
from os import environ as ENV
import requests
from dotenv import load_dotenv

URL = '''https://open-meteo.com/en/docs#
latitude=54.61,56.49,52.13,54.97,53.78,53.8,52.9,52.48,52.24,51.51,51.28,50.78&
longitude=-6.62,-4.2,-3.78,-1.61,-2.7,-1.54,-1.23,-1.89,0.9,-0.13,-0.78,-3.79&
hourly=&daily=sunrise,sunset&timezone=Europe%2FLondon'''

def extract() -> dict:
    '''Returns the solar data for the given set of coordinates'''
    ...

if __name__ == '__main__':