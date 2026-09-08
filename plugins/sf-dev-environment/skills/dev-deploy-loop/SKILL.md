---
name: dev-deploy-loop
description: Run the full agentic Salesforce development loop: deploy code, read errors, fix, redeploy, commit to GitHub, and update JIRA. Use when the user says "deploy to Salesforce", "run the deploy loop", "deploy my changes", "push to SF", "start the dev loop", "deploy and fix errors", "deploy and check in", or "run my Salesforce deployment". Reads credentials from the saved config file.
---
<!-- served-playbook -->
# dev-deploy-loop

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "sf-dev-environment", "skill": "dev-deploy-loop"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Sf dev environment**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
