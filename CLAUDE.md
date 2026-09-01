# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

Starter/baseline repository for the HAW Hamburg elective **Agentic AI / Human–Agent Software Company**. A team ("company") builds a mixed human–agent org on top of a fixed technical stack: Python 3.12, FastAPI, LangChain + LangGraph, PostgreSQL + pgvector, Docker Compose, pytest, and an LLM via local Ollama or an OpenAI-compatible HAW ICC endpoint.

**Critical assessment boundary**: `examples/**` and `tests/starter/**` are course-supplied reference code and do not count as team work — see `docs/STARTER_BOUNDARY.md`. Team-owned agents belong in `src/agents/` (currently empty except a README describing the expected shape of an agent: role, input, state schema, tools/permissions, structured output, failure behavior, trace evidence, accountable human, cost evidence). When asked to build "the agent" for this project, build it there, not by extending `examples/`.

## Commands

```bash
# Python env (3.12 required)
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Start Postgres+pgvector only (app runs natively against it)
docker compose up -d db

# Run the API locally (reads .env)
python -m uvicorn src.app.main:app --reload
# -> http://localhost:8000/docs, /health, /db/health

# Full stack in Docker
docker compose up --build

# Tests — always use `python -m pytest`, not bare `pytest`, so it runs in the
# project's venv and pytest.ini's `pythonpath = .` takes effect (needed to
# import both `src` and `examples`).
python -m pytest
python -m pytest tests/starter/test_api.py::test_health_endpoint  # single test

# Reference LangGraph example (not assessment evidence, but verifies the
# LangChain/LangGraph/LLM/tracing wiring works end to end)
python -m examples.file_review_agent --input src/app/main.py
```

Dependency versions in `requirements.txt` are pinned as a shared course baseline; do not upgrade LangChain/LangGraph packages individually without going through an approval Issue (see README "Compatibility policy").

## Architecture

```
src/app/        FastAPI app + Pydantic settings (env-driven) + Postgres health check
src/llm/        Provider-agnostic chat/embedding model factory (Ollama | OpenAI-compatible)
src/rag/        pgvector helpers (PGEngine/PGVectorStore init + open), infra only — no
                ingestion/chunking/retrieval policy implemented
src/observability/  Local JSONL trace writer + abstract "credit" cost estimator
src/agents/     Empty — team-owned LangGraph agents go here
examples/       Course reference LangGraph agent (excluded from assessment)
tests/starter/  Course reference tests (excluded from assessment)
organization/   company.md + roles.yaml — team fills in during Session 1/2
costs/          cost-model.yaml (rate assumptions) + usage.csv (actual usage log)
docs/           architecture.md (team-owned, mermaid diagram), STARTER_BOUNDARY.md
                (what counts for grading), ICC_CONFIGURATION.md (HAW ICC endpoint setup)
```

**Provider abstraction is load-bearing**: `src/llm/factory.py` is the only place that should branch on `settings.llm_provider` ("ollama" vs "openai_compatible"). Agent code must call `get_chat_model()` / `get_embeddings()` from this factory rather than instantiating `ChatOllama`/`ChatOpenAI` directly, so switching between local Ollama and the HAW ICC endpoint is a config-only change (see `docs/ICC_CONFIGURATION.md`). Same principle for embeddings via `src/rag/vectorstore.py`.

**Settings**: `src/app/settings.py`'s `Settings` (pydantic-settings) reads `.env` and is the single source of config; `get_settings()` is `lru_cache`d. New env vars belong here, mirrored in `.env.example` and in `docker-compose.yml`'s `app.environment` block.

**Tracing/cost pattern** (`src/observability/tracing.py`), used by `examples/file_review_agent.py` as the reference implementation team agents are expected to follow:
- `append_trace(record, trace_file=None)` appends a JSON line (with UTC `logged_at`) to `TRACE_FILE` (default `logs/agent-runs.jsonl`), including `run_id`, `task_id`, `agent`, `status`, `tools`, `duration_seconds`, token counts, and estimated cost.
- `estimate_cost_credits(...)` computes abstract "credits" (not currency) from `costs/cost-model.yaml`-derived settings (base + runtime + per-1k-token input/output).
- `usage_from_message(message)` pulls `usage_metadata` off a LangChain response when the provider returns it.

**Reference agent shape** (`examples/file_review_agent.py`): a small LangGraph `StateGraph` (`TypedDict` state) with a deterministic tool node feeding a chat-model node, parsing the model's JSON reply into a Pydantic result with a graceful `"unparseable"` fallback, and writing a trace record on both success and error paths. It deliberately avoids model-native tool calling for compatibility with small local models. New agents under `src/agents/` are expected to follow this same graph → structured-output → trace shape.

**Role/actor model** (`organization/roles.yaml`, explained in `docs/STARTER_BOUNDARY.md`): twelve predefined company roles, each with `current_actor_type` vs `target_actor_type` (human/agent/hybrid) and an `implementation_status` (`planned` vs `operational`). A role only counts as `operational` when there's team-owned executable evidence (agent code + trace) for it. One agent may cover multiple roles only if role-specific behavior/output is technically distinguishable and the trace identifies which role was performed.

## Working in this repo

- `db/init.sql` only enables the `vector` extension; no application schema exists yet — RAG table creation happens explicitly via `src/rag/vectorstore.py:initialize_vector_store`, not at import time.
- `costs/usage.csv` is meant to hold actual recorded usage, distinct from the rate assumptions in `costs/cost-model.yaml`.
- Placeholder team docs (`organization/company.md`, `organization/roles.yaml`, `docs/architecture.md`, `costs/cost-model.yaml`) are templates with `TBD` fields — filling these in is itself part of the assessed work, not boilerplate to skip past.
