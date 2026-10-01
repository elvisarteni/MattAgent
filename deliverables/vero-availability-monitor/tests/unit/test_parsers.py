import unittest
from pathlib import Path

from tests.helpers import FIXTURES, make_config
from vero_monitor.checks.vero_chat import parse_reply
from vero_monitor.checks.vero_cli import clean, hard_limit_s, parse_stream, task_command


class StreamParserTest(unittest.TestCase):
    def test_real_stream_from_integration_guide(self):
        s = parse_stream((FIXTURES / "vero_task_stream.ndjson").read_text().splitlines())
        self.assertEqual(s.task_id, "1790868292727")
        self.assertEqual(s.completion, "OK")
        self.assertEqual(s.provider_id, "bedrock")
        self.assertEqual(s.model_id, "us.anthropic.claude-haiku-4-5-20251001-v1:0")
        self.assertEqual(s.events, 8)

    def test_only_completion_result_is_the_answer(self):
        s = parse_stream(['{"type":"say","say":"text","text":"OK","partial":false}'])
        self.assertIsNone(s.completion)

    def test_partial_completion_ignored(self):
        s = parse_stream(['{"type":"say","say":"completion_result","text":"O","partial":true}'])
        self.assertIsNone(s.completion)

    def test_garbage_lines_ignored(self):
        s = parse_stream(["", "Vero banner", "{not json", "[1,2]", '"str"', '{"type":"task_started","taskId":7}'])
        self.assertEqual((s.task_id, s.events), ("7", 1))

    def test_error_event_captured_and_cleaned(self):
        s = parse_stream(['{"type":"error","message":"Unauthorized   Bearer abc.def"}'])
        self.assertEqual(s.error, "Unauthorized [masked]")


class CleanTest(unittest.TestCase):
    def test_masks_credentials_and_flattens(self):
        self.assertEqual(clean("a\n  b\tc"), "a b c")
        for secret in ("Bearer eyJabc", "token=abc123", "token: abc", "password=hunter2", "aws_secret_access_key=x"):
            self.assertNotIn(secret.split()[-1].split("=")[-1].split(":")[-1].strip(), clean(f"err {secret} end"))

    def test_length_limited(self):
        self.assertEqual(len(clean("x" * 1000)), 200)


class TaskCommandTest(unittest.TestCase):
    def test_placeholders_filled(self):
        cfg = make_config(
            Path("/tmp/x"),
            vero={
                "command": "vero",
                "task_args": ["task", "--json", "-m", "{model}", "-t", "{timeout}", "-c", "{workdir}", "{prompt}"],
                "task_timeout_s": 180,
            },
            schedule={"interval_minutes": 15},
        )
        args = task_command(cfg, "C:/vero.cmd", Path("/w"))
        self.assertEqual(
            args,
            ["C:/vero.cmd", "task", "--json", "-m", cfg.vero.model, "-t", "180", "-c", str(Path("/w")), "Reply with exactly: OK"],
        )
        self.assertNotIn("--yolo", args)  # never auto-approve (ADR-003)
        self.assertEqual(hard_limit_s(cfg), 210)


class McpReplyTest(unittest.TestCase):
    def test_plain_json(self):
        self.assertEqual(parse_reply('{"jsonrpc":"2.0","id":1,"result":{}}'), {"jsonrpc": "2.0", "id": 1, "result": {}})

    def test_sse(self):
        body = 'event: message\ndata: {"jsonrpc":"2.0","id":1,"result":{"serverInfo":{"name":"WChat MCP Server"}}}\n\n'
        self.assertEqual(parse_reply(body)["result"]["serverInfo"]["name"], "WChat MCP Server")

    def test_error_and_garbage(self):
        self.assertIn("error", parse_reply('data: {"jsonrpc":"2.0","id":1,"error":{"message":"bad"}}'))
        self.assertIsNone(parse_reply("<html>login page</html>"))
        self.assertIsNone(parse_reply('{"jsonrpc":"2.0"}'))


if __name__ == "__main__":
    unittest.main()
