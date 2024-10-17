"""Script to check if email is verified and add to database."""

from os import environ as ENV

import boto3
from dotenv import load_dotenv


def check_and_verify_email(email: str) -> None:
    """Checks if email is in verified identities and adds it if not."""

    load_dotenv()
    ses_client = boto3.client(service_name="ses",
                              aws_access_key_id=ENV['AWS_ACCESS_KEY_BOUDICCA'],
                              aws_secret_access_key=ENV['AWS_ACCESS_SECRET_KEY_BOUDICCA'],
                              region_name=ENV['REGION'])
    if check_email_needs_verifying(ses_client, email):
        verify_email(ses_client, email)


def check_email_needs_verifying(ses: boto3.client, email: str) -> bool:
    """Checks if email is in verified identities."""

    verified_emails = ses.list_verified_email_addresses()
    verified_emails = verified_emails['VerifiedEmailAddresses']
    if email in verified_emails:
        return False
    return True


def verify_email(ses: boto3.client, email: str) -> None:
    """Verifies email."""

    ses.verify_email_identity(
        EmailAddress=email
    )


if __name__ == "__main__":
    check_and_verify_email("tester")
