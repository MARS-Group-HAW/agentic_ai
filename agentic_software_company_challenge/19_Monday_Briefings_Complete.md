# Monday Briefings — Complete Collection

# Monday 1 — Found the Company

## Theme

Organization, roles and first AI employees

## 10:00 — CEO Briefing

Today you do not form a project group. You found a software company.

Your company has four human employees but must cover ten organizational functions.

## Mission

By 16:00 your company must exist as an identifiable organization with an initial human-agent workforce.

## Tasks

### 1. Found the Company

Define:

- company name;
- short mission statement;
- four founders;
- initial organization.

### 2. Cover the Ten Functions

Decide which functions are covered by:

- humans;
- AI employees;
- mixed roles.

### 3. Create an Organization Chart

Store it under:

`organization/org-chart.md`

### 4. ERPNext Mini-Challenge

Complete:

1. Find your company/customer.
2. Open a project.
3. Create a task.
4. Assign a task.
5. Create an issue.
6. Change a status.

### 5. Micro Lecture

**What makes an AI agent an organizational employee?**

Focus:

- goal;
- state;
- tools;
- authority;
- feedback;
- accountability.

### 6. Design the Initial Digital Workforce

Create at least four AI Employee Charters.

### 7. Implement One First Agent

Recommended starting roles:

- QA Agent
- Requirements Agent

The agent does not need to be sophisticated, but it must perform one real task.

## Evidence Required at 15:40

- organization chart;
- four AI Employee Charters;
- one working agent;
- Decision DEC-001: Why did you assign these functions to humans and agents?

## End-of-Day Question

Which part of your initial organization do you currently trust least?

---

# Monday 2 — Win the Contract

## Theme

Requirements engineering and delegation

## 10:00 — Customer Briefing

HarborFlow Logistics GmbH publishes RFP HF-RFP-2026-01 for an Operations Service Portal.

## Mission

Understand the customer problem well enough to create an initial project plan and backlog.

## Tasks

### 1. Analyse the RFP

Identify:

- explicit requirements;
- ambiguous requirements;
- missing information;
- assumptions that must not be made silently.

### 2. Use an AI Employee

At least one meaningful part of requirements analysis must be delegated to an AI employee.

### 3. Customer Clarification

Prepare a maximum of ten high-value clarification questions.

### 4. Build the Product Backlog

Create:

- epics;
- user stories or tasks;
- acceptance criteria;
- priorities.

### 5. Initial Architecture Thinking

Create a first high-level architecture sketch.

### 6. Revisit Your Organization

Does the organization designed last week fit the contract?

If not, reorganize.

## Micro Lecture

**Delegation under uncertainty**

Focus:

- asking vs assuming;
- acceptance criteria;
- confidence;
- escalation;
- decomposition.

## Evidence Required

- requirements backlog;
- clarification questions;
- list of agent-generated findings;
- list of agent mistakes or questionable assumptions;
- updated organization chart if necessary;
- one company decision if the organization changed.

## End-of-Day Question

What did your requirements agent miss that a human noticed?

---

# Monday 3 — Build the Digital Workforce

## Theme

Tool-using agents, permissions and structured outputs

## Mission

Turn planned AI roles into operational employees that can work with company systems.

## Technical Goal

At least two AI employees must perform real tasks using tools.

## Tasks

### 1. Connect Agents to ERPNext

At least one agent must be able to:

- read project information;
- read tasks;
- create or update an allowed business object.

### 2. Connect Agents to GitHub or the Codebase

At least one agent must be able to inspect technical artifacts.

### 3. Define Structured Outputs

Avoid free-form output where machine-readable results are useful.

### 4. Implement Permission Boundaries

Document what each agent can and cannot do.

### 5. Implement Escalation

At least one agent must detect a condition that triggers escalation to a human.

### 6. Test Failure Cases

Test at least:

- missing information;
- invalid tool result;
- ambiguous task;
- forbidden action.

## Micro Lecture

**Tools, permissions and agent control loops**

Focus:

- tool calling;
- structured state;
- permissions;
- error handling;
- escalation.

## Evidence Required

- two operational agents;
- agent charters;
- one successful tool trace per agent;
- one failed or escalated trace;
- permission matrix.

## End-of-Day Question

Which permission would be dangerous to grant your current agent today?

---

# Monday 4 — MVP Sprint

## Theme

Human-agent handoffs and first serious product development

## Mission

Deliver the first usable vertical slice of the HarborFlow Operations Service Portal.

## Required Collaboration Patterns

Demonstrate at least one:

```text
Human → Agent → Human
```

and one:

```text
Agent → Agent
```

workflow.

## Recommended Vertical Slice

Customer creates a service request and a service employee can view and process it.

## Tasks

### Product

Implement an end-to-end slice including:

- persistence;
- API;
- basic UI or API consumer;
- test coverage.

### Organization

Route at least two real development tasks through your agent organization.

### Quality

Use a QA role to verify acceptance criteria.

### Traceability

Record where humans intervened and why.

## Micro Lecture

**Handoffs in mixed teams**

Focus:

- task contracts;
- context transfer;
- review;
- ownership;
- feedback loops.

## Evidence Required

- working vertical slice;
- one human-agent-human trace;
- one agent-agent trace;
- QA evidence;
- human intervention notes.

## End-of-Day Question

Where did coordination cost more than doing the task directly?

---

# Monday 5 — Growth and Competing Priorities

## Theme

Task allocation and prioritization

## 10:00 — Customer Event

HarborFlow is satisfied with progress and adds a new requirement:

> Historical service requests must be importable from CSV.

At the same time, three critical defects have been reported in the current MVP.

## Mission

Handle feature development and urgent defects without losing organizational control.

## Tasks

### 1. Triage

Prioritize:

- three critical bugs;
- CSV import;
- unfinished MVP work.

### 2. Allocate Work

Decide explicitly which tasks go to:

- humans;
- specialized agents;
- mixed teams.

### 3. Compare Two Allocation Strategies

For at least two similar tasks, try different allocation strategies.

Example:

- Human developer
- Developer agent + human reviewer

### 4. Measure Rework

Track tasks that required rework after agent completion.

## Micro Lecture

**Task allocation in human-agent teams**

Focus:

- capability matching;
- urgency;
- cost of coordination;
- reliability;
- parallelism.

## Evidence Required

- prioritized backlog;
- allocation rationale;
- first simple comparison of human vs agent task handling;
- defects fixed or clearly escalated;
- CSV import progress.

## End-of-Day Question

Which task type should no longer be assigned to one of your current agents?

---

# Monday 6 — Customer Review / Board Meeting

## Theme

Evidence-based organizational review

## Purpose

This is a management review, not a conventional presentation.

Each company receives approximately 15 minutes.

## 1. Product Demo — 5 Minutes

Show the current HarborFlow product.

## 2. Organization Review — 5 Minutes

Explain:

- current human-agent organization;
- which agents work well;
- which agents do not;
- where humans intervene;
- major organizational changes so far.

## 3. Evidence — 5 Minutes

Show selected metrics:

- human effort;
- agent runs;
- task acceptance;
- rework;
- defects;
- overrides;
- escalations.

## Board Questions

Be prepared to answer:

1. Which AI employee currently creates the most value?
2. Which employee creates the most risk?
3. Where is human supervision mandatory?
4. Which role would you redesign today?
5. Are you using too many or too few agents?

## Reorganization Window

After the review you may:

- promote agents;
- reduce trust;
- remove agents;
- combine roles;
- split roles;
- redesign workflows.

## Required Evidence

- current product demo;
- current org chart;
- selected metrics;
- at least one explicit reorganization decision.

---

# Monday 7 — Autonomous Company Day

## Theme

Resilience and loss of human expertise

## Important

This day is designed to run without instructor intervention.

## 10:00 — CEO Briefing

Your human Technical Lead is unavailable today.

The person who normally fulfills this responsibility may participate only as an observer and may not perform Technical Lead tasks.

## Situation

A customer issue requires a technical decision before development can continue.

## Mission

Keep the company operational despite temporary loss of a key human role.

## Tasks

### 1. Identify the Capability Gap

What knowledge or authority has become unavailable?

### 2. Reassign Responsibilities

Choose among:

- another human;
- existing agent;
- new temporary agent;
- mixed backup role.

### 3. Resolve the Technical Decision

Document:

- available evidence;
- decision maker;
- confidence;
- escalation path.

### 4. Continue Product Work

Do not turn the entire day into an organization workshop. Deliver real product progress.

### 5. Review the Incident

At the end of the day assess whether the company was resilient.

## Evidence Required

- temporary organization chart;
- technical decision;
- agent/human trace;
- product progress;
- short resilience retrospective.

## End-of-Day Question

Could your company operate for one week without its strongest human expert?

---

# Monday 8 — Second Customer

## Theme

Multi-project coordination and organizational scaling

## 10:00 — New Business Event

A second customer signs a small contract.

# Baltic Components GmbH

## Project

Build a small web application for recording and approving supplier disruptions.

## Minimum Requirements

- suppliers;
- disruption reports;
- severity;
- responsible employee;
- approval status;
- comments;
- simple dashboard;
- REST API;
- deployment.

## Mission

Operate two customer projects in parallel while continuing support for HarborFlow.

## Tasks

### 1. Create the Second Project in ERPNext

### 2. Allocate Capacity

Decide how humans and agents are divided across both projects.

### 3. Reuse vs Specialize

Decide whether existing agents can work for both customers or whether new specialization is needed.

### 4. Project Management Experiment

If possible, delegate part of cross-project coordination to a Project Manager Agent.

### 5. Avoid Customer Context Leakage

Ensure customer information and task context remain properly separated.

## Micro Lecture

**Scaling agentic organizations**

Focus:

- shared vs specialized agents;
- multi-project memory;
- task queues;
- context boundaries;
- resource contention.

## Evidence Required

- second project backlog;
- capacity allocation;
- organization update;
- evidence of one cross-project coordination mechanism;
- product progress on both projects.

## End-of-Day Question

Which roles scale across projects and which should stay customer-specific?

---

# Monday 9 — Security Incident

## Theme

Trust, permissions, accountability and incident response

## 10:00 — Incident Notice

A development agent has committed a secret to a repository.

In addition, another AI employee recommended a third-party dependency without checking its security status or license compatibility.

## Mission

Contain the incident, determine the organizational cause and redesign controls.

## Tasks

### 1. Incident Containment

Address the exposed secret.

### 2. Trace the Decision Chain

Determine:

- which employee acted;
- which permissions were available;
- which review step failed;
- whether a human was expected to intervene.

### 3. Dependency Review

Assess the proposed dependency for:

- security risk;
- license compatibility;
- maintenance status;
- necessity.

### 4. Reassess Trust

Adjust trust levels where appropriate.

### 5. Redesign Permissions

Apply least privilege where feasible.

### 6. Add Preventive Controls

Examples:

- secret scanning;
- protected branches;
- approval gates;
- dependency checks;
- restricted tool permissions.

## Micro Lecture

**Agent safety as organizational design**

Focus:

- least privilege;
- approval boundaries;
- accountability;
- auditability;
- recovery.

## Evidence Required

- incident report;
- root cause analysis;
- changed permission model;
- changed trust level if justified;
- preventive control implemented.

## End-of-Day Question

Was this primarily an agent failure or an organizational design failure?

---

# Monday 10 — Autonomous Enterprise

## Theme

End-to-end agentic business processes

## Mission

Automate one business or engineering process that has previously required substantial human coordination.

## Candidate Processes

- Issue triage
- Requirement intake
- Bug reproduction
- Task decomposition
- Pull request quality review
- Release preparation
- Customer request classification

## Minimum Requirement

The process must include:

```text
Event
  ↓
Agent decision
  ↓
Tool action
  ↓
Next employee or agent
  ↓
Recorded outcome
```

## Tasks

### 1. Select the Process

Choose a process with clear boundaries and measurable outcome.

### 2. Define Authority

Which decisions are autonomous and which require approval?

### 3. Implement the Workflow

Prefer event-driven integration where appropriate.

### 4. Add Human Override

A human must be able to interrupt or reverse the process safely.

### 5. Test Exceptional Cases

At least three failure or edge cases.

### 6. Measure the Process

Collect:

- completion time;
- human intervention;
- agent runs;
- failures;
- rework.

## Micro Lecture

**From tool-using agent to agentic process**

Focus:

- event-driven workflows;
- orchestration;
- autonomy boundaries;
- observability;
- rollback.

## Evidence Required

- process diagram;
- working implementation;
- permission model;
- human override;
- three exception tests;
- initial metrics.

## End-of-Day Question

Would you trust this process to run overnight without a human watching it?

---

# Monday 11 — Science Day

## Theme

Empirical evaluation of human-agent collaboration

## Rule for Today

Do not prioritize new product features.

Today your company becomes an experimental laboratory.

## Mission

Produce evidence about where your agents help, hurt or change work.

## Required Experiments

Run at least two controlled comparisons.

## Example Experiment A — QA

Compare:

- Human QA
- QA Agent

Use comparable test material.

Possible metrics:

- real bugs found;
- false positives;
- time;
- human supervision;
- agent compute.

## Example Experiment B — Development

Compare:

- Human developer
- Developer Agent + Human Reviewer

Possible metrics:

- completion time;
- accepted output;
- rework;
- defects;
- review effort;
- tokens.

## Example Experiment C — Project Management

Compare:

- human task decomposition;
- PM Agent task decomposition.

Evaluate:

- completeness;
- dependency correctness;
- number of clarifications;
- downstream rework.

## Experimental Requirements

For each experiment document:

1. Question
2. Setup
3. Compared conditions
4. Metrics
5. Results
6. Interpretation
7. Limitations

## Micro Lecture

**Evaluating agents without fooling yourself**

Focus:

- controlled comparisons;
- repeatability;
- task selection bias;
- failure rates;
- human effort;
- non-determinism.

## Evidence Required

- two completed experiments;
- raw or summarized measurements;
- results table or visualization;
- interpretation;
- organizational recommendation based on evidence.

## End-of-Day Question

Which belief about your agents changed because of data today?

---

# Monday 12 — Annual General Meeting

## Theme

Customer acceptance and organizational learning

## Morning — Final Customer Acceptance

Demonstrate the HarborFlow Operations Service Portal.

The customer will evaluate:

- core requirements;
- usability;
- reliability;
- traceability;
- testing;
- deployment;
- documentation.

If possible, also show the Baltic Components project.

## Afternoon — Company Retrospective

This is not a conventional final presentation.

Each company should answer five questions.

### 1. What organization did you end up with?

Show the final human-agent organization.

### 2. Where were agents better than humans?

Use evidence.

### 3. Where were humans better than agents?

Use evidence.

### 4. Which AI employee was your most valuable employee?

Explain why.

### 5. If you founded the company again, what would you change?

Describe your preferred future human-agent organization.

## Final Evidence

Submit:

- final org chart;
- final AI employee list;
- selected metrics;
- two evaluation results;
- major company decisions;
- final product state;
- one-page retrospective.

## Optional Awards

- Best Software Product
- Best Human-Agent Organization
- Most Autonomous Company
- Best Evidence-Based Evaluation
- Best Recovery from Failure
- Most Spectacular Agent Failure

## Final Reflection

> The goal was not to prove that agents are better than humans. The goal was to learn how to design an organization in which both can contribute effectively.

---

