# pylint:disable=line-too-long, invalid-name, broad-exception-caught,possibly-used-before-assignment,no-member
'''Streamlit dashboard for the StarWatch project.'''
from datetime import datetime,date
import urllib
from io import BytesIO
from dotenv import load_dotenv
import streamlit as st
import psycopg2
from psycopg2.extras import execute_values
import pandas as pd
import altair as alt
from email_validator import validate_email as ve, EmailNotValidError
import phonenumbers
from phonenumbers import NumberParseException
from load_dashboard_data import connect_to_db, load_from_starwatch_rds, load_forecasts_by_county_name, load_celestial_body_information
from nasa_pipeline import nasa_pipeline, get_image_of_the_day, get_iss_location, get_moon_phase
from aurora_map import create_aurora_map, create_visibility_map, create_body_visibility_map
from azimuth_plot import make_sky_plot, get_bodies, get_star_chart, get_regions

load_dotenv()
st.set_page_config(layout="wide")

if __name__ == '__main__':
    st.title('⭐ Starwatch Data Dashboard ⭐')
    st.write("""At StarWatch, we are dedicated to inspiring curiosity about the universe.
            Our mission is to provide accessible tools and resources for amateur astronomers and hobbyists
            stargazers so that anyone can enjoy the wonders of space.""")
   
    col1, col2 = st.columns(2)
    with col1:
        st.header('Current Aurora Status')
        aurora = create_aurora_map()
        if aurora:
            st.pyplot(aurora)
    with col2:
        st.header("Tonight's Visibility")
        visibility = create_visibility_map()
        if visibility:
            st.pyplot(visibility)

    nasa_pipeline()
    image_title, image = get_image_of_the_day()
    iss = get_iss_location()
    col1, col2 = st.columns(2)
    moon = get_moon_phase()
    with col1:
        st.header('Image of the day')
        st.write(f'{image_title} - {datetime.now().strftime("%d/%m/%Y")}')
        if 'youtube' in image:
            st.video(image)
        else:
            st.image(image)

    with col2:
        st.header("Today's Moon Phase")
        st.markdown(
            f"<div style='text-align: center;'><img src='{
                moon}' width='300'></div>",
            unsafe_allow_html=True
        )


    st.header('Current ISS Location')
    st.write(f'Last updated: {
                iss["timestamp"].strftime("%H:%M:%S %d/%m/%Y")}')
    iss_df = pd.DataFrame({
        'latitude': [float(iss['latitude'])],
        'longitude': [float(iss['longitude'])]
    })
    zoom_level = 1.5
    st.map(iss_df, zoom=zoom_level)
    st.write('Data sources:')
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        st.image('images/astronomy.png')
        st.write('[Astronomy API](%s)' % 'https://docs.astronomyapi.com/')
    with col2:
        st.image('images/aurorawatch.png')
        st.write('[Aurorawatch UK](%s)' % 'https://aurorawatch.lancs.ac.uk/')
    with col3:
        st.image('images/iss.png')
        st.write('[ISS](%s)' %
                 'http://open-notify.org/Open-Notify-API/ISS-Location-Now/')
    with col4:
        st.image('images/nasa.png')
        st.write('[NASA](%s)' % 'https://api.nasa.gov/')
    with col5:
        st.image('images/openmeteo.png')
        st.write('[Openmeteo API](%s)' % 'https://open-meteo.com/en/docs')