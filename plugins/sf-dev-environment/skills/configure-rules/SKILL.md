---
name: configure-rules
description: Register external rule sources - GitHub repositories, local files, or URLs - that Claude should learn from and apply during Salesforce development and code fixes. Use when the user says "add my Salesforce rules", "point to my coding standards", "load rules from GitHub", "add a rules file", "configure my development rules", "teach Claude my coding standards", "add rules from a repo", "load my CLAUDE.md", "add my .cursorrules", or "update my rules". Rules are loaded automatically during the deploy loop and applied when fixing errors.
---
<!-- served-playbook -->
# configure-rules

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "sf-dev-environment", "skill": "configure-rules"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Sf dev environment**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
