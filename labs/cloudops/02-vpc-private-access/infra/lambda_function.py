import json


def lambda_handler(event, context):
    response_body = {
        "lab": "cloudops-02",
        "status": "ok",
    }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps(response_body),
    }
