"""End to end with the bundled fake Vero CLI: probe, store, manifest, dashboard payload, HTTP."""
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

import tests.conftest as h
from vero_latency.probe import run_cycle, time_command
from vero_latency.scheduler import Loop
from vero_latency.server import make_handler, static_report
from vero_latency.store import Store


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


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
        self.assertEqual(len(list(Path(cfg["data_dir"], "runs").rglob("*.json"))), 1)
        rows = store.probes()
        self.assertEqual(len(rows), 2)
        self.assertGreaterEqual(rows[0]["total_ms"], 50)
        self.assertIsNotNone(rows[0]["first_byte_ms"])
        m2 = run_cycle(cfg, store, "manual")
        self.assertNotEqual(m["run_id"], m2["run_id"])  # same minute -> suffix
        self.assertFalse(Path(cfg["data_dir"], "probe.lock").exists())

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

    @unittest.skipIf(os.name == "nt", "POSIX process groups")
    def test_timeout_kills_whole_tree_quickly(self):
        # regression: a grandchild kept the pipe open, the probe stalled ~10 s and left an orphan
        marker = f"sleep {37 + os.getpid() % 50}.5"
        t0 = time.time()
        r = time_command(["sh", "-c", f"{marker}; echo OK"], None, 0.5)
        self.assertTrue(r["timed_out"])
        self.assertLess(time.time() - t0, 3)
        time.sleep(0.2)
        alive = os.popen(f"pgrep -f '[s]{marker[1:]}'").read().strip()
        self.assertEqual(alive, "")

    def test_missing_executable(self):
        cfg = h.demo_config(self.tmp.name, cli={"command": ["no-such-vero-cli", "{prompt}"], "version_command": []})
        m = run_cycle(cfg, Store(cfg["data_dir"]), "manual")
        self.assertEqual(m["results"][0]["status"], "error")

    def test_static_report_cannot_break_out_of_script(self):
        cfg = h.demo_config(self.tmp.name, models=[{"id": "fake-mini", "label": "</script><!--x"}])
        run_cycle(cfg, Store(cfg["data_dir"]), "manual")
        html = static_report(cfg, Store(cfg["data_dir"]), 24, None)
        blob = html.split("window.STATIC_DATA=", 1)[1].split(";</script>", 1)[0]
        self.assertNotIn("<", blob)
        self.assertEqual(json.loads(blob)["per_model"][0]["model"], "</script><!--x")


class HttpTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        os.environ["FAKE_VERO_DELAY"] = "0.05"
        os.environ["FAKE_VERO_FAIL"] = "0"
        port = free_port()
        self.cfg = h.demo_config(self.tmp.name, server={"host": "127.0.0.1", "port": port})
        self.store = Store(self.cfg["data_dir"])
        run_cycle(self.cfg, self.store, "manual")
        self.loop = Loop(self.cfg, self.store)
        self.srv = ThreadingHTTPServer(("127.0.0.1", port), make_handler(self.cfg, self.store, self.loop))
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()
        self.base = f"http://127.0.0.1:{port}"

    def tearDown(self):
        self.srv.shutdown()
        self.srv.server_close()
        self.tmp.cleanup()
        os.environ.pop("FAKE_VERO_DELAY", None)
        os.environ.pop("FAKE_VERO_FAIL", None)

    def get(self, path, **headers):
        return urllib.request.urlopen(urllib.request.Request(self.base + path, headers=headers))

    def status(self, path, method="GET", **headers):
        try:
            return urllib.request.urlopen(urllib.request.Request(self.base + path, method=method, headers=headers)).status
        except urllib.error.HTTPError as e:
            return e.code

    def test_endpoints(self):
        with self.get("/api/dashboard?hours=1") as r:
            d = json.load(r)
        self.assertEqual(d["per_model"][0]["model"], "mini")
        self.assertEqual(d["state"]["scheduler"], "external")
        self.assertNotIn("env", json.dumps(d["config"]))
        with self.get("/api/export.csv") as r:
            self.assertEqual(r.read().decode().count("\n"), 2)
        with self.get("/") as r:
            self.assertIn(b"Vero CLI latency", r.read())
        with self.get("/api/health") as r:
            self.assertEqual(json.load(r)["app"], "vero-latency")

    def test_bad_hours_does_not_crash(self):
        with self.get("/api/dashboard?hours=abc") as r:
            self.assertEqual(json.load(r)["range_hours"], 24)

    def test_foreign_host_and_origin_rejected(self):
        self.assertEqual(self.status("/api/health", Host="evil.example"), 403)
        self.assertEqual(self.status("/api/probe", "POST", Origin="http://evil.example"), 403)

    def test_probe_now(self):
        self.assertEqual(self.status("/api/probe", "POST", Origin=self.base), 202)
        for _ in range(50):
            if not self.loop.running and len(self.store.probes()) == 2:
                break
            time.sleep(0.1)
        self.assertEqual(len(self.store.probes()), 2)


if __name__ == "__main__":
    unittest.main()
