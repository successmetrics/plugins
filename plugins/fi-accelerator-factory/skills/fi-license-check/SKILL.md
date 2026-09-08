---
name: fi-license-check
description: "Detect the Salesforce add-on LICENSE dependencies a Field Inspection engagement's scope triggers (PSF-A-FS Field App / Axsy / Mobile App Plus briefcase for mobility+dispatch tiers, Salesforce Maps, ArcGIS estate, Experience Cloud, DocGen, Shield, identity/SSO) and call them out in the design. Use when analyzing requirements, 'what licenses do we need', 'license dependencies', 'do we need Field Service or Maps', or before pricing/deploying an engagement."
---
<!-- served-playbook -->
# fi-license-check

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "fi-accelerator-factory", "skill": "fi-license-check"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Fi accelerator factory**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
