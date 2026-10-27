---
name: sm-quality-gates
description: "Run the SuccessMetrics quality gates against a Salesforce engagement repository, and wire them into its CI. Covers installing sm-gates, interpreting its findings and exit codes, writing a test contract with justified suppressions, and checking that the rules being enforced are still canon. Use when the user asks to 'run the tests', 'run the gates', 'check the basics', 'lint this metadata', 'is the build green', 'gate the deploy', 'test-first', 'test plan for this build', 'what tests does this engagement need', 'set up CI for this engagement', 'why did the gate fail', or before any deploy or delta. This is the gate for an engagement with no accelerator installed; where a product line has its own, that line's *-test skill covers what is specific to it."
trigger_precedence:
  # Decision 27 (revised 2026-09-22): the seven generic test-gate phrases.
  # The two PSS-shaped ones stay with lpi-test. Reasoning in decisions.md.
  - run the tests
  - gate the deploy
  - check the basics
  - is the build green
  - test-first
  - test plan for this build
  - what tests does this engagement need
playbook_version: "1.5.0"
playbook_digest: "fcfcc9f6662000a5"
---
<!-- served-playbook -->
# sm-quality-gates

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "sm-delivery", "skill": "sm-quality-gates"}` and follow the playbook it returns
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
