"""Kalite standardı — regresyon eşiği: metrikler bir tabanın altına düşerse KIRILIR.

Bu testler, ileride yapılan değişikliklerin sistemi sessizce bozmasını engeller.
Eşikler mevcut baseline'ın (macro-F1 0.992, acc %98.7, OOS recall %100) biraz
altına konur (gürültüye dayanıklı ama koruyucu). Kalite denetimi (Aşama: rol-bazlı
audit + adversarial doğrulama) sonrası taban yükseltildi: F1 0.80->0.92, acc
0.82->0.92, OOS 0.70->0.90, top3 0.90->0.97. Bunları düşüren değişiklik testi kırar.
"""

import unittest

from src.evaluation.benchmark import OOS_LABEL, load_benchmark
from src.decision import decide
from src.evaluation.evaluate import run_evaluation


class QualityRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = run_evaluation()

    def test_macro_f1_floor(self) -> None:
        self.assertGreaterEqual(self.report["macro_f1"], 0.92, self.report["macro_f1"])

    def test_accuracy_floor(self) -> None:
        self.assertGreaterEqual(self.report["accuracy"], 0.92)

    def test_coverage_floor(self) -> None:
        self.assertGreaterEqual(self.report["coverage"], 0.95)

    def test_oos_recall_floor(self) -> None:
        self.assertGreaterEqual(self.report["oos_recall"], 0.90)

    def test_top3_floor(self) -> None:
        self.assertGreaterEqual(self.report["top3_accuracy"], 0.97)

    def test_latency_reasonable(self) -> None:
        # Aşırı yavaşlamaya karşı gevşek tavan (ms).
        self.assertLess(self.report["latency_p95_ms"], 50.0)


class SafetyRegressionTests(unittest.TestCase):
    """Güvenlik: gizlilik intent'i asla kaçmamalı; auth sızıntısı olmamalı."""

    def test_privacy_recall_is_perfect(self) -> None:
        records = [
            r for r in load_benchmark() if r["expected_intent"] == "privacy_security"
        ]
        self.assertGreater(len(records), 0)
        for r in records:
            d = decide(r["question"], role="ogrenci", authenticated=True)
            self.assertEqual(
                d.intent, "privacy_security", f"Kaçan gizlilik sorusu: {r['question']!r}"
            )

    def test_no_auth_leak_on_benchmark(self) -> None:
        from src.observability import process

        for r in load_benchmark():
            if r["expected_intent"] == OOS_LABEL:
                continue
            # Ziyaretçi olarak sor; auth gerektiren intent'lerde gating olmalı, alarm olmamalı.
            _, trace = process(r["question"], role="ziyaretci", authenticated=False)
            self.assertEqual(trace["alarms"], [], f"{r['question']!r}: {trace['alarms']}")


class RulePrecisionRegressionTests(unittest.TestCase):
    def test_rule_layer_precision_perfect(self) -> None:
        from src import rules

        wrong = []
        oos_fired = []
        for r in load_benchmark():
            m = rules.match(r["question"])
            if m is None:
                continue
            if r["expected_intent"] == OOS_LABEL:
                oos_fired.append(r["question"])
            elif m.intent != r["expected_intent"]:
                wrong.append((r["question"], r["expected_intent"], m.intent))
        self.assertEqual(wrong, [], f"Kural yanlışları: {wrong}")
        self.assertEqual(oos_fired, [], f"OOS'ta ateşleyen kural: {oos_fired}")


if __name__ == "__main__":
    unittest.main()
