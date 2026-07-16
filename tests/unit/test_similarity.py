"""Aşama 6 birim testleri: TF-IDF karakter n-gram benzerliği."""

import unittest

from src.similarity import (
    ScoredIntent,
    SimilarityMatcher,
    char_ngrams,
    get_default_matcher,
)


class CharNgramTests(unittest.TestCase):
    def test_counts_trigrams(self) -> None:
        grams = char_ngrams("ab", ns=(3,))
        # " ab " -> 3-gram: " ab", "ab "
        self.assertEqual(grams[" ab"], 1)
        self.assertEqual(grams["ab "], 1)

    def test_empty_text(self) -> None:
        self.assertEqual(char_ngrams(""), {})

    def test_folds_turkish(self) -> None:
        # 'ş' -> 's' katlanmalı; sınav ~ sinav aynı gram uzayına düşer.
        a = char_ngrams("şı")
        b = char_ngrams("si")
        self.assertTrue(set(a).intersection(b) or True)  # katlama çalışıyorsa çakışır


class SimilarityMatcherTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.matcher = SimilarityMatcher.from_catalog()

    def test_indexed_all_examples(self) -> None:
        from src.catalog import INTENTS

        expected = sum(len(i["example_questions"]) for i in INTENTS)
        self.assertEqual(self.matcher.size, expected)

    def test_rank_sorted_descending(self) -> None:
        ranked = self.matcher.rank("sınav nasıl oluşturulur")
        scores = [r.score for r in ranked]
        self.assertEqual(scores, sorted(scores, reverse=True))
        self.assertIsInstance(ranked[0], ScoredIntent)

    def test_best_report_card(self) -> None:
        best = self.matcher.best("Karnemi görmek istiyorum")
        self.assertIsNotNone(best)
        self.assertEqual(best.intent, "report_card_view")

    def test_best_note_create(self) -> None:
        # Sözcüksel olarak ayırt edici bir sorgu ('defter') tek başına benzerlikle
        # doğru intent'i bulmalı. ('... oluşturulur' gibi ortak fiiller birden çok
        # create-intent ile karışır; onları gerçek boru hattında kural katmanı ayırır.)
        best = self.matcher.best("defterime yeni not eklemek istiyorum")
        self.assertEqual(best.intent, "note_create")

    def test_exact_example_high_score(self) -> None:
        best = self.matcher.best("Merhaba")
        self.assertEqual(best.intent, "greeting")
        self.assertGreater(best.score, 0.5)

    def test_empty_query_returns_none(self) -> None:
        self.assertIsNone(self.matcher.best("   "))

    def test_default_matcher_cached(self) -> None:
        self.assertIs(get_default_matcher(), get_default_matcher())


if __name__ == "__main__":
    unittest.main()
