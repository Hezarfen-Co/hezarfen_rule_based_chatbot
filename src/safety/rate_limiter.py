"""Spam / kötüye kullanım için kullanıcı bazlı mesaj sıklığı ve tekrar kontrolü.

Bellek-içi ve basit; süreç ömrü boyunca durum tutar. Zaman kaynağı test için
enjekte edilebilir (time_fn). Not: Çok-instance dağıtımda paylaşımlı bir depo
(ör. Redis) gerekir; bu sınıf tek süreç kapsamındadır.
"""

from __future__ import annotations

import time
from collections import defaultdict
from typing import Callable

from .decisions import TEMPORARY_LIMIT, SafetyDecision, make_decision as _make
from .toxicity import safety_normalize


class RateLimiter:
    """Kullanıcı bazlı mesaj sıklığı ve tekrar kontrolü (kötüye kullanım)."""

    def __init__(
        self,
        max_requests: int = 20,
        window_seconds: float = 60.0,
        max_repeats: int = 4,
        time_fn: Callable[[], float] = time.time,
    ) -> None:
        self._max = max_requests
        self._window = window_seconds
        self._max_repeats = max_repeats
        self._time = time_fn
        self._events: dict[str, list[float]] = defaultdict(list)
        self._last: dict[str, str] = {}
        self._repeat_count: dict[str, int] = defaultdict(int)

    def check(self, user_key: str, message: str) -> SafetyDecision | None:
        """Limit aşıldıysa TEMPORARY_LIMIT kararı, aksi hâlde None döndürür."""

        now = self._time()
        events = [t for t in self._events[user_key] if now - t < self._window]
        events.append(now)
        self._events[user_key] = events
        if len(events) > self._max:
            return _make(TEMPORARY_LIMIT, "SPAM_RATE", 2, "SAFE-RATE-001",
                         "Çok fazla istek gönderdin. Lütfen biraz bekleyip tekrar dene.")

        norm = safety_normalize(message)
        if self._last.get(user_key) == norm:
            self._repeat_count[user_key] += 1
        else:
            self._repeat_count[user_key] = 1
            self._last[user_key] = norm
        if self._repeat_count[user_key] >= self._max_repeats:
            return _make(TEMPORARY_LIMIT, "SPAM_REPEAT", 2, "SAFE-RATE-002",
                         "Aynı mesajı tekrar tekrar gönderiyorsun. Lütfen farklı bir şey dene.")
        return None
