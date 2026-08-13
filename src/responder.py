"""Cevap üretimi: Decision -> kullanıcıya gösterilecek metin.

İlkeler (rehber §0):
- Gerçek etiket/yol içeren `response_template` kullanılır (katalogda hazır).
- Rol-farkında: cevap gövdesi yalnızca güvenilir oturum rolünün derlenmiş
  görünümünden gelir. Retlerde işlem adımı ve rota asla gösterilmez.
- FALLBACK: anlaşılmayan/kapsam dışı sorularda netleştirme metni.
- `response_id` kararlıdır (testler metne değil id'ye bakar).
- Varyantlar (opsiyonel `response_variants`): sosyal intent'lerde robotik tekrarı
  kırmak için aynı response_id altında birden çok metin tutulur. Seçim RASTGELE
  DEĞİL, sorgunun CRC32'sine göre DETERMİNİSTİKTİR: aynı girdi her zaman aynı
  cevabı alır (testler tekrarlanabilir), farklı ifadeler farklı varyant görebilir.
"""

from __future__ import annotations

import zlib
from dataclasses import dataclass
from typing import Final

from .catalog import DEFAULT_GREETING_OPENER, FALLBACK, GREETING_OPENERS, get_intent
from .normalize import fold_accents, normalize
from .decision import (
    LOGIN_REQUIRED,
    ROLE_INSUFFICIENT,
    Decision,
    decide,
)
from .role_spaces import get_role_space


# Rollerin insan-okunur (arayüzdeki) adları.
ROLE_DISPLAY: Final[dict[str, str]] = {
    "ziyaretci": "Ziyaretçi",
    "veli": "Veli",
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


def _select_body(info: dict, query: str | None) -> str:
    """Cevap gövdesini seçer; varyant varsa sorguya göre deterministik dağıtır."""

    variants = info.get("response_variants")
    if not variants or query is None:
        body = info["response_template"]
    else:
        pool = [info["response_template"], *variants]
        index = zlib.crc32(query.strip().encode("utf-8")) % len(pool)
        body = pool[index]
    if "{selam}" in body:
        body = body.replace("{selam}", _greeting_opener(query))
    return body


def _greeting_opener(query: str | None) -> str:
    """Kullanıcının selamını aynalar: 'günaydın' -> 'Günaydın! ☀️'.

    Katlanmış sorguda en uzun eşleşen anahtar kazanır ('iyi günler' > 'hey').
    """

    if not query:
        return DEFAULT_GREETING_OPENER
    folded = fold_accents(normalize(query))
    for key in sorted(GREETING_OPENERS, key=len, reverse=True):
        if key in folded:
            return GREETING_OPENERS[key]
    return DEFAULT_GREETING_OPENER


def render(decision: Decision, query: str | None = None) -> Response:
    """Bir Decision'ı kullanıcı-yüzlü Response'a çevirir.

    `query` verilirse varyantlı intent'lerde metin, sorguya göre deterministik
    seçilir (bkz. modül docstring'i). Verilmezse her zaman ana şablon döner.
    """

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

    view = get_role_space(decision.role).view_for(decision.intent)
    if decision.view_id and view is not None:
        # The view body is already either role-local guidance or a fail-closed
        # denial.  Do not append the global catalog body to a denial.
        body = view.response_template
    else:
        body = _select_body(info, query)

    if decision.auth_action == LOGIN_REQUIRED and not decision.view_id:
        text = "Bu konu oturum bilgisi gerektiriyor. Önce güvenli biçimde giriş yapmalısın."
    elif decision.auth_action == ROLE_INSUFFICIENT and not decision.view_id:
        needed = role_display(decision.required_role or "")
        text = (
            f"Bu işlem için **{needed}** yetkisi gerekir. Yetkisiz işlem adımları "
            "ve yönlendirme paylaşılmadı."
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

    return render(decide(query, role=role, authenticated=authenticated), query=query)
