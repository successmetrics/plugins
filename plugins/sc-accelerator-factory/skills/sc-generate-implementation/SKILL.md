---
name: sc-generate-implementation
description: "Turn a support organisation's requirements into a tailored, generic Service Cloud implementation on top of the Service Cloud Accelerator — Case support processes, Entitlements and milestones, Omni-Channel routing, Lightning Knowledge, self-service Help Center — without forking the product and without Public Sector Solutions. Use when the user shares requirements (RFP, discovery notes, transcript, screenshots of the current desk, an existing org) and says 'generate an implementation', 'new engagement', 'build <company>'s support desk', 'set up their contact center', 'onboard a client', or drops files into an engagement inbox. Orchestrates org assessment, requirements normalisation and triage, licence detection, module scoping, lifecycle-first design, the extension scaffold, the gate, and docs-as-you-go. Not public-sector case management."
---
<!-- served-playbook -->
# sc-generate-implementation

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "sc-accelerator-factory", "skill": "sc-generate-implementation"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Sc accelerator factory**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
