---
name: code-review
description: "Review changed SALESFORCE source — Apex, LWC, flows, validation rules, permission sets and profiles, page layouts, packaging — against the loaded coding rules before a deploy or a commit. Checks what a generic reviewer cannot see: field-level security and persona access, sharing and record visibility, governor limits and bulkification, SOQL in loops, test-context gaps, managed-package and namespace rules. Use for 'review my Salesforce changes', 'review this metadata', 'check my Apex', 'review staged files before I deploy', 'check my code against the rules', 'will this break FLS or sharing'. For code that is not Salesforce, the generic engineering code-review skill applies instead."
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
