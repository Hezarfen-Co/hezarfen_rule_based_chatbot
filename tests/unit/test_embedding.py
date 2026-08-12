"""Aşama 17 birim testleri: backend protokolü + opsiyonel embedding backend'i."""

import importlib.util
import unittest

from src.similarity import SimilarityBackend, SimilarityMatcher

_HAS_ST = importlib.util.find_spec("sentence_transformers") is not None


class BackendProtocolTests(unittest.TestCase):
    def test_tfidf_satisfies_backend(self) -> None:
        matcher = SimilarityMatcher.from_catalog()
        self.assertIsInstance(matcher, SimilarityBackend)


class EmbeddingMatcherTests(unittest.TestCase):
    def test_import_error_when_lib_absent(self) -> None:
        if _HAS_ST:
            self.skipTest("sentence-transformers kurulu; hata yolu test edilemez.")
        from src.embedding import EmbeddingMatcher

        with self.assertRaises(ImportError):
            EmbeddingMatcher(examples=[("greeting", "merhaba")])

    @unittest.skipUnless(_HAS_ST, "sentence-transformers kurulu değil.")
    def test_embedding_backend_ranks(self) -> None:  # pragma: no cover
        from src.embedding import EmbeddingMatcher

        matcher = EmbeddingMatcher.from_catalog()
        self.assertIsInstance(matcher, SimilarityBackend)
        best = matcher.best("karnemi görmek istiyorum")
        self.assertIsNotNone(best)


if __name__ == "__main__":
    unittest.main()
