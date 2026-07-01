---
description: Cartographer — scan all repos, propose the product map, report status, drift & gaps (read-only)
argument-hint: "[--split <repo>]"
---
Use the **Cartographer** skill to run its `/assess` workflow on the current project root.

Optional arguments: $ARGUMENTS
- If the arguments contain `--split <repo>`, run the guided multi-module split for that repo
  (propose two product entries with `scope:` lines, then update the map on confirmation).

Follow the skill's assess steps exactly: read-only discovery via its discovery script,
classify each repo, propose or non-destructively refresh `Product-Map.md`, report maturity
and drift (using the `--log` commit range), flag new/thin/multi-module/stale entries, and
write `Repos-Registry.md`, `Product-Map.md`, and the actions-first `_Assessment.md`. Then
**stop and ask for confirmation before generating** — do not write any stakeholder docs.
On the first run in a project, ask which language(s) to produce and set the project label.
