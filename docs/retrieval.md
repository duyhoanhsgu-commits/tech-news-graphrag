# Retrieval Strategy

## Overview

The system supports three retrieval modes, selectable per-query:

| Mode | Route | Description |
|---|---|---|
| `graphrag` | `/query/graphrag` | Hybrid vector + graph, then rerank |
| `vector` | `/query/vector` | Vector-only baseline |

## GraphRAG Pipeline

```
query
  │
  ├─ embed query ──────────────────────────► VectorRetriever (top_k×4)
  │                                                  │
  └─ GraphRetriever.expand(vector_results) ──────────┘
           │
           ▼
    Reciprocal Rank Fusion (RRF)
           │
           ▼
    CrossEncoder Reranker (top_k)
           │
           ▼
    ContextBuilder (max 4096 tokens)
           │
           ▼
    LLM → answer + [N] citations
```

## Fusion Formula (RRF)

`score(d) = vector_weight / (k + rank_v) + graph_weight / (k + rank_g)`

Default: `vector_weight=0.6`, `graph_weight=0.4`, `k=60`

## Configuration

All weights and top-k values are in `configs/retrieval.yaml` and overridable via `.env`.

## Metrics

Evaluated on `data/evaluation/` with:
- Exact Match (EM)
- Token F1
- Citation Coverage
