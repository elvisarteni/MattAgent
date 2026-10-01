import json
import tempfile
import unittest
from pathlib import Path

import tests.helpers  # noqa: F401
from vero_status.settings import CHEAP_MODEL, Settings, SettingsError, load, save


class SettingsTest(unittest.TestCase):
    def test_defaults(self):
        s = Settings()
        s.validate()
        self.assertEqual((s.check_model, s.interval_minutes, s.port), (CHEAP_MODEL, 15, 8767))

    def test_merge_validates(self):
        self.assertEqual(Settings().merged({"interval_minutes": 0, "check_model": ""}).interval_minutes, 0)
        for bad in (
            {"interval_minutes": 7},
            {"interval_minutes": "15"},
            {"timeout_seconds": 5},
            {"port": 80},
            {"check_model": "two words"},
            {"evil": 1},
            {"vero_path": 3},
        ):
            with self.assertRaises(SettingsError, msg=bad):
                Settings().merged(bad)

    def test_load_save_and_broken_file(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "settings.json"
            self.assertEqual(load(p), Settings())
            save(p, Settings().merged({"interval_minutes": 30}))
            self.assertEqual(load(p).interval_minutes, 30)
            p.write_bytes(b"\xef\xbb\xbf" + json.dumps({"interval_minutes": 60, "old_key": 1}).encode())
            self.assertEqual(load(p).interval_minutes, 60)  # BOM and unknown keys tolerated
            p.write_text("{broken")
            self.assertEqual(load(p), Settings())
            p.write_text('{"interval_minutes": 7}')
            self.assertEqual(load(p), Settings())


if __name__ == "__main__":
    unittest.main()
