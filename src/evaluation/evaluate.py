"""Tam değerlendirme koşum aracı (Aşama 10).

Benchmark'ı izlenmiş boru hattından geçirir ve tek bir raporda toplar:
- macro-F1 (başlık), accuracy, per-class P/R/F1
- coverage, accuracy-on-covered, false-fallback
- OOS recall
- must_not_match çift-karışma raporu
- top-1 vs top-3 accuracy
- latency p50/p95

Çıktı hem makine-okunur (dict) hem insan-okunur (format_report) — regresyon için
Aşama 14, ayar için Aşama 11 bunu kullanır.
"""

from __future__ import annotations

from typing import Any

from .benchmark import OOS_LABEL, load_benchmark
from ..catalog import INTENTS
from ..decision import DEFAULT_THRESHOLD, _is_confusable_pair
from .metrics import (
    accuracy,
    macro_f1,
    per_class_scores,
    percentile,
    topk_accuracy,
)
from ..observability import process
from ..similarity import SimilarityMatcher, get_default_matcher

# in-scope iken FALLBACK'e düşeni işaretlemek için sözde etiket.
_FALLBACK_LABEL = "__fallback__"


def run_evaluation(
    threshold: float = DEFAULT_THRESHOLD,
    matcher: SimilarityMatcher | None = None,
    records: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Benchmark üzerinde tam değerlendirme yapar ve metrik sözlüğü döndürür."""

    matcher = matcher or get_default_matcher()
    records = records if records is not None else load_benchmark()
    labels = {i["intent"] for i in INTENTS}

    in_pairs: list[tuple[str, str]] = []          # (true, pred|__fallback__)
    covered_pairs: list[tuple[str, str]] = []      # yalnızca kapsananlar
    topk_records: list[tuple[str, list[str]]] = [] # (true, sıralı tahminler)
    latencies: list[float] = []

    covered = correct = false_fallback = 0
    oos_total = oos_caught = 0
    confusable_wrong = nonconfusable_wrong = 0
    wrong_pairs: list[tuple[str, str]] = []

    for r in records:
        role = r.get("role", "ziyaretci")
        authenticated = role != "ziyaretci"
        _, trace = process(
            r["question"], role=role, authenticated=authenticated, matcher=matcher
        )
        # Eşik parametresini uygulamak için kararı yeniden değerlendirmek yerine,
        # process varsayılan eşiği kullanır; ayar taraması için threshold enjekte edelim.
        # (threshold != default ise skorlardan yeniden karar ver.)
        pred = _reconsider(trace, threshold)
        latencies.append(trace["latency_ms"]["total"])

        expected = r["expected_intent"]
        if expected == OOS_LABEL:
            oos_total += 1
            if pred is None:
                oos_caught += 1
            continue

        # in-scope
        ranked_intents = _ranked_intents(trace)
        topk_records.append((expected, ranked_intents))

        if pred is None:
            false_fallback += 1
            in_pairs.append((expected, _FALLBACK_LABEL))
        else:
            covered += 1
            in_pairs.append((expected, pred))
            covered_pairs.append((expected, pred))
            if pred == expected:
                correct += 1
            else:
                wrong_pairs.append((expected, pred))
                if _is_confusable_pair(expected, pred):
                    confusable_wrong += 1
                else:
                    nonconfusable_wrong += 1

    in_scope_total = len(in_pairs)
    report: dict[str, Any] = {
        "threshold": threshold,
        "in_scope_total": in_scope_total,
        "oos_total": oos_total,
        "macro_f1": macro_f1(in_pairs, labels),
        "accuracy": accuracy(in_pairs),
        "coverage": covered / in_scope_total if in_scope_total else 0.0,
        "accuracy_on_covered": correct / covered if covered else 0.0,
        "false_fallback": false_fallback,
        "oos_recall": oos_caught / oos_total if oos_total else 0.0,
        "top1_accuracy": topk_accuracy(topk_records, 1),
        "top3_accuracy": topk_accuracy(topk_records, 3),
        "confusable_wrong": confusable_wrong,
        "nonconfusable_wrong": nonconfusable_wrong,
        "wrong_pairs": wrong_pairs,
        "latency_p50_ms": percentile(latencies, 50),
        "latency_p95_ms": percentile(latencies, 95),
        "per_class": per_class_scores(covered_pairs, labels),
    }
    return report


def _ranked_intents(trace: dict[str, Any]) -> list[str]:
    """Trace'ten sıralı tahmin listesi (kural yolu -> tek eleman)."""

    if trace["rule_layer"]["hit"]:
        return [trace["rule_layer"]["intent"]]
    return [item["intent"] for item in trace["similarity"]["top_k"]]


def _reconsider(trace: dict[str, Any], threshold: float) -> str | None:
    """Verilen eşiğe göre tahmini belirler (kural her zaman kazanır; alan kapısı uygulanır)."""

    if trace["rule_layer"]["hit"]:
        return trace["rule_layer"]["intent"]
    if not trace["similarity"].get("in_domain", True):
        return None
    top_k = trace["similarity"]["top_k"]
    if not top_k:
        return None
    top = top_k[0]
    if top["score"] < threshold:
        return None
    return top["intent"]


def format_report(report: dict[str, Any]) -> str:
    """İnsan-okunur özet."""

    lines = [
        "================ DEĞERLENDİRME RAPORU ================",
        f"Eşik (threshold)      : {report['threshold']:.3f}",
        f"In-scope / OOS        : {report['in_scope_total']} / {report['oos_total']}",
        "--- Genel ---",
        f"Macro-F1 (BAŞLIK)     : {report['macro_f1']:.3f}",
        f"Accuracy              : {report['accuracy']:.1%}",
        f"Top-1 / Top-3 acc     : {report['top1_accuracy']:.1%} / {report['top3_accuracy']:.1%}",
        "--- Abstention (eşik) ---",
        f"Coverage              : {report['coverage']:.1%}",
        f"Accuracy-on-covered   : {report['accuracy_on_covered']:.1%}",
        f"False fallback        : {report['false_fallback']}",
        f"OOS recall            : {report['oos_recall']:.1%}",
        "--- must_not_match ---",
        f"Karışan çift (confusable) yanlış : {report['confusable_wrong']}",
        f"Diğer (beklenmedik) yanlış       : {report['nonconfusable_wrong']}",
        "--- Latency ---",
        f"p50 / p95 (ms)        : {report['latency_p50_ms']:.3f} / {report['latency_p95_ms']:.3f}",
        "--- En zayıf 8 intent (F1, kapsananlarda) ---",
    ]
    worst = sorted(report["per_class"], key=lambda s: (s.f1, -s.support))
    for s in worst[:8]:
        lines.append(
            f"  {s.label:26s} P={s.precision:.2f} R={s.recall:.2f} F1={s.f1:.2f} (n={s.support})"
        )
    if report["wrong_pairs"]:
        lines.append("--- Yanlış tahminler (beklenen -> bulunan) ---")
        for true, pred in report["wrong_pairs"]:
            mark = "~" if _is_confusable_pair(true, pred) else "x"
            lines.append(f"  [{mark}] {true} -> {pred}")
    lines.append("=====================================================")
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_report(run_evaluation()))
