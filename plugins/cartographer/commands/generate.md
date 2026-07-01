---
description: Cartographer — write/refresh stakeholder docs (.md + .pdf) from the confirmed product map
argument-hint: "[scope] [audience] [lang]"
---
Use the **Cartographer** skill to run its `/generate` workflow on the current project root.

Parse $ARGUMENTS as up to three optional values, in any order:
- **scope** — a product name from the map, or `all` (default: `all`)
- **audience** — `marketing` (default) or `management`
- **lang** — a configured language code such as `en` or `pt` (default: the project's
  configured language(s) from the `## Settings` block of `Product-Map.md`)

If $ARGUMENTS is empty, generate every product for the `marketing` audience in the
configured language(s). Require a confirmed product map first; if none exists or it is
stale, run `/assess` and get confirmation before generating. Follow the skill's generate
steps: ground every document in value-bearing surfaces, translate HOW→WHAT (substance over
metaphor), keep split products within their `scope:`, add a grounded "What's new" banner on
refreshes, render PDFs with the project wordmark, and update `_Manifest.md`.
