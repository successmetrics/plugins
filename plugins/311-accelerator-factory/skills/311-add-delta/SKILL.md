---
name: 311-add-delta
description: "Add a single change to a LIVE 311 city without regenerating it — a new request type, a changed target or photo rule, a new department or queue, a status, new notice wording, a brand or footer change, switching guest reporting off — through the city config and setup, recorded in the delta log of the city. Use when the user says 'add a request type to <city>', 'change the target days', 'new department', 'rebrand the portal', 'add a report to a client', 'ship this change without regenerating', or 'incremental deploy'."
playbook_version: "1.0.0"
playbook_digest: "a021cff5bacf69d9"
---
<!-- served-playbook -->
# 311-add-delta

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "311-accelerator-factory", "skill": "311-add-delta"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

This file's frontmatter records the playbook version and digest it was
published against. To be served that exact version or refused, pass it as
`pin` — unlike `known_digest`, a mismatched `pin` refuses rather than warns.
Leave `pin` out to follow head.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **311 accelerator factory**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
