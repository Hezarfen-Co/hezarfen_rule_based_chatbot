"""Aşama 6 integration/değerlendirme: kural + benzerlik boru hattı baseline'ı.

Bu aşamada eşik/OOS YOK (o Aşama 7). Bu yüzden yalnızca in-scope sorular üzerinde
sınıflandırma kalitesi ölçülür: accuracy ve macro-F1. Tahmin:
    kural katmanı bir şey döndürürse onu; yoksa benzerlik katmanının en iyisini kullan.
"""

import unittest

from src import rules
from src.evaluation.benchmark import OOS_LABEL, load_benchmark
from src.catalog import INTENTS
from src.evaluation.metrics import accuracy, macro_f1, per_class_scores
from src.similarity import get_default_matcher


def predict(query: str) -> str:
    rule_match = rules.match(query)
    if rule_match is not None:
        return rule_match.intent
    best = get_default_matcher().best(query)
    return best.intent if best is not None else "oos"


def evaluate_pipeline() -> dict:
    records = [r for r in load_benchmark() if r["expected_intent"] != OOS_LABEL]
    labels = {i["intent"] for i in INTENTS}
    pairs = [(r["expected_intent"], predict(r["question"])) for r in records]
    return {
        "n": len(pairs),
        "accuracy": accuracy(pairs),
        "macro_f1": macro_f1(pairs, labels),
        "pairs": pairs,
        "per_class": per_class_scores(pairs, labels),
    }


class PipelineBenchmarkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = evaluate_pipeline()

    def test_accuracy_baseline(self) -> None:
        self.assertGreaterEqual(
            self.result["accuracy"], 0.70, f"accuracy={self.result['accuracy']:.3f}"
        )

    def test_macro_f1_baseline(self) -> None:
        self.assertGreaterEqual(
            self.result["macro_f1"], 0.65, f"macro_f1={self.result['macro_f1']:.3f}"
        )


if __name__ == "__main__":
    result = evaluate_pipeline()
    print("=== KURAL + BENZERLIK BASELINE (in-scope, eşiksiz) ===")
    print(f"Soru sayısı : {result['n']}")
    print(f"Accuracy    : {result['accuracy']:.1%}")
    print(f"Macro-F1    : {result['macro_f1']:.3f}")
    print("\nEn zayıf 10 intent (F1):")
    worst = sorted(result["per_class"], key=lambda s: (s.f1, -s.support))
    for s in worst[:10]:
        print(f"  {s.label:26s} P={s.precision:.2f} R={s.recall:.2f} F1={s.f1:.2f} (n={s.support})")
    print("\nYanlış tahminler:")
    for true, pred in result["pairs"]:
        if true != pred:
            print(f"  beklenen={true:26s} bulunan={pred}")
