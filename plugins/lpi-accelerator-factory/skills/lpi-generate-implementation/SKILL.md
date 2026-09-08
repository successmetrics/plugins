---
name: lpi-generate-implementation
description: "Turn a customer's requirements into a tailored Salesforce Public Sector LPI implementation on top of the LPI Accelerator product, without forking the product. Use when the user shares requirements files (RFP, discovery notes, transcript, screenshots) and says 'generate an implementation', 'new engagement', 'build a city or agency', 'onboard a client', or drops files into an engagement inbox. Orchestrates requirements normalization, use cases, PSS design, org API-name resolution, module scoping, delta scaffolding, and client documents."
---
<!-- served-playbook -->
# lpi-generate-implementation

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "lpi-accelerator-factory", "skill": "lpi-generate-implementation"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Lpi accelerator factory**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
