# Audience profiles

`/generate` takes an audience. The writing standard (`writing-standard.md`) always applies;
the audience profile changes the **detail ceiling**, how **in-progress work** is surfaced,
and the **default length**. Marketing is the default — it is the recurring job.

---

## marketing (default)

The strict standard, for the communication/marketing team and external/non-technical
stakeholders.

- **Detail ceiling:** the writing standard as written. WHAT and WHY only; never HOW.
- **Maturity / in-progress work:** describe **shipped work** (on the default branch /
  merged) in full. Add **one brief, forward-looking mention** of what is coming — a single
  sentence, no detail, no commitments, no dates. Example: *"A live-alerts capability is in
  development and will extend this further."* Never describe a half-built feature branch as
  if it exists.
- **Risk / gap notes:** kept out of the body. If a repo is too thin to document safely, do
  not pad it — note the gap in the assessment, not in the stakeholder doc.
- **Length:** product docs ≈1–2 pages; a many-module portal ≈4–5 pages; overview ≈3 pages.

> In short: marketing docs are confident and clean. They describe what is live, hint once
> at what is next, and never leak mechanism or over-promise.

---

## management

A higher-detail tier for leadership who ask for project status. Same plain voice and the
same HOW→WHAT translation — leadership still does not want frameworks and protocols — but
**status-first**: lead with where things stand and what needs deciding, not with a capability
tour.

**Section order (overrides the standard product skeleton):**

1. **Where this stands** — open with it. Per product: what is live, what is in active
   development (feature branches with unmerged work, described functionally), what is newest
   or least mature. This is the reason the management doc exists; it goes first, not last.
2. **Decisions needed** — a short block of anything awaiting a call: an unmerged branch that
   needs a merge target before it can be announced, a thin/unconfirmed repo, a scope
   question. If there are none, say so in one line.
3. **What it does** — a *compressed* capability recap (bolded-label bullets, one line each).
   Leadership needs the shape, not the full marketing prose; keep this tight.
4. **Dependencies** — supporting repos/services this product relies on, named functionally.

Other notes:

- **Detail ceiling:** still no technical plumbing, but functional detail can go deeper, and
  status is foregrounded.
- **Risk / gap notes:** surface them in the body (in "Decisions needed" or inline), not just
  the assessment.
- **Length:** completeness over brevity, but lead with the decisions — an exec should get the
  state of play from the first half-page.

> In short: management docs open with status and decisions, then compress the capability
> tour. They say what is live, what is moving, what is uncertain, and what needs a call.

---

## What both share

- The same document structures (`document-templates.md`) and the same module pattern.
- The same monochrome PDF template and the project's configured language(s).
- The same integrity rules: nothing invented, gaps flagged, maturity honest.
- The same fixed ordering of products and modules, so a reader moving between the two
  audiences finds the same things in the same places.
