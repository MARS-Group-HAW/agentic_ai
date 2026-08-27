# Wahlpflichtprojekt Agentic AI

Course preparation repository for the **"Wahlpflichtprojekt Agentic AI"** elective (Bachelor
Informatik, HAW Hamburg, Prof. Dr. Thomas Clemen), running WS 2026/27. This repo holds the design
documents, student-facing course package, and supporting cluster infrastructure — it is planning
and ops material, not a software deliverable itself.

## The course, in short

Student teams of four each found a small **software company** that has to cover ten organizational
roles — Managing Director, Account Manager, Requirements Engineer, Project Manager, Architect,
Backend/Frontend Engineer, QA, DevOps, Security & Compliance — with only four humans available. The
company delegates the remaining roles to AI employees at a self-chosen trust level (from advisory
suggestions up to fully autonomous execution), builds a real customer product for a fictional
customer ("HarborFlow Logistics") over 12 weekly sessions, and runs its own **ERPNext** instance as
its company operating system. There is no grading — teams compete instead for awards such as *Best
Human-Agent Organization* or *Most Spectacular Agent Failure*.

## Repository structure

| Path | Contents |
|---|---|
| `agentic_software_company_challenge/` | The course package that ships: course spec, student handbook, customer RFP, role cards, templates, and the twelve weekly "Monday" briefings (released one per week during the semester). Start with `00_Course_Specification.md`; see `20_README.md` for the full index. |
| `WP_AgenticAI_Zusammenfassung.md`, `Agentic_AI_Wahlpflichtprojekt_Zusammenfassung.md` | German design-discussion history. Historical only — an earlier, differently-structured design considered along the way is not the one that shipped (see `agentic_software_company_challenge/` above for the current design). |
| `ICC - vLLM/` | Kubernetes manifests and setup docs (German) for a self-hosted LLM service (Qwen2.5 via vLLM, fronted by a LiteLLM proxy issuing per-student API keys) on HAW's ICC compute cluster. Deployed and in use. |
| `ICC - ERPNext/` | Draft deployment plan for per-company ERPNext instances on the same cluster — one shared Frappe bench, one isolated site per company. **Not yet deployed**; open items are listed in the plan itself. |
| `Projekt Agentic AI - CLM_de.pdf` / `.pptx` | Slide deck. |

## Status

The course design is settled (software-company format, ERPNext-based, ungraded). Remaining open
items — splitting ~17 students into teams of 4, the ERPNext infrastructure build-out, and a few
date/semester labels that still need unifying across documents — are tracked in `CLAUDE.md`.

## A note on `ICC - vLLM/`

That folder contains real operational data from setting up the LLM service (API keys, a couple of
infrastructure credentials, and a student roster). Treat it as sensitive, not as example/placeholder
content, when sharing or reusing anything from it.

## License

MIT — see [LICENSE](LICENSE).
