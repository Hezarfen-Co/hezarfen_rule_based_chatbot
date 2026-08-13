FROM python:3.13-slim@sha256:bffeb7bd6a85767587059c6ba23e1e9122078e3aa3fa836099171b9bb5a9bb00

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Uygulama bağımlılıkları eklendiğinde Docker katman önbelleğinden yararlanır.
COPY requirements.txt ./
RUN pip install --no-cache-dir --requirement requirements.txt

COPY src ./src
COPY tests ./tests
COPY data ./data

# Container'ı root olmayan kullanıcıyla çalıştır.
RUN useradd --create-home --uid 10001 chatbot \
    && chown -R chatbot:chatbot /app
USER chatbot

CMD ["python", "-m", "src.main", "--validate"]
