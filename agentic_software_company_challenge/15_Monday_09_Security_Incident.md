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
