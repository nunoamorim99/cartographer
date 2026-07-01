# Document templates & project files

Two things live here: the **section skeletons** for each stakeholder document, and the
**formats** of the project files Cartographer reads and writes (registry, product map,
manifest, assessment). Everything is project-agnostic; example names below are neutral
placeholders.

All filenames and folders are **English and ASCII**, regardless of output language.
Document language is carried by a **language-code suffix** on the filename, so the same
base name serves every language.

---

## Part A — Stakeholder document skeletons

### File naming

`[Product-Name].[lang].md` plus the matching `.pdf`. Examples:
`Overview.en.md`, `Web-Portal.en.md`, `Web-Portal.pt.md`, `Customer-App.en.md`.
ASCII, hyphenated, no spaces or accents. The `.pdf` shares the base name; keep `.md` and
`.pdf` side by side.

### Ecosystem overview

File: `Overview.[lang].md`, in `Stakeholder-Docs/Overview/`.

```
# [Ecosystem name] — Overview
*A product of [organisation] · overview · [month year]*

[optional "## What's new" banner on a refresh — date + 2–4 change bullets]

---
## What [ecosystem] is
definition · the modular principle ("start with one module, grow to the whole network") ·
the data-isolation principle

---
## The two sides
back office vs. end-user-facing, and the automatic bridge between them

---
## Products at a glance
[the ONE comparison table: Product / What it is / Who uses it]

---
## The [N] modules
one line each, fixed order

---
## How it all connects
a single worked end-to-end example moving through the whole ecosystem

---
## Guiding principles
short bullets, each a bolded label + one sentence
```

### Product document

File: `[Product-Name].[lang].md`, in its product folder.

```
# [Ecosystem name] — [Product]
*A product of [organisation] · product document · [month year]*

[optional "## What's new" banner on a refresh]

---
## Purpose
one to two paragraphs: what it is and the value it delivers

---
## Who it's for
bullets, each a persona + what they do with it

---
## What it does
capabilities as bolded-label bullets in plain language

---
## The modules          [only when the product has modules]
numbered ### subsections, each following the four-part module pattern, in fixed order

---
## How it connects to the rest of the ecosystem
closing prose tying it back to the whole

[management audience only:]
---
## Where this stands
short status close: live / in development / needs confirmation
```

### The standard set

1. One ecosystem overview document.
2. One document per product.
3. Modules are **sections inside their parent product document** — never separate files —
   in a fixed order.

---

## Part B — Project files (read & written by the skill)

All four are plain Markdown, hand-editable, git-traceable. Cartographer proposes and
maintains them; the user can edit them directly. Example repo/product names are neutral.

### 1. `Repos-Registry.md` — shared, at project root

The one file shared with a PM/Agile skill (if present). Neither skill owns it. Cartographer
reads it to run the coverage check and updates role/notes; a PM skill may append new-repo
notices. Keep it a simple table.

```
# Repos Registry
*Shared source of truth for which repositories exist and their high-level role. Read and
updated by Cartographer; a PM/Agile skill may also append new-repo notices.*

| Repo | Role | First seen | Last seen | Notes |
|---|---|---|---|---|
| web-portal | product | 2026-06-26 | 2026-06-26 | admin control room |
| gateway-api | supporting | 2026-06-26 | 2026-06-26 | backs portal + apps |
| network-maps | product (thin) | 2026-06-26 | 2026-06-26 | scope unconfirmed — confirm before publish |
```

Role values: `product`, `supporting`, `multi-module`, `infra`, `unknown`.

### 2. `Product-Map.md` — owned by Cartographer

The repo→product rollup **and** the per-project settings (configured languages, project
label/wordmark, fixed name translations). Cartographer *proposes* the map on first
`/assess`; the user confirms/edits. Owned here only — a PM skill has no concept of "product".

```
# Product Map
*How repositories roll up into stakeholder product documents, plus project settings.
Edit freely; /generate reads this. Fixed module order is preserved across releases.*

## Settings
- languages: en            # configured on first assessment; e.g. "en, pt"
- project label: ACME      # used as the PDF footer wordmark
- name translations: —     # e.g. "Web Portal -> Portal Web" when a non-en language is set

## Overview
included products (in display order): Web Portal, Customer App, Public Site

## Web Portal
- doc base name: Web-Portal
- repos: web-portal
- supporting repos (context, not documented separately): gateway-api
- modules (fixed order): News, Events, Schedules, Sensors, Network-Maps

## Customer App
- doc base name: Customer-App
- repos: customer-app
- modules: —

## Public Site
- doc base name: Public-Site
- repos: public-site
- modules: —

## Analytics-Reporting          # a split product — two products share one repo
- doc base name: Analytics-Reporting
- repos: analytics-suite
- scope: the reporting dashboards only (facilities KPIs) — NOT the export engine
- modules: —

## Analytics-Exports
- doc base name: Analytics-Exports
- repos: analytics-suite
- scope: the scheduled export engine only (PDF/Excel/CSV reports) — NOT the dashboards
- modules: —
```

When two products map to the **same repo** (a multi-module split), each entry MUST carry a
`scope:` line stating exactly which functionality it covers and which it excludes. `scope:`
is the grounding boundary `/generate` uses to keep the two docs from bleeding into each
other — without it, the model cannot reliably tell which capabilities belong to which
product. The writing standard treats `scope:` as the value-bearing boundary for that product.

When a repo holds more than one product/functionality, record it as `multi-module` in the
registry and split it here into two product entries with `scope:` lines (or run guided
`/assess --split <repo>`). `/generate` then treats each as its own documented unit; the
manifest keeps lineage so version history does not reset.

### 3. `_Assessment.md` — written by `/assess`, a first-class deliverable

The latest read of the whole project. It is the most-checked artifact, so it is structured
**decision-first**: what to act on, then a compact per-repo status table, then detail *only*
for the repos that are flagged. Don't repeat clean repos in prose — the table covers them.

```
# Project Assessment — [project] — [date]

## Actions needed
Lead with this. A short, ordered list of what the reader should do, each naming the repo
and the action. If nothing needs action, say "No actions needed — N repos, all documented
and current." Example:
1. Regenerate Web-Portal docs — drift: "fuel logs" merged since last docs.
2. Classify new repo `telemetry-svc` (looks supporting) and add to registry + map.
3. Decide split for `analytics-suite` (holds reporting + exports).
4. Confirm scope of `site-maps` before it appears in any external doc.

## Status at a glance
| Repo | Role | State | Docs | Drift | Flag |
|---|---|---|---|---|---|
| web-portal | product | live + 1 branch in dev | STAKEHOLDER ✓ | changed (abc→def) | drift |
| tenant-app | product | live | README | — | — |
| gateway | supporting | live | README | — | — |
| telemetry-svc | unknown | live | README | — | new repo |
| analytics-suite | multi-module | live | README | — | needs split |
| site-maps | unknown | live | none | — | thin |

## Detail (flagged repos only)
### web-portal — drift
- In development: feature/sensor-alerts (1 commit ahead) — live alerts, not yet merged.
- Changed since last documented: 1 commit — "feat(work-orders): add fuel logs" (abc→def).
### analytics-suite — needs split
- README describes two separable things: reporting dashboards; scheduled exports.
- Recommend two documented units (see proposed map), or confirm one product.
### site-maps — thin
- doc_signal: none (5-word README, no STAKEHOLDER.md, no docs/). Too thin to document
  safely — recommend confirming scope or adding a STAKEHOLDER.md before publishing.

## Coverage & new repos
- Not yet covered by the product map: telemetry-svc (new), site-maps (unconfirmed).
- Stale map entry: `public-site` in the map has no matching repo in this scan — confirm.
- New since last assessment: telemetry-svc (first seen [date]).
```

Notes for filling it in:
- **State** comes from branches: default branch = live; add "+ N branch(es) in dev" when
  feature branches carry unmerged work.
- **Drift** comes from `discover_repos.py --log <repo> <last-documented-sha>` — report the
  commit count and the headline subject(s), not a guess from HEAD.
- **Docs** reflects `doc_signal` plus what surfaces exist; remember the signal is a hint —
  confirm thinness by reading the content. If `readme_boilerplate` is true, mark the README
  as "scaffold" in the Docs column and note where the real source lives (e.g. docs/), since a
  generated README is not real documentation however long it is.

### 4. `_Manifest.md` — the version log & provenance

Written by `/generate`. Per document: product, audience, language, source repo(s) +
**commit SHA**, timestamp, version, the "What's new" bullets, and — when a doc rests mainly
on one source — what it was **grounded in**. The SHA is the join key that makes `/doc-status`
and the "What's new" header answerable rather than guessed; the grounded-in note keeps the
accuracy dependency visible (a doc built from a product sheet is only as current as that
sheet).

```
# Manifest — version log

## Web-Portal
| Version | Date | Audience | Lang | Repos @ SHA | Grounded in | What's new |
|---|---|---|---|---|---|---|
| v3 | 2026-06-26 14:20 | marketing | en | web-portal@def5678 | repo (README + docs/) | payroll export; sensor-alerts mention |
| v2 | 2026-06-12 09:10 | marketing | en | web-portal@abc1234 | repo (README + docs/) | inspections module |

## Customer-App
| Version | Date | Audience | Lang | Repos @ SHA | Grounded in | What's new |
|---|---|---|---|---|---|---|
| v1 | 2026-06-26 | marketing | en | customer-app@1a2b3c4 | docs/Product-Sheet (README is Expo scaffold — single-source) | initial |
```

Use the **Grounded in** column to flag single-source reliance: when the repo's own README is
a generated scaffold and the real content came from one product sheet, say so. That doc is
only as accurate as that sheet — note it here and in the assessment.

---

## Part C — Output folder layout

Written into the project root. `Stakeholder-Docs/` is owned by Cartographer and is skipped
by repo discovery so it never documents itself.

```
<project-root>/
  Repos-Registry.md            # SHARED with a PM/Agile skill
  Stakeholder-Docs/
    Product-Map.md             # the product map + project settings (config)
    _Assessment.md             # latest assessment
    _Manifest.md               # version log + provenance
    Overview/                  # ecosystem overview (.md + .pdf, per language)
    Web-Portal/                # per-product docs (.md + .pdf, per language)
    Customer-App/
    Public-Site/
```
