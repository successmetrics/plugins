---
name: 311-org-resolve
description: "Check a target org before a 311 build — the Public Sector Solutions complaint objects (PublicComplaint, ComplaintCase, ComplaintParticipant), Person Accounts, Experience Cloud, the Public Sector Access and Customer Community Login licences, a check-only deploy of the sm311 package, and the brownfield signals: another program already using Public Complaints, existing Case record types and statuses. Use when pointing the 311 accelerator at a sandbox or production, 'check the org', 'is this org ready for 311', 'resolve org names', 'can we install sm311 here', or before setup_city.sh."
playbook_version: "1.0.0"
playbook_digest: "b8efcc20346f8dff"
---
<!-- served-playbook -->
# 311-org-resolve

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "311-accelerator-factory", "skill": "311-org-resolve"}` and follow the playbook it returns
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
