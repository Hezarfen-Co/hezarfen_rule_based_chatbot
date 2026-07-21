"""Standart içerik-güvenliği karar modeli — tüm güvenlik alt-modüllerinin ortak dili.

Karar türleri, `SafetyDecision` veri sınıfı ve kararları üreten `_make` yardımcısı
burada tanımlıdır. `toxicity`, `pii` ve `rate_limiter` alt-modülleri bu tek modele
göre karar döndürür; motor (engine) bunları giriş kapısı/çıktı kontrolü olarak kullanır.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Final


RULE_VERSION: Final[str] = "1.0.0"

# --- Karar türleri -----------------------------------------------------------
ALLOW: Final[str] = "ALLOW"
ALLOW_WITH_WARNING: Final[str] = "ALLOW_WITH_WARNING"
MASK_AND_ALLOW: Final[str] = "MASK_AND_ALLOW"
BLOCK: Final[str] = "BLOCK"
ASK_CLARIFICATION: Final[str] = "ASK_CLARIFICATION"
REQUIRE_AUTHORIZATION: Final[str] = "REQUIRE_AUTHORIZATION"
ESCALATE_TO_HUMAN: Final[str] = "ESCALATE_TO_HUMAN"
SAFE_RESPONSE: Final[str] = "SAFE_RESPONSE"
TEMPORARY_LIMIT: Final[str] = "TEMPORARY_LIMIT"

# Girişi durduran (intent'e geçmeyen) kararlar.
BLOCKING_DECISIONS: Final[frozenset[str]] = frozenset(
    {BLOCK, ESCALATE_TO_HUMAN, SAFE_RESPONSE, REQUIRE_AUTHORIZATION, TEMPORARY_LIMIT, ASK_CLARIFICATION}
)


@dataclass(frozen=True)
class SafetyDecision:
    """Standart içerik-güvenliği kararı."""

    decision: str
    category: str
    severity: int  # 0 (temiz) .. 5 (en ağır)
    rule_id: str
    confidence: float
    user_message: str
    requires_review: bool = False
    rule_version: str = RULE_VERSION
    masked_message: str | None = None  # MASK_AND_ALLOW için
    matched: tuple[str, ...] = field(default_factory=tuple)


def make_decision(decision, category, severity, rule_id, message, *, review=False,
                  masked=None, matched=()) -> SafetyDecision:
    """Kısa yoldan bir SafetyDecision üretir (varsayılan confidence=0.9)."""

    return SafetyDecision(
        decision=decision,
        category=category,
        severity=severity,
        rule_id=rule_id,
        confidence=0.9,
        user_message=message,
        requires_review=review,
        masked_message=masked,
        matched=tuple(matched),
    )
