'''Contains the code for the subscribe page of the dashboard'''
import streamlit as st
import psycopg2
from psycopg2.extras import execute_values
from email_validator import validate_email as ve, EmailNotValidError
import phonenumbers
from phonenumbers import NumberParseException
from load_dashboard_data import connect_to_db, load_from_starwatch_rds


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

if __name__ == '__main__':
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
