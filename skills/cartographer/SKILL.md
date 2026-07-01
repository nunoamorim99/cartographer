---
name: cartographer
description: >-
  Generate and refresh stakeholder documentation for any software project by assessing
  its repositories. Use whenever the user wants to document products for a
  communication/marketing team or for leadership, refresh existing stakeholder docs,
  check what changed across repos since the docs were last written, or get a project
  status read across repositories and branches. Trigger on requests like "assess the
  project", "generate the stakeholder docs", "update the documentation", "what changed
  since I last documented this", "make the marketing files", or "give management a status
  of the project" — even when the word "skill" is not mentioned. Maps a sprawling
  multi-repo codebase into a legible product picture and produces plain, black-and-white
  Markdown + PDF documents in the project's configured language(s), defaulting to English.
---

# Cartographer — stakeholder documentation from repositories

Turn the repositories in a project into clean, non-technical stakeholder documents —
without anyone on a dispersed team having to announce what they built. Cartographer
discovers the repos, reads their value-bearing surfaces, translates capability into plain
language (never mechanism), and produces audience-appropriate docs with version provenance
so "what changed since last time" is always answerable.

Cartographer is project-agnostic. It operates on the **current project root** (the working
directory where it runs). Install it once; it scans whatever project it sits in, and stores
that project's settings in `Stakeholder-Docs/Product-Map.md`.

---

## The model/script contract

Two kinds of work, kept strictly apart:

- **Scripts do the deterministic, mechanical work** — git discovery and PDF rendering.
  They are reliable and never improvise.
  - `scripts/discover_repos.py [root]` — read-only git scan → JSON. Repos, branches,
    default branch, HEAD SHAs, unmerged feature work, value-bearing files, and a
    conservative `doc_signal` hint (`present`/`minimal`/`none`). The hint is *not* a
    verdict — confirm thinness by reading the content.
  - `scripts/discover_repos.py --log REPO SINCE [--until REF]` — lists the commits since a
    given SHA (default end: the repo's default branch). Use this to ground drift detail and
    "What's new" bullets in the real commit range, not in a guess from the latest commit.
    **This script never writes to any repo.** No commits, checkouts, fetches, or branch
    changes — only reads.
  - `scripts/build_pdf.py INPUT.md [OUTPUT.pdf] [--wordmark LABEL]` — Markdown → styled
    HTML → WeasyPrint → B&W PDF, with a diacritics check. Pass the project label as
    `--wordmark`. It needs the `markdown` and `weasyprint` packages; if they are missing it
    **self-bootstraps a private virtual environment inside the skill** (`scripts/.venv`,
    falling back to a user cache dir) and re-runs — no manual `pip install`, and nothing is
    created in the user's project. If the PDF still cannot be built (WeasyPrint also needs
    system libraries — Pango, Cairo, GDK-PixBuf), the script prints exactly what to install
    and exits non-zero; the workflow then **delivers the `.md` and skips only the `.pdf`**
    (see `/generate` step 5).
- **The model does the judgment** — classifying repo roles, inferring user-facing value,
  translating HOW→WHAT, writing native prose in the configured language(s), flagging gaps
  and maturity. A script must never write stakeholder prose; the model must never hand-run
  git when a script exists.

All git interaction is **read-only**. Cartographer never commits, pushes, branches, merges,
or deletes anything.

---

## Reference files — read these when generating

- `reference/writing-standard.md` — **the source of truth for HOW to write.** Level of
  detail, the HOW→WHAT translation table, voice, the four-part module pattern, formatting,
  language rules. Read before writing any doc.
- `reference/audiences.md` — the `marketing` vs `management` profiles: detail ceiling, how
  in-progress work is surfaced, length.
- `reference/document-templates.md` — the exact section skeleton for each document, the
  file-naming and language-suffix scheme, and the formats of the four project files
  (registry, product map, manifest, assessment) plus the output folder layout.

`COMMANDS.md` at the skill root is a user-facing quick reference for the three commands; if
the user asks how to run the skill or what the commands are, point them there.

---

## Grounding discipline (this is what keeps the docs honest)

The raw input is source code — which is the HOW the standard forbids. So the rule is:
**read the value-bearing surfaces, translate them, and never infer capability from deep
implementation.**

**Read and trust (in priority order):**

1. `STAKEHOLDER.md` if present — a plain-language breadcrumb a developer left ("what this
   does / what's new"). When present, it is the best surface; trust it.
2. `README`, `docs/`, `CHANGELOG` — product copy, feature descriptions, release notes.
3. High-level, user-facing names only — screen/route names, top-level API resource names
   that map to user features (e.g. "events", "alerts"), feature flags named for features.

**Scaffold/boilerplate READMEs are not value-bearing.** A generated README (Expo, Create
React App, Next.js, Vite, etc.) describes the toolchain, not the product — discovery flags
it as `readme_boilerplate: true`. Ignore it for capabilities and look to `docs/`, a product
sheet, or `STAKEHOLDER.md` instead. A long boilerplate README is still empty of product
signal; do not let its length fool you into treating the repo as well-documented.

**Record what each doc rests on.** When a product doc is grounded mainly in one source
(e.g. a single product sheet rather than the repo itself), note that source in the manifest
("grounded in: docs/Product-Sheet"). This makes the accuracy dependency visible — the doc is
only as current as that source — and is exactly the kind of single-source reliance the
assessment should surface. If the only real source is a sheet that may go stale, say so.

**Do NOT read for capabilities:** framework/library choices, database schemas, protocols,
ports, internal class/function structure, config plumbing. Inferring features from
implementation is how both invention and HOW-leakage happen.

**When a repo is thin** (no STAKEHOLDER.md, no docs, a one-line README): do not pad or
guess. Flag it in the assessment and recommend the product team confirm scope before
publishing. Never invent a capability you cannot ground in a surface above.

---

## Commands

Three commands, all read-only on git. Match the user's intent to one; the literal slash
syntax is not required.

### `/assess` — understand the project; propose/refresh the product map

A full read-only pass. **Writes the assessment and map; never writes stakeholder docs.**

1. Run `discover_repos.py` on the project root → JSON facts.
2. **First run only — establish project settings.** If `Product-Map.md` does not yet exist,
   ask the user which language(s) the documentation should be produced in (default
   **English**; they may choose one or several, e.g. English + Portuguese). Derive a
   default project label from the root folder name and confirm it (used as the PDF footer
   wordmark). Persist both in the `## Settings` block of `Product-Map.md`. Keep this to a
   single question where possible.
3. Read `Repos-Registry.md` (shared, project root) if it exists. Reconcile: mark repos
   still present (update *Last seen*), note repos newly appeared, note repos gone. A
   PM/Agile skill may also append new-repo notices here — treat the registry as shared,
   owned by neither skill.
4. **Classify each repo** (model judgment) by reading its value-bearing surfaces:
   `product`, `supporting` (e.g. an API that backs a product but is not documented
   separately), `multi-module` (holds more than one product/functionality), `infra`, or
   `unknown`. Propose a product map, or refresh the existing one non-destructively (keep
   the user's edits, settings, and fixed module order).
5. **Maturity:** default branch = live; feature branches with unmerged work = in
   development (summarize functionally, never by mechanism).
6. **Drift:** for each repo with a last-documented SHA in `_Manifest.md`, run
   `discover_repos.py --log <repo> <sha>` and report the actual commits since — count plus
   the headline subject(s). Do not infer the change from HEAD's latest commit alone.
7. **Flag, judging thinness from content:** treat `doc_signal` as a hint, then read the
   surface to decide. Flag genuinely thin repos, new/unclassified repos, multi-module repos
   that should be split (record a `scope:` per resulting product), scope-unconfirmed repos,
   and stale map entries whose repo no longer exists.
8. Write/update `Repos-Registry.md`, `Product-Map.md`, and `_Assessment.md`. The assessment
   is **actions-first**: lead with what to do, then a compact per-repo status table, then
   detail only for flagged repos (format in `document-templates.md`).
9. **Present a summary and stop.** Ask the user to confirm or edit the product map before
   generating — this is the design-before-build gate. Do not auto-generate.

`/assess --split <repo>` — guided variant for a multi-module repo: propose how to split it
into two documented product units, then update the map on confirmation.

The assessment is a deliverable in its own right: a single glance at every repo, its role,
branch state, drift, and gaps. It answers "what's the status of the project" without
generating any stakeholder doc.

### `/generate [scope] [audience] [lang]` — write/refresh the docs

Writes stakeholder docs from the **confirmed** product map. Defaults in **bold**.

- `scope`: `all` | `<product>` (a product name from the map)
- `audience`: **`marketing`** | `management`
- `lang`: the project's configured language(s) by default; override to produce a specific
  one (e.g. `en`). If a requested language is not in the settings, offer to add it.

Steps:

1. Ensure the map is current. If no map exists or it is stale, run `/assess` first and get
   confirmation. Run `discover_repos.py` to capture current SHAs for provenance regardless.
2. Read `writing-standard.md`, the relevant `audiences.md` profile, and
   `document-templates.md`. Read the `## Settings` block for languages and project label.
3. For the scope, write each doc grounded in value-bearing surfaces, translating HOW→WHAT,
   in each configured language (native reading, not literal translation). Lead every section
   with concrete substance, not metaphor — a reader should learn what was actually built
   (writing-standard §"Substance over metaphor"). For a split product, document only what its
   `scope:` line covers. `scope all` also (re)writes the ecosystem overview, whose
   "How it all connects" example must chain only source-supported links.
   - **marketing:** shipped work in full + one brief forward-looking mention of what's
     coming. Never describe a half-built branch as if it ships.
   - **management:** use the status-first section order in `audiences.md` — open with
     "Where this stands" and "Decisions needed", then a compressed capability recap and
     dependencies.
4. On a refresh, add a "What's new" banner at the top: run `discover_repos.py --log <repo>
   <last-documented-sha>` and turn the real commits since into 2–4 plain-language bullets —
   merged work as live items, plus one forward mention from any feature branch (marketing).
5. Render each `.md` to `.pdf` with `build_pdf.py`, passing `--wordmark "<project label>"`.
   The script installs its own PDF dependencies if needed. If it still exits non-zero
   (missing system libraries), **do not fail the run** — deliver the `.md` files, tell the
   user the `.pdf` was skipped and surface the one-line install hint the script printed, and
   offer to render PDFs once the libraries are present. Confirm the diacritics check passed
   for accented languages (a WARNING means accents may have been stripped — investigate).
6. Update `_Manifest.md`: a new version row per document with audience, language, repos@SHA,
   timestamp, the What's-new bullets, and **what the doc was grounded in** when it rests
   mainly on one source (e.g. "grounded in: docs/Product-Sheet") so the accuracy dependency
   is on record.
7. Write `.md` and `.pdf` side by side in the product's folder under `Stakeholder-Docs/`,
   using the `[Product-Name].[lang].md` naming scheme.

Producing files is a deliverable. Once written, present them to the user (use
`present_files` if available).

### `/doc-status` — am I stale?

A quick staleness read. No map work, no doc writing.

1. Run `discover_repos.py` for current HEAD SHAs.
2. Read `_Manifest.md` for each document's last-documented SHA.
3. Report, per product: changed since last documented? (and which audiences/languages are
   stale), plus any repo in the registry not covered by the product map (the coverage
   guarantee — "is every known repo documented?").

This directly serves the core need: a dispersed, asynchronous team that does not announce
changes. `/doc-status` tells you what moved without anyone telling you.

---

## Division of labour with a PM/Agile skill

If a separate PM/Agile skill is present, both skills read git (cheap, deterministic;
duplicated read is fine — it keeps each skill standalone). What is **not** duplicated is
curated judgment:

- **`Repos-Registry.md`** is the one shared file. A PM skill appends new-repo notices for
  its own purposes; Cartographer cross-checks the registry against the product map for the
  coverage guarantee. Neither skill owns it; it lives at the project root.
- **The product map** (`Product-Map.md`) is owned by Cartographer only — a PM skill has no
  concept of "product".

So: "no repo missing" is guaranteed from the PM side; "all known repos documented" is
guaranteed here. Keep `/assess` in Cartographer — doc generation needs the repo set
regardless, so this skill must run standalone whether or not a PM skill exists.

---

## The STAKEHOLDER.md breadcrumb (encourage its use)

A repo can carry a tiny `STAKEHOLDER.md` where a developer leaves the plain-language "what
this does / what's new" in their own words. When present, it is the highest-trust surface
and cuts both invention risk and mischaracterization. It is the near-zero-friction signal a
dispersed team can leave for the docs to harvest automatically. When you flag a thin repo
in an assessment, suggest adding one. Suggested shape:

```
# What this is
One or two plain sentences: what this repo does for users.
# What's new
- bullet, in plain language
# Status
live / in development / experimental
```

---

## Guardrails

- **Read-only git, always.** Discovery and status never modify a repo.
- **Never invent.** No capability without a value-bearing surface to ground it.
- **Never leak mechanism.** Every technical fact is translated before it appears; if it
  cannot be translated to function or value, it is cut.
- **Confirm before generating.** `/assess` proposes the map and stops; the user confirms.
  Splitting a repo is a map edit the user approves.
- **Both formats, every language.** Each generated document is produced as `.md` and `.pdf`
  in every configured language.
- **Honest maturity.** Marketing hints once at what's next; management states status
  plainly. Neither implies unfinished work is done.
