---
name: jira-to-implementation
description: Read a JIRA ticket, understand the full scope, implement the required code changes, deploy to Salesforce, and open a GitHub pull request - all in one flow. Use when the user says "implement JIRA ticket", "work on PROJ-123", "fix PROJ-456", "implement this ticket", "build the feature in JIRA", "do the work for ticket", "take PROJ-123 from ticket to PR", or "implement and open a PR for a ticket". Modelled on Augment's 'Implement Issue #123 and open a pull request' capability.
---
<!-- served-playbook -->
# jira-to-implementation

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "sf-dev-environment", "skill": "jira-to-implementation"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Sf dev environment**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
