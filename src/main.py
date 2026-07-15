"""Container entry point and catalog validation."""

from __future__ import annotations

import argparse
from collections import Counter
from typing import Any

from .QandA import FALLBACK, INTENTS, MOCK_STUDENT, get_intent


REQUIRED_INTENT_FIELDS = {
    "intent",
    "category",
    "description",
    "response_id",
    "response_template",
    "auth_required",
    "example_questions",
    "must_not_match",
}


def _duplicates(values: list[str]) -> list[str]:
    """Return duplicate values in deterministic order."""

    counts = Counter(values)
    return sorted(value for value, count in counts.items() if count > 1)


def validate_catalog() -> dict[str, int]:
    """Validate invariants required by the future rule engine.

    Raises:
        ValueError: If catalog data is incomplete, ambiguous or inconsistent.
    """

    if not INTENTS:
        raise ValueError("Intent kataloğu boş olamaz.")

    errors: list[str] = []
    intent_names: list[str] = []
    response_ids: list[str] = []
    questions: list[str] = []

    for index, item in enumerate(INTENTS):
        missing_fields = REQUIRED_INTENT_FIELDS.difference(item)
        if missing_fields:
            errors.append(
                f"INTENTS[{index}] eksik alanlar: {', '.join(sorted(missing_fields))}"
            )
            continue

        intent_name = item["intent"]
        intent_names.append(intent_name)
        response_ids.append(item["response_id"])

        examples = item["example_questions"]
        if not examples:
            errors.append(f"{intent_name}: en az bir örnek soru gerekli.")
        if any(not isinstance(question, str) or not question.strip() for question in examples):
            errors.append(f"{intent_name}: boş veya metin olmayan örnek soru var.")
        questions.extend(examples)

    duplicate_intents = _duplicates(intent_names)
    duplicate_responses = _duplicates(response_ids)
    duplicate_questions = _duplicates(questions)
    known_intents = set(intent_names)

    if duplicate_intents:
        errors.append(f"Tekrarlanan intent: {duplicate_intents}")
    if duplicate_responses:
        errors.append(f"Tekrarlanan response_id: {duplicate_responses}")
    if duplicate_questions:
        errors.append(f"Tekrarlanan örnek soru: {duplicate_questions}")

    for item in INTENTS:
        unknown_targets = set(item.get("must_not_match", [])).difference(known_intents)
        if unknown_targets:
            errors.append(
                f"{item.get('intent', '<unknown>')}: bilinmeyen must_not_match "
                f"hedefleri: {sorted(unknown_targets)}"
            )

    if not FALLBACK.get("response_id") or not FALLBACK.get("response_template"):
        errors.append("Fallback cevabı eksik.")
    if not MOCK_STUDENT.get("student_id"):
        errors.append("Mock öğrenci kimliği eksik.")

    if errors:
        raise ValueError("Katalog doğrulanamadı:\n- " + "\n- ".join(errors))

    return {
        "intent_count": len(intent_names),
        "response_count": len(response_ids),
        "example_question_count": len(questions),
    }


def print_validation_result(result: dict[str, Any]) -> None:
    """Print a concise, log-friendly validation result."""

    print("Katalog doğrulandı.")
    print(f"Intent: {result['intent_count']}")
    print(f"Cevap: {result['response_count']}")
    print(f"Örnek soru: {result['example_question_count']}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Eğitim platformu chatbot'u")
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Soru/cevap kataloğunu doğrular ve çıkar.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.validate:
        print_validation_result(validate_catalog())
        return 0

    # Motor eklenene kadar çıplak çalıştırma da güvenli bir doğrulama yapar.
    print_validation_result(validate_catalog())
    print("Chatbot motoru henüz eklenmedi.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
