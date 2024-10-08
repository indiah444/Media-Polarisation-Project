"""Dummy file to output random json data"""

import json


def lambda_handler(event, context):
    """Return dummy data to test pipelines execution"""

    dummy_data = {
        "message": "Hello from Lambda!",
        "data": {
            "item1": "value1",
            "item2": "value2",
            "item3": "value3"
        }
    }

    return {
        "statusCode": 200,
        "body": json.dumps(dummy_data)
    }
