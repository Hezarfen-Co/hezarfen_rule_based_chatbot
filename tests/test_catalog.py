import unittest

from src.QandA import get_intent
from src.main import validate_catalog


class CatalogTests(unittest.TestCase):
    def test_catalog_is_valid(self) -> None:
        result = validate_catalog()

        self.assertGreater(result["intent_count"], 0)
        self.assertGreater(result["example_question_count"], result["intent_count"])

    def test_get_intent_returns_known_intent(self) -> None:
        intent = get_intent("course_grades")

        self.assertIsNotNone(intent)
        self.assertEqual(intent["response_id"], "course_grades_list")

    def test_get_intent_returns_none_for_unknown_intent(self) -> None:
        self.assertIsNone(get_intent("does_not_exist"))


if __name__ == "__main__":
    unittest.main()
