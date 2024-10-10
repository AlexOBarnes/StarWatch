'''This script will message the subscribers if they require notification'''
import logging
from os import environ as ENV
from dotenv import load_dotenv
from boto3 import client

def send_sms(subscribers: list[dict]) -> None:
    '''Uses boto3 to send messages to subscribers by sms'''
    sms = get_client('sns')
    logging.info('Client established for SNS')
    for sub in subscribers:
        if sub['body']:
            message = 'STARWATCH ALERT'
            message += f'\n\n Hello {sub['user'].capitalize()},\n\n'
            if not sub['at']:
                message += f"{sub['body'].capitalize()} will be visible tonight in your county!"
            else:
                message += f"\n{sub['body'].capitalize()} will be visible tonight"
                message += f"at {sub['at'].strftime('%H:%M')} in your county!"
            message += "\n Go to our dashboard for more information."
            logging.info('Message constructed successfully')
            response = sms.publish(PhoneNumber=sub['phone'],
                        Message=message)
            logging.info('Message sent for subscriber: %s',sub['user'])
            logging.info('SNS response received: %s', response)
        else:
            logging.warning('Invalid data in: %s', sub)


def send_email(subscribers: list[dict]) -> None:
    '''Uses boto3 to send messages to subscribers by ses'''
    ses = get_client('ses')
    logging.info('Client established for SES')
    for sub in subscribers:
        if sub['body']:
            message = 'STARWATCH ALERT'
            message += f'\n\n Hello {sub['user'].capitalize()},\n\n'

            if not sub['at']:
                subject = f"ALERT: {sub['body'].capitalize()} visible Today"
                message += f"{sub['body'].capitalize()} will be visible tonight in your county!"
            else:
                subject = f"ALERT: {sub['body'].capitalize()} visible at"
                subject += f"{sub['at'].strftime('%H:%M')} Today"
                message += f"{sub['body'].capitalize()} will be visible tonight at"
                message += f"{sub['at'].strftime('%H:%M')} in your county!"
            message += "\n Go to our dashboard for more information."
            logging.info('Message constructed successfully')
            response = ses.send_email(Source=ENV['FROM'],
                           Destination={'ToAddresses': [sub['email']]},
                           Message={'Subject': {'Data': subject},
                                    'Body': {'Text': {'Data': message}}})
            logging.info('Message sent for subscriber: %s', sub['user'])
            logging.info('SES response received: %s', response)
        else:
            logging.warning('Invalid data in: %s',sub)


def get_client(service: str) -> client:
    '''Returns a AWS client'''
    return client(service, aws_access_key_id=ENV["MY_AWS_ACCESS_KEY"],
                        aws_secret_access_key=ENV["MY_AWS_SECRET_KEY"],
                        region_name=ENV['REGION'])

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    send_sms({})
    send_email({})
