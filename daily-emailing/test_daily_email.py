# pylint: skip-file

from unittest.mock import patch, MagicMock

from daily_email import send_email, lambda_handler


@patch('daily_email.get_daily_subscribers')
@patch('daily_email.get_avg_polarity_by_topic_and_source_yesterday')
@patch('daily_email.generate_html')
@patch('daily_email.get_ses_client')
@patch('daily_email.MIMEMultipart')
@patch.dict('os.environ', {'FROM_EMAIL': 'from@example.com'})
def test_send_email(mock_mime_multipart, mock_get_ses_client, mock_generate_html, mock_get_avg_polarity, mock_get_subscribers):

    mock_get_subscribers.return_value = ['user1@example.com',
                                         'user2@example.com']
    mock_get_avg_polarity.return_value = MagicMock()
    mock_generate_html.return_value = '<html>Report</html>'
    mock_client = MagicMock()
    mock_message = MagicMock()
    mock_get_ses_client.return_value = mock_client
    mock_mime_multipart.return_value = mock_message

    send_email()
    mock_client.send_raw_email.assert_called_once_with(
        Source='from@example.com',
        Destinations=['user1@example.com', 'user2@example.com'],
        RawMessage={'Data': mock_message.as_string()})


class TestLambdaHandler:
    @patch('daily_email.send_email')
    def test_success(self, mock_send_email):
        mock_send_email.return_value = None

        response = lambda_handler({}, {})

        assert response['statusCode'] == 200
        assert response['body'] == "Daily emails sent."

    @patch('daily_email.send_email')
    def test_failure(self, mock_send_email):
        mock_send_email.side_effect = Exception("Test Exception")

        response = lambda_handler({}, {})

        assert response['statusCode'] == 500
        assert "Error: Test Exception" in response['body']
