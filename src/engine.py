"""Backend servis + front/back sözleşmesi.

Motoru net bir istek/yanıt sözleşmesiyle sarar. Frontend (terminal, web vb.)
yalnızca bu sözleşme üzerinden konuşur; iç katmanları (kural/benzerlik/karar)
bilmez. Loglama backend'de yapılır (isteğe bağlı log_sink).

İstek (payload):
    {
      "query": str,                       # zorunlu
      "session": {"role": str, "authenticated": bool},  # isteğe bağlı
      "trace_id": str                     # isteğe bağlı (yoksa üretilir)
    }

Yanıt:
    {
      "trace_id": str,
      "response_id": str,
      "text": str,
      "intent": str | None,
      "confidence": float,
      "fallback": bool,
      "auth_action": str | None,          # None | "login_required" | "role_insufficient"
      "required_role": str | None
    }
"""

from __future__ import annotations

import re
from typing import Any, Callable

from . import dialog_state
from . import rules
from . import safety as safety_mod
from .catalog import (
    FALLBACK,
    ROLE_ALIASES,
    ROLE_HIERARCHY,
    capabilities_for,
    get_intent,
    route_for,
    suggestions_for,
)
from .access import AccessOutcome
from .normalize import folded_tokens
from .observability import new_trace_id, process
from .role_spaces import get_role_space

# Rol beyanını ("ben öğrenciyim") gerçek sorudan ayırmak için yok sayılan doldurma
# kelimeleri. Bunlar dışındaki her kelime rol kelimesi değilse -> beyan sayılmaz.
_ROLE_DECL_FILLER: frozenset[str] = frozenset(
    {"ben", "benim", "bir", "rol", "rolum", "rolumu", "olarak", "ya", "de", "da", "peki"}
)

# İlk iki aday bu farktan yakınsa sistem "emin değil" -> netleştirme adayları sun.
# (Yalnızca benzerlik kararlarında; kural kararları yüksek-kesinlik olduğundan muaf.)
CLARIFY_MARGIN: float = 0.08

# Benzerlik güveni bunun ALTINDAYSA tam cevap VERİLMEZ: "anlayamadım, bunu mu
# demek istedin?" + adaylar döner. Eşik (0.18) ile bu değer arası "belirsiz bölge"dir
# — yanlış-ama-özgüvenli cevap, dürüst soru sormaktan kötüdür.
ASK_CONFIDENCE: float = 0.30

# İkinci "emin değilim" tetikleyicisi: güven orta-düşük VE ilk iki aday neredeyse
# berabere (top1 ~ top2). "ben kimim" gibi kapsam-dışı/gürültü sorgularında sistem
# iki intent arasında bölünüp yanlış-ama-özgüvenli cevap verirdi; bunun yerine
# netleştirme sorar. Benchmark ölçümü: yalnız ~5 doğru cevabı netleştirmeye çevirir,
# buna karşılık düşük-güven+düşük-margin bölgesindeki özgüvenli-yanlışları önler.
# (Metrikler etkilenmez: evaluate karar katmanını ölçer, bu sunum katmanıdır.)
ASK_LOW_MARGIN_CONFIDENCE: float = 0.45
ASK_LOW_MARGIN: float = 0.05
# Top-1 ile Top-2 neredeyse EŞİTse (fark bu değerin altında) model iki intent'i
# ayıramıyor demektir -> yüksek skor olsa bile tam cevap verme, netleştir (asla
# yanlış). Yakın-eş yanlış cevabı önler (kullanıcının 'top1-top2 skor farkı' yöntemi).
ASK_TIE_MARGIN: float = 0.02
# Okul-dışı, net kapsam-dışı konu kelimeleri (FOLD edilmiş). Yalnızca KURAL
# çarpmayıp benzerlik zayıf-eşleşme verdiğinde (ör. 'öğretmenime hediye ne alayım'
# -> messages_use FP) netleştirmeye zorlar. Kısa ve gerçekten alan-dışı tutulur;
# okul terimleriyle çakışmaz. Kalıcı çözüm: gömme-tabanlı OOS (bkz. kriterler.md).
_FAR_OOS_TOPICS: frozenset[str] = frozenset({
    "hediye", "diyet", "kilo", "burc", "fal", "kripto", "bitcoin", "tarif",
    "siir", "fikra", "mac", "sevgili", "flort",
})

# Düşük-margin "emin değilim" YALNIZCA ilk iki aday da sosyal/meta intent iken
# tetiklenir ('ben kimim' -> farewell ~ bot_identity, gerçek görev yok). Görev
# intent'lerinde (report_card_view vb.) doğru-ama-düşük-güvenli bir cevabı
# netleştirmeye çevirip kurban etmesin.
_SOCIAL_INTENTS: frozenset = frozenset(
    {"greeting", "smalltalk", "farewell", "thanks", "bot_identity"}
)

# Belirsiz bölgede kullanıcıya dönen metin (response_id: clarification_prompt).
CLARIFICATION_PROMPT_TEXT: str = (
    "Bunu tam anlayamadım, kusura bakma 🙏 Soruyu biraz daha açık yazar mısın? "
    "Ders, sınav, karne, yoklama, defter, mesaj veya hesap ayarları hakkında "
    "'nasıl yaparım?' diye sorabilirsin."
)
from .similarity import SimilarityMatcher

# İsteğe bağlı log alıcısı: bir trace sözlüğü alır (dosyaya/akışa yazmak çağıranın işi).
LogSink = Callable[[dict[str, Any]], None]


class RequestError(ValueError):
    """Geçersiz istek payload'ı."""


# Gerçek backend'in (REST API) İngilizce rol adları -> iç rol adları.
# Front/back arkadaşların oturumu 'student/teacher/manager/admin' olarak çözer;
# asistan iki adlandırmayı da kabul eder.
_ROLE_NAME_ALIASES: dict[str, str] = {
    "parent": "veli",
    "student": "ogrenci",
    "teacher": "ogretmen",
    "manager": "yonetici",
    "guest": "ziyaretci",
    "visitor": "ziyaretci",
}


def _parse_session(payload: dict[str, Any]) -> tuple[str, bool]:
    session = payload.get("session")
    if session is None:
        session = {}
    if not isinstance(session, dict):
        raise RequestError(f"session bir sözlük olmalı, {type(session).__name__} geldi.")
    role = session.get("role", "ziyaretci")
    if isinstance(role, str):
        role = _ROLE_NAME_ALIASES.get(role.lower(), role)
    # authenticated KESİN boolean olmalı: string "false" bool("false")=True ile auth
    # bypass'ı yaratmasın -> bozuk tip temiz RequestError.
    auth_raw = session.get("authenticated", role != "ziyaretci")
    if not isinstance(auth_raw, bool):
        raise RequestError("session.authenticated bir boolean olmalı.")
    authenticated = auth_raw
    if role not in ROLE_HIERARCHY:
        raise RequestError(f"Bilinmeyen rol: {role!r}")
    if role == "ziyaretci" and authenticated:
        raise RequestError("Ziyaretçi 'authenticated' olamaz.")
    # Doğrulanmamış oturum bir rolü ÜSTLENEMEZ: giriş yapılmadan öğrenci/öğretmen/
    # yönetici/admin işlem yetkisi verilmez -> etkin rol ziyaretçi (login gerekir).
    # Böylece rol adını taşıyan ama authenticated=false olan oturum, yetki kazanmaz.
    if not authenticated:
        role = "ziyaretci"
    return role, authenticated


# Çoklu-istek ayracı: 've', 'ayrıca' bağlaçları + virgül/noktalı virgül.
_MULTI_SPLIT_RE: re.Pattern[str] = re.compile(r"\s+(?:ve|ayrıca)\s+|[;,]", re.IGNORECASE)

# --- Sosyal önek soyma ------------------------------------------------------
# "Merhaba, karnemi nerede görürüm?" -> selam kısmı GÖREVİ gizlememeli. Baştaki
# yalnızca-sosyal cümlecikleri + söylem belirteçlerini soyup kalan görev cümlesini
# yönlendiririz. Kalan boşsa (saf selam/teşekkür) sorgu aynen döner -> greeting/thanks
# doğru cevaptır. Anahtarlar FOLD edilmiş (aksansız) biçimde tutulur (folded_tokens).
_SOCIAL_LEAD: frozenset[str] = frozenset({
    "merhaba", "merhabalar", "selam", "selamlar", "selamun", "aleykum", "aleykm",
    "naber", "nbr", "napiyorsun", "napiyosun", "nasilsin", "hey", "alo", "sa", "as",
    "gunaydin", "iyi", "gunler", "aksamlar", "sabahlar", "gun",
    "tesekkur", "tesekkurler", "tesekkurederim", "sagol", "sagolun", "sag", "ol",
    "eyvallah", "rica", "ederim", "etsem", "lutfen", "acaba", "pardon",
    "affedersin", "affedersiniz", "dostum", "hocam", "kanka", "kardesim", "kardes",
    "abi", "abicim", "peki", "ee", "eee", "sey", "yani", "birde", "de", "da", "bi",
})
# Token bazlı baştan-soyma için DAHA MUHAFAZAKÂR küme (tek başına anlamı görev
# olabilecek 'iyi/gunler/de/da/bi/sag/ol' hariç -> yanlış soyma yok).
_SOCIAL_LEAD_TOKEN: frozenset[str] = frozenset({
    "merhaba", "merhabalar", "selam", "selamlar", "naber", "nbr", "hey", "alo",
    "gunaydin", "tesekkur", "tesekkurler", "tesekkurederim", "sagol", "sagolun",
    "eyvallah", "rica", "etsem", "lutfen", "pardon", "affedersin", "affedersiniz",
    "dostum", "hocam", "kanka", "kardesim", "abi", "abicim", "peki", "ee", "eee",
    "sey", "yani", "acaba",
})


def _strip_social_prefix(query: str) -> str:
    """Baştaki sosyal/nezaket önekini soyup kalan görev cümlesini döndürür.

    Yalnızca sorgunun BAŞINDAki yalnızca-sosyal cümlecikleri ve söylem kelimelerini
    atar; görev kısmı hiç değiştirilmez. Kalan boşsa sorgu aynen döner.
    """

    # 1) Baştaki yalnızca-sosyal cümlecikleri (virgül/;) at.
    clauses = [c for c in re.split(r"\s*[;,]\s*", query.strip())]
    while len(clauses) > 1:
        toks = folded_tokens(clauses[0])
        if toks and all(t in _SOCIAL_LEAD for t in toks):
            clauses.pop(0)
        else:
            break
    residual = ", ".join(clauses).strip()

    # 2) Baştaki sosyal/söylem KELİMELERİNİ tek tek at; ilk görev kelimesinde dur.
    words = residual.split()
    i = 0
    while i < len(words):
        folded = folded_tokens(words[i])
        key = folded[0] if folded else ""
        if key in _SOCIAL_LEAD_TOKEN:
            i += 1
        else:
            break
    stripped = " ".join(words[i:]).strip()
    return stripped if stripped else query


def _multi_intent_segments(query: str, role: str = "ziyaretci") -> list[tuple[str, str]] | None:
    """Sorgu birden çok BAĞIMSIZ isteğe bölünüyor mu? -> [(parça, intent), ...].

    Muhafazakâr tasarım: yalnızca KURAL katmanının (yüksek kesinlik) tanıdığı
    parçalar sayılır; en az 2 FARKLI intent gerekir, en çok 3 parça yanıtlanır.
    Böylece 'roller ve yetkiler nedir' gibi doğal 've'ler bölünmez (parçalar
    kurala çarpmaz), 'sınav oluştur ve yoklama al' ise iki cevap alır.
    """

    raw_segments = [s.strip() for s in _MULTI_SPLIT_RE.split(query) if s.strip()]
    if len(raw_segments) < 2:
        return None
    hits: list[tuple[str, str]] = []
    seen: set[str] = set()
    rule_matcher = get_role_space(role).rule_matcher
    for segment in raw_segments:
        match = rule_matcher.match(segment)
        if match is not None and match.intent not in seen:
            seen.add(match.intent)
            hits.append((segment, match.intent))
    # >3 farklı işlem: tek yanıtta net anlatmak güç -> çağıran netleştirmeye düşürür
    # (asla yarım/yanlış cevap). 2-3 parça yanıtlanır. <2 -> çoklu değil (None).
    return hits if len(hits) >= 2 else None


def _declared_role(query: str) -> str | None:
    """Sorgu yalnızca bir rol beyanı mı? ('Öğrenci', 'ben öğretmenim') -> kanonik rol.

    Doldurma kelimeleri (ben, olarak...) yok sayılır; geriye kalan tüm kelimeler rol
    kelimesiyse ve en az bir rol varsa beyan kabul edilir. 'öğrenci kaydet' gibi ek
    içerikli sorgular (kaydet rol/doldurma değil) beyan SAYILMAZ -> normal boru hattı.
    """

    tokens = folded_tokens(query)
    if not tokens or len(tokens) > 4:
        return None
    found: str | None = None
    for tok in tokens:
        role = None
        for stem, canonical in ROLE_ALIASES.items():
            if tok == stem or (len(stem) >= 4 and tok.startswith(stem)):
                role = canonical
                break
        if role is not None:
            found = role
        elif tok not in _ROLE_DECL_FILLER:
            return None  # rol/doldurma olmayan bir kelime -> beyan değil
    return found


def _role_correction(query: str) -> str | None:
    """Rol DÜZELTMESİ ('Öğretmen değilim, öğrenciyim') -> onaylanan (son) rol.

    Yalnız kısa, salt rol+olumsuzluk cümlelerinde devreye girer; görev içeren
    sorgular ('öğretmen değil öğrenci kaydını sil') HARİÇ (rol/olumsuzluk/doldurma
    dışı bir kelime görülünce None). Böylece yanlış işleme YOK; kullanıcının rolünü
    bilgi olarak alır (intent None)."""

    toks = folded_tokens(query)
    if not toks or len(toks) > 6:
        return None
    if not any(t.startswith("degil") for t in toks):
        return None
    roles: list[str] = []
    for tok in toks:
        matched = None
        for stem, canonical in ROLE_ALIASES.items():
            if tok == stem or (len(stem) >= 4 and tok.startswith(stem)):
                matched = canonical
                break
        if matched is not None:
            roles.append(matched)
        elif not (tok.startswith("degil") or tok in _ROLE_DECL_FILLER):
            return None  # rol/olumsuzluk/doldurma dışı kelime -> düzeltme değil
    return roles[-1] if roles else None


# --- Olumsuzluk (negation) çözümü ------------------------------------------
# "Sınav oluşturmak istemiyorum, sınava girmek istiyorum" -> olumsuz cümleciği
# DÜŞÜR, olumlu olanı yanıtla. Saf olumsuz komut ("notlarımı gösterme") -> hiçbir
# işlem yapma, netleştir (asla yanlış). Bilinçli olarak sağlam/muhafazakâr: yalnız
# net olumsuzluk işaretlerinde devreye girer, normal sorguları etkilemez.
_NEG_MARKERS: tuple[str, ...] = (
    "istemiyorum", "istemem", "istemez", "istemedim", "istemiyor",
    "sormuyorum", "etmeyeceğim", "yapmayacağım", "vermeyeceğim", "istemiyoruz",
)
# Dar/tek-anlamlı saf-olumsuz komutlar ('notlarımı gösterme'): '-ma/-me' isim-fiil
# belirsizliği DÜŞÜK olanlar (oluşturma/ekleme gibi yaygın isim-fiiller HARİÇ) +
# soru kelimesi yoksa -> saf olumsuz kabul edilir (uygula-ma, netleştir).
_PURE_NEG_IMPERATIVES: frozenset[str] = frozenset({"gösterme", "gizleme"})
_QUESTION_WORDS: frozenset[str] = frozenset({
    "nerede", "nereden", "nasıl", "nedir", "ne", "hangi", "kaç", "mi", "mı",
    "mu", "mü", "neden", "kim", "sayfa", "var",
})


def _clause_negated(clause: str) -> bool:
    # Yalnız AÇIK/tek-anlamlı olumsuzluk işaretleri. '-ma/-me' ekli fiiller
    # (gösterme, oluşturma...) Türkçede aynı zamanda İSİM-FİİLdir (oluşturma =
    # işlemin adı); bu yüzden BİLİNÇLİ olarak KULLANILMAZ — aksi hâlde "Ders
    # oluşturma nerede?" yanlışlıkla olumsuz sayılıp netleştirmeye düşüyordu.
    low = clause.casefold()
    return any(marker in low for marker in _NEG_MARKERS)


def _resolve_negation(query: str) -> str:
    """Olumsuzluğu çöz. Döner: yanıtlanacak OLUMLU sorgu; olumsuzluk yoksa sorgu
    aynen; saf olumsuz komutta boş string ("" = uygulama, netleştir)."""

    # "A değil, B" -> son 'değil' sonrasındaki olumlu kısım.
    matches = list(re.finditer("değil", query, re.IGNORECASE))
    if matches:
        return query[matches[-1].end():].lstrip(" ,;:.-").strip()
    # Dar saf-olumsuz komut ('notlarımı gösterme') + soru kelimesi yok -> uygulama.
    low_toks = re.findall(r"[a-zçğıöşü]+", query.casefold())
    if (any(t in _PURE_NEG_IMPERATIVES for t in low_toks)
            and not any(t in _QUESTION_WORDS for t in low_toks)):
        return ""
    if not _clause_negated(query):
        return query  # olumsuzluk yok -> değişmez (normal sorgular etkilenmez)
    kept = [p.strip() for p in re.split(r"[;,]", query)
            if p.strip() and not _clause_negated(p)]
    return ", ".join(kept)


# --- Henüz canlı olmayan / bulunmayan özellikler ----------------------------
# Bu anahtarlar bir sayfaya YANLIŞ yönlendirmek yerine dürüstçe "henüz
# kullanılamıyor" der (asla yanlış). T1 (randevu/yemek/soru-havuzu/beyaz-tahta)
# canlıya alınınca ilgili anahtar bu listeden çıkarılır; duyuru diye bir özellik
# hiç yoktur.
_UNAVAILABLE_FEATURES: tuple[tuple[str, str], ...] = (
    ("randevu", "Randevular"),
    ("yemek", "Yemekler"),
    ("havuz", "Soru havuzu"),
    ("beyaz tahta", "Beyaz tahtalar"),
    ("tahta", "Beyaz tahtalar"),
    ("duyuru", "Duyurular"),
)


def _unavailable_feature(query: str) -> str | None:
    low = query.casefold()
    for keyword, label in _UNAVAILABLE_FEATURES:
        if keyword in low:
            return label
    return None


# --- Kapsam sınırı: canlı VERİ çekme isteği ---------------------------------
# Çelebi gerçek veriyi getirmez/göstermez; yalnızca "nasıl yaparım" anlatır (bkz.
# PROJECT_STATE kapsam-dışı). "Öğrenci listemi buraya getir", "toplam kaç kullanıcı
# var" gibi VERİ-çekme/sayım istekleri yanlış bir sayfaya yönlendirilmez; dürüstçe
# "gerçek veriyi getiremem, yalnızca nasıl yapılacağını anlatırım" denir (asla yanlış).
_DATA_FETCH_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"gerçek\b.*\b(getir|göster|listele|ver\b|çek)", re.IGNORECASE),
    re.compile(r"\b(buraya|bana)\s+getir", re.IGNORECASE),
    re.compile(r"liste(m|mi|sini|yi)\b.*\b(getir|çıkar|ver|göster)", re.IGNORECASE),
    re.compile(r"\btoplam\s+kaç\b", re.IGNORECASE),
    re.compile(r"\bkaç\s+(kullanıcı|öğrenci|öğretmen|kişi|veli)\b.*\bvar\b", re.IGNORECASE),
    re.compile(r"\b(sistemde|veritabanında|kayıtlı)\b.*\bkaç\b", re.IGNORECASE),
)


def _is_data_fetch_request(query: str) -> bool:
    return any(p.search(query) for p in _DATA_FETCH_PATTERNS)


# --- Kapsam sınırı: bot adına İŞ YAPMA / VERİ DEĞİŞTİRME isteği ---------------
# Çelebi ne kullanıcı adına ödev/işlem yapar ne de veriyi (not/devamsızlık/yoklama)
# değiştirir/siler; yalnızca "nasıl yaparım" anlatır. "Ödevimi sen yap", "notumu
# yükselt", "devamsızlığımı sil", "sınav cevaplarını ver" gibi manipülasyon/do-for-me
# istekleri yanlış bir sayfaya yönlendirilmez -> dürüstçe "bunu yapamam" (asla yanlış).
_MANIPULATION_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\b(yerime|yerine)\b", re.IGNORECASE),
    re.compile(r"\bsen\s+(yap|ayarla|çöz|hallet|doldur|gir|oluştur|tamamla)\b", re.IGNORECASE),
    re.compile(r"\bbenim\s+için\s+(yap|çöz|doldur|hallet|tamamla)\b", re.IGNORECASE),
    re.compile(r"(sınav|soru|test)\w*.*\bcevap\w*.*\b(ver|söyle|sızdır|göster)\b", re.IGNORECASE),
    re.compile(r"\bcevap(ları|larını|ını)\b\s*\b(ver|söyle|sızdır)\b", re.IGNORECASE),
    # 1. şahıs korunan veri + değiştirme fiili (öğrenci kendi notunu/devamsızlığını
    # değiştiremez/silemez/yükseltemez). 'göster/gör/bak' DEĞİL -> onlar meşru görüntüleme.
    re.compile(r"\b(notum|notumu|notlarım\w*|karnem|karnemi|ortalamam\w*|puanım\w*|"
               r"devamsızlığım\w*|yoklamam\w*)\b.*\b(sil|kaldır|yükselt|artır|düzelt|değiştir)\b",
               re.IGNORECASE),
    re.compile(r"\b(sil|kaldır|yükselt|artır|düzelt)\b.*\b(notum|notumu|karnem|karnemi|"
               r"devamsızlığım\w*|yoklamam\w*|puanım\w*)\b", re.IGNORECASE),
    re.compile(r"\bvar\s+göster\b", re.IGNORECASE),
)


def _is_manipulation_request(query: str) -> bool:
    return any(p.search(query) for p in _MANIPULATION_PATTERNS)


def _build_navigation(
    intent: str | None,
    auth_action: str | None,
    role: str = "ziyaretci",
) -> dict[str, Any] | None:
    """Seçilen intent için yönlendirme hedefi (route) üretir.

    Frontend bunu "Git →" butonu olarak çizer. `available`, kullanıcının rolü
    yeterliyse True'dur (yetersizse buton pasif gösterilir; neden `auth_action`'da).
    """

    if intent is None or auth_action is not None:
        return None
    view = get_role_space(role).view_for(intent)
    if view is None or view.outcome is not AccessOutcome.ALLOW:
        return None
    # Karne/yoklama sayfası öğrenciye özeldir. Üst roller `reports.read_own` ile ALLOW
    # (kapsam notu metni) alsa da kişisel /marks,/attendance butonu BASILMAZ — aksi
    # halde öğrenci-özel sayfaya giden bir nav sızar (ISO-020..023).
    if intent in {"report_card_view", "attendance_view"} and role != "ogrenci":
        return None
    # Rota, izin verilen intent'in gerçek sayfasıdır (rehber §4). Reddedilen/CLARIFY
    # görünümlerde buraya gelinmez -> ret'te rota sızmaz. Bilgi intent'lerinde
    # (route_for None) navigasyon yoktur.
    route = route_for(intent)
    if route is None:
        return None
    path, label = route
    return {"route": path, "label": label, "available": True}


_WIRE_ROLES: dict[str, str] = {
    "ziyaretci": "visitor",
    "veli": "parent",
    "ogrenci": "student",
    "ogretmen": "teacher",
    "yonetici": "manager",
    "admin": "admin",
}


def assistant_meta_from_result(result: dict[str, Any], role: str) -> dict[str, Any]:
    """Build the role-space V2 metadata from one engine result.

    The legacy engine response remains intact; bridge V2 puts this metadata next
    to ``text`` on the wire.
    """

    space = get_role_space(role)
    intent = result.get("intent")
    view = space.view_for(intent) if isinstance(intent, str) else None
    response_id = result.get("response_id")
    if response_id == "clarification_prompt":
        outcome = "clarify"
        reason_code = "ambiguous_query"
    elif bool(result.get("fallback")):
        outcome = "fallback"
        reason_code = "out_of_scope"
    elif result.get("auth_action") is not None:
        outcome = "deny"
        reason_code = view.reason_code.value if view else "role_not_permitted"
    elif isinstance(response_id, str) and response_id.startswith("safety_"):
        outcome = "deny"
        safety = result.get("safety") or {}
        reason_code = "safety_" + str(safety.get("category", "blocked")).lower()
    else:
        outcome = "allow"
        reason_code = view.reason_code.value if view else "allowed"

    navigation = None
    if outcome == "allow" and view is not None and view.route_key is not None:
        navigation = {"route_key": view.route_key}
        if view.route_label:
            navigation["label"] = view.route_label

    clarification = None
    existing_clarification = result.get("clarification")
    if outcome == "clarify" and isinstance(existing_clarification, dict):
        # Seçenekler kullanıcıya İNSANİ etiketle sunulur; ham intent id (snake_case)
        # ASLA yayımlanmaz (frontend çipe basınca 'anlamadım'a düşerdi -> B07/#12).
        # Çip tıklaması etiket/soruyla yeniden sorulur; action_id yalnız yönlendirme
        # metadatasıdır (kullanıcı-görünür değil).
        options = []
        for candidate in existing_clarification.get("candidates", []):
            if not (isinstance(candidate, dict) and candidate.get("intent")):
                continue
            label = candidate.get("label") or str(candidate["intent"]).replace("_", " ")
            options.append({"action_id": candidate["intent"], "label": label})
        clarification = {"prompt": CLARIFICATION_PROMPT_TEXT, "options": options}

    return {
        "contract_version": 2,
        "served_role": _WIRE_ROLES[role],
        "role_space_version": space.version,
        "role_space_hash": space.content_hash,
        "outcome": outcome,
        "action_id": intent,
        "reason_code": reason_code,
        "navigation": navigation,
        "clarification": clarification,
        "suggestions": list(result.get("suggestions") or []),
    }


def _attach_assistant_meta(result: dict[str, Any], role: str) -> dict[str, Any]:
    result["assistant_meta"] = assistant_meta_from_result(result, role)
    return result


def _build_clarification(trace: dict[str, Any], *, force: bool = False) -> dict[str, Any] | None:
    """Karar belirsizse (ilk iki aday çok yakın) netleştirme adayları üretir.

    `intent` yine en iyi tahmin olarak döner (metrikler değişmez); bu alan yalnızca
    frontend'in "Bunu mu demek istedin?" seçenekleri göstermesi için EK bilgidir.
    `force=True` (düşük-güven bölgesi) margin şartını atlar; adaylar her durumda üretilir.
    """

    dec = trace.get("decision", {})
    if dec.get("fallback") or dec.get("source") != "similarity":
        return None
    sim = trace.get("similarity", {})
    top_k = sim.get("top_k") or []
    margin = sim.get("margin")
    if len(top_k) < 2:
        return None
    if not force and (margin is None or margin >= CLARIFY_MARGIN):
        return None

    candidates = []
    for cand in top_k[:2]:
        info = get_intent(cand["intent"])
        candidates.append({
            "intent": cand["intent"],
            "label": info["description"] if info else cand["intent"],
            "response_id": info["response_id"] if info else None,
            "confidence": cand["score"],
        })
    reason = "low_margin" if (margin is not None and margin < CLARIFY_MARGIN) else "low_confidence"
    return {"reason": reason, "margin": round(margin, 4) if margin is not None else None,
            "candidates": candidates}


def _safety_info(safety: "safety_mod.SafetyDecision") -> dict[str, Any]:
    return {
        "decision": safety.decision,
        "category": safety.category,
        "severity": safety.severity,
        "rule_id": safety.rule_id,
        "requires_review": safety.requires_review,
        "rule_version": safety.rule_version,
    }


def _safety_trace(
    trace_id: str, query: str, role: str, authenticated: bool,
    safety: "safety_mod.SafetyDecision",
) -> dict[str, Any]:
    """Kısa devre (bloklanan) istekler için minimal trace kaydı."""

    return {
        "trace_id": trace_id,
        "query_masked": safety_mod.mask_pii(query)[0],
        "role": role,
        "authenticated": authenticated,
        "short_circuit": "safety",
        "safety": _safety_info(safety),
        "response_id": "safety_" + safety.category.lower(),
    }


# Tire/nokta ile aralanmış tek harf dizisi ("S-ı-n-a-v", "a.b.c"). Kelime
# sınırı (boşluk) ayraç sınıfına DAHİL DEĞİL -> kelimeler birbirine karışmaz.
_SPACED_LETTER_RUN: "re.Pattern[str]" = re.compile(r"(?<!\w)(\w(?:[.\-]\w){2,})(?!\w)")


def _deobfuscate(text: str) -> str:
    """Gizlenmiş sorguyu intent eşleşmesi için temizler.

    safety_normalize (leetspeak/görünmez unicode/aksan) + tire-nokta ile aralanmış
    tek harfleri kelimeye toplama (kelime sınırı korunur):
    'S-ı-n-a-v n-a-s-ı-l' -> 'sinav nasil', '5ın4v' -> 'sinav'.
    """

    text = safety_mod.safety_normalize(text)
    return _SPACED_LETTER_RUN.sub(lambda m: re.sub(r"[.\-]", "", m.group(1)), text)


_BRAND: str = "hezarfen"


def _levenshtein(a: str, b: str) -> int:
    """İki dize arasındaki düzenleme (edit) mesafesi."""

    if a == b:
        return 0
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def _brand_typo(query: str) -> str | None:
    """Sorguda 'Hezarfen' marka adının yanlış yazımı var mı?

    Varsa yanlış yazılan token'ı döndürür; doğru yazım (çekimli hâller dahil:
    'Hezarfen', 'Hezarfen'de', 'Hezarfeni'...) varsa None. Yakınlık edit-mesafesi
    <= 2 ile ölçülür (yalnız gerçek yakın-ıskalar; 'haberler' gibi kelimeler uzak).
    """

    tokens = folded_tokens(query)
    # Doğru yazım (önek eşleşmesi çekimleri de kapsar) varsa uyarı yok.
    if any(t == _BRAND or t.startswith(_BRAND) for t in tokens):
        return None
    for t in tokens:
        if 6 <= len(t) <= 10 and t.startswith("h") and _levenshtein(t, _BRAND) <= 2:
            return t
    return None


def _with_brand_note(text: str, query: str) -> str:
    """Marka adı yanlış yazılmışsa cevabın başına kibar bir düzeltme notu ekler.

    Normal cevap korunur; yalnızca nazik bir hatırlatma öne eklenir.
    """

    typo = _brand_typo(query)
    if typo is None:
        return text
    return (
        f'🙂 Küçük bir not: doğru yazımı **Hezarfen** ("{typo.capitalize()}" yazmışsın).\n\n'
        + text
    )


class Engine:
    """Süreç ömrü boyunca yeniden kullanılan backend motoru."""

    def __init__(
        self,
        matcher: SimilarityMatcher | None = None,
        log_sink: LogSink | None = None,
        rate_limiter: "safety_mod.RateLimiter | None" = None,
    ) -> None:
        # ``None`` means role-local default. A custom matcher is retained for
        # tests/opt-in embedding and projected into the selected space later.
        self._matcher = matcher
        self._log_sink = log_sink
        self._rate_limiter = rate_limiter
        # Çok-turlu diyalog durumu, session.user_id ile anahtarlanır (üretimde her
        # kullanıcı ayrı). user_id yoksa durum tutulmaz -> stateless (paylaşılan
        # motorda kullanıcılar arası sızıntı olmaz). Bkz. dialog_state.py.
        self._dialog: dict[str, "dialog_state.DialogState"] = {}

    def handle(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Diyalog-durumu sarmalayıcısı: önceki durumu okur, işler, durumu günceller.

        Durum güncellemesi burada TEK yerde yapılır (``_run`` içindeki çok sayıda
        erken-return'ü etkilemeden); ``_run`` prior durumu okur, biz sonra yazarız."""

        session = payload.get("session")
        user_id = session.get("user_id") if isinstance(session, dict) else None
        result = self._run(payload)
        if user_id is not None:
            key = str(user_id)
            prior = self._dialog.get(key)
            query = payload.get("query")
            self._dialog[key] = dialog_state.next_state(
                prior, query if isinstance(query, str) else "", result
            )
        return result

    def _run(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Bir istek payload'ını işleyip yanıt sözleşmesi döndürür.

        Akış: içerik-güvenliği giriş kapısı -> (gerekirse kısa devre) -> boru hattı
        -> çıktı güvenliği kontrolü.
        """

        query = payload.get("query")
        # Eksik/yanlış-tipli 'query' -> sözleşme ihlali (çağıran hatası): istisna.
        if not isinstance(query, str):
            raise RequestError("'query' bir metin olmalı.")

        role, authenticated = _parse_session(payload)
        trace_id = payload.get("trace_id") or new_trace_id()
        user_id = (payload.get("session") or {}).get("user_id")
        suggestions = suggestions_for(role)  # role bazlı başlangıç soru önerileri

        # Boş / yalnızca-boşluk girdi kullanıcı kaynaklıdır -> istisna değil, nazik
        # fallback. (AI katmanı kullanıcı girdisine hata fırlatmaz.)
        if not query.strip():
            empty = {
                "trace_id": trace_id,
                "response_id": FALLBACK["response_id"],
                "text": FALLBACK["response_template"],
                "intent": None,
                "confidence": 0.0,
                "fallback": True,
                "auth_action": None,
                "required_role": None,
                "navigation": None,
                "clarification": None,
                "answers": None,
                "suggestions": suggestions,
                "safety": _safety_info(safety_mod.evaluate_input("")),
            }
            if self._log_sink is not None:
                self._log_sink({
                    "trace_id": trace_id, "query_masked": safety_mod.mask_pii(query)[0], "role": role,
                    "authenticated": authenticated, "short_circuit": "empty_query",
                    "response_id": FALLBACK["response_id"],
                })
            return _attach_assistant_meta(empty, role)

        # 0) Rate-limit / spam (opsiyonel; user_id gerekir).
        if self._rate_limiter is not None and user_id:
            limited = self._rate_limiter.check(str(user_id), query)
            if limited is not None:
                if self._log_sink is not None:
                    self._log_sink(_safety_trace(trace_id, query, role, authenticated, limited))
                return _attach_assistant_meta({
                    "trace_id": trace_id,
                    "response_id": "safety_" + limited.category.lower(),
                    "text": limited.user_message,
                    "intent": None,
                    "confidence": limited.confidence,
                    "fallback": False,
                    "auth_action": None,
                    "required_role": None,
                    "navigation": None,
                    "clarification": None,
                    "answers": None,
                    "suggestions": suggestions,
                    "safety": _safety_info(limited),
                }, role)

        # 1) İçerik-güvenliği giriş kapısı.
        safety = safety_mod.evaluate_input(query, role=role, authenticated=authenticated)
        safety_info = _safety_info(safety)

        if safety.decision in safety_mod.BLOCKING_DECISIONS:
            if self._log_sink is not None:
                self._log_sink(_safety_trace(trace_id, query, role, authenticated, safety))
            return _attach_assistant_meta({
                "trace_id": trace_id,
                "response_id": "safety_" + safety.category.lower(),
                "text": safety.user_message,
                "intent": None,
                "confidence": safety.confidence,
                "fallback": False,
                "auth_action": None,
                "required_role": None,
                "navigation": None,
                "clarification": None,
                "answers": None,
                "suggestions": suggestions,
                "safety": safety_info,
            }, role)

        # 1.5) Rol beyanı ("Öğrenci", "ben öğretmenim") -> role özel yetenek özeti.
        # Bot 'rolünü söyle' dediğinde verilen tek kelimelik cevabı anlamlandırır;
        # aksi hâlde 'Öğrenci' yanlışlıkla 'öğrenci kaydet' intent'ine benzerdi.
        # Rol beyanı/sorusu BİLGİ amaçlıdır: sorulan rolün yeteneklerini anlatır,
        # oturumun gerçek yetkisini (gating) ASLA değiştirmez. Doğrulanmış bir öğrenci
        # 'admin' yazarsa admin yeteneklerini bilgi olarak görür, admin OLMAZ.
        declared = _declared_role(query) or _role_correction(query)
        served_declaration = declared
        caps = capabilities_for(served_declaration) if served_declaration else None
        if caps:
            if self._log_sink is not None:
                self._log_sink({
                    "trace_id": trace_id, "query_masked": safety_mod.mask_pii(query)[0], "role": role,
                    "authenticated": authenticated, "short_circuit": "role_declaration",
                    "declared_role": declared, "served_role": served_declaration,
                    "response_id": "role_capabilities_" + served_declaration,
                })
            return _attach_assistant_meta({
                "trace_id": trace_id,
                "response_id": "role_capabilities_" + served_declaration,
                "text": caps,
                "intent": None,
                "confidence": 1.0,
                "fallback": False,
                "auth_action": None,
                "required_role": None,
                "navigation": None,
                "clarification": None,
                "answers": None,
                "suggestions": suggestions,
                "safety": safety_info,
            }, role)

        # PII maskeleme: maskelenmiş sorguyu boru hattına ver.
        effective_query = query
        if safety.decision == safety_mod.MASK_AND_ALLOW and safety.masked_message:
            effective_query = safety.masked_message

        # 1.51) Çok-turlu diyalog takibi: önceki tura göre çöz (onay/sıra "ilki",
        # devam "peki sonra?", itiraz "orada yok", not/karne bağlamında çıplak ad).
        # Çözülürse ilgili intent'in KANONİK sorgusuna çevrilir; kalan adımlar (sosyal
        # önek/olumsuzluk/kapsam/çoklu) kanonikten zararsız geçer. Yalnız user_id varsa.
        _uid = (payload.get("session") or {}).get("user_id")
        if _uid is not None:
            _prior = self._dialog.get(str(_uid))
            if _prior is not None:
                _rule_hit = get_role_space(role).rule_matcher.match(query) is not None
                _resolved = dialog_state.resolve(_prior, query, role, _rule_hit)
                if _resolved is not None:
                    _canon = dialog_state.canonical_query(_resolved)
                    if _canon:
                        effective_query = _canon

        # 1.52) Sosyal önek: "Merhaba, karnemi nerede görürüm?" -> selam kısmını soy,
        # görevi yönlendir. YALNIZCA kalan görev KURAL katmanına (yüksek-kesinlik)
        # çarpıyorsa soyulur; aksi halde 'naber nasıl gidiyor' / 'teşekkür ederim'
        # gibi saf sosyal ifadeler yanlışlıkla bölünmez -> greeting/thanks kalır.
        _stripped = _strip_social_prefix(effective_query)
        if (_stripped != effective_query
                and get_role_space(role).rule_matcher.match(_stripped) is not None):
            effective_query = _stripped

        # 1.55) Olumsuzluk: "A değil/istemiyorum, B istiyorum" -> B'ye göre yanıtla;
        # saf olumsuz komut ("notlarımı gösterme") -> uygulama, netleştir (asla yanlış).
        _neg_resolved = _resolve_negation(effective_query)
        pure_negation = _neg_resolved.strip() == ""
        if not pure_negation and _neg_resolved != effective_query:
            effective_query = _neg_resolved

        # 1.57) Henüz canlı olmayan/bulunmayan özellik -> yanlış yönlendirme YOK,
        # dürüstçe "henüz kullanılamıyor" (intent None, nav yok).
        _unavail = _unavailable_feature(effective_query)
        if _unavail is not None:
            result = {
                "trace_id": trace_id,
                "response_id": "feature_unavailable",
                "text": _with_brand_note(
                    f"**{_unavail}** özelliği şu an henüz aktif değil; bu sayfa "
                    "kullanılamıyor. Eklenince burada yardımcı olacağım.", query),
                "intent": None,
                "confidence": 0.0,
                "fallback": False,
                "auth_action": None,
                "required_role": None,
                "navigation": None,
                "clarification": None,
                "answers": None,
                "suggestions": [],
                "safety": safety_info,
            }
            return _attach_assistant_meta(result, role)

        # 1.58) Kapsam sınırı: canlı VERİ çekme/sayım VEYA bot adına iş yapma/veri
        # değiştirme isteği -> yanlış sayfaya yönlendirme YOK; dürüstçe "yapamam,
        # yalnızca nasıl". Manipülasyon (ödevi yap, notu yükselt, devamsızlığı sil)
        # önce kontrol edilir; ikisi de intent=None döndürür (asla yanlış).
        _scope_kind = None
        if _is_manipulation_request(effective_query):
            _scope_kind = "action"
        elif _is_data_fetch_request(effective_query):
            _scope_kind = "data"
        if _scope_kind is not None:
            if _scope_kind == "action":
                text = (
                    "Bunu senin yerine yapamam ve verini (not, devamsızlık, yoklama, "
                    "ödev) değiştiremem/silemem 🙂 Ben yalnızca nasıl yapılacağını adım "
                    "adım anlatabilirim. Örneğin \"ödevimi nasıl teslim ederim?\" ya da "
                    "\"notlarımı nereden görürüm?\" diye sorabilirsin."
                )
            else:
                text = (
                    "Ben gerçek veriyi getiremem, gösteremem ya da göremem; sistemdeki "
                    "canlı kayıtları bilemiyorum 🙂 Yalnızca nasıl yapılacağını adım adım "
                    "anlatabilirim. Örneğin \"öğrenci listesini nereden görürüm?\" diye "
                    "sorarsan, ilgili sayfayı ve adımları söyleyeyim."
                )
            if self._log_sink is not None:
                self._log_sink({
                    "trace_id": trace_id, "query_masked": safety_mod.mask_pii(query)[0],
                    "role": role, "authenticated": authenticated,
                    "short_circuit": "scope_boundary_" + _scope_kind,
                    "response_id": "out_of_scope_action",
                })
            return _attach_assistant_meta({
                "trace_id": trace_id,
                "response_id": "out_of_scope_action",
                "text": _with_brand_note(text, query),
                "intent": None,
                "confidence": 0.0,
                "fallback": False,
                "auth_action": None,
                "required_role": None,
                "navigation": None,
                "clarification": None,
                "answers": None,
                "suggestions": suggestions,
                "safety": safety_info,
            }, role)

        # 1.6) Çoklu istek ('X ve Y'): her bağımsız parça ayrı yanıtlanır.
        segments = _multi_intent_segments(effective_query, role)
        # >4 farklı işlem tek turda: net anlatmak güç -> netleştir (asla yarım cevap).
        if segments is not None and len(segments) > 4:
            text = (
                "Aynı anda birkaç işlem istedin gibi 🙂 Her birini net anlatabilmem "
                "için tek tek sorar mısın? Örneğin önce \"sınav nasıl oluşturulur?\" "
                "diye başlayabilir, sonra diğerlerini sırayla sorabilirsin."
            )
            if self._log_sink is not None:
                self._log_sink({
                    "trace_id": trace_id, "query_masked": safety_mod.mask_pii(query)[0],
                    "role": role, "authenticated": authenticated,
                    "short_circuit": "multi_intent_overflow",
                    "intents": [i for _s, i in segments], "response_id": "clarification_prompt",
                })
            return _attach_assistant_meta({
                "trace_id": trace_id,
                "response_id": "clarification_prompt",
                "text": _with_brand_note(text, query),
                "intent": None,
                "confidence": 0.0,
                "fallback": False,
                "auth_action": None,
                "required_role": None,
                "navigation": None,
                "clarification": None,
                "answers": None,
                "suggestions": suggestions,
                "safety": safety_info,
            }, role)
        if segments is not None:
            segments = segments[:4]
            answers: list[dict[str, Any]] = []
            parts: list[str] = []
            for order, (segment, _intent) in enumerate(segments, start=1):
                seg_response, seg_trace = process(
                    segment, role=role, authenticated=authenticated,
                    trace_id=f"{trace_id}.{order}", matcher=self._matcher,
                )
                answers.append({
                    "intent": seg_response.intent,
                    "response_id": seg_response.response_id,
                    "text": seg_response.text,
                    "auth_action": seg_response.auth_action,
                    "navigation": _build_navigation(
                        seg_response.intent, seg_response.auth_action, role
                    ),
                })
                # Reddedilen parçada intent açıklaması KULLANILMAZ: açıklama üst-rol
                # etiketi ("(Öğretmen+)") ve ayrıcalıklı eylem adını ("... oluşturma")
                # içerir; deny gövdesinin üstüne basılınca no-leak sözleşmesi kırılır
                # (ISO-017..019). Reddedilene nötr başlık ver.
                if seg_response.auth_action:
                    title = f"İstek {order}"
                else:
                    info = get_intent(seg_response.intent) if seg_response.intent else None
                    title = (info["description"].rstrip(".") if info else segment)
                    if title.endswith(")") and "(" in title:  # sondaki "(...)" rol etiketini at
                        title = title[: title.rfind("(")].rstrip()
                parts.append(f"**{order}) {title}**\n{seg_response.text}")

            text = "Birkaç şey sormuşsun, sırayla cevaplayayım:\n\n" + "\n\n".join(parts)
            out = safety_mod.evaluate_output(text)
            if out.decision == safety_mod.MASK_AND_ALLOW and out.masked_message:
                text = out.masked_message
            elif out.decision == safety_mod.BLOCK:
                text = out.user_message

            first = answers[0]
            if self._log_sink is not None:
                self._log_sink({
                    "trace_id": trace_id, "query_masked": safety_mod.mask_pii(query)[0], "role": role,
                    "authenticated": authenticated, "short_circuit": "multi_intent",
                    "intents": [a["intent"] for a in answers],
                    "response_id": first["response_id"],
                    "safety": safety_info,
                })
            result = {
                "trace_id": trace_id,
                "response_id": first["response_id"],
                "text": _with_brand_note(text, query),
                "intent": first["intent"],
                "confidence": 1.0,  # kural tabanlı parçalar (yüksek kesinlik)
                "fallback": False,
                "auth_action": first["auth_action"],
                "required_role": None,
                "navigation": first["navigation"],
                "clarification": None,
                "answers": answers,
                "suggestions": suggestions,
                "safety": safety_info,
            }
            return _attach_assistant_meta(result, role)

        # 2) Boru hattı.
        response, trace = process(
            effective_query,
            role=role,
            authenticated=authenticated,
            trace_id=trace_id,
            matcher=self._matcher,
        )
        trace["safety"] = safety_info

        # İkinci şans: leetspeak ('5ın4v') veya harf-aralama ('S-ı-n-a-v') gibi
        # gizlemeler normal boru hattında fallback'e düşerse, güvenlik-normalize
        # edilmiş (deleet + tek-harf birleştirme) sorguyla bir kez daha dene. Yalnız
        # fallback'te çalışır, normal sorguları etkilemez; OOS yine OOS kalır.
        # Gizlenmiş sorgu her zaman fallback'e düşmez; orta-güvenli bir similarity
        # yanlışına da oturabilir ('5ın4v nasıl oluşturulur' -> course_create 0.65).
        # O yüzden birincil karar KURAL değilse (similarity) de deobfuscation dene;
        # ama düşük-güvenli similarity'yi YALNIZ deobfuscation bir KURAL eşleşmesi
        # (precision=1.0 garantili) açığa çıkarırsa geçersiz kıl. Fallback yolu aynen.
        primary_source = trace["decision"].get("source")
        if response.fallback or primary_source == "similarity":
            cleaned = _deobfuscate(effective_query)
            if cleaned and cleaned != effective_query.strip().lower():
                alt_response, alt_trace = process(
                    cleaned,
                    role=role,
                    authenticated=authenticated,
                    trace_id=trace_id,
                    matcher=self._matcher,
                )
                alt_source = alt_trace["decision"].get("source")
                if (response.fallback and not alt_response.fallback) or (
                    not response.fallback and alt_source == "rule"
                ):
                    alt_trace["safety"] = safety_info
                    alt_trace["deobfuscated_query"] = cleaned
                    response, trace = alt_response, alt_trace

        # Belirsiz bölge: benzerlik güveni düşükse yanlış-ama-özgüvenli cevap verme;
        # "anlayamadım — bunu mu demek istedin?" + adaylar döndür.
        dec = trace["decision"]
        margin = trace["similarity"].get("margin")
        topk = trace["similarity"].get("top_k") or []
        top2_social = (
            len(topk) >= 2
            and topk[0]["intent"] in _SOCIAL_INTENTS
            and topk[1]["intent"] in _SOCIAL_INTENTS
        )
        # Tek kelimelik belirsiz sorgu (ör. "Ayarlar", "Sınav") KURAL değil similarity
        # ile eşleşiyorsa tam cevap verme -> netleştir + öneri (asla yanlış).
        single_word_similarity = (
            not response.fallback
            and dec["source"] == "similarity"
            and len(effective_query.split()) == 1
        )
        ask_mode = pure_negation or single_word_similarity or (
            not response.fallback
            and dec["source"] == "similarity"
            and (
                dec["confidence"] < ASK_CONFIDENCE
                or (
                    dec["confidence"] < ASK_LOW_MARGIN_CONFIDENCE
                    and margin is not None
                    and margin < ASK_LOW_MARGIN
                    and top2_social
                )
                # Top-1 ≈ Top-2: skor yüksek olsa da ayırt edilemiyor -> netleştir.
                or (margin is not None and margin < ASK_TIE_MARGIN)
                # Net okul-dışı konu (yalnız benzerlik) -> zayıf-eşleşme FP'sini kes.
                or bool(_FAR_OOS_TOPICS.intersection(folded_tokens(effective_query)))
            )
        )
        if ask_mode:
            clarification = _build_clarification(trace, force=True)
            trace["ask_clarification"] = True
            text = CLARIFICATION_PROMPT_TEXT
            if safety.decision == safety_mod.ALLOW_WITH_WARNING and safety.user_message:
                text = safety.user_message + "\n" + text
            if self._log_sink is not None:
                self._log_sink(trace)
            result = {
                "trace_id": trace["trace_id"],
                "response_id": "clarification_prompt",
                "text": text,
                "intent": None,  # tahmin adaylarda; tam cevap bilerek verilmedi
                "confidence": dec["confidence"],
                "fallback": False,
                "auth_action": None,
                "required_role": None,
                "navigation": None,
                "clarification": clarification,
                "answers": None,
                "suggestions": suggestions,
                "safety": safety_info,
            }
            return _attach_assistant_meta(result, role)

        text = response.text
        # "Neler yapabilirim?" -> oturum rolü belliyse jenerik "rolünü söyle" yerine
        # o role özel yetenek özeti (kullanıcı zaten rolünü biliyor).
        if response.intent == "help_capabilities" and authenticated:
            role_caps = capabilities_for(role)
            if role_caps:
                text = role_caps
        if safety.decision == safety_mod.ALLOW_WITH_WARNING and safety.user_message:
            text = safety.user_message + "\n" + text

        # 3) Çıktı güvenliği kontrolü.
        out = safety_mod.evaluate_output(text)
        trace["output_safety"] = {"decision": out.decision, "category": out.category, "rule_id": out.rule_id}
        if out.decision == safety_mod.MASK_AND_ALLOW and out.masked_message:
            text = out.masked_message
        elif out.decision == safety_mod.BLOCK:
            text = out.user_message

        if self._log_sink is not None:
            self._log_sink(trace)

        result = {
            "trace_id": trace["trace_id"],
            "response_id": response.response_id,
            "text": _with_brand_note(text, query),
            "intent": response.intent,
            "confidence": trace["decision"]["confidence"],
            "fallback": response.fallback,
            "auth_action": response.auth_action,
            "required_role": trace["decision"]["required_role"],
            "navigation": _build_navigation(response.intent, response.auth_action, role),
            "clarification": _build_clarification(trace),
            "answers": None,
            "suggestions": suggestions,
            "safety": safety_info,
        }
        return _attach_assistant_meta(result, role)


# Kolaylık: paylaşılan varsayılan motor.
_DEFAULT_ENGINE: Engine | None = None


def get_default_engine() -> Engine:
    global _DEFAULT_ENGINE
    if _DEFAULT_ENGINE is None:
        _DEFAULT_ENGINE = Engine()
    return _DEFAULT_ENGINE


def handle_request(payload: dict[str, Any]) -> dict[str, Any]:
    """Paylaşılan motorla tek atımlık istek işleme."""

    return get_default_engine().handle(payload)
