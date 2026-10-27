---
name: 311-license-check
description: "Detect the Salesforce licences a 311 scope triggers — Public Sector Solutions seats and the Public Sector Access licence, Customer Community Login for residents who sign in, and the add-ons a city might ask for (SMS, an AI assistant, Knowledge authors, surveys, Salesforce Maps, Field Service) — and name what the scope does NOT need. Use when analysing 311 requirements, 'what licenses do we need', 'do residents need a licence', 'do crews need Field Service', or before pricing a 311 engagement."
playbook_version: "1.1.0"
playbook_digest: "65935069a0af9982"
---
<!-- served-playbook -->
# 311-license-check

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "311-accelerator-factory", "skill": "311-license-check"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

This file's frontmatter records the playbook version and digest it was
published against. To be served that exact version or refused, pass it as
`pin` — unlike `known_digest`, a mismatched `pin` refuses rather than warns.
Leave `pin` out to follow head.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **311 accelerator factory**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
