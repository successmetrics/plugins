---
name: af-generate-implementation
description: "Design, ground, build and publish an Agentforce agent end to end from a customer's use case — design document, grounding bake-off (Salesforce's documented method against alternatives on one test library), Data Library, Agent Script authoring from the base template, validate, publish, activate — without hand edits between build and green. Use when the user says 'build the agent', 'new Agentforce agent', 'generate the agent', 'agent from this use case', 'set up the grounding', 'create the data library', or starts an Agentforce engagement."
playbook_version: "1.0.0"
playbook_digest: "5e5cad4e92d8eea2"
---
<!-- served-playbook -->
# af-generate-implementation

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "agentforce-accelerator-factory", "skill": "af-generate-implementation"}` and follow the playbook it returns
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
