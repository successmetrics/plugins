---
name: sc-add-delta
description: "Add a single delta — a new Case record type or support process, a queue or skill, an entitlement process version, a knowledge data category, a macro set, a report, a Help Center page — to an ALREADY-generated Service Cloud engagement without re-running sc-generate-implementation. Use when the user says 'add a queue to the client', 'new support process', 'version the Gold entitlement', 'add a report', 'ship this without regenerating', or 'incremental deploy'. Authors the delta in the engagement, emits a scoped additive manifest, records it in the delta log, and never regenerates or re-runs setup."
---
<!-- served-playbook -->
# sc-add-delta

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "sc-accelerator-factory", "skill": "sc-add-delta"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Sc accelerator factory**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
