---
name: psd-verify
description: "Turn Gherkin acceptance criteria from Public Sector use cases into executable Salesforce tests, run them against the target org, and report pass/fail and coverage per criterion. Use when the user wants to verify a build, generate tests from acceptance criteria, prove a use case is done, check acceptance criteria, run the verification gate, or says 'test this', 'verify UC-001', 'are the acceptance criteria met'. The verification gate of the salesforce-pubsec-delivery pipeline; invoked by psd-orchestrate-build before a use case is marked done."
---
<!-- served-playbook -->
# psd-verify

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "salesforce-pubsec-delivery", "skill": "psd-verify"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Salesforce pubsec delivery**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
