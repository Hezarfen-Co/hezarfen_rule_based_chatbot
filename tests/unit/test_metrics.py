"""Aşama 6/10 birim testleri: çekirdek sınıflandırma metrikleri."""

import unittest

from src.metrics import (
    accuracy,
    confusion_counts,
    macro_f1,
    per_class_scores,
)


# Küçük, elle doğrulanabilir örnek.
PAIRS = [("a", "a"), ("a", "b"), ("b", "b"), ("c", "c")]
LABELS = {"a", "b", "c"}


class ConfusionTests(unittest.TestCase):
    def test_counts(self) -> None:
        counts = confusion_counts(PAIRS, LABELS)
        self.assertEqual(counts["a"], (1, 0, 1))  # tp, fp, fn
        self.assertEqual(counts["b"], (1, 1, 0))
        self.assertEqual(counts["c"], (1, 0, 0))


class AccuracyTests(unittest.TestCase):
    def test_accuracy(self) -> None:
        self.assertAlmostEqual(accuracy(PAIRS), 0.75)

    def test_empty(self) -> None:
        self.assertEqual(accuracy([]), 0.0)


class MacroF1Tests(unittest.TestCase):
    def test_macro_f1(self) -> None:
        # a: f1=0.667, b: f1=0.667, c: f1=1.0 -> ort ~0.778
        self.assertAlmostEqual(macro_f1(PAIRS, LABELS), (2 / 3 + 2 / 3 + 1.0) / 3, places=6)

    def test_perfect(self) -> None:
        perfect = [("a", "a"), ("b", "b")]
        self.assertAlmostEqual(macro_f1(perfect, {"a", "b"}), 1.0)

    def test_empty_labels(self) -> None:
        self.assertEqual(macro_f1(PAIRS, set()), 0.0)


class PerClassTests(unittest.TestCase):
    def test_scores_and_support(self) -> None:
        scores = {s.label: s for s in per_class_scores(PAIRS, LABELS)}
        self.assertAlmostEqual(scores["a"].precision, 1.0)
        self.assertAlmostEqual(scores["a"].recall, 0.5)
        self.assertEqual(scores["a"].support, 2)
        self.assertAlmostEqual(scores["c"].f1, 1.0)


if __name__ == "__main__":
    unittest.main()
