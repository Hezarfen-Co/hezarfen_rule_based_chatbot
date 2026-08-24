"""Aşama 4 birim testleri: normalizasyon ve Türkçe kök bulma.

Her fonksiyon için ayrı test.
"""

import unittest

from src.normalize import (
    MIN_STEM_LENGTH,
    collapse_whitespace,
    fold_accents,
    folded_tokens,
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


class FoldedTokensTests(unittest.TestCase):
    def test_known_chat_typos_are_canonicalized(self) -> None:
        self.assertEqual(
            folded_tokens("ogrnci notunu degstr"),
            ["ogrenci", "notunu", "degistir"],
        )

    def test_valid_tokens_are_not_changed(self) -> None:
        self.assertEqual(folded_tokens("sınav notunu sil"), ["sinav", "notunu", "sil"])

    def test_common_where_contraction_is_canonicalized(self) -> None:
        self.assertEqual(folded_tokens("etkinlikler nerde"), ["etkinlikler", "nerede"])

    def test_safe_social_and_meta_single_typos_are_canonicalized(self) -> None:
        self.assertEqual(
            folded_tokens("mrehaba selalmar plaftorm kiimsin"),
            ["merhaba", "selam", "platform", "kimsin"],
        )

    def test_short_valid_words_are_not_fuzzy_rewritten(self) -> None:
        self.assertEqual(folded_tokens("sol haber"), ["sol", "haber"])
        self.assertEqual(folded_tokens("kimin başladığını"), ["kimin", "basladigini"])

    def test_unique_product_typos_are_canonicalized(self) -> None:
        self.assertEqual(
            folded_tokens("Sisetmden İngilice mensü yaynılıcam"),
            ["sistemden", "ingilizce", "menu", "yayinla"],
        )
        self.assertEqual(
            folded_tokens("veil çcouğu rezervasyyonsuz sevris"),
            ["veli", "cocugu", "rezervasyonsuz", "servis"],
        )

    def test_observed_short_typos_use_exact_aliases(self) -> None:
        self.assertEqual(
            folded_tokens("Sooru srouyu oddev yrmek saoll"),
            ["soru", "soruyu", "odev", "yemek", "sagol"],
        )
        self.assertEqual(
            folded_tokens("gelmdei saay knedi meesaj muutfak drss"),
            ["gelmedi", "saat", "kendi", "mesaj", "mutfak", "ders"],
        )
        self.assertEqual(
            folded_tokens("şirfem değiştirCem tkip drvam yükkselt şubbe nedre"),
            ["sifre", "degistir", "takip", "devam", "yukselt", "sube", "nerede"],
        )

    def test_observed_inflected_product_typos_keep_surface_form(self) -> None:
        self.assertEqual(
            folded_tokens("öğrencnin öğrettmenin kılavzuu listeim sınabdan"),
            ["ogrencinin", "ogretmenin", "kilavuzu", "listemi", "sinavdan"],
        )
        self.assertEqual(
            folded_tokens("pannel tannıtım kaaptmak desrleri aktairrken başksaının"),
            ["panel", "tanitim", "kapatmak", "dersleri", "aktarirken", "baskasinin"],
        )

    def test_deterministic_stress_exact_aliases_are_conservative(self) -> None:
        self.assertEqual(
            folded_tokens("Mesak dres Nabre salo sorıyu sueb yemeek etkinlite nrede"),
            ["mesaj", "ders", "naber", "sagol", "soruyu", "sube", "yemek", "etkinlikte", "nerede"],
        )
        self.assertEqual(
            folded_tokens("getor banaa kç mezuun hrdiye üniversietyi devamsızlığıı"),
            ["getir", "bana", "kac", "mezun", "hediye", "universiteyi", "devamsizligimi"],
        )

    def test_v35_observed_typos_use_exact_conservative_aliases(self) -> None:
        self.assertEqual(
            folded_tokens("nasılsnı kmisin kılavuu Guode çkış Rool sgv enaled"),
            ["nasilsin", "kimsin", "kilavuz", "guide", "cikis", "rol", "svg", "enabled"],
        )
        self.assertEqual(
            folded_tokens("otruumunun konttrolü asekron eklme ödelver teslm mrsai"),
            ["oturumunun", "kontrolu", "asenkron", "ekleme", "odevler", "teslim", "mesai"],
        )
        self.assertEqual(
            folded_tokens("subbeleri Bguün pneldeki banksı etkinlkileri sınvaların dpsyalarını"),
            ["subeleri", "bugun", "paneldeki", "bankasi", "etkinlikler", "sinavlarin", "dosyalarini"],
        )
        self.assertEqual(
            folded_tokens("Öğüm ücrretini yoklamssını meünsü ekllemek yaynılamak mutfal hvuzunda havzua"),
            ["ogun", "ucretini", "yoklamasini", "menusu", "eklemek", "yayinlamak", "mutfak", "havuzunda", "havuza"],
        )

    def test_ambiguous_neighbours_are_not_fuzzy_rewritten(self) -> None:
        self.assertEqual(
            folded_tokens("sorun demek öde bi dr el sona komusu"),
            ["sorun", "demek", "ode", "bi", "dr", "el", "sona", "komusu"],
        )


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
