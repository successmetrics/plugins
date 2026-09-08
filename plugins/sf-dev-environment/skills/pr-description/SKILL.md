---
name: pr-description
description: Auto-generate a comprehensive pull request description from git diff, commit history, and linked JIRA ticket context. Use when the user says "write a PR description", "generate PR description", "write PR notes", "create PR body", "describe my changes", "write the pull request description", "generate release notes", or "summarize my PR". Modelled on Augment's auto-generated PR descriptions feature.
---
<!-- served-playbook -->
# pr-description

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "sf-dev-environment", "skill": "pr-description"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Sf dev environment**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
