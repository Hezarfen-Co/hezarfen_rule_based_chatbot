"""Metin normalizasyonu ve hafif Türkçe kök bulma.

Amaç: aynı anlamı taşıyan farklı yazımları tek forma indirgemek. Türkçe
sondan-eklemeli olduğu için ('notlarımı', 'notların', 'notum' -> 'not') hafif
bir kök bulma, kelime-torbası eşleşmesinin en zayıf noktasını kapatır.

Tasarım kararları:
- Türkçe-duyarlı küçük harf: 'I'->'ı', 'İ'->'i' (Python'un varsayılan lower'ı
  bunları yanlış yapar).
- Aksan katlama (fold): ç->c, ğ->g, ı->i, ö->o, ş->s, ü->u — kullanıcı Türkçe
  karakter kullanmadan yazsa da ('sinav' ~ 'sınav') eşleşme tutar.
- Stemmer bilinçli olarak HAFİF ve fazla-kırpmaya karşı korumalıdır (asgari kök
  uzunluğu). Dilbilimsel mükemmellik değil, sorgu ile anahtar kelime arasında
  TUTARLILIK hedeflenir; kural katmanı önek (prefix) eşleşmesiyle bunu tamamlar.

Tüm fonksiyonlar saf ve deterministiktir (loglanabilir/test edilebilir).
"""

from __future__ import annotations

import re
from typing import Final


MIN_STEM_LENGTH: Final[int] = 3
_MAX_STEM_PASSES: Final[int] = 3

# Türkçe küçük harf için özel eşlemeler (lower() öncesi uygulanır).
_UPPER_MAP: Final[dict[str, str]] = {"İ": "i", "I": "ı"}

# Aksan katlama (küçük harf sonrası).
_FOLD_MAP: Final[dict[str, str]] = str.maketrans(
    {
        "ç": "c",
        "ğ": "g",
        "ı": "i",
        "ö": "o",
        "ş": "s",
        "ü": "u",
        "â": "a",
        "î": "i",
        "û": "u",
    }
)

# Yalnızca harf/rakam/boşluk bırak (Türkçe harfler dahil).
_PUNCT_RE: Final[re.Pattern[str]] = re.compile(r"[^0-9a-zçğıöşü\s]", re.IGNORECASE)
_WS_RE: Final[re.Pattern[str]] = re.compile(r"\s+")

# Katlanmış (ascii) tokenlar üzerinde çalışan, uzundan kısaya denenecek ekler.
_SUFFIXES: Final[tuple[str, ...]] = tuple(
    sorted(
        {
            # çoğul + iyelik/hal birleşik
            "larimizi", "lerimizi", "larinizi", "lerinizi",
            "larimiz", "lerimiz", "lariniz", "leriniz",
            "larini", "lerini", "larimi", "lerimi",
            "lardan", "lerden", "larda", "lerde",
            "larim", "lerim", "larin", "lerin",
            "lara", "lere", "lari", "leri",
            "lar", "ler",
            # iyelik
            "imiz", "iniz", "umuz", "unuz",
            "imi", "ini", "umu", "unu",
            "im", "in", "um", "un",
            # hal ekleri
            "ndan", "nden", "tan", "ten", "dan", "den",
            "nin", "nun", "nda", "nde",
            "da", "de", "ta", "te",
            "na", "ne", "ya", "ye",
            "yi", "yu", "yi",
            "si", "su",
            # fiil/soru
            "yor", "dir", "tir", "dur", "tur", "mis", "mus",
            "acak", "ecek", "mak", "mek",
            "mi", "mu",
            # tekil sesli hal ekleri (asgari uzunlukla korunur)
            "i", "u", "a", "e",
        },
        key=len,
        reverse=True,
    )
)


def turkish_lower(text: str) -> str:
    """Türkçe kurallarına göre küçük harfe çevirir."""

    for upper, lower in _UPPER_MAP.items():
        text = text.replace(upper, lower)
    return text.lower()


def strip_punctuation(text: str) -> str:
    """Harf/rakam/boşluk dışındaki karakterleri boşlukla değiştirir."""

    return _PUNCT_RE.sub(" ", text)


def collapse_whitespace(text: str) -> str:
    """Ardışık boşlukları teke indirir ve baştaki/sondaki boşluğu atar."""

    return _WS_RE.sub(" ", text).strip()


def normalize(text: str) -> str:
    """Tam normalizasyon: küçük harf + noktalama temizliği + boşluk sadeleştirme.

    Türkçe karakterleri KORUR (okunabilir/loglanabilir form).
    """

    return collapse_whitespace(strip_punctuation(turkish_lower(text)))


def fold_accents(text: str) -> str:
    """Türkçe özel karakterleri ascii karşılıklarına katlar."""

    return text.translate(_FOLD_MAP)


def tokenize(text: str) -> list[str]:
    """Normalize edilmiş metni boşluklardan tokenlara ayırır."""

    normalized = normalize(text)
    if not normalized:
        return []
    return normalized.split(" ")


def folded_tokens(text: str) -> list[str]:
    """Normalize + katla ama STEM ETME: kural katmanı önek eşleşmesi için.

    Stem'in aksine kelimeleri çökertmez ('yapamıyor' -> 'yapamiyor', 'yap' değil),
    böylece anahtar kelime önek eşleşmesi ('sifre' <- 'sifremi') kesin kalır.
    """

    return [fold_accents(token) for token in tokenize(text)]


def stem(token: str) -> str:
    """Katlanmış (ascii) bir token için hafif kök bulma.

    Girdi ascii'ye katlanmış varsayılır. Asgari kök uzunluğu korunur; en fazla
    birkaç geçişte en uzun eşleşen ek soyulur.
    """

    for _ in range(_MAX_STEM_PASSES):
        stripped = False
        for suffix in _SUFFIXES:
            if token.endswith(suffix) and len(token) - len(suffix) >= MIN_STEM_LENGTH:
                token = token[: -len(suffix)]
                stripped = True
                break
        if not stripped:
            break
    return token


def roots(text: str) -> list[str]:
    """Metni köklerine indirger: normalize + katla + token + stem.

    Kural katmanının kullandığı kanonik biçim. Boş tokenlar atlanır.
    """

    return [stem(fold_accents(token)) for token in tokenize(text) if token]
