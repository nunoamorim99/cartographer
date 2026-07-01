![Cartographer — stakeholder documentation, mapped from your repositories](assets/cover.png)

# Cartographer

**Turn the repositories in a project into clear, non-technical stakeholder documentation — without anyone on a dispersed team having to announce what they built.**

Cartographer is a Claude Code plugin. It scans a project's repositories, reads what each one actually does for users, and writes audience-appropriate documents (Markdown + polished black-and-white PDF) describing *what exists and why it matters* — never how it's built. It's read-only, audience-aware, and records where every fact came from.

This repository is both the **plugin** and a **Claude Code marketplace** that serves it.

---

## Install

In Claude Code:

```
/plugin marketplace add nunoamorim99/cartographer
/plugin install cartographer@nunoamorim99
```

- `nunoamorim99/cartographer` is the GitHub `owner/repo` for this repository.
- `nunoamorim99` is the marketplace name (the `name` field in `.claude-plugin/marketplace.json`).

Once installed, the plugin's commands are available in the `/` menu, namespaced under the plugin — e.g. `/cartographer:assess`, `/cartographer:generate`, `/cartographer:doc-status` — and the skill also activates on its own when you ask for stakeholder docs. Update later with `/plugin marketplace update`.

### Manual install (without the marketplace)

Copy the skill and commands straight into your project or home config:

```bash
cp -r plugins/cartographer/skills/cartographer  .claude/skills/
mkdir -p .claude/commands && cp plugins/cartographer/commands/*.md .claude/commands/
```

## What it does

```
/assess   →   review & confirm the product map   →   /generate
```

- **`/assess`** — read-only scan: discovers and classifies every repo, proposes a *product map*, reports maturity and drift, flags anything new/thin/ambiguous, and **stops for your confirmation**.
- **`/generate [scope] [audience] [lang]`** — writes/refreshes the docs from the confirmed map (defaults: all products, `marketing` audience, your configured language). `audience` can be `marketing` (comms/external) or `management` (leadership status).
- **`/doc-status`** — read-only staleness check: what changed since last documented, and any repo not yet covered.

Full details, output layout, and design principles are in the skill's own README: [`plugins/cartographer/skills/cartographer/README.md`](plugins/cartographer/skills/cartographer/README.md).

## Requirements

Claude Code. PDF generation needs the Python packages `markdown` and `weasyprint`; the skill installs them into a private virtual environment automatically the first time. (WeasyPrint also needs system libraries — Pango, Cairo, GDK-PixBuf; if they're absent the skill still delivers the Markdown and tells you what to install.)

## Repository layout

```
.
├── .claude-plugin/marketplace.json      # marketplace catalog
├── plugins/cartographer/
│   ├── .claude-plugin/plugin.json       # plugin manifest
│   ├── skills/cartographer/             # the skill (self-contained, bundled fonts)
│   ├── commands/                        # assess.md, generate.md, doc-status.md
│   └── README.md
├── assets/cover.png                     # cover for this landing page
└── README.md
```

## Before you publish

- Create the GitHub repo at `github.com/nunoamorim99/cartographer` and push these files (make sure the hidden `.claude-plugin/` folders are included).
- Drop your cover image into **`assets/cover.png`** (this landing page) — and, if you want it inside the packaged skill too, into `plugins/cartographer/skills/cartographer/docs/assets/cover.png`. Keep the same filenames and the READMEs pick them up with no other changes.
- Optional: confirm the `license` (currently MIT) and add a `LICENSE` file if you want one.

## Credits

Fonts bundled with the skill: **Spectral** (© Production Type) and **Fira Sans** (© The Mozilla Foundation & Telefónica), both under the SIL Open Font License 1.1.
