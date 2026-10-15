---
name: sm-migrate-workbook
description: "Turn a spreadsheet application into a Salesforce design: read the workbook to shape, classify what each tab actually is, map columns to fields, decide where every calculation lands (formula field, roll-up, Business Rules Engine, flow, Apex or a report), and name what should stay outside the platform. Use when the user has an Excel or Google Sheets application to migrate and says 'migrate this spreadsheet', 'move this workbook to Salesforce', 'what would this look like as an app', 'design objects from this workbook', 'replace this spreadsheet', or drops an .xlsx into an engagement. Covers both platform apps and workbooks that turn out to have a CRM inside them."
playbook_version: "1.0.0"
playbook_digest: "934d6ce2641bbff7"
trigger_precedence:
  # sm-agent-core decision 27: a phrase naming a PHASE that happens
  # before a product line is chosen goes to sm-delivery, because at
  # that moment nobody yet knows which accelerator applies.
  - migrate this spreadsheet
  - what would this look like as an app
---
<!-- served-playbook -->
# sm-migrate-workbook

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "sm-delivery", "skill": "sm-migrate-workbook"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

This file's frontmatter records the playbook version and digest it was
published against. To be served that exact version or refused, pass it as
`pin` — unlike `known_digest`, a mismatched `pin` refuses rather than warns.
Leave `pin` out to follow head.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Sm delivery**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
