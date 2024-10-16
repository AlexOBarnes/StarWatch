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
from aurora_map import create_aurora_map, create_visibility_map
from azimuth_plot import make_sky_plot, get_bodies, get_star_chart, get_regions

load_dotenv()
st. set_page_config(layout="wide")


# Database connection setup (for the subscriber page


def validate_email(email: str) -> bool:
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


def validate_phone_number(phone_number: str, region='GB') -> bool:
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
page = st.sidebar.selectbox('Navigate', ['Home', 'Weather', 'Astronomy', 'Stellarium', 'Subscriber Signup'])


# Home page, where the user first interacts with the dashboard by default.
if page == 'Home':
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
        st.header('Current Visibility')
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
       st.warning(
           "Please select a valid start and end date for the visualisation date range.")
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
           filtered_df['cloud_coverage_rolling'] = filtered_df['cloud_coverage_percent'].rolling(
               window=24).mean()
           filtered_df['visibility_rolling'] = filtered_df['visibility_m'].rolling(
               window=24).mean()
           filtered_df['temperature_rolling'] = filtered_df['temperature_c'].rolling(
               window=24).mean()
           filtered_df['precipitation_prob_rolling'] = filtered_df['precipitation_probability_percent'].rolling(
               window=24).mean()
           filtered_df['precipitation_mm_rolling'] = filtered_df['precipitation_mm'].rolling(
               window=24).mean()

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
               y=alt.Y('cloud_coverage_rolling:Q',
                       title='Cloud Coverage (%) (Rolling Average)'),
               tooltip=['at:T', 'cloud_coverage_rolling']
           )
           cloud_chart += rolling_avg_line

       # The visibility visualisation.
       visibility_chart = alt.Chart(filtered_df).mark_line(color="blue").encode(
           x=alt.X('at:T', title='Time'),
           y=alt.Y('visibility_m:Q', title='Visibility (m)',
                   scale=alt.Scale(type='log')),
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
               y=alt.Y('visibility_rolling:Q',
                       title='Visibility (m) (Rolling Average)'),
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
               y=alt.Y('temperature_rolling:Q',
                       title='Temperature (°C) (Rolling Average)'),
               tooltip=['at:T', 'temperature_rolling']
           )
           temperature_chart += rolling_avg_line

       # Precipitation probability (%) and precipitation level (mm) visualisation.

       # Precipitation probability on the left y-axis
       precipitation_prob_chart = alt.Chart(filtered_df).mark_line(color='blue').encode(
           x=alt.X('at:T', title='Time'),
           y=alt.Y('precipitation_probability_percent:Q',
                   title='Precipitation Probability (%)'),
           tooltip=['at:T', 'precipitation_probability_percent']
       ).properties(
           width=1000,
           height=500
       )

       # Precipitation amount (mm) on the right y-axis.
       precipitation_mm_chart = alt.Chart(filtered_df).mark_line(color='green').encode(
           x=alt.X('at:T', title='Time'),
           y=alt.Y('precipitation_mm:Q', title='Precipitation (mm)'),
           tooltip=['at:T', 'precipitation_mm']
       )

       precipitation_chart = alt.layer(
           precipitation_prob_chart,
           precipitation_mm_chart
       ).resolve_scale(
           y='independent'
       ).properties(
           title="Precipitation Probability (%) and Precipitation (mm) Over Time"
       )

       col1, col2 = st.columns(2)
       # Display all charts in a single column
       with col1:
           st.altair_chart(cloud_chart, use_container_width=True)
           st.altair_chart(visibility_chart, use_container_width=True)

       with col2:
           st.altair_chart(temperature_chart, use_container_width=True)
           st.altair_chart(precipitation_chart, use_container_width=True)


elif page == 'Stellarium':

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

   def generate_stellarium_url(lat: str, lon: str, dt: datetime) -> str:
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

       st.markdown(
           f'**Current Date & Time:** {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}')


elif page == 'Subscriber Signup':
   # Markdown is unnecessary here, as Streamlit enlarges the title by default.
   st.title('Subscriber Sign Up')
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
       selected_counties = st.multiselect(
           'Select From County List', options=county_map.keys())

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
           st.error(
               '🛑 Invalid UK phone number format. It must start with +44 followed by 10 digits or 07 followed by 9 digits.')

       # Subscribers need to be mapped to a specific county(ies), otherwise the service is meaningless.
       elif not selected_counties:
           st.error(
               '🛑 Please select a county to subscribe to, so we can send you relevant notifications.')

       else:
           try:
               with conn:
                   with conn.cursor() as cursor:
                       cursor.execute('''
                           INSERT INTO subscriber (subscriber_username, subscriber_phone, subscriber_email)
                           VALUES (%s, %s, %s)
                           RETURNING subscriber_id;
                       ''', (username, user_phone if user_phone else None, user_email if user_email else None))  # Using tertiary statements to account for None(s).

                       subscriber_id = cursor.fetchone()[0]
                       print(subscriber_id)

                       # Retrieve county IDs for the county names selected in the dashboard.
                       selected_county_ids = [county_map[county]
                                              for county in selected_counties]

                       # Flattening insertion values for bulk insertion into the subscriber_county_assignment table.
                       county_tuples = [(subscriber_id, county_id)
                                        for county_id in selected_county_ids]

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
               st.error(
                   '🛑 Username already exists. Please choose a different username.')
           # In the event of any other generalised error, this serves as some basic error handling that is formatted in a pretty way.
           except Exception as e:
               st.error(f'Error adding subscriber: {e}')


elif page == 'Astronomy':
    conn = connect_to_db()
    bodies = [body[0] for body in get_bodies()]
    selected_body = st.selectbox("Select body", bodies)
    col1, col2 = st.columns(2)
    with col1:
       ...
    with col2:
        st.header(f'{selected_body} star chart')
        starchart,constellation = get_star_chart(selected_body)
        if starchart:
            st.write(f'Tonight {selected_body} will be visible in the {constellation} constellation.')
            st.image(starchart)
        else:
            st.write('No star chart is available for this celestial body tonight')
    
    regions = [region[0] for region in get_regions()]
    region = st.selectbox("Select region", regions)
    col1,col2 = st.columns(2)
    with col1:
        ...
    with col2:
        selected_date = st.date_input(
            "Select a date:",
            value=date.today(),
            min_value=date(2024, 10, 7),
            max_value=date(2100, 12, 31)
        )
        animation_data = make_sky_plot(
            region, datetime.combine(selected_date, datetime.min.time()))
        st.header(f'Skyplot for {region} on {datetime.combine(
            selected_date, datetime.min.time()).strftime('%d/%m/%y')} ')
        if animation_data:
            st.video(animation_data, format='.mp4')
        else:
            st.write('No skyplot is available for this region on this date')
