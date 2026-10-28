---
name: af-test
description: "Run an Agentforce agent's test library in Testing Center and record its accuracy scorecard — topic, action and outcome assertions per case, full and partial answers, results by kind, regressions against the previous run — and gate on it. Use when the user says 'test the agent', 'run the agent tests', 'score the agent', 'accuracy', 'did tuning help', 'is the agent green', or after any change to an agent."
playbook_version: "1.4.0"
playbook_digest: "2485191600aaa0dd"
---
<!-- served-playbook -->
# af-test

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "agentforce-accelerator-factory", "skill": "af-test"}` and follow the playbook it returns
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
