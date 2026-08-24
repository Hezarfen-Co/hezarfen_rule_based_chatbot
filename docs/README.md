# Çelebi belgeleri

Kökte yalnız GitHub giriş belgesi `ReadMe.md` ve ajan yönergesi `CLAUDE.md`
tutulur. Projeye ait diğer Markdown belgeleri burada toplanır.

## Ürün ve sistem belgeleri

- [Hezarfen site rehberi](hezarfen-site-rehberi.md): sayfalar, roller, gerçek
  menü etiketleri ve işlem akışları için chatbot bilgi kaynağı.
- [Sistem soru envanteri](SISTEM_SORU_ENVANTERI.md): frontend rotaları, backend
  hata yüzeyi ve kullanıcının sorabileceği destek alanları.
- [Podman/WSL kurulumu](../deploy/PODMAN-WSL-SETUP.md): ürün yığınını repo bazlı
  compose dosyalarıyla çalıştırma notları.

## Benchmark belgeleri

- [Gold benchmark soru-cevap raporu](benchmarks/BENCHMARK_SONUCLARI.md)
- [10K stres benchmark özeti](benchmarks/STRES_BENCHMARK_SONUCLARI.md)
- [10K stres soru-cevap parçaları](benchmarks/STRES_BENCHMARK_SONUCLARI_parcalar/)

Gold soruların tek makine kaynağı `data/benchmark.jsonl`, tam Engine sonuçlarının
tek birleşik JSON çıktısı `data/benchmark_results.json` dosyasıdır. Her kayıtta
rol bulunduğu için ayrı rol benchmark dosyaları tutulmaz.

## Arşiv

- [22 Ağustos 2026 proje devri](archive/PROJECT_STATE-2026-08-22.md): yalnız
  tarihsel bağlamdır; güncel durum belgesi değildir.
