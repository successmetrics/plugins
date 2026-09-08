# sm-agent-core

SuccessMetrics delivery methodology, served as an agent tool surface.

## The boundary

This repo has exactly one rule, and everything else follows from it:

> **The model is the IP. The artifact is not.**

Judgment — estimating velocities, phase ratios, design heuristics, calibration
against actuals — lives server-side in `server/src/sm_agent_core/methodology/`
and is never distributed. Rendering, file I/O, and org access live in the
client plugin, which ships to anyone.

| Layer | Distributed? | Contains |
|---|---|---|
| `server/.../methodology/` | **Never** | Velocities, ratios, prompts, calibration. The vault. |
| `server/.../tools/` | Never | Tool implementations that read the vault. |
| `plugin/` | Yes — org-managed | Thin orchestrators. No method, no numbers. |
| `marketplace/` | Yes | Plugin catalogue for Claude org sync. |

CI enforces this. `scripts/check_leak.py` fails the build if any vault constant
or fingerprint appears under `plugin/` or `marketplace/`. Do not weaken it —
its whole purpose is to stop a well-meaning future engineer from "fixing" a
broken skill by pasting the method back into plaintext.

## Layout

```
server/      FastMCP service (Python, streamable HTTP) — deploy to Railway
plugin/      sm-delivery: thin client skills + local Excel renderer
marketplace/ .claude-plugin/marketplace.json for Claude org sync
scripts/     leak gate
docs/        architecture, ops
```

## Quickstart

```bash
cd server
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env          # add SM_API_KEYS
pytest                        # unit tests
python -m sm_agent_core.server   # serves on :8080/mcp
```

Leak gate:

```bash
python scripts/check_leak.py
```

## Documentation

Read in this order:

| Doc | For | Answers |
|---|---|---|
| `docs/governance.md` | Everyone | The five principles, access rules, versioning, release process |
| `docs/playbooks.md` | Everyone who edits a skill | Skills are stubs; the procedure is served — where it lives and how to change it (§24) |
| `docs/provisioning.md` | Core team | Issuing, approving and revoking engagement keys; the `/admin` page |
| `docs/onboarding-offshore.md` | Delivery team | Setup, how to contribute, the G0–G4 gates |
| `docs/architecture.md` | Engineers | Why the client/server split falls where it does |
| `docs/auth-roadmap.md` | Core team | Access control stages, key → OAuth path |
| `docs/deploy-railway.md` | Core team | Hosting, DNS, connector setup, ops |
| `CHANGELOG.md` | Everyone | What changed, when, in which version line |

## Status

First slice: `sm_estimate`. Ported from the `loe-estimator` skill, whose
method was previously shipped in readable prose to every plugin recipient.
Estimation is **internal-only** — see governance principle 2.
