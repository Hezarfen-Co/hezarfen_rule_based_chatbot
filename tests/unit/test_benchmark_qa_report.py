"""Tam Engine benchmark koşucusunun JSON/Markdown çıktı testleri."""

import json
import tempfile
import unittest
from pathlib import Path

from benchmark_qa_report import (
    RESULT_SCHEMA_VERSION,
    build_json_report,
    collect_results,
    render_markdown,
    write_reports,
)


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
            "trace_id": payload["trace_id"],
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
        self.assertEqual(rows[0]["trace_id"], "benchmark-0001")
        self.assertEqual(rows[0]["response"]["text"], "Merhaba")

    def test_combined_json_has_overall_and_role_summaries(self) -> None:
        records = [
            {"question": "doğru", "expected_intent": "greeting", "role": "ziyaretci"},
            {"question": "kapsam dışı", "expected_intent": "oos", "role": "ogrenci"},
        ]
        rows = collect_results(records, engine=_FakeEngine())
        report = build_json_report(rows)

        self.assertEqual(report["schema_version"], RESULT_SCHEMA_VERSION)
        self.assertEqual(report["source"], "data/benchmark.jsonl")
        self.assertEqual(report["summary"]["total"], 2)
        self.assertEqual(report["summary"]["passed"], 2)
        self.assertEqual(report["summary"]["failed"], 0)
        self.assertEqual(report["summary"]["by_role"]["ziyaretci"]["total"], 1)
        self.assertEqual(report["summary"]["by_role"]["ogrenci"]["total"], 1)
        self.assertEqual(report["results"][1]["question"], records[1]["question"])
        self.assertEqual(report["results"][1]["role"], records[1]["role"])
        self.assertEqual(report["results"][1]["expected_intent"], "oos")
        self.assertEqual(report["results"][1]["expected_contract"]["outcome"], "fallback")

    def test_writes_one_json_and_optional_markdown_from_same_run(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "benchmark.jsonl"
            source.write_text(
                json.dumps(
                    {
                        "question": "doğru",
                        "expected_intent": "greeting",
                        "role": "ziyaretci",
                    },
                    ensure_ascii=False,
                )
                + "\n",
                encoding="utf-8",
            )
            json_output = root / "results.json"
            markdown_output = root / "report.md"

            _, _, rows = write_reports(
                benchmark_path=source,
                json_output=json_output,
                markdown_output=markdown_output,
                engine=_FakeEngine(),
            )

            report = json.loads(json_output.read_text(encoding="utf-8"))
            self.assertEqual(len(rows), 1)
            self.assertEqual(report["summary"]["total"], 1)
            self.assertEqual(report["results"][0]["response"]["trace_id"], "benchmark-0001")
            self.assertIn("### 001 · PASS", markdown_output.read_text(encoding="utf-8"))

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
