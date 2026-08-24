"""Aşama 11 birim testleri: alan (domain) kapısı."""

import unittest

from src.domain import (
    STOPWORDS,
    build_domain_vocab,
    get_domain_vocab,
    is_in_domain,
    is_explicitly_out_of_scope,
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
        for q in [
            "Bana bir fıkra anlat",
            "En yakın pizzacı nerede?",
            "Bugün hava nasıl?",
            "Kilo vermek için ödev önerir misin?",
            "Matematik ödevimi çözer misin?",
        ]:
            with self.subTest(q=q):
                self.assertFalse(is_in_domain(q))

    def test_only_stopwords_is_out(self) -> None:
        self.assertFalse(is_in_domain("nasıl nerede bir"))

    def test_empty_is_out(self) -> None:
        self.assertFalse(is_in_domain(""))

    def test_explicit_oos_variants_do_not_reenter_via_product_words(self) -> None:
        for query in (
            "Bugün hava ne şekilde olacak",
            "Hezarfen'de en yakın pizzacı nerede",
            "Fizik konusunu adım adım özetle",
            "Yarın okul var mı tatil mi",
            "Sınıfın en çalışkanı kim",
            "Python döngüsünü anlat",
        ):
            with self.subTest(query=query):
                self.assertTrue(is_explicitly_out_of_scope(query))
                self.assertFalse(is_in_domain(query))

    def test_school_dietary_profile_is_not_hard_oos(self) -> None:
        self.assertFalse(
            is_explicitly_out_of_scope("öğrencinin diyet profilini güncelle")
        )


class StopwordsTests(unittest.TestCase):
    def test_stopwords_are_folded_ascii(self) -> None:
        # Katlanmış (ascii) olmalı ki içerik tokenlarıyla eşleşsin.
        for word in STOPWORDS:
            self.assertEqual(word, word.encode("ascii", "ignore").decode())


if __name__ == "__main__":
    unittest.main()
