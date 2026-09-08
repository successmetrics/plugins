---
name: check-config
description: Display and update saved Salesforce, GitHub, and JIRA credentials for the sf-dev-environment plugin. Use when the user says "check my config", "show my credentials", "what org am I using", "show dev environment settings", "what GitHub repo is configured", "check JIRA settings", "update my org alias", "change my GitHub token", or "show environment config".
---
<!-- served-playbook -->
# check-config

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "sf-dev-environment", "skill": "check-config"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Sf dev environment**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
