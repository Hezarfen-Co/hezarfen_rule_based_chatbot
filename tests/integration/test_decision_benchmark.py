"""Aşama 7 integration/değerlendirme: karar katmanının (eşikli) benchmark baseline'ı.

Eşik eklenince yeni metrikler doğar:
- coverage: in-scope soruların kaçı FALLBACK yerine cevaplandı.
- accuracy_on_covered: cevaplanınca ne kadar doğru.
- oos_recall: OOS soruların kaçı doğru şekilde FALLBACK'e atıldı.
- false_fallback: in-scope iken haksızca FALLBACK'e atılanlar.
"""

import unittest

from src.benchmark import OOS_LABEL, load_benchmark
from src.decision import DEFAULT_THRESHOLD, decide


def evaluate_decision(threshold: float = DEFAULT_THRESHOLD) -> dict:
    records = load_benchmark()
    ins = [r for r in records if r["expected_intent"] != OOS_LABEL]
    oos = [r for r in records if r["expected_intent"] == OOS_LABEL]

    covered = correct = 0
    for r in ins:
        d = decide(r["question"], threshold=threshold)
        if not d.fallback:
            covered += 1
            if d.intent == r["expected_intent"]:
                correct += 1

    oos_fallback = sum(1 for r in oos if decide(r["question"], threshold=threshold).fallback)

    return {
        "in_scope": len(ins),
        "oos": len(oos),
        "covered": covered,
        "correct": correct,
        "coverage": covered / len(ins) if ins else 0.0,
        "accuracy_on_covered": correct / covered if covered else 0.0,
        "false_fallback": len(ins) - covered,
        "oos_recall": oos_fallback / len(oos) if oos else 0.0,
    }


class DecisionBenchmarkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = evaluate_decision()

    def test_coverage(self) -> None:
        self.assertGreaterEqual(self.result["coverage"], 0.90)

    def test_accuracy_on_covered(self) -> None:
        self.assertGreaterEqual(self.result["accuracy_on_covered"], 0.75)

    def test_oos_recall_baseline(self) -> None:
        # Bilinen zayıflık: char n-gram OOS'u tam ayıramıyor. Aşama 11 iyileştirecek.
        self.assertGreaterEqual(self.result["oos_recall"], 0.30)


if __name__ == "__main__":
    r = evaluate_decision()
    print(f"=== KARAR KATMANI BASELINE (threshold={DEFAULT_THRESHOLD}) ===")
    print(f"In-scope            : {r['in_scope']}")
    print(f"Coverage            : {r['coverage']:.1%}  (covered={r['covered']})")
    print(f"Accuracy-on-covered : {r['accuracy_on_covered']:.1%}  (correct={r['correct']})")
    print(f"False fallback      : {r['false_fallback']}")
    print(f"OOS recall          : {r['oos_recall']:.1%}  ({r['oos']} OOS)")
