# Student Company Handbook

## Your Mission

You are four founders of a new software company.

Your company develops software for customers. Unlike a conventional software firm, your organization consists of both humans and AI employees.

> Your main challenge is to discover which tasks should be performed by humans, which by agents, and which by mixed human-agent teams.

## Starting Conditions

Your company receives:

- 4 human employees;
- its own ERPNext instance;
- a GitHub repository;
- access to a local LLM;
- an agent runtime;
- a first customer;
- a customer project.

You may create as many AI employees as you consider useful. More agents are not automatically better: each agent creates development, compute, coordination and supervision costs.

## Required Company Functions

Your company must cover these ten functions:

| Function | Responsibility |
|---|---|
| Managing Director | Overall company leadership |
| Account Manager | Customer communication |
| Requirements Engineer / Product Owner | Requirements and acceptance criteria |
| Project Manager | Planning and coordination |
| Software Architect | Technical coherence |
| Backend Engineer | Backend implementation |
| Frontend Engineer | User interface |
| QA Engineer | Quality assurance |
| DevOps Engineer | Build, deployment and operation |
| Security & Compliance Officer | Security, permissions and compliance |

A human or agent may cover several functions. A function can also be designed as a mixed role.

## What Counts as an AI Employee?

An AI employee must have:

1. Identity
2. Role
3. Mission
4. Capabilities
5. Tools
6. Authority
7. Escalation rules
8. Traceability

A one-off LLM prompt does not count as an AI employee.

## Trust Levels

### Trust 1 — Advisory
Agent may propose actions.

### Trust 2 — Assisted
Agent may read systems and generate structured outputs.

### Trust 3 — Operational
Agent may create tasks, issues or other bounded business objects.

### Trust 4 — Delegated
Agent may perform defined changes independently.

### Trust 5 — Autonomous
Agent may complete a bounded process end-to-end.

Trust must be justified with evidence and may be reduced at any time.

## Mandatory Collaboration Patterns

During the project, your company must demonstrate at least:

- one Human → Agent → Human workflow;
- one Agent → Agent workflow;
- one workflow triggered by a business event or system event.

## Shared Systems

### ERPNext
Use for:

- customers;
- projects;
- tasks;
- issues;
- employees;
- decisions;
- escalations;
- company-level evidence.

### GitHub
Use for:

- source code;
- technical issues;
- pull requests;
- CI/CD;
- tests;
- releases.

## Experimentation

You may:

- hire new AI employees;
- remove agents;
- redesign roles;
- add or remove supervisors;
- specialize agents;
- combine agents;
- move responsibilities back to humans;
- change trust levels.

Interesting failure is a valid outcome if you can explain it with evidence.

## Company Decision Log

For important organizational changes, document:

```text
Decision:
Date:

Situation:

Decision:

Made by:
[Human / Agent / Human-Agent Team]

Reason:

Expected outcome:

Actual outcome:

Lesson learned:
```

## Metrics

Track at least:

### Human
- Human effort
- Human intervention time
- Review time

### Agent
- Agent runs
- Tool calls
- Tokens / compute
- Failed tasks
- Rework

### Product
- Features
- Defects
- Tests
- Acceptance criteria

### Organization
- Escalations
- Agent task acceptance
- Human overrides

## No Grading

There is no grade. The course is an experimentation environment.

Possible final awards include:

- Best Software Product
- Best Human-Agent Organization
- Most Autonomous Company
- Best Evidence-Based Evaluation
- Best Recovery from Failure
- Most Spectacular Agent Failure
