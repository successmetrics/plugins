---
name: xls-map-design
description: "Turn workbook-inventory.json into a Salesforce design: what each tab actually is, the objects and fields it implies, where every calculation lands (formula field, roll-up, Business Rules Engine decision matrix or expression set, record-triggered or scheduled flow, Apex, or a report), what stays outside the platform, and the normalisation decisions a human must sign. Use after xls-read-workbook, or when the user asks 'what objects does this imply', 'where should these formulas go', 'should this be Apex or a formula', 'what stays in the old system', or 'map this workbook'."
---
<!-- served-playbook -->
# xls-map-design

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "xls-accelerator-factory", "skill": "xls-map-design"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Xls accelerator factory**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
