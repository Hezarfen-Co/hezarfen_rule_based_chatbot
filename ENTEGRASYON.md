# Çelebi Asistanı — Backend Entegrasyon Paketi

Bu belge, **Hezarfen kullanım asistanı "Çelebi"yi** mevcut sisteme (Rust backend +
SolidJS frontend) bağlamak için gereken her şeyi içerir. Asistanın kendisi ayrı bir
konu; burada yalnızca **nasıl çağrılır, ne döndürür, neyi sağlamalısınız** var.

---

## 1. Ne olduğu (30 saniye)

- **Kural + benzerlik tabanlı** bir kullanım asistanı. Üretken (LLM) değil: yalnızca
  **önceden yazılmış, doğrulanmış cevapları** döndürür → halüsinasyon yok, deterministik.
- Girdi: kullanıcı mesajı + oturum bilgisi. Çıktı: **JSON** (cevap metni + niyet +
  yönlendirme hedefi + güvenlik kararı + öneriler).
- **Saf Python, sıfır bağımlılık** (yalnız stdlib). Offline çalışır.
- Kullanıcıyı **işlem yaptırmaz**, yalnızca **anlatır ve doğru sayfaya yönlendirir**.
  Gerçek yetki/erişim kontrolü her zaman sizde kalır.

## 2. Mimari gerçek ⚠️ (önce bunu okuyun)

Backend **Rust**, asistan **Python**. Yani asistanı `import` edemezsiniz —
**ayrı bir HTTP servisi** olarak çalışır, siz ona istek atarsınız:

```
[Frontend] --/api/assistant/chat--> [Rust backend]  (oturumdan role+user_id ekler)
                                          |
                                          +--HTTP--> [Çelebi servisi :8000]  (Python)
```

Frontend doğrudan da çağırabilir; kritik olan: **`role` ve `user_id` istemciden
DEĞİL, doğrulanmış oturumdan gelmeli** (bkz. §5).

## 3. Servisi çalıştırma

**Tek giriş noktası:** `src/engine.py` → `handle_request(payload) -> dict`.
HTTP katmanı bunu sarmaktan ibarettir.

**Geliştirme / hızlı deneme** (stdlib, hazır):
```bash
python -m src.web            # http://127.0.0.1:8000  (POST /api/chat)
```
> `web.py` bir **demo/dev** aracıdır (rolü istemciden alır, TLS yok). Üretimde kullanmayın.

**Üretim (önerilen)** — motoru bir ASGI sunucusuna sarın (örnek, FastAPI):
```python
from fastapi import FastAPI, Request
from src.engine import get_default_engine

app = FastAPI()
engine = get_default_engine()          # süreç ömrü boyunca tek kez kurulur (matcher cache'li)

@app.post("/chat")
async def chat(req: Request):
    body = await req.json()
    # role + user_id'yi İSTEMCİDEN DEĞİL, kendi oturumunuzdan doldurun:
    body["session"] = {"role": current_role(req), "authenticated": True,
                       "user_id": current_user_id(req)}
    return engine.handle(body)         # -> dict (JSON serileştirilebilir)
```
`uvicorn app:app` ile ayağa kalkar. `get_default_engine()` matcher'ı bir kez kurar;
her istekte yeniden yükleme yok.

## 4. Sözleşme — İstek

```json
{
  "query": "sınav nasıl oluşturulur",
  "session": { "role": "teacher", "authenticated": true, "user_id": "u_123" },
  "trace_id": "opsiyonel-izleme-kimliği"
}
```
- `query` (zorunlu, string): kullanıcının ham mesajı.
- `session.role`: aşağıdaki adlardan biri (TR ya da EN kabul edilir, bkz. §5).
- `session.authenticated`: oturum açık mı.
- `session.user_id`: (opsiyonel) rate-limit + telemetri için.
- `trace_id`: (opsiyonel) vermezseniz üretilir; loglarınızla eşleştirmek için verin.

Boş/eksik `query` → istisna DEĞİL, nazik fallback döner (kullanıcı girdisine hata atmaz).
Yalnızca `query` alanı hiç yoksa/string değilse `RequestError` (çağıran hatası).

## 5. Sözleşme — Yanıt

```json
{
  "trace_id": "req-9f3c1a20b7e4",
  "response_id": "exam_create_instructions",
  "text": "Ön koşul: ... 1) /exams → Sınav oluştur ...",
  "intent": "exam_create",
  "confidence": 1.0,
  "fallback": false,
  "auth_action": null,
  "required_role": null,
  "navigation": { "route": "/exams", "label": "Sınavlar", "available": true },
  "clarification": null,
  "answers": null,
  "suggestions": ["Sınav nasıl oluşturulur?", "Yoklama nasıl alınır?"],
  "safety": { "decision": "ALLOW", "category": "CLEAN", "severity": 0,
              "rule_id": "SAFE-OK-000", "requires_review": false, "rule_version": "1.0.0" }
}
```

| Alan | Anlamı / frontend ne yapar |
|---|---|
| `text` | Gösterilecek cevap. **Markdown** içerir (`**kalın**`, `` `kod` ``) — render edin. |
| `response_id` | Kararlı kimlik. 👍/👎 geri bildirimini buna bağlayın (metin değişse de sabit). |
| `intent` | Sınıflandırma etiketi (analitik). Cevap verilmediyse `null`. |
| `confidence` | 0–1. Bilgi amaçlı; karar zaten verilmiş. |
| `fallback` | `true` → "anlamadım" cevabı. |
| `auth_action` | `null` / `"login_required"` / `"role_insufficient"`. Doluysa uyarı gösterin. |
| `required_role` | auth_action doluysa gereken minimum rol. |
| `navigation` | `{route,label,available}` — **"Git →" butonu**. Yoksa `null`. `available:false` → butonu pasif göster. `route` sizin router yollarınızla birebir aynıdır. |
| `clarification` | `{reason,margin,candidates[]}` — "Bunu mu demek istedin?" çipleri. Yoksa `null`. |
| `answers` | Çoklu-istek ("X ve Y") → her parçanın ayrı cevabı (liste). Tekli istekte `null`. |
| `suggestions` | Role göre başlangıç soru önerileri (liste). Selam/yardım/fallback anlarında çip olarak gösterin. |
| `safety` | İçerik güvenliği kararı. `category != "CLEAN"` → bloklanmış/işaretlenmiş istek. |

**Roller** (iç ad ← kabul edilen adlar):
| İç ad | Kabul edilen | Arayüz etiketi |
|---|---|---|
| `ziyaretci` | guest, visitor | Ziyaretçi |
| `veli` | parent | Veli |
| `ogrenci` | student | Öğrenci |
| `ogretmen` | teacher | Öğretmen |
| `yonetici` | manager | Yönetici |
| `admin` | admin | ADMIN |

## 6. Frontend (Vite proxy)

`vite.config.ts` proxy'sine asistan için bir satır ekleyin (mevcut `/api` kuralına
dokunmadan):
```ts
proxy: {
  "/api": { target, changeOrigin: true, ws: true, rewrite: p => p.replace(/^\/api/, "") },
  "/assistant": { target: "http://127.0.0.1:8000", changeOrigin: true },
}
```
Sohbet balonu `/assistant/chat`'e `POST` atar; dönen JSON'daki `text` (markdown),
`navigation`, `clarification`, `suggestions` alanlarını çizer.

## 7. İzleme / loglama (monitoring)

Motor her istekte yapılandırılmış bir **telemetri kaydı** üretir; nereye yazılacağı
**sizin** kararınız. `Engine(log_sink=callable)` ile bir geri-çağırım verin:
```python
engine = Engine(log_sink=lambda trace: your_db.insert("assistant_log", trace))
```
Kayıt (KVKK: sorgu **maskeli**, ham sorgu asla saklanmaz):
```json
{ "trace_id":"...", "query_masked":"numaram 053***4567 ...", "role":"ogrenci",
  "intent":"...", "response_id":"...", "confidence":0.9, "fallback":false,
  "safety":{...}, "latency_ms":{...}, "alarms":[] }
```
İyileştirme için değerli satırlar: `fallback=true`, `confidence` düşük, `safety.alarms`
dolu, ve frontend'den gelen 👎 geri bildirimi. Bunları bize iletirseniz benchmark'a
ekleyip asistanı iyileştiririz.

**Geri bildirim** (opsiyonel): `web.py` örnek bir `POST /api/feedback` uç noktası içerir
(`{trace_id, response_id, intent, rating}` → JSONL). Kendi sisteminizde bunu kendi
DB'nize yazın.

## 8. Rate-limit (opsiyonel)

`Engine(rate_limiter=RateLimiter())` verirseniz, `session.user_id` bazında sıklık/tekrar
sınırı uygulanır → `response_id="safety_spam_*"`. Dağıtık kurulumda kendi limiter'ınız
daha uygun olabilir (bu bellek-içi ve tek süreçtir).

## 9. Davranış referansı (neye güvenebilirsiniz)

- `tests/e2e/test_behavior_matrix.py` — 53 intent × rol gating × güvenlik davranış
  tablosu. "Şu girdiye şu `response_id`" sözleşmesi burada sabit; entegrasyonda buna
  güvenebilirsiniz. Kırılırsa davranış değişmiş demektir.
- `KONUSMALAR.md` — 212 gerçek konuşma transkripti (bot cevaplarıyla). Nasıl konuştuğunu
  görmek için okuyun.
- `python -m tests.e2e.test_conversation --markdown` ile bu raporu yeniden üretebilirsiniz.

## 10. Henüz olmayan / bilinen sınırlar

- **Çok-turlu bağlam yok**: her mesaj bağımsız değerlendirilir ("peki ya silmek?" gibi
  devam soruları önceki mesaja bağlanmaz). İleride eklenebilir; şimdilik her soruyu
  tam yazmak gerekir.
- **Yalnız Türkçe** (İngilizce sorular fallback'e düşer).
- `messages` / pomodoro / etüt-kulüp / veli intent'leri **repo incelemesinden** yazıldı;
  ilgili arayüzler son hâlini alınca metinleri birlikte teyit etmeliyiz.
- `authorization.py` (IDOR/BOLA parametre denetimi) yazılı ama boru hattına bağlı DEĞİL —
  asistan veri çekmediğinden düşük risk; asıl yetki her zaman sizde.
