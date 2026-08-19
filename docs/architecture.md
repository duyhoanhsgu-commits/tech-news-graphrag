# Architecture

## Overview

```
┌─────────────────────────────────────────────────────────┐
│                      FastAPI API                        │
│   /query/graphrag   /query/vector   /graph   /admin     │
└───────────────────────┬─────────────────────────────────┘
                        │
          ┌─────────────▼─────────────┐
          │      GraphRAGPipeline      │
          └───┬───────────────────┬───┘
              │                   │
   ┌──────────▼──────┐   ┌───────▼────────┐
   │ HybridRetriever  │   │ AnswerGenerator│
   └──┬──────────┬───┘   └───────┬────────┘
      │          │               │
 ┌────▼───┐  ┌───▼───┐     ┌────▼────┐
 │ Vector │  │ Graph │     │  LLM    │
 │ (pgvec)│  │(Neo4j)│     │ Client  │
 └────────┘  └───────┘     └─────────┘
```

## Component Responsibilities

| Component | Responsibility |
|---|---|
| `IngestionPipeline` | Load → normalize → clean articles |
| `ChunkingPipeline` | Split articles into overlapping chunks |
| `EmbeddingPipeline` | Batch-embed chunks via provider API |
| `VectorRepository` | Upsert + search embeddings in pgvector |
| `GraphBuilder` | Extract entities/relations and store in Neo4j |
| `HybridRetriever` | RRF fusion of vector + graph results |
| `Reranker` | Cross-encoder score refinement |
| `AnswerGenerator` | LLM grounded answer with [N] citations |

## Data Flow

1. **Indexing** (offline): articles → chunks → embeddings → pgvector
2. **Graph building** (offline): chunks → LLM extraction → entities/relations → Neo4j
3. **Query** (online): question → embed → vector search + graph expansion → RRF → rerank → LLM → answer
