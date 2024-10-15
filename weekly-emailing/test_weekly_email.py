# pylint: skip-file

from unittest.mock import patch, MagicMock

from weekly_email import send_email, lambda_handler


@patch('weekly_email.get_weekly_subscribers')
@patch('weekly_email.get_avg_polarity_last_week')
@patch('weekly_email.get_ses_client')
@patch('weekly_email.generate_pdf')
@patch('weekly_email.load_dotenv')
@patch.dict('os.environ', {'FROM_EMAIL': 'from@example.com'})
def test_send_email(mock_load_dotenv, mock_generate_pdf, mock_get_ses_client,
                    mock_get_avg_polarity_last_week, mock_get_weekly_subscribers):

    mock_load_dotenv.return_value = None
    mock_get_weekly_subscribers.return_value = ['subscriber1@example.com']
    mock_get_avg_polarity_last_week.return_value = MagicMock()

    mock_pdf_content = MagicMock()
    mock_pdf_content.read.return_value = b"PDF content"
    mock_generate_pdf.return_value = mock_pdf_content

    mock_client = MagicMock()
    mock_get_ses_client.return_value = mock_client

    send_email()

    mock_client.send_raw_email.assert_called_once_with(
        Source='from@example.com',
        Destinations=['subscriber1@example.com'],
        RawMessage={
            'Data': mock_client.send_raw_email.call_args[1]['RawMessage']['Data']})


class TestLambdaHandler():

    @patch('weekly_email.send_email')
    def test_lambda_handler_success(self, mock_send_email):
        mock_send_email.return_value = None

        response = lambda_handler({}, {})

        assert response['statusCode'] == 200
        assert response['body'] == "Weekly emails sent."

    @patch('weekly_email.send_email')
    def test_lambda_handler_failure(self, mock_send_email):
        mock_send_email.side_effect = Exception("Email sending failed")

        response = lambda_handler({}, {})

        assert response['statusCode'] == 500
        assert "Error: Email sending failed" == response['body']
