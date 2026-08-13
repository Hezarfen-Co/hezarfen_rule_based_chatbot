"""Aşama bazlı yapısal loglama: her sorgu için izlenmiş (traced) boru hattı.

`process()` boru hattını aşama aşama çalıştırır, her aşamanın çıktısını ve
gecikmesini (latency) yakalar ve hem kullanıcı-yüzlü Response hem de makine-okunur
bir trace kaydı döndürür. Bu kayıt:
  - metriklerin (Aşama 10) kaynağıdır,
  - tek bir yanlış cevabı adım adım geri izlemeyi sağlar,
  - auth sızıntısı gibi değişmezleri denetler (alarms).

Loglama backend'de üretilir; frontend yalnızca cevabı görür. trace_id istekle
gelebilir ya da burada üretilir.
"""

from __future__ import annotations

import json
import time
import uuid
from typing import Any

from .access import AccessOutcome
from .catalog import get_intent, meets_role
from .safety import mask_pii
from .decision import (
    LOGIN_REQUIRED,
    ROLE_INSUFFICIENT,
    Decision,
    decide_core,
)
from .domain import is_in_domain
from . import rules
from .normalize import normalize, roots
from .responder import Response, render
from .similarity import SimilarityMatcher, get_default_matcher
from .similarity import ScoredIntent
from .role_spaces import get_role_space


def new_trace_id() -> str:
    """Yeni bir izleme kimliği üretir."""

    return "req-" + uuid.uuid4().hex[:12]


def _elapsed_ms(start_ns: int) -> float:
    return round((time.perf_counter_ns() - start_ns) / 1_000_000, 3)


def check_auth_alarms(decision: Decision, authenticated: bool, role: str) -> list[str]:
    """Auth/rol değişmezlerini denetler; ihlal varsa alarm mesajları döndürür.

    Asla görülmemesi gereken durum: auth gerektiren/rol yetersiz bir intent'e,
    gating uygulanmadan (auth_action=None) izin verilmesi = veri sızıntısı riski.
    """

    alarms: list[str] = []
    if decision.fallback or decision.intent is None:
        return alarms

    if decision.view_id:
        effective_role = role if authenticated else "ziyaretci"
        view = get_role_space(effective_role).view_for(decision.intent)
        if view is None:
            return [f"ROLE_SPACE_LEAK: '{decision.intent}' bu rol uzayında yok."]
        expected = None
        if view.outcome is AccessOutcome.DENY:
            expected = LOGIN_REQUIRED if not authenticated else ROLE_INSUFFICIENT
        if decision.auth_action != expected:
            return [
                f"ROLE_SPACE_LEAK: '{decision.intent}' outcome={view.outcome.value} "
                f"ama auth_action={decision.auth_action!r}."
            ]
        return alarms

    info = get_intent(decision.intent)
    if info is None:
        return alarms

    auth_required = bool(info["auth_required"])
    min_role = info["min_role"]

    if auth_required and not authenticated and decision.auth_action != LOGIN_REQUIRED:
        alarms.append(
            f"AUTH_LEAK: '{decision.intent}' oturum gerektiriyor ama gating uygulanmadı."
        )
    if authenticated and not meets_role(role, min_role) and decision.auth_action != ROLE_INSUFFICIENT:
        alarms.append(
            f"ROLE_LEAK: '{decision.intent}' için rol yetersiz ama gating uygulanmadı."
        )
    return alarms


def process(
    query: str,
    role: str = "ziyaretci",
    authenticated: bool = False,
    *,
    trace_id: str | None = None,
    matcher: SimilarityMatcher | None = None,
) -> tuple[Response, dict[str, Any]]:
    """Boru hattını izleyerek çalıştırır; (Response, trace kaydı) döndürür."""

    effective_role = role if authenticated else "ziyaretci"
    space = get_role_space(effective_role)
    matcher = matcher or space.similarity_matcher
    trace_id = trace_id or new_trace_id()
    latency: dict[str, float] = {}

    total_start = time.perf_counter_ns()

    # 1) Normalizasyon (loglama/teşhis için; kök çıktısı).
    t = time.perf_counter_ns()
    normalized = normalize(query)
    query_roots = roots(query)
    latency["normalize"] = _elapsed_ms(t)

    # 2) Kural katmanı.
    t = time.perf_counter_ns()
    rule_match = space.rule_matcher.match(query)
    latency["rules"] = _elapsed_ms(t)

    # 3) Benzerlik + alan kapısı (yalnızca kural boş dönerse).
    t = time.perf_counter_ns()
    ranked = None if rule_match is not None else matcher.rank(query)
    if ranked is not None:
        ranked = [
            ScoredIntent(item.intent, item.score, space.space_id)
            for item in ranked
            if item.intent in space.views
        ]
    in_domain = (
        True
        if rule_match is not None
        else is_in_domain(query, set(space.domain_vocab))
    )
    latency["similarity"] = _elapsed_ms(t)

    # 4) Karar.
    t = time.perf_counter_ns()
    decision = decide_core(rule_match, ranked, role, authenticated, in_domain=in_domain)
    latency["decide"] = _elapsed_ms(t)

    # 5) Cevap (query, varyantlı intent'lerde deterministik metin seçimi için).
    t = time.perf_counter_ns()
    response = render(decision, query=query)
    latency["render"] = _elapsed_ms(t)

    latency["total"] = _elapsed_ms(total_start)

    alarms = check_auth_alarms(decision, authenticated, role)

    # KVKK: loglanan sorgu PII-maskelidir (ham sorgu asla kalıcı kayda girmez).
    query_masked, _ = mask_pii(query)
    trace: dict[str, Any] = {
        "trace_id": trace_id,
        "query_masked": query_masked,
        "role": role,
        "role_space_id": space.space_id,
        "role_space_version": space.version,
        "role_space_hash": space.content_hash,
        "authenticated": authenticated,
        "normalized": normalized,
        "roots": query_roots,
        "rule_layer": {
            "hit": rule_match is not None,
            "intent": rule_match.intent if rule_match else None,
            "matched": list(rule_match.matched) if rule_match else [],
        },
        "similarity": {
            "evaluated": ranked is not None,
            "in_domain": in_domain,
            "top_k": [
                {"intent": s.intent, "score": round(s.score, 4), "space_id": s.space_id}
                for s in decision.top_k
            ],
            "margin": decision.margin,
        },
        "decision": {
            "intent": decision.intent,
            "fallback": decision.fallback,
            "source": decision.source,
            "confidence": round(decision.confidence, 4),
            "tie_break": decision.tie_break,
            "role_redirect": decision.role_redirect,
            "auth_action": decision.auth_action,
            "required_role": decision.required_role,
            "view_id": decision.view_id,
            "outcome": decision.outcome,
            "scope": decision.scope,
            "reason_code": decision.reason_code,
        },
        "response_id": response.response_id,
        "latency_ms": latency,
        "alarms": alarms,
    }
    return response, trace


def trace_to_json(trace: dict[str, Any]) -> str:
    """Trace kaydını tek satır JSON'a çevirir (Türkçe karakterler korunur)."""

    return json.dumps(trace, ensure_ascii=False)
