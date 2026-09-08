---
name: sm-estimate
description: "Build a Salesforce project estimate — a Basis of Estimate (BOE) of effort per item, then a Level of Effort (LOE) timeline with phases, staffed team and cost. Use when the user asks to 'estimate', 'build an LOE', 'BOE', 'level of effort', 'staffing plan', 'project duration', 'how many sprints', 'how many hours', 'price a project', or wants a delivery timeline and team for a Salesforce/PSS implementation. Produces a four-tab Excel."
---
<!-- served-playbook -->
# sm-estimate

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "sm-delivery", "skill": "sm-estimate"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Sm delivery**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
