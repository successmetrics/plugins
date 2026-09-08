---
name: psd-start
description: "Bootstrap a Salesforce Public Sector delivery project: create the .sfdesign/ working directory, install the official forcedotcom/sf-skills, configure GitHub + Jira + Salesforce credentials and coding rules for the closed-loop build, and explain the requirements → use-cases → design → build pipeline. Use at the start of a PSS engagement, when the user says 'start a Salesforce public sector project', 'set up the pipeline', 'connect GitHub and Jira', 'install the Salesforce skills', or 'kick off the design', or before running psd-requirements for the first time."
---
<!-- served-playbook -->
# psd-start

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "salesforce-pubsec-delivery", "skill": "psd-start"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Salesforce pubsec delivery**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
