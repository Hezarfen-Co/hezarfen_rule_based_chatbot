"""Aşama 8 birim testleri: cevap üretimi."""

import unittest

from src.catalog import FALLBACK, INTENTS, get_intent
from src.decision import (
    LOGIN_REQUIRED,
    ROLE_INSUFFICIENT,
    Decision,
)
from src.responder import Response, answer, render, role_display


def _decision(intent, **kw) -> Decision:
    base = dict(
        intent=intent,
        fallback=intent is None,
        source="rule" if intent else "fallback",
        confidence=1.0 if intent else 0.0,
    )
    base.update(kw)
    return Decision(**base)


class RenderTests(unittest.TestCase):
    def test_fallback(self) -> None:
        r = render(_decision(None))
        self.assertTrue(r.fallback)
        self.assertEqual(r.response_id, FALLBACK["response_id"])
        self.assertTrue(r.text)

    def test_normal_intent(self) -> None:
        r = render(_decision("greeting"))
        self.assertFalse(r.fallback)
        self.assertEqual(r.response_id, "welcome_message")
        # {selam} yer tutucusu, query verilmediğinde varsayılan selamla çözülür.
        expected = get_intent("greeting")["response_template"].replace("{selam}", "Merhaba!")
        self.assertEqual(r.text, expected)

    def test_login_required_prefix(self) -> None:
        r = render(_decision("report_card_view", auth_action=LOGIN_REQUIRED, required_role="ogrenci"))
        self.assertEqual(r.response_id, "report_card_info")
        self.assertIn("/login", r.text)
        # No-leak: giriş istenir; adımlar (Karnem içeriği) GÖSTERİLMEZ.
        self.assertNotIn("Karnem", r.text)

    def test_role_insufficient_prefix(self) -> None:
        r = render(_decision("course_create", auth_action=ROLE_INSUFFICIENT, required_role="ogretmen"))
        self.assertEqual(r.response_id, "course_create_instructions")
        # No-leak: adımlar ve ayrıcalıklı rol adı GÖSTERİLMEZ.
        self.assertNotIn("Öğretmen", r.text)
        self.assertNotIn("Yeni ders", r.text)

    def test_response_id_stable_under_gating(self) -> None:
        plain = render(_decision("course_create"))
        gated = render(_decision("course_create", auth_action=ROLE_INSUFFICIENT, required_role="ogretmen"))
        self.assertEqual(plain.response_id, gated.response_id)

    def test_all_intents_render_without_error(self) -> None:
        # Her intent'in şablonu sorunsuz render olmalı ve response_id eşleşmeli.
        for item in INTENTS:
            r = render(_decision(item["intent"]))
            self.assertEqual(r.response_id, item["response_id"])
            self.assertTrue(r.text.strip())


class RoleDisplayTests(unittest.TestCase):
    def test_known(self) -> None:
        self.assertEqual(role_display("admin"), "ADMIN")
        self.assertEqual(role_display("ogretmen"), "Öğretmen")

    def test_unknown_passthrough(self) -> None:
        self.assertEqual(role_display("kral"), "kral")


class AnswerEndToEndTests(unittest.TestCase):
    def test_greeting(self) -> None:
        r = answer("Merhaba")
        self.assertEqual(r.response_id, "welcome_message")

    def test_returns_response(self) -> None:
        self.assertIsInstance(answer("Karnemi göster", role="ogrenci", authenticated=True), Response)


if __name__ == "__main__":
    unittest.main()
