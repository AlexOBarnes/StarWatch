'''This script will message the subscribers if they require notification'''
import logging
from os import environ as ENV
from dotenv import load_dotenv
from boto3 import client

def send_sms(subscribers: list[dict]) -> None:
    '''Uses boto3 to send messages to subscribers by sms'''
    sms = get_client('sns')
    for sub in subscribers:
        if sub['body']:
            message = 'STARWATCH ALERT'
            message += f'\n\n Hello {sub['user'].capitalize()},\n\n'
            if not sub['at']:
                message += f"{sub['body'].capitalize()} will be visible tonight in your county!"
            else:
                message += f"\n{sub['body'].capitalize()} will be visible tonight at {sub['at'].strftime('%H:%M')} in your county!"
            message += "\n Go to our dashboard for more information."

            sms.publish(PhoneNumber=sub['phone'],
                        Message=message)


def send_email(subscribers: list[dict]) -> None:
    '''Uses boto3 to send messages to subscribers by ses'''
    ses = get_client('ses')
    for sub in subscribers:
        if sub['body']:
            message = 'STARWATCH ALERT'
            message += f'\n\n Hello {sub['user'].capitalize()},\n\n'
            
            if not sub['at']:
                subject = f"ALERT: {sub['body'].capitalize()} visible Today"
                message += f"{sub['body'].capitalize()} will be visible tonight in your county!"
            else:
                subject = f"ALERT: {sub['body'].capitalize()} visible at {sub['at'].strftime('%H:%M')} Today"
                message += f"{sub['body'].capitalize()} will be visible tonight at {
                    sub['at'].strftime('%H:%M')} in your county!"
            message += "\n Go to our dashboard for more information."

            ses.send_email(Source=ENV['FROM'],
                           Destination={'ToAddresses': [sub['email']]},
                           Message={'Subject': {'Data': subject},
                                    'Body': {'Text': {'Data': message}}})


def get_client(service: str) -> client:
    '''Returns a AWS client'''
    return client(service, aws_access_key_id=ENV["MY_AWS_ACCESS_KEY"],
                        aws_secret_access_key=ENV["MY_AWS_SECRET_KEY"],
                        region_name=ENV['AWS_REGION'])

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    send_sms({})
    send_email({})