---
name: af-voice-after-hours
description: "After-hours and level-1 voice agent for a contact center on NICE CXone or Webex Contact Center: an Agentforce Service agent that answers calls the vendor hands over, verifies the caller before any member answer, reads document and enrollment status, answers rules questions from the agency's documents, and turns everything else into a callback case — with readiness checks, vendor playbooks and agent tests written first. Use when the user says 'after-hours line', 'answer calls after hours', 'level 1 calls', 'status calls', 'IVR overflow', 'voice agent', 'Agentforce Voice', 'where are my documents by phone', or 'hand calls from NICE or Webex to an agent'."
playbook_version: "1.0.0"
playbook_digest: "bff8459f4da6d91d"
---
<!-- served-playbook -->
# af-voice-after-hours

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "agentforce-accelerator-factory", "skill": "af-voice-after-hours"}` and follow the playbook it returns
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
