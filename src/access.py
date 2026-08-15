"""Typed role-space access contract.

The legacy catalog describes content.  This module describes whether a piece of
content is actionable for one concrete, trusted role.  Keeping those concerns
separate prevents a global retrieval result from becoming authorised merely
because a rank-based ``min_role`` comparison happened to pass.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
from typing import Any, Mapping


class AccessOutcome(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    CLARIFY = "clarify"
    FALLBACK = "fallback"


class AccessScope(str, Enum):
    GENERAL = "general"
    OWN = "own"
    LINKED_CHILD = "linked_child"
    ENROLLED_COURSE = "enrolled_course"
    MANAGED_COURSE = "managed_course"
    OWNED_RESOURCE = "owned_resource"
    PARTICIPANT = "participant"
    REQUESTER = "requester"
    EVENT_AUDIENCE = "event_audience"
    SCHOOL = "school"


class ReasonCode(str, Enum):
    ALLOWED = "allowed"
    AUTHENTICATION_REQUIRED = "authentication_required"
    ROLE_NOT_PERMITTED = "role_not_permitted"
    EXACT_STUDENT_ONLY = "exact_student_only"
    LINKED_STUDENT_SCOPE = "linked_student_scope"
    TEACHER_OR_HIGHER_REQUIRED = "teacher_or_higher_required"
    UI_ROUTE_UNAVAILABLE = "ui_route_unavailable"
    CONTEXT_REQUIRED = "context_required"


@dataclass(frozen=True)
class RoleIntentView:
    """One intent as compiled for exactly one role."""

    role: str
    intent: str
    outcome: AccessOutcome
    scope: AccessScope | None
    reason_code: ReasonCode
    response_id: str
    response_template: str
    examples: tuple[str, ...]
    action_id: str
    clarification: str | None = None
    required_role: str | None = None
    route_key: str | None = None
    route_label: str | None = None

    @property
    def view_id(self) -> str:
        return f"{self.role}:{self.intent}"


@dataclass(frozen=True)
class CompiledRoleSpace:
    """Immutable retrieval and policy bundle for one trusted role."""

    role: str
    version: str
    content_hash: str
    views: Mapping[str, RoleIntentView]
    rule_matcher: Any
    similarity_matcher: Any
    domain_vocab: frozenset[str]

    def view_for(self, intent: str) -> RoleIntentView | None:
        return self.views.get(intent)

    @property
    def space_id(self) -> str:
        return f"{self.version}:{self.role}:{self.content_hash[:12]}"

    @classmethod
    def immutable_views(cls, views: dict[str, RoleIntentView]) -> Mapping[str, RoleIntentView]:
        return MappingProxyType(dict(views))
