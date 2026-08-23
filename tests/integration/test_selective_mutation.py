"""Seçici sınıflandırma + mutasyon testi regresyonu.

Kalite kapıları (kriterler.md ile hizalı):
- Mutasyon score = %100 (kritik invariant'lar bozulunca probe'lar YAKALAR).
- İşletim noktasında seçici risk düşük (kabul edilen cevaplarda az hata).
- OOS false-accept ölçülür ve raporlanır (regresyonda artışı fark edelim).

Bu testler ölçüm altyapısının kendisini de korur (harness bozulursa fark edilir).
"""

import unittest

from src.engine import Engine
from src.evaluation import mutation, selective


class NearOOSAbstentionTests(unittest.TestCase):
    """near_oos.jsonl: in-scope'a BENZEYEN kapsam-dışı sorgularda motor ASLA somut
    cevap vermez (abstain: clarify/scope-boundary). 'asla yanlış' engine-katmanı guard'ı."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.engine = Engine()
        cls.cases = selective.load_near_oos()

    def test_near_oos_all_abstain(self) -> None:
        self.assertGreater(len(self.cases), 0, "near_oos.jsonl boş")
        leaked = []
        for c in self.cases:
            role = c.get("role", "ogrenci")
            resp = self.engine.handle({
                "query": c["question"],
                "session": {"role": role, "authenticated": role != "ziyaretci"},
            })
            if resp["intent"] is not None:
                leaked.append((c["question"], resp["intent"]))
        self.assertEqual(leaked, [], f"near-OOS sızıntısı (somut cevap verildi): {leaked}")


class MutationScoreTests(unittest.TestCase):
    def test_baseline_probes_all_hold(self) -> None:
        report = mutation.compute()
        self.assertTrue(
            report["baseline_all_hold"],
            f"Temel invariant probe'ları tutmuyor: {report['baseline']}",
        )

    def test_mutation_score_is_perfect(self) -> None:
        # Kritik invariant'lar için mutasyon score = %100 (hepsi öldürülmeli).
        report = mutation.compute()
        survived = [r["mutation"] for r in report["rows"] if not r["killed"]]
        self.assertEqual(report["score"], 1.0, f"Hayatta kalan mutasyonlar: {survived}")


class SelectiveRiskTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = selective.compute()

    def test_operating_selective_risk_low(self) -> None:
        # İşletim eşiğinde kabul edilen cevaplarda hata oranı <= %1 (şu an ~%0.5).
        self.assertLessEqual(self.report["op_selective_risk"], 0.01)

    def test_aurc_low(self) -> None:
        # Risk-coverage eğrisi altındaki alan küçük (iyi ayrışma).
        self.assertLessEqual(self.report["aurc"], 0.02)

    def test_oos_false_accept_near_zero(self) -> None:
        # Gerçek motor kararıyla OOS false-accept ≈ 0 (near-OOS dahil hepsi abstain).
        # Bir sızıntı yeniden açılırsa bu kırılır (asla-yanlış guard'ı).
        fa = self.report["oos_false_accept"]
        self.assertLessEqual(fa, 0.02, "OOS false-accept arttı — near-OOS sızıntısı geri geldi?")


if __name__ == "__main__":
    unittest.main()
