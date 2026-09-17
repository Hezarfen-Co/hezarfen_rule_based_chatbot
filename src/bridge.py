"""QUIC köprü istemcisi — Çelebi'yi Rust backend'in AI köprüsüne bağlar.

Backend (``hezarfen_backend``) bir QUIC **sunucusudur**: AI servisleri ona
*dial-in* eder, sundukları yetenekleri (`capabilities`) kaydeder ve backend her
sohbet turunu bu bağlantı üzerinden bir isteğe çevirir. Bu modül o istemcinin
Python tarafıdır; wire protokolü backend'deki ``src/ai/protocol.rs`` ("hab/2")
ile birebir aynıdır.

Akış (bkz. backend ``src/ai/mod.rs`` ve ``server.rs``):

1. Backend'in HTTP'sinden sertifikayı çek (``GET /ai/certificate``) ve pinle.
   Self-signed sertifika her açılışta yenilendiği için her (yeniden) bağlanmada
   tazelenir. Sertifikanın SHA-256'sı PEM'den *kendimiz* hesaplanır: sunucunun
   yanındaki ``fingerprint_sha256`` alanı yalnızca çapraz denetlenir (sertifikayı
   uyduran taraf parmak izini de uydurur). ``AI_TLS_FINGERPRINT`` verilmişse
   hesaplanan iz onunla eşleşmezse BAĞLANMAYIZ; boşsa TOFU (her açılışta
   uyarıyla loglanır).
2. QUIC ile ``AI_QUIC_ADDR``'e bağlan (ALPN ``hab/2``).
3. İlk *client-initiated* çift yönlü akış = **kontrol akışı**: bir ``Hello``
   yaz, bir ``Greeting`` oku, akışı hayat boyu açık tut (kapanması = kayıttan
   düşme sinyali).
4. Her istek backend'in açtığı *server-initiated* çift yönlü bir akıştır: tek
   ``Request`` gelir, motoru çalıştırıp tek ``Response`` yazarız. hab/2'de
   ``Request.school`` zorunludur ve ``Response`` onu yankılar; ikisi de eksikse
   backend çerçeveyi reddeder.

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
    AI_RECONNECT_MAX_SECS  Geri çekilmenin tavanı (vars. 120)
    AI_TLS_FINGERPRINT     Beklenen sertifika SHA-256'sı; boş = TOFU

Kalıcı bir red (``unsupported_protocol`` / ``unauthorized``) bir daha
DENENMEZ DEĞİL, ama hızlı denenmez: çıkış yapmak yerine geri çekilme tavana
çekilir, her durum değişiminde BİR kez loglanır ve yapılandırma düzelince
servis kendi kendine toparlanır. Çıkış yapan bir köprü ``restart:
unless-stopped`` altında sonsuz bir crash-loop'a girer ve operatör elle
müdahale etmeden geri gelmez.
"""

from __future__ import annotations

import asyncio
import base64
import binascii
import hashlib
import json
import os
import random
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
# AI_PROTOCOL/AI_ALPN backend'de "hab/2": sunucu hello.protocol'u bununla
# karşılaştırır ve ALPN listesi de aynı dizedir. Sürüm burada geride kalırsa
# backend kaydı reddeder ("this backend speaks hab/2, the service announced …").
PROTOCOL = "hab/2"
CHAT_CAPABILITY = "chat.reply"
MAX_FRAME_BYTES = 8 * 1024 * 1024
KEEPALIVE_SECS = 10  # backend AI_IDLE_TIMEOUT_SECS=30; altında tutulur

#: Yapılandırma değişmeden düzelmeyecek `RejectCode`'lar (backend
#: ``ai/protocol.rs:123-130``). Kardeş servis zeka ile BİREBİR aynı küme: aynı
#: wire'ı konuşan üç servisin geri çekilme davranışı da aynı olmalı.
#: ``malformed``/``no_capabilities`` bilerek dışarıda — onlar bizim hatamız
#: olsa da geçici bir çakışmadan (ör. yarıda kalmış bir deploy) doğabilir ve
#: üstel geri çekilme onları da zaten seyrekleştirir.
PERMANENT_REJECTS = ("unsupported_protocol", "unauthorized")


def _env(name: str, default: str) -> str:
    value = os.environ.get(name)
    return value if value is not None and value.strip() else default


class CapabilityError(Exception):
    """İşlenmiş bir hata — Response::Err {code, message} olarak döner."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


class HandshakeRejected(Exception):
    """Backend `Greeting{type:"rejected"}` ile kaydı reddetti.

    Bu bir çökme DEĞİL, bir teşhistir: ``permanent`` ise yapılandırma
    düzelmeden geçmez, o yüzden çağıran onu bekleyerek karşılar (çıkmaz).
    """

    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"backend kaydı reddetti ({code}): {message}")
        self.code = code
        self.message = message

    @property
    def permanent(self) -> bool:
        return self.code in PERMANENT_REJECTS


# --- Çerçeveleme ------------------------------------------------------------
def build_hello(config: "BridgeConfig") -> dict[str, Any]:
    """hab/2 ``Hello`` gövdesi — backend `ai/protocol.rs:84-101` ile aynı alanlar.

    ``protocol`` backend'in ``AI_PROTOCOL`` sabitiyle birebir eşleşmek
    ZORUNDADIR: sunucu bunu ALPN'de **ve** gövdede ayrı ayrı denetler, eski bir
    sürüm dizesi kaydı reddettirir.
    """
    return {
        "protocol": PROTOCOL,
        "service": config.service,
        "capabilities": [CHAT_CAPABILITY],
        "token": config.token,
        "max_concurrent": config.max_concurrent,
    }


def ok_response(req_id: str, school: str, text: str) -> dict[str, Any]:
    """``Response{status:"ok"}``. ``school`` backend'in çerçeve denetimidir."""
    return {"status": "ok", "id": req_id, "school": school, "payload": {"text": text}}


def err_response(req_id: str, school: str, code: str, message: str) -> dict[str, Any]:
    """``Response{status:"err"}`` — reddin HANGİ okula ait olduğu da taşınır."""
    return {"status": "err", "id": req_id, "school": school, "code": code, "message": message}


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
        hello = build_hello(self._config)
        # Kontrol akışı hayat boyu açık kalır -> end_stream=False.
        self._send_frame(sid, hello, end=False)
        greeting = await asyncio.wait_for(stream.read_frame(), timeout=10)
        kind = greeting.get("type")
        if kind == "welcome":
            # Backend hoş geldin derken BAŞKA bir sürüm yankılayabilir; uyuşmayan
            # bir sürümle devam etmek yanlış ayrışacak çerçeveler yazmak demektir.
            echoed = greeting.get("protocol", "")
            if echoed and echoed != PROTOCOL:
                raise HandshakeRejected(
                    "unsupported_protocol",
                    f"backend '{echoed}' yankıladı, biz '{PROTOCOL}' konuşuyoruz",
                )
            print(
                f"[bridge] kayıt başarılı: worker_id={greeting.get('worker_id')} "
                f"protocol={echoed or PROTOCOL}",
                flush=True,
            )
            return
        raise HandshakeRejected(
            str(greeting.get("code", "?")), str(greeting.get("message", ""))
        )

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
        # hab/2: her istek kendi OKULUNU adıyla taşır ve cevap onu yankılar.
        # Bu alan eksikse backend çerçeveyi reddeder (mesaj error_code=protocol
        # ile düşer) — sürüm dizesi tek başına yetmez.
        school = request.get("school", "")
        capability = request.get("capability", "")
        payload = request.get("payload") or {}
        deadline_ms = request.get("deadline_ms")
        try:
            timeout = (deadline_ms / 1000.0) if isinstance(deadline_ms, (int, float)) else None
            text = await asyncio.wait_for(self._reply(capability, payload), timeout=timeout)
            response = ok_response(req_id, school, text)
        except CapabilityError as exc:
            response = err_response(req_id, school, exc.code, str(exc))
        except asyncio.TimeoutError:
            response = err_response(
                req_id, school, "timed_out", "motor süre içinde cevap veremedi"
            )
        except Exception as exc:  # pragma: no cover - beklenmeyen
            print(f"[bridge] istek {req_id} işlenemedi: {exc}", flush=True)
            response = err_response(req_id, school, "internal", "beklenmeyen hata")

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
        # Parmak izi karşılaştırması için iki nokta ayraçları ve büyük/küçük
        # harf farkı normalize edilir: `openssl ... | xxd` çıktısını yapıştırmak
        # iki noktalı olur ve operatörü sessizce reddettirmemelidir.
        self.tls_fingerprint = (
            _env("AI_TLS_FINGERPRINT", "").strip().lower().replace(":", "")
        )
        if self.tls_fingerprint and (
            len(self.tls_fingerprint) != 64
            or any(c not in "0123456789abcdef" for c in self.tls_fingerprint)
        ):
            raise ValueError(
                "AI_TLS_FINGERPRINT 64 karakterlik onaltılık bir SHA-256 olmalı "
                f"(iki nokta ayraçları atılır); alınan uzunluk: {len(self.tls_fingerprint)}"
            )
        self.service = _env("AI_SERVICE_NAME", "celebi")
        self.role = _env("HEZARFEN_ASSISTANT_ROLE", "ogrenci")
        self.max_concurrent = int(_env("AI_MAX_CONCURRENT", "8"))
        self.reconnect_secs = float(_env("AI_RECONNECT_SECS", "3"))
        self.reconnect_max_secs = float(_env("AI_RECONNECT_MAX_SECS", "120"))


def _leaf_der_from_pem(pem: str) -> bytes:
    """PEM zincirinin İLK sertifikasını DER olarak çıkar."""
    marker_begin = "-----BEGIN CERTIFICATE-----"
    marker_end = "-----END CERTIFICATE-----"
    start = pem.find(marker_begin)
    end = pem.find(marker_end)
    if start < 0 or end < 0:
        raise RuntimeError("sertifika PEM gövdesi bulunamadı")
    body = pem[start + len(marker_begin):end]
    try:
        return base64.b64decode("".join(body.split()))
    except (binascii.Error, ValueError) as exc:
        raise RuntimeError(f"sertifika PEM gövdesi base64 değil: {exc}") from exc


def _fetch_certificate(config: BridgeConfig) -> str:
    """`GET /ai/certificate` — HER (yeniden) bağlanmada çağrılır.

    Yalnız açılışta çağırmak yetmez: ``AI_TLS_CERT``/``AI_TLS_KEY`` boşsa
    backend her boot'ta kendi self-signed sertifikasını YENİDEN üretir, yani
    eski PEM'e güvenmek bir sonraki backend restart'ında bağlantıyı kırar.

    DÜZ HTTP'dir, o yüzden sertifikayı pinlemek tek başına yetmez: yolda araya
    giren biri kendi sertifikasını pinletebilir. İki denetim bunu kapatır —
    (a) sunucunun yanında bildirdiği ``fingerprint_sha256`` PEM'den hesapladığımızla
    eşleşmeli, (b) ``AI_TLS_FINGERPRINT`` verilmişse hesaplanan iz ona eşit olmalı.
    İkisinden biri düşerse BAĞLANILMAZ.
    """
    url = f"{config.backend_url}/ai/certificate"
    with urllib.request.urlopen(url, timeout=10) as resp:  # noqa: S310 (bilinen iç adres)
        data = json.loads(resp.read())
    pem = data.get("certificate_pem")
    if not pem:
        raise RuntimeError(f"{url} beklenen certificate_pem alanını döndürmedi")

    computed = hashlib.sha256(_leaf_der_from_pem(pem)).hexdigest()
    reported = str(data.get("fingerprint_sha256", "")).strip().lower().replace(":", "")
    if reported and reported != computed:
        # Sunucunun kendi beyanı kendi PEM'iyle tutmuyor: ya bozuk bir dağıtım ya
        # da yolda değiştirilmiş bir cevap. İkisinde de bağlanmıyoruz.
        raise RuntimeError(
            "sertifika tutarsız: bildirilen parmak izi PEM'den hesaplananla uyuşmuyor "
            f"(bildirilen {reported[:12]}, hesaplanan {computed[:12]})"
        )

    if config.tls_fingerprint:
        if computed != config.tls_fingerprint:
            raise RuntimeError(
                "sertifika parmak izi PINLENEN değerle uyuşmuyor; bağlanılmıyor "
                f"(beklenen {config.tls_fingerprint[:12]}, gelen {computed[:12]})"
            )
        print(f"[bridge] sertifika alındı ve PINLENDİ (fingerprint {computed[:16]}…)", flush=True)
    else:
        # Bilinçli bir taviz, sessiz bir varsayılan değil: her açılışta loglanır
        # ki operatör neyi kapalı bıraktığını görsün.
        print(
            f"[bridge] sertifika alındı (fingerprint {computed[:16]}…) — "
            "AI_TLS_FINGERPRINT tanımsız, TOFU ile güveniliyor; üretimde pinleyin",
            flush=True,
        )
    return pem


async def _run_once(config: BridgeConfig, engine: Engine) -> None:
    cert_pem = _fetch_certificate(config)

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


def next_backoff(current: float, config: BridgeConfig) -> float:
    """Üstel geri çekilme: ikiye katla ve tavanda dur.

    JITTER BURADA EKLENMEZ — uyumadan hemen önce, çağıran tarafta eklenir:
    jitter bir sonraki beklemenin TABANINI kaydırmamalıdır, yoksa rastgelelik
    birikerek gerçek tavanı aşar. Bu fonksiyon deterministik kalır, yani
    testten doğrulanabilir.
    """
    return min(current * 2.0, config.reconnect_max_secs)


async def run_forever(
    config: BridgeConfig,
    engine: Engine,
    connect_once: Any = _run_once,
    sleeper: Any = None,
) -> int:
    """Köprüyü sürekli ayakta tutar. HİÇBİR hatada ÇIKMAZ.

    Çıkış yapmak burada bir çözüm değil, bir arıza biçimidir: unit
    ``restart: unless-stopped`` ile çalışır, yani çıkan bir köprü sonsuz bir
    crash-loop üretir ve backend düzeltildikten sonra servis kendiliğinden
    toparlanmaz — operatörün elle müdahalesi gerekir. Kalıcı bir red
    (`unsupported_protocol`/`unauthorized`) ise bekleme TAVANA çekilerek
    karşılanır: gürültü yapmadan bekleriz, yapılandırma düzelince döneriz.

    Log durum değişiminde BİR kez atılır. Tavana çekilmiş bir red her ~2
    dakikada bir aynı satırı basarsa, gerçek bir arızayı arayan operatörün
    günlüğü kullanılamaz hale gelir.

    ``connect_once``/``sleeper`` enjeksiyonu test içindir: gerçek QUIC olmadan
    geri çekilme eğrisi ve "çıkmıyor" sözü doğrulanabilir.
    """
    sleep = sleeper or asyncio.sleep
    backoff = config.reconnect_secs
    state = ""
    while True:
        try:
            await connect_once(config, engine)
            # Sağlıklı bir oturumdan sonra bekleme sıfırlanır.
            backoff = config.reconnect_secs
            state = ""
            print(f"[bridge] {backoff:.1f}s sonra yeniden denenecek…", flush=True)
        # SIRA ÖNEMLİ: Python 3.11'den beri `asyncio.TimeoutError` yerleşik
        # `TimeoutError`'dir ve o da `OSError`'in alt sınıfıdır. Zaman aşımı
        # yakalayıcısı OSError'DAN ÖNCE gelmek zorunda; altına konursa
        # ERİŞİLEMEZ olur ve el sıkışma zaman aşımı "backend'e ulaşılamadı"
        # diye loglanır.
        except asyncio.TimeoutError:
            backoff = next_backoff(backoff, config)
            state = _log_state_change(state, "timeout", "[bridge] el sıkışma zaman aşımına uğradı")
        except (urllib.error.URLError, ConnectionError, OSError) as exc:
            backoff = next_backoff(backoff, config)
            state = _log_state_change(
                state, "unreachable", f"[bridge] backend'e ulaşılamadı: {exc}"
            )
        except HandshakeRejected as exc:
            if exc.permanent:
                # Tavana çekilmiş bir red her turda basılırsa log kullanılamaz
                # hale gelir; durum değişiminde bir kez söylenir.
                state = _log_state_change(
                    state,
                    f"rejected:{exc.code}",
                    f"[bridge] {exc} — yapılandırma değişmeden düzelmez; "
                    "yine de çıkmıyoruz, geri çekilerek yeniden denenecek",
                )
                backoff = config.reconnect_max_secs
            else:
                backoff = next_backoff(backoff, config)
                state = _log_state_change(state, f"rejected:{exc.code}", f"[bridge] {exc}")
        except Exception as exc:  # pragma: no cover - döngüyü ayakta tut
            backoff = next_backoff(backoff, config)
            state = _log_state_change(state, "error", f"[bridge] bağlantı hatası: {exc}")

        # Jitter, birden çok Çelebi örneği aynı anda düşerse backend'i eş
        # zamanlı bir dalgayla karşılamamak içindir.
        delay = backoff + random.uniform(0.0, min(backoff, 5.0))
        print(f"[bridge] {delay:.1f}s sonra yeniden denenecek…", flush=True)
        await sleep(delay)


def _log_state_change(previous: str, current: str, message: str) -> str:
    """Aynı durumun tekrarında sus; değiştiğinde bir kez bas."""
    if current != previous:
        print(message, flush=True)
    return current


async def _main(
    connect_once: Any = _run_once,
    sleeper: Any = None,
) -> int:
    config = BridgeConfig()
    print(f"[bridge] Çelebi köprüsü — servis='{config.service}', rol='{config.role}', "
          f"hedef={config.host}:{config.port}", flush=True)
    print(f"[bridge] protokol={PROTOCOL}, yetenek={CHAT_CAPABILITY}, "
          f"tls={'PINLİ' if config.tls_fingerprint else 'TOFU(pinsiz)'}, "
          f"yeniden_bağlanma={config.reconnect_secs:g}s..{config.reconnect_max_secs:g}s",
          flush=True)
    # Motoru (ve benzerlik matcher'ını) önceden kur: ilk istek hızlı olsun.
    engine = get_default_engine()
    print("[bridge] motor hazır", flush=True)
    return await run_forever(config, engine, connect_once=connect_once, sleeper=sleeper)


def main() -> int:
    try:
        return asyncio.run(_main())
    except KeyboardInterrupt:
        print("\n[bridge] durduruldu.", flush=True)
        return 0


if __name__ == "__main__":
    sys.exit(main())
