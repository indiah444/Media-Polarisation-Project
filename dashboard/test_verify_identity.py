# pylint: skip-file

"""Tests for the verify_identity.py file."""

import unittest
from unittest.mock import patch, MagicMock

from verify_identity import check_and_verify_email, check_email_needs_verifying, verify_email


class TestVerifyIdentity(unittest.TestCase):

    @patch('verify_identity.boto3.client')
    @patch('verify_identity.check_email_needs_verifying')
    @patch('verify_identity.verify_email')
    @patch('verify_identity.ENV', {
        "AWS_ACCESS_KEY_BOUDICCA": "test_access_key",
        "AWS_ACCESS_SECRET_KEY_BOUDICCA": "test_secret_key",
        "REGION": "test_region"
    })
    def test_check_and_verify_email(self, fake_verify_email, fake_check_email_needs_verifying, fake_boto_client):
        """Test check_and_verify_email calls the correct functions when email needs verification."""
        fake_ses_client = MagicMock()
        fake_boto_client.return_value = fake_ses_client
        fake_check_email_needs_verifying.return_value = True
        check_and_verify_email('test@example.com')
        fake_boto_client.assert_called_once_with(service_name="ses",
                                                 aws_access_key_id="test_access_key",
                                                 aws_secret_access_key="test_secret_key",
                                                 region_name="test_region")
        fake_check_email_needs_verifying.assert_called_once_with(
            fake_ses_client, 'test@example.com')
        fake_verify_email.assert_called_once_with(
            fake_ses_client, 'test@example.com')

    @patch('verify_identity.boto3.client')
    @patch('verify_identity.check_email_needs_verifying')
    @patch('verify_identity.verify_email')
    @patch('verify_identity.ENV', {
        "AWS_ACCESS_KEY_BOUDICCA": "test_access_key",
        "AWS_ACCESS_SECRET_KEY_BOUDICCA": "test_secret_key",
        "REGION": "test_region"
    })
    def test_check_and_verify_email_no_verification_needed(self, fake_verify_email, fake_check_email_needs_verifying, fake_boto_client):
        """Test check_and_verify_email does not verify when the email is already verified."""
        fake_ses_client = MagicMock()
        fake_boto_client.return_value = fake_ses_client
        fake_check_email_needs_verifying.return_value = False
        check_and_verify_email('test@example.com')

        fake_boto_client.assert_called_once_with(service_name="ses",
                                                 aws_access_key_id="test_access_key",
                                                 aws_secret_access_key="test_secret_key",
                                                 region_name="test_region")
        fake_check_email_needs_verifying.assert_called_once_with(
            fake_ses_client, 'test@example.com')
        fake_verify_email.assert_not_called()

    @patch('verify_identity.boto3.client')
    def test_check_email_needs_verifying(self, fake_boto_client):
        """Test check_email_needs_verifying returns True if the email is not verified."""
        fake_ses_client = MagicMock()
        fake_ses_client.list_verified_email_addresses.return_value = {
            'VerifiedEmailAddresses': ['already_verified@example.com']
        }
        result = check_email_needs_verifying(
            fake_ses_client, 'test@example.com')

        fake_ses_client.list_verified_email_addresses.assert_called_once()
        self.assertTrue(result)

    @patch('verify_identity.boto3.client')
    def test_check_email_needs_verifying_already_verified(self, fake_boto_client):
        """Test check_email_needs_verifying returns False if the email is already verified."""
        fake_ses_client = MagicMock()
        fake_ses_client.list_verified_email_addresses.return_value = {
            'VerifiedEmailAddresses': ['test@example.com']
        }
        result = check_email_needs_verifying(
            fake_ses_client, 'test@example.com')

        fake_ses_client.list_verified_email_addresses.assert_called_once()
        self.assertFalse(result)

    @patch('verify_identity.boto3.client')
    def test_verify_email(self, fake_boto_client):
        """Test verify_email calls SES to verify the email."""
        fake_ses_client = MagicMock()
        verify_email(fake_ses_client, 'test@example.com')

        fake_ses_client.verify_email_identity.assert_called_once_with(
            EmailAddress='test@example.com'
        )
