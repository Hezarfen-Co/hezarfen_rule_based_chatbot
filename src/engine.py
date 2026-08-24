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
from typing import Any, Callable, Final

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
from .domain import FAR_OOS_TOPICS, is_explicitly_out_of_scope
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
# Okul-dışı, net kapsam-dışı konu kelimeleri (FOLD edilmiş). Yalnızca KURAL
# çarpmayıp benzerlik zayıf-eşleşme verdiğinde (ör. 'öğretmenime hediye ne alayım'
# -> messages_use FP) netleştirmeye zorlar. Kısa ve gerçekten alan-dışı tutulur;
# okul terimleriyle çakışmaz. Kalıcı çözüm: gömme-tabanlı OOS (bkz. kriterler.md).
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

_ROLE_CONTEXT_NAME = (
    r"(?:ziyaretçi|ziyaretci|veli|öğrenci|ogrenci|öğretmen|ogretmen|"
    r"yönetici|yonetici|admin)"
)
_ROLE_CONTEXT_PREFIXES: tuple[re.Pattern[str], ...] = (
    re.compile(rf"^{_ROLE_CONTEXT_NAME}\s+hesabımla\s*[,;:]?\s+(.+)$", re.IGNORECASE),
    re.compile(rf"^oturum\s+rolüm\s+{_ROLE_CONTEXT_NAME}\s*[;,:-]\s*(.+)$", re.IGNORECASE),
    re.compile(rf"^{_ROLE_CONTEXT_NAME}\s+olarak\s+şunu\s+yapmak\s+istiyorum\s*:\s*(.+)$", re.IGNORECASE),
    re.compile(rf"^ben\s+{_ROLE_CONTEXT_NAME}\s+rolündeyim\s*[.;,:-]\s*(.+)$", re.IGNORECASE),
    re.compile(rf"^{_ROLE_CONTEXT_NAME}\s+panelinden\s+soruyorum\s*:\s*(.+)$", re.IGNORECASE),
    re.compile(rf"^hesabım\s+{_ROLE_CONTEXT_NAME}\s+yetkisinde\s*[;,:-]\s*(.+)$", re.IGNORECASE),
)

_BRAND_CONTEXT_PREFIX: re.Pattern[str] = re.compile(
    r"^\s*hezarfen(?:['’]?(?:de|da)|\s+uygulamasında)\s*[,;:\-]?\s+(.+)$",
    re.IGNORECASE,
)

# Frontend aynı etiketi Türkçe/İngilizce birlikte gösterebilir. Slash, parantez
# ve köşeli-parantez biçimleri görev metninin parçası değildir; kanonik Türkçe
# etikete indirgenir. Bu, yalnız bilinen UI çiftlerine uygulanır.
_UI_CANONICAL_LABELS: Final[tuple[tuple[str, str], ...]] = (
    ("Profil", "Profile"), ("Ayarlar", "Settings"), ("Hesap", "Account"),
    ("Dersler", "Courses"), ("Sınavlar", "Exams"), ("Ödev", "Homework"),
    ("Mesajlar", "Messages"), ("Defter", "Notebook"), ("Kaydet", "Save"),
    ("Kaldır", "Remove"), ("Gönder", "Submit"), ("Giriş", "Login"),
    ("Çıkış", "Logout"), ("Yoklama", "Attendance"),
    ("Karnem", "Report Card"), ("Randevular", "Appointments"),
)
_INLINE_UI_LABEL_PATTERNS: Final[tuple[tuple[re.Pattern[str], str], ...]] = tuple(
    (
        re.compile(
            rf"(?<!\w)(?:{re.escape(tr)}\s*\(\s*{re.escape(en)}\s*\)|"
            rf"{re.escape(tr)}\s*/\s*{re.escape(en)}|"
            rf"{re.escape(en)}\s*\[\s*{re.escape(tr)}\s*\])(?!\w)",
            re.IGNORECASE,
        ),
        tr,
    )
    for tr, en in _UI_CANONICAL_LABELS
)


def _canonicalize_inline_ui_labels(query: str) -> str:
    for pattern, canonical in _INLINE_UI_LABEL_PATTERNS:
        query = pattern.sub(canonical, query)
    return query

# Kullanıcının asıl görevini değiştirmeyen doğal/prosedürel çerçeveler. Bunlar
# gerçek destek konuşmalarında "hangi ekranda", "menüde bulamıyorum", "amacım şu"
# biçiminde sık görülür; çekirdek görev eşleşmesini gölgelememelidir.
_TASK_CONTEXT_PREFIXES: tuple[re.Pattern[str], ...] = (
    re.compile(r"^\s*arayüzde\b[^;]{0,100}\bekranındayım\s*;\s*(.+)$", re.IGNORECASE),
    re.compile(r"^\s*türkçe/english\s+arayüzde\b[^;?]{0,100}\bsayfasında\s+(.+)$", re.IGNORECASE),
    re.compile(r"^\s*ui\s+etiketi\b[^.]{0,100}\bolarak\s+görünüyor\s*[.:;]\s*(.+)$", re.IGNORECASE),
    re.compile(r"^\s*önce\s+hangi\s+sayfaya\s+gitmeliyim\s*:\s*(.+)$", re.IGNORECASE),
    re.compile(r"^\s*(?:şunu\s+yapmak\s+istiyorum|yapmak\s+istediğim\s+işlem\s+şu)\s*:\s*(.+)$", re.IGNORECASE),
    re.compile(r"^\s*uygulamayı\s+yeni\s+kullanıyorum\s*;\s*(.+)$", re.IGNORECASE),
    re.compile(r"^\s*(?:amacım\s+şu|merak\s+ettiğim\s+konu\s+şu|şunu\s+merak\s+ediyorum)\s*:\s*(.+)$", re.IGNORECASE),
    re.compile(r"^\s*(?:şunu\s+öğrenmek\s+istiyorum|merak\s+ettiğim\s+konu)\s*:\s*(.+)$", re.IGNORECASE),
    re.compile(r"^\s*(?:soru|bir\s+sorum\s+var)\s*:\s*(.+)$", re.IGNORECASE),
    re.compile(
        r"^\s*(?:şimdi\s+ben|yardım\s+eder\s+misin|kısaca|uygulamada|"
        r"hesabımda|kısa\s+bir\s+soru|hocam|dostum|rica\s+etsem|acaba|"
        r"m[üu]saitsen|peki|bir\s+(?:şey|sey)\s+(?:soracağım|soracagim))"
        r"\s*[,;:—-]\s*(.+)$",
        re.IGNORECASE,
    ),
    re.compile(
        r"^\s*(?:kısa\s+bir\s+soru|kisa\s+bir\s+soru|yardım|yardim)\s+"
        # "Yardım menün var mı?" başındaki Yardım bir söylem dolgusu değil,
        # help_capabilities intent'inin gerçek konusudur. Çekimli menü biçimlerini
        # de (menün/menüsü/menüde) koru.
        r"(?!(?:men[üu]\w*|edebil\w*)\b)(.+)$",
        re.IGNORECASE,
    ),
)

_TASK_CONTEXT_SUFFIXES: tuple[re.Pattern[str], ...] = (
    re.compile(r"^(.+?)\s*[.]\s*bu\s+işlem\s+hangi\s+ekrandan\s+yapılıyor\s*[?]?$", re.IGNORECASE),
    re.compile(r"^(.+?)\s+konusunda\s+yol\s+gösterir\s+misin\s*[?]?$", re.IGNORECASE),
    re.compile(r"^(.+?)\s+konusunda\s+hangi\s+yolu\s+izlemeliyim\s*[?]?$", re.IGNORECASE),
    re.compile(r"^(.+?)\s+hakkında\s+bilgi\s+verir\s+misin\s*[?]?$", re.IGNORECASE),
    re.compile(r"^(.+?)\s+konusunu\s+adım\s+adım\s+açıklayabilir\s+misin\s*[?]?$", re.IGNORECASE),
    re.compile(r"^(.+?)\s+konusunu\s+farklı\s+bir+\s+ifadeyle\s+soruyorum\s*;\s*nasıl\s+ilerlerim\s*[?]?$", re.IGNORECASE),
    re.compile(r"^(.+?)\s+için\s+izlenecek\s+doğru\s+akış\s+nedir\s*[?]?$", re.IGNORECASE),
    re.compile(r"^(.+?)\s+işlemini\s+yapmak\s+istiyorum\s*[.]?$", re.IGNORECASE),
    re.compile(r"^(.+?)\s+gerekiyor\s*;\s*doğru\s+işlem\s+akışı\s+nedir\s*[?]?$", re.IGNORECASE),
    re.compile(r"^(.+?)\s*[—-]\s*doğru\s+yol\s+nedir\s*[?]?$", re.IGNORECASE),
    re.compile(r"^(.+?)\s*[.]\s*bana\s+işlem\s+yolunu\s+anlatır\s+mısın\s*[?]?$", re.IGNORECASE),
    re.compile(r"^(.+?)\s*[;]\s*bunu\s+açıklayabilir\s+misin\s*[?]?$", re.IGNORECASE),
    re.compile(r"^(.+?)\s*[.]\s*nasıl\s+ilerlerim\s*[?]?$", re.IGNORECASE),
    re.compile(
        r"^(.+?)\s*[.;…—-]\s*(?:lütfen|lutfen|"
        r"hangi\s+adımları\s+(?:sırayla\s+)?izlemeliyim|"
        r"bir\s+bakar\s+mısın|nereden\s+(?:başlamalıyım|baslamaliyim)|"
        r"yardım(?:cı)?\s+(?:eder|olur)\s+m[ıiuü]s[ıiuü]n|"
        r"yardim(?:ci)?\s+(?:eder|olur)\s+m[ıiuü]s[ıiuü]n|"
        r"nasıl\s+ilerleyeceğim|nasil\s+ilerleyecegim|doğru\s+ekran\s+hangisi|"
        r"bunu\s+açıklayabilir\s+misin|bunu\s+aciklayabilir\s+misin|"
        r"bunu\s+uygulamada\s+hangi\s+adımlarla\s+yaparım|"
        r"ne\s+yapmam\s+gerekiyor|kısaca\s+anlatır\s+mısın|"
        r"yol\s+gösterir\s+misin|mümkün\s+mü|mumkun\s+mu|hangi\s+ekranda|"
        r"nasıl\s+yapılır|nasil\s+yapilir|ne\s+yapmalıyım|adımları\s+nedir)\s*[?]?$",
        re.IGNORECASE,
    ),
    re.compile(
        r"^(.+?)\s*[.]\s*(?:ilgili\s+işlem\s+düğmesi|kaydet['’]?e|formu\s+doldurdum|"
        r"işlem\s+mevcut\s+durum|işlemden\s+sonra|butona\s+basınca|sayfa\s+açılıyor|"
        r"beklediğim\s+kayıt|ekran\s+yükleniyor|yalnız\s+bazı\s+kayıtları|"
        r"menüde\s+ilgili\s+bölümü)\b.*$",
        re.IGNORECASE,
    ),
)


def _strip_role_context_prefix(query: str) -> str:
    """Rol bağlamı önekini at; oturum yetkisini asla metinden değiştirme.

    ``Öğretmen hesabımla ...`` gerçek bir görev sorusudur. Buna karşılık yalnız
    ``Ben öğretmenim`` bir rol beyanı olarak kalır; desenler mutlaka önekten sonra
    boş olmayan bir görev ister.
    """

    stripped = query.strip()
    for pattern in _ROLE_CONTEXT_PREFIXES:
        match = pattern.match(stripped)
        if match:
            task = match.group(1).strip(" \t\r\n?!.,;:…")
            if task:
                return task
    return query


def _strip_brand_context_prefix(query: str) -> str:
    """Baştaki ürün-konum bağlamını at, gerçek görev cümlesini koru.

    ``Hezarfen nedir?`` marka sorusudur ve aynen kalır. ``Hezarfen'de 422 neden
    geliyor?`` ise 422 yardım sorusudur; locative önek platform_info kuralını
    yanlış tetiklememelidir.
    """

    match = _BRAND_CONTEXT_PREFIX.match(query.strip())
    if not match:
        return query
    task = match.group(1).strip(" \t\r\n?!.,;:…")
    return task or query


def _strip_task_context(query: str) -> str:
    """Saf söylem/UI/state çerçevelerini atıp çekirdek görevi döndür."""

    candidate = _canonicalize_inline_ui_labels(query).strip()
    # Bileşik sorularda birden fazla çerçeve iç içe olabilir. Sınırlı tekrar,
    # temizleyicinin serbest bir yeniden-yazıcıya dönüşmesini engeller.
    for _ in range(6):
        changed = False
        # Söylem öneki soyulunca içte marka/rol bağlamı kalabilir. Her turda aynı
        # dar bağlam temizleyicilerini yeniden uygulamak iç içe çerçeveleri çözer.
        for stripper in (_strip_role_context_prefix, _strip_brand_context_prefix):
            stripped = stripper(candidate).strip(" \t\r\n?!.,;:…")
            if len(folded_tokens(stripped)) >= 2 and stripped != candidate:
                candidate = stripped
                changed = True
                break
        if changed:
            continue
        for pattern in _TASK_CONTEXT_PREFIXES + _TASK_CONTEXT_SUFFIXES:
            match = pattern.match(candidate)
            if not match:
                continue
            stripped = match.group(1).strip(" \t\r\n?!.,;:…")
            if len(folded_tokens(stripped)) >= 2 and stripped != candidate:
                candidate = stripped
                changed = True
                break
        if not changed:
            break
    return candidate or query


ENTRY_EXIT_CLARIFICATION_TEXT: str = (
    "Buradaki giriş-çıkışla **hesaba giriş/çıkışı** mı, yoksa **personel mesai "
    "giriş-çıkışını** mı kastediyorsun? Birini yazarsan doğru adımları anlatayım."
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
    # "Arayüzde Defter ekranındayım; notu düzenlemek istiyorum" iki istek
    # değildir. İlk parça yalnız bağlamdır; aksi halde genel ekran intent'i ilk
    # cevap olup gerçek işlemi gölgeler.
    raw_segments = [
        segment for segment in raw_segments
        if not (
            any(token.startswith("arayuz") for token in folded_tokens(segment))
            and any(token.startswith(("ekran", "sayfa")) for token in folded_tokens(segment))
        )
    ]
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

    # "Öğrencinin notunu değil kaydını sil" gibi cümlelerde olumlu taraftaki
    # nesne, olumsuz taraftaki özneyi taşır. Sadece "değil" sonrasını almak
    # "kaydını sil" diye bağlamı kaybettirir; bu iki yüksek-kesinlikli okul
    # kalıbını önce kanonikleştir.
    tokens = folded_tokens(query)
    neg_positions = [i for i, token in enumerate(tokens) if token.startswith("degil")]
    if neg_positions:
        neg_index = neg_positions[-1]
        before, after = tokens[:neg_index], tokens[neg_index + 1:]
        # Karşılaştırmalı görünüm sorusunda özneyi kaybetme: "takvim haftalık
        # değil aylık mı" ifadesinin olumlu kısmı yalnız "aylık mı" değildir.
        if "takvim" in before and any(
            token.startswith(("aylik", "haftalik")) for token in after
        ):
            return "takvim " + " ".join(after)
        has_student = any(token.startswith("ogrenci") for token in before)
        has_remove = any(
            token.startswith(("sil", "kaldir", "cikar")) for token in after
        )
        if has_student and has_remove:
            if any(token.startswith(("kayit", "kayd", "roster")) for token in after):
                return "öğrenci kaydını sil"
            if any(token.startswith(("not", "puan")) for token in after):
                return "öğrenci notunu sil"

    # "A değil, B" -> son 'değil,' sonrasındaki olumlu kısım. Noktalama şartı,
    # "bridge bağlı değil diyor" / "özellik aktif değil" gibi olumsuz DURUM
    # anlatımlarının bağlamını yanlışlıkla kesmemizi engeller. Noktalamasız, anlamı
    # kesin okul karşıtlıkları yukarıda ayrı kanonikleştirilir.
    matches = list(re.finditer(r"değil\s*[,;:]", query, re.IGNORECASE))
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


def _entry_exit_is_ambiguous(query: str) -> bool:
    """Çıplak "giriş çıkış" ifadesinde hesap/mesai arasında tahmin yürütme."""

    tokens = folded_tokens(query)
    has_entry = any(token.startswith("giris") for token in tokens)
    has_exit = any(token.startswith("cikis") for token in tokens)
    qualified = any(
        token.startswith(("mesai", "personel", "hesap", "oturum", "sifre", "parola"))
        for token in tokens
    )
    return has_entry and has_exit and not qualified


# --- Henüz canlı olmayan / bulunmayan özellikler ----------------------------
# Bu anahtarlar bir sayfaya YANLIŞ yönlendirmek yerine dürüstçe "henüz
# kullanılamıyor" der (asla yanlış). T1 (randevu/yemek/soru-havuzu/beyaz-tahta)
# canlıya alınınca ilgili anahtar bu listeden çıkarılır; duyuru diye bir özellik
# hiç yoktur.
# Gerçekten var OLMAYAN özellik. (Randevu/Yemek/Soru bankası/Beyaz tahta artık
# üründe MEVCUT -> _FEATURE_INFO ile anlatılır; "duyuru" diye bir özellik yoktur.)
_UNAVAILABLE_FEATURES: tuple[tuple[str, str], ...] = (
    ("duyuru", "Duyurular"),
)


def _unavailable_feature(query: str) -> str | None:
    low = query.casefold()
    for keyword, label in _UNAVAILABLE_FEATURES:
        if keyword in low:
            return label
    return None


# (T1 özellikleri — randevu/yemek/beyaz tahta/soru havuzu — artık gerçek intent'lerdir;
#  eski _FEATURE_INFO stopgap'i kaldırıldı, boru hattı bunları normal karşılar.)


# --- Kapsam sınırı: canlı VERİ çekme isteği ---------------------------------
# Çelebi gerçek veriyi getirmez/göstermez; yalnızca "nasıl yaparım" anlatır (bkz.
# PROJECT_STATE kapsam-dışı). "Öğrenci listemi buraya getir", "toplam kaç kullanıcı
# var" gibi VERİ-çekme/sayım istekleri yanlış bir sayfaya yönlendirilmez; dürüstçe
# "gerçek veriyi getiremem, yalnızca nasıl yapılacağını anlatırım" denir (asla yanlış).
_DATA_FETCH_PATTERNS: tuple[re.Pattern[str], ...] = (
    # Kalıplar ``folded_tokens`` çıktısında çalışır: Türkçe/ASCII yazım aynı
    # sözleşmeye gider ("gerçek" ve "gercek", "öğrenci" ve "ogrenci").
    re.compile(r"\bgercek\b.*\b(?:getir|goster|listele|ver|cek)\w*\b"),
    re.compile(
        r"\b(?:not|karne|puan|devamsiz|yoklama|liste|kayit|kullanici|ogrenci|"
        r"ogretmen|veli|rezervasyon|teslim|sayi)\w*\b.*\b(?:buraya|bana)\b.*"
        r"\b(?:getir|goster|listele|cek)\w*\b"
    ),
    re.compile(
        r"\b(?:buraya|bana)\b.*\b(?:not|karne|puan|devamsiz|yoklama|liste|kayit|"
        r"kullanici|ogrenci|ogretmen|veli|rezervasyon|teslim|sayi)\w*\b.*"
        r"\b(?:getir|goster|listele|cek)\w*\b"
    ),
    re.compile(r"\b(?:buraya|bana)\b.*\b(?:notlarim|karnem|devamsizligim|yoklamam|liste|kayit|sayi)\w*\b.*\bver\w*\b"),
    re.compile(r"\bliste\w*\b.*\b(?:getir|ver|goster|listele)\w*\b"),
    re.compile(r"\b(?:getir|ver|goster|listele)\w*\b.*\bliste\w*\b"),
    # "listeden çıkar" ürün içi silme/kaldırma eylemidir. Yalnız açıkça
    # kayıtlı bir grubun listesini üretme talebi olduğunda "çıkar" veri çekmedir.
    re.compile(r"\bkayitli\w*\b.*\bliste\w*\b.*\bcikar\w*\b"),
    re.compile(r"\btoplam\b.*\bkac\b|\bkac\b.*\btoplam\b"),
    re.compile(r"\bkac\s+(?:kayitli\s+)?(?:kullanici|ogrenci|ogretmen|kisi|veli)\w*\b.*\bvar\b"),
    re.compile(r"\b(?:sistemde|veritabanin\w*|kayitli)\b.*\b(?:kac|sayi\w*|listele|getir|goster)\w*\b"),
    re.compile(r"\b(?:kullanici|ogrenci|ogretmen|kisi|veli)\w*\s+sayi\w*\b.*\b(?:soyle|ver|getir|goster)\w*\b"),
    re.compile(r"\b(?:rezervasyon|teslim|yoklama|kayit)\w*\b.*\bkac\s+kisi\w*\b|\bkac\s+kisi\w*\b.*\b(?:rezervasyon|teslim|yoklama|kayit)\w*\b"),
)

_HOW_TO_DATA_TOKENS: frozenset[str] = frozenset({
    "nasil", "nerede", "nereden", "adim", "adimlar", "ekran", "sayfa",
})
_EXPLICIT_LIVE_DATA_TOKENS: frozenset[str] = frozenset({
    "gercek", "canli", "buraya", "bana", "sistemde", "veritabaninda",
    "kayitli", "toplam",
})

_DATA_FETCH_TOKEN_ALIASES: Final[dict[str, str]] = {
    # Yalnız canlı-veri sınırında kullanılan dar typo düzeltmeleri; normal intent
    # eşleştirmesini global olarak değiştirmez.
    "banna": "bana",
    "gotser": "goster",
    "ckiar": "cikar",
    "ssyisini": "sayisini",
    "ka": "kac",
}


def _is_data_fetch_request(query: str) -> bool:
    tokens = [
        _DATA_FETCH_TOKEN_ALIASES.get(token, token)
        for token in folded_tokens(query)
    ]
    folded = " ".join(tokens)
    # "bana yol göster" / "yol gösterir misin" prosedür yardımıdır; içindeki
    # ``göster`` canlı kayıt gösterme fiili değildir. Kalıpları çalıştırmadan bu
    # kalıp çıkarılır, sorgunun geri kalanındaki gerçek veri talebi korunur.
    fetch_text = re.sub(r"\byol\w*\s+goster\w*\b", " ", folded)
    if not any(pattern.search(fetch_text) for pattern in _DATA_FETCH_PATTERNS):
        return False
    # "Öğrenci listesini hangi ekrandan görürüm?" bir kullanım sorusudur;
    # "gerçek listeyi buraya getir" ise içinde 'adım' geçse bile canlı veri
    # talebidir. Açık canlı-veri işareti yoksa how-to sorusunu engelleme.
    has_how_to = any(
        any(token.startswith(marker) for marker in _HOW_TO_DATA_TOKENS)
        for token in tokens
    )
    has_live_marker = any(
        any(token.startswith(marker) for marker in _EXPLICIT_LIVE_DATA_TOKENS)
        for token in tokens
    )
    return has_live_marker or not has_how_to


# --- Menü bölüm-özeti (section overview) ------------------------------------
# "Öğrenci yönetimi bölümünde ne var", "Okul hizmetleri nedir" gibi ÜST-BAŞLIK
# sorularını yanıtlar. Kaynak: frontend nav-items.ts NAV_GROUPS (birebir + rol notu).
# (folded_phrase, Başlık, [(öğe, path, rol notu), ...])
_SECTION_OVERVIEWS: tuple[tuple[str, str, tuple[tuple[str, str, str], ...]], ...] = (
    ("ogrenci yonetimi", "Öğrenci yönetimi", (
        ("Sınıflar", "/management/classes", "öğretmen+"),
        ("Öğrenci notları", "/management/student-marks", "öğretmen+"),
        ("Öğrenci yoklaması", "/management/student-attendance", "öğretmen+"),
        ("Öğrenci pomodoro", "/management/pomodoros", "öğretmen+"),
        ("Çocuklarım", "/children", "veli"),
    )),
    ("okul hizmetleri", "Okul hizmetleri", (
        ("Yemekler", "/meals", ""),
        ("Ödeme ekstresi", "/payments", "öğrenci/veli"),
    )),
    ("okul yonetimi", "Okul yönetimi", (
        ("Personel mesaisi", "/management/staff-work", "yönetici+"),
        ("Ayarlar", "/management/settings", "yönetici+"),
        ("Dönemler", "/management/terms", "yönetici+"),
        ("Ödemeler", "/management/payments", "yönetici+"),
        ("Kullanıcılar", "/admin/users", "admin"),
    )),
    ("calisma alani", "Çalışma alanı", (
        ("Defter (Notlar)", "/notes", ""),
        ("Beyaz tahtalar", "/whiteboards", "öğrenci+"),
        ("Pomodoro", "/pomodoro", "öğrenci"),
        ("Mesai", "/work", "öğretmen–yönetici"),
    )),
    ("akademik", "Akademik", (
        ("Eğitim (dersler/etüt/kulüp)", "/courses", ""),
        ("Ödevler", "/homework", ""),
        ("Sınavlar", "/exams", ""),
        ("Soru bankası", "/question-bank", "öğretmen+"),
        ("Karnem", "/marks", "öğrenci"),
    )),
    ("planlama", "Planlama", (
        ("Etkinlikler", "/events", ""),
        ("Takvim", "/calendar", ""),
        ("Randevular", "/appointments", ""),
    )),
    ("topluluk", "Topluluk", (
        ("Mesajlar", "/messages", ""),
        ("Sorular", "/questions", ""),
    )),
)
# Bölüm-özeti tetikleyici sözcükler (folded); bölüm adıyla birlikte gelmeli.
_SECTION_TRIGGERS: frozenset[str] = frozenset({
    "ne", "neler", "nedir", "var", "fonksiyon", "fonksiyonlar", "bolum", "bolumu",
    "bolumunde", "icerik", "hangi", "ozellik", "ozellikler", "yapabilir", "yapabilirim",
    "icinde", "kismi", "kisminda", "kisim", "ise", "yarar", "menu", "sayfalar",
})


# Halk dilindeki bölüm adları -> menüdeki resmi grup adı (folded).
# Not: "Eğitim" bir BÖLÜM değil, /courses SAYFASIDIR (nav.classes; dersler+etüt+kulüp);
# onu course_view karşılar (bkz. rules {eğitim}). Burada alias YOK.
_SECTION_ALIASES: tuple[tuple[str, str], ...] = ()


def _section_overview(query: str) -> str | None:
    """Üst-başlık (menü bölümü) sorusu -> o bölümdeki sayfaların özeti (rol notlu)."""

    toks = folded_tokens(query)
    if not toks:
        return None
    folded = " ".join(toks)
    for alias, canonical in _SECTION_ALIASES:
        folded = folded.replace(alias, canonical)
    for phrase, title, items in _SECTION_OVERVIEWS:
        # Tek kelimelik bölüm adları (akademik/planlama/topluluk) için tetikleyici
        # şart; çok-kelimeli net adlar (öğrenci yönetimi...) tek başına yeter.
        multiword = " " in phrase
        # Alt dize değil gerçek token/ifade ara: ``planlamak`` kelimesi menüdeki
        # ``Planlama`` bölümünü tetiklememeli.
        if multiword:
            if not re.search(rf"(?:^|\s){re.escape(phrase)}(?:$|\s)", folded):
                continue
        elif phrase not in toks:
            continue
        if not multiword and not (set(toks) & _SECTION_TRIGGERS):
            continue
        lines = [f"**{title}** bölümünde şunlar var:"]
        for name, path, note in items:
            suffix = f" _{note}_" if note else ""
            lines.append(f"- **{name}** (`{path}`){suffix}")
        lines.append(
            "\nRolüne göre bazı öğeler menüde görünmeyebilir. Hangisini merak "
            "ediyorsan 'nasıl yaparım?' diye sorabilirsin."
        )
        return "\n".join(lines)
    return None


# Tek SAYFA/konu için "ne yapabilirim / ne işe yarar / nedir" -> o konunun ana
# intent'inin KANONİK sorgusuna çevrilir (generic help_capabilities'e düşmez).
# (folded_anahtar_önek, kanonik sorgu). 'sınav' rol-bağımlı (aşağıda ayrı ele alınır).
_TOPIC_HELP: tuple[tuple[str, str], ...] = (
    ("etkinlik", "etkinlikler nerede"),
    # "Eğitim" = /courses sayfası (dersler+etüt+kulüp) -> course_view.
    ("egitim", "derslerim nerede"),
    ("ders", "derslerim nerede"),
    ("odev", "ödevler nerede"),
    ("takvim", "takvim nerede"),
    ("defter", "defterlerim nerede"),
    ("pomodoro", "pomodoro nedir"),
    ("mesaj", "mesaj nasıl gönderirim"),
    ("kullanici", "kullanıcı rolü nasıl değiştirilir"),  # Kullanıcılar sayfası (ADMIN)
    # T1: 'randevu/yemek/tahta ne işe yarar' -> ilgili T1 intent'ine götür
    ("randevu", "randevu nasıl alırım"),
    ("yemek", "yemek menüsü nerede"),
    ("tahta", "beyaz tahtalar nerede"),
    ("yoklama", "yoklamam nerede"),
    ("devamsiz", "devamsızlığımı nasıl görürüm"),
)
_TOPIC_HELP_TRIGGERS: tuple[str, ...] = (
    "yapabil", "nedir", "ise yarar", "ise yariyor", "ne var", "neler var",
    "ne yapilir", "ne ise", "gorevleri", "ozellikleri",
)


def _topic_help_query(query: str, role: str) -> str | None:
    """'<konu> ne yapabilirim/ne işe yarar' -> o konunun kanonik sorgusu (yoksa None).

    Belirli 'nasıl <fiil>' how-to sorularına DOKUNMAZ (onlar zaten doğru gider)."""

    toks = folded_tokens(query)
    if not toks:
        return None
    tokset = set(toks)
    if "nasil" in tokset:  # 'nasıl oluştururum' gibi net how-to -> karışma
        return None
    folded = " ".join(toks)
    if not any(t in folded for t in _TOPIC_HELP_TRIGGERS):
        return None
    # sınav: rol-bağımlı (öğrenci girer, öğretmen+ oluşturur)
    if any(t.startswith("sinav") for t in toks):
        return ("sınav nasıl oluştururum" if role in _UPPER_ROLES
                else "sınava nasıl girerim")
    # ödeme/ücret: rol-bağımlı (yönetici+ Ödemeler'i yönetir; diğerleri kendi ekstresi)
    if any(t.startswith("odeme") or t.startswith("ucret") for t in toks):
        return ("ödeme yönetimi nerede" if role in ("yonetici", "admin")
                else "ödeme bilgilerim nerede")
    for kw, canon in _TOPIC_HELP:
        if any(t.startswith(kw) for t in toks):
            return canon
    return None


# --- Kapsam sınırı: bot adına İŞ YAPMA / VERİ DEĞİŞTİRME isteği ---------------
# Çelebi ne kullanıcı adına ödev/işlem yapar ne de veriyi (not/devamsızlık/yoklama)
# değiştirir/siler; yalnızca "nasıl yaparım" anlatır. "Ödevimi sen yap", "notumu
# yükselt", "devamsızlığımı sil", "sınav cevaplarını ver" gibi manipülasyon/do-for-me
# istekleri yanlış bir sayfaya yönlendirilmez -> dürüstçe "bunu yapamam" (asla yanlış).
_MANIPULATION_PATTERNS: tuple[re.Pattern[str], ...] = (
    # `yerime` gerçekten botun kullanıcı adına işlem yapmasını ister. Çıplak
    # `yerine` ise "silmek yerine ters kayıt aç" gibi meşru karşılaştırmadır.
    re.compile(r"\b(?:benim\s+)?yerime\b"),
    # "Sen ne yapabiliyorsun?" yetenek sorusudur; do-for-me değildir. Bu yüzden
    # yap- fiilinde yalnız istek çekimleri kabul edilir, geniş ``yap\w*`` değil.
    re.compile(r"\bsen\b(?:\s+\w+){0,2}\s+\b(?:yap(?:ar|iver|sana|abilir)?|(?:ayarla|coz|hallet|doldur|gir|olustur|tamamla)\w*)\b"),
    re.compile(r"\bbenim\s+icin\b(?:\s+\w+){0,2}\s+\b(?:yap|coz|doldur|hallet|tamamla)\w*\b"),
    re.compile(r"(?:sinav|soru|test)\w*.*\bcevap\w*.*\b(?:ver|soyle|sizdir|goster)\w*\b"),
    re.compile(r"\bcevap\w*\b\s*\b(?:ver|soyle|sizdir)\w*\b"),
    # 1. şahıs korunan okul verisi + değiştirme fiili. Kişisel Defter'deki
    # "notumu sil/değiştir" meşru CRUD'dur; çıplak not ürün sözlüğünde Defter
    # notu sayılır. Yalnız "notumu yükselt/artır" açıkça puan manipülasyonudur.
    re.compile(r"\b(?:karnem|karnemi|ortalamam\w*|puanim\w*|devamsizligim\w*|"
               r"yoklamam\w*)\b.*\b(?:sil|kaldir|yukselt|artir|duzelt|degistir)\w*\b"),
    re.compile(r"\b(?:sil|kaldir|yukselt|artir|duzelt|degistir)\w*\b.*\b(?:karnem|karnemi|"
               r"devamsizligim\w*|yoklamam\w*|puanim\w*|ortalamam\w*)\b"),
    re.compile(r"\b(?:notum|notumu|notlarim\w*)\b.*\b(?:yukselt|artir)\w*\b"),
    re.compile(r"\b(?:yukselt|artir)\w*\b.*\b(?:notum|notumu|notlarim\w*)\b"),
    re.compile(r"\bvar\s+goster\w*\b"),
)


def _is_manipulation_request(query: str) -> bool:
    tokens = folded_tokens(query)
    folded = " ".join(tokens)
    if any(pattern.search(folded) for pattern in _MANIPULATION_PATTERNS):
        return True

    # Güvenlik-kritik boundary sözcüklerinde TEK yazım hatası. Genel fuzzy
    # normalizasyon değildir: yalnız korunan nesne + tehlikeli eylem çifti aynı
    # sorguda bulunursa devreye girer. Böylece geçerli kısa sözcükler başka
    # intent'e sürüklenmez.
    own_specs = (
        ("devamsizligim", ("im", "imi", "mi")),
        ("yoklamam", ("am", "ami")),
        ("karnem", ("em", "emi")),
        ("puanim", ("im", "imi")),
        ("ortalamam", ("am", "ami")),
    )
    own_protected = any(
        token.endswith(endings) and _near_stem(token, stem)
        for token in tokens
        for stem, endings in own_specs
    )
    destructive = (
        any(token.startswith("sil") or token in {"sl", "sli", "siil", "sdl", "si"}
            for token in tokens)
        or _contains_near_stem(tokens, (
            "kaldir", "cikar", "yukselt", "artir", "duzelt", "degistir",
        ))
    )
    if own_protected and destructive:
        return True
    if (
        any(token.startswith(("notum", "notlarim")) for token in tokens)
        and _contains_near_stem(tokens, ("yukselt", "artir"))
    ):
        return True
    if (
        any(token in {"var", "vra"} for token in tokens)
        and _contains_near_stem(tokens, ("goster",))
        and _contains_near_stem(tokens, ("yoklama",))
        and any(token == "beni" for token in tokens)
    ):
        return True
    # Bu yüzeyler global alias değildir: ``sik`` bağımsız ve geçerli bir
    # sözcük olabilir; ``vre/vet/veer`` de kısa ve belirsizdir. Yalnız açıkça
    # korunan okul verisiyle birlikte geldiğinde tek-harfli eylem yazım hatası
    # olarak değerlendirilir.
    if (
        any(token.startswith("devamsizlig") for token in tokens)
        and any(token == "sik" for token in tokens)
    ):
        return True
    if (
        _contains_near_stem(tokens, ("sinav",))
        and _contains_near_stem(tokens, ("soru",))
        and _contains_near_stem(tokens, ("cevap",))
        and any(token in {"vre", "vet", "veer"} for token in tokens)
    ):
        return True
    if all(
        condition for condition in (
            any(token.startswith("odevim") for token in tokens),
            _contains_near_stem(tokens, ("yerime",)),
            any(token.startswith("yap") for token in tokens),
        )
    ):
        return True
    if (
        any(token == "ders" for token in tokens)
        and any(token.startswith("programim") for token in tokens)
        and any(_near_stem(token, "sen") for token in tokens if len(token) <= 4)
        and _contains_near_stem(tokens, ("ayarla",))
    ):
        return True
    return False


def _near_stem(token: str, stem: str) -> bool:
    """Token başlangıcı stem'e en fazla bir ekleme/silme/değişme uzaklıkta mı?"""

    if token.startswith(stem):
        return True
    for length in (len(stem) - 1, len(stem), len(stem) + 1):
        if length > 0 and len(token) >= length:
            candidate = token[:length]
            if _levenshtein(candidate, stem) <= 1 or _adjacent_transposition(candidate, stem):
                return True
    return False


def _adjacent_transposition(left: str, right: str) -> bool:
    if len(left) != len(right):
        return False
    differences = [
        index for index, (a, b) in enumerate(zip(left, right)) if a != b
    ]
    return (
        len(differences) == 2
        and differences[1] == differences[0] + 1
        and left[differences[0]] == right[differences[1]]
        and left[differences[1]] == right[differences[0]]
    )


def _contains_near_stem(tokens: list[str], stems: tuple[str, ...]) -> bool:
    return any(_near_stem(token, stem) for token in tokens for stem in stems)


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


# Üst rol (öğretmen/yönetici/admin) "kendi karnem/notlarım/sınav sonuçlarım" derse
# kişisel öğrenci sayfası yoktur; çıkmaz "yapılamıyor" yerine ÖĞRENCİ RAPORLARI
# sayfasına yardımcı yönlendirme + buton verir (asla çıkmaz cevap; kullanım kolay).
_UPPER_ROLES: frozenset[str] = frozenset({"ogretmen", "yonetici", "admin"})
_STUDENT_REPORT_REDIRECT: dict[str, str] = {
    "report_card_view": "student_marks_lookup",
    "attendance_view": "student_attendance_lookup",
    "exam_finish_result": "student_marks_lookup",
}


def _upper_role_report_redirect(
    role: str, intent: str | None
) -> tuple[str, dict[str, Any]] | None:
    """Üst rol + öğrenci-görüntüleme intent'i -> (yardımcı metin, yönetim butonu)."""

    if role not in _UPPER_ROLES or intent not in _STUDENT_REPORT_REDIRECT:
        return None
    mgmt = _STUDENT_REPORT_REDIRECT[intent]
    view = get_role_space(role).view_for(mgmt)
    if view is None or view.outcome is not AccessOutcome.ALLOW:
        return None
    route = route_for(mgmt)
    if route is None:
        return None
    path, label = route
    konu = "not/karne" if mgmt == "student_marks_lookup" else "yoklama/devamsızlık"
    text = (
        f"Senin hesabında kişisel {konu} kaydı yok 🙂 Öğrencilerinin bilgilerini "
        f"**{label}** sayfasından (`{path}`) görürsün: öğrenciyi (ve gerekiyorsa "
        f"dersi) seçince ilgili tablo açılır."
    )
    return text, {"route": path, "label": label, "available": True}


# Sosyal cevaplarda (selam/naber/teşekkür) kullanıcının adını doğal biçimde ekler.
# Ad, güvenilir OTURUM bağlamından gelir (session.name) — veri çekme DEĞİL. Ad yoksa
# davranış aynen kalır (graceful). Bridge/backend'in session.name geçmesi gerekir.
_SOCIAL_PERSONALIZE: frozenset[str] = frozenset({"greeting", "smalltalk", "thanks"})


def _first_name(session: Any) -> str | None:
    if not isinstance(session, dict):
        return None
    raw = session.get("name") or session.get("first_name")
    if not isinstance(raw, str):
        return None
    parts = [p for p in raw.strip().split() if p]
    if not parts:
        return None
    name = parts[0]
    # güvenlik: makul uzunluk + yalnız harf/tire/kesme (enjeksiyon/uzun ad engeli)
    if len(name) > 30 or not all(c.isalpha() or c in "-'’" for c in name):
        return None
    return name


def _personalize(intent: str | None, text: str, name: str | None) -> str:
    """Sosyal cevaba adı doğal yerleştirir ('Merhaba!' -> 'Merhaba Kadir!')."""

    if not name or intent not in _SOCIAL_PERSONALIZE or name in text:
        return text
    idx = text.find("!")
    if idx == -1:
        return text
    return text[:idx] + f" {name}" + text[idx:]


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
    # Üst rolün öğrenciye özgü bir rapor sorusu, gerçek bir yönetim raporuna
    # yönlendirilebilir. Bu durumda V2 metadata da özgün (kimi rollerde DENY)
    # görünümü değil, gerçekten sunulan hedef işlemi anlatmalıdır.
    served_intent = intent
    if (
        response_id == "student_report_redirect"
        and role in _UPPER_ROLES
        and isinstance(intent, str)
        and intent in _STUDENT_REPORT_REDIRECT
    ):
        target_intent = _STUDENT_REPORT_REDIRECT[intent]
        target_view = space.view_for(target_intent)
        if target_view is not None and target_view.outcome is AccessOutcome.ALLOW:
            served_intent = target_intent
            view = target_view
    if response_id == "clarification_prompt":
        outcome = "clarify"
        reason_code = "ambiguous_query"
    elif bool(result.get("fallback")):
        outcome = "fallback"
        reason_code = "out_of_scope"
    elif response_id == "out_of_scope_action":
        # Gerçek alan-dışı fallback ile "canlı veriyi getir / benim yerime yap"
        # kapsam sınırını aynı OOS kovasına atma.
        outcome = "deny"
        boundary = str(result.get("scope_boundary") or "action")
        reason_code = "scope_boundary_" + boundary
    elif response_id == "feature_unavailable":
        outcome = "deny"
        reason_code = "feature_unavailable"
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
        "action_id": served_intent,
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
        context_query = _strip_brand_context_prefix(_strip_role_context_prefix(query))
        declared = _declared_role(context_query) or _role_correction(context_query)
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
        effective_query = context_query
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

        # 1.515) Saf UI/söylem/state çerçeveleri çekirdek görevin intent'ini
        # gölgelememeli. Örn. "Profilim sayfasında biyografiyi değiştir" içindeki
        # sayfa etiketi profile_view'i, gerçek değişiklik görevini bastırmamalıdır.
        effective_query = _strip_task_context(effective_query)

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

        # Üçüncü-şahıs özel-ad iyeliği kişisel Defter değil, öğrenci notlandırma
        # bağlamıdır ("Ali'nin notunu düzelt").
        effective_query = rules.canonicalize_named_grade_query(effective_query)
        entry_exit_ambiguous = _entry_exit_is_ambiguous(effective_query)

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
                "scope_boundary": _scope_kind,
            }, role)

        # 1.585) Yüksek-kesinlikli okul-dışı konu. Bu kapı scope-boundary'den
        # SONRA, kural/benzerlikten ÖNCE çalışır: "ödevimi benim yerime yap" özel
        # action reddini korur; "hava nasıl" gibi bir sorgunun ortak kelimelerle
        # yanlış ürün intent'ine bağlanmasını engeller.
        if is_explicitly_out_of_scope(effective_query):
            if self._log_sink is not None:
                self._log_sink({
                    "trace_id": trace_id,
                    "query_masked": safety_mod.mask_pii(query)[0],
                    "role": role,
                    "authenticated": authenticated,
                    "short_circuit": "explicit_out_of_scope",
                    "response_id": FALLBACK["response_id"],
                })
            return _attach_assistant_meta({
                "trace_id": trace_id,
                "response_id": FALLBACK["response_id"],
                "text": _with_brand_note(FALLBACK["response_template"], query),
                "intent": None,
                "confidence": 0.0,
                "fallback": True,
                "auth_action": None,
                "required_role": None,
                "navigation": None,
                "clarification": None,
                "answers": None,
                "suggestions": suggestions,
                "safety": safety_info,
            }, role)

        # 1.59) Menü bölüm-özeti ("Öğrenci yönetimi bölümünde ne var?"): üst-başlık
        # sorusu -> o bölümdeki sayfaların listesi (rol notlu). help_capabilities/
        # clarify'a düşmeden net cevap.
        _section_rule = get_role_space(role).rule_matcher.match(effective_query)
        _section = (
            _section_overview(effective_query)
            if _section_rule is None
            or _section_rule.intent in {"nav_overview", "help_capabilities"}
            else None
        )
        if _section is not None:
            if self._log_sink is not None:
                self._log_sink({
                    "trace_id": trace_id, "query_masked": safety_mod.mask_pii(query)[0],
                    "role": role, "authenticated": authenticated,
                    "short_circuit": "section_overview", "response_id": "section_overview",
                })
            return _attach_assistant_meta({
                "trace_id": trace_id,
                "response_id": "section_overview",
                "text": _with_brand_note(_section, query),
                # Dinamik bölüm metni nav_overview intent'inin ayrıntılı sunumudur;
                # semantik intent'i koru ki log/benchmark/frontend bunu OOS sanmasın.
                "intent": "nav_overview",
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

        # 1.595) Önce gerçek çoklu isteği ve zaten özgül bir kurala çarpan görevi
        # koru. Konu-yardımı yalnız özgül intent yoksa devreye girer; aksi halde
        # "ders notunu düzenle — doğru akış nedir" genel ders görünümüne kayardı.
        segments = _multi_intent_segments(effective_query, role)
        if segments is None:
            existing_rule = get_role_space(role).rule_matcher.match(effective_query)
            if existing_rule is None or existing_rule.intent == "help_capabilities":
                _topic_canon = _topic_help_query(effective_query, role)
                if _topic_canon is not None:
                    effective_query = _topic_canon
                    segments = _multi_intent_segments(effective_query, role)

        # 1.6) Çoklu istek ('X ve Y'): her bağımsız parça ayrı yanıtlanır.
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
        ask_mode = pure_negation or entry_exit_ambiguous or single_word_similarity or (
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
                # Net okul-dışı konu (yalnız benzerlik) -> zayıf-eşleşme FP'sini kes.
                or bool(FAR_OOS_TOPICS.intersection(folded_tokens(effective_query)))
            )
        )
        if ask_mode:
            clarification = _build_clarification(trace, force=True)
            trace["ask_clarification"] = True
            text = (
                ENTRY_EXIT_CLARIFICATION_TEXT
                if entry_exit_ambiguous
                else CLARIFICATION_PROMPT_TEXT
            )
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
        # Üst rol öğrenci-görüntüleme sorunca çıkmaz cevap yerine öğrenci raporları
        # sayfasına yardımcı yönlendirme (metin + buton; auth_action temizlenir).
        _redirect = _upper_role_report_redirect(role, response.intent)
        if _redirect is not None:
            text = _redirect[0]
        # Sosyal cevaba kullanıcının adını ekle (varsa) — "teşekkürler Kadir" gibi.
        text = _personalize(response.intent, text, _first_name(payload.get("session")))
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
            "response_id": "student_report_redirect" if _redirect else response.response_id,
            "text": _with_brand_note(text, query),
            "intent": response.intent,
            "confidence": trace["decision"]["confidence"],
            "fallback": response.fallback,
            "auth_action": None if _redirect else response.auth_action,
            "required_role": None if _redirect else trace["decision"]["required_role"],
            "navigation": _redirect[1] if _redirect else _build_navigation(
                response.intent, response.auth_action, role),
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
