# Cartographer — Command Reference

Run these from Claude Code with the skill installed and your project as the working
directory. Type the command (the exact slash form below works; describing it in your own
words works too — the skill recognises the intent). All git access is **read-only**.

---

## Quick start

**First time in a project**

1. `/assess` — scans the repos, proposes a product map, asks which language(s) to produce.
2. Review the proposed map, edit if needed, and confirm.
3. `/generate` — writes the stakeholder docs.

**Every time after that**

1. `/doc-status` — what changed since you last documented it?
2. `/generate <product>` — refresh the ones that moved (or `/generate` for everything).

---

## The three commands

### `/assess`
Read-only pass over the whole project. Discovers and classifies every repo, proposes or
refreshes the product map, reports maturity and drift, and flags new/thin/multi-module
repos. **Stops for your confirmation — it never writes stakeholder docs.** On the first run
it asks which language(s) to produce and sets the project label.

- `/assess --split <repo>` — split a repo that holds two products into two documented units.

Writes: `Repos-Registry.md`, `Stakeholder-Docs/Product-Map.md`, `Stakeholder-Docs/_Assessment.md`.

### `/generate [scope] [audience] [lang]`
Writes/refreshes the stakeholder docs from the **confirmed** product map. Produces `.md` and
`.pdf` per product per language and updates the version log.

| Argument | Values | Default |
|---|---|---|
| scope | `all` or a product name (e.g. `Control-Portal`) | `all` |
| audience | `marketing` or `management` | `marketing` |
| lang | a configured language code (e.g. `en`, `pt`), or several | all configured languages |

Examples:

- `/generate` → every product, marketing, your configured language(s)
- `/generate Control-Portal` → just that product, marketing
- `/generate all management` → everything, leadership status view
- `/generate Control-Portal marketing pt` → one product, marketing, Portuguese
- `/generate all marketing en` → everything, marketing, English only

Writes: docs under `Stakeholder-Docs/<Product>/`, updates `Stakeholder-Docs/_Manifest.md`.

### `/doc-status`
Quick staleness check — no writing. Tells you which products changed since they were last
documented (and which audiences/languages are now stale), plus any repo not yet covered by
the product map.

---

## Typical flows

**Refresh after the team shipped things**

1. `/doc-status`
2. `/generate <product>` for each one that changed
3. (optional) `/generate <product> management` for a leadership update

**Leadership asks for a status**

1. `/assess` (get the current picture)
2. `/generate all management`

**A new repo appeared**

1. `/assess` (it gets flagged as new; classify it, confirm the map)
2. `/generate <affected product>`

**A repo turns out to be two products**

1. `/assess --split <repo>` (or edit `Product-Map.md` to add the second entry with a `scope:` line)
2. confirm, then `/generate`

---

## Good to know

- **marketing** = the communication team / external audience (the default, your recurring job).
  **management** = leadership; opens with status and decisions, then a compressed recap.
- **Language** is set on the first `/assess` (default English). Ask for another with `lang`,
  or add it to the `## Settings` block in `Product-Map.md`.
- Everything lands in `Stakeholder-Docs/` at the project root. The product map and the
  assessment are plain Markdown you can edit by hand.
- `Repos-Registry.md` (project root) is shared with the PM/Agile skill; the product map is
  this skill's alone.
