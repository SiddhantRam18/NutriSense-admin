# backend/Dockerfile

# Build stage
FROM python:3.10-slim as builder

WORKDIR /app

COPY FastAPI_Backend/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt && \
    find /root/.local -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true && \
    find /root/.local -type d -name "*.dist-info" -exec rm -rf {} + 2>/dev/null || true

# Runtime stage
FROM python:3.10-slim

# Copy only necessary Python packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY FastAPI_Backend /app/backend
COPY Data /app/Data

WORKDIR /app/backend

# Set PATH and PYTHONPATH
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app/backend:$PYTHONPATH
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONHASHSEED=random

# Aggressive memory optimization
ENV MALLOC_TRIM_THRESHOLD_=64000
ENV MALLOC_MMAP_THRESHOLD_=131072
ENV MALLOC_MMAP_MAX_=65536

# GC settings for lower memory footprint
ENV PYTHONGC_ENABLE=1

EXPOSE 7860

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860", "--workers", "1", "--timeout-keep-alive", "5"]