---
name: xls-test
description: "Test-first quality gate for a spreadsheet-migration engagement. Asserts the things that go wrong in THIS line specifically — a derived value stored as data, a rate left as a literal in a formula, an aggregate carried without its provenance, a period ladder stored instead of generated, an object with no list view replacing a tab people used to click — plus the standard basics and the Apex and Jest suites. Use when the user says 'run the tests', 'gate the deploy', 'check the basics', 'is the build green', or before ANY deploy or xls-add-delta."
---
<!-- served-playbook -->
# xls-test

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "xls-accelerator-factory", "skill": "xls-test"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Xls accelerator factory**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
