"""Backend servis + front/back sözleşmesi.

Motoru net bir istek/yanıt sözleşmesiyle sarar. Frontend (terminal, web vb.)
yalnızca bu sözleşme üzerinden konuşur; iç katmanları (kural/benzerlik/karar)
bilmez. Loglama backend'de yapılır (isteğe bağlı log_sink).

İstek (payload):
    {
      "query": str,                       # zorunlu
      "session": {"role": str, "authenticated": bool},  # isteğe bağlı
      "trace_id": str                     # isteğe bağlı (yoksa üretilir)
    }

Yanıt:
    {
      "trace_id": str,
      "response_id": str,
      "text": str,
      "intent": str | None,
      "confidence": float,
      "fallback": bool,
      "auth_action": str | None,          # None | "login_required" | "role_insufficient"
      "required_role": str | None
    }
"""

from __future__ import annotations

import re
from typing import Any, Callable

from . import rules
from . import safety as safety_mod
from .catalog import (
    FALLBACK,
    ROLE_ALIASES,
    ROLE_HIERARCHY,
    capabilities_for,
    get_intent,
    route_for,
    suggestions_for,
)
from .normalize import folded_tokens
from .observability import new_trace_id, process

# Rol beyanını ("ben öğrenciyim") gerçek sorudan ayırmak için yok sayılan doldurma
# kelimeleri. Bunlar dışındaki her kelime rol kelimesi değilse -> beyan sayılmaz.
_ROLE_DECL_FILLER: frozenset[str] = frozenset(
    {"ben", "benim", "bir", "rol", "rolum", "rolumu", "olarak", "ya", "de", "da", "peki"}
)

# İlk iki aday bu farktan yakınsa sistem "emin değil" -> netleştirme adayları sun.
# (Yalnızca benzerlik kararlarında; kural kararları yüksek-kesinlik olduğundan muaf.)
CLARIFY_MARGIN: float = 0.08

# Benzerlik güveni bunun ALTINDAYSA tam cevap VERİLMEZ: "anlayamadım, bunu mu
# demek istedin?" + adaylar döner. Eşik (0.18) ile bu değer arası "belirsiz bölge"dir
# — yanlış-ama-özgüvenli cevap, dürüst soru sormaktan kötüdür.
ASK_CONFIDENCE: float = 0.30

# Belirsiz bölgede kullanıcıya dönen metin (response_id: clarification_prompt).
CLARIFICATION_PROMPT_TEXT: str = (
    "Bunu tam anlayamadım, kusura bakma 🙏 Aşağıdakilerden birini mi sormak "
    "istedin? Değilse, soruyu biraz daha açık yazarsan yardımcı olayım."
)
from .similarity import SimilarityMatcher, get_default_matcher

# İsteğe bağlı log alıcısı: bir trace sözlüğü alır (dosyaya/akışa yazmak çağıranın işi).
LogSink = Callable[[dict[str, Any]], None]


class RequestError(ValueError):
    """Geçersiz istek payload'ı."""


# Gerçek backend'in (REST API) İngilizce rol adları -> iç rol adları.
# Front/back arkadaşların oturumu 'student/teacher/manager/admin' olarak çözer;
# asistan iki adlandırmayı da kabul eder.
_ROLE_NAME_ALIASES: dict[str, str] = {
    "parent": "veli",
    "student": "ogrenci",
    "teacher": "ogretmen",
    "manager": "yonetici",
    "guest": "ziyaretci",
    "visitor": "ziyaretci",
}


def _parse_session(payload: dict[str, Any]) -> tuple[str, bool]:
    session = payload.get("session") or {}
    role = session.get("role", "ziyaretci")
    if isinstance(role, str):
        role = _ROLE_NAME_ALIASES.get(role.lower(), role)
    authenticated = bool(session.get("authenticated", role != "ziyaretci"))
    if role not in ROLE_HIERARCHY:
        raise RequestError(f"Bilinmeyen rol: {role!r}")
    if role == "ziyaretci" and authenticated:
        raise RequestError("Ziyaretçi 'authenticated' olamaz.")
    return role, authenticated


# Çoklu-istek ayracı: 've', 'ayrıca' bağlaçları + virgül/noktalı virgül.
_MULTI_SPLIT_RE: re.Pattern[str] = re.compile(r"\s+(?:ve|ayrıca)\s+|[;,]", re.IGNORECASE)


def _multi_intent_segments(query: str) -> list[tuple[str, str]] | None:
    """Sorgu birden çok BAĞIMSIZ isteğe bölünüyor mu? -> [(parça, intent), ...].

    Muhafazakâr tasarım: yalnızca KURAL katmanının (yüksek kesinlik) tanıdığı
    parçalar sayılır; en az 2 FARKLI intent gerekir, en çok 3 parça yanıtlanır.
    Böylece 'roller ve yetkiler nedir' gibi doğal 've'ler bölünmez (parçalar
    kurala çarpmaz), 'sınav oluştur ve yoklama al' ise iki cevap alır.
    """

    raw_segments = [s.strip() for s in _MULTI_SPLIT_RE.split(query) if s.strip()]
    if len(raw_segments) < 2:
        return None
    hits: list[tuple[str, str]] = []
    seen: set[str] = set()
    for segment in raw_segments:
        match = rules.match(segment)
        if match is not None and match.intent not in seen:
            seen.add(match.intent)
            hits.append((segment, match.intent))
        if len(hits) == 3:
            break
    return hits if len(hits) >= 2 else None


def _declared_role(query: str) -> str | None:
    """Sorgu yalnızca bir rol beyanı mı? ('Öğrenci', 'ben öğretmenim') -> kanonik rol.

    Doldurma kelimeleri (ben, olarak...) yok sayılır; geriye kalan tüm kelimeler rol
    kelimesiyse ve en az bir rol varsa beyan kabul edilir. 'öğrenci kaydet' gibi ek
    içerikli sorgular (kaydet rol/doldurma değil) beyan SAYILMAZ -> normal boru hattı.
    """

    tokens = folded_tokens(query)
    if not tokens or len(tokens) > 4:
        return None
    found: str | None = None
    for tok in tokens:
        role = None
        for stem, canonical in ROLE_ALIASES.items():
            if tok == stem or (len(stem) >= 4 and tok.startswith(stem)):
                role = canonical
                break
        if role is not None:
            found = role
        elif tok not in _ROLE_DECL_FILLER:
            return None  # rol/doldurma olmayan bir kelime -> beyan değil
    return found


def _build_navigation(intent: str | None, auth_action: str | None) -> dict[str, Any] | None:
    """Seçilen intent için yönlendirme hedefi (route) üretir.

    Frontend bunu "Git →" butonu olarak çizer. `available`, kullanıcının rolü
    yeterliyse True'dur (yetersizse buton pasif gösterilir; neden `auth_action`'da).
    """

    if intent is None:
        return None
    route = route_for(intent)
    if route is None:
        return None
    path, label = route
    return {"route": path, "label": label, "available": auth_action is None}


def _build_clarification(trace: dict[str, Any], *, force: bool = False) -> dict[str, Any] | None:
    """Karar belirsizse (ilk iki aday çok yakın) netleştirme adayları üretir.

    `intent` yine en iyi tahmin olarak döner (metrikler değişmez); bu alan yalnızca
    frontend'in "Bunu mu demek istedin?" seçenekleri göstermesi için EK bilgidir.
    `force=True` (düşük-güven bölgesi) margin şartını atlar; adaylar her durumda üretilir.
    """

    dec = trace.get("decision", {})
    if dec.get("fallback") or dec.get("source") != "similarity":
        return None
    sim = trace.get("similarity", {})
    top_k = sim.get("top_k") or []
    margin = sim.get("margin")
    if len(top_k) < 2:
        return None
    if not force and (margin is None or margin >= CLARIFY_MARGIN):
        return None

    candidates = []
    for cand in top_k[:2]:
        info = get_intent(cand["intent"])
        candidates.append({
            "intent": cand["intent"],
            "label": info["description"] if info else cand["intent"],
            "response_id": info["response_id"] if info else None,
            "confidence": cand["score"],
        })
    reason = "low_margin" if (margin is not None and margin < CLARIFY_MARGIN) else "low_confidence"
    return {"reason": reason, "margin": round(margin, 4) if margin is not None else None,
            "candidates": candidates}


def _safety_info(safety: "safety_mod.SafetyDecision") -> dict[str, Any]:
    return {
        "decision": safety.decision,
        "category": safety.category,
        "severity": safety.severity,
        "rule_id": safety.rule_id,
        "requires_review": safety.requires_review,
        "rule_version": safety.rule_version,
    }


def _safety_trace(
    trace_id: str, query: str, role: str, authenticated: bool,
    safety: "safety_mod.SafetyDecision",
) -> dict[str, Any]:
    """Kısa devre (bloklanan) istekler için minimal trace kaydı."""

    return {
        "trace_id": trace_id,
        "query_masked": safety_mod.mask_pii(query)[0],
        "role": role,
        "authenticated": authenticated,
        "short_circuit": "safety",
        "safety": _safety_info(safety),
        "response_id": "safety_" + safety.category.lower(),
    }


class Engine:
    """Süreç ömrü boyunca yeniden kullanılan backend motoru."""

    def __init__(
        self,
        matcher: SimilarityMatcher | None = None,
        log_sink: LogSink | None = None,
        rate_limiter: "safety_mod.RateLimiter | None" = None,
    ) -> None:
        self._matcher = matcher or get_default_matcher()
        self._log_sink = log_sink
        self._rate_limiter = rate_limiter

    def handle(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Bir istek payload'ını işleyip yanıt sözleşmesi döndürür.

        Akış: içerik-güvenliği giriş kapısı -> (gerekirse kısa devre) -> boru hattı
        -> çıktı güvenliği kontrolü.
        """

        query = payload.get("query")
        # Eksik/yanlış-tipli 'query' -> sözleşme ihlali (çağıran hatası): istisna.
        if not isinstance(query, str):
            raise RequestError("'query' bir metin olmalı.")

        role, authenticated = _parse_session(payload)
        trace_id = payload.get("trace_id") or new_trace_id()
        user_id = (payload.get("session") or {}).get("user_id")
        suggestions = suggestions_for(role)  # role bazlı başlangıç soru önerileri

        # Boş / yalnızca-boşluk girdi kullanıcı kaynaklıdır -> istisna değil, nazik
        # fallback. (AI katmanı kullanıcı girdisine hata fırlatmaz.)
        if not query.strip():
            empty = {
                "trace_id": trace_id,
                "response_id": FALLBACK["response_id"],
                "text": FALLBACK["response_template"],
                "intent": None,
                "confidence": 0.0,
                "fallback": True,
                "auth_action": None,
                "required_role": None,
                "navigation": None,
                "clarification": None,
                "answers": None,
                "suggestions": suggestions,
                "safety": _safety_info(safety_mod.evaluate_input("")),
            }
            if self._log_sink is not None:
                self._log_sink({
                    "trace_id": trace_id, "query_masked": safety_mod.mask_pii(query)[0], "role": role,
                    "authenticated": authenticated, "short_circuit": "empty_query",
                    "response_id": FALLBACK["response_id"],
                })
            return empty

        # 0) Rate-limit / spam (opsiyonel; user_id gerekir).
        if self._rate_limiter is not None and user_id:
            limited = self._rate_limiter.check(str(user_id), query)
            if limited is not None:
                if self._log_sink is not None:
                    self._log_sink(_safety_trace(trace_id, query, role, authenticated, limited))
                return {
                    "trace_id": trace_id,
                    "response_id": "safety_" + limited.category.lower(),
                    "text": limited.user_message,
                    "intent": None,
                    "confidence": limited.confidence,
                    "fallback": False,
                    "auth_action": None,
                    "required_role": None,
                    "navigation": None,
                    "clarification": None,
                    "answers": None,
                    "suggestions": suggestions,
                    "safety": _safety_info(limited),
                }

        # 1) İçerik-güvenliği giriş kapısı.
        safety = safety_mod.evaluate_input(query, role=role, authenticated=authenticated)
        safety_info = _safety_info(safety)

        if safety.decision in safety_mod.BLOCKING_DECISIONS:
            if self._log_sink is not None:
                self._log_sink(_safety_trace(trace_id, query, role, authenticated, safety))
            return {
                "trace_id": trace_id,
                "response_id": "safety_" + safety.category.lower(),
                "text": safety.user_message,
                "intent": None,
                "confidence": safety.confidence,
                "fallback": False,
                "auth_action": None,
                "required_role": None,
                "navigation": None,
                "clarification": None,
                "answers": None,
                "suggestions": suggestions,
                "safety": safety_info,
            }

        # 1.5) Rol beyanı ("Öğrenci", "ben öğretmenim") -> role özel yetenek özeti.
        # Bot 'rolünü söyle' dediğinde verilen tek kelimelik cevabı anlamlandırır;
        # aksi hâlde 'Öğrenci' yanlışlıkla 'öğrenci kaydet' intent'ine benzerdi.
        declared = _declared_role(query)
        caps = capabilities_for(declared) if declared else None
        if caps:
            if self._log_sink is not None:
                self._log_sink({
                    "trace_id": trace_id, "query_masked": safety_mod.mask_pii(query)[0], "role": role,
                    "authenticated": authenticated, "short_circuit": "role_declaration",
                    "declared_role": declared, "response_id": "role_capabilities_" + declared,
                })
            return {
                "trace_id": trace_id,
                "response_id": "role_capabilities_" + declared,
                "text": caps,
                "intent": None,
                "confidence": 1.0,
                "fallback": False,
                "auth_action": None,
                "required_role": None,
                "navigation": None,
                "clarification": None,
                "answers": None,
                "suggestions": suggestions,
                "safety": safety_info,
            }

        # PII maskeleme: maskelenmiş sorguyu boru hattına ver.
        effective_query = query
        if safety.decision == safety_mod.MASK_AND_ALLOW and safety.masked_message:
            effective_query = safety.masked_message

        # 1.6) Çoklu istek ('X ve Y'): her bağımsız parça ayrı yanıtlanır.
        segments = _multi_intent_segments(effective_query)
        if segments is not None:
            answers: list[dict[str, Any]] = []
            parts: list[str] = []
            for order, (segment, _intent) in enumerate(segments, start=1):
                seg_response, seg_trace = process(
                    segment, role=role, authenticated=authenticated,
                    trace_id=f"{trace_id}.{order}", matcher=self._matcher,
                )
                answers.append({
                    "intent": seg_response.intent,
                    "response_id": seg_response.response_id,
                    "text": seg_response.text,
                    "auth_action": seg_response.auth_action,
                    "navigation": _build_navigation(seg_response.intent, seg_response.auth_action),
                })
                info = get_intent(seg_response.intent) if seg_response.intent else None
                title = (info["description"].rstrip(".") if info else segment)
                parts.append(f"**{order}) {title}**\n{seg_response.text}")

            text = "Birkaç şey sormuşsun, sırayla cevaplayayım:\n\n" + "\n\n".join(parts)
            out = safety_mod.evaluate_output(text)
            if out.decision == safety_mod.MASK_AND_ALLOW and out.masked_message:
                text = out.masked_message
            elif out.decision == safety_mod.BLOCK:
                text = out.user_message

            first = answers[0]
            if self._log_sink is not None:
                self._log_sink({
                    "trace_id": trace_id, "query_masked": safety_mod.mask_pii(query)[0], "role": role,
                    "authenticated": authenticated, "short_circuit": "multi_intent",
                    "intents": [a["intent"] for a in answers],
                    "response_id": first["response_id"],
                    "safety": safety_info,
                })
            return {
                "trace_id": trace_id,
                "response_id": first["response_id"],
                "text": text,
                "intent": first["intent"],
                "confidence": 1.0,  # kural tabanlı parçalar (yüksek kesinlik)
                "fallback": False,
                "auth_action": first["auth_action"],
                "required_role": None,
                "navigation": first["navigation"],
                "clarification": None,
                "answers": answers,
                "suggestions": suggestions,
                "safety": safety_info,
            }

        # 2) Boru hattı.
        response, trace = process(
            effective_query,
            role=role,
            authenticated=authenticated,
            trace_id=trace_id,
            matcher=self._matcher,
        )
        trace["safety"] = safety_info

        # Belirsiz bölge: benzerlik güveni düşükse yanlış-ama-özgüvenli cevap verme;
        # "anlayamadım — bunu mu demek istedin?" + adaylar döndür.
        dec = trace["decision"]
        ask_mode = (
            not response.fallback
            and dec["source"] == "similarity"
            and dec["confidence"] < ASK_CONFIDENCE
        )
        if ask_mode:
            clarification = _build_clarification(trace, force=True)
            trace["ask_clarification"] = True
            text = CLARIFICATION_PROMPT_TEXT
            if safety.decision == safety_mod.ALLOW_WITH_WARNING and safety.user_message:
                text = safety.user_message + "\n" + text
            if self._log_sink is not None:
                self._log_sink(trace)
            return {
                "trace_id": trace["trace_id"],
                "response_id": "clarification_prompt",
                "text": text,
                "intent": None,  # tahmin adaylarda; tam cevap bilerek verilmedi
                "confidence": dec["confidence"],
                "fallback": False,
                "auth_action": None,
                "required_role": None,
                "navigation": None,
                "clarification": clarification,
                "answers": None,
                "suggestions": suggestions,
                "safety": safety_info,
            }

        text = response.text
        # "Neler yapabilirim?" -> oturum rolü belliyse jenerik "rolünü söyle" yerine
        # o role özel yetenek özeti (kullanıcı zaten rolünü biliyor).
        if response.intent == "help_capabilities" and authenticated:
            role_caps = capabilities_for(role)
            if role_caps:
                text = role_caps
        if safety.decision == safety_mod.ALLOW_WITH_WARNING and safety.user_message:
            text = safety.user_message + "\n" + text

        # 3) Çıktı güvenliği kontrolü.
        out = safety_mod.evaluate_output(text)
        trace["output_safety"] = {"decision": out.decision, "category": out.category, "rule_id": out.rule_id}
        if out.decision == safety_mod.MASK_AND_ALLOW and out.masked_message:
            text = out.masked_message
        elif out.decision == safety_mod.BLOCK:
            text = out.user_message

        if self._log_sink is not None:
            self._log_sink(trace)

        return {
            "trace_id": trace["trace_id"],
            "response_id": response.response_id,
            "text": text,
            "intent": response.intent,
            "confidence": trace["decision"]["confidence"],
            "fallback": response.fallback,
            "auth_action": response.auth_action,
            "required_role": trace["decision"]["required_role"],
            "navigation": _build_navigation(response.intent, response.auth_action),
            "clarification": _build_clarification(trace),
            "answers": None,
            "suggestions": suggestions,
            "safety": safety_info,
        }


# Kolaylık: paylaşılan varsayılan motor.
_DEFAULT_ENGINE: Engine | None = None


def get_default_engine() -> Engine:
    global _DEFAULT_ENGINE
    if _DEFAULT_ENGINE is None:
        _DEFAULT_ENGINE = Engine()
    return _DEFAULT_ENGINE


def handle_request(payload: dict[str, Any]) -> dict[str, Any]:
    """Paylaşılan motorla tek atımlık istek işleme."""

    return get_default_engine().handle(payload)
