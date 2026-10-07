import json
import os
import socket
import tempfile
import threading
import time
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from unittest import mock

from tests.helpers import fake_run, fake_settings, quiet_scanner
from vero_status.monitor import Monitor, perform_check
from vero_status.server import create


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class PerformCheckTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.work = Path(self.tmp.name) / "sandbox"
        self.env = mock.patch.dict(os.environ, {"FAKE_VERO_DELAY": "0.05", "FAKE_VERO_MODE": "ok"})
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def check(self, mode="ok", **settings):
        os.environ["FAKE_VERO_MODE"] = mode
        return perform_check(fake_settings(**settings), self.work, fake_run)

    def test_available_with_both_models(self):
        r = self.check()
        self.assertTrue(r["available"], r["reason"])
        self.assertEqual(r["asked_model"], "us.anthropic.claude-haiku-4-5-20251001-v1:0")  # pinned cheap model
        self.assertEqual(r["configured"]["model"], "us.anthropic.claude-opus-5")  # Vero's own setting
        self.assertEqual(r["vero_version"], "vero 2.3.3 (fake0000)")
        self.assertEqual(r["reason"], "")
        self.assertIsNotNone(r["seconds"])

    def test_empty_model_uses_veros_own(self):
        self.assertEqual(self.check(check_model="")["asked_model"], "us.anthropic.claude-opus-5")

    def test_failures_are_not_available_with_reason(self):
        down = self.check("down")
        self.assertEqual(down["reason"], "Vero reported an error (exit code 1): provider unavailable (connect ETIMEDOUT)")
        self.assertIsNone(down["seconds"])  # no answer, no response time
        r = self.check("auth")
        self.assertFalse(r["available"])
        self.assertNotIn("abc123secret", r["reason"])
        self.assertEqual(self.check("nocompletion")["reason"], "Vero finished without an answer")

    def test_refusal_is_available_with_note(self):
        r = self.check("refuse")
        self.assertTrue(r["available"])
        self.assertIn("not with OK", r["reason"])

    def test_vero_missing(self):
        with mock.patch("vero_status.monitor.vero.find_vero", return_value=None):
            r = perform_check(fake_settings(), self.work, lambda *a: self.fail("must not run"))
        self.assertFalse(r["available"])
        self.assertTrue(r["reason"].startswith("Vero CLI not found"))

    def test_hang_times_out(self):
        os.environ["FAKE_VERO_MODE"] = "hang"
        s = fake_settings(timeout_seconds=30)
        t0 = time.time()
        r = perform_check(s, self.work, lambda a, t, c=None: fake_run(a, min(t, 1.0), c))  # shorten the wait
        self.assertFalse(r["available"])
        self.assertIn("no answer within", r["reason"])
        self.assertLess(time.time() - t0, 6)

    def test_secret_prompt_never_in_record(self):
        self.assertNotIn("FAKE-SECRET-PROMPT", json.dumps(self.check()))


class MonitorTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.env = mock.patch.dict(os.environ, {"FAKE_VERO_DELAY": "0.05", "FAKE_VERO_MODE": "ok"})
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def wait_idle(self, m):
        for _ in range(100):
            if not m.checking:
                return
            time.sleep(0.05)
        self.fail("check did not finish")

    def make(self):
        m = Monitor(self.dir, fake_run, quiet_scanner())
        m.settings = fake_settings()
        return m

    def test_check_history_state_and_persistence(self):
        m = self.make()
        self.assertTrue(m.check_now())
        self.assertFalse(m.check_now())  # one at a time
        self.wait_idle(m)
        st = m.state()
        self.assertTrue(st["last"]["available"])
        self.assertEqual((st["availability_24h"], st["checks_24h"]), (100.0, 1))
        self.assertEqual(st["configured"]["model"], "us.anthropic.claude-opus-5")
        self.assertIsNotNone(st["next_check"])
        self.assertEqual(len(Monitor(self.dir, fake_run, quiet_scanner()).history), 1)  # saved to disk
        m.scan_sessions()
        self.assertEqual(m.state()["sessions"]["tasks_seen"], 0)
        self.assertEqual(m.own_task_ids(), [st["last"]["task_id"]])  # our probe task is remembered

    def test_since_tracks_the_current_streak(self):
        m = self.make()
        m.history = [{"time": 10, "available": True}, {"time": 20, "available": False}, {"time": 30, "available": False}]
        self.assertEqual(m.state()["since"], 20)

    def test_settings_update_and_interval_off(self):
        m = self.make()
        m.update_settings({"interval_minutes": 0})
        self.assertIsNone(m.next_check)
        self.assertEqual(json.loads((self.dir / "settings.json").read_text())["interval_minutes"], 0)

    def test_scheduler_runs_when_due(self):
        m = self.make()
        m.start(check_at_start=False)
        m.next_check = time.time() + 0.2
        m._wake.set()
        for _ in range(100):
            if m.history:
                break
            time.sleep(0.05)
        m.stop()
        self.assertEqual(m.history[-1]["trigger"], "auto")


class ServerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = mock.patch.dict(os.environ, {"FAKE_VERO_DELAY": "0.05", "FAKE_VERO_MODE": "ok"})
        self.env.start()
        self.port = free_port()
        self.mon = Monitor(Path(self.tmp.name), fake_run, quiet_scanner())
        self.mon.settings = fake_settings()
        self.quit = threading.Event()
        self.srv = create(self.mon, self.port, self.quit.set)
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()
        self.base = f"http://127.0.0.1:{self.port}"

    def tearDown(self):
        self.env.stop()
        if not self.quit.is_set():
            self.srv.shutdown()
        self.srv.server_close()
        self.tmp.cleanup()

    def req(self, path, data=None, **headers):
        body = json.dumps(data).encode() if data is not None else (b"" if headers.pop("post", False) else None)
        r = urllib.request.Request(self.base + path, data=body, headers={"Content-Type": "application/json", **headers})
        try:
            with urllib.request.urlopen(r) as resp:
                return resp.status, json.loads(resp.read() or b"null")
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read() or b"null")

    def test_page_state_health(self):
        with urllib.request.urlopen(self.base + "/") as r:
            self.assertIn(b"Vero Status", r.read())
        code, st = self.req("/api/state")
        self.assertEqual((code, st["last"]), (200, None))
        self.assertEqual(self.req("/api/health")[1]["app"], "vero-status")
        self.assertEqual(self.req("/nope")[0], 404)

    def test_check_now(self):
        self.assertEqual(self.req("/api/check", post=True)[0], 202)
        for _ in range(100):
            if self.mon.history and not self.mon.checking:
                break
            time.sleep(0.05)
        self.assertTrue(self.req("/api/state")[1]["last"]["available"])

    def test_settings_endpoint(self):
        self.assertEqual(self.req("/api/settings", {"interval_minutes": 30})[0], 200)
        self.assertEqual(self.mon.settings.interval_minutes, 30)
        code, body = self.req("/api/settings", {"interval_minutes": 7})
        self.assertEqual(code, 400)
        self.assertIn("interval", body["error"])
        self.assertEqual(self.req("/api/settings", [1])[0], 400)

    def test_foreign_host_and_origin_rejected(self):
        self.assertEqual(self.req("/api/state", Host="evil.example")[0], 403)
        self.assertEqual(self.req("/api/state", Host="evil.example:8767")[0], 403)
        self.assertEqual(self.req("/api/state", Host="localhost.evil.example")[0], 403)

    def test_forwarded_from_another_port(self):
        """VS Code port forwarding or `ssh -L 9000:127.0.0.1:8767` from a VM: the browser's port differs."""
        self.assertEqual(self.req("/api/state", Host="localhost:9000")[0], 200)
        self.assertEqual(self.req("/api/check", post=True, Host="localhost:9000", Origin="http://localhost:9000")[0], 202)
        self.assertEqual(self.req("/api/check", post=True, Host="localhost:9000", Origin="http://localhost:8767")[0], 403)
        self.assertEqual(self.req("/api/check", post=True, Origin="http://evil.example")[0], 403)
        self.assertEqual(self.req("/api/quit", post=True, Origin="http://evil.example")[0], 403)

    def test_quit(self):
        self.assertEqual(self.req("/api/quit", post=True)[1], {"stopping": True})
        self.assertTrue(self.quit.wait(5))


if __name__ == "__main__":
    unittest.main()


class ServerModeTest(unittest.TestCase):
    KEY = "test-admin-key-0123456789"

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = mock.patch.dict(os.environ, {"FAKE_VERO_DELAY": "0.05", "FAKE_VERO_MODE": "ok"})
        self.env.start()
        self.port = free_port()
        self.mon = Monitor(Path(self.tmp.name), fake_run, quiet_scanner(), server_mode=True)
        self.mon.settings = fake_settings()
        self.srv = create(self.mon, self.port, server_mode=True, admin_key=self.KEY, host="127.0.0.1")
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()
        self.base = f"http://127.0.0.1:{self.port}"

    def tearDown(self):
        self.env.stop()
        self.srv.shutdown()
        self.srv.server_close()
        self.tmp.cleanup()

    def req(self, path, data=None, post=False, **headers):
        body = json.dumps(data).encode() if data is not None else (b"" if post else None)
        r = urllib.request.Request(self.base + path, data=body, headers={"Content-Type": "application/json", **headers})
        try:
            with urllib.request.urlopen(r) as resp:
                return resp.status, json.loads(resp.read() or b"null")
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read() or b"null")

    def wait_idle(self):
        for _ in range(100):
            if not self.mon.checking:
                return
            time.sleep(0.05)

    def test_anyone_can_read_without_login_any_host_name(self):
        code, st = self.req("/api/state", Host=f"vero-status.example.nxp.com:{self.port}")
        self.assertEqual(code, 200)
        self.assertEqual((st["mode"], st["admin"]), ("server", False))
        self.assertEqual((st["settings"]["vero_path"], st["settings"]["vero_found"]), ("", None))  # server paths hidden
        self.assertIsNone(st["sessions"])  # no personal panels on a shared server
        self.assertFalse(st["settings"]["track_sessions"])

    def test_admin_key_unlocks_settings(self):
        self.assertEqual(self.req("/api/settings", {"interval_minutes": 30})[0], 403)
        self.assertEqual(self.req("/api/settings", {"interval_minutes": 30}, **{"X-Admin-Key": "wrong"})[0], 403)
        self.assertEqual(self.req("/api/settings", {"interval_minutes": 30}, **{"X-Admin-Key": self.KEY})[0], 200)
        self.assertEqual(self.mon.settings.interval_minutes, 30)
        _, st = self.req("/api/state", **{"X-Admin-Key": self.KEY})
        self.assertTrue(st["admin"])
        self.assertTrue(st["settings"]["vero_found"])

    def test_no_quit_on_the_server(self):
        self.assertEqual(self.req("/api/quit", post=True)[0], 404)
        self.assertEqual(self.req("/api/quit", post=True, **{"X-Admin-Key": self.KEY})[0], 404)
        self.assertEqual(self.req("/api/health")[0], 200)

    def test_check_now_is_rate_limited_for_viewers_not_admin(self):
        self.assertEqual(self.req("/api/check", post=True)[0], 202)
        self.wait_idle()
        code, body = self.req("/api/check", post=True)
        self.assertEqual(code, 429)
        self.assertIn("try again", body["error"])
        self.assertGreater(self.req("/api/state")[1]["check_wait_s"], 0)
        self.assertEqual(self.req("/api/check", post=True, **{"X-Admin-Key": self.KEY})[0], 202)

    def test_cross_site_post_still_blocked(self):
        self.assertEqual(self.req("/api/check", post=True, Origin="http://evil.example")[0], 403)


class AdminKeyTest(unittest.TestCase):
    def test_created_once_and_reused(self):
        from vero_status.app import admin_key

        with tempfile.TemporaryDirectory() as d:
            k1 = admin_key(Path(d))
            self.assertGreaterEqual(len(k1), 24)
            self.assertEqual(admin_key(Path(d)), k1)
            if os.name != "nt":  # a shared Linux VM: other users must not read the admin key
                self.assertEqual((Path(d) / "admin_key.txt").stat().st_mode & 0o077, 0)


class HeadlessTest(unittest.TestCase):
    def test_no_browser_on_a_headless_linux_vm(self):
        from vero_status.app import can_open_browser

        self.assertFalse(can_open_browser("linux", {}))
        self.assertTrue(can_open_browser("linux", {"DISPLAY": ":0"}))
        self.assertTrue(can_open_browser("linux", {"WAYLAND_DISPLAY": "wayland-0"}))
        self.assertTrue(can_open_browser("win32", {}))
