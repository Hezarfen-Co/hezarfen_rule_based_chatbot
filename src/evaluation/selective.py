"""Seçici sınıflandırma (selective classification / abstention) metrikleri.

Ana ilke: "her soruyu cevaplamak" değil, "cevap verdiğinde çok yüksek olasılıkla
doğru olmak" (Geifman & El-Yaniv). Bu modül tek-eşik yerine RİSK–KAPSAMA eğrisi
çıkarır ve şu ürünleri üretir:

- Risk–coverage eğrisi + AURC (düşük = daha iyi): kapsananlar arasında hata oranı.
- İşletim noktası (DEFAULT_THRESHOLD=0.18) için seçici risk + kapsama.
- OOS false-accept (kapsam-dışı ama cevaplanan) + near/far-OOS ayrımı.
- "Rule of three": sıfır-hatalı n test için gerçek hata oranının ~%95 üst sınırı 3/n.

Çalıştırma: ``python -m src.evaluation.selective`` (markdown rapor stdout'a).
Kesinlikle deterministik: motoru (process) her örnek için bir kez çağırır.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..decision import DEFAULT_THRESHOLD
from ..engine import Engine
from ..observability import process
from ..similarity import SimilarityMatcher
from .benchmark import OOS_LABEL, load_benchmark
from .evaluate import get_default_matcher


# Ek near-OOS seti (in-scope'a BENZEYEN kapsam-dışı; domain-gate'i geçebilir ama motor
# ask-zone/manipülasyon/topic guard ile abstain etmeli). Karar-katmanı benchmark'ından
# AYRI tutulur (evaluate.py karar katmanını ölçer; bunlar engine-katmanı testidir).
_NEAR_OOS_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "near_oos.jsonl"


def load_near_oos() -> list[dict[str, Any]]:
    if not _NEAR_OOS_PATH.exists():
        return []
    out: list[dict[str, Any]] = []
    for line in _NEAR_OOS_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


# near-OOS eşiği: benzerlik top-1 skoru bu değerin ÜSTÜNDEyse OOS örneği "desteklenen
# konuya benziyor" (near-OOS) sayılır; altındaysa far-OOS (tamamen ilgisiz). Alan
# kapısı eşiğiyle hizalı (domain-gate DEFAULT_THRESHOLD).
_NEAR_OOS_SCORE: float = DEFAULT_THRESHOLD


def _top1(trace: dict[str, Any]) -> tuple[str | None, float]:
    """(top-1 intent, güven). Kural yolu -> güven 1.0; aksi halde benzerlik top-1."""

    if trace["rule_layer"]["hit"]:
        return trace["rule_layer"]["intent"], 1.0
    top_k = trace["similarity"].get("top_k") or []
    if not top_k:
        return None, 0.0
    return top_k[0]["intent"], float(top_k[0]["score"])


def collect_samples(
    matcher: SimilarityMatcher | None = None,
    records: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Her örnek için hem MODEL top-1'i (eğri için) hem GERÇEK motor kararını toplar.

    - Eğri/AURC: modelin içsel ayrışması -> trace top-1 (conf, doğru mu).
    - İşletim noktası: motorun GERÇEK kullanıcı-görünür kararı (ask-zone/clarify dahil).
      'accepted' = motor somut bir intent döndürdü (clarify/fallback DEĞİL). Böylece
      belirsizde netleşen (asla-yanlış) bir sorgu 'kabul' sayılmaz -> metrik gerçekçi.
    """

    matcher = matcher or get_default_matcher()
    records = records if records is not None else (load_benchmark() + load_near_oos())
    engine = Engine()

    in_scope: list[dict[str, Any]] = []
    oos: list[dict[str, Any]] = []

    for r in records:
        role = r.get("role", "ziyaretci")
        authenticated = role != "ziyaretci"
        _, trace = process(
            r["question"], role=role, authenticated=authenticated, matcher=matcher
        )
        top1, conf = _top1(trace)
        resp = engine.handle({
            "query": r["question"],
            "session": {"role": role, "authenticated": authenticated},
        })
        answered = resp["intent"] is not None  # clarify/fallback -> None
        expected = r["expected_intent"]

        if expected == OOS_LABEL:
            oos.append({"conf": conf, "accepted": answered})
        else:
            in_scope.append({
                "conf": conf,
                "correct": top1 == expected,          # eğri: model top-1 doğruluğu
                "answered": answered,                  # işletim: motor somut cevap verdi mi
                "answer_correct": answered and resp["intent"] == expected,
            })

    return {"in_scope": in_scope, "oos": oos}


def risk_coverage_curve(in_scope: list[dict[str, Any]]) -> list[tuple[float, float]]:
    """(coverage, selective_risk) noktaları: güvene göre azalan sırayla kümülatif.

    coverage = cevaplanan / toplam; risk = cevaplananlar arasında hata oranı.
    """

    ranked = sorted(in_scope, key=lambda s: s["conf"], reverse=True)
    n = len(ranked)
    points: list[tuple[float, float]] = []
    errors = 0
    for k, sample in enumerate(ranked, start=1):
        if not sample["correct"]:
            errors += 1
        points.append((k / n, errors / k))
    return points


def aurc(points: list[tuple[float, float]]) -> float:
    """Risk–coverage eğrisi altındaki alan (kapsamaya göre ortalama risk)."""

    if not points:
        return 0.0
    return sum(risk for _cov, risk in points) / len(points)


def compute(
    matcher: SimilarityMatcher | None = None,
    records: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    samples = collect_samples(matcher, records)
    in_scope = samples["in_scope"]
    oos = samples["oos"]

    curve = risk_coverage_curve(in_scope)

    # İşletim noktası: motorun GERÇEK kararı (ask-zone/clarify dahil). 'answered' =
    # somut intent döndü; 'answer_correct' = döndü ve doğru. Belirsizde netleşenler
    # cevap sayılmaz (asla-yanlış -> risk'i şişirmez, coverage'a girmez).
    answered = [s for s in in_scope if s["answered"]]
    answered_wrong = sum(1 for s in answered if not s["answer_correct"])
    op_coverage = len(answered) / len(in_scope) if in_scope else 0.0
    op_risk = answered_wrong / len(answered) if answered else 0.0

    # OOS false-accept (genel + near/far).
    def _fa(bucket: list[dict[str, Any]]) -> tuple[int, int]:
        accepted = sum(1 for s in bucket if s["accepted"])
        return accepted, len(bucket)

    near = [s for s in oos if s["conf"] >= _NEAR_OOS_SCORE]
    far = [s for s in oos if s["conf"] < _NEAR_OOS_SCORE]
    fa_all, n_all = _fa(oos)
    fa_near, n_near = _fa(near)
    fa_far, n_far = _fa(far)

    return {
        "n_in_scope": len(in_scope),
        "n_oos": len(oos),
        "aurc": aurc(curve),
        "op_threshold": DEFAULT_THRESHOLD,
        "op_coverage": op_coverage,
        "op_selective_risk": op_risk,
        "op_answered": len(answered),
        "op_answered_wrong": answered_wrong,
        "oos_false_accept": fa_all / n_all if n_all else 0.0,
        "oos_fa_count": (fa_all, n_all),
        "oos_fa_near": (fa_near, n_near),
        "oos_fa_far": (fa_far, n_far),
        "curve": curve,
    }


def _rule_of_three(errors: int, n: int) -> str:
    """Sıfır-hatalı n için ~%95 üst sınır 3/n; hata varsa gözlenen oranı ver."""

    if n == 0:
        return "n=0"
    if errors == 0:
        if n < 30:
            return f"0 gözlendi (n={n} — güven aralığı için örnek küçük)"
        return f"≤ {3.0 / n:.2%} (rule-of-three, n={n})"
    return f"{errors / n:.2%} gözlendi ({errors}/{n})"


def format_report(report: dict[str, Any]) -> str:
    fa_near_c, fa_near_n = report["oos_fa_near"]
    fa_far_c, fa_far_n = report["oos_fa_far"]
    aw, an = report["op_answered_wrong"], report["op_answered"]
    lines = [
        "========= SEÇİCİ SINIFLANDIRMA (SELECTIVE RISK) =========",
        f"In-scope / OOS örnek     : {report['n_in_scope']} / {report['n_oos']}",
        "--- Risk–Coverage ---",
        f"AURC (düşük=iyi)         : {report['aurc']:.4f}",
        f"İşletim eşiği            : {report['op_threshold']:.3f}",
        f"  Kapsama (coverage)     : {report['op_coverage']:.1%}",
        f"  Seçici risk            : {report['op_selective_risk']:.2%} ({aw}/{an} yanlış)",
        f"  Kabul-doğruluk üst sın.: {_rule_of_three(aw, an)}",
        "--- OOS false-accept (kapsam-dışı ama cevaplanan) ---",
        f"  Genel                  : {report['oos_false_accept']:.2%} "
        f"({report['oos_fa_count'][0]}/{report['oos_fa_count'][1]})",
        f"  near-OOS (benzeyen)    : {_rule_of_three(fa_near_c, fa_near_n)}",
        f"  far-OOS (ilgisiz)      : {_rule_of_three(fa_far_c, fa_far_n)}",
        "--- Risk–coverage eğrisi (örnek noktalar) ---",
    ]
    curve = report["curve"]
    for frac in (0.5, 0.7, 0.8, 0.9, 0.95, 1.0):
        idx = min(len(curve) - 1, int(frac * len(curve)) - 1)
        if idx >= 0:
            cov, risk = curve[idx]
            lines.append(f"  coverage≈{cov:>5.0%}  ->  risk={risk:.2%}")
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_report(compute()))
