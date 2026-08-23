"""Geliştirici test arayüzü — Hezarfen kullanım asistanı (stdlib-only web sunucusu).

Backend'i (`engine.Engine`) HTTP üzerinden sarar ve tek sayfalık bir sohbet
arayüzü sunar. Sıfır harici bağımlılık: yalnızca `http.server`.

Çalıştırma:
    python -m src.web                # http://127.0.0.1:8000
    python -m src.web --port 9000
    python -m src.web --rate-limit   # RateLimiter'ı da devreye al

Uç noktalar:
    GET  /            -> sohbet arayüzü (HTML)
    POST /api/chat    -> {query, role, authenticated, user_id} -> engine yanıtı (JSON)
"""

from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .catalog import ROLE_HIERARCHY
from .engine import Engine, RequestError
from .safety import RateLimiter

# Geri-bildirim sinyali (item 5): 👍/👎 oyları buraya JSONL olarak yazılır.
# Not: kalıcı depolama/analiz backend arkadaşların işi; bu yalnız sinyali yakalar
# ki "kendini iyileştiren döngü" (yanlış sınıflandırmayı topla -> benchmark'a besle)
# nasıl çalışır gösterilebilsin.
FEEDBACK_LOG = "feedback.jsonl"


INDEX_HTML = """<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Çelebi · Hezarfen Asistanı — Dev</title>
<style>
  :root {
    --bg:#0f1115; --panel:#171a21; --panel2:#1f232c; --line:#2a2f3a;
    --text:#e7e9ee; --muted:#9aa3b2; --accent:#5b8cff; --user:#264a8f;
    --ok:#2f9e5a; --warn:#d0921f; --bad:#d0453b; --info:#7a5cff;
  }
  * { box-sizing:border-box; }
  body { margin:0; font:15px/1.5 system-ui,Segoe UI,Roboto,sans-serif;
    background:var(--bg); color:var(--text); height:100vh; display:flex; flex-direction:column; }
  header { padding:12px 16px; background:var(--panel); border-bottom:1px solid var(--line);
    display:flex; gap:12px; align-items:center; flex-wrap:wrap; }
  header h1 { font-size:15px; margin:0; font-weight:600; }
  header .grow { flex:1; }
  label { color:var(--muted); font-size:13px; }
  select, input[type=text] { background:var(--panel2); color:var(--text);
    border:1px solid var(--line); border-radius:8px; padding:8px 10px; font:inherit; }
  select:focus, input:focus { outline:1px solid var(--accent); }
  .chk { display:flex; align-items:center; gap:6px; color:var(--muted); font-size:13px; }
  #log { flex:1; overflow-y:auto; padding:20px; display:flex; flex-direction:column; gap:14px; }
  .msg { max-width:min(760px,92%); }
  .msg.user { align-self:flex-end; }
  .bubble { padding:10px 14px; border-radius:12px; white-space:pre-wrap; word-wrap:break-word; }
  .user .bubble { background:var(--user); border-bottom-right-radius:4px; }
  .bot .bubble { background:var(--panel2); border:1px solid var(--line); border-bottom-left-radius:4px; }
  .meta { margin-top:6px; display:flex; gap:6px; flex-wrap:wrap; font-size:11px; }
  .tag { padding:2px 8px; border-radius:999px; background:var(--panel);
    border:1px solid var(--line); color:var(--muted); }
  .tag b { color:var(--text); font-weight:600; }
  .tag.intent { border-color:var(--accent); }
  .tag.fallback { border-color:var(--warn); color:var(--warn); }
  .tag.safety { border-color:var(--info); color:#b9a9ff; }
  .tag.auth { border-color:var(--bad); color:#ff9a91; }
  .nav-cta { margin-top:11px; display:inline-flex; align-items:center; gap:9px;
    background:var(--accent); color:#fff; border:0; border-radius:10px; padding:9px 14px;
    font:inherit; font-weight:600; font-size:13.5px; cursor:pointer; }
  .nav-cta .route { font-family:ui-monospace,monospace; font-size:11px; opacity:.8; }
  .nav-cta .arr { font-size:15px; }
  .nav-cta.off { background:var(--panel2); color:var(--muted);
    border:1px solid var(--line); cursor:not-allowed; }
  .sys { align-self:center; font-size:12px; color:var(--muted); font-style:italic;
    padding:2px 0; }
  .clarify { margin-top:10px; padding:10px 12px; background:var(--panel);
    border:1px dashed var(--accent); border-radius:10px; }
  .clarify-q { font-size:13px; color:var(--muted); margin-bottom:8px; }
  .chip { background:var(--panel2); color:var(--text); border:1px solid var(--accent);
    border-radius:999px; padding:6px 12px; margin:0 6px 6px 0; font-size:13px;
    font-weight:500; cursor:pointer; }
  .chip:hover { background:var(--accent); }
  .fb { margin-top:8px; display:flex; align-items:center; gap:8px; }
  .fb-label { font-size:12px; color:var(--muted); }
  .fb-btn { background:transparent; padding:2px 8px; font-size:15px; border-radius:6px; }
  .fb-btn:hover { background:var(--panel2); }
  .fb-done { font-size:12px; color:var(--ok); }
  .suggest { margin-top:12px; padding-top:10px; border-top:1px dashed var(--line); }
  .suggest-q { font-size:12px; color:var(--muted); margin-bottom:8px; }
  .bubble code { background:var(--panel); padding:1px 5px; border-radius:5px;
    font-size:13px; }
  .bubble strong { color:#fff; font-weight:700; }
  footer { padding:12px 16px; background:var(--panel); border-top:1px solid var(--line);
    display:flex; gap:10px; }
  #q { flex:1; }
  button { background:var(--accent); color:#fff; border:0; border-radius:8px;
    padding:9px 18px; font:inherit; font-weight:600; cursor:pointer; }
  button:disabled { opacity:.5; cursor:default; }
  .hint { color:var(--muted); font-size:12px; align-self:center; }
</style>
</head>
<body>
<header>
  <h1>🪽 Çelebi · Hezarfen Asistanı</h1>
  <span class="tag">dev</span>
  <div class="grow"></div>
  <label>Rol</label>
  <select id="role">
    <option value="ziyaretci">Ziyaretçi</option>
    <option value="veli">Veli</option>
    <option value="ogrenci" selected>Öğrenci</option>
    <option value="ogretmen">Öğretmen</option>
    <option value="yonetici">Yönetici</option>
    <option value="admin">ADMIN</option>
  </select>
  <label>Ad</label>
  <input type="text" id="uname" placeholder="ör. Kadir" value="Kadir"
    style="width:90px; padding:6px 8px; border-radius:8px; border:1px solid var(--line); background:var(--panel2); color:var(--text);">
  <label class="chk"><input type="checkbox" id="devmeta" checked> dev etiketleri</label>
</header>

<div id="log"></div>

<footer>
  <input type="text" id="q" placeholder="Bir soru yaz — ör. 'sınav nasıl oluşturulur'"
         autocomplete="off" autofocus>
  <button id="send">Gönder</button>
</footer>

<script>
const log = document.getElementById('log');
const q = document.getElementById('q');
const send = document.getElementById('send');
const roleSel = document.getElementById('role');
const devmeta = document.getElementById('devmeta');

function el(tag, cls, text) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (text !== undefined) e.textContent = text;
  return e;
}

function addUser(text) {
  const wrap = el('div', 'msg user');
  wrap.appendChild(el('div', 'bubble', text));
  log.appendChild(wrap);
  log.scrollTop = log.scrollHeight;
}

function escapeHtml(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}
// Basit markdown: **kalın**, `kod`, satır sonu. Metin bizim şablonlarımızdan gelir
// (güvenilir); yine de önce HTML kaçışı yapılır.
function md(s) {
  return escapeHtml(s || '(boş yanıt)')
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\n/g, '<br>');
}

function addBot(resp) {
  const wrap = el('div', 'msg bot');
  const bubble = el('div', 'bubble');
  bubble.innerHTML = md(resp.text);
  wrap.appendChild(bubble);
  // Yönlendirme (route): ilgili sayfaya götüren buton.
  if (resp.navigation) {
    const nav = el('button', 'nav-cta' + (resp.navigation.available ? '' : ' off'));
    nav.innerHTML = '<span>' + resp.navigation.label + '</span>' +
      '<span class="route">' + resp.navigation.route + '</span><span class="arr">→</span>';
    if (resp.navigation.available) {
      nav.addEventListener('click', () =>
        addSys('→ ' + resp.navigation.route + ' sayfasına yönlendirilir (gerçek gezinme front tarafında)'));
    } else {
      nav.title = 'Bu sayfa için yetkin yetmiyor';
    }
    bubble.appendChild(nav);
  }
  if (devmeta.checked) {
    const meta = el('div', 'meta');
    const safety = resp.safety || {};
    if (resp.intent) {
      const t = el('span', 'tag intent'); t.innerHTML = 'intent <b>' + resp.intent + '</b>'; meta.appendChild(t);
    }
    if (resp.fallback) meta.appendChild(el('span', 'tag fallback', 'fallback'));
    const conf = el('span', 'tag'); conf.innerHTML = 'güven <b>' + (resp.confidence ?? 0).toFixed(3) + '</b>'; meta.appendChild(conf);
    if (safety.category && safety.category !== 'CLEAN') {
      const t = el('span', 'tag safety'); t.innerHTML = 'safety <b>' + safety.category + '</b> · ' + safety.decision; meta.appendChild(t);
    }
    if (resp.auth_action) {
      const t = el('span', 'tag auth'); t.innerHTML = resp.auth_action + (resp.required_role ? ' · ' + resp.required_role : ''); meta.appendChild(t);
    }
    wrap.appendChild(meta);
  }
  // Netleştirme (item 1): ilk iki aday yakınsa "Bunu mu demek istedin?" çipleri.
  if (resp.clarification) {
    const box = el('div', 'clarify');
    box.appendChild(el('div', 'clarify-q', '🤔 Bunu mu demek istedin?'));
    resp.clarification.candidates.forEach(c => {
      const chip = el('button', 'chip', c.label);
      chip.addEventListener('click', () => { q.value = c.label; ask(); });
      box.appendChild(chip);
    });
    wrap.appendChild(box);
  }
  // Geri-bildirim (item 5): gerçek cevaplarda 👍/👎 -> /api/feedback.
  if (resp.intent && !resp.fallback) {
    const fb = el('div', 'fb');
    fb.appendChild(el('span', 'fb-label', 'Yardımcı oldu mu?'));
    ['up', 'down'].forEach(r => {
      const b = el('button', 'fb-btn', r === 'up' ? '👍' : '👎');
      b.addEventListener('click', () => sendFeedback(resp, r, fb));
      fb.appendChild(b);
    });
    wrap.appendChild(fb);
  }
  // Role göre başlangıç soru önerileri — yalnız "başlangıç/kayıp" anlarında
  // (selam/yardım/tanıtım/fallback/netleştirme); somut cevaplarda gösterme.
  const starterIntents = ['greeting', 'smalltalk', 'help_capabilities',
                          'platform_info', 'bot_identity', 'farewell', 'thanks'];
  const showSuggest = resp.fallback || !resp.intent || starterIntents.includes(resp.intent);
  if (resp.suggestions && resp.suggestions.length && showSuggest) {
    const sg = el('div', 'suggest');
    sg.appendChild(el('div', 'suggest-q', 'Şunları sorabilirsin:'));
    resp.suggestions.forEach(s => {
      const chip = el('button', 'chip', s);
      chip.addEventListener('click', () => { q.value = s; ask(); });
      sg.appendChild(chip);
    });
    wrap.appendChild(sg);
  }
  log.appendChild(wrap);
  log.scrollTop = log.scrollHeight;
}

function sendFeedback(resp, rating, fbEl) {
  fetch('/api/feedback', {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({trace_id: resp.trace_id, response_id: resp.response_id,
      intent: resp.intent, rating: rating})
  });
  fbEl.innerHTML = '<span class="fb-done">Teşekkürler! (' + (rating === 'up' ? '👍' : '👎') + ')</span>';
}

function addSys(text) {
  const line = el('div', 'sys', text);
  log.appendChild(line);
  log.scrollTop = log.scrollHeight;
}

function addError(text) {
  const wrap = el('div', 'msg bot');
  const b = el('div', 'bubble', '⚠ ' + text);
  b.style.borderColor = '#d0453b';
  wrap.appendChild(b);
  log.appendChild(wrap);
  log.scrollTop = log.scrollHeight;
}

async function ask() {
  const text = q.value.trim();
  if (!text) return;
  addUser(text);
  q.value = '';
  send.disabled = true;
  try {
    const r = await fetch('/api/chat', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        query: text,
        role: roleSel.value,
        authenticated: roleSel.value !== 'ziyaretci',
        user_id: 'dev-user',
        name: document.getElementById('uname').value
      })
    });
    const data = await r.json();
    if (data.error) addError(data.error); else addBot(data);
  } catch (e) {
    addError('Sunucuya ulaşılamadı: ' + e.message);
  } finally {
    send.disabled = false;
    q.focus();
  }
}

send.addEventListener('click', ask);
q.addEventListener('keydown', e => { if (e.key === 'Enter') ask(); });

addBot({text: "Merhaba! Ben Çelebi 🪽 — Hezarfen kullanım asistanı. Yukarıdan rolü değiştirip \\n" +
  "istediğini sorabilirsin. Örnekler: 'sınav nasıl oluşturulur', 'şifremi unuttum', \\n" +
  "'karnemi nerede görürüm', 'başka bir öğrencinin notunu görebilir miyim'.",
  safety: {}, confidence: 0});
</script>
</body>
</html>"""


class Handler(BaseHTTPRequestHandler):
    engine: Engine  # sınıf düzeyinde enjekte edilir

    def log_message(self, fmt, *args):  # sessiz: konsolu kirletme
        pass

    def _send(self, code: int, body: bytes, content_type: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, code: int, obj: dict) -> None:
        self._send(code, json.dumps(obj, ensure_ascii=False).encode("utf-8"),
                   "application/json; charset=utf-8")

    def do_GET(self) -> None:
        if self.path in ("/", "/index.html"):
            self._send(200, INDEX_HTML.encode("utf-8"), "text/html; charset=utf-8")
        else:
            self._send_json(404, {"error": "Bulunamadı"})

    def do_POST(self) -> None:
        if self.path not in ("/api/chat", "/api/feedback"):
            self._send_json(404, {"error": "Bulunamadı"})
            return
        try:
            length = int(self.headers.get("Content-Length", 0))
            payload_in = json.loads(self.rfile.read(length) or b"{}")
        except (ValueError, json.JSONDecodeError):
            self._send_json(400, {"error": "Geçersiz JSON"})
            return

        if self.path == "/api/feedback":
            record = {
                "trace_id": payload_in.get("trace_id"),
                "response_id": payload_in.get("response_id"),
                "query": payload_in.get("query"),
                "intent": payload_in.get("intent"),
                "rating": payload_in.get("rating"),  # "up" | "down"
            }
            try:
                with open(FEEDBACK_LOG, "a", encoding="utf-8") as fh:
                    fh.write(json.dumps(record, ensure_ascii=False) + "\n")
            except OSError:
                pass
            self._send_json(200, {"ok": True})
            return

        role = payload_in.get("role", "ziyaretci")
        request = {
            "query": payload_in.get("query", ""),
            "session": {
                "role": role,
                "authenticated": bool(payload_in.get("authenticated", role != "ziyaretci")),
                "user_id": payload_in.get("user_id"),
                "name": payload_in.get("name"),
            },
        }
        try:
            resp = self.engine.handle(request)
        except RequestError as exc:
            self._send_json(400, {"error": str(exc)})
            return
        except Exception as exc:  # pragma: no cover - beklenmeyen
            self._send_json(500, {"error": f"Sunucu hatası: {exc}"})
            return
        self._send_json(200, resp)


def main() -> int:
    parser = argparse.ArgumentParser(description="Hezarfen asistanı dev web arayüzü")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--rate-limit", action="store_true",
                        help="RateLimiter'ı devreye al (spam/tekrar testi)")
    args = parser.parse_args()

    limiter = RateLimiter() if args.rate_limit else None
    Handler.engine = Engine(rate_limiter=limiter)

    server = ThreadingHTTPServer((args.host, args.port), Handler)
    url = f"http://{args.host}:{args.port}"
    print(f"Roller: {', '.join(ROLE_HIERARCHY)}")
    print(f"Hezarfen dev arayüzü çalışıyor: {url}  (Ctrl+C ile durdur)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDurduruldu.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
