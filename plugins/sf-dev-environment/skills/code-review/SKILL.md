---
name: code-review
description: Review staged or changed files against loaded coding rules and Salesforce best practices before committing or deploying. Use when the user says "review my changes", "check my code", "review before commit", "audit my code", "check for issues", "review staged files", "run a code review", "check code quality", "look for problems in my changes", "review this PR", or "check my code against the rules". Modelled on Augment's automated code review capability.
---
<!-- served-playbook -->
# code-review

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "sf-dev-environment", "skill": "code-review"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Sf dev environment**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
