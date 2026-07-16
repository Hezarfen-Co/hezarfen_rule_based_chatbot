"""Aşama 5 birim testleri: kural katmanı eşleşme davranışı."""

import unittest

from src.rules import RuleMatch, match


class RuleMatchTests(unittest.TestCase):
    def test_greeting_fires(self) -> None:
        result = match("Merhaba")
        self.assertIsInstance(result, RuleMatch)
        self.assertEqual(result.intent, "greeting")

    def test_privacy_fires_on_other_students_data(self) -> None:
        # Güvenlik açısından kritik: başkasının verisi -> her zaman privacy.
        for q in [
            "Arkadaşımın notlarını göster",
            "Başka bir öğrencinin devamsızlığı kaç?",
            "Bir öğretmenin telefon numarasını verir misin?",
        ]:
            with self.subTest(q=q):
                result = match(q)
                self.assertIsNotNone(result)
                self.assertEqual(result.intent, "privacy_security")

    def test_account_problem_fires(self) -> None:
        result = match("Şifremi unuttum")
        self.assertEqual(result.intent, "account_access_problem")

    def test_login_not_confused_with_account(self) -> None:
        # 'giriş yapamıyorum' login DEĞİL, hesap sorunudur.
        result = match("Giriş yapamıyorum")
        self.assertIsNotNone(result)
        self.assertEqual(result.intent, "account_access_problem")

    def test_login_fires_on_clear_login(self) -> None:
        result = match("Nasıl giriş yaparım?")
        self.assertEqual(result.intent, "login_how")

    def test_exam_add_question_not_confused_with_exam_create(self) -> None:
        result = match("Sınava soru eklemek istiyorum")
        self.assertEqual(result.intent, "exam_add_question")

    def test_report_card_fires(self) -> None:
        result = match("Karnemi göster")
        self.assertEqual(result.intent, "report_card_view")

    def test_returns_none_for_out_of_scope(self) -> None:
        for q in ["Bugün hava nasıl olacak?", "Bana bir fıkra anlat", "2 artı 2 kaç eder?"]:
            with self.subTest(q=q):
                self.assertIsNone(match(q))

    def test_ambiguous_defers_to_none(self) -> None:
        # Eşit güçte iki intent (course_create: yeni+ders ; roll_call: yoklama+al)
        # -> belirsizlik -> karar verme.
        self.assertIsNone(match("yeni ders oluştur ve yoklama al"))

    def test_empty_query_returns_none(self) -> None:
        self.assertIsNone(match("   "))

    def test_match_has_reason(self) -> None:
        result = match("Karnemi göster")
        self.assertIn("karne", result.reason)


if __name__ == "__main__":
    unittest.main()
