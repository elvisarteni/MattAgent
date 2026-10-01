"""Vero Chat check against a local fake MCP server."""

import json
import os
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest import mock

from tests.helpers import make_config
from vero_monitor.checks.vero_chat import check_chat
from vero_monitor.domain import Status


class FakeMcp(BaseHTTPRequestHandler):
    mode = "sse"
    seen_auth = None

    def log_message(self, *a):
        pass

    def do_POST(self):
        FakeMcp.seen_auth = self.headers.get("Authorization")
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        assert body["method"] == "initialize"
        if self.mode == "401":
            self.send_response(401)
            self.end_headers()
            return
        msg = {"jsonrpc": "2.0", "id": 1, "result": {"serverInfo": {"name": "WChat MCP Server", "version": "4.0.3"}}}
        if self.mode == "error":
            msg = {"jsonrpc": "2.0", "id": 1, "error": {"code": -32600, "message": "bad request"}}
        data = (f"event: message\ndata: {json.dumps(msg)}\n\n" if self.mode != "html" else "<html>SSO</html>").encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


class ChatCheckTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.srv = ThreadingHTTPServer(("127.0.0.1", 0), FakeMcp)
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()
        cls.url = f"http://127.0.0.1:{cls.srv.server_address[1]}/mcp"

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()
        cls.srv.server_close()

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.cfg = make_config(
            Path(self.tmp.name), checks={"chat": True}, chat={"url": self.url, "token_env": "VAM_TEST_TOKEN", "timeout_s": 5}
        )
        self.env = mock.patch.dict(os.environ, {"VAM_TEST_TOKEN": "tok-123"})
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def run_mode(self, mode):
        FakeMcp.mode = mode
        return check_chat(self.cfg)

    def test_handshake_up(self):
        r = self.run_mode("sse")
        self.assertEqual((r.status, r.version), (Status.UP, "WChat MCP Server 4.0.3"))
        self.assertEqual(FakeMcp.seen_auth, "Bearer tok-123")
        self.assertNotIn("tok-123", repr(r))

    def test_rejected_token(self):
        r = self.run_mode("401")
        self.assertEqual(r.status, Status.DOWN)
        self.assertIn("token rejected", r.detail)

    def test_mcp_error_and_non_mcp_reply(self):
        self.assertIn("bad request", self.run_mode("error").detail)
        self.assertIn("not an MCP", self.run_mode("html").detail)

    def test_missing_token_variable(self):
        os.environ.pop("VAM_TEST_TOKEN")
        r = check_chat(self.cfg)
        self.assertEqual(r.status, Status.DOWN)
        self.assertIn("VAM_TEST_TOKEN", r.detail)

    def test_unreachable(self):
        cfg = make_config(
            Path(self.tmp.name),
            checks={"chat": True},
            chat={"url": "http://127.0.0.1:9/mcp", "token_env": "VAM_TEST_TOKEN", "timeout_s": 2},
        )
        r = check_chat(cfg)
        self.assertEqual(r.status, Status.DOWN)
        self.assertIn("unreachable", r.detail)


if __name__ == "__main__":
    unittest.main()
