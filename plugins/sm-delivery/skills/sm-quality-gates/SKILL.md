---
name: sm-quality-gates
description: "Run the SuccessMetrics quality gates against a Salesforce engagement repository, and wire them into its CI. Covers installing sm-gates, interpreting its findings and exit codes, writing a test contract with justified suppressions, and checking that the rules being enforced are still canon. Use when the user asks to 'run the gates', 'check the basics', 'lint this metadata', 'is the build green', 'gate the deploy', 'set up CI for this engagement', 'why did the gate fail', or before any deploy or delta."
---
<!-- served-playbook -->
# sm-quality-gates

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "sm-delivery", "skill": "sm-quality-gates"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Sm delivery**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
