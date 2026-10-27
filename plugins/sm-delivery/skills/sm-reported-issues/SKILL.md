---
name: sm-reported-issues
description: "Turn a tester's or customer's list of reported issues into a verdict table: for each item, bug, regression, gap, by design or needs info, judged against the engagement's behaviour contract, with the rule, the evidence, the root cause, the bug class and the regression test to add. Use when the user says 'the testers reported these', 'go through the UAT feedback', 'is this a bug or by design', 'the customer sent a list of problems', 'triage the tester's list', 'which of these UAT issues are real', 'write up the round', or pastes a list of UAT or customer issues."
playbook_version: "1.0.0"
playbook_digest: "8a299b0ea40cd26b"
---
<!-- served-playbook -->
# sm-reported-issues

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "sm-delivery", "skill": "sm-reported-issues"}` and follow the playbook it returns
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
