---
name: sm-triage-findings
description: "Turn a wall of gate findings into a short list worth acting on. Takes the JSON from `sm-gates run`, returns a verdict per finding — real, false positive, accepted risk, or needs-human — with reasoning and a draft suppression you commit. Use when the user says 'triage these findings', 'which of these are real', 'the gate returned 44 findings', 'are these false positives', 'help me work through the gate output', 'draft the suppressions', or after any gate run big enough that nobody is going to read all of it."
playbook_version: "1.1.0"
playbook_digest: "891bec42767a3746"
---
<!-- served-playbook -->
# sm-triage-findings

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "sm-delivery", "skill": "sm-triage-findings"}` and follow the playbook it returns
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

Scripts the playbook names live in this skill's `scripts/` directory.
