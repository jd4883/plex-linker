# Chainguard Python multi-stage build.
# https://edu.chainguard.dev/chainguard/chainguard-images/getting-started/python/
FROM cgr.dev/chainguard/python:latest-dev AS builder

ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

WORKDIR /app

RUN python -m venv /app/venv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p data config_files config_files/archives \
    && chown -R 65532:65532 /app

# --- Runtime: minimal Chainguard Python (no shell, no pip) ---
FROM cgr.dev/chainguard/python:latest

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

ENV PLEX_LINKER=/app \
    CONFIG_ARCHIVES=/app/config_files/archives \
    DATABASE_URL=sqlite:////app/data/plex_linker.db \
    MEDIA_ROOT= \
    DOCKER_MEDIA_PATH= \
    HOST_MEDIA_PATH= \
    SONARR_0_URL= \
    SONARR_0_API_PATH=/api/v3 \
    SONARR_API_KEY= \
    RADARR_0_URL= \
    RADARR_0_API_PATH=/api/v3 \
    RADARR_API_KEY= \
    PLEX_URL= \
    PLEX_API_KEY= \
    SONARR_ROOT_PATH_PREFIX=/ \
    PLEX_LINKER_SCAN_INTERVAL_MINUTES=15 \
    TZ=UTC

COPY --from=builder /app /app

USER 65532:65532

EXPOSE 8080

CMD ["python", "main.py", "serve", "--host", "0.0.0.0", "--port", "8080"]
