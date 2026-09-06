FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

# Reconstruct the verified ReasonEval V8 source bundle from text-safe chunks.
COPY src.part*.b64 /tmp/reasoneval-src/
RUN apt-get update \
    && apt-get install -y --no-install-recommends xz-utils \
    && cat /tmp/reasoneval-src/src.part*.b64 | base64 -d > /tmp/reasoneval.tar.xz \
    && tar -xJf /tmp/reasoneval.tar.xz -C /app \
    && pip install --no-cache-dir -r /app/requirements.txt \
    && rm -rf /tmp/reasoneval-src /tmp/reasoneval.tar.xz /var/lib/apt/lists/*

EXPOSE 8000
CMD ["sh","-c","uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers ${WEB_CONCURRENCY:-2}"]
