---
name: 311-module-scope
description: "Select the 311 footprint a city needs — intake and routing core, resident portal and accounts, field completion on mobile, GIS address check, duplicates and the public map, appointments, notices, reporting — resolving dependencies, and turn the answer into the city config switches. Use when scoping a 311 engagement, 'which modules', 'what does this 311 build involve', 'tailor the footprint', 'do they need the portal', or before estimating."
playbook_version: "1.0.0"
playbook_digest: "911cd2f39cd0453b"
---
<!-- served-playbook -->
# 311-module-scope

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "311-accelerator-factory", "skill": "311-module-scope"}` and follow the playbook it returns
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
