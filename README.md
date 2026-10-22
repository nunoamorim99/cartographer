<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo/cartographer-horizontal-color-dark.svg">
    <img src="assets/logo/cartographer-horizontal-color-light.svg" alt="Cartographer" height="72">
  </picture>
</p>

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

Cartographer is published in the **[`nunoamorim99`](https://github.com/nunoamorim99/claude-skills)** plugin marketplace, alongside Nuno Amorim's other plugins. Pick whichever install route fits.

### 1. As a plugin, via the marketplace — recommended

One command installs the skill *and* the slash commands, and keeps them updatable:

```
/plugin marketplace add nunoamorim99/claude-skills
/plugin install cartographer@nunoamorim99
```

Already have the `nunoamorim99` marketplace? Skip the first line, run `/plugin marketplace update nunoamorim99`, then install.

The commands appear in the `/` menu namespaced under the plugin — `/cartographer:assess`, `/cartographer:generate`, `/cartographer:doc-status` — and the skill also activates on its own when you ask for stakeholder docs. Update later with `/plugin marketplace update nunoamorim99`.

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

### 4. Download a zip — no marketplace, or Claude.ai

Every download is on the **[latest release](https://github.com/nunoamorim99/cartographer/releases/latest)** page — no need to clone the repo:

| Where | Download | How |
|---|---|---|
| Claude Code without a marketplace (offline, corporate policy, or to read the files first) | `cartographer-<version>.zip` | Unzip into your project's `.claude/` folder — or `~/.claude/` for every project. Restart Claude Code. |
| Claude.ai **web or desktop** | `cartographer-skill-<version>.zip` | Upload via *Customize → Skills*. Slash commands are Claude Code only; on the web, just ask. |

> Manual installs don't auto-update — grab the newer zip when a release ships. The marketplace route updates itself.

---

## Requirements

Claude Code. PDF generation needs the Python packages `markdown` and `weasyprint`; the skill installs them into a private virtual environment automatically the first time. (WeasyPrint also needs system libraries — Pango, Cairo, GDK-PixBuf; if they're absent the skill still delivers the Markdown and tells you what to install.)

## Repository layout

```
.
├── plugins/cartographer/                # listed in the "nunoamorim99" marketplace (nunoamorim99/claude-skills)
│   ├── .claude-plugin/plugin.json       # plugin manifest
│   ├── skills/cartographer/             # THE SKILL — self-contained, bundled fonts
│   ├── commands/                        # assess.md, generate.md, doc-status.md
│   └── README.md
├── scripts/build_bundles.py         # builds the release zips from the plugin
├── .github/workflows/               # validate (every push) · release (on a v* tag)
├── INSTALL.txt                      # ships inside the drop-in zip
├── assets/
│   ├── logo/                            # README logo (light + dark lockups)
│   └── cover.png                        # social preview image
├── LICENSE
└── README.md
```

Single source of truth: the skill lives once, at `plugins/cartographer/skills/cartographer/`. Every install route reads from that one copy — nothing is duplicated; the release zips are built from it.

## Cutting a release

The zips are built from `plugins/cartographer/` by [`scripts/build_bundles.py`](scripts/build_bundles.py) and are never committed (`dist/` is gitignored). To publish a version:

1. Bump `version` in `plugins/cartographer/.claude-plugin/plugin.json`, commit and push.
2. Tag it: `git tag v1.0.1 && git push origin v1.0.1`

The `release` workflow checks the tag matches `plugin.json`, builds both zips and attaches them to a GitHub Release. The `validate` workflow builds and checks them on every push. Marketplace users don't need a release — they get `main` with `/plugin marketplace update nunoamorim99`.

## Credits

Fonts bundled with the skill: **Spectral** (© Production Type) and **Fira Sans** (© The Mozilla Foundation & Telefónica), both under the SIL Open Font License 1.1.
