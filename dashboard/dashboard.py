#pylint:disable=line-too-long, invalid-name, broad-exception-caught,possibly-used-before-assignment,no-member
'''Streamlit dashboard for the StarWatch project.'''

from datetime import datetime
import urllib

from dotenv import load_dotenv
import streamlit as st
import psycopg2
from psycopg2.extras import execute_values
import pandas as pd
import altair as alt
from email_validator import validate_email as ve, EmailNotValidError
import phonenumbers
from phonenumbers import NumberParseException
import numpy as np

from load_dashboard_data import connect_to_db, load_from_starwatch_rds, load_forecasts_by_county_name


load_dotenv()
st. set_page_config(layout="wide")

# Database connection setup (for the subscriber page


def validate_email(email:str) -> bool:
    '''
    Validates an email address to RFC 5322 standards using the 
    email_validator Python library. Returns True if the email
    passed in can be considered valid, and False if an error
    is raised due to the email being unvalid.
    '''

    try:
        ve(email)
        return True
    except EmailNotValidError:
        return False


def validate_phone_number(phone_number:str, region='GB') -> bool:
    '''
    Validates a UK phone number format, with and without country code:
    
    - With the +44 country code: +44 followed by 10 digits (e.g., +44 1234567890)
    - Without the country code: 0 followed by 10 digits (e.g., 01234567890

    Returns True if the phone number passed in can be considered valid, and False 
    if an error is raised due to the phone number being unvalid.
    '''

    try:
        parsed_number = phonenumbers.parse(phone_number, region)
        return phonenumbers.is_valid_number(parsed_number)
    except NumberParseException:
        return False


# This defines a navigation sidebar for the pages on the Streamlit dashboard.
page = st.sidebar.selectbox('Navigate', ['Home', 'Weather', 'Stellarium Integration' ,'Subscriber Signup', 'Test'])

# Home page, where the user first interacts with the dashboard by default.
if page == 'Home':
    st.title('⭐ Starwatch Data Dashboard ⭐')


# The part of the dashboard visualising weather and its effect on stargazing.
elif page == 'Weather':
    st.title('⛅ Weather Data Dashboard 🌨️')

    conn = connect_to_db()
    # Loading all weather forecasts, joined by county ID to county names.
    data = load_forecasts_by_county_name(conn)

    df = pd.DataFrame(data)

    forecast_df = pd.DataFrame(data)

    # Ensuring there are no duplicate columns that can cause problems, as we joined on 'county_id'.
    forecast_df.columns = forecast_df.columns.str.replace(r'.1', '', regex=True)
    if forecast_df.columns.duplicated().any():
        forecast_df = forecast_df.loc[:, ~forecast_df.columns.duplicated()]

    forecast_df['at'] = pd.to_datetime(forecast_df['at'])

    # Extract just the date from the datetime for filtering purposes.
    forecast_df['date'] = forecast_df['at'].dt.date

    # Title of the weather page.
    st.title("Forecast Data Visualisation")

    county_names = forecast_df['county_name'].unique()
    selected_county = st.selectbox("Select County", county_names)

    # Let users select a date or date range for the forecast data.
    selected_dates = st.date_input(
        "Select Date or Date Range",
        [forecast_df['date'].min(), forecast_df['date'].max()]
    )

    # Initialise start_date and end_date, so the below if-clause holds.
    start_date = end_date = None

    # Check if the user selected only one date (i.e. they haven't picked an end date)
    if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
        start_date, end_date = selected_dates
    elif isinstance(selected_dates, tuple) and len(selected_dates) == 1:
        # User only selected one date, show a clearer warning.
        st.warning("Please select a valid start and end date for the visualisation date range.")
    else:
        start_date = end_date = selected_dates  # Single day selection

    if start_date and end_date:
    # Filter the forecast DataFrame based on the selected date(s) and county
        filtered_df = forecast_df[
            (forecast_df['date'] >= start_date) &
            (forecast_df['date'] <= end_date) &
            (forecast_df['county_name'] == selected_county)
        ]

        # A rolling average can only be applied if there's filtered data to apply it to.
        if not filtered_df.empty:
            # Apply rolling mean for smoother lines (adjust window size)
            filtered_df['cloud_coverage_rolling'] = filtered_df['cloud_coverage_percent'].rolling(window=24).mean()
            filtered_df['visibility_rolling'] = filtered_df['visibility_m'].rolling(window=24).mean()
            filtered_df['temperature_rolling'] = filtered_df['temperature_c'].rolling(window=24).mean()

        # Check if a single day is selected
        is_single_day = start_date == end_date

        # The cloud coverage visualisation.
        cloud_chart = alt.Chart(filtered_df).mark_line().encode(
            x=alt.X('at:T', title='Time'),
            y=alt.Y('cloud_coverage_percent:Q', title='Cloud Coverage (%)'),
            tooltip=['at:T', 'cloud_coverage_percent']
        ).properties(
            width=1000,
            height=500,
            title='Cloud Coverage Over Time (Real vs. Rolling Average)'
        )

        # If it's a single day, add small points to the visualisation for clarity.
        if is_single_day:
            points = alt.Chart(filtered_df).mark_point(size=30, color="lightblue").encode(
                x='at:T',
                y='cloud_coverage_percent:Q',
                tooltip=['at:T', 'cloud_coverage_percent']
            )
            cloud_chart += points
        else:
            rolling_avg_line = alt.Chart(filtered_df).mark_line(color="white", opacity=0.28).encode(
                x='at:T',
                y=alt.Y('cloud_coverage_rolling:Q', title='Cloud Coverage (%) (Rolling Average)'),
                tooltip=['at:T', 'cloud_coverage_rolling']
            )
            cloud_chart += rolling_avg_line



        # The visibility visualisation.
        visibility_chart = alt.Chart(filtered_df).mark_line(color="blue").encode(
            x=alt.X('at:T', title='Time'),
            y=alt.Y('visibility_m:Q', title='Visibility (m)', scale=alt.Scale(type='log')),
            tooltip=['at:T', 'visibility_m']
        ).properties(
            width=1000,
            height=500,
            title='Visibility Over Time (Real vs. Rolling Average)'
        )

        if is_single_day:
            points = alt.Chart(filtered_df).mark_point(size=30, color="blue").encode(
                x='at:T',
                y='visibility_m:Q',
                tooltip=['at:T', 'visibility_m']
            )
            visibility_chart += points
        else:
            rolling_avg_line = alt.Chart(filtered_df).mark_line(color="white", opacity=0.28).encode(
                x='at:T',
                y=alt.Y('visibility_rolling:Q', title='Visibility (m) (Rolling Average)'),
                tooltip=['at:T', 'visibility_rolling']
            )
            visibility_chart += rolling_avg_line


        # The temperature visualisation.
        temperature_chart = alt.Chart(filtered_df).mark_line(color="#D9372A").encode(
            x=alt.X('at:T', title='Time'),
            y=alt.Y('temperature_c:Q', title='Temperature (°C)'),
            tooltip=['at:T', 'temperature_c']
        ).properties(
            width=1000,
            height=500,
            title='Temperature Over Time (Real vs. Rolling Average)'
        )

        if is_single_day:
            points = alt.Chart(filtered_df).mark_point(size=30, color="#D9372A").encode(
                x='at:T',
                y='temperature_c:Q',
                tooltip=['at:T', 'temperature_c']
            )
            temperature_chart += points
        else:
            rolling_avg_line = alt.Chart(filtered_df).mark_line(color="white", opacity=0.28).encode(
                x='at:T',
                y=alt.Y('temperature_rolling:Q', title='Temperature (°C) (Rolling Average)'),
                tooltip=['at:T', 'temperature_rolling']
            )
            temperature_chart += rolling_avg_line


        # col1, col2, col3 = st.columns(3)
        # # Display all charts in a single column
        # with col1:
        st.altair_chart(cloud_chart, use_container_width=True)
        st.altair_chart(visibility_chart, use_container_width=True)
        st.altair_chart(temperature_chart, use_container_width=True)


elif page == 'Stellarium Integration':

    st.markdown('''
    This dashboard provides an interactive view of the night sky as seen from **London**. The view updates automatically to reflect the current date and time.
    ''')

    # General coordinates for London, Liverpool street.
    DEFAULT_LATITUDE = 51.5074
    DEFAULT_LONGITUDE = -0.1278

    # Unless a specific location is provided, London used as a default.
    if 'latitude' not in st.session_state:
        st.session_state['latitude'] = DEFAULT_LATITUDE
    if 'longitude' not in st.session_state:
        st.session_state['longitude'] = DEFAULT_LONGITUDE


    def generate_stellarium_url(lat:str, lon:str, dt:datetime) -> str:
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


    def get_current_datetime() -> datetime:
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



elif page == 'Subscriber Signup':
    st.title('Subscriber Sign Up') # Markdown is unnecessary here, as Streamlit enlarges the title by default.
    st.write('Please provide either a valid email or UK phone number to sign up. ')
    st.write("Please also select the counties you'd like to be notified for.")



    # A basic Streamlit input form, for a username and at least an email or phone number.
    username = st.text_input('Desired Username', '')
    user_email = st.text_input('Email Address', '')
    user_phone = st.text_input('Phone Number (UK)', '')


    # Establishing a connection instance for a given refresh.
    conn = connect_to_db()

    # Reading from the StarWatch database to retrieve all static country names and IDs.
    counties = load_from_starwatch_rds(conn, 'county')

    # not counties.empty is used here as 'not' as an indication of truthiness, cannot be applied to an entire DataFrame.
    if not counties.empty:
        # A hashmap mapping county names to county IDs for the multi-select dropdown box.
        # Flattening the county DataFrame for its names.
        county_map = counties.set_index('county_name')['county_id'].to_dict()
        selected_counties = st.multiselect('Select From County List', options=county_map.keys())

    # Create a mapping dictionary: {county_name: county_id}

    else:
        # Basic error handling in a way that is visually aesthetic to the dashboard.
        # There will be static county data to pull from in all likelihood, but just in case.
        county_options = []
        st.warning('There are currently no available counties for selection.')


    # The logic for what happens when a user presses the 'Submit' button in the Streamlit dashboard.
    if st.button('Submit'):
        # Ensure username, either email or phone is provided
        if not username:
            st.error('🛑 Please provide a username.')

        # Either a phone number or emails as to be provided.
        elif not user_email and not user_phone:
            st.error('🛑 Please provide either an email or a phone number.')

        elif user_email and not validate_email(user_email):
            st.error('🛑 Invalid email format. Please enter a valid email.')
        elif user_phone and not validate_phone_number(user_phone):
            st.error('🛑 Invalid UK phone number format. It must start with +44 followed by 10 digits or 07 followed by 9 digits.')

        # Subscribers need to be mapped to a specific county(ies), otherwise the service is meaningless.
        elif not selected_counties:
            st.error('🛑 Please select a county to subscribe to, so we can send you relevant notifications.')

        else:
            try:
                with conn:
                    with conn.cursor() as cursor:
                        cursor.execute('''
                            INSERT INTO subscriber (subscriber_username, subscriber_phone, subscriber_email) 
                            VALUES (%s, %s, %s)
                            RETURNING subscriber_id;
                        ''', (username, user_phone if user_phone else None, user_email if user_email else None)) # Using tertiary statements to account for None(s).


                        subscriber_id = cursor.fetchone()[0]
                        print(subscriber_id)

                        # Retrieve county IDs for the county names selected in the dashboard.
                        selected_county_ids = [county_map[county] for county in selected_counties]

                        # Flattening insertion values for bulk insertion into the subscriber_county_assignment table.
                        county_tuples = [(subscriber_id, county_id) for county_id in selected_county_ids]

                        # Bulk inserting values for efficiency, in the case where a single subscriber selects multiple counties.
                        execute_values(cursor, '''
                            INSERT INTO subscriber_county_assignment (subscriber_id, county_id)
                            VALUES %s;
                        ''', county_tuples)


                    # Commiting the valid user information to the 'subscriber' table in the RDS,
                    # while also mapping that subscriber instance to their associated county ID.
                    conn.commit()
                st.success('✅ Your subscription has been added successfully!')

            # If there's an error from the database itself, it will be due to a UNIQUE schema violation.
            except psycopg2.errors.UniqueViolation:
                st.error('Username already exists. Please choose a different username.')
            # In the event of any other generalised error, this serves as some basic error handling that is formatted in a pretty way.
            except Exception as e:
                st.error(f'Error adding subscriber: {e}')

elif page == 'Test':


    def calculate_visibility(test_max_visibility, test_cloud_coverage, test_time_step, test_orbital_frequency):
        orbital_effect = np.sin(2 * np.pi * test_orbital_frequency * test_time_step)
        visibility = test_max_visibility * (1 - test_cloud_coverage / 100) * (0.5 + 0.5 * orbital_effect)
        return visibility

    bodies = ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Moon', 'Pluto']
    max_visibilities = [12000, 25000, 30000, 20000, 18000, 15000, 13000, 30000, 10000]
    orbital_frequencies = [0.2, 0.1, 0.05, 0.07, 0.03, 0.02, 0.01, 0.5, 0.005]

    start_date = pd.Timestamp('2024-11-01')
    end_date = pd.Timestamp('2024-11-30')
    days = pd.date_range(start=start_date, end=end_date, freq='D')

    data = []
    for body, max_visibility, frequency in zip(bodies, max_visibilities, orbital_frequencies):
        for i, day in enumerate(days):
            cloud_coverage = np.random.randint(0, 100)
            visibility = calculate_visibility(max_visibility, cloud_coverage, i, frequency)
            data.append({
                'body_name': body,
                'date': day,
                'max_visibility_m': max_visibility,
                'cloud_coverage_percent': cloud_coverage,
                'visibility_m': visibility
            })


    visibility_df = pd.DataFrame(data)

    source = pd.DataFrame({
        'x': visibility_df['date'].dt.date,  
        'y': visibility_df['body_name'],     
        'z': visibility_df['visibility_m']    
    })


    heatmap = alt.Chart(source).mark_rect().encode(
        x=alt.X('x:O', title='Date', axis=alt.Axis(labels=False, ticks=False)),
        y=alt.Y('y:O', title='Celestial Body'),
        color=alt.Color('z:Q',
                        scale=alt.Scale(domain=[0, 30000],
                                        range=['#fff5eb', '#ff0000', '#800080']),
                        title='Visibility (m)'),
        tooltip=['y', 'x:T', 'z']
    ).properties(
        width=2000,
        height=500,
        title='Daily Visibility of Celestial Bodies'
    )

    col1, col2, col3 = st.columns(3)
    with col2:
        st.altair_chart(heatmap, use_container_width=True)
