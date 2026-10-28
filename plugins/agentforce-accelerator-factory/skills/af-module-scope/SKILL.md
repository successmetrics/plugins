---
name: af-module-scope
description: "Select the Agentforce workstreams an engagement needs — the grounded assistant, knowledge readiness, agent actions into records, a public channel, Agent Ops, additional languages — from the customer's requirements, and name what they are not getting. Use when the user says 'scope the agent', 'which agent workstreams', 'what does this agent project include', 'tailor the footprint', or before estimating an Agentforce engagement."
playbook_version: "1.1.0"
playbook_digest: "e66a41bb9897c16a"
---
<!-- served-playbook -->
# af-module-scope

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "agentforce-accelerator-factory", "skill": "af-module-scope"}` and follow the playbook it returns
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
