# SuccessMetrics plugin marketplace

## Adding this marketplace

It depends on the client. The first version of this file printed only
the Claude Code command, which is not a thing that exists in Cowork —
where most people reading it actually are.

**Cowork** — Cowork tab → **Customize** → **Plugins** → under
**Personal plugins**, the **+** button → **Add marketplace** →
**Add from a repository** → `successmetrics/plugins`.

**Claude Code**

```
/plugin marketplace add successmetrics/plugins       # inside a session
claude plugin marketplace add successmetrics/plugins # from a shell
/plugin install sm-delivery@successmetrics
```

This repository is public and read-only: installing needs no GitHub
account and no approval. What it holds is the *client* half of each
plugin — skill descriptions, stubs and local scripts. The procedures,
rules, thresholds and licence maps are served by `sm-agent-core` to a
session holding an engagement key, and are not in this repository or
its history.

No key yet? Request one at <https://agents.successmetrics.io/request-access>.

| plugin | version | description |
|---|---|---|
| `sm-delivery` | 0.9.0 | SuccessMetrics delivery tooling. |
| `lpi-accelerator-factory` | 0.7.0 | Factory skills for the Salesforce Public Sector LPI Accelerator: turn customer requirements into a tailored extension on one managed base product with editable unmanaged baseline workflows. |
| `grant-accelerator-factory` | 0.7.0 | Factory skills for the Salesforce Public Sector Grantmaking Accelerator: turn requirements into a tailored extension on one managed base. |
| `fi-accelerator-factory` | 0.4.0 | Factory skills for the Salesforce Public Sector Field Inspection Accelerator: turn a public-sector asset-inspection agency's requirements into a tailored extension on one managed base product. |
| `salesforce-pubsec-delivery` | 0.3.0 | Requirements-to-deployment delivery pipeline for Salesforce Public Sector Solutions. |
| `sf-dev-environment` | 0.2.0 | Configure and drive Salesforce, GitHub, and JIRA credentials for agentic dev loops - deploy, fix errors, commit, and update tickets automatically. |
| `xls-accelerator-factory` | 0.3.0 | Factory skills for the Excel-to-Salesforce Accelerator: turn a spreadsheet application into a platform application without guessing. |
| `sc-accelerator-factory` | 0.2.0 | Factory skills for the Service Cloud Accelerator: turn a support organisation's requirements into a tailored, generic Service Cloud implementation — Case support processes, Entitlements and milestones, Omni-Channel routing, Lightning Knowledge and a self-service Help Center — without forking the product and without Public Sector Solutions. |

The judgment runs on the service; these skills gather input, call it and
render the result.

Installing asks you for nothing. The first time a skill needs the service,
your client opens a page that asks for your engagement key; the key is
exchanged there for a token that expires. See `docs/connecting.md`.

`SM_API_KEY` is still how the **gates** authenticate — they run in your CI,
not in a client, and have no browser to be redirected to.

## This repository is GENERATED

**Do not edit anything here.** Every plugin folder is a copy, written by
`sm-agent-core/scripts/sync_marketplace.py --sync` from the plugin's home
repository. An edit made here is lost on the next sync and, worse, is a
copy of the method that nothing will keep in step.

Edit the skill in its home repo, then re-sync.

The copies exist because the accelerator repositories are private: this
marketplace is the only public surface, and the sync is the only path
into it — every file passes the leak gate (stub-only skills, no vault
passages) before it is written here.

```bash
python3 scripts/sync_marketplace.py --check   # exits 1 if any source moved on
python3 scripts/sync_marketplace.py --sync    # regenerate
```

`--check` compares the content of every skill file, not git metadata.
No file is written without the runtime guard reading it first.
