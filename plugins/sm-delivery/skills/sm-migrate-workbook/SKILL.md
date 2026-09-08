---
name: sm-migrate-workbook
description: "Turn a spreadsheet application into a Salesforce design: read the workbook to shape, classify what each tab actually is, map columns to fields, decide where every calculation lands (formula field, roll-up, Business Rules Engine, flow, Apex or a report), and name what should stay outside the platform. Use when the user has an Excel or Google Sheets application to migrate and says 'migrate this spreadsheet', 'move this workbook to Salesforce', 'what would this look like as an app', 'design objects from this workbook', 'replace this spreadsheet', or drops an .xlsx into an engagement. Covers both platform apps and workbooks that turn out to have a CRM inside them."
---
<!-- served-playbook -->
# sm-migrate-workbook

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "sm-delivery", "skill": "sm-migrate-workbook"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Sm delivery**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
