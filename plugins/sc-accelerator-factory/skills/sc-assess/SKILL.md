---
name: sc-assess
description: "Assess an existing Salesforce org BEFORE designing a Service Cloud implementation on it: run the collector's service sections (queues and members, assignment rules, entitlement processes and milestones, Omni routing and presence configs, messaging channels, case status and origin shape, knowledge shape, retired surfaces) and hand the inventory to sm_assess_fit for the routing-collision, SLA-collision, status-model, queue-sprawl, retired-surface and knowledge findings. Use when the user says 'assess the org', 'what will collide', 'is Omni already on', 'what are they standing on', 'brownfield check', or before sc-generate-implementation against any org that has users or cases."
---
<!-- served-playbook -->
# sc-assess

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "sc-accelerator-factory", "skill": "sc-assess"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Sc accelerator factory**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
