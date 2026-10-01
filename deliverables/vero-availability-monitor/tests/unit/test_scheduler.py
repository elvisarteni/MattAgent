import unittest
import xml.etree.ElementTree as ET

import tests.helpers  # noqa: F401
from vero_monitor import scheduler

NS = "{http://schemas.microsoft.com/windows/2004/02/mit/task}"


def parse(xml):
    return ET.fromstring(xml.split("\n", 1)[1])


class TaskXmlTest(unittest.TestCase):
    def test_check_task_laptop_safe(self):
        root = parse(scheduler.probe_task_xml(15))
        s = root.find(f"{NS}Settings")
        for tag, val in (
            ("DisallowStartIfOnBatteries", "false"),
            ("StopIfGoingOnBatteries", "false"),
            ("StartWhenAvailable", "true"),
            ("MultipleInstancesPolicy", "IgnoreNew"),
            ("ExecutionTimeLimit", "PT1H"),
        ):
            self.assertEqual(s.find(NS + tag).text, val, tag)
        self.assertEqual(root.find(f".//{NS}Repetition/{NS}Interval").text, "PT15M")
        args = root.find(f".//{NS}Exec/{NS}Arguments").text
        self.assertIn("vam.py", args)
        self.assertIn("check --trigger task", args)
        self.assertEqual(root.find(f".//{NS}RunLevel").text, "LeastPrivilege")

    def test_dashboard_task(self):
        root = parse(scheduler.dashboard_task_xml())
        self.assertIsNotNone(root.find(f".//{NS}LogonTrigger"))
        self.assertEqual(root.find(f".//{NS}ExecutionTimeLimit").text, "PT0S")
        self.assertIn("serve --no-scheduler", root.find(f".//{NS}Exec/{NS}Arguments").text)

    def test_names_differ_from_the_old_latency_monitor(self):
        self.assertNotIn("Latency", scheduler.PROBE_TASK + scheduler.DASH_TASK)

    def test_cron_and_alignment(self):
        self.assertEqual(scheduler._cron_expr(15), "*/15 * * * *")
        self.assertEqual(scheduler._cron_expr(120), "0 */2 * * *")
        self.assertEqual(scheduler.next_aligned(900, 1000), 1800)
        self.assertEqual(scheduler.next_aligned(900, 1800), 2700)


if __name__ == "__main__":
    unittest.main()
