# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository purpose

This repo exists to support Prof. Dr. Thomas Clemen in **preparing and running** the "Wahlpflichtprojekt
Agentic AI" elective at HAW Hamburg's Faculty of CS — it is planning material, not a deliverable
itself. It holds two unrelated bodies of content — treat them independently:

1. **Course design and content** (repo root + `agentic_software_company_challenge/`) — design
   documents, briefings, and templates for "Wahlpflichtprojekt Agentic AI" (Bachelor Informatik, HAW
   Hamburg, Prof. Dr. Thomas Clemen). No build system, package manifest, or test suite; all content
   is Markdown (plus a PDF/PPTX slide deck). Treat tasks here as editing/authoring documentation, not
   writing or running code.
2. **`ICC - vLLM/`** — Kubernetes/deployment material for a self-hosted LLM service on HAW's ICC
   compute cluster, used to give students API access to an open-weight model. This is ops
   config (YAML manifests, a couple of Python scripts, setup docs), unrelated to the course-design
   content above. See its own section below.
3. **`ICC - ERPNext/`** — deployment *plan* (not yet executed) for the per-company ERPNext instances
   the course design requires. Same ICC cluster as above, but an unrelated deployment (no GPU, own
   namespace). See its own section below.

## Course design content

**Decided (2026-08-27): the course runs the software-company idea** —
`agentic_software_company_challenge/` (10 mandatory company roles, ERPNext as company OS, **no
grading**) — as-is, for WS 2026/27. Treat this as settled; do not re-open it.

- `README.md` — placeholder, one line.
- `WP_AgenticAI_Zusammenfassung.md` — **superseded / historical only.** Describes a different,
  not-adopted design (4 selectable tracks, a graded individual Hausarbeit, a Bewertungsraster) that
  conflicts with the decision above. Don't treat anything in it as current, and don't resurface that
  conflict — it's resolved.
- `Agentic_AI_Wahlpflichtprojekt_Zusammenfassung.md` — earlier brainstorm document (concept
  discussion history) that already converges on the same software-company/no-grading idea that was
  adopted; historical context only, not a source of open decisions.
- `agentic_software_company_challenge/` — **the course package that ships**, as a sequence of
  numbered Markdown files meant to be read/released in order:
  - `00`–`06`: core documents (course spec, student handbook, customer RFP, role cards, AI employee
    charter template, repo structure, decision log template). These can be published to students at
    the start of the semester.
  - `07`–`18`: the twelve weekly ("Monday") briefings, `01_Found_the_Company` through
    `12_Annual_General_Meeting`. **These are meant to be released one per week** — do not treat them
    as already-known-to-students content when drafting related material, since later weeks' events
    are intentionally hidden from the student teams until each corresponding Monday.
  - `19_Monday_Briefings_Complete.md`: all twelve weekly briefings concatenated into one file.
  - `20_README.md`: index/manifest for this subfolder — update it if files are added, renamed, or
    reordered here.

### Planning constraints for the run this content targets

- Per `00_Course_Specification.md`: 12 Mondays, 10:00–16:00 (6h/session), fixed team size of **4**
  students per company.
- Current cohort planning figure is **~17 students** (mixed German/international) — this doesn't
  divide evenly into teams of 4 (4 teams of 4 + 1 leftover). This isn't resolved in any doc yet;
  needs an explicit decision (extra team of 5, floater, or adjust admission count) before rollout.
- **No grading is a deliberate, confirmed choice** (`01_Student_Company_Handbook.md`: "There is no
  grade") — not an open question. Don't propose reconciling it with graded-assessment models from
  the superseded docs above.
- **ERPNext hosting**: a deployment *plan* now exists (`ICC - ERPNext/erpnext-deployment-plan.md`) —
  one shared Frappe bench with a separate site per company, matching `01_Student_Company_Handbook.md`
  ("its own ERPNext instance") for blast-radius isolation without running 4–5 fully separate stacks.
  **Not yet executed** — several items are explicitly unresolved in that doc (RWX/CephFS storage
  class availability on ICC is the blocking one; also Helm permissions, exact frappe_docker image
  tags/commands, DNS, and a new resource quota). See that file's "Offene Punkte" section before
  building.

### Working conventions (course content)

- **Language:** primary design/summary docs are in German; the course package
  (`agentic_software_company_challenge/`) is in English (it's student-facing, English is the course's
  working language). Match the existing language of whatever file you're editing.
- **Numbered filenames encode reading/release order** in `agentic_software_company_challenge/` —
  preserve the `NN_` prefix scheme when adding or reordering files, and update `20_README.md`'s
  listing to match.
- **Known inconsistency to watch for:** date/semester labels across documents are not yet unified
  (e.g. some drafts reference SS 2026 while the practicum is designed for WS 2026/27, and a
  deadline of Aug 16, 2026 appears in one place). Don't propagate a specific date/semester into new
  content without checking it against the current source doc first.
- **No Mode-A/Mode-B experiment in this design.** The binary "Full-Agentic vs. Mixed Team" split only
  exists in the superseded docs above. `agentic_software_company_challenge/` instead uses one
  continuous 12-week company narrative per team, with autonomy dialed per role via the 5-level trust
  scale (Advisory → Autonomous, see `01_Student_Company_Handbook.md`). Don't introduce an A/B split
  when drafting related material — each company needs one persistent state, not two parallel runs.

## `ICC - vLLM/` (cluster infra, unrelated to the course content above)

Deploys a self-hosted, OpenAI-API-compatible LLM service (Qwen2.5, via vLLM) on HAW's ICC Kubernetes
cluster, fronted by a LiteLLM proxy that issues per-student API keys, plus n8n and Qdrant for
workflow/vector-store experimentation. `myNotes.md` (German) is the author's running scratch log of
the setup; `final/vllm-litellm-setup.md` is the cleaned-up step-by-step build doc; `final/
llm-service-fuer-studierende.md` is the student-facing usage guide for the resulting
`https://llm.inf.haw-hamburg.de` endpoint.

- Deployment order (each step's YAML is applied with `kubectl apply -f <file> -n inf-vllm`, waiting
  for `kubectl get pods -n inf-vllm` to show `Running` before continuing): PVC for model weights →
  HuggingFace token secret → model-download init job (`download-qwen25-*.yaml`) → vLLM deployment
  (`04-vllm.yaml` / `final/vllm-qwen25-7b.yaml`) → PostgreSQL for LiteLLM (`litellm-postgres.yaml`) →
  LiteLLM master-key secret → LiteLLM proxy (`litellm.yaml`) → ingress with HTTPS
  (`final/ingress.yaml`) → per-student key generation (`final/rbac-students.yaml`,
  `final/bulk_key_gen.py` reads `students*.csv` and calls the LiteLLM `/key/generate` API).
  `final/vllm-litellm-setup.md` is the authoritative walkthrough, including a troubleshooting
  section and two cleanup variants (selective vs. full teardown).
  `01-n8n-postgres.yaml`/`02-n8n.yaml`/`03-qdrant.yaml` are auxiliary services (workflow automation,
  vector store), independent of the vLLM/LiteLLM chain.
- `final/` holds the current, cleaned-up version of each config/doc; `old/` (both at the top level
  and inside `final/`) holds superseded drafts kept for reference only — don't edit them, and prefer
  the `final/` version when the two overlap (e.g. `vllm-litellm-setup.md` exists in both).
- **Hardware ceiling — read before proposing a different model:** the ICC cluster's GPUs are Tesla
  **V100 (16GB) / V100S (32GB)**, Compute Capability 7.0. The current deployment is pinned to
  `vllm/vllm-openai:v0.7.3` because *newer vLLM releases dropped CUDA kernels for V100 entirely* —
  this caps not just which model fits, but which vLLM version (and therefore which models it
  supports) can run here at all. Current model is Qwen2.5-7B, FP16, `--max-model-len=8192` (kept low
  for lack of FlashAttention2 support on V100). A `download-qwen25-14b.yaml` job exists but isn't
  wired into a deployment yet — 14B in FP16 (~28GB weights) is marginal on a 32GB card once KV cache
  is added; would need testing or quantization (AWQ/GPTQ). Large MoE models (e.g. Kimi K2-class,
  ~1T params / 32B active, realistically needing 8×H100/H200) are **not feasible** to self-host on
  this cluster regardless of the vLLM-version constraint.
- **Sensitive data is committed in this directory** — treat as live, not placeholder: `myNotes.md`
  contains plaintext secrets (a HuggingFace token, a PostgreSQL password, a LiteLLM master key),
  `04-vllm.yaml` has a separate plaintext HuggingFace token in its Secret manifest, and
  `students*.csv` / `final/old/keys.csv` contain real student names, emails, Matrikelnummern, and
  issued API keys. Don't paste, echo, or otherwise surface the contents of these specific files in
  full, and don't reuse the embedded credentials as if they were placeholders.

## `ICC - ERPNext/` (planned cluster infra, not yet deployed)

Contains `erpnext-deployment-plan.md`: a **draft plan** (German, matching the vLLM docs' language)
for hosting the per-company ERPNext instances the course design requires — one shared Frappe bench,
one isolated **site** per company (own DB, own subdomain, own admin login), reusing the same
manifest style as `ICC - vLLM/` (`rook-ceph-block` for block storage, `cert-manager` +
`letsencrypt-production` + nginx ingress). Unlike vLLM, this workload needs a **ReadWriteMany**
volume for the shared `sites/` directory (multiple Frappe pods — web, socketio, scheduler, workers —
all mount it at once); `rook-ceph-block` is RWO-only and won't work here, so confirming an RWX/CephFS
storage class with ICC is the first blocking step. The doc marks every unverified specific (image
tags, exact bench commands, RWX storage class name) with ⚠️ — treat those as placeholders to check
against current [frappe_docker](https://github.com/frappe/frappe_docker) docs before applying
anything, not as confirmed values. Nothing in this folder has been run against the real cluster yet.
