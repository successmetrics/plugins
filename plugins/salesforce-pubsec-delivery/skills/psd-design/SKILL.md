---
name: psd-design
description: "Translate Public Sector use cases into a Salesforce technical design — data model, fields, validation rules, ownership and sharing, roles, permission sets/groups, business processes (Flows and Business Rules Engine), OmniStudio, LWC, Experience Cloud sites, and integrations — built against out-of-the-box Public Sector Solutions objects first. Use after .sfdesign/use-cases.yaml exists and the user wants a Salesforce design, data model, design document, or solution architecture for a PSS engagement, or says 'design this', 'create the data model', 'map to Salesforce'. Third stage of the salesforce-pubsec-delivery pipeline; writes .sfdesign/design.yaml and .sfdesign/traceability.md, and tags every element with the official forcedotcom/sf-skill that will build it."
---
<!-- served-playbook -->
# psd-design

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "salesforce-pubsec-delivery", "skill": "psd-design"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Salesforce pubsec delivery**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
