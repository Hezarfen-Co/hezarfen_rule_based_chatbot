"""Yetki motoru: parametre/erişim doğrulaması (IDOR/BOLA koruması) — madde 8 & 10.

İçerik filtresinden ve niyet motorundan AYRIDIR. Niyet doğru olsa bile, işlemin
parametreleri (student_id, course_id, school_id) oturumdaki DOĞRULANMIŞ yetkiye
göre denetlenir. Kullanıcının mesajında iddia ettiği rol değil, oturumdaki rol
esas alınır.

Bu, "Ali'nin notunu göster (kendisi izin verdi)" veya "başka okulun ID'si" gibi
yetkisiz veri erişimi (IDOR/BOLA) denemelerini engeller.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Final

from ..catalog import meets_role, role_rank


# Karar türleri (safety ile uyumlu adlandırma).
ALLOW: Final[str] = "ALLOW"
DENY: Final[str] = "DENY"
REQUIRE_AUTHORIZATION: Final[str] = "REQUIRE_AUTHORIZATION"
BLOCK_IDOR: Final[str] = "BLOCK"


@dataclass(frozen=True)
class Session:
    """Oturumdaki DOĞRULANMIŞ kimlik/yetki (backend'den gelir, mesajdan değil)."""

    role: str
    user_id: str | None = None
    school_id: str | None = None
    authorized_courses: frozenset[str] = field(default_factory=frozenset)
    authorized_students: frozenset[str] = field(default_factory=frozenset)


@dataclass(frozen=True)
class AccessRequest:
    """Bir işlemin çözülmüş parametreleri."""

    action: str
    student_id: str | None = None
    course_id: str | None = None
    school_id: str | None = None


@dataclass(frozen=True)
class AccessDecision:
    decision: str
    reason: str
    rule_id: str


def _d(decision: str, reason: str, rule_id: str) -> AccessDecision:
    return AccessDecision(decision=decision, reason=reason, rule_id=rule_id)


def validate_access(req: AccessRequest, session: Session) -> AccessDecision:
    """İşlem parametrelerini oturum yetkisine göre doğrular (IDOR/BOLA)."""

    # 1) Cross-school IDOR: farklı okul ID'si (admin hariç) -> engelle.
    if (
        req.school_id is not None
        and session.school_id is not None
        and req.school_id != session.school_id
        and not meets_role(session.role, "admin")
    ):
        return _d(BLOCK_IDOR, "Farklı okulun kaynağına erişim engellendi (IDOR).",
                  "AUTHZ-IDOR-001")

    # 2) Kendi verisi -> her zaman izin.
    if req.student_id is not None and req.student_id == session.user_id:
        return _d(ALLOW, "Kendi verisi.", "AUTHZ-SELF-001")

    accessing_other = req.student_id is not None and req.student_id != session.user_id

    # 3) Rol bazlı.
    if session.role == "ogrenci":
        if accessing_other or req.action.startswith("write") or "manage" in req.action:
            return _d(REQUIRE_AUTHORIZATION,
                      "Öğrenci yalnızca kendi bilgilerine erişebilir.", "AUTHZ-STU-001")
        return _d(ALLOW, "Öğrenci kendi kaynağı.", "AUTHZ-STU-002")

    if session.role == "ogretmen":
        # Öğretmen yalnızca yetkili olduğu ders/öğrenci üzerinde işlem yapar.
        if req.course_id is not None and req.course_id not in session.authorized_courses:
            return _d(REQUIRE_AUTHORIZATION,
                      "Bu ders için yönetim yetkin yok.", "AUTHZ-TEA-001")
        if accessing_other and (
            session.authorized_students and req.student_id not in session.authorized_students
        ):
            return _d(REQUIRE_AUTHORIZATION,
                      "Bu öğrenci senin yetkili olduğun kapsamda değil.", "AUTHZ-TEA-002")
        return _d(ALLOW, "Öğretmen yetkili kapsamda.", "AUTHZ-TEA-003")

    if meets_role(session.role, "yonetici"):
        # Yönetici/ADMIN: (okul kontrolü yukarıda yapıldı) izin.
        return _d(ALLOW, "Yönetici/ADMIN kapsamı.", "AUTHZ-MGR-001")

    return _d(REQUIRE_AUTHORIZATION, "Yetki doğrulanamadı.", "AUTHZ-DEFAULT-001")
