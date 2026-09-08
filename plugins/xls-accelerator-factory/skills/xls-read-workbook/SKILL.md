---
name: xls-read-workbook
description: "Read a customer's workbook to SHAPE — sheet and column labels, inferred types, counts, and the formula graph with literals removed — and write workbook-inventory.json. Cell values never leave the machine. Use when the user says 'read the workbook', 'what is in this spreadsheet', 'inventory the file', 'profile this xlsx', or before any mapping. Also use to diagnose a partial read or a redaction refusal."
---
<!-- served-playbook -->
# xls-read-workbook

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "xls-accelerator-factory", "skill": "xls-read-workbook"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Xls accelerator factory**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
