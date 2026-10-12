# Architecture - Harbor QA Agents

This document describes the Termin 1 company-owned architecture.

```mermaid
flowchart LR
    Human[Sebastian\nAccountable human] --> GH[GitHub / Issues / commits]
    Human --> Gate[Human approval gate]

    QA[qa-test-agent\nLangGraph workflow] --> Tool[run_pytest_tool\nbounded pytest execution]
    QA --> LLM[LLM factory\nsrc.llm.factory]
    LLM --> Ollama[Ollama qwen3:4b]
    LLM -. optional .-> ICC[HAW ICC\nOpenAI-compatible endpoint]

    Tool --> Tests[pytest targets under tests/]
    QA --> Trace[evidence/session-01\nJSONL trace]
    Trace --> Cost[costs/usage.csv\ncourse credits]

    API[FastAPI app] --> DB[(PostgreSQL + pgvector)]
    Tests --> API
    API --> Health[/health and /db/health]
    DB --> Health

    Gate --> Decision[Delivery or escalation decision]
```

## Termin 1 design decisions

1. The first own agent is `qa-test-agent` in `src/agents/qa_test_agent.py`.
2. The real tool is `run_pytest_tool`, which executes a bounded pytest run only
   for targets below `tests/`.
3. LLM access goes through `src.llm.factory.get_chat_model`, so the agent can use
   either local Ollama or the HAW ICC configuration.
4. The agent returns structured Pydantic output with status, summary, pytest
   exit code, findings, and a human approval flag.
5. Error handling covers invalid test targets, missing files, and pytest timeout.
6. Local traces are written to `evidence/session-01/qa-test-agent-trace.jsonl`.
7. Usage and estimated course credits are recorded in `costs/usage.csv`.
8. Sebastian reviews QA output before it affects a delivery decision.

## Current limitations

- The Termin 1 agent supports QA evidence only; other roles are planned for later
  sessions.
- Token usage is recorded only when the selected provider returns usage metadata.
- GitHub Issues must exist in GitHub for final assessment; local issue drafts are
  documented in `docs/session-01-github-issues.md` if online creation is blocked.
