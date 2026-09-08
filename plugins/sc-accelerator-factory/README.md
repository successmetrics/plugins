# Service Cloud Accelerator

A reusable, generic **Service Cloud** accelerator — Case support processes, Entitlements and
milestones, Omni-Channel routing, Lightning Knowledge, a self-service Help Center — and the
factory that turns a support organisation's requirements into a tailored implementation on top
of it. Not public-sector case management; no Public Sector Solutions dependency.

Start with `CLAUDE.md`. The judgment (module selection, licence detection, org assessment,
the rule set behind the gate) is served by `sm-agent-core`; this repo holds patterns, a gate,
and skills that instruct without containing.

## Plugin

`sc-accelerator-factory` — skills `sc-generate-implementation`, `sc-assess`, `sc-module-scope`,
`sc-license-check`, `sc-test`, `sc-add-delta`. Declares its own connection to the engine; authorize
it once under Settings → Plugins → Connectors.
