# Company Repository Structure

Recommended structure:

```text
agentic-company/
│
├── README.md
│
├── product/
│   ├── backend/
│   ├── frontend/
│   ├── tests/
│   └── docker/
│
├── agents/
│   ├── common/
│   ├── architect/
│   │   ├── charter.yaml
│   │   ├── agent.py
│   │   └── prompts/
│   ├── qa/
│   ├── project_manager/
│   └── ...
│
├── integrations/
│   ├── erpnext/
│   ├── github/
│   └── llm/
│
├── organization/
│   ├── org-chart.md
│   ├── roles.md
│   ├── decision-rights.md
│   └── employees/
│
├── decisions/
│   ├── DEC-001.md
│   ├── DEC-002.md
│   └── ...
│
├── evaluation/
│   ├── experiments/
│   ├── metrics/
│   └── results/
│
├── docs/
│   ├── architecture/
│   ├── requirements/
│   └── operations/
│
├── scripts/
├── docker-compose.yml
├── .env.example
└── requirements.txt
```

## Storage Principle

Use ERPNext for operational company data and agent runs.

Use GitHub for:

- source code;
- important technical decisions;
- selected experiment traces;
- reproducible evaluation results.

Do not commit large raw agent logs to Git unless they are required as evidence for a specific experiment.
