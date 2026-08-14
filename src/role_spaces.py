"""Compile independent, closed retrieval spaces for every Çelebi role.

The action vocabulary mirrors the backend-owned role-space V2 contract.  The
bridge still treats the policy embedded in each V2 request as authoritative and
echoes that request's version/hash; this local copy makes direct Engine/CLI use
safe and deterministic instead of falling back to a privilege ladder.
"""

from __future__ import annotations

import hashlib
import json
from functools import lru_cache
from typing import Final

from .access import (
    AccessOutcome,
    AccessScope,
    CompiledRoleSpace,
    ReasonCode,
    RoleIntentView,
)
from .catalog import INTENTS, ROLE_HIERARCHY
from .domain import build_domain_vocab
from .rules import RuleMatcher
from .similarity import SimilarityMatcher


ROLE_SPACE_VERSION: Final[str] = "2026-08-12.1"
AUTHENTICATED_ROLES: Final[tuple[str, ...]] = (
    "veli", "ogrenci", "ogretmen", "yonetici", "admin"
)


def _matrix(parent, student, teacher, manager, admin):
    return dict(zip(AUTHENTICATED_ROLES, (parent, student, teacher, manager, admin)))


A = AccessOutcome.ALLOW
D = AccessOutcome.DENY
G = AccessScope.GENERAL
O = AccessScope.OWN
E = AccessScope.ENROLLED_COURSE
M = AccessScope.MANAGED_COURSE
S = AccessScope.SCHOOL
V = AccessScope.EVENT_AUDIENCE

# (outcome, scope, navigation_key). İkili model: bir rol o işlemi backend'de
# yapabiliyorsa (kapsamı ne olursa olsun) ALLOW — asistan adımları anlatır, kapsam
# cevabın içinde nottur. Yapamıyorsa DENY — adım/rota/ayrıcalıklı rol adı sızmaz.
# Kaynak: hezarfen_backend endpoint guard'ları (rol×yetki taraması). CLARIFY-for-
# scope KALDIRILDI: bu asistan sistemi ANLATIR, kapsamı çalışma anında doğrulamaz.
_ACTION_RULES: Final[dict[str, dict[str, tuple[AccessOutcome, AccessScope | None, str | None]]]] = {
    "platform.help": _matrix((A, G, "guide"), (A, G, "guide"), (A, G, "guide"), (A, G, "guide"), (A, G, "guide")),
    "account.self": _matrix((A, O, "profile"), (A, O, "profile"), (A, O, "profile"), (A, O, "profile"), (A, O, "profile")),
    "messages.use": _matrix((A, O, "messages"), (A, O, "messages"), (A, O, "messages"), (A, O, "messages"), (A, O, "messages")),
    "notes.use": _matrix((A, O, "notes"), (A, O, "notes"), (A, O, "notes"), (A, O, "notes"), (A, O, "notes")),
    # Ders görüntüleme: Veli erişemez (kayıt/yönetim yok); öğrenci kayıtlı derslerini,
    # öğretmen yönettiklerini görür — ikisi de ALLOW (kapsam nottur).
    "courses.view": _matrix((D, None, None), (A, E, "courses"), (A, M, "courses"), (A, S, "courses"), (A, S, "courses")),
    "courses.create": _matrix((D, None, None), (D, None, None), (A, O, "courses"), (A, S, "courses"), (A, S, "courses")),
    "courses.manage": _matrix((D, None, None), (D, None, None), (A, M, "courses"), (A, S, "courses"), (A, S, "courses")),
    "courses.enroll_student": _matrix((D, None, None), (D, None, None), (A, M, "courses"), (A, S, "courses"), (A, S, "courses")),
    # Sınava girme yalnız Öğrenci (backend: tam olarak Student + enrolled). Personel giremez.
    "exams.take": _matrix((D, None, None), (A, E, "exams"), (D, None, None), (D, None, None), (D, None, None)),
    "exams.manage": _matrix((D, None, None), (D, None, None), (A, M, "exams"), (A, S, "exams"), (A, S, "exams")),
    # Ödev: görüntüleme öğrenci+ (Veli /students'tan çocuğunu izler, /homework'ü
    # kullanmaz -> D); teslim yalnız Öğrenci (backend: exactly Student + enrolled);
    # oluşturma/notlandırma Öğretmen+ (yönettiği ders).
    "homework.view": _matrix((D, None, None), (A, E, "homework"), (A, M, "homework"), (A, S, "homework"), (A, S, "homework")),
    "homework.submit": _matrix((D, None, None), (A, E, "homework"), (D, None, None), (D, None, None), (D, None, None)),
    "homework.manage": _matrix((D, None, None), (D, None, None), (A, M, "homework"), (A, S, "homework"), (A, S, "homework")),
    # Randevu: alma yalnız Öğrenci+Veli (backend: exactly Student|Parent; personel
    # alamaz); saat açma/talep onaylama Öğretmen+.
    "appointments.book": _matrix((A, O, "appointments"), (A, O, "appointments"), (D, None, None), (D, None, None), (D, None, None)),
    "appointments.manage": _matrix((D, None, None), (D, None, None), (A, O, "appointments"), (A, S, "appointments"), (A, S, "appointments")),
    # Yemek: menü görüntüleme herkese açık; yer ayırma yalnız Öğrenci(self)+Veli
    # (çocuğu); menü/öğün/kredi yönetimi Yönetici+ (öğretmen para/menü yönetmez).
    "meals.view": _matrix((A, O, "meals"), (A, O, "meals"), (A, O, "meals"), (A, S, "meals"), (A, S, "meals")),
    "meals.book": _matrix((A, O, "meals"), (A, O, "meals"), (D, None, None), (D, None, None), (D, None, None)),
    "meals.manage": _matrix((D, None, None), (D, None, None), (D, None, None), (A, S, "meals"), (A, S, "meals")),
    # Soru havuzu: sorma/çözme Öğrenci+ (backend RequireStudent — Veli hariç);
    # onaylama/reddetme Öğretmen+ (moderatör).
    "qpool.participate": _matrix((D, None, None), (A, O, "questions"), (A, O, "questions"), (A, S, "questions"), (A, S, "questions")),
    "qpool.moderate": _matrix((D, None, None), (D, None, None), (A, M, "questions"), (A, S, "questions"), (A, S, "questions")),
    # Beyaz tahta: görüntüleme/oluşturma Öğrenci+ (backend student+; Veli hariç).
    "boards.use": _matrix((D, None, None), (A, O, "whiteboards"), (A, O, "whiteboards"), (A, S, "whiteboards"), (A, S, "whiteboards")),
    "events.create": _matrix((D, None, None), (D, None, None), (A, O, "events"), (A, S, "events"), (A, S, "events")),
    # Kendi etkinlik yoklamasını herkes işaretler (öğrenci+); Veli salt-okunur gözlemci.
    "events.mark_attendance": _matrix((D, None, None), (A, O, "events"), (A, V, "events"), (A, V, "events"), (A, V, "events")),
    "reports.read_own": _matrix((A, O, "reports_self"), (A, O, "reports_self"), (A, O, "reports_self"), (A, O, "reports_self"), (A, O, "reports_self")),
    # Öğrenci not/yoklama arama = Öğretmen yönetim sayfası (Öğretmen+). Veli bu sayfayı
    # kullanmaz (çocuğunun verisini ayrı akıştan görür) -> DENY.
    "reports.observe_student": _matrix((D, None, None), (D, None, None), (A, M, "student_marks"), (A, S, "student_marks"), (A, S, "student_marks")),
    # Pomodoro backend'de her doğrulanmış kullanıcıya açık (CurrentUser) -> hepsi ALLOW.
    "pomodoro.start": _matrix((A, O, "pomodoro"), (A, O, "pomodoro"), (A, O, "pomodoro"), (A, O, "pomodoro"), (A, O, "pomodoro")),
    "pomodoro.observe_student": _matrix((D, None, None), (D, None, None), (A, S, "student_pomodoro"), (A, S, "student_pomodoro"), (A, S, "student_pomodoro")),
    "work.self": _matrix((D, None, None), (D, None, None), (A, O, "work"), (A, O, "work"), (A, O, "work")),
    "work.manage": _matrix((D, None, None), (D, None, None), (D, None, None), (A, S, "staff_work"), (A, S, "staff_work")),
    "school.settings_manage": _matrix((D, None, None), (D, None, None), (D, None, None), (A, S, "school_settings"), (A, S, "school_settings")),
    "school.terms_manage": _matrix((D, None, None), (D, None, None), (D, None, None), (A, S, "school_terms"), (A, S, "school_terms")),
    "users.roles_manage": _matrix((D, None, None), (D, None, None), (D, None, None), (D, None, None), (A, S, "admin_users")),
}

_ACTION_BY_INTENT: Final[dict[str, str]] = {
    "greeting": "platform.help",
    "smalltalk": "platform.help",
    "thanks": "platform.help",
    "farewell": "platform.help",
    "bot_identity": "platform.help",
    "platform_info": "platform.help",
    "help_capabilities": "platform.help",
    "guide_info": "platform.help",
    "login_how": "platform.help",
    "register_how": "platform.help",
    "logout_how": "account.self",
    "session_info": "account.self",
    "account_access_problem": "platform.help",
    "profile_edit": "account.self",
    "language_theme": "account.self",
    "roles_permissions": "platform.help",
    "access_denied_help": "platform.help",
    "navigation_help": "platform.help",
    "course_view": "courses.view",
    "course_create": "courses.create",
    "course_enroll_student": "courses.enroll_student",
    "course_remove_student": "courses.manage",
    "lesson_session_add": "courses.manage",
    "roll_call": "courses.manage",
    "exam_modes_info": "platform.help",
    "exam_create": "exams.manage",
    "exam_add_question": "exams.manage",
    "exam_enter_room": "exams.take",
    "exam_save_answer": "exams.take",
    "exam_finish_result": "exams.take",
    "exam_rejoin_retake": "exams.take",
    "exam_grade_student": "exams.manage",
    "exam_live_monitor": "exams.manage",
    "homework_view": "homework.view",
    "homework_submit": "homework.submit",
    "homework_assign": "homework.manage",
    "homework_grade": "homework.manage",
    "report_card_view": "reports.read_own",
    "weighted_average_info": "platform.help",
    "student_marks_lookup": "reports.observe_student",
    "attendance_view": "reports.read_own",
    "attendance_rate_info": "platform.help",
    "event_attendance_mark": "events.mark_attendance",
    "student_attendance_lookup": "reports.observe_student",
    "event_create": "events.create",
    "note_create": "notes.use",
    "work_checkin_out": "work.self",
    "staff_work_manage": "work.manage",
    "term_manage": "school.terms_manage",
    "school_settings": "school.settings_manage",
    "user_role_change": "users.roles_manage",
    "privacy_security": "platform.help",
    "pomodoro_use": "pomodoro.start",
    "student_pomodoro_lookup": "pomodoro.observe_student",
    "messages_use": "messages.use",
    "study_club_info": "platform.help",
    "parent_info": "platform.help",
    "appointment_book": "appointments.book",
    "appointment_slot_open": "appointments.manage",
    "appointment_requests": "appointments.manage",
    "meal_view": "meals.view",
    "meal_book": "meals.book",
    "meal_menu_manage": "meals.manage",
    "question_ask": "qpool.participate",
    "question_solve": "qpool.participate",
    "question_approve": "qpool.moderate",
    "board_view": "boards.use",
    "board_create": "boards.use",
}

_OWN_REPORT_RESPONSES: Final[dict[str, str]] = {
    "veli": (
        "Veli hesabının kendi öğrenci karnesi veya yoklama kaydı yoktur. Bağlı bir "
        "çocuğun kaydını soruyorsan bunu açıkça belirt; erişim yalnız doğrulanmış "
        "veli–öğrenci bağlantısıyla mümkündür."
    ),
    "ogretmen": (
        "Öğretmen hesabının kendi öğrenci karnesi/yoklama raporu yerine, yalnız "
        "yönettiğin derslerdeki öğrencilerin raporlarını görüntüleme kapsamı vardır. "
        "Hangi öğrenciyi ve dersi kastettiğini belirtmelisin."
    ),
    "yonetici": (
        "Yönetici hesabında kişisel öğrenci karnesi yerine okul kapsamındaki öğrenci "
        "raporları yönetim ekranlarından görüntülenir. Hangi öğrenciyi kastettiğini belirt."
    ),
    "admin": (
        "ADMIN hesabında kişisel öğrenci karnesi yerine okul kapsamındaki öğrenci "
        "raporları görüntülenir. Hangi öğrenciyi kastettiğini belirt."
    ),
}

def action_id_for_intent(intent: str) -> str:
    return _ACTION_BY_INTENT[intent]


def _local_rule(item: dict, role: str):
    action_id = action_id_for_intent(item["intent"])
    if role == "ziyaretci":
        if item["auth_required"]:
            return action_id, D, None, None
        return action_id, A, G, None
    outcome, scope, route_key = _ACTION_RULES[action_id][role]
    return action_id, outcome, scope, route_key


def _deny_text(reason: ReasonCode) -> str:
    """Ret metni. Ayrıcalıklı adım, rota veya gerekli-rol adı ASLA sızmaz.

    Giriş gereken durumda (ziyaretçi) yalnız kamuya açık `/login` yolu verilir —
    bu bir sızıntı değil, herkesin erişebildiği giriş sayfasıdır.
    """

    if reason is ReasonCode.AUTHENTICATION_REQUIRED:
        return (
            "Bu konu için önce giriş yapman gerekiyor. `/login` sayfasından "
            "güvenli biçimde giriş yapabilirsin."
        )
    return (
        "Bu işlem senin rolünde yapılamıyor. Yetkisiz işlem adımları ve "
        "yönlendirme paylaşılmadı."
    )


def _view(item: dict, role: str) -> RoleIntentView:
    action_id, outcome, scope, route_key = _local_rule(item, role)
    if outcome is D:
        reason = (
            ReasonCode.AUTHENTICATION_REQUIRED
            if role == "ziyaretci" and item["auth_required"]
            else ReasonCode.ROLE_NOT_PERMITTED
        )
        body = _deny_text(reason)
        scope = None
        route_key = None
    else:  # ALLOW
        reason = ReasonCode.ALLOWED
        body = item["response_template"]
        # Karne/yoklama sayfası öğrenciye özeldir; üst roller için kişisel karne
        # yerine kapsam notu döndürülür (adım değil, bilgi).
        if item["intent"] in {"report_card_view", "attendance_view"} and role != "ogrenci":
            body = _OWN_REPORT_RESPONSES.get(role, body)

    return RoleIntentView(
        role=role,
        intent=item["intent"],
        action_id=action_id,
        outcome=outcome,
        scope=scope,
        reason_code=reason,
        response_id=item["response_id"],
        response_template=body,
        examples=tuple(item["example_questions"]),
        clarification=None,
        # Sözleşme metadata'sı (frontend butonu pasifleştirmek için kullanabilir);
        # kullanıcıya dönen METİN ayrıcalıklı rol adını/adımı ASLA içermez.
        required_role=item["min_role"] if outcome is D else None,
        route_key=route_key if outcome is A else None,
        route_label=None,
    )


def _hash_views(role: str, views: dict[str, RoleIntentView]) -> str:
    manifest = [
        {
            "view": view.view_id,
            "action": view.action_id,
            "outcome": view.outcome.value,
            "scope": view.scope.value if view.scope else None,
            "route": view.route_key,
        }
        for view in views.values()
    ]
    raw = json.dumps(
        {"version": ROLE_SPACE_VERSION, "role": role, "views": manifest},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


@lru_cache(maxsize=len(ROLE_HIERARCHY))
def get_role_space(role: str) -> CompiledRoleSpace:
    if role not in ROLE_HIERARCHY:
        raise KeyError(f"bilinmeyen rol uzayı: {role!r}")
    views = {item["intent"]: _view(item, role) for item in INTENTS}
    content_hash = _hash_views(role, views)
    space_id = f"{ROLE_SPACE_VERSION}:{role}:{content_hash[:12]}"
    examples = [
        (view.intent, question)
        for view in views.values()
        for question in view.examples
    ]
    return CompiledRoleSpace(
        role=role,
        version=ROLE_SPACE_VERSION,
        content_hash=content_hash,
        views=CompiledRoleSpace.immutable_views(views),
        rule_matcher=RuleMatcher(set(views), space_id=space_id),
        similarity_matcher=SimilarityMatcher(examples, space_id=space_id),
        domain_vocab=frozenset(build_domain_vocab(question for _, question in examples)),
    )


def validate_role_spaces() -> None:
    expected = {item["intent"] for item in INTENTS}
    if set(_ACTION_BY_INTENT) != expected:
        missing = expected - set(_ACTION_BY_INTENT)
        extra = set(_ACTION_BY_INTENT) - expected
        raise ValueError(f"intent/action eşlemesi eksik={missing}, fazla={extra}")
    ids: set[str] = set()
    for role in ROLE_HIERARCHY:
        space = get_role_space(role)
        if set(space.views) != expected:
            raise ValueError(f"{role}: eksik/fazla intent görünümü")
        if space.space_id in ids:
            raise ValueError(f"{role}: rol uzayı kimliği benzersiz değil")
        ids.add(space.space_id)
        if any(view.role != role for view in space.views.values()):
            raise ValueError(f"{role}: başka role ait görünüm sızdı")


validate_role_spaces()
