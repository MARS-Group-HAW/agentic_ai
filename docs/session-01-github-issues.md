# Session 01 GitHub Issue Drafts

Use these three issues if GitHub issue creation is not available from the local machine.

## Issue 1: Implement first team-owned QA LangGraph agent

Problem: Termin 1 requires at least one own LangGraph agent with a real tool, structured input/output, trace evidence, and error handling.

Acceptance criteria:
- Agent lives under `src/agents/`.
- Agent uses the shared LLM factory.
- Agent runs at least one real repository tool.
- Agent writes a local JSONL trace.
- At least one pytest outside `tests/starter/` covers it.

## Issue 2: Complete company and role model for Termin 1

Problem: The starter roles and company document still contain placeholders.

Acceptance criteria:
- All twelve roles have current and target actors.
- Each role has an accountable human.
- Human approval gates are explicit.
- The company mission, decision rule, escalation rule, and role-change rule are documented.

## Issue 3: Adapt architecture and usage evidence for Termin 1

Problem: The architecture document and cost usage file must reflect the real team-owned setup.

Acceptance criteria:
- Architecture includes the QA agent, pytest tool, LLM adapter, traces, cost path, FastAPI, and PostgreSQL.
- `costs/usage.csv` contains Termin 1 usage rows.
- Evidence under `evidence/session-01/` contains a team-owned trace.
