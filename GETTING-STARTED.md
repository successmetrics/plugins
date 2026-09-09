# Getting started — for a customer or partner

Everything a new engagement needs, on one page: what you receive from us,
how to install, how to use it, and what to do when something refuses.

*(Published as `GETTING-STARTED.md` in <https://github.com/successmetrics/plugins>;
`docs/welcome-email.md` is the covering note that points here.)*

There are exactly two things: a **plugin** you install in Claude (Cowork or
Claude Code), and an **engagement key** we issue. Nothing else to configure.

---

## 1. What you receive

**An engagement key.** It looks like `sm_<engagement>_<random>`, it is yours
alone, it names your engagement, and it expires (90 days by default; we
re-issue). Treat it like a password: paste it where asked, never into a
document, a ticket or a chat. If you did not get one, request it at
<https://agents.successmetrics.io/request-access> — a person reviews every
request and replies by email.

**The name of the plugin(s) for your engagement**, from this list:

| Plugin | Use it for |
|---|---|
| `sm-delivery` | Any Salesforce engagement: assess an existing org, scope, licence check, design review, quality gates, finding triage, spreadsheet-to-platform migration |
| `lpi-accelerator-factory` | Public Sector Licensing, Permitting & Inspections on the LPI Accelerator |
| `grant-accelerator-factory` | Public Sector Grantmaking on the Grant Accelerator |
| `fi-accelerator-factory` | Asset inventory and field inspection on the Field Inspection Accelerator |
| `sc-accelerator-factory` | A Service Cloud support organisation (no Public Sector dependency) |
| `xls-accelerator-factory` | Replacing a spreadsheet application with a platform application |
| `salesforce-pubsec-delivery` | The requirements → use cases → design → build pipeline for PSS |
| `sf-dev-environment` | Deploy loops against Salesforce, GitHub and Jira |

The plugins are public and free to download. They are deliberately thin:
each skill knows *when* it applies and asks our service for *how* when it
runs. Without a key, an installed plugin does nothing.

---

## 2. Install (ten minutes, once per person)

### Cowork (Claude desktop app)

1. **Customize → Plugins → Personal plugins → +** → **Add marketplace** →
   **Add from a repository** → `successmetrics/plugins`.
2. Install the plugin(s) named for your engagement.
3. Open the plugin → **Connectors** → `sm-agent-core` → **Connect**. If the
   dialog shows *Client ID* and *Client Secret*, leave both empty.
4. A browser page opens asking for your engagement key. Paste it, press
   **Authorize**.
5. Start a **new** session. The tools appear in it.

### Claude Code (terminal)

```
/plugin marketplace add successmetrics/plugins
/plugin install sm-delivery@successmetrics        # and any accelerator plugin
```

The first skill that needs the service prompts you to connect; approve it,
paste the key on the page that opens, then start a new session.

You are never asked for a GitHub account, a token, or repository access.
The key is exchanged for a short-lived token that renews itself; the key is
not stored by your client. Each plugin connects separately — authorizing
`sm-delivery` does not authorize `lpi-accelerator-factory`; connect each.

### Local tools (engineers only)

`sm-gates` (quality gates), `sm-collect` (org inventory) and `sm-workbook`
(spreadsheet shape) run on your machine or in your CI, next to your metadata,
your `sf` CLI auth and your files — which never leave it.

```bash
pip install -r https://raw.githubusercontent.com/successmetrics/plugins/main/tools/requirements.txt
export SM_API_KEY='sm_…'          # the same engagement key
cd <your Salesforce project> && sm-gates run
```

GitHub Actions: `uses: successmetrics/plugins/tools/gates-action@main` with
`api-key: ${{ secrets.SM_API_KEY }}`. Details and checksums:
<https://github.com/successmetrics/plugins/tree/main/tools>.

---

## 3. Use it

Say what you want, in your own words. The skills fire from their
descriptions; you do not name them.

- "Assess this org before we design anything" → org inventory (local) →
  `sm_assess_fit` → a verdict, conflicts and the decisions you must make.
- "Here are the RFP and the discovery notes — generate an implementation
  for the City of X" → the accelerator's factory: requirements, use cases,
  licence dependencies, module scope, resolver, extension scaffold, docs.
- "Which add-on licences does this scope trigger?" → `sm_license_check`.
- "Run the gates" / "is the build green?" → `sm-gates` locally, findings
  triaged by `sm_triage_findings` where your key allows it.
- "Add a report to the existing build without regenerating" → the
  add-delta skill.

Each skill fetches its procedure from the service at the start of a session
and follows it. The procedure carries the steps, the gates and the reference
documents, at your key's tier — so a corrected procedure reaches you the next
session, with no plugin update.

**What the tools will not do:** guess an org's API names (the resolver blocks
on ambiguity), design against a brownfield org before it is assessed, or
report a gate as passed when it could not run (exit code 2, on purpose).

**What we can see:** which engagement called which tool, when, and how often.
Not your metadata, not your data, not your workbook's values — the local
tools send names, counts and shapes only, and the scrubber refuses anything
else.

---

## 3b. People on the engagement who do not have the plugin

Not everyone needs a key. A developer or tester who has a Salesforce sandbox,
the `sf` CLI, Git and access to the engagement repository works in the
**developer lane**: their whole process is the one-page
`docs/DEVELOPER_QUICKSTART.md` in the engagement repo — own sandbox, one
ticket = one branch = one pull request, build in Setup, retrieve the named
metadata into the branch, open the PR with three lines (what changed, how it
was tested in the sandbox, ticket number). They never write a manifest, run a
gate or touch a generated file.

A plugin holder then **lands** that PR (`scripts/land_pr.sh` in the engagement
repo, or the add-delta skill's landing entry): delta number, manifest built
from the diff, gates, verification of the ticket's acceptance criteria in a
sandbox the developer did not use, delta-log row, merge, deploy. The landed PR
is a delta like any other.

Two rules keep the lanes honest: nobody builds in the shared integration org
(it runs `main`, deployed by a plugin holder), and a developer PR is never
merged as is. Anyone who ends up doing more than a handful of tickets should
be given a key and the plugin — ask us; the developer lane is how people
start, not where they stay.

---

## 4. When something refuses

| You see | It means | Do |
|---|---|---|
| "That key was not accepted" | Wrong key, or the whole `key:engagement:…` line was pasted | Paste the first field only |
| "Unrecognised or revoked API key" | Expired or revoked | Ask us for a re-issue |
| "…carries no usable scopes" | Issued without the scopes the tool needs | Ask us — our side |
| A tool is missing from the list | This plugin's connector is not authorized yet, or the session predates it | Connect it (step 3 above), start a new session |
| A tool refuses by tier | The tool is above your key's tier | Expected; ask if you think the tier is wrong |
| The client never opens a browser page | Wrong service URL in the client | It must be `https://agents.successmetrics.io/mcp` |
| `sm-gates` exits 2 | It could not run — no metadata, no rules, or an unusable contract | Read the message; `--allow-no-metadata` only if that is a decision |

Anything else: reply to the email that carried your key, with the message
text and the tool name.

---

## 5. Keys, plainly

- One key per engagement, named to a person. Share within the engagement
  team by asking us for one per person — it costs nothing and lets us revoke
  one without disturbing the others.
- Revocation takes effect on the next call. Nothing to uninstall.
- Rotation: we issue the new key, you authorize the connector again, we
  revoke the old one.
- We never ask for your key back, and we cannot read it out of the service —
  only its hash is stored. Lost = re-issued.
