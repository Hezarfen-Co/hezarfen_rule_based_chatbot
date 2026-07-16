"""Benzerlik katmanı: saf-Python TF-IDF karakter n-gram + kosinüs.

Kural katmanı bir soruyu kapsamadığında (None döndüğünde) devreye girer. Katalog
`example_questions`'larını karakter n-gram TF-IDF vektörlerine çevirir; sorguyu
aynı uzaya taşıyıp en yakın örneği kosinüs benzerliğiyle bulur ve o örneğin
intent'ini döndürür.

Neden karakter n-gram: Türkçe sondan-eklemeli olduğundan ('notlarımı' ~ 'notlar')
karakter n-gram'lar çekim varyasyonlarını kelime-torbasından çok daha iyi tolere
eder ve harici model/bağımlılık gerektirmez.

Neden vektör DB yok: ~215 örnek vektörde brute-force kosinüs milisaniyenin
altındadır; FAISS/Chroma gereksizdir.

Arayüz soyuttur (SimilarityMatcher); ileride yerel embedding modeli aynı
`rank()/best()` sözleşmesiyle takılabilir.
"""

from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass
from typing import Final, Iterable

from .catalog import INTENTS
from .normalize import fold_accents, normalize


DEFAULT_NGRAMS: Final[tuple[int, ...]] = (3, 4, 5)


def _prepare(text: str) -> str:
    """Normalize + katla + boşluklarla sınır işaretle (n-gram için)."""

    folded = fold_accents(normalize(text))
    return f" {folded} " if folded else ""


def char_ngrams(text: str, ns: Iterable[int] = DEFAULT_NGRAMS) -> Counter[str]:
    """Metnin karakter n-gram frekanslarını döndürür."""

    prepared = _prepare(text)
    counts: Counter[str] = Counter()
    if not prepared:
        return counts
    length = len(prepared)
    for n in ns:
        if length < n:
            continue
        for i in range(length - n + 1):
            counts[prepared[i : i + n]] += 1
    return counts


@dataclass(frozen=True)
class ScoredIntent:
    intent: str
    score: float


class SimilarityMatcher:
    """Karakter n-gram TF-IDF üzerinden intent benzerliği."""

    def __init__(
        self,
        examples: list[tuple[str, str]],
        ns: Iterable[int] = DEFAULT_NGRAMS,
    ) -> None:
        """examples: (intent, question) çiftleri."""

        self._ns = tuple(ns)
        self._intents: list[str] = []
        self._doc_tfs: list[Counter[str]] = []

        document_frequency: Counter[str] = Counter()
        for intent, question in examples:
            tf = char_ngrams(question, self._ns)
            if not tf:
                continue
            self._intents.append(intent)
            self._doc_tfs.append(tf)
            for gram in tf:
                document_frequency[gram] += 1

        num_docs = len(self._doc_tfs)
        # Düzeltmeli (smoothed) IDF.
        self._idf: dict[str, float] = {
            gram: math.log((num_docs + 1) / (df + 1)) + 1.0
            for gram, df in document_frequency.items()
        }

        # Örnek vektörlerini ve normlarını önceden hesapla.
        self._doc_vectors: list[dict[str, float]] = []
        self._doc_norms: list[float] = []
        for tf in self._doc_tfs:
            vector = self._to_vector(tf)
            self._doc_vectors.append(vector)
            self._doc_norms.append(_norm(vector))

    @classmethod
    def from_catalog(cls, ns: Iterable[int] = DEFAULT_NGRAMS) -> "SimilarityMatcher":
        """Katalog example_questions'larından bir eşleştirici kurar."""

        examples = [
            (item["intent"], question)
            for item in INTENTS
            for question in item["example_questions"]
        ]
        return cls(examples, ns=ns)

    @property
    def size(self) -> int:
        """Dizinlenmiş örnek sayısı."""

        return len(self._doc_vectors)

    def _to_vector(self, tf: Counter[str]) -> dict[str, float]:
        """TF sayımını IDF ağırlıklı vektöre çevirir (bilinmeyen gram'lar atlanır)."""

        return {
            gram: count * self._idf[gram]
            for gram, count in tf.items()
            if gram in self._idf
        }

    def rank(self, query: str) -> list[ScoredIntent]:
        """Sorguyu intent'lere göre azalan benzerlikle sıralar.

        Her intent için, o intent'e ait örnekler arasındaki EN YÜKSEK kosinüs
        benzerliği o intent'in skorudur.
        """

        query_tf = char_ngrams(query, self._ns)
        query_vec = self._to_vector(query_tf)
        query_norm = _norm(query_vec)
        if query_norm == 0.0:
            return []

        best: dict[str, float] = {}
        for intent, doc_vec, doc_norm in zip(
            self._intents, self._doc_vectors, self._doc_norms
        ):
            if doc_norm == 0.0:
                continue
            score = _dot(query_vec, doc_vec) / (query_norm * doc_norm)
            if score > best.get(intent, 0.0):
                best[intent] = score

        return [
            ScoredIntent(intent, score)
            for intent, score in sorted(best.items(), key=lambda kv: kv[1], reverse=True)
        ]

    def best(self, query: str) -> ScoredIntent | None:
        """En yüksek skorlu intent'i döndürür (yoksa None)."""

        ranked = self.rank(query)
        return ranked[0] if ranked else None


def _dot(a: dict[str, float], b: dict[str, float]) -> float:
    # Daha kısa sözlük üzerinde döngü kur.
    if len(a) > len(b):
        a, b = b, a
    return sum(weight * b.get(gram, 0.0) for gram, weight in a.items())


def _norm(vector: dict[str, float]) -> float:
    return math.sqrt(sum(weight * weight for weight in vector.values()))


# Katalogdan kurulmuş, süreç ömrü boyunca yeniden kullanılan varsayılan örnek.
_DEFAULT_MATCHER: SimilarityMatcher | None = None


def get_default_matcher() -> SimilarityMatcher:
    """Katalogdan kurulmuş paylaşılan eşleştiriciyi döndürür (tembel kurulum)."""

    global _DEFAULT_MATCHER
    if _DEFAULT_MATCHER is None:
        _DEFAULT_MATCHER = SimilarityMatcher.from_catalog()
    return _DEFAULT_MATCHER
