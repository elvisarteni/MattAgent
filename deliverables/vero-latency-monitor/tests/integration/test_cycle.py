"""End to end with the bundled fake Vero CLI: probe, store, manifest, dashboard payload, HTTP."""
import json
import os
import tempfile
import threading
import unittest
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

import tests.conftest as h
from vero_latency.probe import run_cycle
from vero_latency.server import dashboard_payload, make_handler
from vero_latency.store import Store


class CycleTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        os.environ["FAKE_VERO_DELAY"] = "0.05"
        os.environ["FAKE_VERO_FAIL"] = "0"

    def tearDown(self):
        self.tmp.cleanup()
        os.environ.pop("FAKE_VERO_DELAY", None)
        os.environ.pop("FAKE_VERO_FAIL", None)

    def test_cycle_records_probe_and_manifest(self):
        cfg = h.demo_config(self.tmp.name, models=[{"id": "fake-mini", "label": "mini"},
                                                   {"id": "fake-std", "label": "std"}])
        store = Store(cfg["data_dir"])
        m = run_cycle(cfg, store, "manual")
        self.assertEqual(m["totals"], {"probes": 2, "ok": 2, "failed": 0})
        self.assertEqual(m["cli"]["version"], "vero-fake 0.0.1")
        self.assertRegex(m["run_id"], r"^\d{8}-\d{4}-vero-latency$")
        files = list(Path(cfg["data_dir"], "runs").rglob("*.json"))
        self.assertEqual(len(files), 1)
        rows = store.probes()
        self.assertEqual(len(rows), 2)
        self.assertGreaterEqual(rows[0]["total_ms"], 50)
        self.assertIsNotNone(rows[0]["first_byte_ms"])
        m2 = run_cycle(cfg, store, "manual")
        self.assertNotEqual(m["run_id"], m2["run_id"])  # same minute -> suffix

    def test_failure_and_timeout_recorded(self):
        os.environ["FAKE_VERO_FAIL"] = "1"
        cfg = h.demo_config(self.tmp.name)
        m = run_cycle(cfg, Store(cfg["data_dir"]), "manual")
        self.assertEqual(m["results"][0]["status"], "error")
        os.environ["FAKE_VERO_FAIL"] = "0"
        os.environ["FAKE_VERO_DELAY"] = "5"
        cfg = h.demo_config(self.tmp.name, cli={"timeout_s": 0.5})
        m = run_cycle(cfg, Store(cfg["data_dir"]), "manual")
        self.assertEqual(m["results"][0]["status"], "timeout")
        self.assertLess(m["results"][0]["total_ms"], 4000)

    def test_missing_executable(self):
        cfg = h.demo_config(self.tmp.name, cli={"command": ["no-such-vero-cli", "{prompt}"], "version_command": []})
        m = run_cycle(cfg, Store(cfg["data_dir"]), "manual")
        self.assertEqual(m["results"][0]["status"], "error")

    def test_http_api(self):
        cfg = h.demo_config(self.tmp.name)
        store = Store(cfg["data_dir"])
        run_cycle(cfg, store, "manual")
        payload = dashboard_payload(cfg, store, 24, None)
        self.assertEqual(payload["overall"]["probes"], 1)
        self.assertNotIn("env", json.dumps(payload["config"]))
        srv = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(cfg, store, None))
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        base = f"http://127.0.0.1:{srv.server_address[1]}"
        try:
            with urllib.request.urlopen(base + "/api/dashboard?hours=1") as r:
                self.assertEqual(json.load(r)["per_model"][0]["model"], "mini")
            with urllib.request.urlopen(base + "/api/export.csv") as r:
                self.assertEqual(r.read().decode().count("\n"), 2)
            with urllib.request.urlopen(base + "/") as r:
                self.assertIn(b"Vero CLI latency", r.read())
        finally:
            srv.shutdown()


if __name__ == "__main__":
    unittest.main()
