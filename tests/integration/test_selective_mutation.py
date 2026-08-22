"""Seçici sınıflandırma + mutasyon testi regresyonu.

Kalite kapıları (kriterler.md ile hizalı):
- Mutasyon score = %100 (kritik invariant'lar bozulunca probe'lar YAKALAR).
- İşletim noktasında seçici risk düşük (kabul edilen cevaplarda az hata).
- OOS false-accept ölçülür ve raporlanır (regresyonda artışı fark edelim).

Bu testler ölçüm altyapısının kendisini de korur (harness bozulursa fark edilir).
"""

import unittest

from src.evaluation import mutation, selective


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

    def test_oos_false_accept_reported(self) -> None:
        # Ölçülüyor ve mantıklı aralıkta (regresyonda artışı yakalamak için üst sınır).
        fa = self.report["oos_false_accept"]
        self.assertGreaterEqual(fa, 0.0)
        self.assertLessEqual(fa, 0.20, "OOS false-accept beklenenden yüksek — gerileme?")


if __name__ == "__main__":
    unittest.main()
