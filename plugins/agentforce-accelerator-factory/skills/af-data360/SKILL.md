---
name: af-data360
description: "Member status from several systems through Data 360 (Data Cloud): the fit check first, then data streams, mapping, a custom status object, identity resolution across the systems and Salesforce, a data graph an agent reads in one call, and the Apex status source and case-agent action that read it — with the platform's traps, the agent user's access, and a Flex Credit estimate. Use when the user says 'Data 360', 'Data Cloud', 'member status from PeopleSoft', 'one member across systems', 'identity resolution', 'unified profile', 'data graph', 'zero copy', 'Snowflake', or 'do we need Data Cloud for this'."
playbook_version: "1.0.0"
playbook_digest: "eb80521404bdf55a"
---
<!-- served-playbook -->
# af-data360

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "agentforce-accelerator-factory", "skill": "af-data360"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

This file's frontmatter records the playbook version and digest it was
published against. To be served that exact version or refused, pass it as
`pin` — unlike `known_digest`, a mismatched `pin` refuses rather than warns.
Leave `pin` out to follow head.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Agentforce accelerator factory**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
