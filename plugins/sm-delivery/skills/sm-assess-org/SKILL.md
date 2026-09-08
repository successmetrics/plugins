---
name: sm-assess-org
description: "Assess an existing Salesforce org BEFORE designing against it: collect an inventory with the sf CLI, get conflicts and decisions from sm_assess_fit, and gate the pipeline on the verdict. Use when the user says 'assess the org', 'is this org greenfield', 'what will collide', 'run the assessment', 'can we build this here', 'brownfield check', when an engagement targets any org that already has users or data, or BEFORE sm-scope-engagement's design work and any estimate for an existing org."
---
<!-- served-playbook -->
# sm-assess-org

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "sm-delivery", "skill": "sm-assess-org"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Sm delivery**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
