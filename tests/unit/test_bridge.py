"""Backend ``chat.reply`` rol sözleşmesi + hab/2 köprü wire regresyon testleri."""

import asyncio
import hashlib
import io
import json
import os
import time
import unittest
from contextlib import redirect_stdout
from unittest import mock

from src import bridge
from src.bridge_contract import resolve_session
from src.engine import Engine

#: Gerçek bir self-signed sertifika (openssl, EC P-256). Parmak izi testte
#: sabit: matematik gerçek bir X.509 gövdesi üzerinde doğrulanır, uydurma bir
#: base64 üzerinde değil.
#:     openssl req -x509 -newkey ec -pkeyopt ec_paramgen_curve:prime256v1 ...
#:     openssl x509 -in cert.pem -outform DER | sha256sum
CERT_PEM = """-----BEGIN CERTIFICATE-----
MIIBfDCCASOgAwIBAgIUTFL6mXX7RANF/ifo1dfMTZ/bfy0wCgYIKoZIzj0EAwIw
FDESMBAGA1UEAwwJbG9jYWxob3N0MB4XDTI2MDkxNzA1MzA1OFoXDTM2MDkxNDA1
MzA1OFowFDESMBAGA1UEAwwJbG9jYWxob3N0MFkwEwYHKoZIzj0CAQYIKoZIzj0D
AQcDQgAEYE2oRVK5XtfcL9AxKi8TFVgWbszWqG2x2W1MGN58nm+/gk9f9xIB2zsB
Et4NPMxNDldeweLT3FB1+m7sml3PB6NTMFEwHQYDVR0OBBYEFJGmsXzrOhrFrnpk
iHBOgHbYm7l0MB8GA1UdIwQYMBaAFJGmsXzrOhrFrnpkiHBOgHbYm7l0MA8GA1Ud
EwEB/wQFMAMBAf8wCgYIKoZIzj0EAwIDRwAwRAIgSPvQ0AIKlWcDCvSubgRfn0Zo
9JZGXKGsD5ms2ieHmwwCIHN3dRl3EH16APGviHy6jfT3jUqFBR5oEeorWNJ7bWMb
-----END CERTIFICATE-----
"""
CERT_FINGERPRINT = "40d2b5d99fb8ed0720d1948796f41c9c778b4aa11dff06815fd77985bf4b0f61"


class _StubEngine:
    """Motor yerine geçen ikiz: thread'e alınan çağrı sözleşmesini korur."""

    def __init__(self, text: str = "cevap", delay: float = 0.0) -> None:
        self.text = text
        self.delay = delay

    def handle(self, request: dict) -> dict:
        if self.delay:
            time.sleep(self.delay)
        return {"text": self.text}


class _BoomEngine:
    def handle(self, request: dict) -> dict:
        raise ValueError("motor patladı")


class _FakeQuic:
    """`send_stream_data`/`get_next_available_stream_id` yeten kadar QUIC."""

    def __init__(self) -> None:
        self.sent: list[tuple[int, bytes, bool]] = []
        self._next_sid = 0

    def get_next_available_stream_id(self) -> int:
        sid = self._next_sid
        self._next_sid += 4
        return sid

    def send_stream_data(self, sid: int, data: bytes, end_stream: bool = False) -> None:
        self.sent.append((sid, bytes(data), end_stream))


class _Harness(bridge.BridgeProtocol):
    """`QuicConnectionProtocol.__init__`'i atlayan test ikizi.

    Gerçek `_serve_request`/`register` gövdeleri koşar — çerçeve çözme, motor
    çağrısı ve cevap yazma dâhil; yalnızca soket ve `transmit` taklit edilir.
    """

    def __init__(self, config: bridge.BridgeConfig, engine: object) -> None:
        self._config = config
        self._engine = engine
        self._streams: dict[int, bridge._FrameStream] = {}
        self._control_sid: int | None = None
        self._ping_uid = 0
        self._quic = _FakeQuic()

    def transmit(self) -> None:  # soket yok
        pass


def _unwrap(frame: bytes) -> dict:
    return json.loads(frame[4:])


def _config(**env: str) -> bridge.BridgeConfig:
    """Ortamdan bağımsız yapılandırma: testler operatörün env'ini okumaz."""
    base = {
        "AI_BRIDGE_HOST": "127.0.0.1",
        "AI_BACKEND_URL": "http://127.0.0.1:8080",
        "AI_TLS_FINGERPRINT": "",
        "AI_RECONNECT_SECS": "3",
        "AI_RECONNECT_MAX_SECS": "120",
    }
    base.update(env)
    with mock.patch.dict(os.environ, base):
        return bridge.BridgeConfig()


class _FakeHttp:
    def __init__(self, payload: dict) -> None:
        self._payload = payload

    def __enter__(self) -> "_FakeHttp":
        return self

    def __exit__(self, *exc: object) -> bool:
        return False

    def read(self) -> bytes:
        return json.dumps(self._payload).encode()


class BridgeRoleContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = Engine()

    def test_backend_asker_role_is_accepted_for_every_school_role(self) -> None:
        for role in ("parent", "student", "teacher", "manager", "admin"):
            with self.subTest(role=role):
                self.assertEqual(
                    resolve_session({"asker_role": role}, "ogrenci"),
                    (role, True),
                )

    def test_asker_role_wins_over_legacy_role_fields(self) -> None:
        role, authenticated = resolve_session(
            {
                "asker_role": "admin",
                "role": "teacher",
                "session": {"role": "student", "authenticated": False},
            },
            "ogrenci",
        )
        self.assertEqual(role, "admin")
        self.assertTrue(authenticated)

    def test_legacy_session_role_remains_supported(self) -> None:
        self.assertEqual(
            resolve_session(
                {"session": {"role": "teacher", "authenticated": True}},
                "ogrenci",
            ),
            ("teacher", True),
        )

    def test_missing_role_uses_configured_legacy_fallback(self) -> None:
        self.assertEqual(resolve_session({}, "manager"), ("manager", True))

    def test_backend_role_changes_the_rendered_answer_scope(self) -> None:
        question = "sınav nasıl oluşturulur?"
        student_role, student_auth = resolve_session(
            {"asker_role": "student"}, "ogrenci"
        )
        admin_role, admin_auth = resolve_session({"asker_role": "admin"}, "ogrenci")
        student = self.engine.handle(
            {
                "query": question,
                "session": {"role": student_role, "authenticated": student_auth},
            }
        )
        admin = self.engine.handle(
            {
                "query": question,
                "session": {"role": admin_role, "authenticated": admin_auth},
            }
        )

        self.assertEqual(student["auth_action"], "role_insufficient")
        self.assertEqual(student["required_role"], "ogretmen")  # sözleşme metadata'sı
        self.assertIsNone(student["navigation"])                # no-leak: rota sızmaz
        self.assertIsNone(admin["auth_action"])
        self.assertIsNotNone(admin["navigation"])
        self.assertTrue(admin["navigation"]["available"])


class BridgeWireTests(unittest.TestCase):
    """hab/2 wire sözleşmesi: sürüm dizesi, Hello gövdesi, okul yankısı."""

    def test_protocol_marker_is_hab2(self) -> None:
        # Backend ALPN'i ve hello.protocol'u bu dizeyle karşılaştırır
        # (constant.rs AI_PROTOCOL); geride kalan bir sürüm kaydı reddettirir.
        self.assertEqual(bridge.PROTOCOL, "hab/2")

    def test_register_writes_a_hab2_hello_on_the_wire(self) -> None:
        harness = _Harness(_config(), _StubEngine())
        greeting = {"type": "welcome", "worker_id": "w1", "protocol": "hab/2"}

        async def drive() -> None:
            task = asyncio.ensure_future(harness.register())
            await asyncio.sleep(0)  # kontrol akışı açılsın
            stream = harness._streams[harness._control_sid]
            stream.feed(bridge._encode_frame(greeting), end=False)
            await task

        asyncio.run(drive())

        sid, frame, end = harness._quic.sent[0]
        hello = _unwrap(frame)
        self.assertEqual(hello["protocol"], "hab/2")
        self.assertEqual(hello["service"], "celebi")
        self.assertEqual(hello["capabilities"], ["chat.reply"])
        # Kontrol akışı yaşam boyu açık kalmalı: kapanması kayıttan düşmedir.
        self.assertFalse(end)
        self.assertEqual(sid, harness._control_sid)

    def test_welcome_echoing_another_protocol_is_rejected(self) -> None:
        harness = _Harness(_config(), _StubEngine())
        greeting = {"type": "welcome", "worker_id": "w1", "protocol": "hab/1"}

        async def drive() -> None:
            task = asyncio.ensure_future(harness.register())
            await asyncio.sleep(0)
            harness._streams[harness._control_sid].feed(
                bridge._encode_frame(greeting), end=False
            )
            await task

        with self.assertRaises(bridge.HandshakeRejected) as ctx:
            asyncio.run(drive())
        self.assertTrue(ctx.exception.permanent)

    def _serve(self, engine: object, request: dict) -> dict:
        harness = _Harness(_config(), engine)
        stream = bridge._FrameStream()
        stream.feed(bridge._encode_frame(request), end=True)
        asyncio.run(harness._serve_request(1, stream))
        sid, frame, end = harness._quic.sent[-1]
        self.assertEqual(sid, 1)
        self.assertTrue(end)  # tek istek -> tek cevap -> FIN
        return _unwrap(frame)

    def test_ok_response_echoes_the_request_school(self) -> None:
        response = self._serve(
            _StubEngine("sınav menüsü"),
            {"id": "r1", "school": "ataturk-ilkokulu", "capability": "chat.reply",
             "deadline_ms": 5000, "payload": {"message": "sınav"}},
        )
        self.assertEqual(response["status"], "ok")
        self.assertEqual(response["id"], "r1")
        self.assertEqual(response["school"], "ataturk-ilkokulu")
        self.assertEqual(response["payload"]["text"], "sınav menüsü")

    def test_every_error_branch_echoes_the_request_school(self) -> None:
        # Okulu düşüren bir dal, reddi YANLIŞ okula yazar: backend çerçeveyi
        # `malformed` sayar ve mesaj error_code=protocol ile düşer.
        cases = {
            "unsupported_capability": (
                _StubEngine(),
                {"capability": "rag.index", "payload": {"message": "x"}},
            ),
            "timed_out": (
                _StubEngine(delay=0.05),
                {"capability": "chat.reply", "deadline_ms": 1, "payload": {"message": "x"}},
            ),
            "internal": (
                _BoomEngine(),
                {"capability": "chat.reply", "deadline_ms": 5000, "payload": {"message": "x"}},
            ),
        }
        for expected_code, (engine, extra) in cases.items():
            with self.subTest(code=expected_code):
                response = self._serve(
                    engine,
                    {"id": "r2", "school": "cumhuriyet-lisesi", "capability": "chat.reply",
                     "deadline_ms": 5000, "payload": {"message": "x"}, **extra},
                )
                self.assertEqual(response["status"], "err")
                self.assertEqual(response["code"], expected_code)
                self.assertEqual(response["school"], "cumhuriyet-lisesi")

    def test_bad_payload_is_a_refusal_not_a_traceback(self) -> None:
        response = self._serve(
            _StubEngine(),
            {"id": "r3", "school": "okul", "capability": "chat.reply",
             "deadline_ms": 5000, "payload": {"message": 42}},
        )
        self.assertEqual(response["status"], "err")
        self.assertEqual(response["code"], "bad_request")
        self.assertEqual(response["school"], "okul")


class PermanentRejectBackoffTests(unittest.TestCase):
    """Kalıcı red: çıkmak yok, üstel geri çekilme + durum değişiminde tek log."""

    def _loop(self, script: list[str], iterations: int) -> tuple[list[float], list[int], str]:
        """`script` her turda ne olacağını söyler: 'ok' | 'reject' | 'down'."""
        config = _config()
        self.config = config
        delays: list[float] = []
        attempts = [0]

        async def connect_once(cfg: bridge.BridgeConfig, engine: object) -> None:
            attempts[0] += 1
            step = script[min(attempts[0] - 1, len(script) - 1)]
            if step == "ok":
                return
            if step == "down":
                raise ConnectionError("backend yok")
            raise bridge.HandshakeRejected("unauthorized", "token uyuşmuyor")

        async def sleeper(delay: float) -> None:
            delays.append(delay)
            if len(delays) >= iterations:
                raise KeyboardInterrupt  # döngüyü testte kıran tek şey

        buf = io.StringIO()
        with redirect_stdout(buf):
            with self.assertRaises(KeyboardInterrupt):
                asyncio.run(
                    bridge.run_forever(config, _StubEngine(), connect_once, sleeper)
                )
        return delays, attempts, buf.getvalue()

    def test_permanent_reject_backs_off_instead_of_exiting(self) -> None:
        delays, attempts, out = self._loop(["reject"], iterations=8)

        # Çıkmadı: sekiz kez denedi ve döngü hâlâ ayakta.
        self.assertEqual(attempts[0], 8)
        # Kalıcı red doğrudan TAVANA gider (zeka ile aynı): yapılandırma
        # düzelmeden geçmeyeceği için 3 saniyede ısrar etmenin anlamı yok.
        self.assertGreaterEqual(delays[0], 120)
        self.assertTrue(all(d >= 120 for d in delays))
        # Tavan aşılmıyor: jitter her turda yeniden eklenir, birikmez.
        self.assertLessEqual(max(delays), self.config.reconnect_max_secs + 5.0)
        self.assertIn("yine de çıkmıyoruz", out)

    def test_permanent_reject_is_logged_once_per_state_change(self) -> None:
        _, _, out = self._loop(["reject", "reject", "ok", "reject", "reject"], iterations=5)

        # Durum 'rejected' -> 'ok' -> 'rejected' olarak İKİ kez değişir. Sekiz
        # turda sekiz satır basan bir log, arızayı arayan operatörün günlüğünü
        # kullanılamaz hale getirir.
        self.assertEqual(out.count("kaydı reddetti"), 2)
        self.assertEqual(out.count("yine de çıkmıyoruz"), 2)

    def test_backoff_resets_after_a_healthy_session(self) -> None:
        delays, _, _ = self._loop(["reject", "reject", "ok", "reject", "reject"], iterations=4)

        self.assertGreaterEqual(delays[0], 3)
        self.assertGreaterEqual(delays[1], 6)
        # 'ok' turundan sonra taban yeniden 3'e döner: 6 ve 12'de takılı kalmaz.
        self.assertGreaterEqual(delays[2], 3)
        self.assertLessEqual(delays[2], 8.0)

    def test_transient_failure_also_backs_off_without_exiting(self) -> None:
        delays, attempts, out = self._loop(["down"], iterations=4)
        self.assertEqual(attempts[0], 4)
        self.assertGreaterEqual(delays[3], 24)
        self.assertIn("backend'e ulaşılamadı", out)


class CertificatePinTests(unittest.TestCase):
    """`GET /ai/certificate` denetimleri: bildirilen iz + pinlenen iz."""

    def _fetch(self, payload: dict, config: bridge.BridgeConfig) -> str:
        with mock.patch.object(bridge.urllib.request, "urlopen", return_value=_FakeHttp(payload)):
            return bridge._fetch_certificate(config)

    def test_der_fingerprint_matches_openssl(self) -> None:
        der = bridge._leaf_der_from_pem(CERT_PEM)
        self.assertEqual(hashlib.sha256(der).hexdigest(), CERT_FINGERPRINT)

    def test_mismatched_reported_fingerprint_refuses_to_connect(self) -> None:
        payload = {"certificate_pem": CERT_PEM, "fingerprint_sha256": "ab" * 32}
        with self.assertRaises(RuntimeError) as ctx:
            self._fetch(payload, _config())
        self.assertIn("tutarsız", str(ctx.exception))

    def test_reported_fingerprint_agrees_so_fetch_succeeds(self) -> None:
        payload = {"certificate_pem": CERT_PEM, "fingerprint_sha256": CERT_FINGERPRINT}
        self.assertEqual(self._fetch(payload, _config()), CERT_PEM)

    def test_pinned_fingerprint_mismatch_refuses_to_connect(self) -> None:
        payload = {"certificate_pem": CERT_PEM, "fingerprint_sha256": CERT_FINGERPRINT}
        config = _config(AI_TLS_FINGERPRINT="cd" * 32)
        with self.assertRaises(RuntimeError) as ctx:
            self._fetch(payload, config)
        self.assertIn("PINLENEN", str(ctx.exception))

    def test_pinned_fingerprint_accepts_colon_separated_and_uppercase_hex(self) -> None:
        spaced = ":".join(
            CERT_FINGERPRINT[i:i + 2] for i in range(0, len(CERT_FINGERPRINT), 2)
        ).upper()
        payload = {"certificate_pem": CERT_PEM, "fingerprint_sha256": CERT_FINGERPRINT}
        config = _config(AI_TLS_FINGERPRINT=spaced)
        self.assertEqual(config.tls_fingerprint, CERT_FINGERPRINT)
        self.assertEqual(self._fetch(payload, config), CERT_PEM)

    def test_unset_pin_warns_that_it_is_tofu(self) -> None:
        payload = {"certificate_pem": CERT_PEM, "fingerprint_sha256": CERT_FINGERPRINT}
        buf = io.StringIO()
        with redirect_stdout(buf):
            self._fetch(payload, _config())
        self.assertIn("TOFU", buf.getvalue())

    def test_malformed_pin_is_a_config_error_not_a_silent_tofu(self) -> None:
        # Yarım yapıştırılmış bir parmak izi TOFU'ya düşerse operatör pinlediğini
        # SANIR: sessizce kabul etmek yerine yapılandırma hatası olmalı.
        with self.assertRaises(ValueError):
            _config(AI_TLS_FINGERPRINT="40d2b5d9")


if __name__ == "__main__":
    unittest.main()
