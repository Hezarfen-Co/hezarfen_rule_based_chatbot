"""Benchmark (değerlendirme) setinin yüklenmesi ve doğrulanması.

Benchmark, motorun DÜRÜST ölçülmesi için `example_questions`'tan AYRI tutulan
etiketli sorulardır. Her kayıt:
    {"question": str, "expected_intent": str | "oos", "role": str?}

`expected_intent == "oos"` -> kapsam dışı; motor bunları FALLBACK'e atmalıdır.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Final


OOS_LABEL: Final[str] = "oos"

# Depo kökü: src/benchmark.py -> parents[1] = proje kökü.
DEFAULT_BENCHMARK_PATH: Final[Path] = (
    Path(__file__).resolve().parents[1] / "data" / "benchmark.jsonl"
)


def load_benchmark(path: str | Path | None = None) -> list[dict[str, Any]]:
    """Benchmark kayıtlarını JSONL dosyasından yükler.

    Boş satırlar atlanır. Her satır 'question' ve 'expected_intent' içermelidir.

    Raises:
        FileNotFoundError: Dosya yoksa.
        ValueError: Bir satır bozuksa veya zorunlu alan eksikse.
    """

    benchmark_path = Path(path) if path is not None else DEFAULT_BENCHMARK_PATH
    if not benchmark_path.exists():
        raise FileNotFoundError(f"Benchmark dosyası bulunamadı: {benchmark_path}")

    records: list[dict[str, Any]] = []
    with benchmark_path.open("r", encoding="utf-8") as handle:
        for line_no, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Benchmark satırı {line_no} geçersiz JSON: {exc}") from exc
            if "question" not in record or "expected_intent" not in record:
                raise ValueError(
                    f"Benchmark satırı {line_no}: 'question' ve 'expected_intent' zorunlu."
                )
            records.append(record)
    return records


def validate_benchmark(
    records: list[dict[str, Any]],
    known_intents: set[str],
    known_roles: set[str] | None = None,
    example_questions: set[str] | None = None,
) -> dict[str, int]:
    """Benchmark kayıtlarının tutarlılığını doğrular.

    Kontroller:
        - question boş olmayan metin.
        - expected_intent ya bilinen bir intent ya da OOS_LABEL.
        - (verilirse) role bilinen bir rol.
        - benchmark içinde tekrarlanan soru yok.
        - (verilirse) hiçbir soru example_questions ile örtüşmez.
        - en az bir OOS kaydı bulunur.

    Returns:
        Sayımlar: total, in_scope, oos, intents_covered.

    Raises:
        ValueError: Herhangi bir kontrol başarısızsa.
    """

    errors: list[str] = []
    if not records:
        raise ValueError("Benchmark boş olamaz.")

    seen_questions: set[str] = set()
    covered: set[str] = set()
    oos_count = 0

    for index, record in enumerate(records):
        question = record.get("question")
        expected = record.get("expected_intent")
        role = record.get("role")

        if not isinstance(question, str) or not question.strip():
            errors.append(f"[{index}] boş/metin olmayan question.")
            continue

        norm_q = question.strip().casefold()
        if norm_q in seen_questions:
            errors.append(f"[{index}] tekrarlanan soru: {question!r}")
        seen_questions.add(norm_q)

        if expected == OOS_LABEL:
            oos_count += 1
        elif expected in known_intents:
            covered.add(expected)
        else:
            errors.append(f"[{index}] bilinmeyen expected_intent: {expected!r}")

        if role is not None and known_roles is not None and role not in known_roles:
            errors.append(f"[{index}] bilinmeyen rol: {role!r}")

        if example_questions is not None and norm_q in example_questions:
            errors.append(
                f"[{index}] soru example_questions ile örtüşüyor (benchmark ayrı olmalı): {question!r}"
            )

    if oos_count == 0:
        errors.append("En az bir OOS (kapsam dışı) kaydı gerekli.")

    if errors:
        raise ValueError("Benchmark doğrulanamadı:\n- " + "\n- ".join(errors))

    return {
        "total": len(records),
        "in_scope": len(records) - oos_count,
        "oos": oos_count,
        "intents_covered": len(covered),
    }
