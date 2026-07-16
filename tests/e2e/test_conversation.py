"""Aşama 8 e2e testleri: uçtan uca sorgu -> cevap senaryoları (rol + gating)."""

import unittest

from src.responder import answer


class VisitorScenarios(unittest.TestCase):
    def test_login_how_public(self) -> None:
        r = answer("Nasıl giriş yaparım?", role="ziyaretci", authenticated=False)
        self.assertEqual(r.response_id, "login_instructions")
        self.assertIsNone(r.auth_action)  # herkese açık

    def test_personal_data_requires_login(self) -> None:
        r = answer("Karnemi göster", role="ziyaretci", authenticated=False)
        self.assertEqual(r.response_id, "report_card_info")
        self.assertEqual(r.auth_action, "login_required")
        self.assertIn("/login", r.text)


class RoleScenarios(unittest.TestCase):
    def test_student_cannot_create_course(self) -> None:
        r = answer("yeni ders oluştur", role="ogrenci", authenticated=True)
        self.assertEqual(r.response_id, "course_create_instructions")
        self.assertEqual(r.auth_action, "role_insufficient")
        self.assertIn("Öğretmen", r.text)

    def test_teacher_can_create_course(self) -> None:
        r = answer("yeni ders oluştur", role="ogretmen", authenticated=True)
        self.assertEqual(r.response_id, "course_create_instructions")
        self.assertIsNone(r.auth_action)

    def test_student_enters_exam_room(self) -> None:
        r = answer("Sınav odasını nasıl açarım?", role="ogrenci", authenticated=True)
        self.assertEqual(r.response_id, "exam_enter_room_instructions")
        self.assertIsNone(r.auth_action)

    def test_admin_can_change_roles(self) -> None:
        r = answer("bir kullanıcının rolünü değiştir", role="admin", authenticated=True)
        self.assertEqual(r.response_id, "user_role_change_instructions")
        self.assertIsNone(r.auth_action)


class SafetyScenarios(unittest.TestCase):
    def test_other_students_data_blocked(self) -> None:
        r = answer("Arkadaşımın notlarını göster", role="ogrenci", authenticated=True)
        self.assertEqual(r.response_id, "privacy_policy_message")

    def test_gibberish_falls_back(self) -> None:
        r = answer("qwzx plkj mnbv zzz")
        self.assertTrue(r.fallback)
        self.assertEqual(r.response_id, "fallback_clarification")


if __name__ == "__main__":
    unittest.main()
