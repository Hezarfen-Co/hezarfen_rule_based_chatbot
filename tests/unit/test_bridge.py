"""Backend ``chat.reply`` rol sözleşmesi için köprü regresyon testleri."""

import unittest

from src.bridge_contract import resolve_session
from src.engine import Engine


class BridgeRoleContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = Engine()

    def test_backend_asker_role_is_accepted_for_every_school_role(self) -> None:
        for role in ("parent", "student", "teacher", "manager", "admin"):
            with self.subTest(role=role):
                self.assertEqual(
                    resolve_session({"asker_role": role}, "ogrenci"),
                    (role, True),
                )

    def test_asker_role_wins_over_legacy_role_fields(self) -> None:
        role, authenticated = resolve_session(
            {
                "asker_role": "admin",
                "role": "teacher",
                "session": {"role": "student", "authenticated": False},
            },
            "ogrenci",
        )
        self.assertEqual(role, "admin")
        self.assertTrue(authenticated)

    def test_legacy_session_role_remains_supported(self) -> None:
        self.assertEqual(
            resolve_session(
                {"session": {"role": "teacher", "authenticated": True}},
                "ogrenci",
            ),
            ("teacher", True),
        )

    def test_missing_role_uses_configured_legacy_fallback(self) -> None:
        self.assertEqual(resolve_session({}, "manager"), ("manager", True))

    def test_backend_role_changes_the_rendered_answer_scope(self) -> None:
        question = "sınav nasıl oluşturulur?"
        student_role, student_auth = resolve_session(
            {"asker_role": "student"}, "ogrenci"
        )
        admin_role, admin_auth = resolve_session({"asker_role": "admin"}, "ogrenci")
        student = self.engine.handle(
            {
                "query": question,
                "session": {"role": student_role, "authenticated": student_auth},
            }
        )
        admin = self.engine.handle(
            {
                "query": question,
                "session": {"role": admin_role, "authenticated": admin_auth},
            }
        )

        self.assertEqual(student["auth_action"], "role_insufficient")
        self.assertEqual(student["required_role"], "ogretmen")  # sözleşme metadata'sı
        self.assertIsNone(student["navigation"])                # no-leak: rota sızmaz
        self.assertIsNone(admin["auth_action"])
        self.assertIsNotNone(admin["navigation"])
        self.assertTrue(admin["navigation"]["available"])


if __name__ == "__main__":
    unittest.main()
