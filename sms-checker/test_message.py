'''Contains tests for message.py'''
from os import environ as ENV
from unittest import mock
from message import send_sms, send_email


class TestSendSMS:
    '''Tests for the send SMS function'''
    @mock.patch('message.get_client')
    def test_send_sms_valid(self, mock_get_client,valid_sub_list):
        '''Tests that a valid list results in two sns calls'''
        mock_sns = mock.MagicMock()
        mock_get_client.return_value = mock_sns
        send_sms(valid_sub_list)
        assert mock_sns.publish.call_count == 2

    @mock.patch('message.get_client')
    def test_send_sms_erroneous(self, mock_get_client,invalid_sub_list):
        '''Tests that an invalid list does not result in a sns call'''
        mock_sns = mock.MagicMock()
        mock_get_client.return_value = mock_sns
        send_sms(invalid_sub_list)
        mock_sns.publish.assert_not_called()

    @mock.patch('message.get_client')
    def test_send_sms_empty(self, mock_get_client):
        '''Tests that an empty list does not raise an error'''
        mock_sns = mock.MagicMock()
        mock_get_client.return_value = mock_sns
        subscribers = []
        send_sms(subscribers)
        mock_sns.publish.assert_not_called()

class TestSendEmail:
    '''Tests for send SES function'''
    @mock.patch('message.get_client')
    @mock.patch.dict(ENV, {'FROM': 'from@example.com'})
    def test_send_email_valid(self, mock_get_client,valid_sub_list):
        '''Tests that a valid list results in a SES call'''
        mock_ses = mock.MagicMock()
        mock_get_client.return_value = mock_ses

        send_email(valid_sub_list)
        assert mock_ses.send_email.call_count == 2

    @mock.patch('message.get_client')
    @mock.patch.dict(ENV, {'FROM': 'from@example.com'})
    def test_send_email_erroneous(self, mock_get_client,invalid_sub_list):
        '''Tests that an invalid list does not result in a SES call'''
        mock_ses = mock.MagicMock()
        mock_get_client.return_value = mock_ses
        send_email(invalid_sub_list)
        mock_ses.send_email.assert_not_called()

    @mock.patch('message.get_client')
    @mock.patch.dict(ENV, {'FROM': 'from@example.com'})
    def test_send_email_empty(self, mock_get_client):
        '''Tests that an empty list does not result in a call'''
        mock_ses = mock.MagicMock()
        mock_get_client.return_value = mock_ses
        subscribers = []
        send_email(subscribers)
        mock_ses.send_email.assert_not_called()
