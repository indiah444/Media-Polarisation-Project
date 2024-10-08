"""Dummy file to combine random json data and output a single json"""

import json


def lambda_handler(event, context):
    """
    iterate through event and return dummy data to test pipelines execution
    """

    combined_data = {}

    for json_data in event['json_inputs']:
        combined_data.update(json_data)

    return {
        "statusCode": 200,
        "body": json.dumps(combined_data)
    }
