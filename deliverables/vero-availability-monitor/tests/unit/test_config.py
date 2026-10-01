import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import tests.helpers  # noqa: F401
from vero_monitor import config
from vero_monitor.config import ConfigError


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

    def test_example_file_is_valid_and_equals_defaults(self):
        cfg = config.load(config.EXAMPLE_FILE)
        self.assertEqual(config.read_json(config.EXAMPLE_FILE), config.DEFAULTS)
        self.assertEqual((cfg.interval_minutes, cfg.vero.task_timeout_s, cfg.port), (15, 180, 8766))
        self.assertIn("--json", cfg.vero.task_args)
        self.assertNotIn("--yolo", cfg.vero.task_args)

    def test_notepad_bom(self):
        self.assertEqual(config.load(self.write({}, bom=True)).vero.command, "vero")

    def test_invalid_values(self):
        bad = [
            {"schedule": {"interval_minutes": "abc"}},
            {"schedule": {"interval_minutes": 0}},
            {"schedule": {"interval_minutes": 2000}},
            {"vero": {"task_args": ["task"]}},  # no {prompt}
            {"vero": {"task_args": "task --json"}},  # not a list
            {"vero": {"command": " "}},
            {"checks": {"cli": False, "task": False, "chat": False}},
            {"checks": {"task": "yes"}},
            {"schedule": {"interval_minutes": 3}},  # 180 s task cannot fit in 3 min
            {"retention_days": -1},
            {"vero": {"env": []}},
        ]
        for b in bad:
            with self.assertRaises(ConfigError, msg=b):
                config.load(self.write(b))

    def test_broken_json_and_hint(self):
        p = self.dir / "c.json"
        p.write_text('{"data_dir": "C:\\Tools\\x"}')
        with self.assertRaisesRegex(ConfigError, "Windows paths"):
            config.load(p)
        p.write_text("[1]")
        with self.assertRaisesRegex(ConfigError, "object"):
            config.load(p)

    def test_missing_file(self):
        with self.assertRaisesRegex(ConfigError, "not found"):
            config.load(self.dir / "nope.json")

    def test_data_dir_relative_and_env(self):
        self.assertEqual(config.load(self.write({})).data_dir, config.ROOT / "data")
        var = "%VAM_T%" if os.name == "nt" else "$VAM_T"
        with mock.patch.dict(os.environ, {"VAM_T": str(self.dir)}):
            self.assertEqual(config.load(self.write({"data_dir": f"{var}/d"})).data_dir, self.dir / "d")

    def test_public_view_has_no_secrets(self):
        cfg = config.load(self.write({"vero": {"env": {"AWS_SECRET": "s3cr3t"}}, "checks": {"chat": True}}))
        text = json.dumps(cfg.public())
        self.assertNotIn("s3cr3t", text)
        self.assertNotIn("token_env", text)


if __name__ == "__main__":
    unittest.main()
