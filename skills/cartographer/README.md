![Cartographer — stakeholder documentation, mapped from your repositories](assets/cover.png)

# Cartographer

**Turn the repositories in a project into clear, non-technical stakeholder documentation — without anyone on a dispersed team having to announce what they built.**

Cartographer is a Claude Code skill. It scans a project's repositories, reads what each one actually does for users, and writes audience-appropriate documents (Markdown + polished black-and-white PDF) that describe *what exists and why it matters* — never how it's built. It records where every fact came from, so "what changed since last time" is always answerable.

---

## The problem it solves

On a dispersed, asynchronous team, nobody announces every change. Communication and marketing stakeholders fall behind on what's been built, and keeping them updated becomes a recurring manual chore. Cartographer automates the chore: point it at the project root, and it maps the current state of every repository into documentation a non-technical reader can use.

## What it produces

- **An ecosystem overview** — what the products are and how they fit together.
- **One document per product** — what it does, who it's for, and how it connects to the rest, with modules described in a consistent pattern.
- **A project assessment** — an actions-first status read of every repo: what's live, what's in development, what drifted since last documented, and what needs a decision.
- Every document in **Markdown and PDF**, in your project's configured language(s).

## How it works

```
/assess      →   review & confirm the product map   →   /generate
```

1. **`/assess`** does a read-only pass: discovers and classifies every repo, proposes a *product map* (which repos roll up into which product doc), reports maturity and drift, and flags anything new, thin, or ambiguous. It **stops and waits for you to confirm** — it never writes stakeholder docs on its own.
2. You review the proposed map, edit if needed, and confirm.
3. **`/generate`** writes and refreshes the documents from the confirmed map, renders PDFs, and records provenance.
4. **`/doc-status`** later tells you, at a glance, which products changed since they were last documented — so you know what to refresh without anyone telling you.

See **[COMMANDS.md](COMMANDS.md)** for the full command reference.

## The commands

| Command | What it does |
|---|---|
| `/assess [--split <repo>]` | Read-only scan; proposes the product map; reports status, drift, and gaps. Stops for confirmation. |
| `/generate [scope] [audience] [lang]` | Writes/refreshes the docs. Defaults to all products, `marketing` audience, your configured language(s). |
| `/doc-status` | Read-only staleness check: what changed since last documented, and any repo not yet covered. |

`audience` is `marketing` (the default — for the communication team and external readers) or `management` (a status-first view for leadership).

## Installation

**The skill** — place the `cartographer/` folder in your Claude Code skills directory (`.claude/skills/cartographer/`), or install the packaged `cartographer.skill` / `cartographer.zip`.

**The slash commands (optional but recommended)** — copy the command files into `.claude/commands/` so `/assess`, `/generate`, and `/doc-status` appear in the `/` menu with hints:

```bash
mkdir -p .claude/commands && cp commands/*.md .claude/commands/
```

Then run Cartographer from any project root — it operates on the current working directory and stores that project's settings and output under `Stakeholder-Docs/`.

## Output layout

```
<project-root>/
  Repos-Registry.md          # shared record of which repos exist (also used by a PM/Agile skill)
  Stakeholder-Docs/
    Product-Map.md           # repo → product rollup + project settings (languages, label)
    _Assessment.md           # latest actions-first project status
    _Manifest.md             # version log + provenance (source commit per doc)
    Overview/                # ecosystem overview (.md + .pdf)
    <Product>/               # per-product docs (.md + .pdf)
```

Everything is plain, hand-editable Markdown. The product map and assessment are yours to adjust.

## What makes the output trustworthy

- **What, not how.** Every technical fact is translated into plain functional or value language before it appears. Frameworks, protocols, schemas, and endpoints never reach the reader.
- **Grounded, never invented.** Capabilities are drawn from value-bearing surfaces (a `STAKEHOLDER.md` breadcrumb, README, `docs/`, product sheets). Generated scaffold READMEs are recognised and ignored. If a repo is too thin to document safely, Cartographer flags it instead of guessing.
- **Honest about maturity.** Shipped work is described as live; in-development work is handled per audience — a brief forward mention for marketing, real status for management.
- **Provenance on record.** Each document notes the source commit it was generated from and, when it rests on a single source, says so — so its accuracy dependency is visible.
- **Read-only.** Cartographer never commits, pushes, branches, or deletes. It only reads git.

## Design & typography

Documents are set in **Spectral** (a serif designed for legible screen and print reading) with **Fira Sans** headings — both bundled with the skill under the SIL Open Font License, so PDFs render identically on every machine. The palette is deliberately black and white: hierarchy is carried by weight, rules, and space, so the documents are equally at home in a leadership review or a marketing handoff.

## Requirements

- **Claude Code**, run from your project root.
- **PDF generation** needs the Python packages `markdown` and `weasyprint`. Cartographer installs them into a private virtual environment inside the skill automatically the first time — no manual setup. (WeasyPrint additionally needs system libraries — Pango, Cairo, GDK-PixBuf; if they're missing, Cartographer still delivers the Markdown and tells you exactly what to install for PDFs.)

## Credits

Fonts: **Spectral** (© Production Type) and **Fira Sans** (© The Mozilla Foundation & Telefónica), both under the SIL Open Font License 1.1. See `scripts/fonts/` for the license texts.
