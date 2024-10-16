'''This script contains the lambda handler for this pipeline'''
#pylint: disable=W0613,W0612
import logging
import asyncio
from checker import get_subscribers_bodies, get_subscribers_aurora
from message import send_email_for_bodies,send_sms_for_bodies,\
                    construct_aurora_email,construct_aurora_sms


def process_users(contacts: list) -> tuple[list]:
    '''Processes the user lists into email and phone lists'''
    return ([entry for entry in contacts if entry['email']],
            [entry for entry in contacts if entry['phone']])


async def alerts_for_bodies() -> None:
    '''Asynchronous function that alerts users about celestial bodies'''
    subscribers = get_subscribers_bodies()
    if subscribers:
        logging.info('Subscribers found: %s', len(subscribers))
        email_list, phone_list = process_users(subscribers)
        logging.info('Emails to be sent: %s', len(email_list))
        logging.info('Texts to be sent: %s', len(phone_list))
        tasks = []
        if email_list:
            tasks.append(send_email_for_bodies(email_list))
        if phone_list:
            tasks.append(send_sms_for_bodies(phone_list))
        if tasks:
            await asyncio.gather(*tasks)
    else:
        logging.info('No subscribers found.')


async def alerts_for_auroras() -> None:
    '''Asynchronous function that alerts users about auroras'''
    users,colour = get_subscribers_aurora()
    if users:
        logging.info('Subscribers found: %s', len(users))
        email_list, phone_list = process_users(users)
        logging.info('Emails to be sent: %s', len(email_list))
        logging.info('Texts to be sent: %s', len(phone_list))
        tasks = []
        if email_list:
            tasks.append(construct_aurora_email(email_list,colour))
        if phone_list:
            tasks.append(construct_aurora_sms(phone_list,colour))
        if tasks:
            await asyncio.gather(*tasks)
    else:
        logging.info('No subscribers found.')


async def run_notifications():
    '''Runs asynchronous functions'''
    await asyncio.gather(alerts_for_bodies(),
                         alerts_for_auroras())


def lambda_handler(event,context) -> None:
    '''Runs the notification pipeline'''
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run_notifications())


if __name__ == '__main__':
    lambda_handler({},{})
