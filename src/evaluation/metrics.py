"""Sınıflandırma metrikleri (çekirdek).

Bu modül temel metrikleri sağlar: per-class precision/recall/F1, macro-F1,
accuracy ve confusion sayımları. Aşama 10'da coverage, OOS recall, PR eğrisi ve
gecikme (latency) ölçümleriyle genişletilecektir.

Girdi her yerde `pairs`: (gerçek_etiket, tahmin_etiket) çiftlerinin listesi.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class ClassScore:
    label: str
    precision: float
    recall: float
    f1: float
    support: int


def _prf(tp: int, fp: int, fn: int) -> tuple[float, float, float]:
    """tp/fp/fn'den precision, recall, F1 (harmonik ortalama) döndürür."""

    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    return precision, recall, f1


def confusion_counts(
    pairs: list[tuple[str, str]], labels: set[str]
) -> dict[str, tuple[int, int, int]]:
    """Her etiket için (tp, fp, fn) döndürür."""

    tp: Counter[str] = Counter()
    fp: Counter[str] = Counter()
    fn: Counter[str] = Counter()
    for true_label, pred_label in pairs:
        if true_label == pred_label:
            tp[true_label] += 1
        else:
            fp[pred_label] += 1
            fn[true_label] += 1
    return {label: (tp[label], fp[label], fn[label]) for label in labels}


def per_class_scores(pairs: list[tuple[str, str]], labels: set[str]) -> list[ClassScore]:
    """Her etiket için ClassScore listesi (support'a göre azalan)."""

    support: Counter[str] = Counter(true for true, _ in pairs)
    counts = confusion_counts(pairs, labels)
    scores: list[ClassScore] = []
    for label in labels:
        tp, fp, fn = counts[label]
        precision, recall, f1 = _prf(tp, fp, fn)
        scores.append(ClassScore(label, precision, recall, f1, support[label]))
    scores.sort(key=lambda s: (s.support, s.label), reverse=True)
    return scores


def macro_f1(pairs: list[tuple[str, str]], labels: set[str]) -> float:
    """Etiketler arası düz ortalama F1.

    Dengesiz sınıfta nadir ama kritik intent'lerin bozukluğunu saklamaz; bu yüzden
    başlık metriği olarak kullanılır.
    """

    if not labels:
        return 0.0
    counts = confusion_counts(pairs, labels)
    total = 0.0
    for label in labels:
        tp, fp, fn = counts[label]
        total += _prf(tp, fp, fn)[2]
    return total / len(labels)


def accuracy(pairs: list[tuple[str, str]]) -> float:
    """Doğru tahmin oranı (ikincil metrik; dengesizlikte yanıltıcı olabilir)."""

    if not pairs:
        return 0.0
    correct = sum(1 for true, pred in pairs if true == pred)
    return correct / len(pairs)


def percentile(values: list[float], p: float) -> float:
    """Doğrusal interpolasyonlu yüzdelik (p ∈ [0, 100]). Gecikme p50/p95 için."""

    if not values:
        return 0.0
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    rank = (len(ordered) - 1) * (p / 100.0)
    low = int(rank)
    high = min(low + 1, len(ordered) - 1)
    frac = rank - low
    return ordered[low] + (ordered[high] - ordered[low]) * frac


def topk_accuracy(records: list[tuple[str, list[str]]], k: int) -> float:
    """Gerçek etiket, ilk k tahmin içinde mi? (records: (true, sıralı_tahminler))."""

    if not records:
        return 0.0
    hits = sum(1 for true, preds in records if true in preds[:k])
    return hits / len(records)
