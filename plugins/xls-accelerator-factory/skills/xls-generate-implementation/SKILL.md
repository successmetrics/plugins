---
name: xls-generate-implementation
description: "Turn a customer's spreadsheet application into a tailored Salesforce implementation on top of the Excel Accelerator product, without forking the product. Use when the user shares a workbook and says 'migrate this spreadsheet', 'move this to Salesforce', 'new engagement', 'onboard a client', 'what would this look like as an app', 'replace this workbook', or drops an .xlsx into an engagement inbox. Orchestrates the local shape read, tab classification, object and field mapping, calculation targeting, the stays-outside conversation, module scoping, licence detection, and the decision register a human signs."
---
<!-- served-playbook -->
# xls-generate-implementation

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "xls-accelerator-factory", "skill": "xls-generate-implementation"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Xls accelerator factory**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
