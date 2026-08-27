# HarborFlow Logistics GmbH

## Request for Proposal — HF-RFP-2026-01

### Project: Operations Service Portal

## 1. Customer Background

HarborFlow Logistics GmbH is a medium-sized logistics service provider. Operational customer requests are currently handled mainly through email, telephone calls and spreadsheets.

This causes increasing problems with transparency, ownership and traceability.

## 2. Project Goal

HarborFlow wants a web-based **Operations Service Portal**.

Customers and HarborFlow employees should be able to create, process and track operational service requests.

## 3. Example Requests

### Transport Request
8 pallets must be transported from Hamburg to Bremen at short notice.

### Delivery Problem
Shipment HF-29881 has not been delivered.

### Complaint
Two boxes were damaged during transport.

### Special Transport
A temperature-controlled transport is required.

## 4. Core Object: Service Request

Each service request must contain at least:

- ID
- Customer
- Title
- Description
- Category
- Priority
- Status
- Assigned Employee
- Created timestamp
- Updated timestamp
- Comments

## 5. Minimum Workflow

```text
NEW
 ↓
ASSIGNED
 ↓
IN_PROGRESS
 ↓
RESOLVED
 ↓
CLOSED
```

Optional states may include `WAITING_FOR_CUSTOMER`.

## 6. MVP Requirements

### MUST

- Login
- User management
- Customers
- Service requests
- Categories
- Priorities
- Assignment
- Status changes
- Comments
- Search
- Filters
- Audit trail
- REST API
- Automated tests
- Reproducible deployment

### SHOULD

- Attachments
- Dashboard
- Notifications
- Export
- Import

### COULD

- SLA monitoring
- Customer portal
- Reporting
- API integration
- Automatic classification

## 7. Customer Roles

### Customer User
May create and view own requests.

### Service Employee
May process assigned requests.

### Service Manager
May assign and prioritize requests.

### Administrator
May manage users and system configuration.

## 8. Technical Constraints

Recommended stack:

- Python
- FastAPI
- PostgreSQL
- REST
- Docker
- GitHub

Teams may choose an appropriate frontend technology.

## 9. Non-Functional Requirements

The system should be:

- understandable;
- maintainable;
- testable;
- traceable;
- reproducibly deployable.

Security-relevant design decisions must be documented.

## 10. Intentionally Open Questions

The customer has not specified everything.

Examples:

- May all employees of a customer see all company requests?
- Who may close a request?
- What exactly means `Critical` priority?
- Must deleted information remain visible in the audit trail?
- How long must information be retained?
- Does a customer need multiple locations?

Missing requirements must be clarified. Agents must not silently invent requirements.

## 11. Minimum Acceptance Scenario

```text
Customer creates request
        ↓
Service Manager assigns request
        ↓
Employee processes request
        ↓
Resolution is recorded
        ↓
Request is closed
```
