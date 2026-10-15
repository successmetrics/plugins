---
name: xls-add-delta
description: "Add a single change — a new report, field, calculation, tab that turned up late, or small feature — to an ALREADY-generated spreadsheet-migration engagement without re-running xls-generate-implementation. Use when the user says 'they found another tab', 'add a field to the client', 'the rate changed', 'add a report to a client', 'ship this change without regenerating', or 'incremental deploy'. Authors the delta in the engagement, records it in the delta log, and never re-reads the whole workbook or re-runs the mapping."
playbook_version: "1.1.0"
playbook_digest: "29ba6b917b460c58"
---
<!-- served-playbook -->
# xls-add-delta

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "xls-accelerator-factory", "skill": "xls-add-delta"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Xls accelerator factory**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
