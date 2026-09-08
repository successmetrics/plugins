---
name: sm-review-design
description: "Get senior-architect pushback on a proposed Salesforce Public Sector design before anyone builds it — standard-before-custom alternatives, external and portal access, record ownership, screen completeness, and the basics a quality gate would later fail on. Use when the user has a design, data model or solution approach and asks to 'review this design', 'challenge this', 'is this the right approach', 'have we considered alternatives', 'sanity check the data model', 'will this work for portal users', or before a design review or build kickoff."
---
<!-- served-playbook -->
# sm-review-design

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "sm-delivery", "skill": "sm-review-design"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Sm delivery**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
