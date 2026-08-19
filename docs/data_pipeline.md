# Data Pipeline

## Stages

```
HuggingFace (cc_news)
        │
        ▼
  ArticleLoader
        │
        ▼
  ArticleNormalizer   ← Unicode NFKC, whitespace
        │
        ▼
  ArticleCleaner      ← strip HTML, min-length filter
        │
        ▼
  RecursiveChunker    ← chunk_size=512, overlap=64
        │
        ▼
  EmbeddingPipeline   ← batch=512, OpenAI text-embedding-3-small
        │
        ├──► pgvector (chunks table)
        │
        └──► GraphBuilder
                │
                ├── EntityExtractor  (LLM)
                ├── RelationExtractor (LLM)
                └── EntityDeduplicator → Neo4j
```

## Output Files (data/processed/)

| Path | Format | Description |
|---|---|---|
| `articles/articles.jsonl` | JSONL | Cleaned articles |
| `chunks/*.jsonl` | JSONL | Chunks per article |
| `entities/*.jsonl` | JSONL | Extracted entities |
| `relationships/*.jsonl` | JSONL | Extracted relationships |

## Running

```bash
python scripts/download_dataset.py
python scripts/ingest_articles.py --limit 5000
python scripts/build_vector_index.py
python scripts/build_graph.py
```
