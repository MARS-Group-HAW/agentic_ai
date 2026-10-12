# Architecture – initial course baseline

> Team-owned after Session 1. Adapt this document so that it reflects the real company infrastructure.

```mermaid
flowchart LR
    subgraph Humans ["Human Team Members (Accountable Roles)"]
        H_Roles["Yaw (MD/Customer/Data), Saad (PO/Int),<br/>Felix (PM/QA), Minh (Arch/Cost),<br/>Mirko (Backend/Safety), Muhammad (Agent/DevOps)"]
    end

    Humans --> GH["GitHub / Issues / PRs"]

    subgraph Agents ["Team Agents (LangGraph + LangChain)"]
        DataAgent["data-agent\n(Data & RAG Engineer)\n[Primary Initial Agent]"]
        OtherAgents["Other Role Agents\n(bae-agent, sa-agent, test-agent, etc.)"]
    end

    Agents --> GH
    GH --> CI["GitHub Actions"]
    CI --> Tests["pytest"]
    
    %% Human Approval Gate vor Deployment
    CI --> HumanGate{"Human Gate\n(Approval required\nbefore deployment)"}
    HumanGate --> Deploy["Deployment / Produktion"]

    %% Eskalationspfad bei Fehlern/Kritischem
    Agents -.->|"Escalation:\nShutdown, Report & Rollback"| Humans

    API["FastAPI"] --> DB[("(PostgreSQL + pgvector)")]
    DataAgent --> API
    Agents --> LLM{"LLM adapter"}
    LLM --> Ollama["Native Ollama"]
    LLM --> ICC["HAW ICC\nOpenAI-compatible endpoint"]

    Agents --> Trace["Local JSONL traces"]
    Trace --> Cost["Cost analysis\n(Cost spike: less credits,\nmore human effort)"]

    LangSmith["LangSmith\n(optional / approval required)"]
    Agents -. optional .-> LangSmith
```

## Baseline design decisions

1. Agent orchestration uses LangGraph.
2. LangChain provides model/integration abstractions.
3. Team code must not depend directly on a specific LLM deployment.
4. PostgreSQL + pgvector is the common relational and vector data platform.
5. Local structured traces are mandatory project evidence.
6. LangSmith is optional and cannot replace local evidence.
7. Ollama normally runs natively on the host when used on macOS.

## Team changes

Document all material changes here and add ADRs where appropriate.
