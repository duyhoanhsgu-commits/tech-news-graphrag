FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./
RUN pip install --no-cache-dir -e "."

COPY src/ ./src/
COPY configs/ ./configs/
COPY scripts/ ./scripts/

# Worker entry point — e.g. celery or arq for background indexing jobs
CMD ["python", "scripts/build_vector_index.py"]
