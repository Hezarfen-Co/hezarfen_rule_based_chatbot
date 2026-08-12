"""İçerik güvenliği & yetki paketi.

Alt-modüller:
    decisions      — standart SafetyDecision modeli + karar türleri
    toxicity       — toksik/zararlı içerik tespiti (giriş kapısı + çıktı kontrolü)
    pii            — kişisel veri tespiti ve maskeleme
    rate_limiter   — spam/tekrar sıklık kontrolü
    authorization  — IDOR/BOLA parametre-yetki doğrulaması (ayrı içe aktarılır)

Motor (engine) yalnızca bu paketin genel API'sini kullanır; alt-modül düzenini bilmez.
`authorization` sabitleri (ALLOW/REQUIRE_AUTHORIZATION) toxicity ile çakıştığından
bilerek buradan RE-EXPORT EDİLMEZ; `from src.safety.authorization import ...` ile alınır.
"""

from __future__ import annotations

from .decisions import (
    ALLOW,
    ALLOW_WITH_WARNING,
    ASK_CLARIFICATION,
    BLOCK,
    BLOCKING_DECISIONS,
    ESCALATE_TO_HUMAN,
    MASK_AND_ALLOW,
    REQUIRE_AUTHORIZATION,
    RULE_VERSION,
    SAFE_RESPONSE,
    TEMPORARY_LIMIT,
    SafetyDecision,
)
from .pii import mask_pii
from .rate_limiter import RateLimiter
from .toxicity import (
    MAX_MESSAGE_LEN,
    evaluate_input,
    evaluate_output,
    safety_normalize,
    safety_tokens,
)

__all__ = [
    "ALLOW",
    "ALLOW_WITH_WARNING",
    "ASK_CLARIFICATION",
    "BLOCK",
    "BLOCKING_DECISIONS",
    "ESCALATE_TO_HUMAN",
    "MASK_AND_ALLOW",
    "REQUIRE_AUTHORIZATION",
    "RULE_VERSION",
    "SAFE_RESPONSE",
    "TEMPORARY_LIMIT",
    "SafetyDecision",
    "mask_pii",
    "RateLimiter",
    "MAX_MESSAGE_LEN",
    "evaluate_input",
    "evaluate_output",
    "safety_normalize",
    "safety_tokens",
]
