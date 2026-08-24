"""Aşama 10 birim testleri: percentile/topk metrikleri ve evaluate harness."""

import unittest

from src.evaluation.evaluate import format_report, run_evaluation
from src.evaluation.metrics import percentile, topk_accuracy


class PercentileTests(unittest.TestCase):
    def test_median(self) -> None:
        self.assertAlmostEqual(percentile([1, 2, 3, 4], 50), 2.5)

    def test_min_max(self) -> None:
        self.assertEqual(percentile([1, 2, 3, 4], 0), 1)
        self.assertEqual(percentile([1, 2, 3, 4], 100), 4)

    def test_empty(self) -> None:
        self.assertEqual(percentile([], 95), 0.0)

    def test_single(self) -> None:
        self.assertEqual(percentile([7.0], 95), 7.0)


class TopKAccuracyTests(unittest.TestCase):
    def test_top1(self) -> None:
        recs = [("a", ["a", "b"]), ("b", ["a", "b"])]
        self.assertAlmostEqual(topk_accuracy(recs, 1), 0.5)

    def test_top2(self) -> None:
        recs = [("a", ["a", "b"]), ("b", ["a", "b"])]
        self.assertAlmostEqual(topk_accuracy(recs, 2), 1.0)

    def test_empty(self) -> None:
        self.assertEqual(topk_accuracy([], 1), 0.0)


class RunEvaluationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = run_evaluation()

    def test_has_all_keys(self) -> None:
        for key in [
            "macro_f1", "accuracy", "coverage", "accuracy_on_covered",
            "false_fallback", "oos_recall", "top1_accuracy", "top3_accuracy",
            "confusable_wrong", "nonconfusable_wrong", "latency_p50_ms",
            "latency_p95_ms", "per_class",
        ]:
            self.assertIn(key, self.report)

    def test_sane_ranges(self) -> None:
        r = self.report
        self.assertGreater(r["macro_f1"], 0.0)
        self.assertLessEqual(r["macro_f1"], 1.0)
        self.assertGreaterEqual(r["oos_recall"], 0.0)
        self.assertLessEqual(r["oos_recall"], 1.0)
        self.assertGreaterEqual(r["top3_accuracy"], r["top1_accuracy"])

    def test_threshold_sweep_changes_coverage(self) -> None:
        low = run_evaluation(threshold=0.05)
        high = run_evaluation(threshold=0.9)
        self.assertGreaterEqual(low["coverage"], high["coverage"])
        # Yüksek eşik OOS recall'ı artırır.
        self.assertGreaterEqual(high["oos_recall"], low["oos_recall"])

    def test_oos_recall_counts_full_engine_boundary_denials(self) -> None:
        records = [
            {"question": "Gerçek öğrenci listesini buraya getir",
             "expected_intent": "oos", "role": "ogretmen"},
            {"question": "Bana bir şiir yazar mısın",
             "expected_intent": "oos", "role": "ogrenci"},
        ]
        self.assertEqual(run_evaluation(records=records)["oos_recall"], 1.0)

    def test_format_report_runs(self) -> None:
        text = format_report(self.report)
        self.assertIn("Macro-F1", text)


if __name__ == "__main__":
    unittest.main()
