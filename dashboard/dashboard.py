#pylint:disable=line-too-long, invalid-name, broad-exception-caught
'''Streamlit dashboard for the StarWatch project.'''

import re
import os
from datetime import datetime
import urllib

from dotenv import load_dotenv
import streamlit as st
import psycopg2
import pandas as pd
import altair as alt


load_dotenv()

# Database connection setup (for the subscriber page

def connect_to_db():
    '''Returns a psycopg2 connection object'''

    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )

def validate_email(email):
    '''
    Validates an email address using an RFC 5322 compliant regex.
    Returns a re match object if valid, None if invalid.
    '''

    email_regex = r'''
        (?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+  
        (?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*) 
        |                                
        '(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f] 
        |\\[\x01-\x09\x0b\x0c\x0e-\x7f])*')  
        @                               
        (?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+ 
        [a-z0-9](?:[a-z0-9-]*[a-z0-9])?           
        |                                
        \[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]
        |[1-9]?[0-9]))\.){3}
        (?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]
        |[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:       
        (?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]
        |\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])  
    '''
    return re.match(email_regex, email, re.VERBOSE)


def validate_phone(phone):
    '''
    Validates a UK phone number format, with and without country code:
    
    - With the +44 country code: +44 followed by 10 digits (e.g., +44 1234567890)
    - Without the country code: 0 followed by 10 digits (e.g., 01234567890

    Returns a re match object if valid, None if invalid.
    '''

    phone_regex = r'^(\+44\d{10}|0\d{10})$'
    return re.match(phone_regex, phone)


# This defines a navigation sidebar for the pages on the Streamlit dashboard.
page = st.sidebar.selectbox('Navigate', ['Home', 'Subscriber Signup'])


# Home page, where the user first interacts with the dashboard by default.
if page == 'Home':
    st.title('⭐ Starwatch Data Dashboard ⭐')

    st.markdown('''
    This dashboard provides an interactive view of the night sky as seen from **London**. The view updates automatically to reflect the current date and time.
    ''')

    # General coordinates for London
    DEFAULT_LATITUDE = 51.5074
    DEFAULT_LONGITUDE = -0.1278

    # Unless a specific location is provided, London used as a default.
    if 'latitude' not in st.session_state:
        st.session_state['latitude'] = DEFAULT_LATITUDE
    if 'longitude' not in st.session_state:
        st.session_state['longitude'] = DEFAULT_LONGITUDE


    def generate_stellarium_url(lat, lon, dt):
        '''
        Returns a stellarium URL to be used in an iFrame
        in the Streamlit dashboard.
        '''

        base_url = 'https://stellarium-web.org/'
        params = {
            'lat': lat,
            'lon': lon,
            'date': dt.strftime('%Y-%m-%d'),
            'time': dt.strftime('%H:%M')
        }
        query_string = urllib.parse.urlencode(params)
        full_url = f'{base_url}?{query_string}'
        return full_url

    def get_current_datetime():
        '''Returns the current time as a datetime object.'''
        return datetime.now()

    # The Stellarium iFrame is stored in a Streamlit container.
    with st.container():

        st.markdown('## Interactive Night Sky View')

        current_datetime = get_current_datetime()

        stellarium_url = generate_stellarium_url(
            DEFAULT_LATITUDE,
            DEFAULT_LONGITUDE,
            current_datetime
        )

        st.components.v1.html(f'''
        <iframe src='{stellarium_url}' style='width: 100%; height: 600px; border: none;'></iframe>
        ''', height=600)

        st.markdown(f'**Current Date & Time:** {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}')



    conn = connect_to_db()

    with conn:
        with conn.cursor() as cur:
            query = """
            SELECT *
            FROM forecast
            WHERE at >= '2024-10-11 00:00:00' 
            AND at < '2024-10-12 00:00:00';
            """
            cur.execute(query)
            data = cur.fetchall()

            columns = [desc[0] for desc in cur.description]

    df = pd.DataFrame(data, columns=columns)  # Specify column names
    print(df.head())
    # Create two columns: one for controls, one for the chart
    controls_col, chart_col = st.columns([1, 4], gap="small")  # Adjust the ratio as needed

    with controls_col:
        st.subheader("Select Weather Indicators")
        # Define the available weather indicators and their display names
        weather_indicators = {
            'Temperature (°C)': 'temperature_c',
            'Precipitation Probability (%)': 'precipitation_probability_percent',
            'Precipitation (mm)': 'precipitation_mm',
            'Cloud Coverage (%)': 'cloud_coverage_percent',
            'Visibility (m)': 'visibility_m'
        }

        # Initialize an empty list to hold selected indicators
        selected_indicators = []

        # Create checkboxes for each indicator
        for label, column in weather_indicators.items():
            if st.checkbox(label, value=True):
                selected_indicators.append(column)

    with chart_col:
        if not selected_indicators:
            st.warning("Please select at least one weather indicator to display the chart.")
        else:
            # Melt the dataframe to long format for Altair
            df_melted = df.melt(id_vars=['at'], value_vars=selected_indicators,
                                var_name='Indicator', value_name='Value')

            # Define a color scheme
            color_scheme = alt.Scale(scheme='category10')  # 'category10' is a good default

            # Create the Altair chart
            chart = alt.Chart(df_melted).mark_line(point=True).encode(
                x=alt.X('at:T', title='Timestamp'),
                y=alt.Y('Value:Q', title='Value'),
                color=alt.Color('Indicator:N', title='Weather Indicator', scale=color_scheme),
                tooltip=[
                    alt.Tooltip('at:T', title='Time'),
                    alt.Tooltip('Indicator:N', title='Indicator'),
                    alt.Tooltip('Value:Q', title='Value')
                ]
            ).properties(
                width=700,  # Adjust width as needed
                height=400,
                title="Weather Indicators Over Time"
            ).interactive()  # Enables zooming and panning

            st.altair_chart(chart, use_container_width=True)





elif page == 'Subscriber Signup':
    st.title('Subscriber Sign Up') # Markdown is unnecessary here, as Streamlit enlarges the title by default.
    st.write('Please provide either a valid email or UK phone number to sign up.')

    # A basic Streamlit input form, for a username and at least an email or phone number.
    username = st.text_input('Desired Username', '')
    user_email = st.text_input('Email Address', '')
    user_phone = st.text_input('Phone Number (UK)', '')

    if st.button('Submit'):
        # Ensure username, either email or phone is provided
        if not username:
            st.error('Please provide a username.')

        elif not user_email and not user_phone:
            st.error('Please provide either an email or a phone number.')

        elif user_email and not validate_email(user_email):

            st.error('Invalid email format. Please enter a valid email.')
        elif user_phone and not validate_phone(user_phone):

            st.error('Invalid UK phone number format. It must start with +44 or 0 followed by 10 digits.')

        else:
            try:
                with connect_to_db() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute('''
                            INSERT INTO subscriber (subscriber_username, subscriber_phone, subscriber_email) 
                            VALUES (%s, %s, %s);
                        ''', (username, user_phone if user_phone else None, user_email if user_email else None)) # Using tertiary statements to account for None(s).
                    conn.commit()  # Commiting the valid user information to the 'subscriber' table in the RDS.
                st.success('Subscriber added successfully!')
            except Exception as e:
                st.error(f'Error adding subscriber: {e}')
