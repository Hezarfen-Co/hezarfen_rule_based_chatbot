"""Değerlendirme paketi: benchmark yükleme, metrikler ve tam değerlendirme raporu.

Alt-modüller:
    benchmark  — benchmark.jsonl yükleme/doğrulama
    metrics    — precision/recall/F1, accuracy, top-k, percentile
    evaluate   — uçtan uca değerlendirme koşusu + rapor biçimleme
"""

from __future__ import annotations

from .benchmark import OOS_LABEL, load_benchmark, validate_benchmark
from .evaluate import format_report, run_evaluation

__all__ = [
    "OOS_LABEL",
    "load_benchmark",
    "validate_benchmark",
    "format_report",
    "run_evaluation",
]
