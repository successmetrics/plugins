---
name: psd-requirements
description: "Ingest and normalize customer requirements for a Salesforce Public Sector Solutions engagement, enrich them with web research, map each to a PSS module, and flag out-of-the-box vs. custom fit. Use when the user provides customer requirements, an RFP, a discovery document, meeting notes, or a transcript and wants them turned into structured Salesforce requirements; or says 'analyze these requirements', 'start a PSS design', 'build requirements', or names PSS modules like Licensing/Permitting/Inspections, Complex Case Management, Grantmaking, Field Service, Service Cloud, or Experience Cloud. First stage of the salesforce-pubsec-delivery pipeline; writes .sfdesign/requirements.yaml."
---
<!-- served-playbook -->
# psd-requirements

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "salesforce-pubsec-delivery", "skill": "psd-requirements"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Salesforce pubsec delivery**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
