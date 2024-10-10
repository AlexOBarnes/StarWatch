'''This script contains the lambda handler for this pipeline'''
import logging
from checker import get_subscribers
from message import send_email,send_sms

def lambda_handler(event,context) -> None:
    '''Runs the notification pipeline'''
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    lambda_handler({},{})
    