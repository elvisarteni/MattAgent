import unittest

import tests.conftest  # noqa: F401
from vero_latency import stats


def p(ms, status="ok", epoch=0, model="m"):
    return {"total_ms": ms, "first_byte_ms": ms, "status": status, "epoch": epoch, "model": model, "ts": "t"}


class StatsTest(unittest.TestCase):
    def test_percentile(self):
        self.assertIsNone(stats.percentile([], 50))
        self.assertEqual(stats.percentile([5], 95), 5)
        self.assertEqual(stats.percentile([1, 2, 3, 4], 50), 2.5)
        self.assertAlmostEqual(stats.percentile(list(range(1, 101)), 95), 95.05)

    def test_summary_counts_failures_in_availability_only(self):
        s = stats.summarize([p(100), p(200), p(9000, "timeout"), p(6000)], warn_ms=5000, crit_ms=8000)
        self.assertEqual((s["probes"], s["ok"], s["failed"]), (4, 3, 1))
        self.assertEqual(s["availability_percent"], 75.0)
        self.assertEqual(s["max_ms"], 6000)
        self.assertEqual((s["warn_breaches"], s["crit_breaches"]), (1, 0))

    def test_empty_summary(self):
        s = stats.summarize([], 1, 2)
        self.assertIsNone(s["availability_percent"])
        self.assertIsNone(s["last"])

    def test_bucket_seconds(self):
        self.assertEqual(stats.bucket_seconds(1), 60)
        self.assertEqual(stats.bucket_seconds(24), 900)
        self.assertEqual(stats.bucket_seconds(720), 21600)

    def test_series_groups_by_bucket(self):
        rows = [p(100, epoch=10), p(300, epoch=50), p(0, "error", epoch=70), p(500, epoch=130)]
        out = stats.series(rows, 60)["m"]
        self.assertEqual([b["t"] for b in out], [0, 60, 120])
        self.assertEqual(out[0]["p50"], 200)
        self.assertEqual(out[1]["fail"], 1)
        self.assertIsNone(out[1]["p50"])


if __name__ == "__main__":
    unittest.main()
