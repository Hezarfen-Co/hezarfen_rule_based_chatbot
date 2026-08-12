"""QUIC köprü istemcisi — Çelebi'yi Rust backend'in AI köprüsüne bağlar.

Backend (``hezarfen_backend``) bir QUIC **sunucusudur**: AI servisleri ona
*dial-in* eder, sundukları yetenekleri (`capabilities`) kaydeder ve backend her
sohbet turunu bu bağlantı üzerinden bir isteğe çevirir. Bu modül o istemcinin
Python tarafıdır; wire protokolü backend'deki ``src/ai/protocol.rs`` ("hab/1")
ile birebir aynıdır.

Akış (bkz. backend ``src/ai/mod.rs`` ve ``server.rs``):

1. Backend'in HTTP'sinden sertifikayı çek (``GET /ai/certificate``) ve pinle.
   Self-signed sertifika her açılışta yenilendiği için her (yeniden) bağlanmada
   tazelenir.
2. QUIC ile ``AI_QUIC_ADDR``'e bağlan (ALPN ``hab/1``).
3. İlk *client-initiated* çift yönlü akış = **kontrol akışı**: bir ``Hello``
   yaz, bir ``Greeting`` oku, akışı hayat boyu açık tut (kapanması = kayıttan
   düşme sinyali).
4. Her istek backend'in açtığı *server-initiated* çift yönlü bir akıştır: tek
   ``Request`` gelir, motoru çalıştırıp tek ``Response`` yazarız.

Çerçeveleme: 4 bayt big-endian uzunluk + o kadar bayt JSON.

Not — sözleşme sınırları (bilerek):
* Backend ``chat.reply`` üzerinden doğrulanmış güncel okul rolünü
  ``asker_role`` alanında gönderir. Çelebi bu rolü cevap kapsamı ve rol
  kapıları için kullanır. Eski backend sürümleriyle uyumluluk amacıyla
  ``session.role`` / ``role`` ve son çare olarak ``HEZARFEN_ASSISTANT_ROLE``
  desteği korunur. Gerçek yetki her zaman backend'de kalır.
* Çelebi tek-turludur; ``history`` yok sayılır (her mesaj bağımsız değerlendirilir).

Çalıştırma::

    python -m src.bridge

Ortam değişkenleri (hepsinin makul varsayılanı vardır)::

    AI_BRIDGE_HOST         QUIC ile bağlanılacak host   (vars. 127.0.0.1)
    AI_BRIDGE_PORT         QUIC portu (UDP)             (vars. 8090)
    AI_BACKEND_URL         Sertifika için HTTP kökü     (vars. http://127.0.0.1:8080)
    AI_SHARED_TOKEN        Hello'daki paylaşılan sır    (vars. change-me)
    AI_TLS_SERVER_NAME     TLS doğrulaması için ad      (vars. localhost)
    AI_SERVICE_NAME        Loglarda görünen servis adı  (vars. celebi)
    HEZARFEN_ASSISTANT_ROLE  Eski backend için yedek rol (vars. ogrenci)
    AI_MAX_CONCURRENT      Aynı anda kabul edilen istek (vars. 8)
    AI_RECONNECT_SECS      Kopunca yeniden deneme aralığı (vars. 3)
"""

from __future__ import annotations

import asyncio
import json
import os
import ssl
import struct
import sys
import urllib.error
import urllib.request
from functools import partial
from typing import Any

from aioquic.asyncio import connect
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import ConnectionTerminated, QuicEvent, StreamDataReceived

from .bridge_contract import resolve_session
from .engine import Engine, RequestError, get_default_engine

# --- Protokol sabitleri (backend src/constant.rs ile eşleşir) ---------------
PROTOCOL = "hab/1"
CHAT_CAPABILITY = "chat.reply"
MAX_FRAME_BYTES = 8 * 1024 * 1024
KEEPALIVE_SECS = 10  # backend AI_IDLE_TIMEOUT_SECS=30; altında tutulur


def _env(name: str, default: str) -> str:
    value = os.environ.get(name)
    return value if value is not None and value.strip() else default


class CapabilityError(Exception):
    """İşlenmiş bir hata — Response::Err {code, message} olarak döner."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


# --- Çerçeveleme ------------------------------------------------------------
def _encode_frame(obj: Any) -> bytes:
    body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
    if len(body) > MAX_FRAME_BYTES:
        raise CapabilityError("frame_too_large", f"{len(body)} bayt çerçeve sınırı aşıyor")
    return struct.pack(">I", len(body)) + body


class _FrameStream:
    """Bir QUIC akışından gelen baytları length-prefixed JSON çerçevelere böler."""

    def __init__(self) -> None:
        self._buf = bytearray()
        self._queue: asyncio.Queue[bytes | None] = asyncio.Queue()
        self._eof = False

    def feed(self, data: bytes, end: bool) -> None:
        if data:
            self._queue.put_nowait(data)
        if end:
            self._queue.put_nowait(None)

    async def _read_exact(self, n: int) -> bytes:
        while len(self._buf) < n:
            if self._eof:
                raise EOFError("çerçeve tamamlanmadan akış bitti")
            chunk = await self._queue.get()
            if chunk is None:
                self._eof = True
                continue
            self._buf.extend(chunk)
        out = bytes(self._buf[:n])
        del self._buf[:n]
        return out

    async def read_frame(self) -> Any:
        header = await self._read_exact(4)
        (length,) = struct.unpack(">I", header)
        if length > MAX_FRAME_BYTES:
            raise CapabilityError("frame_too_large", f"{length} bayt çerçeve sınırı aşıyor")
        body = await self._read_exact(length)
        return json.loads(body)


class BridgeProtocol(QuicConnectionProtocol):
    """Tek bir QUIC bağlantısını yöneten protokol: handshake + istek servisi."""

    def __init__(self, *args: Any, config: "BridgeConfig", engine: Engine, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._config = config
        self._engine = engine
        self._streams: dict[int, _FrameStream] = {}
        self._control_sid: int | None = None
        self._ping_uid = 0

    # -- aioquic olay kancası --
    def quic_event_received(self, event: QuicEvent) -> None:
        if isinstance(event, StreamDataReceived):
            stream = self._streams.get(event.stream_id)
            if stream is None:
                stream = _FrameStream()
                self._streams[event.stream_id] = stream
                # server-initiated bidi (id % 4 == 1) => yeni bir istek
                if event.stream_id % 4 == 1:
                    asyncio.ensure_future(self._serve_request(event.stream_id, stream))
            stream.feed(event.data, event.end_stream)
        elif isinstance(event, ConnectionTerminated):
            for stream in self._streams.values():
                stream.feed(b"", end=True)

    # -- kontrol akışı: Hello / Greeting --
    async def register(self) -> None:
        sid = self._quic.get_next_available_stream_id()
        self._control_sid = sid
        stream = _FrameStream()
        self._streams[sid] = stream
        hello = {
            "protocol": PROTOCOL,
            "service": self._config.service,
            "capabilities": [CHAT_CAPABILITY],
            "token": self._config.token,
            "max_concurrent": self._config.max_concurrent,
        }
        # Kontrol akışı hayat boyu açık kalır -> end_stream=False.
        self._send_frame(sid, hello, end=False)
        greeting = await asyncio.wait_for(stream.read_frame(), timeout=10)
        kind = greeting.get("type")
        if kind == "welcome":
            print(
                f"[bridge] kayıt başarılı: worker_id={greeting.get('worker_id')} "
                f"protocol={greeting.get('protocol')}",
                flush=True,
            )
            return
        code = greeting.get("code", "?")
        message = greeting.get("message", "")
        raise RuntimeError(f"backend kaydı reddetti ({code}): {message}")

    def _send_frame(self, sid: int, obj: Any, end: bool) -> None:
        self._quic.send_stream_data(sid, _encode_frame(obj), end_stream=end)
        self.transmit()

    # -- istek servisi --
    async def _serve_request(self, sid: int, stream: _FrameStream) -> None:
        try:
            request = await stream.read_frame()
        except (EOFError, CapabilityError, ValueError) as exc:
            print(f"[bridge] istek {sid} okunamadı: {exc}", flush=True)
            self._streams.pop(sid, None)
            return

        req_id = request.get("id", "")
        capability = request.get("capability", "")
        payload = request.get("payload") or {}
        deadline_ms = request.get("deadline_ms")
        try:
            timeout = (deadline_ms / 1000.0) if isinstance(deadline_ms, (int, float)) else None
            text = await asyncio.wait_for(self._reply(capability, payload), timeout=timeout)
            response: dict[str, Any] = {"status": "ok", "id": req_id, "payload": {"text": text}}
        except CapabilityError as exc:
            response = {"status": "err", "id": req_id, "code": exc.code, "message": str(exc)}
        except asyncio.TimeoutError:
            response = {"status": "err", "id": req_id, "code": "timed_out",
                        "message": "motor süre içinde cevap veremedi"}
        except Exception as exc:  # pragma: no cover - beklenmeyen
            print(f"[bridge] istek {req_id} işlenemedi: {exc}", flush=True)
            response = {"status": "err", "id": req_id, "code": "internal",
                        "message": "beklenmeyen hata"}

        try:
            self._send_frame(sid, response, end=True)
        except Exception as exc:  # pragma: no cover
            print(f"[bridge] cevap {req_id} yazılamadı: {exc}", flush=True)
        finally:
            self._streams.pop(sid, None)

    async def _reply(self, capability: str, payload: dict[str, Any]) -> str:
        if capability != CHAT_CAPABILITY:
            raise CapabilityError("unsupported_capability", f"bilinmeyen yetenek: {capability}")
        message = payload.get("message")
        if not isinstance(message, str):
            raise CapabilityError("bad_request", "'message' bir metin olmalı")
        # Motor senkron/CPU işidir -> event loop'u bloklamasın diye thread'e al.
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._run_engine, message, payload)

    def _resolve_session(self, payload: dict[str, Any]) -> tuple[str, bool]:
        """Rolü backend'in ilettiği payload'dan al; iletmezse varsayılana düş.

        Güncel backend sözleşmesinin güvenilir alanı `asker_role`'dür. Eski
        sözleşmelerdeki `session: {role, authenticated}` ve düz `role` alanları
        geriye uyumluluk için kabul edilir. Engine İngilizce rol adlarını da
        (student/teacher/manager/parent/admin) kabul eder. Hiçbiri yoksa
        `HEZARFEN_ASSISTANT_ROLE` (varsayılan 'ogrenci') kullanılır.
        """
        return resolve_session(payload, self._config.role)

    def _run_engine(self, message: str, payload: dict[str, Any]) -> str:
        role, authenticated = self._resolve_session(payload)
        request = {
            "query": message,
            # Rol backend payload'ından gelir (yoksa varsayılan). history bilerek
            # atlanır: Çelebi tek-turludur.
            "session": {"role": role, "authenticated": authenticated},
        }
        try:
            result = self._engine.handle(request)
        except RequestError as exc:
            raise CapabilityError("bad_request", str(exc)) from exc
        text = result.get("text")
        if not isinstance(text, str) or not text.strip():
            raise CapabilityError("empty_reply", "motor boş cevap üretti")
        return text

    async def keepalive(self) -> None:
        """Boşta kalan bağlantı backend'in idle timeout'unda düşmesin diye PING."""
        while True:
            await asyncio.sleep(KEEPALIVE_SECS)
            self._ping_uid += 1
            try:
                self._quic.send_ping(self._ping_uid)
                self.transmit()
            except Exception:
                return


class BridgeConfig:
    def __init__(self) -> None:
        self.host = _env("AI_BRIDGE_HOST", "127.0.0.1")
        self.port = int(_env("AI_BRIDGE_PORT", "8090"))
        self.backend_url = _env("AI_BACKEND_URL", "http://127.0.0.1:8080").rstrip("/")
        self.token = _env("AI_SHARED_TOKEN", "change-me")
        self.server_name = _env("AI_TLS_SERVER_NAME", "localhost")
        self.service = _env("AI_SERVICE_NAME", "celebi")
        self.role = _env("HEZARFEN_ASSISTANT_ROLE", "ogrenci")
        self.max_concurrent = int(_env("AI_MAX_CONCURRENT", "8"))
        self.reconnect_secs = float(_env("AI_RECONNECT_SECS", "3"))


def _fetch_certificate(backend_url: str) -> str:
    """Backend'in köprü sertifikasını (PEM) çeker ve döndürür."""
    url = f"{backend_url}/ai/certificate"
    with urllib.request.urlopen(url, timeout=10) as resp:  # noqa: S310 (bilinen iç adres)
        data = json.loads(resp.read())
    pem = data.get("certificate_pem")
    if not pem:
        raise RuntimeError(f"{url} beklenen certificate_pem alanını döndürmedi")
    print(f"[bridge] sertifika alındı (fingerprint {data.get('fingerprint_sha256', '?')[:16]}…)",
          flush=True)
    return pem


async def _run_once(config: BridgeConfig, engine: Engine) -> None:
    cert_pem = _fetch_certificate(config.backend_url)

    quic_config = QuicConfiguration(is_client=True, alpn_protocols=[PROTOCOL])
    quic_config.server_name = config.server_name  # SAN: localhost / 127.0.0.1
    quic_config.verify_mode = ssl.CERT_REQUIRED
    # aioquic cadata'yı bytes olarak bekler (içeride bytes boundary ile böler);
    # str geçmek `str.split(bytes)` TypeError'ına yol açar.
    quic_config.load_verify_locations(cadata=cert_pem.encode("utf-8"))  # sertifikayı pinle
    quic_config.idle_timeout = 30.0

    create = partial(BridgeProtocol, config=config, engine=engine)
    print(f"[bridge] {config.host}:{config.port} adresine bağlanılıyor (ALPN {PROTOCOL})…",
          flush=True)
    async with connect(
        config.host,
        config.port,
        configuration=quic_config,
        create_protocol=create,
    ) as protocol:
        assert isinstance(protocol, BridgeProtocol)
        await protocol.wait_connected()
        await protocol.register()
        keepalive_task = asyncio.ensure_future(protocol.keepalive())
        try:
            await protocol.wait_closed()
        finally:
            keepalive_task.cancel()
    print("[bridge] bağlantı kapandı", flush=True)


async def _main() -> int:
    config = BridgeConfig()
    print(f"[bridge] Çelebi köprüsü — servis='{config.service}', rol='{config.role}', "
          f"hedef={config.host}:{config.port}", flush=True)
    # Motoru (ve benzerlik matcher'ını) önceden kur: ilk istek hızlı olsun.
    engine = get_default_engine()
    print("[bridge] motor hazır", flush=True)

    while True:
        try:
            await _run_once(config, engine)
        except (urllib.error.URLError, ConnectionError, OSError) as exc:
            print(f"[bridge] backend'e ulaşılamadı: {exc}", flush=True)
        except Exception as exc:  # pragma: no cover - döngüyü ayakta tut
            print(f"[bridge] bağlantı hatası: {exc}", flush=True)
        print(f"[bridge] {config.reconnect_secs}s sonra yeniden denenecek…", flush=True)
        await asyncio.sleep(config.reconnect_secs)


def main() -> int:
    try:
        return asyncio.run(_main())
    except KeyboardInterrupt:
        print("\n[bridge] durduruldu.", flush=True)
        return 0


if __name__ == "__main__":
    sys.exit(main())
