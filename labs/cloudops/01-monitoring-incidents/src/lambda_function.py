"""Disposable synchronous invocation fixture for the monitoring lab."""

import json


def lambda_handler(event, context):
    fail = event.get("fail", False) is True
    record = {
        "level": "ERROR" if fail else "INFO",
        "service": "cloudops-01",
        "request_id": context.aws_request_id,
        "outcome": "failure" if fail else "success",
        "message": "Deliberate lab failure" if fail else "Lab invocation succeeded",
    }
    print(json.dumps(record))
    if fail:
        raise RuntimeError("Deliberate CloudOps lab failure")
    return {"ok": True, "request_id": context.aws_request_id}
