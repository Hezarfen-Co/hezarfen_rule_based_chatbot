"""Kural katmanı: yüksek-kesinlik, deterministik intent eşleşmesi.

Felsefe: Bu katman HER soruyu kapsamaz; yalnızca anahtar kelimesi TEK ANLAMLI
olan (ve özellikle güvenlik açısından kritik) soruları deterministik olarak
bağlar. Belirsizlikte (birden çok intent eşit güçle eşleşirse) bilerek KARAR
VERMEZ (None döner) ve kararı benzerlik katmanına bırakır. Amaç coverage değil,
kapsanan sorularda ~%100 kesinliktir.

Eşleşme tabanı: `normalize.folded_tokens` (küçük harf + aksan katlama, STEM YOK) +
ÖNEK karşılaştırması. Stemmer bilinçli olarak KULLANILMAZ; çünkü kök bulma
'yapamıyor' -> 'yap' gibi kelimeleri çökertip kesinliği bozar. Önek eşleşmesi
Türkçe çekimi ('şifre' <- 'şifremi') çökertmeden yakalar.

Kural grubu (group):
    {"all": [kelime, ...], "none": [kelime, ...]?}
Grup eşleşir <=> "all" içindeki her kelime soruda VAR ve "none" içindeki hiçbir
kelime soruda YOK. Bir intent'in grupları OR ile birleşir; grup büyüklüğü (all
uzunluğu) o eşleşmenin "özgüllük skoru"dur — belirsizlik çözümünde kullanılır.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Final

from .normalize import fold_accents, folded_tokens, normalize


# Ham (Türkçe) kelimelerle yazılmış kurallar; yüklemede katlanmış köke indirgenir.
_RAW_RULES: Final[list[dict[str, Any]]] = [
    {"intent": "greeting", "groups": [
        {"all": ["merhaba"]}, {"all": ["selam"]}, {"all": ["günaydın"]},
        {"all": ["hey"]}, {"all": ["iyi", "günler"]},
    ]},
    {"intent": "smalltalk", "groups": [
        {"all": ["naber"]}, {"all": ["nasılsın"]}, {"all": ["napıyorsun"]},
        {"all": ["ne", "haber"]}, {"all": ["keyifler"]},
    ]},
    {"intent": "thanks", "groups": [
        {"all": ["teşekkür"]}, {"all": ["sağol"]}, {"all": ["sağ", "ol"]},
        {"all": ["eyvallah"]},
    ]},
    {"intent": "farewell", "groups": [
        {"all": ["görüşürüz"]}, {"all": ["hoşça"]}, {"all": ["hoşçakal"]},
        {"all": ["iyi", "gece"]},
    ]},
    {"intent": "bot_identity", "groups": [
        {"all": ["kimsin"]}, {"all": ["robot"]}, {"all": ["yapay", "zeka"]},
        {"all": ["adın", "ne"]}, {"all": ["kim", "yaptı", "seni"]},
    ]},
    {"intent": "platform_info", "groups": [
        # 'Hezarfen nedir' + sık yazım hatası 'hazerfen'. Salt 'hezarfen' KULLANILMAZ
        # (çünkü 'hezarfen'de sınav oluştur' gibi sorularda da geçer) — 'ne/nedir'
        # veya 'tanıt' ile birlikte istenir. 'hazerfen' yanlış-yazımı tek başına yeter.
        {"all": ["hezarfen", "nedir"]}, {"all": ["hezarfen", "ne"]},
        {"all": ["hezarfen", "tanıt"]}, {"all": ["hazerfen"]},
        {"all": ["bu", "site", "nedir"]}, {"all": ["bu", "uygulama", "nedir"]},
        {"all": ["bu", "platform"]},
    ]},
    {"intent": "help_capabilities", "groups": [
        {"all": ["neler", "yapabil"], "none": ["yönetici", "öğretmen", "rol", "yetki"]},
        {"all": ["ne", "yapabil"], "none": ["yönetici", "öğretmen", "rol", "yetki"]},
        {"all": ["özellik"]},
        {"all": ["yardım", "edebil"]},
    ]},
    {"intent": "roles_permissions", "groups": [
        {"all": ["yönetici", "yapabil"]}, {"all": ["öğretmen", "yapabil"]},
        {"all": ["rol", "kademe"]}, {"all": ["yetki", "seviye"]},
        {"all": ["rol", "nedir"]}, {"all": ["kim", "yetki"]},
        # 'Rolüm ne?' — kendi rolünü sorma ('rolümü değiştir' user_role_change'in
        # 2'lik kuralına takılır, o kazanır).
        {"all": ["rolüm"]},
    ]},
    {"intent": "privacy_security", "groups": [
        {"all": ["arkadaş"]}, {"all": ["başka", "öğrenci"]},
        {"all": ["başka", "öğretmen"]}, {"all": ["başka", "birinin"]},
        {"all": ["başka", "karne"]}, {"all": ["başka", "telefon"]},
        {"all": ["öğretmen", "telefon"]}, {"all": ["herkes", "not"]},
        {"all": ["birinin", "karne"]},
    ]},
    {"intent": "account_access_problem", "groups": [
        {"all": ["şifre", "unut"]}, {"all": ["şifre", "yanlış"]},
        {"all": ["şifre", "sıfırla"]}, {"all": ["parola", "unut"]},
        {"all": ["parola", "hatırla"]}, {"all": ["giremiyor"]},
        {"all": ["yapamıyor"]}, {"all": ["erişemiyor"]},
    ]},
    {"intent": "login_how", "groups": [
        {"all": ["giriş", "yap"], "none": ["yapamıyor", "giremiyor", "mesai"]},
        {"all": ["log", "in"]},
    ]},
    {"intent": "logout_how", "groups": [
        {"all": ["oturum", "kapat"]}, {"all": ["sistemden", "çık"]},
        {"all": ["hesap", "çık"]},
    ]},
    {"intent": "session_info", "groups": [
        {"all": ["oturum", "süre"]}, {"all": ["kaç", "gün", "geçerli"]},
    ]},
    {"intent": "report_card_view", "groups": [
        {"all": ["karne"], "none": ["öğrenci", "başka", "birinin"]},
        {"all": ["harf", "not"]},
    ]},
    {"intent": "weighted_average_info", "groups": [
        {"all": ["ortalama", "hesap"]}, {"all": ["ağırlık", "ortalama"]},
        {"all": ["ağırlıklı", "ortalama"]},
    ]},
    {"intent": "student_marks_lookup", "groups": [
        # 'başka/birinin' varsa bu meşru bir öğretmen sorgusu değil, gizlilik
        # sorusudur ('başka bir öğrencinin notunu görebilir miyim') -> privacy'ye bırak.
        {"all": ["öğrenci", "karne"], "none": ["başka", "birinin"]},
        {"all": ["öğrenci", "not", "gör"], "none": ["başka", "birinin"]},
        {"all": ["öğrenci", "not", "sorgu"], "none": ["başka", "birinin"]},
        {"all": ["öğrenci", "not", "bak"], "none": ["başka", "birinin"]},
    ]},
    {"intent": "note_create", "groups": [
        {"all": ["defter"]}, {"all": ["yeni", "not"]}, {"all": ["not", "oluştur"]},
    ]},
    {"intent": "course_create", "groups": [
        {"all": ["yeni", "ders"], "none": ["saat", "oturum", "sınav"]},
        {"all": ["ders", "oluştur"], "none": ["saat", "oturum", "sınav"]},
        {"all": ["ders", "aç"], "none": ["saat", "oturum", "sınav"]},
        {"all": ["sınıf", "oluştur"]},
    ]},
    {"intent": "lesson_session_add", "groups": [
        {"all": ["oturum", "ekle"]}, {"all": ["oturum", "oluştur"]},
        {"all": ["ders", "oturum"]},
        {"all": ["ders", "saat"], "none": ["var", "yok", "yoklama", "işaretle"]},
    ]},
    {"intent": "roll_call", "groups": [
        {"all": ["yoklama", "al"]}, {"all": ["yoklama", "kaydet"]},
        {"all": ["devam", "kontrol"]},
    ]},
    {"intent": "exam_create", "groups": [
        {"all": ["sınav", "oluştur"]}, {"all": ["yeni", "sınav"]},
        {"all": ["sınav", "hazırla"]}, {"all": ["yazılı", "oluştur"]},
    ]},
    {"intent": "exam_add_question", "groups": [
        {"all": ["soru", "ekle"]}, {"all": ["soru", "oluştur"]},
        {"all": ["seçmeli", "soru"]},
    ]},
    {"intent": "exam_grade_student", "groups": [
        {"all": ["öğrenci", "not", "gir"]}, {"all": ["notlandır"]},
        {"all": ["sınav", "puanla"]},
    ]},
    {"intent": "event_create", "groups": [
        {"all": ["etkinlik", "oluştur"]}, {"all": ["etkinlik", "ekle"]},
        {"all": ["etkinlik", "planla"]},
    ]},
    {"intent": "user_role_change", "groups": [
        {"all": ["rol", "değiştir"]}, {"all": ["rol", "ata"]},
        {"all": ["yetki", "yükselt"]}, {"all": ["kullanıcı", "rol"]},
    ]},
    {"intent": "term_manage", "groups": [
        {"all": ["dönem", "oluştur"]}, {"all": ["akademik", "dönem"]},
        {"all": ["yarıyıl"]},
    ]},
    {"intent": "school_settings", "groups": [
        {"all": ["okul", "ayar"]}, {"all": ["not", "bant"]},
        {"all": ["sınav", "tür", "ağırlık"]},
    ]},
    {"intent": "work_checkin_out", "groups": [
        {"all": ["mesai", "giriş"]}, {"all": ["mesai", "çık"]},
        {"all": ["işe", "gel"]},
    ]},
    # --- Aşama 11: kapsamı olmayan/karışan intent'ler için hedefli kurallar ---
    {"intent": "guide_info", "groups": [
        {"all": ["kılavuz"]}, {"all": ["guide"]}, {"all": ["adım", "tanıtım"]},
    ]},
    {"intent": "register_how", "groups": [
        {"all": ["üye", "ol"]}, {"all": ["kayıt", "ol"]},
        {"all": ["kayıt", "form"]}, {"all": ["hesap", "aç"]},
    ]},
    {"intent": "profile_edit", "groups": [
        {"all": ["iletişim", "bilgi", "değiştir"]},
        {"all": ["ad", "soyad", "güncelle"]},
        {"all": ["telefon", "değiştir"]},
    ]},
    {"intent": "attendance_view", "groups": [
        {"all": ["devamsızlık", "gör"]}, {"all": ["devamsızlık", "durum"]},
        {"all": ["yoklama", "geçmiş"]}, {"all": ["devam", "yüzde"]},
    ]},
    {"intent": "student_attendance_lookup", "groups": [
        {"all": ["öğrenci", "yoklama"]}, {"all": ["öğrenci", "devamsızlık"]},
        {"all": ["öğrenci", "devam", "durum"]},
    ]},
    {"intent": "event_attendance_mark", "groups": [
        {"all": ["etkinlik", "katıl"]}, {"all": ["etkinlik", "yoklama"]},
    ]},
    # --- Backend v2: pomodoro / mesajlar / etüt-kulüp / veli ---
    {"intent": "pomodoro_use", "groups": [
        # 'odağı' çekiminde ünsüz yumuşar (k->ğ); iki kök de tanınır.
        {"all": ["pomodoro"], "none": ["öğrenci"]},
        {"all": ["odak", "başlat"]}, {"all": ["odağ", "başlat"]},
        {"all": ["odak", "bitir"]}, {"all": ["odağ", "bitir"]},
        {"all": ["odak", "oturum"], "none": ["öğrenci"]},
    ]},
    {"intent": "student_pomodoro_lookup", "groups": [
        {"all": ["öğrenci", "pomodoro"]}, {"all": ["öğrenci", "odak"]},
        {"all": ["öğrenci", "odağ"]},
    ]},
    {"intent": "messages_use", "groups": [
        {"all": ["mesaj"]}, {"all": ["gelen", "kutusu"]},
    ]},
    {"intent": "study_club_info", "groups": [
        # 'etüde/kulübe' çekimlerinde ünsüz yumuşar (t->d, p->b); iki kök de tanınır.
        {"all": ["etüt"]}, {"all": ["etüd"]},
        {"all": ["kulüp"]}, {"all": ["kulüb"]},
    ]},
    {"intent": "parent_info", "groups": [
        {"all": ["veli"]}, {"all": ["ebeveyn"]},
    ]},
]


def _kw_of(word: str) -> str:
    """Ham kelimeyi katlanmış (ascii, stem YOK) forma indirger."""

    return fold_accents(normalize(word)).replace(" ", "")


@dataclass(frozen=True)
class _Group:
    all_kw: tuple[str, ...]
    none_kw: tuple[str, ...] = ()


@dataclass(frozen=True)
class _Rule:
    intent: str
    groups: tuple[_Group, ...]


def _compile_rules(raw_rules: list[dict[str, Any]]) -> list[_Rule]:
    compiled: list[_Rule] = []
    for raw in raw_rules:
        groups = tuple(
            _Group(
                all_kw=tuple(_kw_of(w) for w in group["all"]),
                none_kw=tuple(_kw_of(w) for w in group.get("none", ())),
            )
            for group in raw["groups"]
        )
        compiled.append(_Rule(intent=raw["intent"], groups=groups))
    return compiled


_RULES: Final[list[_Rule]] = _compile_rules(_RAW_RULES)


@dataclass(frozen=True)
class RuleMatch:
    """Kural katmanının kararı."""

    intent: str
    score: int
    matched: tuple[str, ...]
    reason: str


def _present(keyword: str, tokens: list[str]) -> bool:
    """Anahtar kelime soruda var mı? (>=2 harf önek, aksi hâlde tam eşleşme)."""

    if len(keyword) >= 2:
        return any(token.startswith(keyword) for token in tokens)
    return any(token == keyword for token in tokens)


def _group_matches(group: _Group, tokens: list[str]) -> bool:
    if any(not _present(k, tokens) for k in group.all_kw):
        return False
    if any(_present(k, tokens) for k in group.none_kw):
        return False
    return True


def match(query: str) -> RuleMatch | None:
    """Soruyu kural katmanından geçirir.

    Returns:
        Tek bir intent en yüksek özgüllükle eşleşirse RuleMatch; hiçbir kural
        eşleşmezse veya birden çok intent aynı en yüksek skorda eşleşirse (belirsiz)
        None.
    """

    tokens = folded_tokens(query)
    if not tokens:
        return None

    best_by_intent: dict[str, tuple[int, tuple[str, ...]]] = {}
    for rule in _RULES:
        for group in rule.groups:
            if _group_matches(group, tokens):
                score = len(group.all_kw)
                prev = best_by_intent.get(rule.intent)
                if prev is None or score > prev[0]:
                    best_by_intent[rule.intent] = (score, group.all_kw)

    if not best_by_intent:
        return None

    ranked = sorted(best_by_intent.items(), key=lambda kv: kv[1][0], reverse=True)
    top_intent, (top_score, matched) = ranked[0]

    # Belirsizlik: aynı en yüksek skorda birden çok intent -> karar verme.
    if len(ranked) > 1 and ranked[1][1][0] == top_score:
        return None

    return RuleMatch(
        intent=top_intent,
        score=top_score,
        matched=matched,
        reason=f"kural: {top_intent} <- {list(matched)}",
    )
