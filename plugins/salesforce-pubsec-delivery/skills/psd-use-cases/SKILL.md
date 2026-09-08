---
name: psd-use-cases
description: "Turn structured Salesforce Public Sector requirements into detailed use cases with personas, main and alternate flows, and Gherkin acceptance criteria. Use after requirements exist (.sfdesign/requirements.yaml) and the user wants use cases, user stories, personas, acceptance criteria, or 'turn requirements into use cases' for a PSS engagement (Licensing/Permitting/Inspections, Complex Case Management, Grantmaking, Field Service, Service Cloud, Experience Cloud). Second stage of the salesforce-pubsec-delivery pipeline; writes .sfdesign/use-cases.yaml."
---
<!-- served-playbook -->
# psd-use-cases

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "salesforce-pubsec-delivery", "skill": "psd-use-cases"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Salesforce pubsec delivery**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
