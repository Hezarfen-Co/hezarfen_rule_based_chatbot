"""Opsiyonel embedding backend'i — SimilarityBackend arayüzüne takılabilir.

Bu modül `sentence-transformers`'ı TEMBEL (lazy) içe aktarır. Kurulu değilse,
kurulum talimatı içeren net bir ImportError verir. Böylece temel proje SIFIR
bağımlılık kalır; embedding tamamen opt-in'dir.

Kullanım:
    from src.embedding import EmbeddingMatcher
    matcher = EmbeddingMatcher.from_catalog()   # model indirir (ilk sefer)
    # sonra decision/observability'ye matcher=matcher olarak enjekte edilebilir.

Neden aynı arayüz: `rank()/best()/size` sözleşmesi TF-IDF ile birebir aynı; karar
katmanı hangi backend'in kullanıldığını bilmez.
"""

from __future__ import annotations

from typing import Iterable

from .catalog import INTENTS
from .similarity import ScoredIntent

# Türkçe'ye özel eğitilmiş varsayılan. Çok dilli MiniLM'e göre "not" (grade vs
# note) gibi Türkçe belirsizliklerini daha iyi ayırır; skorları daha temiz.
DEFAULT_MODEL: str = "trmteb/turkish-embedding-model"

_IMPORT_HINT = (
    "EmbeddingMatcher için 'sentence-transformers' gerekli. Kurulum:\n"
    "    pip install sentence-transformers\n"
    "Temel proje bu bağımlılık olmadan (TF-IDF ile) çalışır."
)


class EmbeddingMatcher:
    """Yerel sentence-transformer ile intent benzerliği (opt-in)."""

    def __init__(
        self,
        examples: list[tuple[str, str]],
        model_name: str = DEFAULT_MODEL,
    ) -> None:
        try:
            from sentence_transformers import SentenceTransformer  # type: ignore
            import numpy as np  # type: ignore
        except ImportError as exc:  # pragma: no cover - ortama bağlı
            raise ImportError(_IMPORT_HINT) from exc

        self._np = np
        self._model = SentenceTransformer(model_name)
        self._intents = [intent for intent, _ in examples]
        questions = [q for _, q in examples]
        # Normalize edilmiş embedding'ler -> nokta çarpımı = kosinüs.
        self._matrix = self._model.encode(
            questions, normalize_embeddings=True, convert_to_numpy=True
        )

    @classmethod
    def from_catalog(cls, model_name: str = DEFAULT_MODEL) -> "EmbeddingMatcher":
        examples = [
            (item["intent"], q)
            for item in INTENTS
            for q in item["example_questions"]
        ]
        return cls(examples, model_name=model_name)

    @property
    def size(self) -> int:
        return len(self._intents)

    def rank(self, query: str) -> list[ScoredIntent]:
        if not query.strip():
            return []
        vec = self._model.encode([query], normalize_embeddings=True, convert_to_numpy=True)[0]
        scores = self._matrix @ vec  # kosinüs (normalize edilmiş)
        best: dict[str, float] = {}
        for intent, score in zip(self._intents, scores):
            value = float(score)
            if value > best.get(intent, -1.0):
                best[intent] = value
        return [
            ScoredIntent(intent, score)
            for intent, score in sorted(best.items(), key=lambda kv: kv[1], reverse=True)
        ]

    def best(self, query: str) -> ScoredIntent | None:
        ranked = self.rank(query)
        return ranked[0] if ranked else None
