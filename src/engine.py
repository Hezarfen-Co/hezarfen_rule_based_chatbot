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

from typing import Any, Callable

from .catalog import ROLE_HIERARCHY
from .observability import process
from .similarity import SimilarityMatcher, get_default_matcher

# İsteğe bağlı log alıcısı: bir trace sözlüğü alır (dosyaya/akışa yazmak çağıranın işi).
LogSink = Callable[[dict[str, Any]], None]


class RequestError(ValueError):
    """Geçersiz istek payload'ı."""


def _parse_session(payload: dict[str, Any]) -> tuple[str, bool]:
    session = payload.get("session") or {}
    role = session.get("role", "ziyaretci")
    authenticated = bool(session.get("authenticated", role != "ziyaretci"))
    if role not in ROLE_HIERARCHY:
        raise RequestError(f"Bilinmeyen rol: {role!r}")
    if role == "ziyaretci" and authenticated:
        raise RequestError("Ziyaretçi 'authenticated' olamaz.")
    return role, authenticated


class Engine:
    """Süreç ömrü boyunca yeniden kullanılan backend motoru."""

    def __init__(
        self,
        matcher: SimilarityMatcher | None = None,
        log_sink: LogSink | None = None,
    ) -> None:
        self._matcher = matcher or get_default_matcher()
        self._log_sink = log_sink

    def handle(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Bir istek payload'ını işleyip yanıt sözleşmesi döndürür."""

        query = payload.get("query")
        if not isinstance(query, str) or not query.strip():
            raise RequestError("'query' boş olmayan bir metin olmalı.")

        role, authenticated = _parse_session(payload)
        trace_id = payload.get("trace_id")

        response, trace = process(
            query,
            role=role,
            authenticated=authenticated,
            trace_id=trace_id,
            matcher=self._matcher,
        )

        if self._log_sink is not None:
            self._log_sink(trace)

        return {
            "trace_id": trace["trace_id"],
            "response_id": response.response_id,
            "text": response.text,
            "intent": response.intent,
            "confidence": trace["decision"]["confidence"],
            "fallback": response.fallback,
            "auth_action": response.auth_action,
            "required_role": trace["decision"]["required_role"],
        }


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
