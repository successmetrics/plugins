---
name: 311-test
description: "Gate a 311 city build before anyone tests by hand — queues, list views, request types, record type, statuses that actually close, settings and the public portal address, the live site, guest access, the resident profile, GIS remote site, notice address, plus the Apex suite and the generator tests — one gate that blocks on failure and names what it did not check. Use when the user says 'run the 311 tests', 'gate the deploy', 'check the basics', 'is the build green', 'verify the city build', or after setup_city.sh and before UAT."
playbook_version: "1.1.0"
playbook_digest: "39ba9a6391bd848f"
---
<!-- served-playbook -->
# 311-test

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "311-accelerator-factory", "skill": "311-test"}` and follow the playbook it returns
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
