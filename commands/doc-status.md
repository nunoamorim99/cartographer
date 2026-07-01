---
description: Cartographer — check which products are stale versus the latest repo commits (read-only)
---
Use the **Cartographer** skill to run its `/doc-status` workflow on the current project root.

Compare each product's last-documented commit (from `_Manifest.md`) against the current
HEAD of its repos, and report: which products changed since they were last documented (and
which audiences/languages are now stale), plus any repo in `Repos-Registry.md` not yet
covered by `Product-Map.md` (the coverage guarantee). This is read-only — do not write
anything or modify any repo.
