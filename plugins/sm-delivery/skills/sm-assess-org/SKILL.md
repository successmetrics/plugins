---
name: sm-assess-org
description: "Assess an existing Salesforce org BEFORE designing against it: collect an inventory with the sf CLI, get conflicts and decisions from sm_assess_fit, and gate the pipeline on the verdict. Use when the user says 'assess the org', 'is this org greenfield', 'what will collide', 'run the assessment', 'can we build this here', 'brownfield check', when an engagement targets any org that already has users or data, or BEFORE sm-scope-engagement's design work and any estimate for an existing org."
playbook_version: "1.0.0"
playbook_digest: "0152432d23093033"
trigger_precedence:
  # sm-agent-core decision 27: a phrase naming a PHASE that happens
  # before a product line is chosen goes to sm-delivery, because at
  # that moment nobody yet knows which accelerator applies.
  - brownfield check
  - assess the org
  - what will collide
---
<!-- served-playbook -->
# sm-assess-org

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "sm-delivery", "skill": "sm-assess-org"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

This file's frontmatter records the playbook version and digest it was
published against. To be served that exact version or refused, pass it as
`pin` — unlike `known_digest`, a mismatched `pin` refuses rather than warns.
Leave `pin` out to follow head.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Sm delivery**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
