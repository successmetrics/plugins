---
name: psd-orchestrate-build
description: "Drive a Salesforce Public Sector design to deployed, tested, version-controlled code through a closed build-test-fix loop with GitHub and Jira. Creates a Jira Epic per requirement and a Story per use case, a feature branch per use case, generates metadata via the official forcedotcom/sf-skills, generates tests from acceptance criteria, validates and fixes errors iteratively, deploys, opens a PR, and updates traceability. Use after .sfdesign/design.yaml exists and the user wants to build, implement, generate, test, or deploy the implementation, or says 'build the design', 'run the loop', 'implement the requirements', 'check in the code', or 'deploy'. Final stage of the salesforce-pubsec-delivery pipeline; orchestrates the sf-dev-environment plugin (jira-to-implementation, dev-deploy-loop, code-review, pr-description)."
---
<!-- served-playbook -->
# psd-orchestrate-build

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "salesforce-pubsec-delivery", "skill": "psd-orchestrate-build"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Salesforce pubsec delivery**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
