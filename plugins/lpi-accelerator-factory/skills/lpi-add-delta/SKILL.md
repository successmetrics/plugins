---
name: lpi-add-delta
description: "Add a single delta — a new report, dashboard, form, flow, permit/license type, field, or small feature — to an ALREADY-generated LPI engagement without re-running lpi-generate-implementation. Use when the user says 'add a report to a client', 'add a new form', 'add a permit type to the existing build', 'new dashboard for a client', 'ship this change to a client without regenerating', or 'incremental deploy'. Authors the delta in the correct tier, emits a scoped additive package.xml, and records it in the engagement delta-log. Never regenerates, never re-runs seeds."
---
<!-- served-playbook -->
# lpi-add-delta

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "lpi-accelerator-factory", "skill": "lpi-add-delta"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Lpi accelerator factory**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.

Scripts the playbook names live in this skill's `scripts/` directory.
