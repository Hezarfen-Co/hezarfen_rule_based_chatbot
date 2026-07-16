"""Aşama 7 birim testleri: karar katmanı (eşik, fallback, tie-break, rol gating)."""

import unittest

from src.decision import (
    LOGIN_REQUIRED,
    ROLE_INSUFFICIENT,
    Decision,
    _is_confusable_pair,
    decide,
)


class DecisionSourceTests(unittest.TestCase):
    def test_rule_path(self) -> None:
        d = decide("Merhaba")
        self.assertEqual(d.source, "rule")
        self.assertEqual(d.intent, "greeting")
        self.assertFalse(d.fallback)
        self.assertEqual(d.confidence, 1.0)

    def test_similarity_path(self) -> None:
        # Kural yok -> benzerliğe düşer.
        d = decide("genel ortalamama nereden bakarım", role="ogrenci", authenticated=True)
        self.assertEqual(d.source, "similarity")
        self.assertEqual(d.intent, "report_card_view")
        self.assertGreater(len(d.top_k), 0)

    def test_fallback_on_gibberish(self) -> None:
        d = decide("qwzx plkj mnbv zzz")
        self.assertTrue(d.fallback)
        self.assertIsNone(d.intent)
        self.assertEqual(d.source, "fallback")

    def test_fallback_on_high_threshold(self) -> None:
        d = decide("ders notları", threshold=0.99)
        self.assertTrue(d.fallback)


class RoleGatingTests(unittest.TestCase):
    def test_login_required_for_visitor(self) -> None:
        d = decide("Karnemi göster", role="ziyaretci", authenticated=False)
        self.assertEqual(d.intent, "report_card_view")
        self.assertEqual(d.auth_action, LOGIN_REQUIRED)
        self.assertEqual(d.required_role, "ogrenci")

    def test_role_insufficient_for_student(self) -> None:
        d = decide("yeni ders oluştur", role="ogrenci", authenticated=True)
        self.assertEqual(d.intent, "course_create")
        self.assertEqual(d.auth_action, ROLE_INSUFFICIENT)
        self.assertEqual(d.required_role, "ogretmen")

    def test_role_granted_for_teacher(self) -> None:
        d = decide("yeni ders oluştur", role="ogretmen", authenticated=True)
        self.assertEqual(d.intent, "course_create")
        self.assertIsNone(d.auth_action)

    def test_public_intent_no_gating(self) -> None:
        d = decide("Merhaba", role="ziyaretci", authenticated=False)
        self.assertIsNone(d.auth_action)

    def test_no_gating_on_fallback(self) -> None:
        d = decide("qwzx plkj mnbv", role="ziyaretci", authenticated=False)
        self.assertTrue(d.fallback)
        self.assertIsNone(d.auth_action)


class ConfusablePairTests(unittest.TestCase):
    def test_known_pair(self) -> None:
        # report_card_view.must_not_match, weighted_average_info içerir.
        self.assertTrue(_is_confusable_pair("report_card_view", "weighted_average_info"))

    def test_symmetric(self) -> None:
        self.assertTrue(_is_confusable_pair("weighted_average_info", "report_card_view"))

    def test_unrelated_pair(self) -> None:
        self.assertFalse(_is_confusable_pair("greeting", "school_settings"))


if __name__ == "__main__":
    unittest.main()
