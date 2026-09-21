---
name: sm-draft-sow
description: "Draft the house Statement of Work from an estimate that already exists. Use when the user asks to 'draft a SOW', 'write the SOW', 'statement of work', 'turn the estimate into a SOW', 'put the LOE into our template', 'SOW from the BOE', 'update the SOW with the new numbers', or wants the fee table, delivery checkpoints, project plan or weekly staffing grid that go in one. Also for the contract-vehicle framing — CMAS, GSA, a master agreement — and for the T&M-capped-at-not-to-exceed fee language. It does not estimate: it consumes sm_boe_expand and sm_estimate output, so every hour in the document traces to the model. Produces a .docx on the house Implementation Services spine with a scope table by release, a project plan, a landscape staffing grid by week, a checkpoint grid of hours by capability and delivery phase, a basis-of-estimate fee table, and the assumption, exclusion, responsibility and general-terms sections."
---
<!-- served-playbook -->
# sm-draft-sow

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "sm-delivery", "skill": "sm-draft-sow"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Sm delivery**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.

Scripts the playbook names live in this skill's `scripts/` directory.
