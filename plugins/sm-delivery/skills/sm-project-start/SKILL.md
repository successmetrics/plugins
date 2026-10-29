---
name: sm-project-start
description: "INTERNAL. Start a project — a delivery, a takeover of someone else's org, an org assessment or a pursuit: inventory what it was given (a reference application, an existing org, a backlog, one of our packages, an agent's knowledge, a SOW or RFP, or just a SOW and notes), draw the epic map with evidence and scope colours, assign week-one tasks by role, plan the workshops and build the kickoff deck and workshop packs. Use when the user says 'start the project', 'kick off the project', 'first week plan', 'week one tasks', 'kickoff deck', 'mobilise the team', 'prepare for the workshops', 'how do we start this project', 'plan the handover from the previous partner', 'week one of the takeover', 'bid plan for this RFP', or 'what do we share at kickoff'."
playbook_version: "1.2.0"
playbook_digest: "ef888539fcbe99cb"
---
<!-- served-playbook -->
# sm-project-start

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "sm-delivery", "skill": "sm-project-start"}` and follow the playbook it returns
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
