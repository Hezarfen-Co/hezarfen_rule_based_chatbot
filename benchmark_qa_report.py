"""Gerçek Engine çıktılarıyla benchmark soru-cevap Markdown raporu üretir.

Kullanım:
    python benchmark_qa_report.py
    python benchmark_qa_report.py --output BENCHMARK_SONUCLARI.md

Rapor, ``data/benchmark.jsonl`` içindeki her kaydı kullanıcıya hizmet veren tam
``Engine.handle`` akışından geçirir. PASS için yalnız intent yetmez; rol sonucu,
``response_id``, giriş eylemi, legacy rota, V2 route key/outcome/reason ve dolu
kullanıcı metni birlikte doğrulanır.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

from src.access import AccessOutcome
from src.catalog import route_for
from src.engine import Engine
from src.evaluation.benchmark import OOS_LABEL, load_benchmark
from src.role_spaces import get_role_space


DEFAULT_OUTPUT = Path(__file__).with_name("BENCHMARK_SONUCLARI.md")
ROLE_LABELS = {
    "ziyaretci": "Ziyaretçi",
    "veli": "Veli",
    "ogrenci": "Öğrenci",
    "ogretmen": "Öğretmen",
    "yonetici": "Yönetici",
    "admin": "ADMIN",
}

_UPPER_REPORT_REDIRECTS = {
    "report_card_view": "student_marks_lookup",
    "attendance_view": "student_attendance_lookup",
    "exam_finish_result": "student_marks_lookup",
}
_UPPER_ROLES = {"ogretmen", "yonetici", "admin"}


def _expected_contract(record: dict[str, Any]) -> dict[str, Any]:
    """Gold etiketini intent + rol/yanıt/rota sözleşmesine genişletir."""

    expected = record["expected_intent"]
    role = record.get("role", "ziyaretci")
    if expected == OOS_LABEL:
        outcome = str(record.get("expected_outcome") or "fallback")
        response_id = str(
            record.get("expected_response_id")
            or ("fallback_clarification" if outcome == "fallback" else "out_of_scope_action")
        )
        reason = str(
            record.get("expected_reason_code")
            or ("out_of_scope" if outcome == "fallback" else "scope_boundary_action")
        )
        return {
            "intent": OOS_LABEL,
            "outcome": outcome,
            "meta_action_id": None,
            "response_ids": [response_id],
            "reason_code": reason,
            "fallback": outcome == "fallback",
            "auth_action": None,
            "navigation_route": None,
            "meta_route_key": None,
        }

    view = get_role_space(role).view_for(expected)
    if view is None:
        # Bozuk/gelecekte eklenmiş bir test etiketi intent uyuşmazlığı olarak görünür;
        # olmayan katalog metadata'sını uydurmayız.
        return {"intent": expected}

    served_intent = expected
    redirected = _UPPER_REPORT_REDIRECTS.get(expected) if role in _UPPER_ROLES else None
    redirect_route: tuple[str, str] | None = None
    if redirected is not None:
        target_view = get_role_space(role).view_for(redirected)
        target_route = route_for(redirected)
        if (
            target_view is not None
            and target_view.outcome is AccessOutcome.ALLOW
            and target_route is not None
        ):
            view = target_view
            served_intent = redirected
            redirect_route = target_route

    denied = view.outcome is AccessOutcome.DENY
    response_ids = [view.response_id]
    navigation_route: str | None = None
    if redirect_route is not None:
        response_ids = ["student_report_redirect"]
        navigation_route = redirect_route[0]
    elif not denied:
        if expected in {"report_card_view", "attendance_view"} and role != "ogrenci":
            navigation_route = None
        else:
            target = route_for(expected)
            navigation_route = target[0] if target else None

    # Bölüm başlığı kısa devresi nav_overview'in kararlı, kabul edilen bir sunumudur.
    if expected == "nav_overview":
        response_ids.append("section_overview")

    return {
        "intent": expected,
        "outcome": view.outcome.value,
        "meta_action_id": served_intent,
        "response_ids": sorted(set(response_ids)),
        "reason_code": view.reason_code.value,
        "fallback": False,
        "auth_action": (
            "login_required" if denied and role == "ziyaretci"
            else "role_insufficient" if denied
            else None
        ),
        "navigation_route": navigation_route,
        "meta_route_key": view.route_key if not denied else None,
    }


def _contract_failures(
    expectation: dict[str, Any],
    response: dict[str, Any],
) -> list[str]:
    """Kullanıcıya görünen cevabı ve V2 metadata'yı ayrı ayrı doğrular."""

    actual_intent = response.get("intent") or OOS_LABEL
    failures: list[str] = []
    if actual_intent != expectation["intent"]:
        failures.append(f"intent: {expectation['intent']} != {actual_intent}")
    if "outcome" not in expectation:
        return failures

    response_id = response.get("response_id")
    if response_id not in expectation["response_ids"]:
        failures.append(
            "response_id: " + "/".join(expectation["response_ids"])
            + f" != {response_id}"
        )
    if bool(response.get("fallback")) != expectation["fallback"]:
        failures.append(
            f"fallback: {expectation['fallback']} != {bool(response.get('fallback'))}"
        )
    if response.get("auth_action") != expectation["auth_action"]:
        failures.append(
            f"auth_action: {expectation['auth_action']} != {response.get('auth_action')}"
        )

    navigation = response.get("navigation")
    actual_route = navigation.get("route") if isinstance(navigation, dict) else None
    if actual_route != expectation["navigation_route"]:
        failures.append(
            f"navigation.route: {expectation['navigation_route']} != {actual_route}"
        )
    if isinstance(navigation, dict) and navigation.get("available") is not True:
        failures.append("navigation.available true değil")

    meta = response.get("assistant_meta")
    if not isinstance(meta, dict):
        failures.append("assistant_meta eksik")
    else:
        if meta.get("outcome") != expectation["outcome"]:
            failures.append(
                f"assistant_meta.outcome: {expectation['outcome']} != {meta.get('outcome')}"
            )
        if meta.get("action_id") != expectation["meta_action_id"]:
            failures.append(
                "assistant_meta.action_id: "
                f"{expectation['meta_action_id']} != {meta.get('action_id')}"
            )
        if meta.get("reason_code") != expectation["reason_code"]:
            failures.append(
                "assistant_meta.reason_code: "
                f"{expectation['reason_code']} != {meta.get('reason_code')}"
            )
        meta_navigation = meta.get("navigation")
        actual_key = (
            meta_navigation.get("route_key") if isinstance(meta_navigation, dict) else None
        )
        if actual_key != expectation["meta_route_key"]:
            failures.append(
                f"assistant_meta.navigation: {expectation['meta_route_key']} != {actual_key}"
            )

    if not isinstance(response.get("text"), str) or not response.get("text", "").strip():
        failures.append("kullanıcı metni boş")
    return failures


def collect_results(
    records: Iterable[dict[str, Any]] | None = None,
    *,
    engine: Engine | None = None,
) -> list[dict[str, Any]]:
    """Benchmark kayıtlarını tam Engine akışında çalıştırıp karşılaştırır."""

    rows = list(load_benchmark() if records is None else records)
    runner = engine or Engine()
    results: list[dict[str, Any]] = []

    for index, record in enumerate(rows, start=1):
        role = record.get("role", "ziyaretci")
        response = runner.handle({
            "query": record["question"],
            "session": {
                "role": role,
                "authenticated": role != "ziyaretci",
            },
        })
        expected = record["expected_intent"]
        actual = response.get("intent") or OOS_LABEL
        expectation = _expected_contract(record)
        failure_reasons = _contract_failures(expectation, response)
        meta = response.get("assistant_meta") or {}
        results.append({
            "index": index,
            "question": record["question"],
            "role": role,
            "expected_intent": expected,
            "actual_intent": actual,
            "passed": not failure_reasons,
            "failure_reasons": failure_reasons,
            "expectation": expectation,
            "response_id": response.get("response_id"),
            "confidence": float(response.get("confidence") or 0.0),
            "fallback": bool(response.get("fallback")),
            "auth_action": response.get("auth_action"),
            "navigation": response.get("navigation"),
            "assistant_outcome": meta.get("outcome"),
            "assistant_reason_code": meta.get("reason_code"),
            "text": response.get("text") or "",
        })
    return results


def _table_text(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def _quote(text: str) -> str:
    lines = text.splitlines() or [""]
    return "\n".join("> " + line if line else ">" for line in lines)


def _inline_json(value: object) -> str:
    if value is None:
        return "None"
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def render_markdown(results: Iterable[dict[str, Any]]) -> str:
    """Toplu özet, hata listesi ve bütün soru-cevapları Markdown'a dönüştürür."""

    rows = list(results)
    passed = sum(bool(row["passed"]) for row in rows)
    failed = len(rows) - passed
    rate = passed / len(rows) if rows else 0.0
    by_role: dict[str, Counter[str]] = {}
    for row in rows:
        stats = by_role.setdefault(row["role"], Counter())
        stats["total"] += 1
        stats["passed" if row["passed"] else "failed"] += 1

    out = [
        "# Çelebi Benchmark Soru-Cevap Sonuçları",
        "",
        "Bu dosya `python benchmark_qa_report.py` komutuyla "
        "`data/benchmark.jsonl` üzerinden üretilir. Her soru, kullanıcının "
        "gördüğü tam `Engine.handle` akışında çalıştırılır. PASS; intent, rol "
        "sonucu, response kimliği ve iki yönlendirme sözleşmesinin tamamını kapsar.",
        "",
        "## Özet",
        "",
        f"- Toplam soru: **{len(rows)}**",
        f"- PASS: **{passed}**",
        f"- FAIL: **{failed}**",
        f"- Kullanıcı-akışı sözleşme başarısı: **{rate:.1%}**",
        "",
        "| Rol | Toplam | PASS | FAIL |",
        "|---|---:|---:|---:|",
    ]
    for role in ("ziyaretci", "veli", "ogrenci", "ogretmen", "yonetici", "admin"):
        stats = by_role.get(role)
        if not stats:
            continue
        out.append(
            f"| {ROLE_LABELS.get(role, role)} | {stats['total']} | "
            f"{stats['passed']} | {stats['failed']} |"
        )

    failures = [row for row in rows if not row["passed"]]
    out.extend(["", "## Hatalar", ""])
    if not failures:
        out.append("Tüm benchmark soruları beklenen intent ile sonuçlandı.")
    else:
        out.extend([
            "| # | Rol | Soru | Beklenen | Gerçek | Sözleşme hataları |",
            "|---:|---|---|---|---|---|",
        ])
        for row in failures:
            out.append(
                f"| {row['index']} | {ROLE_LABELS.get(row['role'], row['role'])} | "
                f"{_table_text(row['question'])} | `{row['expected_intent']}` | "
                f"`{row['actual_intent']}` | {_table_text('; '.join(row['failure_reasons']))} |"
            )

    out.extend(["", "## Tüm soru ve cevaplar", ""])
    for row in rows:
        status = "PASS" if row["passed"] else "FAIL"
        role_label = ROLE_LABELS.get(row["role"], row["role"])
        out.extend([
            f"### {row['index']:03d} · {status} · {role_label}",
            "",
            f"- Soru: {_table_text(row['question'])}",
            f"- Beklenen intent: `{row['expected_intent']}`",
            f"- Gerçek intent: `{row['actual_intent']}`",
            f"- response_id: `{row['response_id']}`",
            f"- confidence: `{row['confidence']:.4f}`",
            f"- fallback: `{str(row['fallback']).lower()}`",
            f"- auth_action: `{row['auth_action']}`",
            f"- navigation: `{_inline_json(row['navigation'])}`",
            f"- assistant outcome/reason: `{row['assistant_outcome']}` / "
            f"`{row['assistant_reason_code']}`",
            f"- Sözleşme: `{'PASS' if row['passed'] else '; '.join(row['failure_reasons'])}`",
            "",
            _quote(row["text"]),
            "",
        ])
    return "\n".join(out).rstrip() + "\n"


def write_report(output: Path = DEFAULT_OUTPUT) -> tuple[Path, list[dict[str, Any]]]:
    results = collect_results()
    output.write_text(render_markdown(results), encoding="utf-8")
    return output, results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output, results = write_report(args.output)
    failed = sum(not row["passed"] for row in results)
    print(f"{len(results)} soru -> {output} (FAIL={failed})")


if __name__ == "__main__":
    main()
