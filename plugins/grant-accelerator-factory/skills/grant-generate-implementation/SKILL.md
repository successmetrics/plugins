---
name: grant-generate-implementation
description: "Turn a customer's requirements into a tailored Salesforce Public Sector Solutions Grantmaking implementation on top of the Grant Accelerator product, without forking the product. Use when the user shares requirements files (RFP, NOFO, discovery notes, transcript, screenshots) and says 'generate an implementation', 'new engagement', 'build an agency's grant program', 'onboard a client', or drops files into an engagement inbox. Orchestrates requirements normalization, use cases, PSS Grantmaking design, org API-name resolution, module scoping, delta scaffolding, CDS role design, fit-and-finish, and client documents."
---
<!-- served-playbook -->
# grant-generate-implementation

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "grant-accelerator-factory", "skill": "grant-generate-implementation"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Grant accelerator factory**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
