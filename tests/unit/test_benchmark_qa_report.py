"""Benchmark soru-cevap Markdown üreticisi testleri."""

import unittest

from benchmark_qa_report import collect_results, render_markdown


class _FakeEngine:
    def handle(self, payload: dict) -> dict:
        if payload["query"] == "doğru":
            intent = "greeting"
            text = "Merhaba"
            response_id = "welcome_message"
            fallback = False
            outcome = "allow"
            reason_code = "allowed"
        else:
            intent = None
            text = "Bunu yanıtlayamam."
            response_id = "fallback_clarification"
            fallback = True
            outcome = "fallback"
            reason_code = "out_of_scope"
        return {
            "intent": intent,
            "response_id": response_id,
            "confidence": 0.75,
            "fallback": fallback,
            "auth_action": None,
            "navigation": None,
            "assistant_meta": {
                "outcome": outcome,
                "action_id": intent,
                "reason_code": reason_code,
                "navigation": None,
            },
            "text": text,
        }


class BenchmarkQaReportTests(unittest.TestCase):
    def test_collects_pass_and_oos_from_full_response(self) -> None:
        records = [
            {"question": "doğru", "expected_intent": "greeting", "role": "ziyaretci"},
            {"question": "kapsam dışı", "expected_intent": "oos", "role": "ogrenci"},
        ]
        rows = collect_results(records, engine=_FakeEngine())
        self.assertEqual(len(rows), 2)
        self.assertTrue(all(row["passed"] for row in rows))
        self.assertEqual(rows[1]["actual_intent"], "oos")

    def test_markdown_contains_summary_metadata_and_every_answer(self) -> None:
        rows = collect_results(
            [{"question": "doğru", "expected_intent": "wrong", "role": "ziyaretci"}],
            engine=_FakeEngine(),
        )
        markdown = render_markdown(rows)
        self.assertIn("FAIL: **1**", markdown)
        self.assertIn("Beklenen intent: `wrong`", markdown)
        self.assertIn("Gerçek intent: `greeting`", markdown)
        self.assertIn("response_id: `welcome_message`", markdown)
        self.assertIn("navigation: `None`", markdown)
        self.assertIn("> Merhaba", markdown)


if __name__ == "__main__":
    unittest.main()
