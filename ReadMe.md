# Rule-Based Education Chatbot

Eğitim platformu için geliştirilen kural tabanlı chatbot projesi.

## Docker ile çalıştırma

Gereksinimler: Docker Desktop ve Docker Compose.

Katalog doğrulamasını container içinde çalıştırmak için:

```powershell
docker compose run --rm chatbot
```

İmajı yeniden oluşturmadan yalnızca tekrar çalıştırmak için:

```powershell
docker compose run --rm --no-build chatbot
```

Testleri container içinde çalıştırmak için:

```powershell
docker compose run --rm chatbot python -m unittest discover -v
```

Kaynak kod veya bağımlılıklar değiştiğinde imajı yeniden oluşturun:

```powershell
docker compose build
```

Şimdilik container, `src/QandA.py` soru/cevap kataloğunun veri bütünlüğünü
doğrulayan tek seferlik bir komut çalıştırır. Chatbot motoru veya HTTP API
eklendiğinde `Dockerfile` ve `compose.yaml` başlangıç komutu güncellenecektir.
