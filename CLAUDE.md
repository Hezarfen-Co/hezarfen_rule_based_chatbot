# CLAUDE.md — Rule-Based-Chatbot (Hezarfen kullanım asistanı)

## Ne bu proje
Hezarfen okul yönetim sitesi için **rol-farkında, kural+benzerlik hibrit**
kullanım asistanı + **içerik güvenliği** katmanı. Sıfır harici bağımlılık
(yalnızca stdlib), offline. Bilgi kaynağı: `hezarfen-site-rehberi.md`.

## Boru hattı
`safety(giriş) → normalize → rules → similarity → domain-gate → decision → responder → safety(çıktı)`
İzleme/loglama: `observability.py`. Backend sözleşmesi: `engine.py`.
Frontend'ler: `cli.py` (terminal), `web.py` (geliştirici web arayüzü, stdlib http.server).
İçerik güvenliği: `safety/` paketi (bağımsız kural motoru, standart SafetyDecision).

## Paket yapısı (Aşama 12: reorg)
- `safety/` — güvenlik & yetki: `toxicity.py` (içerik tespiti), `pii.py` (maskeleme),
  `rate_limiter.py`, `authorization.py` (IDOR/BOLA), `decisions.py` (SafetyDecision).
  Genel API `safety/__init__.py`'den re-export edilir; `engine` yalnız bunu kullanır.
  `authorization` sabitleri (ALLOW/REQUIRE_AUTHORIZATION) toxicity ile çakıştığından
  RE-EXPORT EDİLMEZ — `from src.safety.authorization import ...` ile alınır.
- `evaluation/` — `benchmark.py`, `metrics.py`, `evaluate.py`.
- Düz kalanlar: catalog, normalize, rules, similarity, embedding, domain, decision,
  responder, engine, observability, cli, web, main.

## Komutlar
- `python -m src.main --validate` — katalog doğrulama
- `python -m src.main --evaluate` — tam metrik raporu (benchmark)
- `python -m src.main --chat` — etkileşimli terminal
- `python -m src.web` — geliştirici web arayüzü (http://127.0.0.1:8000)
- `python -m unittest discover -s tests -t .` — tüm testler (334)
- `python -m tests.e2e.test_conversation --transcript` — 212 konuşmayı bot
  cevaplarıyla konsola basar; `--markdown` aynısını `KONUSMALAR.md`'ye yazar
  (KONUSMALAR.md üretilmiş dosyadır, elle düzenlenmez)

## Asistan kimliği & konuşma davranışları
- Asistanın adı **Çelebi** (`catalog.ASSISTANT_NAME`; Hezarfen Ahmed Çelebi'den).
  Bota adıyla sataşma kişiye-taciz DEĞİL bota-yönelik sayılır ('celebi'
  toxicity._COMMON_TITLE'da).
- **Cevap varyantları**: sosyal intent'lerde (smalltalk/thanks/farewell) opsiyonel
  `response_variants`; seçim RASTGELE DEĞİL, sorgunun CRC32'siyle deterministik
  (responder._select_body). response_id her varyantta sabit.
- **Selamlama aynalama**: greeting şablonundaki `{selam}`, kullanıcının selamına
  göre çözülür ('günaydın' -> 'Günaydın! ☀️'; catalog.GREETING_OPENERS).
- **Belirsiz bölge (ask-zone)**: benzerlik güveni < 0.30 (engine.ASK_CONFIDENCE) ise
  tam cevap VERİLMEZ — `response_id="clarification_prompt"` + "anlayamadım, bunu mu
  demek istedin?" + 2 aday döner (intent=None, fallback=False). Kural kararları muaf.
  Metrikler etkilenmez (evaluate karar katmanını ölçer, sunum katmanını değil).
- **Çoklu-istek**: 've/ayrıca/virgül' ile ayrılan parçalardan ≥2'si KURAL katmanında
  FARKLI intent'lere çarparsa hepsi yanıtlanır (en çok 3); sözleşmede `answers`
  listesi dolar, tekli istekte `answers=null`. Benzerlik-intent'li parçalar
  sayılmaz (muhafazakâr tasarım — 'roller ve yetkiler' bölünmez).
- Oturum rolleri İngilizce adlarla da gelebilir (student/teacher/manager/admin/
  **parent** -> engine._ROLE_NAME_ALIASES).
- **Rol hiyerarşisi 6 kademe**: ziyaretci < **veli** < ogrenci < ogretmen <
  yonetici < admin. Veli = bağlı öğrencilerin salt-okunur gözlemcisi (backend
  Parent); sınava giremez/kaydolamaz. MIN_AUTHENTICATED_ROLE='veli'.
- **Backend v2 intent'leri** (gerçek repo incelemesinden): pomodoro_use,
  student_pomodoro_lookup, messages_use, study_club_info, parent_info. Kaynak:
  hezarfen_backend/hezarfen_frontend repoları (i18n etiketleri birebir);
  rehberde YOKLAR — rehber güncellenince metinler teyit edilmeli.

## Önemli tasarım kararları (tekrar keşfetme)
- **Kural katmanı stem KULLANMAZ**; `folded_tokens` + önek eşleşmesi kullanır.
  Stemmer 'yapamıyor'→'yap' gibi çökertip kesinliği bozuyordu. Stemmer yalnızca
  `roots()` (log/teşhis) içindir.
- **Kural katmanı belirsizlikte karar vermez** (None → benzerliğe bırakır); hedef
  kapsanan sorularda ~%100 kesinlik.
- **Domain-gate** OOS için şart: char n-gram tek başına OOS'u ayıramıyor. Gate OOS
  recall'ı %44→%78 yaptı. Eşik = 0.18 (`decision.DEFAULT_THRESHOLD`).
- **safety/toxicity.py niyet/yetki'den AYRI** bir kural motorudur; giriş kapısı + çıktı
  kontrolü olarak `engine.handle` içinde çağrılır. Standart SafetyDecision döndürür.
  - Güvenlik-normalizasyonu agresif (leetspeak/tekrar/harf-aralama/görünmez unicode).
  - Yanlış-pozitif önleme: kısa kökler (`mal`,`sik`) TAM-kelime eşleşir; alan/ortak
    kelimeler ('Ders','Karne') isim sayılmaz (domain vocab ile elenir).
  - Kendine zarar → SAFE_RESPONSE (cezalandırıcı DEĞİL); tehdit/çocuk → requires_review.
- **Hezarfen'de ödev/ders-programı/duyuru YOK** — eski generic katalog pivotlandı
  (`src/QandA.py` silindi). Bu özelliklere intent EKLEME.
- `response_id` gating altında bile kararlıdır; testler metne değil id'ye bakar.

## Kalite eşikleri (regresyon — tests/integration/test_regression.py)
macro-F1 ≥ 0.80, OOS recall ≥ 0.70, coverage ≥ 0.95, gizlilik recall = 1.0,
kural precision = 1.0. Bunları düşüren değişiklik testi kırar.
Güvenlik örnek-tablosu regresyonu: tests/unit/test_safety.py (ExampleTableTests).

## Test yapısı
`tests/unit` (her modül), `tests/integration` (benchmark değerlendirmeleri +
regresyon + engine + safety_engine + **edge_cases**: adversarial/gizleme regresyonu),
`tests/e2e` (sohbet senaryoları + **behavior_matrix**: "şu girdiye şu response_id"
davranış sözleşmesi — 53 intent × rol gating × güvenlik; front/back buna güvenir).
Kullanıcıya görünen davranışı değiştiren HER değişiklikte behavior_matrix
güncellenmeli; bilinçli sınırlar `test_edge_cases.KnownLimitTests`'te sabitli
(olumsuzlama yok sayılır, çoklu-intent ilkini alır, İngilizce fallback).

## Genişletme
- Yeni intent: `catalog.INTENTS` + `INTENT_ROUTES` (route ya da None; validate zorlar)
  + `data/benchmark.jsonl` (örneklerden farklı) + gerekiyorsa `rules.py` +
  `tests/e2e/test_behavior_matrix.INTENT_MATRIX`'e satır (kapsam testi zorlar).
  Sonra `--validate`, `--evaluate`, testler.
- Yeni güvenlik kuralı: `safety/toxicity.py` içine sözlük/pattern + standart SafetyDecision;
  test grubunu (normal/açık/gizlenmiş/eğitim/FP) `tests/unit/test_safety.py`'a ekle.
- Daha güçlü OOS/anlam: `SimilarityMatcher` arayüzüne yerel embedding tak.
