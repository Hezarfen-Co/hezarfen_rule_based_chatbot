"""Deterministik, dengeli ve sözleşme-farkında 10K Çelebi stres benchmarkı.

Yalnız insanların elle etiketlediği ``data/benchmark.jsonl`` sorularını
metamorfik olarak çoğaltır; katalogdaki ``example_questions`` değerlendirme
seed'i değildir. Varsayılan koşu 9.000 uygulama-içi ve 1.000 OOS vaka üretir.

Artefaktlar: sentetik vakalar JSONL, tam Engine sonuçları JSONL, küçük Markdown
özet/index ve 250-500 vakalık kullanıcı-görünür Markdown parçalarıdır. Sentetik
koşu tanısal olarak varsayılan exit 0 kullanır; CI kapısı için ``--strict`` verilir.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Final, Iterable, Iterator, Mapping, Sequence

from src.access import AccessOutcome
from src.catalog import FALLBACK, INTENTS, ROLE_HIERARCHY, route_for
from src.engine import Engine
from src.role_spaces import get_role_space


PROJECT_ROOT: Final[Path] = Path(__file__).resolve().parent
DEFAULT_BENCHMARK_PATH: Final[Path] = PROJECT_ROOT / "data" / "benchmark.jsonl"
DEFAULT_NEAR_OOS_PATH: Final[Path] = PROJECT_ROOT / "data" / "near_oos.jsonl"
DEFAULT_DATA_OUTPUT: Final[Path] = PROJECT_ROOT / "data" / "stress_benchmark.jsonl"
DEFAULT_RESULTS_OUTPUT: Final[Path] = PROJECT_ROOT / "data" / "stress_benchmark_results.jsonl"
DEFAULT_REPORT_OUTPUT: Final[Path] = PROJECT_ROOT / "STRES_BENCHMARK_SONUCLARI.md"

GENERATOR_VERSION: Final[str] = "stress-v3.5.0"
# Generator rapor sürümü değiştiğinde bütün roller/mutasyonlar rastgele yeniden
# dağılmasın. v3.4 dağılımı sabit tabandır; böylece sürümler arası sonuç farkı
# gerçekten kod/jeneratör davranışından gelir.
MUTATION_SEED_VERSION: Final[str] = "stress-v3.4.0"
OOS_LABEL: Final[str] = "oos"
DEFAULT_IN_SCOPE_COUNT: Final[int] = 9_000
DEFAULT_OOS_COUNT: Final[int] = 1_000
DEFAULT_TOTAL_COUNT: Final[int] = DEFAULT_IN_SCOPE_COUNT + DEFAULT_OOS_COUNT
DEFAULT_REPORT_CHUNK_SIZE: Final[int] = 400
MIN_REPORT_CHUNK_SIZE: Final[int] = 250
MAX_REPORT_CHUNK_SIZE: Final[int] = 500

MUTATION_FAMILIES: Final[tuple[str, ...]] = (
    "semantic_paraphrase", "sentence_form", "ui_label_tr_en", "role_context",
    "turkish_ascii", "conversational_filler", "punctuation_case", "single_typo",
    "state_error", "compound",
)
OOS_MUTATION_FAMILIES: Final[tuple[str, ...]] = (
    "semantic_paraphrase", "sentence_form", "role_context", "turkish_ascii",
    "conversational_filler", "punctuation_case", "single_typo", "compound",
)

ROLE_LABELS: Final[dict[str, str]] = {
    "ziyaretci": "Ziyaretçi", "veli": "Veli", "ogrenci": "Öğrenci",
    "ogretmen": "Öğretmen", "yonetici": "Yönetici", "admin": "ADMIN",
}
SOCIAL_INTENTS: Final[frozenset[str]] = frozenset({
    "greeting", "smalltalk", "thanks", "farewell", "bot_identity",
})
_OTHER_PERSON_SAFETY_INTENTS: Final[frozenset[str]] = frozenset({
    "exam_grade_student", "student_marks_lookup", "student_attendance_lookup",
})
_POSSESSIVE_NAME_RE: Final[re.Pattern[str]] = re.compile(
    r"\b[A-ZÇĞİÖŞÜ][a-zçğıöşü]{2,}['’](?:n?in|n?ın|n?un|n?ün)\b"
)
STATE_ERROR_ALWAYS_EXCLUDED: Final[frozenset[str]] = SOCIAL_INTENTS | frozenset({
    "platform_info", "help_capabilities", "guide_info", "roles_permissions",
    "privacy_security", "exam_modes_info", "weighted_average_info",
    "attendance_rate_info", "parent_info", "calendar_info", "today_info",
    "nav_overview", "branches_info", "notification_settings_info",
})

_WORD_RE: Final[re.Pattern[str]] = re.compile(r"[^\W\d_]+", re.UNICODE)
_TRAILING_PUNCTUATION: Final[str] = " \t\r\n?!.,;:…"
_TURKISH_ASCII_TABLE: Final[dict[int, str]] = str.maketrans({
    "ç": "c", "Ç": "C", "ğ": "g", "Ğ": "G", "ı": "i", "İ": "I",
    "ö": "o", "Ö": "O", "ş": "s", "Ş": "S", "ü": "u", "Ü": "U",
    "â": "a", "Â": "A", "î": "i", "Î": "I", "û": "u", "Û": "U",
})

_FILLER_PREFIXES: Final[tuple[str, ...]] = (
    "hocam", "dostum", "rica etsem", "bir şey soracağım", "acaba", "şimdi ben",
    "yardım eder misin", "kısaca", "müsaitsen", "peki", "uygulamada", "Hezarfen'de",
)
_FILLER_SUFFIXES: Final[tuple[str, ...]] = (
    "lütfen", "hangi adımları izlemeliyim", "bir bakar mısın", "nereden başlamalıyım",
    "yardımcı olur musun", "nasıl ilerleyeceğim", "doğru ekran hangisi",
    "bunu açıklayabilir misin", "ne yapmam gerekiyor", "kısaca anlatır mısın",
    "yol gösterir misin", "mümkün mü",
)
_ASCII_PREFIXES: Final[tuple[str, ...]] = (
    "hocam", "lutfen", "uygulamada", "hesabimda", "acaba", "kisa bir soru",
    "yardim", "hezarfende",
)
_ASCII_SUFFIXES: Final[tuple[str, ...]] = (
    "nasil yapilir", "yardim eder misin", "nereden baslamaliyim", "hangi ekranda",
    "bir bakar misin", "ne yapmaliyim", "mumkun mu", "adimlari nedir",
)

_SEMANTIC_REPLACEMENTS: Final[tuple[tuple[re.Pattern[str], tuple[str, ...]], ...]] = (
    (re.compile(r"\bnasıl\b", re.IGNORECASE), ("hangi adımlarla", "ne şekilde", "hangi yolu izleyerek")),
    (re.compile(r"\bnereden\b", re.IGNORECASE), ("hangi ekrandan", "hangi bölümden", "hangi sayfadan")),
    (re.compile(r"\bnerede\b", re.IGNORECASE), ("hangi ekranda", "hangi bölümde", "hangi sayfada")),
    # Fiilden sonra doğrudan kullanılabilen biçimler: "silmek isterim" ve
    # "silmek niyetindeyim". Eski "silmek yapmam gerekiyor" dönüşümü Türkçe
    # değildi ve gerçek bir dayanıklılık testi üretmiyordu.
    (re.compile(r"\bistiyorum\b", re.IGNORECASE), ("isterim", "niyetindeyim")),
    (re.compile(r"\bsilmek\b", re.IGNORECASE), ("kaldırmak", "listeden çıkarmak", "kaydı kaldırmak")),
    (re.compile(r"\bsil\b", re.IGNORECASE), ("kaldır", "listeden çıkar")),
    (re.compile(r"\bdeğiştirmek\b", re.IGNORECASE), ("güncellemek", "düzenlemek")),
    (re.compile(r"\bdüzenlemek\b", re.IGNORECASE), ("güncellemek", "değiştirmek")),
    (re.compile(r"\boluşturmak\b", re.IGNORECASE), ("eklemek", "tanımlamak")),
    (re.compile(r"\beklemek\b", re.IGNORECASE), ("ilave etmek",)),
    (re.compile(r"\bgörmek\b", re.IGNORECASE), ("görüntülemek", "incelemek", "bakmak")),
    (re.compile(r"\bgörüntülemek\b", re.IGNORECASE), ("görmek", "incelemek", "ekranda açmak")),
    (re.compile(r"\bgiremiyorum\b", re.IGNORECASE), ("erişemiyorum", "açamıyorum", "içeri alınmıyorum")),
    (re.compile(r"\bolmuyor\b", re.IGNORECASE), ("çalışmıyor", "tamamlanmıyor", "sonuç vermiyor")),
    (re.compile(r"\bkaydetmek\b", re.IGNORECASE), ("kayda almak", "saklamak", "değişiklikleri uygulamak")),
    (re.compile(r"\bgöndermek\b", re.IGNORECASE), ("teslim etmek", "iletmek", "sisteme yollamak")),
    (re.compile(r"\bkaldırmak\b", re.IGNORECASE), ("listeden çıkarmak", "kaydı silmek")),
)

_SENTENCE_FRAMES: Final[tuple[tuple[str, str], ...]] = (
    ("direct_goal", "Şunu yapmak istiyorum: {q}."),
    ("step_request", "{q}; hangi adımları sırayla izlemeliyim?"),
    ("screen_request", "{q}. Bu işlem hangi ekrandan yapılıyor?"),
    ("how_to", "Hezarfen'de {q} konusunda yol gösterir misin?"),
    ("first_person", "Ben {q_lower}; nereden başlamalıyım?"),
    ("concise", "Kısaca sorayım: {q}?"),
    ("need", "{q} gerekiyor; doğru işlem akışı nedir?"),
    ("where_then", "Önce hangi sayfaya gitmeliyim: {q}?"),
    ("explain", "{q} konusunu adım adım açıklayabilir misin?"),
    ("task", "Yapmak istediğim işlem şu: {q}. Nasıl ilerlerim?"),
    ("new_user", "Uygulamayı yeni kullanıyorum; {q}?"),
    ("short", "{q} — doğru yol nedir?"),
)

# OOS soruları ürün yardımı değildir. Bu çerçeveler kaynak soruyu olduğu gibi
# korur ve ona ekran, menü, işlem akışı veya Hezarfen bağlamı eklemez. Action ve
# data boundary talepleri ayrıca doğrudan talep olarak kalır; bir "nasıl yaparım"
# sorusuna çevrilip istemeden ürün-içi yardım kapsamına sokulmaz.
_OOS_NEUTRAL_FRAMES: Final[dict[str, tuple[tuple[str, str], ...]]] = {
    "fallback": (
        ("curious", "Şunu merak ediyorum: {q}."),
        ("plain_question", "Bir sorum var: {q}?"),
        ("ask_opinion", "{q}; bu konuda ne söyleyebilirsin?"),
        ("request_answer", "Sana şunu sormak istiyorum: {q}."),
        ("topic", "Merak ettiğim konu şu: {q}."),
        ("brief", "Kısaca şunu sorayım: {q}?"),
    ),
    "action": (
        ("direct_action", "Senden şu isteği yerine getirmeni istiyorum: {q}."),
        ("explicit_request", "Talebim şu: {q}."),
        ("perform", "{q}; bunu benim için gerçekleştir."),
        ("imperative", "Şunu doğrudan yap: {q}."),
        ("request", "Yapmanı istediğim şey şu: {q}."),
        ("fulfil", "{q}; bu isteği yerine getir."),
    ),
    "data": (
        ("direct_data", "Senden şu bilgiyi istiyorum: {q}."),
        ("disclose", "{q}; bu bilgiyi benimle paylaş."),
        ("data_request", "İstediğim veri şu: {q}."),
        ("reveal", "Şu bilgiyi bana açıkla: {q}."),
        ("provide_data", "{q}; ilgili veriyi bana ver."),
        ("explicit_data", "Bilgi talebim şu: {q}."),
    ),
}

_OOS_FILLER_PREFIXES: Final[dict[str, tuple[str, ...]]] = {
    "fallback": ("merak ettim", "bir soru soracağım", "acaba", "kısaca", "şunu sorayım"),
    "action": ("açıkça istiyorum", "talebim şu", "doğrudan yap", "lütfen yerine getir", "isteğim şu"),
    "data": ("bilgi talebim var", "açıkça soruyorum", "bu veriyi istiyorum", "lütfen paylaş", "merak ettiğim veri şu"),
}

_OOS_FILLER_SUFFIXES: Final[dict[str, tuple[str, ...]]] = {
    "fallback": ("cevaplar mısın", "ne düşünüyorsun", "bilgi verir misin", "fikrin nedir", "anlatır mısın"),
    "action": ("bu isteği yerine getir", "bunu benim için yap", "talebimi gerçekleştir", "doğrudan uygula", "bunu tamamla"),
    "data": ("bu bilgiyi paylaş", "veriyi bana ver", "bilgiyi açıkla", "bunu benimle paylaş", "talebimi yanıtla"),
}

_OOS_ASCII_PREFIXES: Final[dict[str, tuple[str, ...]]] = {
    kind: tuple(turkish.translate(_TURKISH_ASCII_TABLE) for turkish in values)
    for kind, values in _OOS_FILLER_PREFIXES.items()
}
_OOS_ASCII_SUFFIXES: Final[dict[str, tuple[str, ...]]] = {
    kind: tuple(turkish.translate(_TURKISH_ASCII_TABLE) for turkish in values)
    for kind, values in _OOS_FILLER_SUFFIXES.items()
}

_UI_LABELS: Final[tuple[tuple[re.Pattern[str], str, str], ...]] = (
    (re.compile(r"\bprofil(?:im|i|de|den)?\b", re.IGNORECASE), "Profil", "Profile"),
    (re.compile(r"\bayarlar(?:ı|da|dan)?\b", re.IGNORECASE), "Ayarlar", "Settings"),
    (re.compile(r"\bhesap(?:ta|tan|ım)?\b", re.IGNORECASE), "Hesap", "Account"),
    (re.compile(r"\bdersler(?:de|den|i)?\b", re.IGNORECASE), "Dersler", "Courses"),
    (re.compile(r"\bsınavlar(?:da|dan|ı)?\b", re.IGNORECASE), "Sınavlar", "Exams"),
    (re.compile(r"\bödev(?:ler|de|i)?\b", re.IGNORECASE), "Ödev", "Homework"),
    (re.compile(r"\bmesajlar(?:da|ı)?\b", re.IGNORECASE), "Mesajlar", "Messages"),
    (re.compile(r"\bdefter(?:de|i)?\b", re.IGNORECASE), "Defter", "Notebook"),
    (re.compile(r"\bkaydet\b", re.IGNORECASE), "Kaydet", "Save"),
    (re.compile(r"\bkaldır\b", re.IGNORECASE), "Kaldır", "Remove"),
    (re.compile(r"\bgönder\b", re.IGNORECASE), "Gönder", "Submit"),
    (re.compile(r"\bgiriş\b", re.IGNORECASE), "Giriş", "Login"),
    (re.compile(r"\bçıkış\b", re.IGNORECASE), "Çıkış", "Logout"),
    (re.compile(r"\byoklama\b", re.IGNORECASE), "Yoklama", "Attendance"),
    (re.compile(r"\bkarne(?:m|yi)?\b", re.IGNORECASE), "Karnem", "Report Card"),
    (re.compile(r"\brandevu(?:lar)?\b", re.IGNORECASE), "Randevular", "Appointments"),
)

_PUNCTUATION_STYLES: Final[tuple[tuple[str, str], ...]] = (
    ("lower_questions", "{lower}???"), ("upper_exclaims", "{upper}!!!"),
    ("swapcase_ellipsis", "{swap}..."), ("alternating_mixed", "{alternating}?!"),
    ("lower_spaced", "{lower} ? ! ?"), ("upper_question", "{upper}????"),
    ("quoted", "“{base}?”"), ("parenthesized", "({base})?"),
    ("colon", "Soru: {base}?"), ("dash", "{base} — ?"),
)

_GENERIC_ACTION_ERRORS: Final[tuple[tuple[str, str], ...]] = (
    ("button_disabled", "İlgili işlem düğmesi pasif görünüyor; neden olabilir?"),
    ("save_no_effect", "Kaydet'e bastığım halde değişiklik uygulanmıyor."),
    ("validation", "Formu doldurdum fakat doğrulama hatası alıyorum."),
    ("state_conflict", "İşlem mevcut durum nedeniyle tamamlanamadı uyarısı veriyor."),
    ("stale_screen", "İşlemden sonra liste güncellenmiyor."),
    ("permission", "Butona basınca yetki uyarısı çıkıyor."),
)
_GENERIC_VIEW_ERRORS: Final[tuple[tuple[str, str], ...]] = (
    ("empty_screen", "Sayfa açılıyor fakat kayıtlar boş görünüyor."),
    ("not_visible", "Beklediğim kayıt ekranda görünmüyor."),
    ("loading", "Ekran yükleniyor durumunda kalıyor."),
    ("wrong_scope", "Yalnız bazı kayıtları görebiliyorum; kapsam neden dar?"),
    ("navigation_missing", "Menüde ilgili bölümü bulamıyorum."),
)
_SPECIAL_STATE_ERRORS: Final[dict[str, tuple[tuple[str, str], ...]]] = {
    "account_access_problem": (
        ("invalid_credentials", "Bilgiler doğru görünse de 401 alıyorum."),
        ("registered_no_login", "Kayıt başarılı göründü ama giriş yapamıyorum."),
    ),
    "upload_problem": (
        ("payload_too_large", "Dosya yüklerken 413 hatası alıyorum."),
        ("bad_type", "Dosya türü kabul edilmiyor uyarısı çıkıyor."),
        ("missing_multipart", "Dosya seçili olduğu halde file alanı eksik deniyor."),
        ("attachment_cap", "On birinci eki eklemeye çalışınca işlem reddediliyor."),
    ),
    "chatbot_service_problem": (
        ("service_unavailable", "Çelebi yanıt vermiyor ve 503 görünüyor."),
        ("rate_limit", "Çok istek uyarısıyla 429 alıyorum."),
        ("pending", "Yanıt sürekli pending durumunda kalıyor."),
        ("bridge", "AI bridge bağlı değil uyarısı çıkıyor."),
    ),
    "exam_enter_room": (
        ("not_started", "Başla düğmesi görünmüyor; sınav henüz açılmamış olabilir mi?"),
        ("expired", "Sınav süresi dışında olduğum için odaya alınmıyorum."),
    ),
    "exam_rejoin_retake": (
        ("attempt_limit", "Deneme hakkı tükendi uyarısı alıyorum."),
        ("already_submitted", "Teslim edilmiş sınava yeniden giremiyorum."),
    ),
    "homework_submit": (
        ("deadline", "Teslim tarihi geçti uyarısıyla gönderemiyorum."),
        ("graded_lock", "Notlandırılmış teslimi değiştiremiyorum."),
        ("attachment_cap", "On birinci dosyada ek sınırı hatası çıkıyor."),
    ),
    "appointment_book": (
        ("slot_taken", "Seçtiğim saat artık müsait değil uyarısı veriyor."),
        ("duplicate", "Aynı saat için ikinci talep oluşturamıyorum."),
    ),
    "meal_book": (
        ("insufficient_credit", "Bakiye yetersiz olduğu için rezervasyon olmuyor."),
        ("closed_day", "Geçmiş veya kapalı gün için ayıramıyorum."),
    ),
    "course_remove_student": (
        ("not_enrolled", "Öğrenci listede olmadığı için kaldırılamıyor."),
        ("history_retained", "Öğrenciyi çıkardım ama eski notları hâlâ görünüyor."),
    ),
    "board_view": (
        ("capacity", "Tahtaya katılırken katılımcı sınırı dolu uyarısı çıkıyor."),
        ("loading", "Tahta açılıyor durumunda kalıyor."),
    ),
    "board_create": (
        ("board_closed", "Tahtayı kapattıktan sonra yeniden açamıyorum."),
        ("board_locked", "Tahta kilitli olduğu için düzenleyemiyorum."),
    ),
}

# State/error mutasyonu ancak semptomun aynı intent içinde kalabildiği gerçek bir
# ekran/işlem için üretilir. Intent adındaki ``manage`` gibi parçalardan çıkarım
# yapmak, ``logout_how`` veya ``session_info`` gibi bilgi sorularına "kayıtlar boş"
# ekleyip gold etiketi geçersizleştiriyordu; liste bu nedenle bilinçli ve açıktır.
_STATE_ACTION_INTENTS: Final[frozenset[str]] = frozenset({
    "profile_edit", "personal_settings", "language_theme",
    "course_create", "course_enroll_student", "course_subject_manage",
    "course_note_manage", "course_teacher_manage", "lesson_session_add", "roll_call",
    "exam_create", "exam_add_question", "exam_save_answer", "exam_finish_result",
    "exam_grade_student", "homework_withdraw_submission", "homework_assign",
    "homework_manage", "homework_grade", "event_attendance_mark", "event_create",
    "note_import_ocr", "note_file_manage", "note_create", "note_edit", "note_delete",
    "work_checkin_out", "staff_work_manage", "term_manage", "school_settings",
    "user_role_change", "pomodoro_use", "fees_manage", "class_section_manage",
    "question_bank_manage", "appointment_slot_open", "meal_service_mark",
    "meal_menu_manage", "meal_dietary_profile_manage", "meal_credit_manage",
    "question_ask", "question_solve", "question_approve", "board_create",
})
_STATE_VIEW_INTENTS: Final[frozenset[str]] = frozenset({
    "profile_view", "navigation_help", "course_view", "exam_live_monitor",
    "homework_view", "report_card_view", "student_marks_lookup", "attendance_view",
    "student_attendance_lookup", "event_view", "student_pomodoro_lookup",
    "messages_use", "fees_info", "calendar_info", "today_info",
    "question_bank_info", "exam_schedule_info", "course_materials_info",
    "appointment_requests", "meal_view",
})
STATE_ERROR_ELIGIBLE: Final[frozenset[str]] = frozenset(_SPECIAL_STATE_ERRORS) | _STATE_ACTION_INTENTS | _STATE_VIEW_INTENTS


def _supports_state_error(intent: str | None) -> bool:
    return bool(intent) and intent not in STATE_ERROR_ALWAYS_EXCLUDED and intent in STATE_ERROR_ELIGIBLE

_PII_SECRET_PATTERNS: Final[tuple[tuple[str, re.Pattern[str]], ...]] = (
    ("email", re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)),
    ("phone", re.compile(r"(?<!\d)(?:\+?90[\s.-]?)?0?5\d{2}(?:[\s.-]?\d{3}){2}(?!\d)")),
    ("national_id", re.compile(r"(?<!\d)[1-9]\d{10}(?!\d)")),
    ("api_key", re.compile(r"\b(?:sk|pk|api)[-_][A-Za-z0-9_-]{16,}\b", re.IGNORECASE)),
    ("assigned_secret", re.compile(r"\b(?:api[_ -]?key|access[_ -]?token|bearer|password|parola|şifre)\s*[:=]\s*\S+", re.IGNORECASE)),
    ("private_key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
)


@dataclass(frozen=True)
class Seed:
    question: str
    expected_intent: str
    role: str
    source_dataset: str
    source_index: int
    expected_outcome: str | None = None
    expected_response_ids: tuple[str, ...] = ()
    expected_reason_code: str | None = None
    scope_boundary_type: str | None = None


@dataclass(frozen=True)
class MutationContext:
    seed: Seed
    role: str
    intent: str | None
    family: str
    round_index: int
    variant: int
    ui_label: str | None
    allow_state_error: bool
    scope: str


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line:
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number} geçersiz JSON: {exc}") from exc
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{line_number} JSON nesnesi olmalı.")
            records.append(value)
    return records


def privacy_findings(text: str) -> list[str]:
    return [label for label, pattern in _PII_SECRET_PATTERNS if pattern.search(text)]


def normalise_question_key(text: str) -> str:
    value = unicodedata.normalize("NFKC", text).replace("I", "ı").replace("İ", "i").casefold()
    # Büyük/küçük harf, boşluk ve noktalama stili aynı soruyu yeni vaka yapmaz.
    # Türkçe karakterleri koruruz; ASCII dönüşümü gerçekten ayrı bir robustness
    # varyasyonudur. Alt çizgi de sözcük ayırıcı kabul edilir.
    return " ".join(re.findall(r"[^\W_]+", value, flags=re.UNICODE)).strip()


def _clean_question(value: object, *, source: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{source}: question boş olmayan metin olmalı.")
    question = " ".join(value.split())
    findings = privacy_findings(question)
    if findings:
        raise ValueError(f"{source}: PII/secret bulundu: {', '.join(findings)}")
    return question


def _clean_role(value: object, *, source: str) -> str:
    role = value if isinstance(value, str) else "ziyaretci"
    if role not in ROLE_HIERARCHY:
        raise ValueError(f"{source}: bilinmeyen rol {role!r}.")
    return role


def _optional_string(record: Mapping[str, Any], key: str, source: str) -> str | None:
    value = record.get(key)
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{source}: {key} metin olmalı.")
    return value.strip()


def _response_ids(record: Mapping[str, Any], source: str) -> tuple[str, ...]:
    plural = record.get("expected_response_ids")
    single = record.get("expected_response_id")
    if plural is None:
        values: Sequence[object] = (single,) if single is not None else ()
    elif isinstance(plural, list):
        values = plural
    else:
        raise ValueError(f"{source}: expected_response_ids liste olmalı.")
    cleaned: list[str] = []
    for value in values:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{source}: response_id boş olmayan metin olmalı.")
        if value.strip() not in cleaned:
            cleaned.append(value.strip())
    return tuple(cleaned)


def _scope_boundary_type(record: Mapping[str, Any], reason_code: str | None) -> str | None:
    explicit = record.get("scope_boundary_type") or record.get("scope_boundary")
    if isinstance(explicit, str) and explicit.strip():
        return explicit.strip()
    if reason_code and reason_code.startswith("scope_boundary_"):
        return reason_code.removeprefix("scope_boundary_")
    return None


def _seed_from_record(record: Mapping[str, Any], *, dataset: str, index: int, require_oos: bool = False) -> Seed:
    source = f"{dataset}:{index}"
    expected = record.get("expected_intent", OOS_LABEL if require_oos else None)
    if not isinstance(expected, str) or not expected:
        raise ValueError(f"{source}: expected_intent zorunlu.")
    if require_oos and expected != OOS_LABEL:
        raise ValueError(f"{source}: near-OOS expected_intent='oos' olmalı.")
    known = {item["intent"] for item in INTENTS}
    if expected != OOS_LABEL and expected not in known:
        raise ValueError(f"{source}: katalog dışı intent {expected!r}.")
    reason_code = _optional_string(record, "expected_reason_code", source)
    return Seed(
        question=_clean_question(record.get("question"), source=source),
        expected_intent=expected,
        role=_clean_role(record.get("role"), source=source),
        source_dataset=dataset,
        source_index=index,
        expected_outcome=_optional_string(record, "expected_outcome", source),
        expected_response_ids=_response_ids(record, source),
        expected_reason_code=reason_code,
        scope_boundary_type=_scope_boundary_type(record, reason_code),
    )


def _deduplicate_seeds(seeds: Iterable[Seed]) -> list[Seed]:
    output: list[Seed] = []
    seen: set[tuple[str, str, str, str | None]] = set()
    for seed in seeds:
        key = (normalise_question_key(seed.question), seed.role, seed.expected_intent, seed.expected_outcome)
        if key not in seen:
            seen.add(key)
            output.append(seed)
    return output


def load_source_seeds(
    benchmark_path: str | Path = DEFAULT_BENCHMARK_PATH,
    near_oos_path: str | Path = DEFAULT_NEAR_OOS_PATH,
) -> tuple[list[Seed], list[Seed]]:
    """Yalnız benchmark ve near-OOS yükler; katalog örneklerini seed yapmaz."""
    in_scope: list[Seed] = []
    oos: list[Seed] = []
    for index, record in enumerate(_read_jsonl(Path(benchmark_path)), start=1):
        seed = _seed_from_record(record, dataset="benchmark", index=index)
        (oos if seed.expected_intent == OOS_LABEL else in_scope).append(seed)
    for index, record in enumerate(_read_jsonl(Path(near_oos_path)), start=1):
        oos.append(_seed_from_record(record, dataset="near_oos", index=index, require_oos=True))
    in_scope = _deduplicate_seeds(in_scope)
    oos = _deduplicate_seeds(oos)
    if not in_scope:
        raise ValueError("Uygulama-içi üretim için elle etiketli seed bulunamadı.")
    if not oos:
        raise ValueError("OOS üretim için elle etiketli seed bulunamadı.")
    return in_scope, oos


def turkish_ascii(text: str) -> str:
    translated = text.translate(_TURKISH_ASCII_TABLE)
    decomposed = unicodedata.normalize("NFKD", translated)
    return decomposed.encode("ascii", "ignore").decode("ascii")


def _base(text: str) -> str:
    return " ".join(text.split()).rstrip(_TRAILING_PUNCTUATION)


def _stable_int(*parts: object) -> int:
    raw = "\x1f".join(str(part) for part in parts).encode("utf-8")
    return int.from_bytes(hashlib.sha256(raw).digest()[:8], "big")


def _variant_for(seed: Seed, round_index: int, family: str, role: str) -> int:
    return _stable_int(
        MUTATION_SEED_VERSION, seed.source_dataset, seed.source_index, seed.question,
        round_index, family, role,
    )


def _is_information_intent(intent: str | None) -> bool:
    if not intent:
        return False
    return (
        intent in SOCIAL_INTENTS
        or intent.endswith(("_info", "_view", "_lookup"))
        or intent in {
            "platform_info", "guide_info", "help_capabilities", "roles_permissions",
            "privacy_security", "nav_overview", "navigation_help", "profile_view",
            "branches_info", "today_info", "course_materials_info",
            "notification_settings_info",
        }
    )


def _semantic_variant(ctx: MutationContext) -> tuple[str, list[str], dict[str, Any]]:
    base = _base(ctx.seed.question)
    applicable = [item for item in _SEMANTIC_REPLACEMENTS if item[0].search(base)]
    if applicable:
        pattern, alternatives = applicable[ctx.variant % len(applicable)]
        replacement = alternatives[(ctx.variant // max(1, len(applicable))) % len(alternatives)]
        out, count = pattern.subn(replacement, base, count=1)
        return out, ["semantic_paraphrase"], {
            "strategy": "lexical_replacement", "pattern": pattern.pattern,
            "replacement": replacement, "replacement_count": count, "variant": ctx.variant,
        }
    if ctx.intent in SOCIAL_INTENTS:
        frames = (
            "Şunu sorayım: {q}?",
            "Kısaca: {q}.",
            "Sohbet arasında merak ettim: {q}?",
            "Bir şey soracağım: {q}.",
        )
    elif _is_information_intent(ctx.intent):
        frames = (
            "{q} hakkında bilgi verir misin?",
            "Şunu öğrenmek istiyorum: {q}.",
            "Merak ettiğim konu: {q}.",
            "{q}; bunu açıklayabilir misin?",
        )
    else:
        frames = (
        "{q} konusunda hangi yolu izlemeliyim?",
        "{q}; bunu uygulamada hangi adımlarla yaparım?",
        "Amacım şu: {q}. Bana işlem yolunu anlatır mısın?",
        "{q} için izlenecek doğru akış nedir?",
        "Hezarfen'de {q} işlemini yapmak istiyorum.",
        "{q} konusunu farklı bir ifadeyle soruyorum; nasıl ilerlerim?",
        )
    frame = frames[ctx.variant % len(frames)]
    return frame.format(q=base), ["semantic_paraphrase"], {
        "strategy": "meaning_preserving_frame", "frame": frame, "variant": ctx.variant,
    }


def _sentence_variant(ctx: MutationContext) -> tuple[str, list[str], dict[str, Any]]:
    frames = (
        (("plain", "{q}?"), ("curious", "Şunu merak ettim: {q}."),
         ("chat", "Sohbet arasında sorayım: {q}?"), ("concise", "Kısaca: {q}."))
        if ctx.intent in SOCIAL_INTENTS else _SENTENCE_FRAMES
    )
    label, frame = frames[ctx.variant % len(frames)]
    base = _base(ctx.seed.question)
    return frame.format(q=base, q_lower=base[:1].lower() + base[1:]), ["sentence_form"], {
        "frame": label, "variant": ctx.variant,
    }


def _oos_semantics(ctx: MutationContext) -> str:
    """OOS talebinin fallback/action/data anlam sınıfını döndür."""

    boundary = (ctx.seed.scope_boundary_type or "").strip().casefold()
    if boundary == "action":
        return "action"
    if boundary == "data":
        return "data"
    return "fallback"


def _oos_neutral_frame(ctx: MutationContext) -> tuple[str, str, str]:
    semantics = _oos_semantics(ctx)
    frames = _OOS_NEUTRAL_FRAMES[semantics]
    label, frame = frames[ctx.variant % len(frames)]
    return frame.format(q=_base(ctx.seed.question)), label, semantics


def _oos_semantic_variant(ctx: MutationContext) -> tuple[str, list[str], dict[str, Any]]:
    out, label, semantics = _oos_neutral_frame(ctx)
    return out, ["semantic_paraphrase"], {
        "strategy": "neutral_scope_frame", "frame": label,
        "boundary_semantics": semantics, "variant": ctx.variant,
    }


def _oos_sentence_variant(ctx: MutationContext) -> tuple[str, list[str], dict[str, Any]]:
    out, label, semantics = _oos_neutral_frame(ctx)
    return out, ["sentence_form"], {
        "frame": label, "scope_framing": "neutral_oos",
        "boundary_semantics": semantics, "variant": ctx.variant,
    }


def _ui_variant(ctx: MutationContext) -> tuple[str, list[str], dict[str, Any]]:
    base = _base(ctx.seed.question)
    matches = [item for item in _UI_LABELS if item[0].search(base)]
    if matches:
        pattern, tr_label, en_label = matches[ctx.variant % len(matches)]
        styles = (f"{tr_label} ({en_label})", f"{tr_label}/{en_label}", f"{en_label} [{tr_label}]")
        replacement = styles[(ctx.variant // max(1, len(matches))) % len(styles)]
        out, _ = pattern.subn(replacement, base, count=1)
        return out, ["ui_label_tr_en"], {
            "strategy": "inline_label", "tr": tr_label, "en": en_label,
            "replacement": replacement, "variant": ctx.variant,
        }
    label = ctx.ui_label or "ilgili"
    frames = (
        "Arayüzde {label} ekranındayım; {q}?",
        "Türkçe/English arayüzde {label} sayfasında {q}?",
        "UI etiketi {label} olarak görünüyor. {q}?",
    )
    frame = frames[ctx.variant % len(frames)]
    return frame.format(label=label, q=base), ["ui_label_tr_en"], {
        "strategy": "screen_context", "label": label, "frame": frame, "variant": ctx.variant,
    }


def _role_variant(ctx: MutationContext) -> tuple[str, list[str], dict[str, Any]]:
    role = ROLE_LABELS[ctx.role]
    base = _base(ctx.seed.question)
    frames = (
        "{role} hesabımla {q}?", "Oturum rolüm {role}; {q}?",
        "{role} olarak şunu yapmak istiyorum: {q}.", "Ben {role} rolündeyim. {q}?",
        "{role} panelinden soruyorum: {q}?", "Hesabım {role} yetkisinde; {q}?",
    )
    frame = frames[ctx.variant % len(frames)]
    return frame.format(role=role, q=base), ["role_context"], {
        "frame": frame, "served_role": ctx.role, "variant": ctx.variant,
    }


def _oos_role_variant(ctx: MutationContext) -> tuple[str, list[str], dict[str, Any]]:
    role = ROLE_LABELS[ctx.role]
    base = _base(ctx.seed.question)
    semantics = _oos_semantics(ctx)
    role_frames = {
        "fallback": (
            ("identity", "{role} olduğumu belirteyim: {q}?"),
            ("speaking_as", "Bir {role} olarak soruyorum: {q}?"),
            ("context", "Durumumu belirteyim, ben {role} rolündeyim: {q}."),
            ("perspective", "{role} açısından şunu soruyorum: {q}?"),
            ("plain", "Ben {role}; sorum şu: {q}?"),
            ("preface", "Ön bilgi: Rolüm {role}. {q}?"),
        ),
        "action": (
            ("identity_action", "{role} olduğumu belirteyim. Talebim: {q}."),
            ("speaking_as_action", "Bir {role} olarak senden şunu yapmanı istiyorum: {q}."),
            ("context_action", "Durumumu belirteyim, ben {role} rolündeyim. Şunu yap: {q}."),
            ("perspective_action", "{role} olarak doğrudan talebim şu: {q}."),
            ("plain_action", "Ben {role}; şu isteği yerine getir: {q}."),
            ("preface_action", "Ön bilgi: Rolüm {role}. Yapmanı istediğim şey: {q}."),
        ),
        "data": (
            ("identity_data", "{role} olduğumu belirteyim. Şu bilgiyi istiyorum: {q}."),
            ("speaking_as_data", "Bir {role} olarak şu veriyi talep ediyorum: {q}."),
            ("context_data", "Durumumu belirteyim, ben {role} rolündeyim. Bilgi talebim: {q}."),
            ("perspective_data", "{role} olarak doğrudan veri talebim şu: {q}."),
            ("plain_data", "Ben {role}; şu bilgiyi benimle paylaş: {q}."),
            ("preface_data", "Ön bilgi: Rolüm {role}. İstediğim veri: {q}."),
        ),
    }
    frames = role_frames[semantics]
    label, frame = frames[ctx.variant % len(frames)]
    return frame.format(role=role, q=base), ["role_context"], {
        "frame": label, "served_role": ctx.role, "scope_framing": "neutral_oos",
        "boundary_semantics": semantics, "variant": ctx.variant,
    }


def _ascii_variant(ctx: MutationContext) -> tuple[str, list[str], dict[str, Any]]:
    base = turkish_ascii(_base(ctx.seed.question))
    prefix = _ASCII_PREFIXES[ctx.variant % len(_ASCII_PREFIXES)]
    suffix = _ASCII_SUFFIXES[(ctx.variant // len(_ASCII_PREFIXES)) % len(_ASCII_SUFFIXES)]
    mode = (ctx.variant // (len(_ASCII_PREFIXES) * len(_ASCII_SUFFIXES))) % 4
    if mode == 0:
        out = f"{prefix} {base}?"
    elif mode == 1:
        out = f"{base}; {suffix}?"
    elif mode == 2:
        out = f"{prefix}, {base}; {suffix}?"
    else:
        out = f"{base}... {suffix}"
    return turkish_ascii(out), ["turkish_ascii"], {
        "mode": mode, "prefix": prefix, "suffix": suffix, "variant": ctx.variant,
    }


def _oos_ascii_variant(ctx: MutationContext) -> tuple[str, list[str], dict[str, Any]]:
    semantics = _oos_semantics(ctx)
    base = turkish_ascii(_base(ctx.seed.question))
    prefixes = _OOS_ASCII_PREFIXES[semantics]
    suffixes = _OOS_ASCII_SUFFIXES[semantics]
    prefix = prefixes[ctx.variant % len(prefixes)]
    suffix = suffixes[(ctx.variant // len(prefixes)) % len(suffixes)]
    mode = (ctx.variant // (len(prefixes) * len(suffixes))) % 4
    if mode == 0:
        out = f"{prefix}: {base}?"
    elif mode == 1:
        out = f"{base}; {suffix}."
    elif mode == 2:
        out = f"{prefix}, {base}; {suffix}."
    else:
        out = f"{base}... {suffix}."
    return turkish_ascii(out), ["turkish_ascii"], {
        "mode": mode, "prefix": prefix, "suffix": suffix,
        "scope_framing": "neutral_oos", "boundary_semantics": semantics,
        "variant": ctx.variant,
    }


def _filler_variant(ctx: MutationContext) -> tuple[str, list[str], dict[str, Any]]:
    base = _base(ctx.seed.question)
    prefix = _FILLER_PREFIXES[ctx.variant % len(_FILLER_PREFIXES)]
    suffix = _FILLER_SUFFIXES[(ctx.variant // len(_FILLER_PREFIXES)) % len(_FILLER_SUFFIXES)]
    mode = (ctx.variant // (len(_FILLER_PREFIXES) * len(_FILLER_SUFFIXES))) % 4
    if mode == 0:
        out = f"{prefix}, {base}?"
    elif mode == 1:
        out = f"{base}; {suffix}?"
    elif mode == 2:
        out = f"{prefix}, {base}; {suffix}?"
    else:
        out = f"{prefix} — {base}. {suffix}?"
    return out, ["conversational_filler"], {
        "mode": mode, "prefix": prefix, "suffix": suffix, "variant": ctx.variant,
    }


def _oos_filler_variant(ctx: MutationContext) -> tuple[str, list[str], dict[str, Any]]:
    semantics = _oos_semantics(ctx)
    base = _base(ctx.seed.question)
    prefixes = _OOS_FILLER_PREFIXES[semantics]
    suffixes = _OOS_FILLER_SUFFIXES[semantics]
    prefix = prefixes[ctx.variant % len(prefixes)]
    suffix = suffixes[(ctx.variant // len(prefixes)) % len(suffixes)]
    mode = (ctx.variant // (len(prefixes) * len(suffixes))) % 4
    if mode == 0:
        out = f"{prefix}: {base}?"
    elif mode == 1:
        out = f"{base}; {suffix}."
    elif mode == 2:
        out = f"{prefix}, {base}; {suffix}."
    else:
        out = f"{prefix} — {base}. {suffix}."
    return out, ["conversational_filler"], {
        "mode": mode, "prefix": prefix, "suffix": suffix,
        "scope_framing": "neutral_oos", "boundary_semantics": semantics,
        "variant": ctx.variant,
    }


def _alternating_case(text: str) -> str:
    upper = True
    output: list[str] = []
    for char in text:
        if char.isalpha():
            output.append(char.upper() if upper else char.lower())
            upper = not upper
        else:
            output.append(char)
    return "".join(output)


def _punctuation_variant(ctx: MutationContext) -> tuple[str, list[str], dict[str, Any]]:
    base = _base(ctx.seed.question)
    label, frame = _PUNCTUATION_STYLES[ctx.variant % len(_PUNCTUATION_STYLES)]
    out = frame.format(base=base, lower=base.lower(), upper=base.upper(), swap=base.swapcase(), alternating=_alternating_case(base))
    return out, ["punctuation_case"], {"style": label, "variant": ctx.variant}


def _replacement_for(char: str) -> str:
    neighbors = {
        "a": "s", "b": "v", "c": "v", "ç": "c", "d": "s", "e": "r",
        "f": "g", "g": "h", "ğ": "g", "h": "j", "ı": "i", "i": "o",
        "j": "k", "k": "l", "l": "k", "m": "n", "n": "m", "o": "p",
        "ö": "o", "p": "o", "r": "t", "s": "d", "ş": "s", "t": "y",
        "u": "ı", "ü": "u", "v": "b", "y": "u", "z": "x",
    }
    replacement = neighbors.get(char.casefold(), "x")
    return replacement.upper() if char.isupper() else replacement


def _single_typo(text: str, variant: int) -> tuple[str, dict[str, Any]]:
    base = _base(text)
    words = [match for match in _WORD_RE.finditer(base) if len(match.group(0)) >= 2]
    if not words:
        return base + "x", {"operation": "insert", "index": len(base), "before": "", "after": "x"}
    operation = ("delete", "duplicate", "transpose", "substitute")[variant % 4]
    word = words[(variant // 4) % len(words)]
    relative = 1 + ((variant // max(1, 4 * len(words))) % (len(word.group(0)) - 1))
    index = word.start() + relative
    if operation == "delete":
        out = base[:index] + base[index + 1:]
        detail = {"operation": operation, "index": index, "before": base[index], "after": ""}
    elif operation == "duplicate":
        char = base[index]
        out = base[:index] + char + base[index:]
        detail = {"operation": operation, "index": index, "before": char, "after": char * 2}
    elif operation == "transpose" and index + 1 < word.end() and base[index] != base[index + 1]:
        pair = base[index:index + 2]
        out = base[:index] + pair[::-1] + base[index + 2:]
        detail = {"operation": operation, "index": index, "before": pair, "after": pair[::-1]}
    else:
        char = base[index]
        replacement = _replacement_for(char)
        out = base[:index] + replacement + base[index + 1:]
        detail = {"operation": "substitute", "index": index, "before": char, "after": replacement}
    return out, detail


def _typo_variant(ctx: MutationContext) -> tuple[str, list[str], dict[str, Any]]:
    out, detail = _single_typo(ctx.seed.question, ctx.variant)
    return out, ["single_typo"], {"typo": detail, "typo_count": 1, "variant": ctx.variant}


def _state_frames(intent: str | None) -> tuple[tuple[str, str], ...]:
    if not _supports_state_error(intent):
        return ()
    if intent in _SPECIAL_STATE_ERRORS:
        return _SPECIAL_STATE_ERRORS[intent]
    if intent in _STATE_ACTION_INTENTS:
        return _GENERIC_ACTION_ERRORS
    return _GENERIC_VIEW_ERRORS


def _state_variant(ctx: MutationContext) -> tuple[str, list[str], dict[str, Any]]:
    if not ctx.allow_state_error or not _supports_state_error(ctx.intent):
        raise ValueError(f"{ctx.intent}: state/error ailesi bu intent için uygun değil.")
    frames = _state_frames(ctx.intent)
    label, detail = frames[ctx.variant % len(frames)]
    return f"{_base(ctx.seed.question)}. {detail}", ["state_error"], {
        "state": label, "detail": detail, "variant": ctx.variant,
    }


def _compound_variant(ctx: MutationContext) -> tuple[str, list[str], dict[str, Any]]:
    semantic_ctx = MutationContext(
        seed=ctx.seed, role=ctx.role, intent=ctx.intent, family="semantic_paraphrase",
        round_index=ctx.round_index, variant=ctx.variant, ui_label=ctx.ui_label,
        allow_state_error=ctx.allow_state_error, scope=ctx.scope,
    )
    mode_count = 5 if ctx.allow_state_error and _supports_state_error(ctx.intent) else 4
    mode = ctx.variant % mode_count
    if mode == 0:
        # Typo yalnız insanın yazdığı çekirdek soruya uygulanır; jeneratörün kendi
        # "Hezarfen'de / işlem yolu" çerçevesini bozmak ölçümü kirletir.
        typo_core, typo_meta = _single_typo(ctx.seed.question, ctx.variant // max(1, mode_count))
        typo_ctx = replace(semantic_ctx, seed=replace(ctx.seed, question=typo_core))
        first, _, semantic_meta = _semantic_variant(typo_ctx)
        out = f"{_FILLER_PREFIXES[ctx.variant % len(_FILLER_PREFIXES)]}, {first}?"
        transforms = ["semantic_paraphrase", "single_typo", "conversational_filler"]
        extra = {"typo": typo_meta, "typo_count": 1}
    elif mode == 1:
        first, _, semantic_meta = _semantic_variant(semantic_ctx)
        out = turkish_ascii(first) + "; " + _ASCII_SUFFIXES[ctx.variant % len(_ASCII_SUFFIXES)] + "?"
        transforms = ["semantic_paraphrase", "turkish_ascii", "sentence_form"]
        extra = {"ascii": True}
    elif mode == 2:
        first, _, semantic_meta = _semantic_variant(semantic_ctx)
        out = f"{ROLE_LABELS[ctx.role]} hesabımla, {first}; {_FILLER_SUFFIXES[ctx.variant % len(_FILLER_SUFFIXES)]}?"
        transforms = ["semantic_paraphrase", "role_context", "conversational_filler"]
        extra = {"served_role": ctx.role}
    elif mode == 3:
        first, _, semantic_meta = _semantic_variant(semantic_ctx)
        out = f"Soru: {_alternating_case(first)}?!"
        transforms = ["semantic_paraphrase", "punctuation_case"]
        extra = {"style": "alternating_mixed"}
    else:
        first, _, semantic_meta = _semantic_variant(semantic_ctx)
        frames = _state_frames(ctx.intent)
        state_label, detail = frames[(ctx.variant // mode_count) % len(frames)]
        out = f"{first}. {detail}"
        transforms = ["semantic_paraphrase", "state_error"]
        extra = {"state": state_label, "detail": detail}
    return out, transforms, {"mode": mode, "semantic": semantic_meta, "variant": ctx.variant, **extra}


def _oos_compound_variant(ctx: MutationContext) -> tuple[str, list[str], dict[str, Any]]:
    semantics = _oos_semantics(ctx)
    neutral, frame_label, _ = _oos_neutral_frame(ctx)
    mode = ctx.variant % 5
    if mode == 0:
        mutated, typo_meta = _single_typo(neutral, ctx.variant // 5)
        out = mutated
        transforms = ["semantic_paraphrase", "single_typo"]
        extra: dict[str, Any] = {"typo": typo_meta, "typo_count": 1}
    elif mode == 1:
        suffixes = _OOS_ASCII_SUFFIXES[semantics]
        out = f"{turkish_ascii(neutral)} {suffixes[ctx.variant % len(suffixes)]}."
        transforms = ["semantic_paraphrase", "turkish_ascii"]
        extra = {"ascii": True}
    elif mode == 2:
        role = ROLE_LABELS[ctx.role]
        out = f"Bir {role} olarak soruyorum: {neutral}"
        transforms = ["semantic_paraphrase", "role_context"]
        extra = {"served_role": ctx.role}
    elif mode == 3:
        out = f"Soru: {_alternating_case(neutral)}?!"
        transforms = ["semantic_paraphrase", "punctuation_case"]
        extra = {"style": "alternating_mixed"}
    else:
        prefixes = _OOS_FILLER_PREFIXES[semantics]
        suffixes = _OOS_FILLER_SUFFIXES[semantics]
        out = (
            f"{prefixes[ctx.variant % len(prefixes)]}, {neutral} "
            f"{suffixes[(ctx.variant // len(prefixes)) % len(suffixes)]}."
        )
        transforms = ["semantic_paraphrase", "conversational_filler"]
        extra = {"neutral_filler": True}
    return out, transforms, {
        "mode": mode, "semantic_frame": frame_label,
        "scope_framing": "neutral_oos", "boundary_semantics": semantics,
        "variant": ctx.variant, **extra,
    }


_TRANSFORMERS: Final[Mapping[str, Any]] = {
    "semantic_paraphrase": _semantic_variant, "sentence_form": _sentence_variant,
    "ui_label_tr_en": _ui_variant, "role_context": _role_variant,
    "turkish_ascii": _ascii_variant, "conversational_filler": _filler_variant,
    "punctuation_case": _punctuation_variant, "single_typo": _typo_variant,
    "state_error": _state_variant, "compound": _compound_variant,
}

_OOS_TRANSFORMERS: Final[Mapping[str, Any]] = {
    "semantic_paraphrase": _oos_semantic_variant,
    "sentence_form": _oos_sentence_variant,
    "role_context": _oos_role_variant,
    "turkish_ascii": _oos_ascii_variant,
    "conversational_filler": _oos_filler_variant,
    # Noktalama ve tek yazım hatası kaynak anlamına ürün bağlamı eklemez.
    "punctuation_case": _punctuation_variant,
    "single_typo": _typo_variant,
    "compound": _oos_compound_variant,
}


def _ui_context(intent: str, seed_question: str) -> tuple[bool, str | None]:
    route = route_for(intent)
    label = route[1] if route else None
    return route is not None or any(pattern.search(seed_question) for pattern, _, _ in _UI_LABELS), label


def _eligible_families(intent: str, seed_question: str) -> tuple[str, ...]:
    has_ui, _ = _ui_context(intent, seed_question)
    return tuple(
        family for family in MUTATION_FAMILIES
        if not (family == "state_error" and not _supports_state_error(intent))
        and not (family == "ui_label_tr_en" and not has_ui)
    )


def _policy_roles(intent: str) -> dict[str, tuple[str, ...]]:
    groups: dict[str, list[str]] = defaultdict(list)
    for role in ROLE_HIERARCHY:
        redirect = _report_redirect(role, intent)
        view = redirect[1] if redirect is not None else get_role_space(role).view_for(intent)
        if view is None:
            raise ValueError(f"{role}:{intent} rol görünümü bulunamadı.")
        groups[view.outcome.value].append(role)
    ordered: dict[str, tuple[str, ...]] = {}
    for outcome in (AccessOutcome.ALLOW.value, AccessOutcome.DENY.value):
        if groups.get(outcome):
            ordered[outcome] = tuple(groups[outcome])
    for outcome in sorted(set(groups).difference(ordered)):
        ordered[outcome] = tuple(groups[outcome])
    return ordered


_UPPER_ROLES: Final[frozenset[str]] = frozenset({"ogretmen", "yonetici", "admin"})
_REPORT_REDIRECTS: Final[dict[str, str]] = {
    "report_card_view": "student_marks_lookup",
    "attendance_view": "student_attendance_lookup",
    "exam_finish_result": "student_marks_lookup",
}


def _report_redirect(role: str, intent: str):
    """Gerçekte sunulabilen üst-rol rapor hedefini ve görünümünü döndür."""

    if role not in _UPPER_ROLES or intent not in _REPORT_REDIRECTS:
        return None
    target_intent = _REPORT_REDIRECTS[intent]
    target_view = get_role_space(role).view_for(target_intent)
    target_route = route_for(target_intent)
    if (
        target_view is None
        or target_view.outcome is not AccessOutcome.ALLOW
        or target_route is None
    ):
        return None
    return target_intent, target_view, target_route


def _expected_in_scope_contract(seed: Seed, role: str) -> tuple[dict[str, Any], dict[str, Any]]:
    intent = seed.expected_intent
    source_view = get_role_space(role).view_for(intent)
    if source_view is None:
        raise ValueError(f"{role}:{intent} rol görünümü bulunamadı.")
    redirect = _report_redirect(role, intent)
    served_intent = redirect[0] if redirect is not None else intent
    view = redirect[1] if redirect is not None else source_view
    policy = {
        "outcome": view.outcome.value, "action_id": view.action_id,
        "scope": view.scope.value if view.scope else None,
        "reason_code": view.reason_code.value, "route_key": view.route_key,
    }
    outcome = view.outcome.value
    auth_action = None
    if view.outcome is AccessOutcome.DENY:
        auth_action = "login_required" if role == "ziyaretci" else "role_insufficient"
    response_ids = list(seed.expected_response_ids or (source_view.response_id,))
    route = route_for(intent)
    legacy_route = route[0] if view.outcome is AccessOutcome.ALLOW and route else None
    if intent in {"report_card_view", "attendance_view"} and role != "ogrenci":
        legacy_route = None
    if redirect is not None:
        outcome, auth_action = "allow", None
        response_ids, legacy_route = ["student_report_redirect"], redirect[2][0]
    # Bölüm başlığı kısa devresi aynı nav intent'inin geçerli sunumudur.
    if intent == "nav_overview":
        response_ids.append("section_overview")
    expected = {
        "intent": intent, "outcome": outcome, "meta_outcome": outcome,
        "meta_action_id": served_intent,
        "response_ids": response_ids, "auth_action": auth_action, "fallback": False,
        "navigation_route": legacy_route if auth_action is None else None,
        "meta_route_key": view.route_key if outcome == "allow" else None,
        "reason_code": view.reason_code.value,
    }
    return expected, policy


def _expected_oos_contract(seed: Seed) -> tuple[dict[str, Any], dict[str, Any]]:
    outcome = seed.expected_outcome or "fallback"
    response_ids = list(seed.expected_response_ids)
    if not response_ids:
        response_ids = [FALLBACK["response_id"] if outcome == "fallback" else "out_of_scope_action"]
    reason_code = seed.expected_reason_code or ("out_of_scope" if outcome == "fallback" else seed.scope_boundary_type)
    expected = {
        "intent": None, "outcome": outcome, "meta_outcome": outcome,
        "meta_action_id": None,
        "response_ids": response_ids, "auth_action": None,
        "fallback": outcome == "fallback", "navigation_route": None,
        "meta_route_key": None, "reason_code": reason_code,
    }
    policy = {
        "outcome": outcome, "action_id": None, "scope": seed.scope_boundary_type,
        "reason_code": reason_code, "route_key": None,
    }
    return expected, policy


def _expected_other_person_safety_contract(
    intent: str, role: str, question: str,
) -> tuple[dict[str, Any], dict[str, Any]] | None:
    """İsimli üçüncü-kişi verisinde safety önceliğini sözleşmeye yansıt."""

    if (
        role in {"ogretmen", "yonetici", "admin"}
        or intent not in _OTHER_PERSON_SAFETY_INTENTS
        or _POSSESSIVE_NAME_RE.search(question) is None
    ):
        return None
    reason = "safety_other_person_data"
    expected = {
        "intent": None, "outcome": "deny", "meta_outcome": "deny",
        "meta_action_id": None, "response_ids": [reason], "auth_action": None,
        "fallback": False, "navigation_route": None, "meta_route_key": None,
        "reason_code": reason,
    }
    policy = {
        "outcome": "deny", "action_id": None, "scope": "other_person_data",
        "reason_code": reason, "route_key": None,
    }
    return expected, policy


def _make_record(seed: Seed, *, role: str, family: str, round_index: int, scope: str) -> dict[str, Any]:
    intent = None if seed.expected_intent == OOS_LABEL else seed.expected_intent
    supports_ui, ui_label = _ui_context(intent, seed.question) if intent else (False, None)
    allow_state = scope == "in_scope" and _supports_state_error(intent)
    if family == "ui_label_tr_en" and not supports_ui:
        raise ValueError(f"{intent}: UI ailesi için ekran/etiket bağlamı yok.")
    variant = _variant_for(seed, round_index, family, role)
    ctx = MutationContext(
        seed=seed, role=role, intent=intent, family=family, round_index=round_index,
        variant=variant, ui_label=ui_label, allow_state_error=allow_state, scope=scope,
    )
    transformer = _OOS_TRANSFORMERS[family] if scope == "oos" else _TRANSFORMERS[family]
    question, transformations, mutation = transformer(ctx)
    if scope == "oos":
        # Noktalama/typo gibi çerçeve kullanmayan ailelerde de anlam sınıfı açık
        # kalsın; bu metadata rapor/audit sırasında boundary korunmasını kanıtlar.
        mutation = {
            **mutation,
            "scope_framing": "neutral_oos",
            "boundary_semantics": _oos_semantics(ctx),
        }
    question = " ".join(question.split())
    findings = privacy_findings(question)
    if findings:
        raise ValueError(f"{seed.source_dataset}:{seed.source_index} mutasyonu PII/secret üretti: {', '.join(findings)}")
    expected, policy = (
        _expected_in_scope_contract(seed, role) if scope == "in_scope"
        else _expected_oos_contract(seed)
    )
    if scope == "in_scope":
        safety_contract = _expected_other_person_safety_contract(
            seed.expected_intent, role, question,
        )
        if safety_contract is not None:
            expected, policy = safety_contract
    return {
        "question": question, "expected_intent": seed.expected_intent,
        "expected": expected, "role": role, "scope": scope,
        "scope_boundary_type": seed.scope_boundary_type, "family": family,
        "transformations": transformations,
        "mutation": {**mutation, "variant_hash": f"{variant:016x}"},
        "policy": policy,
        "source": {
            "dataset": seed.source_dataset, "index": seed.source_index,
            "question": seed.question, "role": seed.role,
        },
        "synthetic": True, "is_gold": False, "generator_version": GENERATOR_VERSION,
        "generation_round": round_index,
        "privacy_scan": {"passed": True, "findings": []},
    }


def _iter_intent_candidates(intent: str, seeds: Sequence[Seed]) -> Iterator[dict[str, Any]]:
    role_groups = _policy_roles(intent)
    outcomes = tuple(role_groups)
    for slot in range(200_000):
        outcome = outcomes[slot % len(outcomes)]
        seed_cycle = slot // len(outcomes)
        seed = seeds[seed_cycle % len(seeds)]
        families = _eligible_families(intent, seed.question)
        family = families[(seed_cycle // len(seeds)) % len(families)]
        round_index = seed_cycle // max(1, len(seeds) * len(families))
        roles = role_groups[outcome]
        role = roles[_stable_int(MUTATION_SEED_VERSION, intent, seed.question, round_index, family, outcome) % len(roles)]
        yield _make_record(seed, role=role, family=family, round_index=round_index, scope="in_scope")


def _intent_quotas(intents: Sequence[str], target: int) -> dict[str, int]:
    if target < 0:
        raise ValueError("Hedef kayıt sayısı negatif olamaz.")
    if not intents and target:
        raise ValueError("Intent kotası için intent bulunamadı.")
    base, remainder = divmod(target, len(intents)) if intents else (0, 0)
    return {intent: base + (1 if index < remainder else 0) for index, intent in enumerate(intents)}


def _accept_unique(record: dict[str, Any], records: list[dict[str, Any]], seen_questions: set[str]) -> bool:
    key = normalise_question_key(record["question"])
    if key in seen_questions:
        return False
    seen_questions.add(key)
    records.append(record)
    return True


def _generate_in_scope(seeds: Sequence[Seed], target: int, seen_questions: set[str]) -> list[dict[str, Any]]:
    grouped: dict[str, list[Seed]] = defaultdict(list)
    for seed in seeds:
        grouped[seed.expected_intent].append(seed)
    catalog_order = [item["intent"] for item in INTENTS if item["intent"] in grouped]
    intents = catalog_order + sorted(set(grouped).difference(catalog_order))
    quotas = _intent_quotas(intents, target)
    records: list[dict[str, Any]] = []
    for intent in intents:
        wanted, accepted = quotas[intent], 0
        for candidate in _iter_intent_candidates(intent, grouped[intent]):
            if _accept_unique(candidate, records, seen_questions):
                accepted += 1
                if accepted == wanted:
                    break
        if accepted != wanted:
            raise ValueError(f"{intent} için {wanted} normalize-benzersiz vaka üretilemedi; {accepted} kayıtta kaldı.")
    return records


def _iter_oos_candidates(seeds: Sequence[Seed]) -> Iterator[dict[str, Any]]:
    for slot in range(500_000):
        seed = seeds[slot % len(seeds)]
        cycle = slot // len(seeds)
        family = OOS_MUTATION_FAMILIES[cycle % len(OOS_MUTATION_FAMILIES)]
        round_index = cycle // len(OOS_MUTATION_FAMILIES)
        role = ROLE_HIERARCHY[_stable_int(MUTATION_SEED_VERSION, "oos", seed.question, round_index, family) % len(ROLE_HIERARCHY)]
        yield _make_record(seed, role=role, family=family, round_index=round_index, scope="oos")


def _generate_oos(seeds: Sequence[Seed], target: int, seen_questions: set[str]) -> list[dict[str, Any]]:
    if target < 0:
        raise ValueError("Hedef kayıt sayısı negatif olamaz.")
    records: list[dict[str, Any]] = []
    for candidate in _iter_oos_candidates(seeds):
        _accept_unique(candidate, records, seen_questions)
        if len(records) == target:
            return records
    raise ValueError(f"OOS için {target} normalize-benzersiz vaka üretilemedi; {len(records)} kayıtta kaldı.")


def _stable_record_id(record: Mapping[str, Any]) -> str:
    identity = {
        "generator_version": GENERATOR_VERSION,
        "question_key": normalise_question_key(str(record["question"])),
        "role": record["role"], "expected": record["expected"],
        "source": record["source"], "family": record["family"],
    }
    raw = json.dumps(identity, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "stress-" + hashlib.sha256(raw).hexdigest()[:20]


def generate_stress_records(
    *, benchmark_path: str | Path = DEFAULT_BENCHMARK_PATH,
    near_oos_path: str | Path = DEFAULT_NEAR_OOS_PATH,
    in_scope_count: int = DEFAULT_IN_SCOPE_COUNT,
    oos_count: int = DEFAULT_OOS_COUNT,
) -> list[dict[str, Any]]:
    in_scope_seeds, oos_seeds = load_source_seeds(benchmark_path, near_oos_path)
    seen_questions: set[str] = set()
    records = _generate_in_scope(in_scope_seeds, in_scope_count, seen_questions)
    records.extend(_generate_oos(oos_seeds, oos_count, seen_questions))
    output: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for record in records:
        record_id = _stable_record_id(record)
        if record_id in seen_ids:
            raise ValueError(f"Kararlı vaka kimliği çakıştı: {record_id}")
        seen_ids.add(record_id)
        output.append({"id": record_id, **record})
    return output


def write_jsonl(records: Iterable[dict[str, Any]], output: str | Path) -> Path:
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")) for record in records]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return path


def load_stress_records(path: str | Path = DEFAULT_DATA_OUTPUT) -> list[dict[str, Any]]:
    return _read_jsonl(Path(path))


def _actual_outcome(response: Mapping[str, Any]) -> str:
    response_id = response.get("response_id")
    meta = response.get("assistant_meta")
    if response_id == "out_of_scope_action":
        return "deny"
    if response_id == "clarification_prompt":
        return "clarify"
    if bool(response.get("fallback")):
        return "fallback"
    if response.get("auth_action") is not None:
        return "deny"
    if isinstance(response_id, str) and response_id.startswith("safety_"):
        return "deny"
    if isinstance(meta, Mapping) and isinstance(meta.get("outcome"), str):
        return str(meta["outcome"])
    return "allow"


def _nested_route(response: Mapping[str, Any], *, meta: bool) -> str | None:
    if meta:
        assistant_meta = response.get("assistant_meta")
        if not isinstance(assistant_meta, Mapping):
            return None
        navigation, key = assistant_meta.get("navigation"), "route_key"
    else:
        navigation, key = response.get("navigation"), "route"
    if not isinstance(navigation, Mapping):
        return None
    value = navigation.get(key)
    return value if isinstance(value, str) else None


def _contract_checks(expected: Mapping[str, Any], response: Mapping[str, Any]) -> tuple[dict[str, dict[str, Any]], list[str]]:
    meta = response.get("assistant_meta")
    meta_mapping = meta if isinstance(meta, Mapping) else {}
    actual = {
        "intent": response.get("intent"), "outcome": _actual_outcome(response),
        "meta_outcome": meta_mapping.get("outcome"), "response_id": response.get("response_id"),
        "meta_action_id": meta_mapping.get("action_id"),
        "auth_action": response.get("auth_action"), "fallback": bool(response.get("fallback")),
        "navigation_route": _nested_route(response, meta=False),
        "meta_route_key": _nested_route(response, meta=True),
        "reason_code": meta_mapping.get("reason_code"),
    }
    response_ids = list(expected.get("response_ids") or [])
    predicates = {
        "intent": actual["intent"] == expected.get("intent"),
        "outcome": actual["outcome"] == expected.get("outcome"),
        "meta_outcome": actual["meta_outcome"] == expected.get("meta_outcome"),
        "meta_action_id": actual["meta_action_id"] == expected.get("meta_action_id"),
        "response_id": actual["response_id"] in response_ids,
        "auth_action": actual["auth_action"] == expected.get("auth_action"),
        "fallback": actual["fallback"] is bool(expected.get("fallback")),
        "navigation_route": actual["navigation_route"] == expected.get("navigation_route"),
        "meta_route_key": actual["meta_route_key"] == expected.get("meta_route_key"),
        "reason_code": expected.get("reason_code") is None or actual["reason_code"] == expected.get("reason_code"),
    }
    checks = {
        key: {
            "passed": passed,
            "expected": response_ids if key == "response_id" else expected.get(key),
            "actual": actual["response_id"] if key == "response_id" else actual.get(key),
        }
        for key, passed in predicates.items()
    }
    reasons = [f"{key}_mismatch" for key, passed in predicates.items() if not passed]
    text = response.get("text")
    if not isinstance(text, str) or not text.strip():
        checks["visible_text"] = {"passed": False, "expected": "non_empty", "actual": text}
        reasons.append("empty_visible_text")
    else:
        checks["visible_text"] = {"passed": True, "expected": "non_empty", "actual": "present"}
        findings = privacy_findings(text)
        checks["response_privacy"] = {"passed": not findings, "expected": [], "actual": findings}
        if findings:
            reasons.append("response_privacy_finding")
    return checks, reasons


def _is_semantic_safe_oos_clarification(
    record: Mapping[str, Any], response: Mapping[str, Any], reasons: Sequence[str],
) -> bool:
    """Katı fallback yerine eylemsiz clarification dönen OOS FAIL'ini tanır.

    Bu durum sözleşme bakımından hâlâ FAIL'dir. Yalnız intent/action/route
    üretmeyen güvenli bir netleştirme olduğu için tanısal raporda ``soft`` diye
    ayrılır; boundary reddi beklenen action/data talepleri bu sınıfa girmez.
    """

    expected = record.get("expected")
    meta = response.get("assistant_meta")
    if not reasons or not isinstance(expected, Mapping) or not isinstance(meta, Mapping):
        return False
    if record.get("scope") != "oos" or record.get("scope_boundary_type"):
        return False
    if expected.get("outcome") != "fallback" or expected.get("intent") is not None:
        return False
    if {"engine_exception", "empty_visible_text", "response_privacy_finding"}.intersection(reasons):
        return False
    return (
        response.get("intent") is None
        and response.get("response_id") == "clarification_prompt"
        and _actual_outcome(response) == "clarify"
        and meta.get("outcome") == "clarify"
        and meta.get("action_id") is None
        and response.get("auth_action") is None
        and _nested_route(response, meta=False) is None
        and _nested_route(response, meta=True) is None
    )


def collect_results(records: Iterable[dict[str, Any]], *, engine: Engine | None = None) -> list[dict[str, Any]]:
    runner = engine or Engine()
    results: list[dict[str, Any]] = []
    for index, record in enumerate(records, start=1):
        role = record.get("role", "ziyaretci")
        payload = {
            "query": record["question"], "trace_id": f"stress-{index:05d}",
            "session": {"role": role, "authenticated": role != "ziyaretci"},
        }
        engine_exception: dict[str, str] | None = None
        try:
            response = runner.handle(payload)
            if not isinstance(response, dict):
                raise TypeError("Engine.handle bir sözlük döndürmeli.")
        except Exception as exc:
            engine_exception = {"type": type(exc).__name__, "message": str(exc)}
            response = {"exception": engine_exception}
        expected = record.get("expected")
        if not isinstance(expected, Mapping):
            raise ValueError(f"{record.get('id', index)}: expected sözleşmesi eksik.")
        checks, reasons = _contract_checks(expected, response)
        if engine_exception is not None:
            reasons.insert(0, "engine_exception")
        actual_intent = response.get("intent") if engine_exception is None else None
        failure_severity = None
        if reasons:
            failure_severity = (
                "soft" if _is_semantic_safe_oos_clarification(record, response, reasons)
                else "hard"
            )
        results.append({
            "index": index, **record, "actual_intent": actual_intent or OOS_LABEL,
            "actual_outcome": _actual_outcome(response), "contract_checks": checks,
            "failure_reasons": reasons, "failure_severity": failure_severity,
            "passed": not reasons, "response": response,
        })
    return results


def _table_text(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def _quote(text: object) -> str:
    lines = str(text).splitlines() or [""]
    return "\n".join("> " + line if line else ">" for line in lines)


def _value_at(row: Mapping[str, Any], path: str) -> str:
    value: Any = row
    for key in path.split("."):
        if not isinstance(value, Mapping):
            return "-"
        value = value.get(key)
    return "-" if value is None else str(value)


def _ordered_values(key: str, values: Iterable[str]) -> list[str]:
    unique = set(values)
    if key == "family":
        fixed = [value for value in MUTATION_FAMILIES if value in unique]
        return fixed + sorted(unique.difference(fixed))
    if key == "role":
        fixed = [value for value in ROLE_HIERARCHY if value in unique]
        return fixed + sorted(unique.difference(fixed))
    return sorted(unique)


def _breakdown_table(rows: Sequence[dict[str, Any]], key: str, heading: str) -> list[str]:
    counts: dict[str, Counter[str]] = {}
    for row in rows:
        value = _value_at(row, key)
        bucket = counts.setdefault(value, Counter())
        bucket["total"] += 1
        bucket["passed" if row["passed"] else "failed"] += 1
    output = [f"## {heading}", "", "| Değer | Toplam | PASS | FAIL | Başarı |", "|---|---:|---:|---:|---:|"]
    for value in _ordered_values(key, counts):
        count = counts[value]
        rate = count["passed"] / count["total"] if count["total"] else 0.0
        label = ROLE_LABELS.get(value, value) if key == "role" else value
        output.append(f"| {_table_text(label)} | {count['total']} | {count['passed']} | {count['failed']} | {rate:.1%} |")
    return output


def _failure_cluster_table(rows: Sequence[dict[str, Any]]) -> list[str]:
    clusters: Counter[str] = Counter(reason for row in rows for reason in row.get("failure_reasons", []))
    output = ["## Hata kümeleri", ""]
    if not clusters:
        return output + ["Sözleşme ihlali oluşmadı."]
    output.extend(["| Failure reason | Vaka |", "|---|---:|"])
    output.extend(f"| `{reason}` | {count} |" for reason, count in clusters.most_common())
    return output


def _oos_case_type(row: Mapping[str, Any]) -> str:
    boundary = row.get("scope_boundary_type")
    if not boundary:
        expected = row.get("expected")
        reason = expected.get("reason_code") if isinstance(expected, Mapping) else None
        if isinstance(reason, str) and reason.startswith("scope_boundary_"):
            boundary = reason.removeprefix("scope_boundary_")
    if not boundary:
        return "fallback"
    normalized = str(boundary).strip().casefold()
    return f"{normalized}-boundary"


def _oos_quality_table(rows: Sequence[dict[str, Any]]) -> list[str]:
    oos_rows = [row for row in rows if row.get("scope") == "oos"]
    counts: dict[str, Counter[str]] = {}
    for row in oos_rows:
        bucket = counts.setdefault(_oos_case_type(row), Counter())
        bucket["total"] += 1
        if row.get("passed"):
            bucket["passed"] += 1
        elif row.get("failure_severity") == "soft":
            bucket["soft"] += 1
        else:
            bucket["hard"] += 1
    # Temel üç sınıf hiç vaka üretmemiş olsa bile görünür; sıfır data-boundary
    # satırı örneğin veri sınırı kapsamasının eksik olduğunu saklamaz.
    ordered = ["fallback", "action-boundary", "data-boundary"]
    ordered.extend(sorted(set(counts).difference(ordered)))
    output = [
        "## OOS türü ve FAIL şiddeti", "",
        "`soft`, yalnız katı fallback sözleşmesi yerine intent/action/route üretmeden "
        "netleştirme isteyen semantik olarak güvenli yanıttır; sözleşme sonucu yine FAIL kalır. "
        "Diğer bütün sözleşme ihlalleri `hard` sayılır.", "",
        "| OOS türü | Toplam | PASS | Soft FAIL | Hard FAIL | Sözleşme başarısı |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for kind in ordered:
        count = counts.get(kind, Counter())
        rate = count["passed"] / count["total"] if count["total"] else 0.0
        output.append(
            f"| `{kind}` | {count['total']} | {count['passed']} | {count['soft']} | "
            f"{count['hard']} | {rate:.1%} |"
        )
    return output


def _failure_examples(rows: Sequence[dict[str, Any]], *, scope: str, limit: int = 50) -> list[str]:
    failures = [row for row in rows if row.get("scope") == scope and not row.get("passed")]
    heading = "İlk uygulama-içi FAIL örnekleri" if scope == "in_scope" else "İlk OOS FAIL örnekleri"
    output = [f"## {heading}", ""]
    if not failures:
        return output + ["FAIL oluşmadı."]
    if scope == "oos":
        output.extend([
            "| ID | Tür | Şiddet | Rol | Soru | Nedenler |",
            "|---|---|---|---|---|---|",
        ])
        for row in failures[:limit]:
            output.append(
                f"| `{row.get('id', '-')}` | `{_oos_case_type(row)}` | "
                f"`{row.get('failure_severity') or 'hard'}` | "
                f"{_table_text(ROLE_LABELS.get(row['role'], row['role']))} | "
                f"{_table_text(row['question'])} | "
                f"{_table_text(', '.join(row.get('failure_reasons', [])))} |"
            )
    else:
        output.extend(["| ID | Rol | Soru | Nedenler |", "|---|---|---|---|"])
        for row in failures[:limit]:
            output.append(
                f"| `{row.get('id', '-')}` | {_table_text(ROLE_LABELS.get(row['role'], row['role']))} | "
                f"{_table_text(row['question'])} | {_table_text(', '.join(row.get('failure_reasons', [])))} |"
            )
    return output


def render_markdown(
    results: Iterable[dict[str, Any]], *, part_links: Sequence[str] = (),
    results_link: str = "data/stress_benchmark_results.jsonl",
) -> str:
    rows = list(results)
    passed = sum(bool(row["passed"]) for row in rows)
    failed = len(rows) - passed
    soft_failed = sum(
        not row.get("passed") and row.get("failure_severity") == "soft"
        for row in rows
    )
    hard_failed = failed - soft_failed
    rate = passed / len(rows) if rows else 0.0
    output = [
        "# Çelebi Sentetik Stres Benchmarkı Sonuçları", "", "> [!IMPORTANT]",
        "> Bu küme bağımsız bir **gold benchmark değildir**. Yalnız insan etiketli "
        "sorulardan türetilen tanısal/metamorfik stres testidir; katalog örnekleri "
        "değerlendirme seed'i değildir.", "", f"- Generator: `{GENERATOR_VERSION}`",
        f"- Toplam vaka: **{len(rows)}**",
        f"- Uygulama-içi: **{sum(row.get('scope') == 'in_scope' for row in rows)}**",
        f"- OOS: **{sum(row.get('scope') == 'oos' for row in rows)}**",
        f"- PASS: **{passed}**", f"- FAIL: **{failed}**",
        f"- Soft FAIL: **{soft_failed}**", f"- Hard FAIL: **{hard_failed}**",
        f"- Tam sözleşme başarı oranı: **{rate:.1%}**", "",
        "Tam Engine payload'ı `python stress_benchmark.py` çalıştırıldığında yerelde "
        f"`{results_link}` olarak üretilir (büyük ve yeniden üretilebilir olduğu için "
        "Git'e alınmaz). Markdown parçaları inceleme metadata'sı ile kullanıcıya "
        "görünen soru/cevabı gösterir; iç içe makine payload'ını göstermez.", "",
    ]
    for key, heading in (
        ("source.dataset", "Kaynak bazında"),
        ("expected.outcome", "Beklenen outcome bazında"),
        ("actual_outcome", "Gerçek outcome bazında"),
        ("family", "Varyasyon ailesi bazında"),
        ("expected_intent", "Beklenen intent bazında"),
        ("role", "Rol bazında"),
    ):
        output.extend(_breakdown_table(rows, key, heading))
        output.append("")
    output.extend(_oos_quality_table(rows))
    output.append("")
    output.extend(_failure_cluster_table(rows))
    output.extend(["", "## Okunabilir rapor parçaları", ""])
    output.extend(f"- [{Path(link).name}]({link})" for link in part_links) if part_links else output.append("Parça bağlantısı verilmedi.")
    output.append("")
    output.extend(_failure_examples(rows, scope="in_scope"))
    output.append("")
    output.extend(_failure_examples(rows, scope="oos"))
    return "\n".join(output).rstrip() + "\n"


def render_markdown_part(rows: Sequence[dict[str, Any]], *, part_number: int, total_parts: int) -> str:
    output = [
        f"# Çelebi Stres Vakaları · Parça {part_number}/{total_parts}", "",
        "Bu dosyada her vaka için kısa inceleme metadata'sı ile kullanıcıya görünen soru ve cevap "
        "vardır. Tam Engine yanıtı ve iç içe makine alanları results JSONL artefaktındadır.", "",
    ]
    for row in rows:
        status = "PASS" if row["passed"] else "FAIL"
        response = row.get("response") or {}
        visible_text = response.get("text", "[Engine görünür metin döndürmedi]")
        output.extend([
            f"## {row['index']:05d} · {status} · {ROLE_LABELS.get(row['role'], row['role'])}", "",
            f"- ID: `{row.get('id', '-')}`", f"- Aile: `{row.get('family', '-')}`",
            f"- Kaynak: `{_value_at(row, 'source.dataset')}:{_value_at(row, 'source.index')}`",
            f"- Beklenen: `{_value_at(row, 'expected.intent')}` / `{_value_at(row, 'expected.outcome')}`",
            f"- Gerçek: `{row.get('actual_intent', '-')}` / `{row.get('actual_outcome', '-')}`",
            f"- Failure reasons: `{', '.join(row.get('failure_reasons', [])) or '-'}`", "",
            "### Soru", "", _quote(row["question"]), "",
            "### Kullanıcıya görünen cevap", "", _quote(visible_text), "",
        ])
    return "\n".join(output).rstrip() + "\n"


def write_report(
    results: Iterable[dict[str, Any]], output: str | Path, *, chunk_size: int = DEFAULT_REPORT_CHUNK_SIZE,
    results_path: str | Path = DEFAULT_RESULTS_OUTPUT,
) -> Path:
    if not MIN_REPORT_CHUNK_SIZE <= chunk_size <= MAX_REPORT_CHUNK_SIZE:
        raise ValueError(f"Markdown parça boyutu {MIN_REPORT_CHUNK_SIZE}-{MAX_REPORT_CHUNK_SIZE} olmalı.")
    rows = list(results)
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    part_dir = path.with_name(path.stem + "_parcalar")
    part_dir.mkdir(parents=True, exist_ok=True)
    # Önceki koşuda daha fazla parça üretildiyse eski generated part dosyaları
    # raporda görünmeden klasörde kalmasın. Kapsam yalnız bu raporun türetilmiş
    # hedef klasöründeki tam ``part-*.md`` desenidir; diğer dosyalara dokunulmaz.
    for stale_part in part_dir.glob("part-*.md"):
        if stale_part.is_file():
            stale_part.unlink()
    total_parts = max(1, (len(rows) + chunk_size - 1) // chunk_size)
    part_paths: list[Path] = []
    for part_index in range(total_parts):
        chunk = rows[part_index * chunk_size:(part_index + 1) * chunk_size]
        part_path = part_dir / f"part-{part_index + 1:04d}.md"
        part_path.write_text(
            render_markdown_part(chunk, part_number=part_index + 1, total_parts=total_parts),
            encoding="utf-8", newline="\n",
        )
        part_paths.append(part_path)
    links = [part.relative_to(path.parent).as_posix() for part in part_paths]
    result_target = Path(results_path)
    try:
        result_link = result_target.resolve().relative_to(path.parent.resolve()).as_posix()
    except ValueError:
        result_link = result_target.resolve().as_posix()
    path.write_text(
        render_markdown(rows, part_links=links, results_link=result_link),
        encoding="utf-8", newline="\n",
    )
    return path


def build_artifacts(
    *, benchmark_path: str | Path = DEFAULT_BENCHMARK_PATH,
    near_oos_path: str | Path = DEFAULT_NEAR_OOS_PATH,
    data_output: str | Path = DEFAULT_DATA_OUTPUT,
    results_output: str | Path = DEFAULT_RESULTS_OUTPUT,
    report_output: str | Path = DEFAULT_REPORT_OUTPUT,
    report_chunk_size: int = DEFAULT_REPORT_CHUNK_SIZE,
    engine: Engine | None = None,
) -> tuple[Path, Path, list[dict[str, Any]]]:
    records = generate_stress_records(benchmark_path=benchmark_path, near_oos_path=near_oos_path)
    data_path = write_jsonl(records, data_output)
    persisted_records = load_stress_records(data_path)
    results = collect_results(persisted_records, engine=engine)
    results_path = write_jsonl(results, results_output)
    report_path = write_report(
        results, report_output, chunk_size=report_chunk_size,
        results_path=results_path,
    )
    return data_path, report_path, results


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--benchmark", type=Path, default=DEFAULT_BENCHMARK_PATH)
    parser.add_argument("--near-oos", type=Path, default=DEFAULT_NEAR_OOS_PATH)
    parser.add_argument("--data-output", type=Path, default=DEFAULT_DATA_OUTPUT)
    parser.add_argument("--results-output", type=Path, default=DEFAULT_RESULTS_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT_OUTPUT)
    parser.add_argument("--report-chunk-size", type=int, default=DEFAULT_REPORT_CHUNK_SIZE,
                        help="Okunabilir Markdown parçası başına 250-500 vaka (varsayılan 400).")
    parser.add_argument("--strict", action="store_true", help="En az bir sözleşme FAIL'inde exit 1 kullan.")
    parser.add_argument("--allow-failures", action="store_true",
                        help="Geriye uyumlu no-op; tanısal varsayılan zaten FAIL'de exit 0 kullanır.")
    args = parser.parse_args(argv)
    data_path, report_path, results = build_artifacts(
        benchmark_path=args.benchmark, near_oos_path=args.near_oos,
        data_output=args.data_output, results_output=args.results_output,
        report_output=args.report_output, report_chunk_size=args.report_chunk_size,
    )
    failed = sum(not row["passed"] for row in results)
    print(
        f"{len(results)} sentetik vaka -> {data_path}, {args.results_output}, {report_path} "
        f"(PASS={len(results) - failed}, FAIL={failed})"
    )
    return 1 if args.strict and failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
