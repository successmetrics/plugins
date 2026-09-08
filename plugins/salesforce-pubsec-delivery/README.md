# Salesforce Public Sector Delivery

A delivery pipeline that turns **customer requirements** into a **deployed Salesforce Public Sector Solutions (PSS)** implementation — through a chain of skills that hand off structured artifacts, and that **reuse the official [`forcedotcom/sf-skills`](https://github.com/forcedotcom/sf-skills)** for all platform-level metadata generation and deployment.

## The pipeline

```
Customer input + web research
        │
   psd-requirements   →  .sfdesign/requirements.yaml
        │
   psd-use-cases      →  .sfdesign/use-cases.yaml      (personas, Gherkin acceptance criteria)
        │
   psd-design         →  .sfdesign/design.yaml         (PSS-aware SF design)
        │                 .sfdesign/traceability.md     (req → use case → design → build)
        │
   psd-orchestrate-build  ──delegates──▶  forcedotcom/sf-skills generators
        │   (closed loop)                  (objects, fields, validation rules,
        │                                   permission sets, sharing, flows, LWC,
        │                                   OmniStudio) → platform-metadata-deploy
        │
        ├── psd-verify ─▶ tests generated from Gherkin acceptance criteria (the gate)
        │
        └──────────────────────────────▶  sf-dev-environment (Jira → branch → implement → deploy/fix → PR)
```

Each skill reads the previous stage's artifact and writes the next. The artifacts in `.sfdesign/` are the real deliverable — versionable, reviewable, and the audit trail for public-sector clients.

## Skills

| Skill | Input | Output | Purpose |
|-------|-------|--------|---------|
| `psd-start` | — | `.sfdesign/` + sf-skills installed | Bootstrap a delivery project; ensure official sf-skills are available |
| `psd-requirements` | customer docs, notes | `requirements.yaml` | Normalize + web-enrich requirements; map each to a PSS module and flag OOTB vs. custom |
| `psd-use-cases` | `requirements.yaml` | `use-cases.yaml` | Personas, flows, and **Gherkin** acceptance criteria with traceability |
| `psd-design` | `use-cases.yaml` | `design.yaml`, `traceability.md` | Translate to a Salesforce design **against standard PSS objects first**; emit a build map naming the official sf-skill for each element |
| `psd-verify` | `use-cases.yaml`, `design.yaml` | tests + per-criterion results | Generate tests from Gherkin acceptance criteria, run them, report pass/fail — the **definition-of-done gate** |
| `psd-orchestrate-build` | `design.yaml` | tested, deployed, PR'd metadata | Closed build-test-fix loop: Jira Epic/Story, feature branch per use case, generate via official sf-skills, verify, deploy, open PR, update traceability |

## Closed-loop delivery (Augment-style)

The build stage does not assume its output is correct. For each use case it creates a Jira **Story** (under an **Epic** per requirement), cuts a **feature branch**, generates metadata via the official sf-skills, generates **tests from the acceptance criteria**, runs a **validate-first** gate that **parses errors and fixes them iteratively** (up to 5 passes), deploys to the sandbox, then opens a **PR** linked back to Jira and updates the traceability matrix. A use case is "done" only when every Gherkin criterion passes. The loop primitives (`jira-to-implementation`, `dev-deploy-loop`, `code-review`, `pr-description`) come from the installed **`sf-dev-environment`** plugin; this plugin supplies the PSS design and the orchestration. See `skills/psd-orchestrate-build/references/closed-loop-delivery.md`.

**Requires** the `sf-dev-environment` plugin configured via `psd-start` (Salesforce sandbox, GitHub repo/token, Jira project/token, coding-rule sources).

## Design principle: standard PSS first

Public-sector projects fail when teams over-customize. Every skill is biased to **use out-of-the-box PSS capability** — Licensing/Permitting/Inspections, Complex Case Management, Grantmaking, Business Rules Engine (BRE) for eligibility, OmniStudio for guided intake, Action Plans, Field Service, Service Cloud + Omni-Channel, Experience Cloud — and to introduce custom objects/fields/code only where OOTB genuinely falls short. See `skills/psd-design/references/pss-data-model.md`.

## Reuse of `forcedotcom/sf-skills`

This plugin deliberately does **not** reimplement metadata generation. The official Salesforce repo is refreshed frequently and owns:
`platform-custom-object-generate`, `platform-custom-field-generate`, `platform-validation-rule-generate`, `platform-permission-set-generate`, `platform-sharing-rules-generate`, `automation-flow-generate`, `experience-lwc-generate`, `omnistudio-*`, `platform-apex-generate`, `platform-metadata-deploy`, and more.

Install/refresh them with:

```bash
npx skills add forcedotcom/sf-skills
```

`psd-start` does this for you and `psd-orchestrate-build` routes work to them. The mapping lives in `skills/psd-design/references/sf-skills-map.md`.

## Human-in-the-loop gates

Approval is expected between **requirements → use cases → design → build**. Nothing is generated as metadata until the design is signed off; nothing deploys without the deploy gate in `psd-orchestrate-build`.
