# Cartographer (plugin)

Generate stakeholder documentation from a project's repositories — what each product does and how it fits together, as black-and-white Markdown + PDF. Read-only, audience-aware, provenance-tracked.

This plugin bundles:

- **The skill** (`skills/cartographer/`) — the full workflow, references, PDF pipeline, and bundled fonts. Its own README has the complete documentation: [`skills/cartographer/README.md`](skills/cartographer/README.md).
- **Three commands** (`commands/`) — `/assess`, `/generate`, `/doc-status`. Installed under the plugin namespace (e.g. `/cartographer:assess`), they appear in the `/` menu with hints and invoke the skill's workflow.

See the repository root README for installation via the marketplace.
