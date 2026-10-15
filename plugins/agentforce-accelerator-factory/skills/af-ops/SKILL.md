---
name: af-ops
description: "Agent Ops for a live Agentforce agent — rerun its test library on Salesforce release previews, after the org upgrades, after Knowledge or source changes and monthly; compare with the last scorecard; open regression findings with both answers and the Builder trace; publish the customer scorecard. Use when the user says 'agent ops', 'release regression', 'check the agent after the release', 'is the agent still accurate', 'monthly agent check', 'scorecard for the customer', or on a schedule."
playbook_version: "1.0.0"
playbook_digest: "e36d57db2d6d3550"
---
<!-- served-playbook -->
# af-ops

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "agentforce-accelerator-factory", "skill": "af-ops"}` and follow the playbook it returns
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
