---
name: sc-license-check
description: "Detect the Salesforce licences a Service Cloud scope triggers — the seat edition itself (Enterprise vs Unlimited), Knowledge user licences, Digital Engagement for messaging channels, Service Cloud Voice plus telephony, Experience Cloud for an authenticated Help Center, Agentforce for Service, Feedback Management, Slack swarming, Workforce Engagement, Field Service, CRM Analytics, Shield, identity, Data 360 — and name what is on the seat. Use when analysing requirements, 'what licences do we need', 'is Knowledge included', 'do we need Digital Engagement', 'what does WhatsApp cost', or before pricing a support-desk engagement."
---
<!-- served-playbook -->
# sc-license-check

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "sc-accelerator-factory", "skill": "sc-license-check"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Sc accelerator factory**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
