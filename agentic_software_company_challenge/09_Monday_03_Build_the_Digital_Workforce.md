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
