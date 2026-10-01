"""The CLI checks against scripts/fake_vero.py in every failure mode."""

import os
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

from tests.helpers import make_config
from vero_monitor.checks import run_all
from vero_monitor.checks.vero_cli import check_cli, check_task
from vero_monitor.domain import Check, CheckResult, Status


class CliChecksTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.cfg = make_config(Path(self.tmp.name))
        self.env = mock.patch.dict(os.environ, {"FAKE_VERO_DELAY": "0.05", "FAKE_VERO_MODE": "ok"})
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def mode(self, m, delay="0.05"):
        os.environ["FAKE_VERO_MODE"] = m
        os.environ["FAKE_VERO_DELAY"] = delay
        return check_task(self.cfg)

    def test_cli_up_with_version(self):
        r = check_cli(self.cfg)
        self.assertEqual((r.status, r.version), (Status.UP, "vero 2.3.3 (fake0000)"))

    def test_cli_missing(self):
        cfg = make_config(Path(self.tmp.name), vero={"command": "no-such-vero-xyz"})
        self.assertEqual(check_cli(cfg).status, Status.DOWN)
        self.assertIn("not found", check_task(cfg).detail)

    def test_task_up_reports_real_model(self):
        r = self.mode("ok")
        self.assertEqual(r.status, Status.UP, r.detail)
        self.assertEqual((r.provider_id, r.model_id), ("bedrock", self.cfg.vero.model))
        self.assertTrue((self.cfg.data_dir / "sandbox").is_dir())

    def test_task_slow_is_degraded(self):
        r = self.mode("ok", delay="3.2")  # threshold 3 s in make_config
        self.assertEqual(r.status, Status.DEGRADED)
        self.assertIn("slow", r.detail)

    def test_task_provider_down(self):
        r = self.mode("down")
        self.assertEqual(r.status, Status.DOWN)
        self.assertIn("provider unavailable", r.detail)

    def test_task_auth_error_secret_masked(self):
        r = self.mode("auth")
        self.assertEqual(r.status, Status.DOWN)
        self.assertIn("Unauthorized", r.detail)
        self.assertNotIn("abc123secret", r.detail)

    def test_no_completion_result_is_down(self):
        r = self.mode("nocompletion")
        self.assertEqual((r.status, r.detail), (Status.DOWN, "no completion_result"))

    def test_refusal_is_degraded_not_down(self):
        r = self.mode("refuse")
        self.assertEqual(r.status, Status.DEGRADED)
        self.assertIn("not with 'OK'", r.detail)

    def test_hang_is_killed_at_hard_limit(self):
        cfg = make_config(Path(self.tmp.name), vero={"task_timeout_s": 1})
        os.environ["FAKE_VERO_MODE"] = "hang"
        t0 = time.time()
        r = check_task(cfg)
        self.assertEqual(r.status, Status.DOWN)
        self.assertIn("no completion within 2 s", r.detail)
        self.assertLess(time.time() - t0, 6)

    def test_missing_json_flag_explained(self):
        cfg = make_config(Path(self.tmp.name), vero={"task_args": [self.cfg.vero.task_args[0], "task", "{prompt}"]})
        r = check_task(cfg)
        self.assertEqual(r.status, Status.DOWN)
        self.assertIn("--json", r.detail)


class RunAllTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmp.cleanup()

    def test_task_skipped_when_cli_down(self):
        cfg = make_config(Path(self.tmp.name), vero={"command": "no-such-vero-xyz"})
        res = run_all(cfg)
        self.assertEqual([(r.check, r.status) for r in res], [(Check.CLI, Status.DOWN), (Check.TASK, Status.DOWN)])
        self.assertIn("skipped", res[1].detail)

    def test_crashing_check_is_contained(self):
        cfg = make_config(Path(self.tmp.name))

        def boom(_):
            raise ValueError("bug")

        cli_up = lambda c: CheckResult(Check.CLI, Status.UP, 1.0)  # noqa: E731
        with mock.patch("vero_monitor.checks.check_task", boom), mock.patch(
            "vero_monitor.checks.check_cli", cli_up
        ), self.assertLogs("vero_monitor", "ERROR") as logs:
            res = run_all(cfg)
        self.assertIn("check task crashed", logs.output[0])
        self.assertEqual(res[-1].status, Status.DOWN)
        self.assertEqual(res[-1].detail, "monitor error: ValueError")


if __name__ == "__main__":
    unittest.main()
