---
name: xls-license-check
description: "Detect the Salesforce licences a spreadsheet-migration scope triggers — the user licence itself (Platform vs a full CRM licence, decided by whether the workbook has a people tab), Business Rules Engine, Big Objects, Salesforce Connect, Experience Cloud, Document Generation, Shield and the integration effort behind every pasted extract. Use when analysing a workbook, 'what licences do we need', 'Platform or Sales Cloud', 'do we need Business Rules Engine', 'how much will this cost', or before pricing a migration."
---
<!-- served-playbook -->
# xls-license-check

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "xls-accelerator-factory", "skill": "xls-license-check"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Xls accelerator factory**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
