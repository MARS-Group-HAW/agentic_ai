# Company

## Name

Harbor QA Agents

## Mission

Harbor QA Agents builds small, auditable agent workflows for software teams. The
company focuses on quality checks, reproducible evidence, and clear human
responsibility before any result is used for delivery decisions.

## Team members

- Sebastian: accountable human for Termin 1 setup, QA approval, and delivery
  decisions.

## Working rules

- Technical decisions are made by Sebastian after reviewing agent evidence,
  tests, and repository impact.
- Human approval is mandatory for customer communication, architecture changes,
  security-relevant decisions, failed test results, and any generated artifact
  that affects delivery.
- Agents may read repository files, run approved local tools, and write local
  evidence files. They may not change secrets, bypass tests, or publish results
  without review.
- Incidents are escalated to Sebastian when an agent returns `error`,
  `needs_review`, unexpected tool output, missing trace data, or cost growth
  that is not explained by the task.
- Cost overruns are handled by stopping repeated runs, documenting the cause in
  the usage file, and reducing scope before another execution.

## Pflichtentscheidungen Termin 1

1. The first technically supported role is QA & Test Engineer, because it can
   use a safe real tool (`pytest`) and produces objective evidence.
2. Managing Director / Customer Lead remains human-first, because customer
   commitments and prioritization require explicit accountability.
3. A Human Approval Gate is required after every QA agent run before the result
   is used for a delivery decision, especially for failed or ambiguous tests.
