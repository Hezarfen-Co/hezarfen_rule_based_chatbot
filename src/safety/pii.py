"""PII (kişisel veri) tespiti ve maskeleme.

E-posta, IBAN, kredi kartı, telefon ve T.C. kimlik numarasını yakalar ve maskeler.
Giriş güvenliğinde MASK_AND_ALLOW, çıktı güvenliğinde sızıntı önleme için kullanılır.

Kaçırma dayanıklılığı: eşleşmeden önce metin normalize edilir — görünmez unicode
silinir ve fullwidth rakam/harf (０-９) normal ASCII'ye indirgenir. Sayı grupları
arasında nokta/eğik çizgi/boşluk/parantez ayraçlarına tolerans gösterilir
(0532.123.45.67, +90 (532) 123 45 67, 0532/123/45/67, 123 456 789 01 vb.).
"""

from __future__ import annotations

import re
from typing import Final


# Görünmez/sıfır-genişlik unicode (e-posta ve numaraların ortasına sokularak
# regex'i bölmek için kullanılır) — eşleşmeden önce temizlenir.
_INVISIBLE_RE: Final[re.Pattern[str]] = re.compile(
    "[​‌‍‎‏‪-‮⁠﻿­]"
)

# Sayı grupları arasındaki kabul edilen ayraçlar.
_SEP = r"[\s.\-/()]*"

# Sıra önemli: kart (16 hane) -> telefon (0/5 ile, 11 hane) -> TC (11 hane, 0/5 dışı).
_PII_PATTERNS: Final[list[tuple[str, re.Pattern[str]]]] = [
    ("email", re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")),
    ("iban", re.compile(r"TR\d{2}" + _SEP + r"(?:\d{4}" + _SEP + r"){5}\d{2}", re.IGNORECASE)),
    ("credit_card", re.compile(r"\b\d{4}[\s.\-]?\d{4}[\s.\-]?\d{4}[\s.\-]?\d{4}\b")),
    ("phone", re.compile(r"(?:\+?90)?" + _SEP + r"0?5\d{2}" + _SEP + r"\d{3}" + _SEP + r"\d{2}" + _SEP + r"\d{2}")),
    ("tc_kimlik", re.compile(r"\b[1-9]\d{2}[\s.]?\d{3}[\s.]?\d{3}[\s.]?\d{2}\b")),
]


def _normalize(text: str) -> str:
    """Görünmez unicode'u sil, fullwidth rakam/harfi ASCII'ye indir."""

    text = _INVISIBLE_RE.sub("", text)
    out: list[str] = []
    for ch in text:
        code = ord(ch)
        if 0xFF01 <= code <= 0xFF5E:  # fullwidth ASCII
            out.append(chr(code - 0xFEE0))
        else:
            out.append(ch)
    return "".join(out)


def _mask_value(value: str) -> str:
    digits = re.sub(r"\D", "", value)
    if "@" in value:  # email
        name, _, domain = value.partition("@")
        head = name[:2]
        return f"{head}***@{domain}"
    if len(digits) <= 4:
        return "*" * len(value)
    keep_tail = 4 if len(digits) >= 8 else 2
    return digits[:3] + "*" * 3 + digits[-keep_tail:]


def mask_pii(text: str) -> tuple[str, list[str]]:
    """Metindeki PII'leri maskeler. Döner: (maskelenmiş_metin, bulunan_kategoriler).

    Eşleşme normalize edilmiş metin üzerinde yapılır (kaçırma dayanıklılığı); dönen
    maskelenmiş metin de normalize edilmiş hâlidir (görünmez unicode temizlenmiş)."""

    found: list[str] = []
    masked = _normalize(text)
    for category, pattern in _PII_PATTERNS:
        if pattern.search(masked):
            found.append(category)
            masked = pattern.sub(lambda m: _mask_value(m.group(0)), masked)
    return masked, found
