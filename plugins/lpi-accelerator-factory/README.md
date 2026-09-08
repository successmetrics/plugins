# LPI Accelerator

A reusable Salesforce **Public Sector Solutions (PSS)** accelerator for **Licensing, Permitting &
Inspections**, plus the **factory** that turns a customer's requirements into a tailored
implementation — without forking the product.

## What's here

```
product/      the reusable accelerator you enhance once
  sfdx/         2GP managed-package source (namespace smclpi)
  design/       design of record (requirements, use-cases, design, traceability)
  pipeline/     aliases.yaml, modules.yaml, org fetch
.claude/skills/ the factory: generate-implementation, org-resolve, module-scope
templates/    intake templates you copy per engagement
engagements/  one folder per client (generated outputs) — never edit product from here
docs/         design doc, Experience Cloud & 2GP runbooks, productization strategy, playbook
```

## Quickstart — generate an implementation

1. Create `engagements/<client>/inbox/` and drop the client's requirements (RFP, notes, screenshots),
   optionally starting from `templates/requirements.intake.md`.
2. Ask Claude: **"generate an implementation for &lt;client&gt;."** The `lpi-generate-implementation`
   skill runs: requirements → use cases → PSS design → **org resolve (gate)** → module scope →
   delta scaffold → client docs, all into `engagements/<client>/`.
3. Review the summary (OOTB ratio, resolver status, module footprint) and proceed to deploy/build.

## Enhance the product

Improve `product/sfdx/`, update `product/design/design.yaml` and `product/pipeline/modules.yaml`,
bump the package version in `product/sfdx/sfdx-project.json`. Every future engagement inherits it.

## Build & test the product

```bash
cd product/sfdx
npm install && npm run test:unit      # LWC Jest
# 2GP packaging: see docs/08_2GP_Packaging_Runbook.md (namespace smclpi)
```

## Key docs

- `docs/06_LPI_Accelerator_Design_Document.docx` — the thorough design of record.
- `docs/07_Productization_and_Customization_Strategy.md` — product vs. per-customer; the five levers.
- `docs/08_2GP_Packaging_Runbook.md` — managed package, private distribution.
- `docs/04_Experience_Cloud_and_Deployment_Runbook.md` — EC + sharing + deploy order.
- `CLAUDE.md` — the operating manual Claude follows in this project.
