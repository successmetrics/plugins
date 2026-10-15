---
name: 311-generate-implementation
description: "Turn the 311 / citizen service request requirements of a city into a tailored implementation on Public Sector Solutions on top of the 311 Accelerator (sm311) — residents' reports as Public Complaints, the work as Cases in department queues, a branded resident portal with Customer Community Login, crews on the Salesforce mobile app — without forking the package. Use when the user shares 311 requirements for a city (RFP, account-executive notes, discovery notes, screenshots of their current 311 or SeeClickFix tool, an existing org) and says 'build a 311 for <city>', 'stand up 311 for a city', 'new 311 city', 'generate an implementation', 'onboard a client', or 'new engagement'. Orchestrates the org check, requirements triage, licences, module scope, the request-type library, the city config and brand file, setup, the build gate and the enablement plan."
playbook_version: "1.0.0"
playbook_digest: "4532ed4b016441ee"
---
<!-- served-playbook -->
# 311-generate-implementation

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "311-accelerator-factory", "skill": "311-generate-implementation"}` and follow the playbook it returns
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
