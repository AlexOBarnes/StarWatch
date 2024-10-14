import re
import os

from dotenv import load_dotenv
import streamlit as st
import psycopg2
from datetime import datetime
import urllib


load_dotenv()

# Database connection setup (for the subscriber page

def connect_to_db():
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
    st.write('Please provide either a valid email or UK phone number to sign up.')

    # A basic Streamlit input form, for a username and at least an email or phone number.
    username = st.text_input('Desired Username', '')
    email = st.text_input('Email Address', '')
    phone = st.text_input('Phone Number (UK)', '')

    if st.button('Submit'):
        # Ensure username, either email or phone is provided
        if not username:
            st.error('Please provide a username.')

        elif not email and not phone:
            st.error('Please provide either an email or a phone number.')

        elif email and not validate_email(email):

            st.error('Invalid email format. Please enter a valid email.')
        elif phone and not validate_phone(phone):

            st.error('Invalid UK phone number format. It must start with +44 or 0 followed by 10 digits.')
        
        else:
            try:
                with connect_to_db() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute('''
                            INSERT INTO subscriber (subscriber_username, subscriber_phone, subscriber_email) 
                            VALUES (%s, %s, %s);
                        ''', (username, phone if phone else None, email if email else None)) # Using tertiary statements to account for None(s).
                    conn.commit()  # Commiting the valid user information to the 'subscriber' table in the RDS.
                st.success('Subscriber added successfully!')
            except Exception as e:
                st.error(f'Error adding subscriber: {e}')