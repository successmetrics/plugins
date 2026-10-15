---
name: sc-module-scope
description: "Select the Service Cloud configuration footprint an engagement needs — Case foundation and support processes, Omni-Channel routing, entitlements and milestones, Lightning Knowledge, self-service Help Center, messaging channels, voice, agent productivity, reporting, surveys, Agentforce for Service — resolving dependencies. Use when scoping a support-desk engagement, 'which modules', 'what does this build involve', 'tailor the footprint', 'do they need Omni', or before estimating."
playbook_version: "1.0.0"
playbook_digest: "af9bd3a2277c6a51"
trigger_precedence:
  # sm-agent-core decision 27. lpi wins the module-scope family, but does
  # not OFFER this phrase -- only sc and xls do -- so declaring it there
  # would be stale on arrival. It goes to a claimant instead.
  - what does this build involve
---
<!-- served-playbook -->
# sc-module-scope

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "sc-accelerator-factory", "skill": "sc-module-scope"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Sc accelerator factory**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
