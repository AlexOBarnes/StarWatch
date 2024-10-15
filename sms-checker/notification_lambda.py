'''This script contains the lambda handler for this pipeline'''
import logging
from dotenv import load_dotenv
from checker import get_subscribers
from message import send_email,send_sms

def lambda_handler(event,context) -> None:
    '''Runs the notification pipeline'''
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    subscribers = get_subscribers()
    email_list = [entry for entry in subscribers if entry['email']]
    phone_list = [entry for entry in subscribers if entry['phone']]
    if email_list:
        send_email(email_list)
    if phone_list:
        send_sms(phone_list)

if __name__ == '__main__':
    lambda_handler({},{})
    