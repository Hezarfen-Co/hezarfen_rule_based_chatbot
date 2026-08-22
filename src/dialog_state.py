"""Hafif diyalog-durumu (dialog-state) — çok-turlu takip için.

İLKE (asla yanlış): durum yalnızca ZATEN sunulmuş bir netleştirmeyi/bağlamı ÇÖZER;
asla yeni bilgi uydurmaz. Çözülemezse motorun mevcut clarify davranışı sürer.

Durum, motorda `session.user_id` ile anahtarlanır (üretimde her kullanıcı ayrı;
user_id yoksa durum tutulmaz -> stateless, paylaşılan motorda sızıntı olmaz).
Çözülen takip, ilgili intent'in KANONİK sorgusuna çevrilip normal boru hattından
geçirilir (rol-gating/nav/güvenlik aynen uygulanır).
"""

from __future__ import annotations

from dataclasses import dataclass

from .catalog import get_intent
from .normalize import folded_tokens


@dataclass
class DialogState:
    last_intent: str | None = None
    last_topic: str | None = None
    offered: tuple[str, ...] = ()   # son clarify'da sunulan aday intent id'leri
    last_query: str | None = None


# intent -> kaba konu (takip çözümü için).
_MARKS = {"report_card_view", "student_marks_lookup", "weighted_average_info"}
_NAV = {"guide_info", "navigation_help", "nav_overview", "help_capabilities"}
_EXAM = {"exam_enter_room", "exam_create", "exam_finish_result",
         "exam_modes_info", "exam_rejoin_retake", "exam_schedule_info"}
_ATT = {"attendance_view", "student_attendance_lookup", "attendance_rate_info"}


def topic_of(intent: str | None) -> str | None:
    if intent in _MARKS:
        return "marks"
    if intent in _NAV:
        return "nav"
    if intent in _EXAM:
        return "exam"
    if intent in _ATT:
        return "attendance"
    return intent


# Çözülen intent -> onu tetikleyen KANONİK sorgu (doğrulanmış). Yoksa intent'in ilk
# örnek sorusu kullanılır (genel yedek).
_CANONICAL: dict[str, str] = {
    "report_card_view": "karnemi nasıl görürüm",
    "student_marks_lookup": "öğrencinin notuna nasıl bakarım",
    "navigation_help": "menüde bulamıyorum",
    "exam_enter_room": "sınava nasıl girerim",
    "attendance_view": "devamsızlığımı nasıl görürüm",
    "guide_info": "rehber sayfası nerede",
    "help_capabilities": "neler yapabilirsin",
}


def canonical_query(intent: str) -> str | None:
    if intent in _CANONICAL:
        return _CANONICAL[intent]
    info = get_intent(intent)
    ex = info.get("example_questions") if info else None
    return ex[0] if ex else None


_ORDINAL_0 = {"ilk", "ilki", "ilkini", "birinci", "birincisi", "evet", "ilkin"}
_ORDINAL_1 = {"ikinci", "ikincisi", "ikincini", "digeri", "sonraki"}
_ORDINAL_2 = {"ucuncu", "ucuncusu"}
_CONT_PHRASES = ("peki sonra", "sonra ne", "ondan sonra", "sonrasinda", "daha sonra",
                 "baska ne", "devaminda")
_CONT_WORDS = {"peki", "sonra", "devam", "baska", "e"}
_COMPLAINT = ("orada yok", "burada yok", "bulamad", "goremiyor", "gorunmuyor",
              "cikmiyor", "gozukmuyor", "erisemiyor", "gorunmez", "goremedim")
_QWORDS = {"nerede", "nereden", "nasil", "nedir", "ne", "hangi", "kac", "neden", "kim"}


def resolve(prior: DialogState | None, query: str, role: str,
            rule_hit: bool) -> str | None:
    """Takip turunu önceki duruma göre çöz -> intent id (yoksa None).

    `rule_hit`: sorgu kendi başına bir kurala çarpıyor mu (çarpıyorsa yeni bir
    komuttur, slot-doldurma sayılmaz)."""

    if prior is None:
        return None
    toks = folded_tokens(query)
    if not toks:
        return None
    low = " ".join(toks)
    tokset = set(toks)

    # 1) Netleştirme sonrası onay/sıra ("evet", "ilki", "ikincisi").
    if prior.offered and len(toks) <= 4:
        idx = None
        if tokset & _ORDINAL_0:
            idx = 0
        elif tokset & _ORDINAL_1:
            idx = 1
        elif tokset & _ORDINAL_2:
            idx = 2
        if idx is not None and idx < len(prior.offered):
            return prior.offered[idx]

    # 2) Devam ("peki sonra?", "başka?") -> önceki intent'i sürdür.
    if prior.last_intent and len(toks) <= 3 and (
        low in _CONT_WORDS or any(p in low for p in _CONT_PHRASES)
    ):
        return prior.last_intent

    # 3) Navigasyon/rehber sonrası itiraz ("orada yok", "bulamadım") -> nav yardımı.
    if prior.last_topic == "nav" and len(toks) <= 4 and (
        low == "yok" or any(p in low for p in _COMPLAINT)
    ):
        return "navigation_help"

    # 4) Not/karne bağlamından sonra çıplak ad/slot ("Ahmet." / "Ali, Matematik
    #    dersi.") -> öğretmen+ ise öğrenci-notu sorgusu, aksi halde kendi karnesi.
    if (prior.last_topic == "marks" and not rule_hit and 0 < len(toks) <= 5
            and not (tokset & _QWORDS)
            and low != "yok" and not any(p in low for p in _COMPLAINT)):
        if role in ("ogretmen", "yonetici", "admin"):
            return "student_marks_lookup"
        return "report_card_view"

    return None


def next_state(prior: DialogState | None, query: str, result: dict) -> DialogState:
    """Bir turdan sonra yeni durumu üretir (sonraki tur için)."""

    intent = result.get("intent")
    rid = result.get("response_id")
    offered: tuple[str, ...] = ()
    if rid == "clarification_prompt":
        cl = result.get("clarification") or {}
        offered = tuple(
            c["intent"] for c in cl.get("candidates", [])
            if isinstance(c, dict) and c.get("intent")
        )
    if intent is not None:
        topic = topic_of(intent)
    elif offered:
        topic = topic_of(offered[0])
    else:
        topic = prior.last_topic if prior else None
    return DialogState(last_intent=intent, last_topic=topic,
                       offered=offered, last_query=query)
