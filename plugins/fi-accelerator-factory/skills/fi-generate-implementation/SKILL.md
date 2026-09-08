---
name: fi-generate-implementation
description: "Turn a public-sector asset-inspection customer's requirements into a tailored implementation on top of the Field Inspection Accelerator product, without forking it. Use when the user shares requirements (RFP, discovery notes, transcript) and says 'generate an implementation', 'new engagement', 'onboard a client', or 'build the agency's inspection program'. Orchestrates requirements normalization, org resolve, module scope, and per-engagement delta scaffolding (asset types, InspectionTypes, condition scales, seed data) into an engagements/CLIENT folder."
---
<!-- served-playbook -->
# fi-generate-implementation

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "fi-accelerator-factory", "skill": "fi-generate-implementation"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Fi accelerator factory**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
