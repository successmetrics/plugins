---
name: af-voice-calls
description: "Contact center call intelligence on Salesforce Voice: every call logs itself after it ends — transcript, a wrap-up the rep approves, caller sentiment with the quoted line, a QA score with quoted evidence, a case when there is none — from NICE CXone, Webex Contact Center, Amazon Connect or an Agentforce Voice call, or from a simulated transcript for a demo. Use when the user says 'call wrap-up', 'call summary', 'QA scoring', 'score the calls', 'call sentiment', 'log the calls', 'VoiceCall', 'call transcript', 'NICE' or 'Webex' with Salesforce."
playbook_version: "1.0.0"
playbook_digest: "cac9370b4d5a24f6"
---
<!-- served-playbook -->
# af-voice-calls

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "agentforce-accelerator-factory", "skill": "af-voice-calls"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

This file's frontmatter records the playbook version and digest it was
published against. To be served that exact version or refused, pass it as
`pin` — unlike `known_digest`, a mismatched `pin` refuses rather than warns.
Leave `pin` out to follow head.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Agentforce accelerator factory**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
