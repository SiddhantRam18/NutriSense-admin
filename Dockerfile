FROM python:3.10-slim as builder

WORKDIR /app

COPY FastAPI_Backend/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt && \
    find /root/.local -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

FROM python:3.10-slim

COPY --from=builder /root/.local /root/.local

COPY FastAPI_Backend/main.py FastAPI_Backend/model.py /app/backend/
COPY Data /app/Data

WORKDIR /app/backend

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app/backend:$PYTHONPATH
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

EXPOSE 7860

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860", "--workers", "1", "--timeout-keep-alive", "5"]
