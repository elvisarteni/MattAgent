import unittest

import tests.helpers  # noqa: F401  (sets sys.path)
from vero_monitor.domain import (
    Check,
    CheckResult,
    Point,
    Status,
    availability_percent,
    current_since,
    incidents,
    overall_status,
    timeline,
    worst,
)

U, D, X, N = Status.UP, Status.DEGRADED, Status.DOWN, Status.UNKNOWN


def cr(check, status, detail=""):
    return CheckResult(check, status, 1.0, detail)


class WorstTest(unittest.TestCase):
    def test_order(self):
        self.assertIs(worst([]), N)
        self.assertIs(worst([U, D]), D)
        self.assertIs(worst([U, X, D]), X)
        self.assertIs(worst([N, U]), U)


class OverallStatusTest(unittest.TestCase):
    def test_empty_is_unknown(self):
        self.assertIs(overall_status([]), N)

    def test_all_up(self):
        self.assertIs(overall_status([cr(Check.CLI, U), cr(Check.TASK, U)]), U)

    def test_task_down_means_down(self):
        self.assertIs(overall_status([cr(Check.CLI, U), cr(Check.TASK, X)]), X)

    def test_task_slow_means_degraded(self):
        self.assertIs(overall_status([cr(Check.CLI, U), cr(Check.TASK, D)]), D)

    def test_secondary_down_only_degrades(self):
        self.assertIs(overall_status([cr(Check.CLI, U), cr(Check.CHAT, X), cr(Check.TASK, U)]), D)

    def test_cli_is_primary_when_no_task(self):
        self.assertIs(overall_status([cr(Check.CLI, X), cr(Check.CHAT, U)]), X)
        self.assertIs(overall_status([cr(Check.CLI, U), cr(Check.CHAT, X)]), D)

    def test_chat_only(self):
        self.assertIs(overall_status([cr(Check.CHAT, X)]), X)


class AvailabilityTest(unittest.TestCase):
    def test_degraded_counts_as_available(self):
        self.assertEqual(availability_percent([U, D, X, U]), 75.0)

    def test_unknown_ignored_and_empty(self):
        self.assertIsNone(availability_percent([]))
        self.assertIsNone(availability_percent([N, N]))
        self.assertEqual(availability_percent([U, N]), 100.0)


class IncidentsTest(unittest.TestCase):
    def test_groups_consecutive_bad_runs(self):
        pts = [Point(0, U), Point(10, X, "task: timeout"), Point(20, D, "slow"), Point(30, U), Point(40, D, "slow"), Point(50, U)]
        inc = incidents(pts, min_degraded_runs=1)
        self.assertEqual(len(inc), 2)
        self.assertEqual((inc[0].start, inc[0].end, inc[0].worst, inc[0].runs), (10, 30, X, 2))
        self.assertEqual(inc[0].reason, "task: timeout")  # reason of the worst run
        self.assertEqual(inc[0].duration_s(now=99), 20)

    def test_single_slow_run_is_not_an_incident(self):
        pts = [Point(0, U), Point(10, D, "slow"), Point(20, U), Point(30, D), Point(40, D), Point(50, U)]
        inc = incidents(pts)
        self.assertEqual([(i.start, i.runs) for i in inc], [(30, 2)])
        self.assertEqual(len(incidents(pts, min_degraded_runs=1)), 2)

    def test_ongoing_incident(self):
        inc = incidents([Point(0, U), Point(10, X, "down")])
        self.assertIsNone(inc[0].end)
        self.assertEqual(inc[0].duration_s(now=70), 60)

    def test_unsorted_input_and_no_incident(self):
        self.assertEqual(incidents([Point(30, U), Point(10, U)]), [])
        self.assertEqual(len(incidents([Point(20, U), Point(10, X)])), 1)


class TimelineTest(unittest.TestCase):
    def test_worst_per_bin_and_empty_bins(self):
        pts = [Point(1, U), Point(2, X), Point(15, U), Point(29.9, D)]
        bins = timeline(pts, 0, 30, 3)
        self.assertEqual([(t, s, n) for t, s, n in bins], [(0, X, 2), (10, U, 1), (20, D, 1)])
        self.assertIs(timeline([], 0, 30, 3)[0][1], N)

    def test_outside_range_and_bad_args(self):
        self.assertEqual(timeline([Point(-1, X), Point(30, X)], 0, 30, 3)[0][2], 0)
        self.assertEqual(timeline([], 10, 10, 3), [])
        self.assertEqual(timeline([], 0, 10, 0), [])


class CurrentSinceTest(unittest.TestCase):
    def test_since_first_of_trailing_streak(self):
        self.assertEqual(current_since([Point(0, U), Point(10, X), Point(20, X)]), (X, 10))
        self.assertEqual(current_since([Point(20, U), Point(0, U)]), (U, 0))
        self.assertEqual(current_since([]), (N, None))


if __name__ == "__main__":
    unittest.main()
