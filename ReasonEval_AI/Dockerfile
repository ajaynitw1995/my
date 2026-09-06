FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY ReasonEval_AI_V8_Production_Beta.zip /tmp/reasoneval.zip
RUN python -m zipfile -e /tmp/reasoneval.zip /app \
    && pip install --no-cache-dir -r /app/requirements.txt \
    && rm /tmp/reasoneval.zip
EXPOSE 8000
CMD ["sh","-c","uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers ${WEB_CONCURRENCY:-2}"]
