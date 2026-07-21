"""Alan (domain) kapısı: sorgu Hezarfen alanına ait mi?

OOS (kapsam dışı) tespitini güçlendirir. Char n-gram benzerliği, ortak Türkçe
diziler yüzünden alakasız sorulara da skor verdiğinden tek başına eşik yetmez.
Buradaki kapı basit ama etkili bir sinyaldir: sorgunun içerik kelimeleri (jenerik
bağlaçlar/soru kalıpları çıkarıldıktan sonra) katalog söz varlığıyla hiç örtüşmüyorsa
soru büyük olasılıkla kapsam dışıdır.

Söz varlığı `example_questions`'ın katlanmış tokenlarından üretilir; jenerik
kelimeler (nasıl, nerede, bir, ...) elenir çünkü onlar hem in-scope hem OOS'ta
bulunur ve ayırt edici değildir.
"""

from __future__ import annotations

from typing import Final

from .catalog import INTENTS
from .normalize import folded_tokens


_MIN_TOKEN_LEN: Final[int] = 3

# Jenerik/işlevsel kelimeler (katlanmış). Hem in-scope hem OOS'ta geçtikleri için
# alan sinyali taşımazlar; söz varlığından ve sorgu içerik tokenlarından elenir.
STOPWORDS: Final[frozenset[str]] = frozenset(
    {
        "nasil", "nerede", "nedir", "hangi", "kac", "kacta", "neden",
        "istiyorum", "ister", "isterim", "gosterir", "goster", "gormek", "gorurum",
        "var", "yok", "mumkun", "olur", "olacak", "olabilir", "yapmak", "yapilir",
        "edebilir", "misin", "miyim", "muyum", "musun", "mi", "mu",
        "bir", "bana", "benim", "sen", "ben", "ile", "icin", "daha", "cok",
        "bu", "sunu", "sonra", "once", "gibi", "kadar", "ama", "veya",
        "lazim", "gerek", "acaba", "peki", "yeni",
        "eder", "ederim", "edeyim", "etmek", "edilir",
        # Generic anlatım/tanıtım fiilleri — alan-ayırt edici değil (fıkra anlat,
        # şiir anlat da bunları içerir). platform_info örnekleriyle sözlüğe sızmasın.
        "anlat", "anlatir", "anlatabilir", "kisaca", "tanit", "tanitir", "bilgi",
    }
)


def _content_tokens(text: str) -> list[str]:
    """Sorgunun ayırt edici (jenerik olmayan, >=3 harf) içerik tokenları."""

    return [
        token
        for token in folded_tokens(text)
        if len(token) >= _MIN_TOKEN_LEN and token not in STOPWORDS
    ]


def build_domain_vocab() -> set[str]:
    """Katalog örneklerinden ayırt edici alan söz varlığını üretir."""

    vocab: set[str] = set()
    for item in INTENTS:
        for question in item["example_questions"]:
            vocab.update(_content_tokens(question))
    return vocab


_DEFAULT_VOCAB: set[str] | None = None


def get_domain_vocab() -> set[str]:
    """Paylaşılan alan söz varlığını döndürür (tembel kurulum)."""

    global _DEFAULT_VOCAB
    if _DEFAULT_VOCAB is None:
        _DEFAULT_VOCAB = build_domain_vocab()
    return _DEFAULT_VOCAB


def _overlaps(token: str, vocab: set[str]) -> bool:
    if token in vocab:
        return True
    # Çekim varyasyonları için önek eşleşmesi (her iki yönde, >=3 harf).
    return any(
        (token.startswith(v) or v.startswith(token))
        for v in vocab
        if len(v) >= _MIN_TOKEN_LEN
    )


def is_in_domain(query: str, vocab: set[str] | None = None) -> bool:
    """Sorgunun içerik kelimeleri alan söz varlığıyla yeterince örtüşüyor mu?

    Sinyal gücü sorgu uzunluğuna göre ayarlanır:
    - Tam eşleşme (kelime söz varlığında birebir var) -> güçlü sinyal, tek başına yeter.
    - Kısa sorgu (<=2 içerik kelimesi): tek bir kısmi (önek) örtüşme yeter.
    - Uzun sorgu (>=3 içerik kelimesi) ve hiç tam eşleşme yok: tek bir zayıf önek
      örtüşmesi ('yazılır' ~ 'yazılı') yanıltıcı olabilir -> en az 2 örtüşme iste.
      Bu, alan-dışı uzun cümlelerin ('python'da döngü nasıl yazılır') tek bir
      yanlış-dost yüzünden alan-içi sayılmasını azaltır.
    """

    vocab = vocab if vocab is not None else get_domain_vocab()
    content = _content_tokens(query)
    if not content:
        # Yalnızca jenerik kelimelerden oluşan sorgu -> ayırt edici alan sinyali yok.
        return False
    if any(token in vocab for token in content):
        return True
    overlaps = sum(1 for token in content if _overlaps(token, vocab))
    if len(content) <= 2:
        return overlaps >= 1
    return overlaps >= 2
