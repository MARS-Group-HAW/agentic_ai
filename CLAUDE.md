# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository purpose

This is a **course design and content repository**, not a software project. It holds the design
documents, briefings, and templates for "Wahlpflichtprojekt Agentic AI" (Bachelor Informatik, HAW
Hamburg, Prof. Dr. Thomas Clemen). There is no build system, package manifest, source code, or test
suite here — all content is Markdown (plus a PDF/PPTX slide deck). Treat tasks in this repo as
editing/authoring documentation, not writing or running code.

## Document map

- `README.md` — placeholder, one line.
- `WP_AgenticAI_Zusammenfassung.md` — German summary of the course's current design state: guiding
  idea, the A/B experiment, the four project tracks, open decisions, and status of the three
  deliverable documents (Praktikums-Aufgabenstellung, Hausarbeits-Aufgabenstellung,
  Bewertungsraster). Read this first to understand what has been decided vs. still open.
- `Agentic_AI_Wahlpflichtprojekt_Zusammenfassung.md` — longer/earlier working document covering the
  same project (concept discussion history).
- `agentic_software_company_challenge/` — the actual course package, one specific track scenario
  ("Agentic Software Company Challenge" / "HarborFlow"), as a sequence of numbered Markdown files
  meant to be read/released in order:
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

## Working conventions

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
- **Two-mode (A/B) experiment** is the connecting structure across the whole course: every team
  builds the same task in "Full-Agentic" (Mode A) vs. "Mixed Team" (Mode B, human required in the
  loop) and compares them empirically. This framing recurs across the course spec, weekly briefings,
  and the Hausarbeit chapter structure — keep it consistent if editing any of them.
