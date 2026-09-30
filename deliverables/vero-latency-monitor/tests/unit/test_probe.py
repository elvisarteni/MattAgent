import unittest

import tests.conftest  # noqa: F401
from vero_latency.probe import build_command, classify


def res(**kw):
    base = {"total_ms": 10.0, "first_byte_ms": 5.0, "exit_code": 0, "stdout": "OK\n", "stderr": "", "timed_out": False}
    base.update(kw)
    return base


class BuildCommandTest(unittest.TestCase):
    T = ["nonexistent-vero", "-p", "{prompt}", "--model", "{model}"]

    def test_fills_placeholders(self):
        self.assertEqual(build_command(self.T, "hi", "m1", "arg"), ["nonexistent-vero", "-p", "hi", "--model", "m1"])

    def test_empty_model_drops_flag(self):
        self.assertEqual(build_command(self.T, "hi", "", "arg"), ["nonexistent-vero", "-p", "hi"])

    def test_stdin_mode_drops_prompt_arg(self):
        self.assertEqual(build_command(["v", "{prompt}"], "hi", "", "stdin"), ["v"])


class ClassifyTest(unittest.TestCase):
    def test_ok(self):
        self.assertEqual(classify(res(), "ok"), ("ok", None))

    def test_timeout(self):
        self.assertEqual(classify(res(timed_out=True), "OK")[0], "timeout")

    def test_nonzero_exit(self):
        st, msg = classify(res(exit_code=2, stderr="guardrail blocked"), "OK")
        self.assertEqual(st, "error")
        self.assertIn("guardrail blocked", msg)

    def test_unexpected_answer(self):
        self.assertEqual(classify(res(stdout="I cannot help"), "OK")[0], "unexpected")

    def test_not_started(self):
        self.assertEqual(classify(res(total_ms=None, exit_code=None, stderr="cannot start"), "OK")[0], "error")


if __name__ == "__main__":
    unittest.main()


class LockTest(unittest.TestCase):
    def test_stale_lock_is_ignored_and_cleared(self):
        import os
        import tempfile
        import time
        from pathlib import Path

        from vero_latency.probe import RunLock, run_in_progress
        with tempfile.TemporaryDirectory() as d:
            cfg = {"data_dir": d, "cli": {"timeout_s": 1}, "models": [{}]}
            lock = Path(d) / "probe.lock"
            lock.write_text("123")
            self.assertTrue(run_in_progress(cfg))
            old = time.time() - 3600
            os.utime(lock, (old, old))
            self.assertFalse(run_in_progress(cfg))
            with RunLock(d, 121) as held:
                self.assertTrue(held.held)
            self.assertFalse(lock.exists())
