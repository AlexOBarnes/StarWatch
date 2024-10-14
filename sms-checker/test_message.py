'''Contains tests for message.py'''
#pylint: disable=W0613,R0903
from os import environ as ENV
from unittest import mock
from message import send_sms_for_bodies, send_email_for_bodies,\
                send_aurora_sms,assign_content,\
                construct_aurora_email,construct_aurora_sms

class TestSendSMS:
    '''Tests for the send SMS function'''
    @mock.patch('message.get_client')
    def test_send_sms_for_bodies_valid(self, mock_get_client,valid_sub_list):
        '''Tests that a valid list results in two sns calls'''
        mock_sns = mock.MagicMock()
        mock_get_client.return_value = mock_sns
        send_sms_for_bodies(valid_sub_list)
        assert mock_sns.publish.call_count == 2

    @mock.patch('message.get_client')
    def test_send_sms_for_bodies_erroneous(self, mock_get_client,invalid_sub_list):
        '''Tests that an invalid list does not result in a sns call'''
        mock_sns = mock.MagicMock()
        mock_get_client.return_value = mock_sns
        send_sms_for_bodies(invalid_sub_list)
        mock_sns.publish.assert_not_called()

    @mock.patch('message.get_client')
    def test_send_sms_for_bodies_empty(self, mock_get_client):
        '''Tests that an empty list does not raise an error'''
        mock_sns = mock.MagicMock()
        mock_get_client.return_value = mock_sns
        subscribers = []
        send_sms_for_bodies(subscribers)
        mock_sns.publish.assert_not_called()

class TestSendEmail:
    '''Tests for send SES function'''
    @mock.patch('message.get_client')
    @mock.patch.dict(ENV, {'FROM': 'from@example.com'})
    def test_send_email_for_bodies_valid(self, mock_get_client,valid_sub_list):
        '''Tests that a valid list results in a SES call'''
        mock_ses = mock.MagicMock()
        mock_get_client.return_value = mock_ses

        send_email_for_bodies(valid_sub_list)
        assert mock_ses.send_email.call_count == 2

    @mock.patch('message.get_client')
    @mock.patch.dict(ENV, {'FROM': 'from@example.com'})
    def test_send_email_for_bodies_erroneous(self, mock_get_client,invalid_sub_list):
        '''Tests that an invalid list does not result in a SES call'''
        mock_ses = mock.MagicMock()
        mock_get_client.return_value = mock_ses
        send_email_for_bodies(invalid_sub_list)
        mock_ses.send_email.assert_not_called()

    @mock.patch('message.get_client')
    @mock.patch.dict(ENV, {'FROM': 'from@example.com'})
    def test_send_email_for_bodies_empty(self, mock_get_client):
        '''Tests that an empty list does not result in a call'''
        mock_ses = mock.MagicMock()
        mock_get_client.return_value = mock_ses
        subscribers = []
        send_email_for_bodies(subscribers)
        mock_ses.send_email.assert_not_called()


class TestAssignContent:
    '''Contains tests for assign content function'''
    def test_yellow_alert(self):
        '''Tests that yellow alerts return the correct thing'''
        result = assign_content('Yellow')
        assert result == 'Starwatch Aurora Alert: Minor Geomagnetic Activity'

    def test_amber_alert(self):
        '''Tests that amber alerts return the correct thing'''
        result = assign_content('Amber')
        assert result == 'Starwatch Aurora Alert: Possible Aurora'

    def test_default_alert(self):
        '''Tests that green alerts return the correct thing'''
        result = assign_content('Green')
        assert result == 'Starwatch Aurora Alert: Aurora Likely'

    def test_unknown_alert(self):
        '''Tests that red alerts return the correct thing'''
        result = assign_content('Red')
        assert result == 'Starwatch Aurora Alert: Aurora Likely'


class TestSendAuroraSMS:
    '''Contains tests for send aurora sms function'''
    @mock.patch('message.client')
    def test_send_aurora_sms(self, mock_boto_client):
        '''Tests that valid inputs results in a publish'''
        mock_client = mock_boto_client.return_value
        number = '+12345678901'
        message = 'Test alert message'
        send_aurora_sms(mock_client, number, message)
        mock_client.publish.assert_called_once_with(
            PhoneNumber=number, Message=message)


class TestAuroraNotifications:
    '''Contains tests for the two aurora notification functions'''
    @mock.patch('message.get_client')
    @mock.patch('message.send_aurora_email')
    @mock.patch('message.logging')
    def test_construct_aurora_email(self, mock_logging, mock_send_aurora_email, mock_get_client):
        '''Tests that the client function is called the correct number of times'''
        mock_ses = mock.MagicMock()
        mock_get_client.return_value = mock_ses
        users = [{'user': 'davidjohnson', 'email': 'davidjohnson@example.com'},
            {'user': 'johndoe', 'email': 'johndoe@example.com'}]
        alert = ('Yellow', 'Minor Geomagnetic Activity')
        with mock.patch('message.assign_content',
                        return_value='Starwatch Aurora Alert: Minor Geomagnetic Activity'):
            construct_aurora_email(users, alert)
        mock_get_client.assert_called_once_with('ses')

    @mock.patch('message.get_client')
    @mock.patch('message.send_aurora_sms')
    @mock.patch('message.logging')
    def test_construct_aurora_sms(self, mock_logging, mock_send_aurora_sms, mock_get_client):
        '''Tests that the client function is called the correct number of times'''
        mock_sns = mock.MagicMock()
        mock_get_client.return_value = mock_sns
        users = [{'user': 'davidjohnson', 'phone': '+12345678901'},
                {'user': 'johndoe', 'phone': '+19876543210'}]
        alert = 'Minor Geomagnetic Activity'
        with mock.patch('message.assign_content',
                        return_value='Starwatch Aurora Alert: Minor Geomagnetic Activity'):
            construct_aurora_sms(users, alert)
        mock_get_client.assert_called_once_with('sns')
