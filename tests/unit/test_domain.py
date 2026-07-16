"""Aşama 11 birim testleri: alan (domain) kapısı."""

import unittest

from src.domain import (
    STOPWORDS,
    build_domain_vocab,
    get_domain_vocab,
    is_in_domain,
)


class VocabTests(unittest.TestCase):
    def test_vocab_nonempty(self) -> None:
        self.assertGreater(len(build_domain_vocab()), 0)

    def test_vocab_contains_domain_words(self) -> None:
        vocab = build_domain_vocab()
        self.assertIn("ders", vocab)

    def test_vocab_excludes_stopwords(self) -> None:
        vocab = build_domain_vocab()
        for stop in ["nasil", "nerede", "bir"]:
            self.assertNotIn(stop, vocab)

    def test_cached(self) -> None:
        self.assertIs(get_domain_vocab(), get_domain_vocab())


class IsInDomainTests(unittest.TestCase):
    def test_in_domain_queries(self) -> None:
        for q in ["Karnemi göster", "sınav oluştur", "yoklama al", "derslerim neler"]:
            with self.subTest(q=q):
                self.assertTrue(is_in_domain(q))

    def test_out_of_domain_queries(self) -> None:
        for q in ["Bana bir fıkra anlat", "En yakın pizzacı nerede?", "Bugün hava nasıl?"]:
            with self.subTest(q=q):
                self.assertFalse(is_in_domain(q))

    def test_only_stopwords_is_out(self) -> None:
        self.assertFalse(is_in_domain("nasıl nerede bir"))

    def test_empty_is_out(self) -> None:
        self.assertFalse(is_in_domain(""))


class StopwordsTests(unittest.TestCase):
    def test_stopwords_are_folded_ascii(self) -> None:
        # Katlanmış (ascii) olmalı ki içerik tokenlarıyla eşleşsin.
        for word in STOPWORDS:
            self.assertEqual(word, word.encode("ascii", "ignore").decode())


if __name__ == "__main__":
    unittest.main()
