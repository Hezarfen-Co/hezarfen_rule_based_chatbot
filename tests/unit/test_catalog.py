"""Aşama 1+2 birim testleri: intent kataloğu, rol modeli ve doğrulayıcı.

Her katalog metodu ve her önemli değişmez için ayrı test.
"""

import unittest

from src import catalog
from src.catalog import (
    FALLBACK,
    INTENTS,
    MIN_AUTHENTICATED_ROLE,
    REQUIRED_INTENT_FIELDS,
    ROLE_HIERARCHY,
    get_intent,
    is_known_role,
    list_intent_names,
    meets_role,
    role_rank,
    validate_catalog,
)


class RoleModelTests(unittest.TestCase):
    def test_hierarchy_is_ordered_low_to_high(self) -> None:
        self.assertEqual(ROLE_HIERARCHY[0], "ziyaretci")
        self.assertEqual(ROLE_HIERARCHY[-1], "admin")

    def test_role_rank_is_strictly_increasing(self) -> None:
        ranks = [role_rank(r) for r in ROLE_HIERARCHY]
        self.assertEqual(ranks, sorted(ranks))
        self.assertEqual(len(set(ranks)), len(ranks))

    def test_role_rank_unknown_raises(self) -> None:
        with self.assertRaises(KeyError):
            role_rank("kral")

    def test_is_known_role(self) -> None:
        self.assertTrue(is_known_role("ogrenci"))
        self.assertFalse(is_known_role("kral"))

    def test_meets_role_higher_satisfies_lower(self) -> None:
        self.assertTrue(meets_role("admin", "ogrenci"))
        self.assertTrue(meets_role("ogretmen", "ogretmen"))

    def test_meets_role_lower_fails_higher(self) -> None:
        self.assertFalse(meets_role("ogrenci", "ogretmen"))
        self.assertFalse(meets_role("ziyaretci", "ogrenci"))

    def test_meets_role_unknown_raises(self) -> None:
        with self.assertRaises(KeyError):
            meets_role("ogrenci", "kral")


class GetIntentTests(unittest.TestCase):
    def test_returns_known_intent(self) -> None:
        intent = get_intent("exam_create")
        self.assertIsNotNone(intent)
        self.assertEqual(intent["response_id"], "exam_create_instructions")

    def test_returns_none_for_unknown(self) -> None:
        self.assertIsNone(get_intent("does_not_exist"))

    def test_list_intent_names_matches_catalog(self) -> None:
        names = list_intent_names()
        self.assertEqual(len(names), len(INTENTS))
        self.assertEqual(names, [i["intent"] for i in INTENTS])


class ValidateCatalogTests(unittest.TestCase):
    def test_catalog_is_valid(self) -> None:
        result = validate_catalog()
        self.assertGreater(result["intent_count"], 0)
        self.assertEqual(result["intent_count"], result["response_count"])
        self.assertGreater(result["example_question_count"], result["intent_count"])
        self.assertGreater(result["category_count"], 1)

    def test_all_intents_have_required_fields(self) -> None:
        for item in INTENTS:
            missing = REQUIRED_INTENT_FIELDS.difference(item)
            self.assertEqual(missing, set(), f"{item.get('intent')} eksik: {missing}")

    def test_intent_names_unique(self) -> None:
        names = [i["intent"] for i in INTENTS]
        self.assertEqual(len(names), len(set(names)))

    def test_response_ids_unique(self) -> None:
        ids = [i["response_id"] for i in INTENTS]
        self.assertEqual(len(ids), len(set(ids)))

    def test_example_questions_unique_across_catalog(self) -> None:
        questions = [q for i in INTENTS for q in i["example_questions"]]
        self.assertEqual(len(questions), len(set(questions)))

    def test_every_intent_has_examples(self) -> None:
        for item in INTENTS:
            self.assertTrue(item["example_questions"], f"{item['intent']} örnek soru yok")

    def test_min_role_values_are_known(self) -> None:
        for item in INTENTS:
            self.assertTrue(is_known_role(item["min_role"]), item["intent"])

    def test_auth_required_consistent_with_min_role(self) -> None:
        for item in INTENTS:
            expected = role_rank(item["min_role"]) >= role_rank(MIN_AUTHENTICATED_ROLE)
            self.assertEqual(bool(item["auth_required"]), expected, item["intent"])

    def test_must_not_match_targets_exist(self) -> None:
        known = {i["intent"] for i in INTENTS}
        for item in INTENTS:
            for target in item["must_not_match"]:
                self.assertIn(target, known, f"{item['intent']} -> {target}")

    def test_must_not_match_excludes_self(self) -> None:
        for item in INTENTS:
            self.assertNotIn(item["intent"], item["must_not_match"], item["intent"])

    def test_fallback_present(self) -> None:
        self.assertTrue(FALLBACK.get("response_id"))
        self.assertTrue(FALLBACK.get("response_template"))


class ValidatorFailureTests(unittest.TestCase):
    """Doğrulayıcının gerçekten hata yakaladığını, geçici bozma ile kanıtla."""

    def test_detects_duplicate_intent(self) -> None:
        original = list(INTENTS)
        try:
            INTENTS.append(dict(original[0]))  # aynı intent'i tekrar ekle
            with self.assertRaises(ValueError):
                validate_catalog()
        finally:
            INTENTS[:] = original

    def test_detects_unknown_must_not_match(self) -> None:
        original = catalog.INTENTS[0]["must_not_match"]
        try:
            catalog.INTENTS[0]["must_not_match"] = ["yok_boyle_intent"]
            with self.assertRaises(ValueError):
                validate_catalog()
        finally:
            catalog.INTENTS[0]["must_not_match"] = original

    def test_detects_auth_inconsistency(self) -> None:
        original = catalog.INTENTS[0]["auth_required"]
        try:
            # greeting min_role=ziyaretci; auth_required=True yaparak tutarsızlık kur.
            catalog.INTENTS[0]["auth_required"] = True
            with self.assertRaises(ValueError):
                validate_catalog()
        finally:
            catalog.INTENTS[0]["auth_required"] = original


if __name__ == "__main__":
    unittest.main()
