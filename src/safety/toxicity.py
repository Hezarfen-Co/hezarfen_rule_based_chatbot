"""Toksik/zararlı içerik tespiti — kural tabanlı giriş kapısı ve çıktı kontrolü.

Mimari ilke: içerik filtresi; niyet, yetki ve iş-kuralı motorlarından AYRIDIR.
Her kural standart bir `SafetyDecision` döndürür (bkz. `.decisions`). Motor bunu
bir GİRİŞ KAPISI (intent'ten önce) ve bir ÇIKTI KONTROLÜ olarak kullanır.

Kapsanan kontroller (öncelik sırası):
    1) Prompt injection / sistem manipülasyonu   -> BLOCK
    2) Kendine zarar                              -> SAFE_RESPONSE (destekleyici)
    3) Tehdit / şiddet                            -> ESCALATE_TO_HUMAN
    4) Cinsel içerik / çocuk güvenliği            -> BLOCK (requires_review)
    5) Nefret söylemi                             -> BLOCK
    6) Küfür / hakaret (hedef-farkında)           -> ALLOW / ALLOW_WITH_WARNING / BLOCK
    7) Başkasının kişisel verisi (isimli)         -> REQUIRE_AUTHORIZATION
    8) PII (kişisel veri)                         -> MASK_AND_ALLOW
    else                                          -> ALLOW

Güvenlik-normalizasyonu, niyet-normalizasyonundan DAHA agresiftir (leetspeak,
tekrar harf, boşlukla ayrılmış harfler, görünmez unicode) çünkü amacı gizlenmiş
ihlalleri açığa çıkarmaktır. Orijinal mesaj loglama/inceleme için korunur.

Not: Kelime listeleri başlangıç niteliğindedir ve genişletilebilir. Tehdit/çocuk
güvenliği gibi ciddi kararlar otomatik "suçlu" ilan etmez; `requires_review=True`
ile insan incelemesine bırakılır.
"""

from __future__ import annotations

import re
from typing import Final

from ..normalize import fold_accents, turkish_lower
from .decisions import (
    ALLOW,
    ALLOW_WITH_WARNING,
    BLOCK,
    ESCALATE_TO_HUMAN,
    MASK_AND_ALLOW,
    REQUIRE_AUTHORIZATION,
    SAFE_RESPONSE,
    TEMPORARY_LIMIT,
    SafetyDecision,
    make_decision as _make,
)
from .pii import mask_pii


# --- Güvenlik normalizasyonu -------------------------------------------------
_INVISIBLE_RE: Final[re.Pattern[str]] = re.compile(
    r"[​‌‍‎‏﻿­⁠]"
)
_LEET_MAP: Final[dict[str, str]] = {
    "4": "a", "@": "a", "1": "i", "!": "i", "3": "e", "0": "o",
    "5": "s", "$": "s", "7": "t", "8": "b", "9": "g",
}
_REPEAT_RE: Final[re.Pattern[str]] = re.compile(r"(.)\1{2,}")


def _apply_leet(text: str) -> str:
    return "".join(_LEET_MAP.get(ch, ch) for ch in text)


def safety_normalize(message: str) -> str:
    """Agresif normalizasyon: gizlenmiş ihlalleri açığa çıkarır.

    Adımlar: görünmez unicode temizliği -> Türkçe küçük harf -> leetspeak ->
    3+ tekrar harfi teke indir -> aksan katla.
    """

    text = _INVISIBLE_RE.sub("", message)
    text = turkish_lower(text)
    text = _apply_leet(text)
    text = _REPEAT_RE.sub(r"\1", text)
    text = fold_accents(text)
    return text


def safety_tokens(message: str) -> list[str]:
    """Güvenlik-normalize edilmiş tokenlar; boşlukla ayrılmış tek harfler birleştirilir.

    'a h m e t' -> 'ahmet', 's a l a k' -> 'salak' (harf-harf gizleme).
    """

    normalized = safety_normalize(message)
    raw = re.findall(r"[a-z0-9]+", normalized)
    tokens: list[str] = []
    buffer: list[str] = []
    for tok in raw:
        if len(tok) == 1 and tok.isalpha():
            buffer.append(tok)
            continue
        if buffer:
            tokens.append("".join(buffer))
            buffer = []
        tokens.append(tok)
    if buffer:
        tokens.append("".join(buffer))
    return tokens


# --- Sözlükler (başlangıç; genişletilebilir) ---------------------------------
# Not: 'mal' gibi çok kısa/çakışan kökler bilinçli olarak DIŞARIDA (malzeme, mali...
# gibi masum kelimelere yapışır). Kısa kökler için eşleşme tam-kelime yapılır.
MILD_INSULTS: Final[frozenset[str]] = frozenset(
    {"salak", "aptal", "gerizekali", "ahmak", "dangalak", "ebleh",
     "budala", "sersem", "gerzek", "embesil", "andaval", "beyinsiz"}
)
STRONG_PROFANITY: Final[frozenset[str]] = frozenset(
    {"serefsiz", "orospu", "pic", "kahpe", "yavsak", "gavat", "amk", "aq",
     "sik", "sikeyim", "siktir", "got", "gotveren", "oc", "piçkurusu", "ananisik"}
)
_SYSTEM_TERMS: Final[frozenset[str]] = frozenset(
    {"sistem", "uygulama", "site", "program", "chatbot", "bot", "asistan", "arayuz"}
)
_ROLE_TARGETS: Final[frozenset[str]] = frozenset(
    {"ogretmen", "hoca", "mudur", "ogrenci", "arkadas", "veli", "danisman"}
)
_EDU_MARKERS: Final[frozenset[str]] = frozenset(
    {"anlami", "nedir", "demek", "kelime", "kelimesi", "tanimi", "manasi"}
)
# İsim tespitinde yanlış-pozitifi önlemek için sık büyük-harfli kelimeler.
# 'celebi' = asistanın adı; bota adıyla sataşma kişiye-taciz DEĞİL, bota-yönelik
# sayılır (uyar ama yardım et) — bu yüzden özel isim tespitinden dışlanır.
_COMMON_TITLE: Final[frozenset[str]] = frozenset(
    {"bu", "su", "o", "ben", "sen", "biz", "siz", "merhaba", "selam", "evet",
     "hayir", "nasil", "neden", "hangi", "peki", "ama", "gunaydin", "tesekkur",
     "lutfen", "naber", "bir", "birkac", "yeni", "kim", "kime", "kimin", "niye",
     "ne", "cok", "daha", "acaba", "bugun", "yarin", "simdi", "tum", "butun",
     "her", "bazi", "hep", "neler", "nerede", "nereden", "celebi"}
)

_THREAT_PATTERNS: Final[tuple[str, ...]] = (
    "dovecegim", "dovecem", "gebertecegim", "oldurecegim", "olduricem",
    "vuracagim", "yakacagim", "patlatacagim", "zarar verecegim", "zarar verecem",
    "canina okuyacagim", "silahla gelecegim", "biçaklayacagim", "bicaklayacagim",
    "kafani kiracagim",
)
_SELF_HARM_PATTERNS: Final[tuple[str, ...]] = (
    "kendime zarar", "intihar", "olmek istiyorum", "yasamak istemiyorum",
    "canima kiymak", "kendimi oldur", "hayatima son", "yasamak istemiyor",
    "intihar etmek",
)
_INJECTION_PATTERNS: Final[tuple[str, ...]] = (
    "onceki talimat", "talimatlari unut", "kurallari unut", "kurallari yok say",
    "sistem prompt", "gizli kural", "gizli talimat", "beni admin yap",
    "admin yap", "rolundeymis gibi", "gibi davran", "ignore previous",
    "disregard previous", "yok say ve", "sistem promptunu", "kurallarini yaz",
    "kurallarini goster", "onceki mesajlari unut",
)
_SEXUAL_TERMS: Final[frozenset[str]] = frozenset(
    {"seks", "porno", "ciplak", "cinsel", "tecavuz"}
)
_MINOR_TERMS: Final[frozenset[str]] = frozenset(
    {"cocuk", "resit", "kucuk", "ogrenci"}
)
_HATE_GROUP_TERMS: Final[frozenset[str]] = frozenset(
    {"irk", "din", "milliyet", "grup", "topluluk", "azinlik", "mezhep"}
)
_HARM_WORDS: Final[frozenset[str]] = frozenset(
    {"zarar", "olsun", "yok edilmeli", "yokedilmeli", "atilmali", "olmeli",
     "verilmeli", "temizlenmeli"}
)
_DATA_TERMS: Final[frozenset[str]] = frozenset(
    {"not", "notlar", "notlari", "notunu", "karne", "devamsiz", "yoklama"}
)
_SELF_REF: Final[frozenset[str]] = frozenset({"benim", "kendi", "kendimin"})

MAX_MESSAGE_LEN: Final[int] = 2000


# --- Yardımcılar -------------------------------------------------------------
def _matched_root(tokens: list[str], roots: frozenset[str]) -> str | None:
    """Kök eşleşmesi. Kısa kökler (<5 harf) yanlış-pozitife açık olduğundan yalnız
    TAM eşleşir; uzun kökler çekim için önek eşleşir ('aptalsın' <- 'aptal')."""

    for tok in tokens:
        for root in roots:
            if tok == root:
                return root
            if len(root) >= 5 and tok.startswith(root):
                return root
    return None


def _contains_any(normalized: str, patterns) -> str | None:
    for pat in patterns:
        if pat in normalized:
            return pat
    return None


def _matched_harm(tokens: list[str], joined: str) -> str | None:
    """Zarar eylemi eşleşmesi. Tek-kelime kökler token bazlı; çok-kelimeli ifadeler
    ('yok edilmeli') token-token eşleşmediğinden birleşik metinde aranır."""

    hit = _matched_root(tokens, _HARM_WORDS)
    if hit:
        return hit
    return _contains_any(joined, [w for w in _HARM_WORDS if " " in w])


def _has_letter_spacing(message: str) -> bool:
    """Harf-harf yazım (>=3 ardışık tek harf) — kasıtlı kaçırma sinyali."""

    raw = re.findall(r"[a-z0-9]+", safety_normalize(message))
    run = 0
    for tok in raw:
        if len(tok) == 1 and tok.isalpha():
            run += 1
            if run >= 3:
                return True
        else:
            run = 0
    return False


def _has_studly_caps(message: str) -> bool:
    """Kelime-içi rastgele büyük/küçük harf ('AhMeT', 'sAlAk') — kasıtlı kaçırma sinyali.

    İlk harften SONRA büyük harf içeren karışık-kasa kelimeler. Normal yazım
    ('Ahmet') ve tümü-büyük ('SALAK') tetiklemez; yalnızca 'studly caps' evasion.
    Bu sinyal yalnız bir hakaret zaten tespit edildiğinde değerlendirilir, o yüzden
    'iPhone' gibi masum kelimeler tek başına bir şeyi bloklamaz.
    """

    for word in re.findall(r"[A-Za-zÇĞİÖŞÜçğıöşü]{3,}", message):
        has_lower = any(c.islower() for c in word)
        upper_after_first = any(c.isupper() for c in word[1:])
        if has_lower and upper_after_first:
            return True
    return False


_POSSESSIVE_NAME_RE: Final[re.Pattern[str]] = re.compile(
    r"\b[A-ZÇĞİÖŞÜ][a-zçğıöşü]{2,}(?:['’]\w+|nin|nın|nun|nün|['’]?in|['’]?ın)\b"
)


def _has_possessive_name(message: str) -> bool:
    """Orijinal mesajda iyelik ekli özel isim var mı? ('Ali'nin', 'Ahmet'in')."""

    for m in _POSSESSIVE_NAME_RE.finditer(message):
        base = re.match(r"[A-ZÇĞİÖŞÜ][a-zçğıöşü]{2,}", m.group(0))
        if base:
            folded = fold_accents(turkish_lower(base.group(0)))
            if folded not in _COMMON_TITLE and folded not in _SYSTEM_TERMS:
                return True
    return False


def _has_proper_name(message: str) -> bool:
    """Orijinal mesajda özel isim var mı?

    Yanlış-pozitifi azaltmak için ortak/alan kelimeleri ('Ders', 'Karne', 'Sınav'...)
    isim sayılmaz — bunları domain söz varlığından ve _COMMON_TITLE'dan eliyoruz.
    """

    from ..domain import get_domain_vocab

    excluded = _COMMON_TITLE | _SYSTEM_TERMS | get_domain_vocab()
    for raw in re.findall(r"\b[\wçğıöşüÇĞİÖŞÜ']+\b", message):
        core = raw.split("'")[0]
        if re.match(r"^[A-ZÇĞİÖŞÜ][a-zçğıöşü]{2,}$", core):
            folded = fold_accents(turkish_lower(core))
            if folded not in excluded:
                return True
    return False


# --- Giriş güvenliği ---------------------------------------------------------
def evaluate_input(message: str, role: str = "ziyaretci", authenticated: bool = False) -> SafetyDecision:
    """Kullanıcı mesajını içerik güvenliği açısından değerlendirir."""

    normalized = safety_normalize(message)
    tokens = safety_tokens(message)
    joined = " ".join(tokens)

    # 0) Spam: aşırı uzunluk.
    if len(message) > MAX_MESSAGE_LEN:
        return _make(TEMPORARY_LIMIT, "SPAM_LENGTH", 2, "SAFE-SPAM-001",
                     "Mesaj çok uzun. Lütfen daha kısa bir mesaj gönder.")

    # 1) Prompt injection / manipülasyon.
    hit = _contains_any(joined, _INJECTION_PATTERNS) or _contains_any(normalized, _INJECTION_PATTERNS)
    if hit:
        return _make(BLOCK, "PROMPT_INJECTION", 3, "SAFE-INJECT-001",
                     "Bu istek işlenemez. Yalnızca Hezarfen kullanımıyla ilgili sorulara yardımcı olabilirim.",
                     matched=[hit])

    # 2) Kendine zarar (küfürden ÖNCE; cezalandırıcı değil, destekleyici).
    hit = _contains_any(joined, _SELF_HARM_PATTERNS) or _contains_any(normalized, _SELF_HARM_PATTERNS)
    if hit:
        return _make(SAFE_RESPONSE, "SELF_HARM", 4, "SAFE-SELFHARM-001",
                     "Böyle hissetmen çok zor olmalı ve yalnız değilsin. Lütfen güvendiğin bir "
                     "yetişkinle, rehber öğretmeninle konuş. Türkiye'de acil destek için 182'yi "
                     "arayabilir ya da acil bir durumda 112'ye ulaşabilirsin.",
                     review=True, matched=[hit])

    # 3) Tehdit / şiddet.
    hit = _contains_any(joined, _THREAT_PATTERNS) or _contains_any(normalized, _THREAT_PATTERNS)
    if hit:
        return _make(ESCALATE_TO_HUMAN, "THREAT", 5, "SAFE-THREAT-001",
                     "Bu mesaj güvenlik açısından incelenmek üzere yetkili personele iletildi.",
                     review=True, matched=[hit])

    # 4) Cinsel içerik / çocuk güvenliği.
    sexual = _matched_root(tokens, _SEXUAL_TERMS)
    if sexual:
        minor = _matched_root(tokens, _MINOR_TERMS)
        if minor:
            return _make(BLOCK, "CHILD_SAFETY", 5, "SAFE-CHILD-001",
                         "Bu içerik engellendi ve incelenmek üzere işaretlendi.",
                         review=True, matched=[sexual, minor])
        return _make(BLOCK, "SEXUAL_CONTENT", 4, "SAFE-SEXUAL-001",
                     "Bu içerik bu platformda uygun değil ve engellendi.", matched=[sexual])

    # 5) Nefret söylemi: grup terimi + zarar eylemi.
    group = _matched_root(tokens, _HATE_GROUP_TERMS)
    if group and _matched_harm(tokens, joined):
        return _make(BLOCK, "HATE_SPEECH", 5, "SAFE-HATE-001",
                     "Bu içerik nefret söylemi içeriyor ve engellendi.", review=True, matched=[group])

    # 6) Küfür / hakaret (hedef-farkında).
    insult = _matched_root(tokens, MILD_INSULTS)
    profanity = _matched_root(tokens, STRONG_PROFANITY)
    if insult or profanity:
        # Eğitim/alıntı bağlamı -> izin.
        educational = any(m in tokens for m in _EDU_MARKERS) or "'" in message or '"' in message
        if educational:
            return _make(ALLOW, "PROFANITY_EDUCATIONAL", 0, "SAFE-PROF-000",
                         "", matched=[insult or profanity])

        system_target = any(t in _SYSTEM_TERMS for t in tokens)
        person_target = (
            any(t in _ROLE_TARGETS for t in tokens)
            or _has_proper_name(message)
            or _has_letter_spacing(message)   # kasıtlı harf-aralama gizlemesi
            or _has_studly_caps(message)      # 'AhMeT sAlAk' gibi karışık-kasa kaçırma
        )

        if person_target:
            sev = 4 if profanity else 3
            return _make(BLOCK, "TARGETED_HARASSMENT", sev, "SAFE-HARASS-001",
                         "Bu içerik başka bir kişiye yönelik hakaret içeriyor ve engellendi.",
                         matched=[profanity or insult])
        if system_target and not profanity:
            # Sistem eleştirisi -> izin.
            return _make(ALLOW, "SYSTEM_CRITICISM", 1, "SAFE-CRIT-001", "",
                         matched=[insult])
        # Bota yönelik veya hedefsiz -> uyar, yine de yardım et.
        return _make(ALLOW_WITH_WARNING, "PROFANITY_UNTARGETED", 2, "SAFE-PROF-001",
                     "Sana yardımcı olmak isterim; lütfen daha kibar bir dil kullanır mısın?",
                     matched=[profanity or insult])

    # 7) Başkasının kişisel verisi (isimli talep) -> yetki gerekir.
    # İYELİK EKLİ isim aranır ('Ali'nin notları'); 'Bir öğrencinin' / 'Yeni not'
    # gibi masum how-to soruları yanlışlıkla engellenmesin.
    if _matched_root(tokens, _DATA_TERMS) and not any(t in _SELF_REF for t in tokens):
        if _has_possessive_name(message):
            return _make(REQUIRE_AUTHORIZATION, "OTHER_PERSON_DATA", 3, "SAFE-AUTHZ-001",
                         "Başka bir kişinin bilgilerini gösteremem. Yalnızca kendi bilgilerine erişebilirsin.")

    # 8) PII -> maskele ve devam et.
    masked, found = mask_pii(message)
    if found:
        return _make(MASK_AND_ALLOW, "PII", 1, "SAFE-PII-001",
                     "", masked=masked, matched=tuple(found))

    return _make(ALLOW, "CLEAN", 0, "SAFE-OK-000", "")


# --- Çıktı güvenliği ---------------------------------------------------------
def evaluate_output(text: str) -> SafetyDecision:
    """Chatbot cevabını gönderilmeden önce kontrol eder (PII/token/küfür sızıntısı)."""

    tokens = safety_tokens(text)
    leak = _matched_root(tokens, STRONG_PROFANITY) or _matched_root(tokens, MILD_INSULTS)
    if leak:
        return _make(BLOCK, "OUTPUT_PROFANITY", 3, "SAFE-OUT-001",
                     "Cevap güvenlik kontrolünden geçemedi.", matched=[leak])
    masked, found = mask_pii(text)
    if found:
        return _make(MASK_AND_ALLOW, "OUTPUT_PII", 2, "SAFE-OUT-002",
                     "", masked=masked, matched=tuple(found))
    return _make(ALLOW, "CLEAN", 0, "SAFE-OUT-000", "")
