"""Aşama 3 birim testleri: benchmark yükleme ve doğrulama."""

import json
import tempfile
import unittest
from pathlib import Path

from src import catalog
from src.evaluation.benchmark import (
    OOS_LABEL,
    load_benchmark,
    validate_benchmark,
)


def _known_intents() -> set[str]:
    return {item["intent"] for item in catalog.INTENTS}


def _example_questions() -> set[str]:
    return {
        q.strip().casefold()
        for item in catalog.INTENTS
        for q in item["example_questions"]
    }


class LoadBenchmarkTests(unittest.TestCase):
    def test_loads_default_benchmark(self) -> None:
        records = load_benchmark()
        self.assertGreater(len(records), 0)
        self.assertIn("question", records[0])
        self.assertIn("expected_intent", records[0])

    def test_missing_file_raises(self) -> None:
        with self.assertRaises(FileNotFoundError):
            load_benchmark(Path("yok_boyle_bir_dosya.jsonl"))

    def test_blank_lines_skipped(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "b.jsonl"
            path.write_text(
                '{"question": "a", "expected_intent": "oos"}\n\n'
                '{"question": "b", "expected_intent": "oos"}\n',
                encoding="utf-8",
            )
            self.assertEqual(len(load_benchmark(path)), 2)

    def test_invalid_json_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "b.jsonl"
            path.write_text("{bozuk json}\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_benchmark(path)

    def test_missing_field_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "b.jsonl"
            path.write_text('{"question": "a"}\n', encoding="utf-8")
            with self.assertRaises(ValueError):
                load_benchmark(path)


class ValidateBenchmarkTests(unittest.TestCase):
    def test_real_benchmark_is_valid(self) -> None:
        records = load_benchmark()
        result = validate_benchmark(
            records,
            known_intents=_known_intents(),
            known_roles=set(catalog.ROLE_HIERARCHY),
            example_questions=_example_questions(),
        )
        self.assertGreater(result["total"], 0)
        self.assertGreater(result["oos"], 0)
        self.assertGreater(result["in_scope"], 0)

    def test_real_benchmark_has_no_overlap_with_examples(self) -> None:
        # Örtüşme varsa validate_benchmark ValueError atar; burada net doğrula.
        records = load_benchmark()
        examples = _example_questions()
        overlap = [
            r["question"]
            for r in records
            if r["question"].strip().casefold() in examples
        ]
        self.assertEqual(overlap, [], f"Örtüşen sorular: {overlap}")

    def test_every_intent_has_at_least_one_benchmark_question(self) -> None:
        records = load_benchmark()
        covered = {r["expected_intent"] for r in records if r["expected_intent"] != OOS_LABEL}
        missing = _known_intents().difference(covered)
        self.assertEqual(missing, set(), f"Benchmark'ta karşılığı olmayan intent: {missing}")

    def test_detects_unknown_intent(self) -> None:
        records = [{"question": "x", "expected_intent": "yok_intent"}]
        with self.assertRaises(ValueError):
            validate_benchmark(records, known_intents=_known_intents())

    def test_detects_duplicate_question(self) -> None:
        records = [
            {"question": "aynı", "expected_intent": "oos"},
            {"question": "Aynı", "expected_intent": "oos"},
        ]
        with self.assertRaises(ValueError):
            validate_benchmark(records, known_intents=_known_intents())

    def test_detects_overlap_with_examples(self) -> None:
        sample_example = catalog.INTENTS[0]["example_questions"][0]
        records = [
            {"question": sample_example, "expected_intent": catalog.INTENTS[0]["intent"]},
            {"question": "kapsam disi soru", "expected_intent": "oos"},
        ]
        with self.assertRaises(ValueError):
            validate_benchmark(
                records,
                known_intents=_known_intents(),
                example_questions=_example_questions(),
            )

    def test_requires_at_least_one_oos(self) -> None:
        records = [{"question": "x", "expected_intent": catalog.INTENTS[0]["intent"]}]
        with self.assertRaises(ValueError):
            validate_benchmark(records, known_intents=_known_intents())

    def test_detects_unknown_role(self) -> None:
        records = [
            {"question": "x", "expected_intent": "oos", "role": "kral"},
        ]
        with self.assertRaises(ValueError):
            validate_benchmark(
                records,
                known_intents=_known_intents(),
                known_roles=set(catalog.ROLE_HIERARCHY),
            )


if __name__ == "__main__":
    unittest.main()
