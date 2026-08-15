"""Karar katmanı: kural + benzerlik katmanlarını nihai bir karara bağlar.

Akış:
    1) Kural katmanı bir intent döndürürse onu kullan (yüksek kesinlik).
    2) Aksi hâlde benzerlik katmanının en iyi skoru:
       - eşiğin (threshold) altındaysa -> FALLBACK (kapsam dışı / emin değil).
       - eşiğin üstündeyse -> o intent; en yakın iki skor birbirine çok yakın ve
         çift `must_not_match`'te işaretliyse tie-break olarak KAYDEDİLİR.
    3) Rol gating: seçilen intent oturum/rol gerektiriyor ve kullanıcı yetersizse
       auth_action belirlenir (intent yine döner; ne gösterileceğine cevap katmanı karar verir).

Eşik/margin parametreleri Aşama 11'de benchmark üzerinde ayarlanacaktır; buradaki
varsayılanlar makul bir başlangıçtır.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Final

from . import rules
from .access import AccessOutcome
from .catalog import get_intent
from .domain import is_in_domain
from .role_spaces import get_role_space
from .similarity import ScoredIntent, SimilarityMatcher, get_default_matcher


# Varsayılan parametreler (Aşama 11'de benchmark taramasıyla seçildi).
# 0.18 + domain-gate: coverage %100, acc-on-covered ~%80, OOS recall ~%78,
# false-fallback 0. (Domain-gate olmadan OOS recall yalnızca ~%44'tü.)
DEFAULT_THRESHOLD: Final[float] = 0.18
DEFAULT_TIE_MARGIN: Final[float] = 0.05
DEFAULT_TOP_K: Final[int] = 3
# Rol-farkında yönlendirme marjı: seçilen (kapalı) intent ile erişilebilir,
# karışabilir bir aday arasındaki en yüksek skor farkı. Confusable-pair şartı
# zaten çok kısıtlayıcı olduğundan cömert tutulabilir.
DEFAULT_ROLE_REDIRECT_MARGIN: Final[float] = 0.15

# auth_action değerleri
LOGIN_REQUIRED: Final[str] = "login_required"
ROLE_INSUFFICIENT: Final[str] = "role_insufficient"


@dataclass(frozen=True)
class Decision:
    """Karar katmanının çıktısı (loglanabilir)."""

    intent: str | None
    fallback: bool
    source: str  # "rule" | "similarity" | "fallback"
    confidence: float
    top_k: tuple[ScoredIntent, ...] = ()
    margin: float | None = None
    tie_break: str | None = None
    # "src_intent->dst_intent" — top1 oturuma kapalıyken erişilebilir,
    # karışabilir bir adaya yönlendirildiyse (rol-farkında tie-break).
    role_redirect: str | None = None
    auth_action: str | None = None  # None | LOGIN_REQUIRED | ROLE_INSUFFICIENT
    required_role: str | None = None
    role: str = "ziyaretci"
    view_id: str | None = None
    outcome: str | None = None
    scope: str | None = None
    reason_code: str | None = None
    role_space_version: str | None = None
    role_space_hash: str | None = None


def _apply_role_gating(
    decision: Decision, role: str, authenticated: bool
) -> Decision:
    """Seçilen intent için oturum/rol yeterliliğini değerlendirir."""

    if decision.fallback or decision.intent is None:
        return decision

    effective_role = role if authenticated else "ziyaretci"
    space = get_role_space(effective_role)
    view = space.view_for(decision.intent)
    if view is None:
        return decision
    action: str | None = None
    if view.outcome is AccessOutcome.DENY:
        action = LOGIN_REQUIRED if not authenticated else ROLE_INSUFFICIENT
    return replace(
        decision,
        auth_action=action,
        required_role=view.required_role,
        role=effective_role,
        view_id=view.view_id,
        outcome=view.outcome.value,
        scope=view.scope.value if view.scope else None,
        reason_code=view.reason_code.value,
        role_space_version=space.version,
        role_space_hash=space.content_hash,
    )


def _accessible(intent: str, role: str, authenticated: bool) -> bool:
    """Oturum bu intent'i (auth + min_role) gerçekten yapabilir mi?"""

    effective_role = role if authenticated else "ziyaretci"
    view = get_role_space(effective_role).view_for(intent)
    return view is not None and view.outcome is AccessOutcome.ALLOW


def _is_confusable_pair(intent_a: str, intent_b: str) -> bool:
    """İki intent must_not_match ile (herhangi yönde) karışabilir işaretli mi?"""

    info_a = get_intent(intent_a)
    info_b = get_intent(intent_b)
    a_targets = set(info_a.get("must_not_match", [])) if info_a else set()
    b_targets = set(info_b.get("must_not_match", [])) if info_b else set()
    return intent_b in a_targets or intent_a in b_targets


def decide_core(
    rule_match: "rules.RuleMatch | None",
    ranked: list[ScoredIntent] | None,
    role: str,
    authenticated: bool,
    *,
    in_domain: bool = True,
    threshold: float = DEFAULT_THRESHOLD,
    tie_margin: float = DEFAULT_TIE_MARGIN,
    top_k: int = DEFAULT_TOP_K,
    role_redirect_margin: float = DEFAULT_ROLE_REDIRECT_MARGIN,
) -> Decision:
    """Önceden hesaplanmış kural/benzerlik sonuçlarından nihai kararı üretir.

    Karar mantığının tek yetkili yeri; hem `decide` hem de loglama boru hattı
    (per-stage zamanlama için) bunu kullanır.

    in_domain=False ise (alan kapısı) benzerlik skoru yüksek olsa bile FALLBACK'e
    düşülür — kural katmanı bu kapıdan muaftır (yüksek kesinlik).
    """

    if rule_match is not None:
        decision = Decision(
            intent=rule_match.intent,
            fallback=False,
            source="rule",
            confidence=1.0,
        )
        return _apply_role_gating(decision, role, authenticated)

    if not ranked:
        return Decision(intent=None, fallback=True, source="fallback", confidence=0.0)

    top1 = ranked[0]
    if (not in_domain) or top1.score < threshold:
        return Decision(
            intent=None,
            fallback=True,
            source="fallback",
            confidence=top1.score,
            top_k=tuple(ranked[:top_k]),
        )

    margin: float | None = None
    tie_break: str | None = None
    if len(ranked) >= 2:
        margin = top1.score - ranked[1].score
        if margin < tie_margin and _is_confusable_pair(top1.intent, ranked[1].intent):
            tie_break = f"{top1.intent}~{ranked[1].intent}"

    # V2 closed-space invariant: candidates were produced inside one concrete
    # role-space. Never redirect to another candidate based on a global role
    # hierarchy; the chosen view carries its own allow/deny policy.
    chosen = top1
    role_redirect: str | None = None

    decision = Decision(
        intent=chosen.intent,
        fallback=False,
        source="similarity",
        confidence=chosen.score,
        top_k=tuple(ranked[:top_k]),
        margin=margin,
        tie_break=tie_break,
        role_redirect=role_redirect,
    )
    return _apply_role_gating(decision, role, authenticated)


def decide(
    query: str,
    role: str = "ziyaretci",
    authenticated: bool = False,
    *,
    matcher: SimilarityMatcher | None = None,
    threshold: float = DEFAULT_THRESHOLD,
    tie_margin: float = DEFAULT_TIE_MARGIN,
    top_k: int = DEFAULT_TOP_K,
) -> Decision:
    """Bir sorgu için nihai kararı üretir."""

    effective_role = role if authenticated else "ziyaretci"
    space = get_role_space(effective_role)
    matcher = matcher or space.similarity_matcher
    rule_match = space.rule_matcher.match(query)
    ranked = None if rule_match is not None else matcher.rank(query)
    if ranked is not None:
        # Legacy injected matchers remain supported, but their candidates are
        # projected into this role's local view set and tagged accordingly.
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
    return decide_core(
        rule_match,
        ranked,
        role,
        authenticated,
        in_domain=in_domain,
        threshold=threshold,
        tie_margin=tie_margin,
        top_k=top_k,
    )
