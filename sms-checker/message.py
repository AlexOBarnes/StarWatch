'''This script will message the subscribers if they require notification'''
import logging
from dotenv import load_dotenv
from boto3 import client

def send_sms(subscriber: dict) -> None:
    '''Uses boto3 to send messages to subscribers by sms'''
    ...

def send_email(subscriber: dict) -> None:
    '''Uses boto3 to send messages to subscribers by ses'''
    ...

def get_client(service: str) -> client:
    '''Returns a AWS client'''
    ...

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    send_sms({})
    send_email({})