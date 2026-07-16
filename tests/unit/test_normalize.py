"""Aşama 4 birim testleri: normalizasyon ve Türkçe kök bulma.

Her fonksiyon için ayrı test.
"""

import unittest

from src.normalize import (
    MIN_STEM_LENGTH,
    collapse_whitespace,
    fold_accents,
    normalize,
    roots,
    stem,
    strip_punctuation,
    tokenize,
    turkish_lower,
)


class TurkishLowerTests(unittest.TestCase):
    def test_dotted_capital_i(self) -> None:
        self.assertEqual(turkish_lower("İSTANBUL"), "istanbul")

    def test_dotless_capital_i(self) -> None:
        self.assertEqual(turkish_lower("IŞIK"), "ışık")

    def test_mixed(self) -> None:
        self.assertEqual(turkish_lower("Güneş Işığı"), "güneş ışığı")

    def test_no_combining_dot_artifact(self) -> None:
        # Python'un varsayılan 'İ'.lower() birleşik nokta üretir; biz üretmemeliyiz.
        self.assertNotIn("̇", turkish_lower("İ"))


class StripPunctuationTests(unittest.TestCase):
    def test_removes_punctuation(self) -> None:
        self.assertEqual(strip_punctuation("merhaba!!!").strip(), "merhaba")

    def test_keeps_turkish_letters(self) -> None:
        self.assertEqual(strip_punctuation("çğıöşü").strip(), "çğıöşü")

    def test_keeps_digits(self) -> None:
        self.assertEqual(strip_punctuation("oda 12").strip(), "oda 12")


class CollapseWhitespaceTests(unittest.TestCase):
    def test_collapses_and_trims(self) -> None:
        self.assertEqual(collapse_whitespace("  a   b \t c "), "a b c")


class NormalizeTests(unittest.TestCase):
    def test_full_pipeline(self) -> None:
        self.assertEqual(normalize("Merhaba!!!  Nasılsın?"), "merhaba nasılsın")

    def test_empty_string(self) -> None:
        self.assertEqual(normalize("   "), "")

    def test_preserves_turkish_chars(self) -> None:
        self.assertEqual(normalize("Şifremi Unuttum"), "şifremi unuttum")


class FoldAccentsTests(unittest.TestCase):
    def test_folds_all_specials(self) -> None:
        self.assertEqual(fold_accents("çğıöşü"), "cgiosu")

    def test_word(self) -> None:
        self.assertEqual(fold_accents("güneş"), "gunes")


class TokenizeTests(unittest.TestCase):
    def test_splits_words(self) -> None:
        self.assertEqual(tokenize("Notlarımı göster"), ["notlarımı", "göster"])

    def test_empty(self) -> None:
        self.assertEqual(tokenize("   "), [])


class StemTests(unittest.TestCase):
    def test_plural(self) -> None:
        self.assertEqual(stem("dersler"), "ders")

    def test_plural_possessive_accusative(self) -> None:
        self.assertEqual(stem("sinavlarim"), "sinav")

    def test_plural_short_root(self) -> None:
        self.assertEqual(stem("notlar"), "not")

    def test_respects_min_stem_length(self) -> None:
        # Kök çok kısalacaksa ek soyulmaz.
        result = stem("eve")  # "e" ekini soyarsa "ev" (2) < MIN; soyulmamalı
        self.assertGreaterEqual(len(result), min(len("eve"), MIN_STEM_LENGTH))

    def test_no_suffix_unchanged(self) -> None:
        self.assertEqual(stem("goster"), "goster")

    def test_idempotent(self) -> None:
        once = stem("derslerimiz")
        twice = stem(once)
        self.assertEqual(once, twice)


class RootsTests(unittest.TestCase):
    def test_end_to_end(self) -> None:
        result = roots("Notlarımı göster")
        self.assertIn("not", result)
        self.assertIn("goster", result)

    def test_folds_and_stems(self) -> None:
        self.assertEqual(roots("sınavlarım"), ["sinav"])

    def test_keyword_consistency_for_rule_layer(self) -> None:
        # Kural katmanı için asıl invaryant: bir anahtar kelimenin kökü, o kelimenin
        # çekimli halinin köküyle AYNI olmalı. Böylece kural anahtarını aynı stemmer'la
        # işlersek eşleşme tutar (mükemmel dilbilim değil, tutarlılık).
        keyword_root = roots("şifre")[0]
        result = roots("Şifremi unuttum")
        self.assertIn(keyword_root, result, (keyword_root, result))

    def test_empty(self) -> None:
        self.assertEqual(roots(""), [])


if __name__ == "__main__":
    unittest.main()
