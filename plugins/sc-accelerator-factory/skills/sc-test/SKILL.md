---
name: sc-test
description: "Test-first quality gate for a Service Cloud engagement. Asserts the things a service build fails in ways a permit build does not — a closed-reading status that does not close, two owners of assignment, a Case queue with nobody in it, an entitlement process nobody is accountable for, a Help Center whose contact form bypasses assignment — plus the shared basics (list views, related lists, quick actions, persona access) via sm-gates. Use when the user says 'run the tests', 'gate the deploy', 'check the basics', 'is the build green', or before ANY deploy or sc-add-delta."
---
<!-- served-playbook -->
# sc-test

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "sc-accelerator-factory", "skill": "sc-test"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Sc accelerator factory**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
