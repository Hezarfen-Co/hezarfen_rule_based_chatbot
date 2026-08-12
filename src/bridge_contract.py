"""Backend ``chat.reply`` payload'ını Çelebi oturumuna dönüştürür.

Bu modül bilerek yalnızca stdlib kullanır: QUIC bağımlılığı kurulu olmadan da
backend–AI rol sözleşmesi birim testlerinde doğrulanabilsin.
"""

from __future__ import annotations

from typing import Any


def resolve_session(payload: dict[str, Any], default_role: str) -> tuple[str, bool]:
    """Doğrulanmış backend rolünü, geriye uyumlu alanlarla birlikte çöz.

    Güncel ve yetkili alan ``asker_role``'dür. ``session.role`` ile düz ``role``
    yalnızca eski backend sürümleri için tutulur; hiçbir alan yoksa yapılandırılmış
    yedek rol kullanılır.
    """

    asker_role = payload.get("asker_role")
    if asker_role:
        # Güncel backend bu alanı yalnız CurrentUser ile doğrulanmış chat
        # endpoint'inden üretir. Eski metadata kanonik rolün auth durumunu
        # düşüremez veya değiştiremez.
        return asker_role, True

    session = payload.get("session")
    session = session if isinstance(session, dict) else {}
    role = session.get("role") or payload.get("role") or default_role
    authenticated = session.get("authenticated")
    if authenticated is None:
        authenticated = role != "ziyaretci"
    return role, bool(authenticated)
