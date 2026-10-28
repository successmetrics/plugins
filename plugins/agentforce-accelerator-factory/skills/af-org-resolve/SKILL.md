---
name: af-org-resolve
description: "Check whether a Salesforce org is ready to build, ground and test an Agentforce agent — Agentforce and Einstein settings, Data Cloud provisioned, Knowledge enabled, namespace, API and CLI versions, Data Cloud access for the agent user, agents already in the org — and name the steps only a person can do in Setup. Use when the user says 'check the org for Agentforce', 'is this org ready for an agent', 'agent readiness', 'can we build the agent here', 'connect the build sandbox', or before the first agent build in an org."
playbook_version: "1.2.0"
playbook_digest: "f155ae683862eced"
---
<!-- served-playbook -->
# af-org-resolve

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "agentforce-accelerator-factory", "skill": "af-org-resolve"}` and follow the playbook it returns
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
