---
name: af-case-triage
description: "Case documentation and routing for a service team on Service Cloud: classify each case by reason and sub-reason from the agency's own rules, record the member details it states, route it to the right queue, suggest next steps from the agency's guidance, and draft a plain-language status update a rep approves — with an accuracy set and agent tests written first. Use when the user says 'case triage', 'classify cases', 'route cases to queues', 'case reason and sub-reason', 'case documentation agent', 'member status summary', 'auto-route cases', or 'next steps on a case'."
playbook_version: "1.0.0"
playbook_digest: "9faa3d61ccdadfca"
---
<!-- served-playbook -->
# af-case-triage

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "agentforce-accelerator-factory", "skill": "af-case-triage"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

This file's frontmatter records the playbook version and digest it was
published against. To be served that exact version or refused, pass it as
`pin` — unlike `known_digest`, a mismatched `pin` refuses rather than warns.
Leave `pin` out to follow head.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Agentforce accelerator factory**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
