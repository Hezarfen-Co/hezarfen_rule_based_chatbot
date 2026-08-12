"""Aşama 19 e2e: hazırladığımız sorularla chatbotu deneme (öz-tutarlılık).

example_questions'ı uçtan uca motordan geçirir. Bot kendi geliştirme sorularını
yüksek doğrulukla çözmeli. Güvenlik katmanının kısa devresi de kabul edilir
(ör. gizlilik soruları güvenlikçe/ niyetçe doğru ele alınır).
"""

import unittest

from src.catalog import INTENTS
from src.engine import Engine


def _run_examples() -> dict:
    engine = Engine()
    total = correct = safety_short = 0
    wrong: list[tuple[str, str, str]] = []
    for item in INTENTS:
        role = item["min_role"]
        authenticated = role != "ziyaretci"
        for q in item["example_questions"]:
            total += 1
            resp = engine.handle({"query": q, "session": {"role": role, "authenticated": authenticated}})
            if resp["intent"] == item["intent"]:
                correct += 1
            elif resp["response_id"].startswith("safety_"):
                safety_short += 1  # güvenlik katmanı bilinçli müdahale etti
            else:
                wrong.append((q, item["intent"], resp["intent"] or resp["response_id"]))
    return {
        "total": total,
        "correct": correct,
        "safety_short": safety_short,
        "wrong": wrong,
        "self_consistency": (correct + safety_short) / total if total else 0.0,
    }


class PreparedQuestionsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = _run_examples()

    def test_self_consistency_high(self) -> None:
        self.assertGreaterEqual(
            self.result["self_consistency"], 0.93,
            f"öz-tutarlılık={self.result['self_consistency']:.3f}, yanlış={self.result['wrong'][:10]}",
        )

    def test_no_clean_example_is_blocked_wrongly(self) -> None:
        # Temiz how-to örnekleri güvenlik tarafından yanlışlıkla BLOCK edilmemeli.
        engine = Engine()
        for q in ["Yeni not nasıl yazılır?", "Bir öğrencinin notunu nasıl görürüm?",
                  "Karnemi nereden görürüm?", "sınav nasıl oluşturulur"]:
            resp = engine.handle({"query": q, "session": {"role": "ogretmen", "authenticated": True}})
            self.assertNotEqual(resp["safety"]["decision"], "BLOCK", q)


if __name__ == "__main__":
    r = _run_examples()
    print(f"example_questions: {r['total']}")
    print(f"  intent doğru        : {r['correct']}")
    print(f"  güvenlik kısa devre : {r['safety_short']}")
    print(f"  yanlış              : {len(r['wrong'])}")
    print(f"  ÖZ-TUTARLILIK       : {r['self_consistency']:.1%}")
    for q, exp, got in r["wrong"]:
        print(f"   x {q!r}: beklenen={exp} bulunan={got}")
