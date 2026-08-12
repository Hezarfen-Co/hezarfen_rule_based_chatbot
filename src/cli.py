"""Terminal (CLI) frontend — Hezarfen kullanım asistanı.

Backend'e (Engine) YALNIZCA istek/yanıt sözleşmesiyle bağlanır; iç katmanları
bilmez. Etkileşimli sohbet döngüsü + rol simülasyonu + komutlar.

Komutlar:
    /rol <rol>   -> oturum rolünü değiştir (ziyaretci/ogrenci/ogretmen/yonetici/admin)
    /roller      -> geçerli rolleri listele
    /yardim      -> yardım
    /cikis       -> çık
"""

from __future__ import annotations

from typing import Any, Callable

from .catalog import ROLE_HIERARCHY
from .engine import Engine, RequestError

_EXIT_COMMANDS = {"/cikis", "/çıkış", "/quit", "/exit"}


class ChatSession:
    """Terminal oturum durumu (rol) + backend'e köprü."""

    def __init__(self, engine: Engine | None = None, role: str = "ziyaretci") -> None:
        self._engine = engine or Engine()
        self.role = role
        self.authenticated = role != "ziyaretci"

    def set_role(self, role: str) -> str:
        if role not in ROLE_HIERARCHY:
            return f"Bilinmeyen rol: {role!r}. Geçerli: {', '.join(ROLE_HIERARCHY)}"
        self.role = role
        self.authenticated = role != "ziyaretci"
        return f"Rol ayarlandı: {role} (authenticated={self.authenticated})"

    def ask(self, query: str) -> dict[str, Any]:
        return self._engine.handle(
            {
                "query": query,
                "session": {"role": self.role, "authenticated": self.authenticated},
            }
        )

    @staticmethod
    def format_response(resp: dict[str, Any]) -> str:
        safety = resp.get("safety") or {}
        if safety.get("decision") and safety["decision"] != "ALLOW" and resp["intent"] is None:
            tag = f"safety:{safety['category']}"
        elif resp["fallback"]:
            tag = "fallback"
        else:
            tag = resp["intent"]
        return f"[{tag}] {resp['text']}"

    def handle_line(self, line: str) -> tuple[str | None, bool]:
        """Bir girdi satırını işler. Döner: (gösterilecek_metin, çıkılsın_mı)."""

        line = line.strip()
        if not line:
            return None, False

        if line in _EXIT_COMMANDS:
            return "Görüşürüz!", True

        if line.startswith("/"):
            return self._handle_command(line), False

        try:
            resp = self.ask(line)
        except RequestError as exc:
            return f"Hata: {exc}", False
        return self.format_response(resp), False

    def _handle_command(self, line: str) -> str:
        parts = line.split()
        cmd = parts[0].lower()
        if cmd in {"/rol", "/role"}:
            if len(parts) < 2:
                return "Kullanım: /rol <ziyaretci|ogrenci|ogretmen|yonetici|admin>"
            return self.set_role(parts[1].lower())
        if cmd in {"/roller", "/roles"}:
            return "Geçerli roller: " + ", ".join(ROLE_HIERARCHY)
        if cmd in {"/yardim", "/help"}:
            return _HELP_TEXT
        return f"Bilinmeyen komut: {cmd}. /yardim yaz."


_HELP_TEXT = (
    "Hezarfen kullanım asistanı. Bir soru yaz (ör. 'sınav nasıl oluşturulur').\n"
    "Komutlar: /rol <rol>, /roller, /yardim, /cikis"
)

_BANNER = (
    "=== Çelebi — Hezarfen Kullanım Asistanı (terminal) ===\n"
    "Rolünü /rol ile ayarla, soru sor. Çıkış: /cikis\n"
)


def run(
    session: ChatSession | None = None,
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
) -> None:
    """Etkileşimli sohbet döngüsü (input/output enjekte edilebilir -> test edilebilir)."""

    session = session or ChatSession()
    output_fn(_BANNER)
    while True:
        try:
            line = input_fn(f"({session.role}) > ")
        except (EOFError, KeyboardInterrupt):
            output_fn("\nGörüşürüz!")
            return
        text, should_exit = session.handle_line(line)
        if text is not None:
            output_fn(text)
        if should_exit:
            return


def main() -> int:
    # Windows konsollarında (cp1254) Türkçe/işaret karakterleri için UTF-8'e geç.
    import sys

    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8")
            except Exception:  # pragma: no cover - platforma bağlı
                pass

    run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
