---
name: 311-request-library
description: "Browse, clone, tune and author request types (pothole, streetlight, graffiti, illegal dumping and the rest) from the request library of the 311 Accelerator — category, department, target days, photo rule, duplicate radius, public map, appointment — into the city config. Use when choosing request types for a city, 'what request types do we have', 'add a request type', 'add a pothole type', 'library of 311 types', or when a city needs a type the library lacks."
playbook_version: "1.0.0"
playbook_digest: "9fd83e1c40cbbc84"
---
<!-- served-playbook -->
# 311-request-library

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "311-accelerator-factory", "skill": "311-request-library"}` and follow the playbook it returns
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
