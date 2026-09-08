---
name: lpi-content-library
description: "Browse, clone, validate, and author pre-built permit-type content packages (forms, stage models, fee matrices, inspection and document checklists) from the LPI Accelerator's content library. Use when scoping or building an engagement's permit types, 'what permit types do we have', 'clone a permit type', 'add a reroof/electrical/demolition permit', 'library of permit types', or when authoring a new reusable type. Types clone into engagements — the library is never forked."
---
<!-- served-playbook -->
# lpi-content-library

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "lpi-accelerator-factory", "skill": "lpi-content-library"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Lpi accelerator factory**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
