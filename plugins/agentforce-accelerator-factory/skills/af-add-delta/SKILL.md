---
name: af-add-delta
description: "Add one change to a live Agentforce agent — a new topic or intent, a new source, an instruction fix, a new action, a changed refusal — without rebuilding it: change the design, add its test cases first, re-render, publish to the test sandbox, rerun the whole library and record the scorecard row. Use when the user says 'add a topic to the agent', 'the agent got this wrong', 'add a question', 'add an action', 'new source for the agent', 'tune the agent', or 'incremental change to the agent'."
playbook_version: "1.0.0"
playbook_digest: "b4f9479e9625c634"
---
<!-- served-playbook -->
# af-add-delta

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "agentforce-accelerator-factory", "skill": "af-add-delta"}` and follow the playbook it returns
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
