"""Run lifecycle (lock, store, manifest, privacy) and the HTTP status page."""

import json
import os
import socket
import tempfile
import threading
import time
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest import mock

from tests.helpers import make_config
from vero_monitor.domain import Check, CheckResult, Status
from vero_monitor.report import payload, static_html
from vero_monitor.runner import RunLock, in_progress, run_once
from vero_monitor.scheduler import Loop
from vero_monitor.server import make_handler
from vero_monitor.store import Store


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class RunnerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.cfg = make_config(Path(self.tmp.name))
        self.store = Store(self.cfg.data_dir)
        self.env = mock.patch.dict(os.environ, {"FAKE_VERO_DELAY": "0.05", "FAKE_VERO_MODE": "ok"})
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def test_run_stores_and_writes_manifest(self):
        run = run_once(self.cfg, self.store, "manual")
        self.assertEqual(run.overall, Status.UP)
        self.assertRegex(run.run_id, r"^\d{8}-\d{4}-vero-availability$")
        m = json.loads(next((self.cfg.data_dir / "runs").rglob("*.json")).read_text())
        self.assertEqual(m["model"]["id"], self.cfg.vero.model)
        self.assertEqual([c["check"] for c in m["checks"]], ["cli", "task"])
        self.assertEqual(self.store.count(), 1)
        self.assertNotEqual(run_once(self.cfg, self.store, "manual").run_id, run.run_id)  # -2 suffix
        self.assertFalse(in_progress(self.cfg))

    def test_full_prompt_never_persisted(self):
        run_once(self.cfg, self.store, "manual")
        blobs = [p.read_bytes() for p in self.cfg.data_dir.rglob("*") if p.is_file()]
        self.assertFalse(any(b"FAKE-SECRET-api_req_started" in b for b in blobs))

    def test_lock_blocks_overlap_and_stale_lock_is_cleared(self):
        with RunLock(self.cfg.data_dir, 999) as held:
            self.assertTrue(held.held)
            self.assertTrue(in_progress(self.cfg))
            self.assertIsNone(run_once(self.cfg, self.store, "manual"))
        lock = self.cfg.data_dir / "run.lock"
        lock.write_text("1")
        old = time.time() - 99999
        os.utime(lock, (old, old))
        self.assertFalse(in_progress(self.cfg))
        self.assertIsNotNone(run_once(self.cfg, self.store, "manual"))

    def test_down_run_reason_and_prune(self):
        down = [CheckResult(Check.CLI, Status.UP, 1.0), CheckResult(Check.TASK, Status.DOWN, 5.0, "provider unavailable")]
        run_once(self.cfg, self.store, "manual", checker=lambda c: down)
        r = self.store.runs(limit=1)[0]
        self.assertEqual((r["overall"], r["reason"]), ("down", "task: provider unavailable"))
        self.assertEqual(len(r["checks"]), 2)
        self.assertEqual(self.store.prune(1, now=time.time() + 3 * 86400), 1)
        self.assertEqual(self.store.csv_rows(), [])  # checks removed with their run (cascade)

    def test_payload_and_static_report(self):
        run_once(self.cfg, self.store, "manual", checker=lambda c: [CheckResult(Check.TASK, Status.DOWN, 1.0, "</script><x>")])
        d = payload(self.cfg, self.store, 24)
        self.assertEqual(d["current"]["status"], "down")
        self.assertEqual(len(d["timeline"]), 96)
        self.assertEqual(d["availability"]["24h"], 0.0)
        self.assertEqual(d["incidents"][0]["end"], None)
        html = static_html(self.cfg, self.store, 24)
        blob = html.split("window.STATIC_DATA=", 1)[1].split(";</script>", 1)[0]
        self.assertNotIn("<", blob)
        self.assertEqual(json.loads(blob)["recent"][0]["reason"], "task: </script><x>")


class ServerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        port = free_port()
        self.cfg = make_config(Path(self.tmp.name), server={"host": "127.0.0.1", "port": port})
        self.store = Store(self.cfg.data_dir)
        self.loop = Loop(self.cfg, self.store)
        self.srv = ThreadingHTTPServer(("127.0.0.1", port), make_handler(self.cfg, self.store, self.loop))
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()
        self.base = f"http://127.0.0.1:{port}"
        self.env = mock.patch.dict(os.environ, {"FAKE_VERO_DELAY": "0.05", "FAKE_VERO_MODE": "ok"})
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.srv.shutdown()
        self.srv.server_close()
        self.tmp.cleanup()

    def status(self, path, method="GET", **headers):
        try:
            return urllib.request.urlopen(urllib.request.Request(self.base + path, method=method, headers=headers)).status
        except urllib.error.HTTPError as e:
            return e.code

    def get_json(self, path):
        with urllib.request.urlopen(self.base + path) as r:
            return json.load(r)

    def test_pages_and_api(self):
        with urllib.request.urlopen(self.base + "/") as r:
            self.assertIn(b"Vero status", r.read())
        d = self.get_json("/api/status?hours=6")
        self.assertEqual((d["range_hours"], d["current"]["status"]), (6, "unknown"))
        self.assertEqual(self.get_json("/api/status?hours=abc")["range_hours"], 24)
        self.assertEqual(self.get_json("/api/health")["app"], "vero-availability")
        self.assertEqual(self.status("/nope"), 404)

    def test_security_checks(self):
        self.assertEqual(self.status("/api/health", Host="evil.example"), 403)
        self.assertEqual(self.status("/api/check", "POST", Origin="http://evil.example"), 403)

    def test_check_now_then_csv(self):
        self.assertEqual(self.status("/api/check", "POST", Origin=self.base), 202)
        for _ in range(60):
            if self.store.count() == 1 and not self.loop.running:
                break
            time.sleep(0.1)
        self.assertEqual(self.store.count(), 1)
        with urllib.request.urlopen(self.base + "/api/export.csv") as r:
            self.assertEqual(r.read().decode().count("\n"), 3)  # header + cli + task


if __name__ == "__main__":
    unittest.main()
