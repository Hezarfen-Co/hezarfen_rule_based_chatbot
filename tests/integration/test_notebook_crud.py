"""Kişisel Defter CRUD ifadeleri için kullanıcı-bildirimi regresyonları."""

import unittest

from src.engine import Engine


class NotebookCrudRegressionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = Engine()

    def _ask(self, query: str, role: str = "ogrenci") -> dict:
        return self.engine.handle({
            "query": query,
            "session": {"role": role, "authenticated": True},
        })

    def test_reported_short_queries_are_answered_directly(self) -> None:
        cases = {
            "not silmek": ("note_delete", "note_delete_instructions"),
            "ben not silmek": ("note_delete", "note_delete_instructions"),
            "not değiştirmek": ("note_edit", "note_edit_instructions"),
        }
        for query, (intent, response_id) in cases.items():
            with self.subTest(query=query):
                result = self._ask(query)
                self.assertEqual(result["intent"], intent)
                self.assertEqual(result["response_id"], response_id)
                self.assertEqual(result["confidence"], 1.0)
                self.assertEqual(result["navigation"]["route"], "/notes")

    def test_personal_possessive_forms_are_not_blocked_as_grade_manipulation(self) -> None:
        self.assertEqual(self._ask("notumu silmek")["intent"], "note_delete")
        self.assertEqual(self._ask("notumu değiştirmek")["intent"], "note_edit")

    def test_explicit_grade_context_does_not_leak_into_notebook(self) -> None:
        cases = {
            "sınav notunu silmek": "exam_grade_student",
            "ödev notunu kaldırmak": "homework_grade",
            "not bantlarını değiştirmek": "school_settings",
        }
        for query, intent in cases.items():
            with self.subTest(query=query):
                self.assertEqual(self._ask(query, "yonetici")["intent"], intent)

    def test_actual_grade_manipulation_is_still_refused(self) -> None:
        result = self._ask("notumu yükselt")
        self.assertEqual(result["response_id"], "out_of_scope_action")
        self.assertIsNone(result["intent"])

    def test_named_third_party_note_is_student_grading_not_personal_notebook(self) -> None:
        result = self._ask("Ali'nin notunu düzelt", "ogretmen")
        self.assertEqual(result["intent"], "exam_grade_student")
        self.assertNotEqual(result["navigation"]["route"], "/notes")

    def test_not_this_but_that_keeps_student_context(self) -> None:
        cases = {
            "öğrencinin notunu değil kaydını sil": "course_remove_student",
            "öğrenciyi değil notunu sil": "exam_grade_student",
        }
        for query, expected in cases.items():
            with self.subTest(query=query):
                self.assertEqual(self._ask(query, "ogretmen")["intent"], expected)

    def test_unqualified_entry_exit_asks_which_meaning(self) -> None:
        result = self._ask("giriş çıkış yapcam", "ogretmen")
        self.assertEqual(result["response_id"], "clarification_prompt")
        self.assertIsNone(result["intent"])
        self.assertIn("mesai", result["text"])


if __name__ == "__main__":
    unittest.main()
