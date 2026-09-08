---
name: lpi-test
description: "Test-first quality gate for LPI (and Grants-ready) engagements. Asserts the basics that must ALWAYS be present — All list views, curated related lists, correct detail-page fields, quick actions per record type, and persona-based access — plus runs the Apex and Jest suites, as ONE gate that blocks build/deploy on critical failures. Use when the user says 'run the tests', 'test-first', 'gate the deploy', 'check the basics', 'verify list views / related lists / quick actions / persona access', 'is the build green', 'add a test for this customer', 'set up the engineering pipeline / branch / commit / traceability', or before ANY engagement_deploy.sh / bootstrap_org.sh / lpi-add-delta. Contract-driven: extend per customer via engagements/CLIENT/design/test-contract.yaml, never by editing the product."
---
<!-- served-playbook -->
# lpi-test

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "lpi-accelerator-factory", "skill": "lpi-test"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Lpi accelerator factory**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.

Scripts the playbook names live in this skill's `scripts/` directory.
