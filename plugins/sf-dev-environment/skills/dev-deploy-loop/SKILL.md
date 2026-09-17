---
name: dev-deploy-loop
description: Run the full agentic Salesforce development loop: deploy metadata to the org, read the deploy errors, fix, redeploy, commit to GitHub, update JIRA. Use for "deploy to Salesforce", "run the deploy loop", "deploy my changes", "push to SF", "deploy and fix errors", "deploy and check in", or a pre-deploy check of a Salesforce release (org deploy, tests, packaging). Reads credentials from the saved config file. A release that is not a Salesforce org deploy belongs to the generic engineering deploy-checklist skill.
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
