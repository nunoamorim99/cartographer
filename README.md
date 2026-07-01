<p align="center">
  <img src="assets/cover.png" alt="Cartographer" width="100%" />
</p>

<h1 align="center">Cartographer</h1>

<p align="center">
  <b>Stakeholder documentation, mapped from your repositories —<br/>
  what each product does and how it fits, in Markdown &amp; PDF.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Claude_Code-Skill_%2B_Plugin-8b5cf6?style=flat-square&labelColor=2d2d2d" alt="Claude Code: Skill + Plugin" />
  <img src="https://img.shields.io/badge/Output-Markdown_%2B_PDF-10b981?style=flat-square&labelColor=2d2d2d" alt="Output: Markdown + PDF" />
  <img src="https://img.shields.io/badge/Git-read--only-06b6d4?style=flat-square&labelColor=2d2d2d" alt="Git: read-only" />
  <img src="https://img.shields.io/badge/Typography-Spectral_%2B_Fira-a855f7?style=flat-square&labelColor=2d2d2d" alt="Typography: Spectral + Fira" />
  <img src="https://img.shields.io/badge/License-MIT-64748b?style=flat-square&labelColor=2d2d2d" alt="License: MIT" />
</p>

---

Cartographer is a **Claude Code skill** (packaged here also as an installable **plugin**). It scans a project's repositories, reads what each one actually does for users, and writes audience-appropriate documents — Markdown + polished black-and-white PDF — describing *what exists and why it matters*, never how it's built. It turns the repositories in a project into clear, non-technical stakeholder documentation without anyone on a dispersed team having to announce what they built. It's read-only, audience-aware, and records where every fact came from.

---

## What it does

```
/assess   →   review & confirm the product map   →   /generate
```

- **`/assess`** — a read-only pass: discovers and classifies every repo, proposes a *product map* (which repos roll up into which product doc), reports maturity and drift, flags anything new/thin/ambiguous, and **stops for your confirmation**. It never writes stakeholder docs on its own.
- **`/generate [scope] [audience] [lang]`** — writes/refreshes the docs from the confirmed map (defaults: all products, `marketing` audience, your configured language). `audience` is `marketing` (comms / external) or `management` (leadership status).
- **`/doc-status`** — a read-only staleness check: what changed since last documented, and any repo not yet covered.

It produces an **ecosystem overview** (what the products are and how they fit), **one document per product** (what it does, who it's for, how it connects), and an **actions-first assessment** of project status — all in Markdown and PDF, in your configured language(s). Full details, output layout, and design principles are in the skill's own README: **[`plugins/cartographer/skills/cartographer/README.md`](plugins/cartographer/skills/cartographer/README.md)**.

---

## Install

Pick whichever fits. This repo is both the **skill** (at `skills/cartographer/`) and a **plugin marketplace** that serves it.

### 1. As a plugin, via the marketplace — recommended

One command installs the skill *and* the slash commands, and keeps them updatable:

```
/plugin marketplace add nunoamorim99/cartographer
/plugin install cartographer@nunoamorim99
```

The commands appear in the `/` menu namespaced under the plugin — `/cartographer:assess`, `/cartographer:generate`, `/cartographer:doc-status` — and the skill also activates on its own when you ask for stakeholder docs. Update later with `/plugin marketplace update`.

### 2. As a skill only — manual

Copy the skill folder into your skills directory (project-level `.claude/skills/`, or `~/.claude/skills/` for all projects):

```bash
cp -r plugins/cartographer/skills/cartographer ~/.claude/skills/
```

Then just describe what you want ("assess the project", "generate the stakeholder docs") — the skill activates on its own. No commands required.

### 3. Add the slash commands — optional

To get `/assess`, `/generate`, `/doc-status` in the `/` menu without the plugin, drop the command files in too:

```bash
mkdir -p .claude/commands && cp plugins/cartographer/commands/*.md .claude/commands/
```

---

## Requirements

Claude Code. PDF generation needs the Python packages `markdown` and `weasyprint`; the skill installs them into a private virtual environment automatically the first time. (WeasyPrint also needs system libraries — Pango, Cairo, GDK-PixBuf; if they're absent the skill still delivers the Markdown and tells you what to install.)

## Repository layout

```
.
├── .claude-plugin/
│   └── marketplace.json                 # marketplace catalog (source: ./plugins/cartographer)
├── plugins/cartographer/
│   ├── .claude-plugin/plugin.json       # plugin manifest
│   ├── skills/cartographer/             # THE SKILL — self-contained, bundled fonts
│   ├── commands/                        # assess.md, generate.md, doc-status.md
│   └── README.md
├── assets/cover.png                     # cover for this landing page
└── README.md
```

Single source of truth: the skill lives once, at `plugins/cartographer/skills/cartographer/`. All three install routes read from that one copy — nothing is duplicated.

## Credits

Fonts bundled with the skill: **Spectral** (© Production Type) and **Fira Sans** (© The Mozilla Foundation & Telefónica), both under the SIL Open Font License 1.1.
