"""Aşama 5 integration/değerlendirme: kural katmanının benchmark üzerindeki baseline'ı.

Kural katmanı yüksek-kesinlik hedefler:
- Kapsanan (karar verilen) in-scope sorularda kesinlik ~%100 olmalı.
- Kapsam dışı (OOS) sorularda kural KESİNLİKLE ateşlememeli (yanlış-pozitif = 0).
Coverage'ın düşük olması normaldir; gerisini benzerlik katmanı toplar.
"""

import unittest

from src.evaluation.benchmark import OOS_LABEL, load_benchmark
from src.rules import match


def evaluate_rule_layer(records: list[dict]) -> dict:
    in_scope = [r for r in records if r["expected_intent"] != OOS_LABEL]
    oos = [r for r in records if r["expected_intent"] == OOS_LABEL]

    covered = 0
    correct = 0
    wrong: list[tuple[str, str, str]] = []
    for r in in_scope:
        m = match(r["question"])
        if m is None:
            continue
        covered += 1
        if m.intent == r["expected_intent"]:
            correct += 1
        else:
            wrong.append((r["question"], r["expected_intent"], m.intent))

    oos_fired = [(r["question"], match(r["question"]).intent) for r in oos if match(r["question"])]

    return {
        "in_scope": len(in_scope),
        "oos": len(oos),
        "covered": covered,
        "correct": correct,
        "coverage": covered / len(in_scope) if in_scope else 0.0,
        "precision_on_covered": correct / covered if covered else 1.0,
        "oos_fired": len(oos_fired),
        "wrong": wrong,
        "oos_fired_detail": oos_fired,
    }


class RuleLayerBenchmarkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = evaluate_rule_layer(load_benchmark())

    def test_precision_on_covered_is_perfect(self) -> None:
        self.assertEqual(
            self.result["precision_on_covered"],
            1.0,
            f"Yanlış sınıflananlar: {self.result['wrong']}",
        )

    def test_rules_do_not_fire_on_oos(self) -> None:
        self.assertEqual(
            self.result["oos_fired"],
            0,
            f"OOS'ta ateşleyen kurallar: {self.result['oos_fired_detail']}",
        )

    def test_has_some_coverage(self) -> None:
        self.assertGreater(self.result["covered"], 0)


if __name__ == "__main__":
    result = evaluate_rule_layer(load_benchmark())
    print("=== KURAL KATMANI BASELINE ===")
    print(f"In-scope soru       : {result['in_scope']}")
    print(f"Kapsanan (covered)  : {result['covered']}")
    print(f"Coverage            : {result['coverage']:.1%}")
    print(f"Precision (covered) : {result['precision_on_covered']:.1%}")
    print(f"OOS yanlış-ateşleme : {result['oos_fired']}")
    if result["wrong"]:
        print("Yanlışlar:")
        for q, exp, got in result["wrong"]:
            print(f"  - {q!r}: beklenen={exp} bulunan={got}")
