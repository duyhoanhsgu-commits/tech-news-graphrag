# tech-news-graphrag

A production-ready **GraphRAG** pipeline for tech-news articles.
Combines **vector similarity search** (pgvector) with **knowledge-graph traversal** (Neo4j)
to answer questions with grounded, cited responses via a FastAPI service.

---

## Architecture

```
articles ──► ingestion ──► chunking ──► embedding ──► pgvector
                │
                └──► entity/relation extraction ──► Neo4j
                                                      │
query ──► vector retriever ◄── hybrid retriever ──────┘
              │
              └──► reranker ──► context builder ──► LLM ──► answer + citations
```

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python ≥ 3.11
- OpenAI API key (or another supported provider)

### 1. Clone & configure
```bash
git clone <repo-url> tech-news-graphrag
cd tech-news-graphrag
cp .env.example .env
# Edit .env — set OPENAI_API_KEY at minimum
```

### 2. Start infrastructure
```bash
docker compose up -d postgres neo4j
```

### 3. Install Python dependencies
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

### 4. Run migrations
```bash
alembic upgrade head
```

### 5. Ingest data
```bash
python scripts/download_dataset.py
python scripts/ingest_articles.py
python scripts/build_vector_index.py
python scripts/build_graph.py
```

### 6. Start the API
```bash
uvicorn src.graphrag.main:app --reload
# → http://localhost:8000/docs
```

---

## Project Layout

```
configs/          YAML configs (app, embedding, retrieval, graph, logging)
data/             raw → processed articles/chunks/entities/relationships
docker/           Dockerfiles for api and worker
docs/             architecture, data pipeline, graph schema, retrieval docs
migrations/       Alembic SQL migrations
scripts/          one-off CLI scripts (download, ingest, index, eval)
src/graphrag/     main application package
tests/            unit + integration tests
```

## Key Commands

| Command | Description |
|---|---|
| `pytest` | Run all tests |
| `ruff check src` | Lint |
| `mypy src` | Type check |
| `alembic revision --autogenerate -m "msg"` | New migration |
| `python scripts/run_evaluation.py` | Evaluate retrieval quality |

## Configuration

All runtime config lives in `configs/` (loaded by `src/graphrag/core/config.py`).
Environment variables override YAML values — see `.env.example` for the full list.

## Documentation

- [Architecture](docs/architecture.md)
- [Data Pipeline](docs/data_pipeline.md)
- [Graph Schema](docs/graph_schema.md)
- [Retrieval Strategy](docs/retrieval.md)
# tech-news-graphrag
