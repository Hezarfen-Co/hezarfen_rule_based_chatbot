FROM python:3.13-slim@sha256:bffeb7bd6a85767587059c6ba23e1e9122078e3aa3fa836099171b9bb5a9bb00

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Uygulama bağımlılıkları eklendiğinde konteyner katman önbelleğinden yararlanır.
COPY requirements.txt ./
RUN pip install --no-cache-dir --requirement requirements.txt

COPY src ./src
COPY tests ./tests
COPY data ./data

# Konteynerı root olmayan kullanıcıyla çalıştır.
RUN useradd --create-home --uid 10001 chatbot \
    && chown -R chatbot:chatbot /app
USER chatbot

# Dağıtım varsayılanları — TEK yazıldıkları yer. Sunucu bunları
# hezarfen_rule_based_chatbot.env (env_file) ile ezer; compose dosyası hiçbir anahtar
# listelemez, böylece operatörün dosyası gölgelenemez.
#
# AI_BACKEND_URL köprünün sertifikayı çektiği HTTP kökü: backend konteynerinin
# kendi portu (compose'da PORT=7656). Sertifika her (yeniden) bağlanmada
# tazelenir.
#
# AI_TLS_FINGERPRINT BURADA TANIMLI DEĞİL, bilerek: tanımsız = TOFU (sertifika
# pinlenir ama kimliği doğrulanmaz, her açılışta loglanır). Üretimde operatörün
# env dosyasından 64 karakterlik SHA-256 verilir; uyuşmayan sertifikaya
# bağlanılmaz. Değeri `GET /ai/certificate` cevabındaki `fingerprint_sha256`
# verir.
ENV AI_BRIDGE_HOST=hezarfen_backend \
    AI_BRIDGE_PORT=8090 \
    AI_BACKEND_URL=http://hezarfen_backend:7656 \
    AI_SHARED_TOKEN= \
    AI_TLS_SERVER_NAME=localhost \
    AI_SERVICE_NAME=celebi \
    HEZARFEN_ASSISTANT_ROLE=ogrenci \
    AI_MAX_CONCURRENT=8 \
    AI_RECONNECT_SECS=3 \
    AI_RECONNECT_MAX_SECS=120

# Konteynerın işi köprüyü çalıştırmak. Katalog/benchmark komutları bu imajın
# içinde elle koşulur: `podman run --rm IMAGE python -m src.main --validate`.
CMD ["python", "-m", "src.bridge"]
