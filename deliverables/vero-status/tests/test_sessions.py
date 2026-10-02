import json
import os
import tempfile
import time
import unittest
from pathlib import Path

import tests.helpers  # noqa: F401
from vero_status import sessions
from vero_status.vero import PROMPT

HAIKU = {"providerId": "bedrock", "modelId": "us.anthropic.claude-haiku-4-5-20251001-v1:0", "mode": "act"}
OPUS = {"providerId": "bedrock", "modelId": "us.anthropic.claude-opus-5", "mode": "act"}


PROMPT_TEXT = "SECRET PROMPT TEXT"  # stands for the full prompt Vero logs; must never be kept


def req(ts, tokens_in=1200, tokens_out=80):
    text = json.dumps({"request": PROMPT_TEXT, "tokensIn": tokens_in, "tokensOut": tokens_out, "cost": 0.01})
    return {"ts": ts, "type": "say", "say": "api_req_started", "text": text, "modelInfo": OPUS}


def session(t0_ms, task_text="refactor the parser"):
    """A user's task: two model requests answered after 4.0 s and 2.5 s, then a completion."""
    return [
        {"ts": t0_ms, "type": "say", "say": "task", "text": task_text, "modelInfo": OPUS},
        req(t0_ms + 100),
        {"ts": t0_ms + 4100, "type": "say", "say": "text", "text": "Let me look", "partial": True, "modelInfo": OPUS},
        {"ts": t0_ms + 9000, "type": "ask", "ask": "tool", "text": "read file"},
        req(t0_ms + 20000),
        {"ts": t0_ms + 20000 + 2500, "type": "say", "say": "completion_result", "text": "done", "modelInfo": OPUS},
    ]


class ParseTest(unittest.TestCase):
    def test_latency_per_request_from_veros_timestamps(self):
        s = sessions.parse_ui_messages(session(1_000_000), "t1", "CLI", now=2000)
        self.assertEqual([r.seconds for r in s.requests], [4.0, 2.5])
        self.assertEqual((s.model, s.provider), ("us.anthropic.claude-opus-5", "bedrock"))
        self.assertEqual((s.requests[0].tokens_in, s.requests[0].tokens_out), (1200, 80))
        self.assertAlmostEqual(s.last_activity, 1022.5)
        self.assertIsNone(s.waiting_since)
        self.assertFalse(s.first_prompt_is_probe)

    def test_prompt_and_answer_text_never_kept(self):
        s = sessions.parse_ui_messages(session(1_000_000), "t1", "CLI", now=2000)
        summary = sessions.summarize([s], False, 2000, [])
        blob = repr(s) + json.dumps(summary)
        for text in ("SECRET PROMPT TEXT", "refactor the parser", "Let me look", "read file"):
            self.assertNotIn(text, blob)

    def test_request_in_progress_and_failed(self):
        evs = [*session(1_000_000)[:2], req(1_030_000)]
        s = sessions.parse_ui_messages(evs, "t", "CLI", now=1040)
        self.assertEqual(s.waiting_since, 1030)
        failed = [req(1_000_000), {"ts": 1_003_000, "type": "ask", "ask": "api_req_failed", "text": "429"}]
        self.assertTrue(sessions.parse_ui_messages(failed, "t", "CLI", now=2000).requests[0].failed)

    def test_long_pause_and_bad_events_ignored(self):
        evs = [req(0), {"ts": 31 * 60 * 1000, "say": "text"}, "junk", {"no_ts": 1}, {"ts": "x"}]
        s = sessions.parse_ui_messages(evs, "t", "CLI", now=99999)
        self.assertEqual(s.requests, [])

    def test_probe_task_recognised(self):
        evs = session(1_000_000, task_text=PROMPT)
        self.assertTrue(sessions.parse_ui_messages(evs, "t", "CLI").first_prompt_is_probe)

    def test_percentile(self):
        self.assertIsNone(sessions.percentile([], 50))
        self.assertEqual(sessions.percentile([1, 2, 3, 4], 50), 2.5)
        self.assertEqual(sessions.percentile([5], 95), 5)


class ProcessDetectionTest(unittest.TestCase):
    IGN = ("C:\\Tools\\vero-status\\data\\sandbox", "vero_status")

    def test_user_vero_cli(self):
        for cmd in (
            '"C:\\Program Files\\nodejs\\node.exe" '
            '"C:\\Users\\me\\AppData\\Roaming\\npm\\node_modules\\@nxp\\vero\\bin\\vero.js"',
            "node /usr/lib/node_modules/vero/dist/cli.js",
            "vero",
            "vero task fix the build",
            "C:\\npm\\vero.cmd --continue",
        ):
            self.assertTrue(sessions.is_interactive_vero(cmd, self.IGN), cmd)

    def test_not_user_vero(self):
        for cmd in (
            "node server.js",
            "node build.js --verbose",
            "C:\\npm\\vero.cmd task --json -c C:\\Tools\\vero-status\\data\\sandbox Reply",
            "pythonw C:\\Tools\\vero-status\\vero_status\\app.py",
            "vero version",
            "vero config",
            "python3 Vero Status.pyw",
            '"C:\\Python312\\pythonw.exe" "C:\\Tools\\vero-status\\Vero Status.pyw"',
            "code --extensions-dir C:\\Users\\me\\.vscode\\extensions\\nxp.vero-1.0",
            "node C:\\work\\averone\\index.js",
            "",
        ):
            self.assertFalse(sessions.is_interactive_vero(cmd, self.IGN), cmd)


class ScannerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.cli = self.root / "home" / ".vero" / "data" / "tasks"
        self.code = self.root / "Code" / "User" / "globalStorage" / "nxp.vero-assistant" / "tasks"
        self.procs = []

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, base, task_id, events, age_s=0):
        p = base / task_id / "ui_messages.json"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(events))
        t = time.time() - age_s
        os.utime(p, (t, t))
        return p

    def scanner(self):
        roots = [(str(self.cli), "CLI"), (str(self.root / "Code" / "User" / "globalStorage" / "*vero*" / "tasks"), "VS Code")]
        return sessions.Scanner(roots, ignore_processes=["sandbox"], list_processes=lambda: self.procs)

    def test_open_session_latency_and_own_tasks_excluded(self):
        now_ms = int(time.time() * 1000)
        self.write(self.cli, "user1", session(now_ms - 60_000))
        self.write(self.cli, "probe1", session(now_ms - 50_000))  # one of our availability checks (by id)
        self.write(self.cli, "probe2", session(now_ms - 40_000, task_text=PROMPT))  # ours (by prompt)
        st = self.scanner().state(own_task_ids=["probe1"])
        self.assertEqual(st["tasks_seen"], 1)
        self.assertTrue(st["open"])
        self.assertEqual(st["current"]["model"], "us.anthropic.claude-opus-5")
        self.assertEqual(st["current"]["source"], "CLI")
        self.assertEqual(st["latency"]["hour"], {"n": 2, "p50": 3.2, "p95": 3.9})
        self.assertEqual([r["s"] for r in st["recent"]], [4.0, 2.5])

    def test_vscode_extension_storage_found(self):
        now_ms = int(time.time() * 1000)
        self.write(self.code, "vs1", session(now_ms - 30_000))
        st = self.scanner().state()
        self.assertEqual(st["current"]["source"], "VS Code")

    def test_idle_history_is_not_open_but_open_cli_is(self):
        old_ms = int((time.time() - 3 * 3600) * 1000)
        self.write(self.cli, "old", session(old_ms), age_s=3 * 3600)
        s = self.scanner()
        st = s.state()
        self.assertFalse(st["open"])
        self.assertIsNone(st["current"])
        self.assertEqual(st["latency"]["day"]["n"], 2)
        self.procs = ["node /x/node_modules/vero/bin/vero.js"]
        st = s.state(force=True)
        self.assertTrue(st["open"] and st["cli_process"])
        self.assertIsNone(st["current"])  # idle CLI: the page shows Vero's configured model

    def test_cache_and_old_files_skipped(self):
        now_ms = int(time.time() * 1000)
        self.write(self.cli, "week_old", session(now_ms - 9 * 86400_000), age_s=9 * 86400)
        s = self.scanner()
        self.assertEqual(s.state()["tasks_seen"], 0)
        self.assertIs(s.state(), s.state())  # cached between scans
        p = self.write(self.cli, "new", session(now_ms))
        self.assertEqual(s.state(force=True)["tasks_seen"], 1)
        p.write_text("{not json")
        os.utime(p, (time.time() + 5, time.time() + 5))
        self.assertEqual(s.state(force=True)["tasks_seen"], 0)  # a broken file is skipped, not fatal

    def test_missing_folders(self):
        st = self.scanner().state()
        self.assertEqual((st["open"], st["tasks_seen"], st["recent"]), (False, 0, []))


if __name__ == "__main__":
    unittest.main()
