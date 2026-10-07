import os
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

import tests.helpers  # noqa: F401
from vero_status import vero

GUIDE_STREAM = [
    '{"type":"task_started","taskId":"1790868292727"}',
    '{"type":"say","say":"task","text":"Reply with exactly: OK","modelInfo":{"providerId":"bedrock",'
    '"modelId":"us.anthropic.claude-haiku-4-5-20251001-v1:0","mode":"act"}}',
    '{"type":"say","say":"api_req_started","text":"{\\"request\\":\\"secret prompt\\"}"}',
    '{"type":"say","say":"text","text":"O","partial":true}',
    '{"type":"say","say":"error","text":"[ERROR] You did not use a tool in your previous response!"}',
    '{"type":"say","say":"completion_result","text":"OK"}',
]


class ParseTaskStreamTest(unittest.TestCase):
    def test_stream_from_integration_guide(self):
        s = vero.parse_task_stream(GUIDE_STREAM)
        self.assertEqual((s.answer, s.provider, s.model), ("OK", "bedrock", "us.anthropic.claude-haiku-4-5-20251001-v1:0"))
        self.assertEqual(s.events, 6)

    def test_only_completion_result_counts_and_partials_ignored(self):
        s = vero.parse_task_stream(['{"say":"text","text":"OK"}', '{"say":"completion_result","text":"O","partial":true}'])
        self.assertIsNone(s.answer)

    def test_garbage_ignored(self):
        s = vero.parse_task_stream(["", "banner", "{bad", "[1]", '{"type":"error","message":"Bearer abc.def failed"}'])
        self.assertEqual((s.events, s.error), (1, "[hidden] failed"))


class ParseConfigTest(unittest.TestCase):
    def test_key_value_lines_as_in_the_guide(self):
        text = (
            "actModeApiProvider : bedrock\n"
            "actModeApiModelId  : us.anthropic.claude-opus-5\n"
            "awsRegion          : us-west-2\n"
            "other : x"
        )
        self.assertEqual(
            vero.parse_config(text), {"provider": "bedrock", "model": "us.anthropic.claude-opus-5", "region": "us-west-2"}
        )

    def test_json_and_quoted_variants(self):
        self.assertEqual(vero.parse_config('{"actModeApiModelId": "m1", "awsRegion": "eu"}'), {"model": "m1", "region": "eu"})
        self.assertEqual(vero.parse_config('  "actModeApiModelId": "m2",'), {"model": "m2"})
        self.assertEqual(vero.parse_config("nothing useful"), {})


class SmallParsersTest(unittest.TestCase):
    def test_version_and_clean(self):
        self.assertEqual(vero.parse_version("vero 2.3.3 (35b52374)\nmore"), "vero 2.3.3 (35b52374)")
        self.assertEqual(vero.parse_version(""), "")
        self.assertNotIn("abc123", vero.clean("error token=abc123 password=x"))
        self.assertEqual(len(vero.clean("x" * 999)), vero.DETAIL_MAX)

    def test_task_args(self):
        a = vero.task_args("vero", "", 120, Path("w"))
        self.assertEqual(a, ["vero", "task", "--json", "-t", "120", "-c", "w", vero.PROMPT])
        self.assertIn("-m", vero.task_args("vero", "m1", 120, Path("w")))
        self.assertNotIn("--yolo", a)


class RunAndFindTest(unittest.TestCase):
    def test_run_collects_output(self):
        r = vero.run([sys.executable, "-c", "print('hi'); import sys; sys.exit(3)"], 10)
        self.assertEqual((r.started, r.code, r.out.strip(), r.timed_out), (True, 3, "hi", False))

    def test_run_missing_program(self):
        self.assertFalse(vero.run(["no-such-program-xyz"], 5).started)

    @unittest.skipIf(os.name == "nt", "POSIX process group")
    def test_timeout_kills_the_whole_tree_fast(self):
        t0 = time.time()
        r = vero.run(["sh", "-c", "sleep 30 & sleep 30; echo late"], 0.5)
        self.assertTrue(r.timed_out)
        self.assertLess(time.time() - t0, 3)

    def test_find_vero(self):
        self.assertEqual(vero.find_vero(sys.executable), sys.executable)
        with tempfile.TemporaryDirectory() as d:
            no_path = mock.patch("vero_status.vero.shutil.which", return_value=None)
            home = mock.patch("vero_status.vero.Path.home", return_value=Path(d))
            with no_path, home, mock.patch.dict(os.environ, {"APPDATA": ""}), mock.patch.object(
                Path, "is_file", return_value=False
            ):
                self.assertIsNone(vero.find_vero("/nope/vero-xyz"))
            npm = Path(d) / "npm"
            npm.mkdir()
            (npm / "vero.cmd").write_text("@echo off")
            with no_path, home, mock.patch.dict(os.environ, {"APPDATA": d}):
                self.assertEqual(vero.find_vero(""), str(npm / "vero.cmd"))  # npm default location on Windows

    def test_find_vero_linux_vm_nvm_newest_node(self):
        """On a VM a service has a minimal PATH: an nvm install must still be found (newest node first)."""
        with tempfile.TemporaryDirectory() as d:
            for v in ("v9.11.2", "v20.11.0", "v18.19.1"):
                b = Path(d) / ".nvm" / "versions" / "node" / v / "bin"
                b.mkdir(parents=True)
                (b / "vero").write_text("#!/usr/bin/env node")
            with mock.patch("vero_status.vero.shutil.which", return_value=None), mock.patch(
                "vero_status.vero.Path.home", return_value=Path(d)
            ), mock.patch.dict(os.environ, {"APPDATA": ""}):
                self.assertIn("v20.11.0", vero.find_vero("") or "")

    @unittest.skipIf(os.name == "nt", "POSIX shell script")
    def test_run_puts_the_program_folder_first_on_path(self):
        """So `#!/usr/bin/env node` finds the node that nvm installed next to vero."""
        with tempfile.TemporaryDirectory() as d:
            script = Path(d) / "show-path"
            script.write_text('#!/bin/sh\necho "$PATH"\n')
            script.chmod(0o755)
            r = vero.run([str(script)], 10)
            self.assertTrue(r.out.startswith(d + os.pathsep), r.out)


if __name__ == "__main__":
    unittest.main()
