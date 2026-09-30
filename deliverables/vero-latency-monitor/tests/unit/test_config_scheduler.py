import json
import os
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from unittest import mock

import tests.conftest  # noqa: F401
from vero_latency import cli, config, scheduler

NS = "{http://schemas.microsoft.com/windows/2004/02/mit/task}"


class ConfigTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, obj, bom=False):
        p = self.dir / "c.json"
        p.write_bytes((b"\xef\xbb\xbf" if bom else b"") + json.dumps(obj).encode())
        return p

    def test_notepad_bom_accepted(self):
        cfg = config.load(self.write({"models": [{"id": "m"}]}, bom=True))
        self.assertEqual(cfg["models"][0]["label"], "m")

    def test_bad_types_are_config_errors(self):
        for bad in ({"schedule": {"interval_minutes": "abc"}}, {"thresholds_ms": {"warn": 9, "crit": 1}},
                    {"models": []}, {"cli": {"command": "vero -p x"}}, {"models": [{"id": "a"}, {"id": "a"}]}):
            with self.assertRaises(config.ConfigError, msg=bad):
                config.load(self.write(bad))

    def test_windows_path_hint(self):
        p = self.dir / "c.json"
        p.write_text('{"data_dir": "C:\\Tools\\x"}')
        with self.assertRaisesRegex(config.ConfigError, "Windows paths"):
            config.load(p)

    def test_example_is_valid(self):
        cfg = config.load(config.EXAMPLE_FILE)
        self.assertEqual(cfg["schedule"]["interval_minutes"], 15)

    def test_data_dir_env_expansion(self):
        with mock.patch.dict(os.environ, {"VLM_TEST_DIR": str(self.dir)}):
            cfg = config.load(self.write({"data_dir": "$VLM_TEST_DIR/d" if os.name != "nt" else "%VLM_TEST_DIR%/d"}))
        self.assertEqual(Path(cfg["data_dir"]), self.dir / "d")

    def test_configure_wizard(self):
        target = self.dir / "monitor.json"
        answers = iter([f'"{sys.executable}" -p {{prompt}} --model {{model}}', "cheap-1, big-2", "5", "30", "4", "12"])
        with mock.patch("builtins.input", lambda *_: next(answers)), mock.patch("builtins.print"):
            rc = cli.main(["--config", str(target), "configure"])
        self.assertEqual(rc, 0)
        cfg = config.load(target)
        self.assertEqual(cfg["cli"]["command"][0], sys.executable)
        self.assertEqual([m["id"] for m in cfg["models"]], ["cheap-1", "big-2"])
        self.assertEqual(cfg["schedule"]["interval_minutes"], 5)
        self.assertEqual(cfg["thresholds_ms"], {"warn": 4000.0, "crit": 12000.0})

    def test_configure_recovers_from_broken_config(self):
        target = self.dir / "monitor.json"
        target.write_text("{ broken")
        answers = iter([f'"{sys.executable}" -p {{prompt}}', "", "15", "60", "5", "15"])
        with mock.patch("builtins.input", lambda *_: next(answers)), mock.patch("builtins.print"):
            self.assertEqual(cli.main(["--config", str(target), "configure"]), 0)
        self.assertEqual(config.load(target)["models"][0]["id"], "")

    def test_demo_uses_separate_data_dir(self):
        target = self.dir / "monitor.json"
        with mock.patch("builtins.print"):
            cli.main(["--config", str(target), "init", "--demo"])
        self.assertTrue(config.load(target)["data_dir"].endswith("data-demo"))


class TaskXmlTest(unittest.TestCase):
    def test_probe_task_is_laptop_safe(self):
        root = ET.fromstring(scheduler.probe_task_xml(15).split("\n", 1)[1])
        s = root.find(f"{NS}Settings")
        self.assertEqual(s.find(f"{NS}DisallowStartIfOnBatteries").text, "false")
        self.assertEqual(s.find(f"{NS}StopIfGoingOnBatteries").text, "false")
        self.assertEqual(s.find(f"{NS}StartWhenAvailable").text, "true")
        self.assertEqual(s.find(f"{NS}MultipleInstancesPolicy").text, "IgnoreNew")
        self.assertEqual(root.find(f".//{NS}Repetition/{NS}Interval").text, "PT15M")
        args = root.find(f".//{NS}Exec/{NS}Arguments").text
        self.assertIn("vlm.py", args)
        self.assertIn("--trigger task", args)
        self.assertTrue(root.find(f".//{NS}StartBoundary").text.endswith((":00:00", ":15:00", ":30:00", ":45:00")))

    def test_dashboard_task_runs_forever_at_logon(self):
        root = ET.fromstring(scheduler.dashboard_task_xml().split("\n", 1)[1])
        self.assertIsNotNone(root.find(f".//{NS}LogonTrigger"))
        self.assertEqual(root.find(f".//{NS}ExecutionTimeLimit").text, "PT0S")
        self.assertIn("--no-scheduler", root.find(f".//{NS}Exec/{NS}Arguments").text)

    def test_cron_expr(self):
        self.assertEqual(scheduler._cron_expr(15), "*/15 * * * *")
        self.assertEqual(scheduler._cron_expr(120), "0 */2 * * *")
        self.assertEqual(scheduler._cron_expr(1440), "0 0 * * *")

    def test_next_aligned(self):
        self.assertEqual(scheduler.next_aligned(900, 1000), 1800)
        self.assertEqual(scheduler.next_aligned(900, 1800), 2700)


if __name__ == "__main__":
    unittest.main()
