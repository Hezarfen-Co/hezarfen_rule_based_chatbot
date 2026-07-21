"""Aşama 9 birim testleri: yapısal loglama / izleme (trace)."""

import json
import unittest

from src.decision import LOGIN_REQUIRED, Decision
from src.observability import (
    check_auth_alarms,
    new_trace_id,
    process,
    trace_to_json,
)


class TraceIdTests(unittest.TestCase):
    def test_prefix_and_uniqueness(self) -> None:
        a, b = new_trace_id(), new_trace_id()
        self.assertTrue(a.startswith("req-"))
        self.assertNotEqual(a, b)


class ProcessTests(unittest.TestCase):
    def test_returns_response_and_trace(self) -> None:
        response, trace = process("Merhaba", trace_id="t1")
        self.assertEqual(trace["trace_id"], "t1")
        self.assertEqual(response.response_id, "welcome_message")

    def test_required_trace_keys(self) -> None:
        _, trace = process("Merhaba")
        for key in [
            "trace_id", "query_masked", "normalized", "roots", "rule_layer",
            "similarity", "decision", "response_id", "latency_ms", "alarms",
        ]:
            self.assertIn(key, trace)

    def test_rule_path_marks_rule_hit(self) -> None:
        _, trace = process("Merhaba")
        self.assertTrue(trace["rule_layer"]["hit"])
        self.assertFalse(trace["similarity"]["evaluated"])

    def test_similarity_path_records_topk(self) -> None:
        _, trace = process("genel ortalamama nereden bakarım", role="ogrenci", authenticated=True)
        self.assertTrue(trace["similarity"]["evaluated"])
        self.assertGreater(len(trace["similarity"]["top_k"]), 0)

    def test_fallback_path(self) -> None:
        _, trace = process("qwzx plkj mnbv")
        self.assertTrue(trace["decision"]["fallback"])
        self.assertEqual(trace["response_id"], "fallback_clarification")

    def test_latency_has_all_stages(self) -> None:
        _, trace = process("Merhaba")
        for stage in ["normalize", "rules", "similarity", "decide", "render", "total"]:
            self.assertIn(stage, trace["latency_ms"])
        self.assertGreaterEqual(trace["latency_ms"]["total"], 0.0)

    def test_no_alarms_on_normal_flow(self) -> None:
        _, trace = process("Karnemi göster", role="ogrenci", authenticated=True)
        self.assertEqual(trace["alarms"], [])

    def test_login_required_no_alarm(self) -> None:
        # Ziyaretçi karne isteyince gating uygulanmalı -> alarm YOK.
        _, trace = process("Karnemi göster", role="ziyaretci", authenticated=False)
        self.assertEqual(trace["decision"]["auth_action"], LOGIN_REQUIRED)
        self.assertEqual(trace["alarms"], [])


class AuthAlarmTests(unittest.TestCase):
    def test_detects_auth_leak(self) -> None:
        # auth gerektiren intent, oturum yok, ama gating uygulanmamış -> ALARM.
        leaky = Decision(
            intent="report_card_view",
            fallback=False,
            source="rule",
            confidence=1.0,
            auth_action=None,
        )
        alarms = check_auth_alarms(leaky, authenticated=False, role="ziyaretci")
        self.assertTrue(any("AUTH_LEAK" in a for a in alarms))

    def test_no_alarm_when_gated(self) -> None:
        gated = Decision(
            intent="report_card_view",
            fallback=False,
            source="rule",
            confidence=1.0,
            auth_action=LOGIN_REQUIRED,
        )
        self.assertEqual(check_auth_alarms(gated, authenticated=False, role="ziyaretci"), [])


class TraceJsonTests(unittest.TestCase):
    def test_valid_json_and_preserves_turkish(self) -> None:
        _, trace = process("Şifremi unuttum")
        text = trace_to_json(trace)
        parsed = json.loads(text)
        self.assertEqual(parsed["query_masked"], "Şifremi unuttum")  # PII yok -> aynen
        self.assertIn("Ş", text)  # ensure_ascii=False


if __name__ == "__main__":
    unittest.main()
