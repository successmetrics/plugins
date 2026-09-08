---
name: configure-environment
description: Set up or update Salesforce, GitHub, and JIRA credentials for the sf-dev-environment plugin. Use when the user says "configure environment", "set up credentials", "update Salesforce org", "change GitHub token", "update JIRA settings", "set up dev environment", or "configure SF/GitHub/JIRA". Walks through each service conversationally and saves to a local config file.
---
<!-- served-playbook -->
# configure-environment

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "sf-dev-environment", "skill": "configure-environment"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Sf dev environment**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
