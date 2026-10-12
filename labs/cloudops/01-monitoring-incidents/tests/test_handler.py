"""Local behavior checks; these do not validate AWS monitoring."""

import contextlib
import importlib.util
import io
import json
from pathlib import Path
from types import SimpleNamespace
import unittest


spec = importlib.util.spec_from_file_location(
    "lab_handler", Path(__file__).resolve().parents[1] / "src" / "lambda_function.py"
)
handler_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(handler_module)


class HandlerTests(unittest.TestCase):
    def setUp(self):
        self.context = SimpleNamespace(aws_request_id="synthetic-request")

    def test_success_is_correlated_and_does_not_log_event_body(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = handler_module.lambda_handler(
                {"fail": False, "private_value": "do-not-log"}, self.context
            )
        self.assertTrue(result["ok"])
        record = json.loads(output.getvalue())
        self.assertEqual(record["request_id"], result["request_id"])
        self.assertEqual(record["outcome"], "success")
        self.assertNotIn("do-not-log", output.getvalue())

    def test_failure_raises_instead_of_returning_error_dictionary(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            with self.assertRaisesRegex(RuntimeError, "Deliberate CloudOps lab failure"):
                handler_module.lambda_handler({"fail": True}, self.context)
        record = json.loads(output.getvalue())
        self.assertEqual(record["outcome"], "failure")
        self.assertEqual(record["request_id"], self.context.aws_request_id)


if __name__ == "__main__":
    unittest.main()
