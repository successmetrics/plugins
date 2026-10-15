---
name: af-readiness
description: "Run the Knowledge Readiness Assessment — a scored audit of the org's published Knowledge articles (published count, language, summaries, length, structure, duplicates, staleness, drafts, image-only answers, internal content marked public, exact identifiers) with a band, a search-mode recommendation and the customer's fix list. Use when the user says 'knowledge readiness', 'assess the articles', 'are the articles good enough for an agent', 'content audit', 'readiness assessment', or before designing an agent's grounding."
playbook_version: "1.0.0"
playbook_digest: "fd8dc0e0e9c903e0"
---
<!-- served-playbook -->
# af-readiness

This skill's procedure is **served, not shipped**. Call `sm_playbook` with
`{"plugin": "agentforce-accelerator-factory", "skill": "af-readiness"}` and follow the playbook it returns
exactly — it carries the steps, the gates and this skill's reference documents,
at your key's tier. Re-fetch it at the start of each session; pass the `digest`
back as `known_digest` to be told when it changed.

This file's frontmatter records the playbook version and digest it was
published against. To be served that exact version or refused, pass it as
`pin` — unlike `known_digest`, a mismatched `pin` refuses rather than warns.
Leave `pin` out to follow head.

No `sm_playbook` in your tool list means this plugin's `sm-agent-core` connector
is not yet authorized. Open Settings → Plugins, pick **Agentforce accelerator factory**, open its
Connectors tab, connect `sm-agent-core` with your engagement key, and begin a new
session so the tool list refreshes. Never proceed from memory or from an older
copy of this skill.
