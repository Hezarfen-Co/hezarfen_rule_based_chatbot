# Hezarfen Kullanım Asistanı — Kural Tabanlı Chatbot

Hezarfen okul yönetim sitesinin **rol-farkında kullanım asistanı**. "Nasıl
yaparım?" tarzı soruları, sitenin gerçek menü/etiket ve yollarına dayanarak
adım adım yanıtlar. Harici çalışma-zamanı bağımlılığı yoktur (yalnızca Python
standart kütüphanesi) ve tamamen offline çalışır.

Bilgi kaynağı: `hezarfen-site-rehberi.md`.

## Mimari (boru hattı)

```
sorgu
  → normalize (Türkçe küçük harf + aksan katlama + hafif kök)   src/normalize.py
  → kural katmanı (yüksek kesinlik, önek eşleşmesi)             src/rules.py
  → benzerlik (TF-IDF karakter n-gram + kosinüs)                src/similarity.py
  → domain-gate (alan-dışı sorguyu OOS'a at)                    src/domain.py
  → karar (eşik + tie-break + rol gating)                       src/decision.py
  → cevap (rol-farkında, gerçek etiket/yol)                     src/responder.py
```

Her sorgu izlenir (per-stage latency + karar detayı) — `src/observability.py`.
Backend sözleşmesi `src/engine.py`, terminal frontend `src/cli.py`.

### Katmanlı tasarım neden?
- **Kural katmanı** tek-anlamlı ve güvenlik-kritik soruları deterministik
  (~%100 kesinlikle) bağlar; belirsizlikte karar vermez.
- **Benzerlik** kalan soruları toplar; "X nasıl oluşturulur" gibi ortak fiilli
  kalıpları kural katmanı alan-ismiyle (sınav/ders/dönem) ayırır.
- **Domain-gate** char n-gram'ın OOS zayıflığını kapatır (OOS recall %44 → %78).

## Modüller

| Modül | Görev |
|---|---|
| `catalog.py` | Intent kataloğu (43 intent) + rol modeli + doğrulayıcı |
| `benchmark.py` | Değerlendirme setini yükle/doğrula (`data/benchmark.jsonl`) |
| `normalize.py` | Normalizasyon + Türkçe kök bulma + katlanmış token |
| `rules.py` | Yüksek-kesinlik kural katmanı |
| `similarity.py` | TF-IDF karakter n-gram benzerliği |
| `domain.py` | Alan (OOS) kapısı |
| `decision.py` | Eşik + tie-break + rol gating |
| `responder.py` | Cevap üretimi (rol-farkında) |
| `observability.py` | Aşama bazlı yapısal loglama (trace + alarm) |
| `metrics.py` / `evaluate.py` | Metrikler + tam değerlendirme aracı |
| `engine.py` | Backend servis + front/back sözleşmesi |
| `cli.py` | Terminal frontend |

## Çalıştırma

```bash
python -m src.main --validate    # kataloğu doğrula
python -m src.main --evaluate    # benchmark üzerinde tam metrik raporu
python -m src.main --chat        # etkileşimli terminal asistanı

# Docker
docker compose up --build        # container içinde --validate
```

### Terminal örneği
```
(ziyaretci) > /rol ogrenci
Rol ayarlandı: ogrenci (authenticated=True)
(ogrenci) > sınava nasıl girerim
[exam_enter_room] Ön koşul: sınavın dersine kayıtlı olmak; ...
```

## Front/back sözleşmesi

İstek:
```json
{"query": "...", "session": {"role": "ogrenci", "authenticated": true}, "trace_id": "opsiyonel"}
```
Yanıt:
```json
{"trace_id","response_id","text","intent","confidence","fallback","auth_action","required_role"}
```

## Metrikler (mevcut baseline)

`python -m src.main --evaluate` (eşik 0.18 + domain-gate):

| Metrik | Değer | Anlamı |
|---|---|---|
| **Macro-F1** | **0.86** | Başlık metriği; her intent'e eşit ağırlık (nadir intent'leri saklamaz) |
| Accuracy | %86 | Genel doğruluk (dengesizlikte yanıltıcı olabilir) |
| Top-1 / Top-3 | %86 / %95 | Doğru cevap ilk 1 / ilk 3 tahminde |
| Coverage | %100 | FALLBACK yerine cevap verilen in-scope oranı |
| Accuracy-on-covered | %86 | Cevap verince doğruluk |
| OOS recall | %78 | Kapsam dışını doğru reddetme |
| Latency p50/p95 | ~0.8 / 1.3 ms | Sorgu başına gecikme |

**Neden bu metrikler:** Macro-F1 dengesiz sınıfta kritik-ama-nadir intent'lerin
(gizlilik, şifre) bozukluğunu saklamaz. Coverage/OOS-recall, FALLBACK'in
getirdiği "cevap verme cesareti" dengesini ölçer. Güvenlik için `privacy_security`
recall'ı ve auth sızıntısı ayrıca izlenir (regresyon testinde sabitlenmiştir).

## Testler

```bash
python -m unittest discover -s tests -t .
```
- `tests/unit/` — her modül/metot için birim testler
- `tests/integration/` — kural/karar/motor + benchmark değerlendirmesi
- `tests/e2e/` — uçtan uca sohbet senaryoları
- `tests/integration/test_regression.py` — kalite eşikleri (macro-F1 ≥ 0.80,
  OOS recall ≥ 0.70, gizlilik recall = 1.0, kural precision = 1.0) düşerse kırılır.

## Yeni intent ekleme

1. `src/catalog.py` içine `INTENTS`'e kayıt ekle (tüm zorunlu alanlar + `min_role`).
2. `data/benchmark.jsonl`'e o intent için birkaç (örneklerden farklı) soru ekle.
3. Çok belirgin bir anahtar kelimesi varsa `src/rules.py`'a kural ekle.
4. `python -m src.main --validate && python -m src.main --evaluate` ile öncesi/
   sonrası karşılaştır; `python -m unittest discover -s tests -t .` yeşil olmalı.

## Bilinen sınırlar / sıradaki adım
- OOS'ta ~%22 (alan fiili paylaşan sorular) hâlâ kaçıyor — char n-gram tavanı.
  Benzerlik arayüzü soyut (`SimilarityMatcher`); **yerel embedding** modeli aynı
  sözleşmeyle takılıp bu boşluğu kapatabilir.
