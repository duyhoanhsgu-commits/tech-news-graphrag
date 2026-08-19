#!/usr/bin/env bash
# scaffold.sh — Creates the full tech-news-graphrag project skeleton
# Run from anywhere; TARGET_DIR is the project root.
set -euo pipefail

TARGET_DIR="/home/hoanh-tran/my project/RAG_report/tech-news-graphrag"
cd "$TARGET_DIR"

# ── helpers ──────────────────────────────────────────────────────────────────
mkf() { mkdir -p "$(dirname "$1")"; touch "$1"; }
pyinit() { mkf "$1/__init__.py"; }

# ── data skeleton ────────────────────────────────────────────────────────────
for d in data/raw data/processed/articles data/processed/chunks \
          data/processed/entities data/processed/relationships \
          data/evaluation; do
  mkdir -p "$d"
  touch "$d/.gitkeep"
done

# ── migrations (Alembic) ─────────────────────────────────────────────────────
mkdir -p migrations/versions
touch migrations/__init__.py

# ── docs ─────────────────────────────────────────────────────────────────────
mkdir -p docs

# ── tests ────────────────────────────────────────────────────────────────────
pyinit tests
pyinit tests/unit
pyinit tests/integration
mkdir -p tests/fixtures
touch tests/fixtures/__init__.py
touch tests/conftest.py

# ── docker ───────────────────────────────────────────────────────────────────
mkdir -p docker

# ── src Python packages ──────────────────────────────────────────────────────
GRAPHRAG="src/graphrag"
for pkg in \
    "" \
    api api/routes \
    core \
    schemas \
    ingestion \
    chunking \
    embeddings \
    vectorstore \
    graph graph/extraction graph/resolution graph/store \
    retrieval \
    generation \
    pipelines \
    repositories \
    evaluation; do
  pyinit "$GRAPHRAG/$pkg"
done

echo "✓ directory & __init__ skeleton done"
