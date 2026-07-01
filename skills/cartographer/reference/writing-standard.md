# Writing standard — stakeholder documentation

This is the **source of truth for HOW to write** every stakeholder document Cartographer
produces. It is consulted on every `/generate`. The workflow lives in SKILL.md; the
audience profiles live in `audiences.md`; the section skeletons and project-file formats
live in `document-templates.md`.

The standard is project-agnostic. Where an example helps, a neutral illustration is used;
none of it is specific to any one product or company.

---

## 1. Purpose & audience

These documents keep a **communication/marketing team and non-technical stakeholders**
informed about a software ecosystem and its products. They are a shared reference and a
single source of truth for how things are described publicly and internally.

- **Write for:** communication teams, business stakeholders, partners, leadership —
  people who need to understand *what* exists and *why it matters*.
- **Do not write for:** developers, integrators, or API consumers. This is not technical
  documentation.
- **Test every sentence:** "Would a smart non-technical reader understand this and find it
  useful?" If it needs implementation knowledge to parse, rewrite or cut it.

---

## 2. The core standard — level of detail

This is the defining rule.

> **Describe WHAT each component does and WHY it matters. Never describe HOW it is built.**

Aim one level below a marketing tagline and one level above technical documentation:
concrete and credible, with enough specifics to be trusted, but no mechanisms. Every
technical fact must be **translated into plain functional or value language** before it
appears.

> **Generation context — read this carefully.** Cartographer generates from *source code
> repositories*, where the raw input is exactly the HOW the standard forbids (frameworks,
> protocols, schemas, ports). The discipline is therefore inverted from writing from a
> curated brief: you must *infer user-facing value and translate it*, never transcribe
> what you see. See SKILL.md §"Grounding discipline" for which surfaces to read and which
> to ignore.

### Exclude entirely

Frameworks and languages (web framework, backend language), protocols and transport
(REST, gRPC, MQTT, LoRaWAN, JWT, websockets), datastores and data-layer concepts
(database engines, schemas, row-level isolation, geospatial extensions), ports,
infrastructure, repository names, internal version numbers, endpoint names, entity/field
counts, and any auth mechanism described mechanically.

### Translate — don't drop

Keep the *capability*, lose the *mechanism*. This table shows the kind of translation
expected; it is illustrative, not exhaustive.

| Technical reality (source) | How it is expressed for stakeholders |
|---|---|
| Per-tenant schema / data isolation | "Each customer's data is kept completely separate and secure" |
| JWT, API keys, role-based access control | "Each person sees only what their role and subscription allow" |
| Single API gateway service | "A single, secure entry point" / "one secure gateway" |
| Real-time pub/sub, websockets | "In real time, within seconds" |
| Journey-planning engine | "Plan multi-step journeys" / "a planning engine" |
| Realtime data feeds | "Live status and alerts" |
| Automatic translation service | "Translated automatically" / "in their own language" |
| IoT ingestion (LoRaWAN/MQTT) | "Receives sensor readings in real time" |
| Actuator command API | "Send commands to equipment in the field" |
| Operator impersonation / act-as | "Administrators can temporarily act as a user to provide support" |
| Progressive web app | "Installable on your device like an app" |

### Keep as-is (credible proof points the audience values)

Production status and reach ("live on the App Store and Google Play"), number of supported
languages, export formats (PDF / Excel / CSV), editorial workflow states (draft → review →
publish — functional, not technical), and consumer-facing third parties only (Google /
Apple / email sign-in, YouTube / Vimeo embeds).

### Granularity guide

Be specific about **functions**, never about **plumbing**. "Shift scheduling, payroll,
inspections, fuel logs, incident reports" is the right level. "A scheduling endpoint backed
by a relational table" is not. When a domain acronym is unavoidable, introduce it
functionally — name what it does for the user — rather than defining it technically.

### Substance over metaphor (the quality bar)

The reader must come away knowing concretely **what was built**. Lead every section with
real, repeatable substance — the specific things a team does or gets — and use analogy only
to frame that substance, never to replace it.

- **Failing (tagline drift):** "Work Orders is the day-to-day heartbeat of the portal — a
  window onto everything that keeps a building moving."
- **Passing (substance first):** "Work Orders is where maintenance is run: jobs are created,
  assigned to a technician, and tracked to closure, including fuel logs and incident
  reports." A single framing line ("the engine of the portal") may follow — but the concrete
  capability comes first.

Test each paragraph: *could a communication-team member repeat this to a stakeholder and
have actually told them something?* If it is all warmth and no specifics, rewrite it. One
anchoring analogy per section is plenty; more than that, and substance is being crowded out.

---

## 3. Voice & tone

- **Plain, warm, professional, confident — never hype.** State what something does plainly;
  let the capability impress.
- **Active voice, present tense.** "The portal manages…", not "is able to be used to
  manage…".
- **Close sections with a takeaway.** Many sections end with a one-line synthesis
  ("In short: …", "Think of it as…") that hands the reader the point.
- **Use anchoring analogies** for abstract structure: *backbone* (core shared data),
  *control room* (an admin portal), *front door* (a public website), *sibling modules*
  (two related features that play different roles).
- **One idea per sentence.** Short sentences. No nested clauses that require re-reading.

---

## 4. The module section pattern

When a product contains modules, each module follows the same shape (≈2–4 short
paragraphs), in a fixed order across releases so readers always find the same module in
the same place:

1. **A defining sentence** — what the module is and its role in the platform.
2. **A capabilities paragraph** — concrete, functional things teams can do with it
   (the *what*, never the *how*).
3. **A standout-capability callout** — the one differentiating thing that makes the module
   matter.
4. **A positioning line** — how it relates to a neighbouring module or to the end-user
   apps (e.g. "one feature tells the lasting story, its sibling sounds the timely alert").

---

## 5. Formatting conventions

- **Markdown.** `#` title, `##` sections, `###` module subsections.
- **Subtitle line** directly under the title, in italics:
  *A product of [organisation] · [document type] · [month year]*. (Lowercase months in
  languages that require it, e.g. Portuguese *junho de 2026*.)
- **Horizontal rules** (`---`) between major sections.
- **Bold** only for: bullet lead-in labels, product/module names on first mention in a
  flow, and a few key phrases. Never bold whole sentences.
- **One comparison table**, in the overview only (*Product / What it is / Who uses it*).
- **Bullets** are complete thoughts, one to two sentences; lead with a bolded label where
  the list is labelled.
- **Prose-forward with light structure** — headers for navigation, prose for substance.
  Avoid bullet-spam.
- **No contact or sales footer** in the body.
- **Length targets:** product docs ≈1–2 pages; a portal with many modules ≈4–5 pages;
  overview ≈3 pages. (Management-audience docs may run longer — see `audiences.md`.)

---

## 6. Language rules

- **Output language is per-project.** On the first assessment, Cartographer asks which
  language(s) to produce; the choice is stored in `Product-Map.md`. The default is
  **English**. When more than one language is configured, produce each.
- Each document is written to **read natively** in its language — never as a literal
  carry-over of another language's structure. Translate meaning, not word order.
- Some technical/business loanwords are conventionally left in English even in
  other-language documents (e.g. *back office, backend, feed, push, onboarding,
  stakeholders, clustering*). Use judgement per language and localise fully on request.
- Keep product and module name translations **consistent** across releases. If a project
  fixes specific name translations, record them in `Product-Map.md` so every refresh uses
  the same ones.

### Language appendix — European Portuguese (Pt-PT)

Applies only when Pt-PT is a configured language. Provided because it is a common target
and easy to get subtly wrong; the same care applies to any language.

- **Pt-PT vocabulary, never Brazilian.** Use: *telemóvel* (not celular), *ecrã* (not tela),
  *ficheiro* (not arquivo), *utilizador* (not usuário), *equipa* (not equipe), *autocarro*
  (not ônibus), *comboio* (not trem), *palavra-passe*, *gestão* (not gerenciamento),
  *conceção*, and the "estar a + infinitive" construction (not the gerund).
- Months lowercase (*junho de 2026*).
- Subtitle form: *Um produto da [organização] · [tipo de documento] · [mês ano]*.

---

## 7. Content integrity rules

- **Source of truth:** the repositories in the project, read through their value-bearing
  surfaces (see SKILL.md). Synthesize across them; never copy a README's structure or
  wording.
- **Flag gaps and risks proactively.** Where source material is thin, say so inline rather
  than inventing detail. (Worked example: a repo with no STAKEHOLDER.md, no docs folder,
  and a one-line README carries a note recommending the product team confirm scope before
  external publication.)
- **Be honest about maturity.** Note modules that are newest or partially in development
  rather than implying everything is complete. How in-progress work is surfaced depends on
  the audience — see `audiences.md`.
- **Never invent capabilities** not supported by the source. If you cannot ground a
  capability in a value-bearing surface, do not write it.
- **Worked examples chain only real links.** An end-to-end example (e.g. the overview's "How
  it all connects") is the easiest place to invent. Every hop in the chain must trace to
  something the sources actually support — if product A "publishes" and product B "displays",
  you may connect them; if nothing shows A's output reaching B, do not assert that it does.
  When a connection is plausible but unconfirmed, soften it ("can be") or leave it out, and
  note it as an assumption to confirm. A vivid example that implies an integration nobody
  built is worse than a plainer one that is true.
- **"How it fits in" must be concrete, not gestural.** When describing how a product relates
  to the others, name the actual flow — what moves from where to where, and what the reader
  gains — rather than asserting a vague "everything is connected". Each connection should be
  one a reader could verify against the sources.

---

## 8. Pre-delivery checklist

- [ ] No technical jargon survived — every mechanism translated to function or value.
- [ ] Each document follows its required section structure (`document-templates.md`).
- [ ] Each module follows the four-part pattern, in fixed order (§4).
- [ ] Voice is plain, active, present tense; sections close with a takeaway (§3).
- [ ] Produced in every configured language; native reading verified (§6).
- [ ] In-progress work handled per the audience profile (`audiences.md`).
- [ ] Gaps and maturity flagged honestly; nothing invented (§7).
- [ ] Filenames follow convention; `.md` and `.pdf` both present.
- [ ] PDF styling applied; diacritics confirmed rendering for accented languages.
