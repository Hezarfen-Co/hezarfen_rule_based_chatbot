"""Cevap üretimi: Decision -> kullanıcıya gösterilecek metin.

İlkeler (rehber §0):
- Gerçek etiket/yol içeren `response_template` kullanılır (katalogda hazır).
- Rol-farkında: seçilen intent oturum/rol gerektiriyor ve kullanıcı yetersizse,
  cevabın başına kibar bir uyarı eklenir (ama adımlar yine gösterilir; kullanıcı
  ne gerektiğini görsün).
- FALLBACK: anlaşılmayan/kapsam dışı sorularda netleştirme metni.
- `response_id` kararlıdır (testler metne değil id'ye bakar).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from .catalog import FALLBACK, get_intent
from .decision import (
    LOGIN_REQUIRED,
    ROLE_INSUFFICIENT,
    Decision,
    decide,
)


# Rollerin insan-okunur (arayüzdeki) adları.
ROLE_DISPLAY: Final[dict[str, str]] = {
    "ziyaretci": "Ziyaretçi",
    "ogrenci": "Öğrenci",
    "ogretmen": "Öğretmen",
    "yonetici": "Yönetici",
    "admin": "ADMIN",
}


@dataclass(frozen=True)
class Response:
    """Kullanıcıya dönecek nihai cevap."""

    response_id: str
    text: str
    intent: str | None
    fallback: bool
    auth_action: str | None = None


def role_display(role: str) -> str:
    """Rolün arayüzdeki adını döndürür (bilinmiyorsa olduğu gibi)."""

    return ROLE_DISPLAY.get(role, role)


def render(decision: Decision) -> Response:
    """Bir Decision'ı kullanıcı-yüzlü Response'a çevirir."""

    if decision.fallback or decision.intent is None:
        return Response(
            response_id=FALLBACK["response_id"],
            text=FALLBACK["response_template"],
            intent=None,
            fallback=True,
        )

    info = get_intent(decision.intent)
    if info is None:  # savunmacı: katalog dışı intent
        return Response(
            response_id=FALLBACK["response_id"],
            text=FALLBACK["response_template"],
            intent=None,
            fallback=True,
        )

    body = info["response_template"]

    if decision.auth_action == LOGIN_REQUIRED:
        text = (
            "Bunun için önce giriş yapmalısın (`/login`). Giriş yaptıktan sonra:\n"
            + body
        )
    elif decision.auth_action == ROLE_INSUFFICIENT:
        needed = role_display(decision.required_role or "")
        text = (
            f"Bu işlem için en az **{needed}** yetkisi gerekir; mevcut rolün bunu "
            f"yapmaya yetmiyor. Yine de adımlar şöyle:\n" + body
        )
    else:
        text = body

    return Response(
        response_id=info["response_id"],
        text=text,
        intent=decision.intent,
        fallback=False,
        auth_action=decision.auth_action,
    )


def answer(query: str, role: str = "ziyaretci", authenticated: bool = False) -> Response:
    """Uçtan uca kolaylık: karar ver + cevabı üret."""

    return render(decide(query, role=role, authenticated=authenticated))
