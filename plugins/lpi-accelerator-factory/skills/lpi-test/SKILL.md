---
name: lpi-test
description: "Test-first quality gate for LPI (and Grants-ready) engagements. Asserts the basics that must ALWAYS be present — list views, related lists, detail-page fields, quick actions per record type, persona access — plus runs the Apex and Jest suites, as ONE gate that blocks the deploy on critical failures. Use when the user says 'run the tests', 'test-first', 'gate the deploy', 'check the basics', 'verify list views / related lists / quick actions / persona access', 'is the build green', 'add a test for this customer', 'set up the engineering pipeline / branch / commit / traceability', or before ANY engagement_deploy.sh / bootstrap_org.sh / lpi-add-delta. Also answers 'what tests does this engagement need' and 'test plan for this build' for a SALESFORCE build specifically — persona and channel contexts, flow branch and fault paths, refusal paths, money invariants, portal run-as. A testing strategy for anything that is not a Salesforce build belongs to the generic engineering testing-strategy skill."
playbook_version: "1.1.0"
playbook_digest: "c0663469b99d3298"
trigger_precedence:
  # sm-agent-core decision 27. A phrase may be declared by exactly one
  # claimant; two produce CONTESTED. This does not change what the model
  # picks -- it records which skill is supposed to win.
  #
  # Narrowed on 2026-09-22. This skill used to declare all nine test-gate
  # phrases, which made lpi-test the supposed winner of a bare "run the
  # tests" for the four product lines that are not LPI. What is left here
  # is the two phrases that name PSS artifacts and therefore really are
  # this line's: everything generic moved to sm-quality-gates, which is
  # product-agnostic. The siblings -- fi, grant, sc, xls -- keep offering
  # every phrase they offered before; only the declaration moved.
  - add a test for this customer
  - verify list views / related lists / quick actions / persona access
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
