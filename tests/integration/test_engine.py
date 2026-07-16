"""Aşama 12 integration testleri: backend motoru + sözleşme."""

import unittest

from src.engine import Engine, RequestError, handle_request


class ContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = Engine()

    def test_response_has_contract_keys(self) -> None:
        resp = self.engine.handle({"query": "Merhaba"})
        for key in [
            "trace_id", "response_id", "text", "intent",
            "confidence", "fallback", "auth_action", "required_role",
        ]:
            self.assertIn(key, resp)

    def test_greeting(self) -> None:
        resp = self.engine.handle({"query": "Merhaba"})
        self.assertEqual(resp["response_id"], "welcome_message")
        self.assertFalse(resp["fallback"])

    def test_trace_id_honored(self) -> None:
        resp = self.engine.handle({"query": "Merhaba", "trace_id": "abc-1"})
        self.assertEqual(resp["trace_id"], "abc-1")

    def test_trace_id_generated_when_absent(self) -> None:
        resp = self.engine.handle({"query": "Merhaba"})
        self.assertTrue(resp["trace_id"].startswith("req-"))

    def test_role_gating_in_contract(self) -> None:
        resp = self.engine.handle(
            {"query": "yeni ders oluştur", "session": {"role": "ogrenci", "authenticated": True}}
        )
        self.assertEqual(resp["intent"], "course_create")
        self.assertEqual(resp["auth_action"], "role_insufficient")
        self.assertEqual(resp["required_role"], "ogretmen")

    def test_login_required_in_contract(self) -> None:
        resp = self.engine.handle(
            {"query": "Karnemi göster", "session": {"role": "ziyaretci", "authenticated": False}}
        )
        self.assertEqual(resp["auth_action"], "login_required")

    def test_fallback(self) -> None:
        resp = self.engine.handle({"query": "qwzx plkj mnbv"})
        self.assertTrue(resp["fallback"])
        self.assertEqual(resp["response_id"], "fallback_clarification")


class ValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = Engine()

    def test_empty_query_raises(self) -> None:
        with self.assertRaises(RequestError):
            self.engine.handle({"query": "   "})

    def test_missing_query_raises(self) -> None:
        with self.assertRaises(RequestError):
            self.engine.handle({})

    def test_unknown_role_raises(self) -> None:
        with self.assertRaises(RequestError):
            self.engine.handle({"query": "Merhaba", "session": {"role": "kral"}})

    def test_visitor_cannot_be_authenticated(self) -> None:
        with self.assertRaises(RequestError):
            self.engine.handle(
                {"query": "Merhaba", "session": {"role": "ziyaretci", "authenticated": True}}
            )


class LogSinkTests(unittest.TestCase):
    def test_log_sink_receives_trace(self) -> None:
        captured: list[dict] = []
        engine = Engine(log_sink=captured.append)
        engine.handle({"query": "Merhaba", "trace_id": "t9"})
        self.assertEqual(len(captured), 1)
        self.assertEqual(captured[0]["trace_id"], "t9")
        self.assertIn("latency_ms", captured[0])


class SharedEngineTests(unittest.TestCase):
    def test_handle_request_helper(self) -> None:
        resp = handle_request({"query": "Merhaba"})
        self.assertEqual(resp["response_id"], "welcome_message")


if __name__ == "__main__":
    unittest.main()
