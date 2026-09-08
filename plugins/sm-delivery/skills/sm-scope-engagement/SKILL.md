---
name: sm-scope-engagement
description: "Turn a customer's requirements — an RFP, discovery notes, a transcript, legacy screenshots — into a scoped Salesforce Public Sector engagement: structured requirements, matched pre-built content types, the module footprint to deploy, and the add-on licences the scope triggers. Use when the user shares requirements and asks to 'scope this', 'analyse these requirements', 'which modules do we need', 'what licences does this need', 'onboard a client', 'new engagement', or drops an RFP or discovery document. Covers LPI (licensing/permitting/inspections), Grantmaking and Field Inspection."
---
<!-- served-playbook -->
# sm-scope-engagement

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "sm-delivery", "skill": "sm-scope-engagement"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Sm delivery**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
