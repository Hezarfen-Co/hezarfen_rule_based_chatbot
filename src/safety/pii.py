"""PII (kişisel veri) tespiti ve maskeleme.

E-posta, IBAN, kredi kartı, telefon ve T.C. kimlik numarasını yakalar ve maskeler.
Giriş güvenliğinde MASK_AND_ALLOW, çıktı güvenliğinde sızıntı önleme için kullanılır.
"""

from __future__ import annotations

import re
from typing import Final


# Sıra önemli: telefon TC'den ÖNCE denenir (ikisi de 11 hane olabilir; telefon
# 0/5 ile başlar, TC ise 0 ile başlamaz).
_PII_PATTERNS: Final[list[tuple[str, re.Pattern[str]]]] = [
    ("email", re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")),
    ("iban", re.compile(r"\bTR\d{24}\b", re.IGNORECASE)),
    ("credit_card", re.compile(r"\b\d{4}[ -]?\d{4}[ -]?\d{4}[ -]?\d{4}\b")),
    ("phone", re.compile(r"\b(?:\+?90[ -]?)?0?5\d{2}[ -]?\d{3}[ -]?\d{2}[ -]?\d{2}\b")),
    ("tc_kimlik", re.compile(r"\b[1-9]\d{10}\b")),
]


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
    """Metindeki PII'leri maskeler. Döner: (maskelenmiş_metin, bulunan_kategoriler)."""

    found: list[str] = []
    masked = text
    for category, pattern in _PII_PATTERNS:
        if pattern.search(masked):
            found.append(category)
            masked = pattern.sub(lambda m: _mask_value(m.group(0)), masked)
    return masked, found
