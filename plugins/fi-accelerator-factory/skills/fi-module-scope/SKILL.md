---
name: fi-module-scope
description: "Select only the Field Inspection modules a customer needs and emit a tailored package.xml, resolving module dependencies. Use when scoping an engagement, 'which modules', 'pick modules', 'tailor the footprint', 'generate a subset package', or deciding what to deploy for a client."
---
<!-- served-playbook -->
# fi-module-scope

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "fi-accelerator-factory", "skill": "fi-module-scope"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Fi accelerator factory**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
