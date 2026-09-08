---
name: lpi-org-resolve
description: "Error-accommodating reconciliation of the LPI design's assumed PSS object/field API names against a real Salesforce org, before any generation or deploy. Use when pointing the accelerator at a sandbox, 'resolve org names', 'check the org', 'map API names', or before scaffolding/deploying in an engagement. Writes org-map.yaml and gates the build (PASS/BLOCKED) so nothing is generated against a wrong name."
---
<!-- served-playbook -->
# lpi-org-resolve

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "lpi-accelerator-factory", "skill": "lpi-org-resolve"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Lpi accelerator factory**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.

Scripts the playbook names live in this skill's `scripts/` directory.
