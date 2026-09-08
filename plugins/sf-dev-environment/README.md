# sf-dev-environment Plugin

Agentic Salesforce development loop for Cowork. Configure your SF org, GitHub repo, and JIRA project once — then trigger the full deploy → fix → commit → ticket update cycle with a single instruction.

## Skills

### `jira-to-implementation`
Take a JIRA ticket all the way to a merged PR without leaving Cowork.

**Trigger phrases:** "implement PROJ-123", "work on this ticket", "build the feature in JIRA", "take PROJ-123 from ticket to PR"

Full flow: fetch ticket → understand scope → scan codebase → plan tasks → implement → deploy to Salesforce → run code review → open GitHub PR → link PR back to JIRA ticket.

### `code-review`
Review changed files against your loaded rules and Salesforce platform best practices.

**Trigger phrases:** "review my changes", "check my code before commit", "run a code review", "audit my code", "review PR #42"

Findings are severity-graded (Critical / Major / Minor / Info). Optionally posts the review directly to a GitHub PR as a review comment with approve/request-changes.

### `pr-description`
Auto-generate a comprehensive PR description from git diff + JIRA ticket context.

**Trigger phrases:** "write a PR description", "generate PR notes", "describe my changes", "create the PR body"

Produces: summary, JIRA link, per-file change breakdown, test coverage notes, manual test steps, acceptance criteria coverage, and deployment notes. Can post directly to GitHub or copy to clipboard.

### `configure-rules`
Register GitHub repos, file URLs, or local files as rule sources Claude applies during all coding and fixes.

**Trigger phrases:** "add my Salesforce rules", "load rules from GitHub", "point to my coding standards", "add a rules file", "configure my development rules", "teach Claude my coding standards"

Supports:
- **GitHub repo URL** — Claude auto-discovers CLAUDE.md, RULES.md, .cursorrules, STANDARDS.md, CONVENTIONS.md, etc.
- **GitHub file URL** — link to a specific file
- **Local file path** — any markdown or text file on your machine
- **Confluence page URL** — pulls Confluence page content using your JIRA credentials (same auth)
- **Confluence space** — scans for pages with "standard", "guideline", "convention" in the title

Rules are fetched fresh on every deploy run and applied to all error fixes — naming conventions, forbidden patterns, required patterns, and code style preferences are all respected.

### `configure-environment`
Set up or update credentials for Salesforce, GitHub, and JIRA.

**Trigger phrases:** "configure environment", "set up credentials", "update my Salesforce org", "change GitHub token", "update JIRA settings"

Walks through each service conversationally. Credentials are saved to `~/.config/sf-dev-environment/config.json` with restricted permissions (600).

### `dev-deploy-loop`
Run the full agentic dev loop.

**Trigger phrases:** "deploy to Salesforce", "run the deploy loop", "deploy my changes", "deploy and fix errors", "deploy and check in"

What it does:
1. Reads your saved credentials
2. Runs `sf project deploy start` against your configured org
3. Parses errors → fixes code → redeploys (up to 5 iterations)
4. Commits and pushes to GitHub when clean
5. Adds a comment to the linked JIRA ticket

### `check-config`
View and update your saved credentials.

**Trigger phrases:** "check my config", "show my credentials", "what org am I using", "verify credentials"

Optionally runs connectivity checks against all three services.

## Requirements

- [Salesforce CLI](https://developer.salesforce.com/tools/salesforcecli) (`sf`) installed and authenticated
- Git initialized in your project directory
- JIRA API token from https://id.atlassian.com/manage-profile/security/api-tokens

## Credentials Storage

All credentials are stored locally at `~/.config/sf-dev-environment/config.json` with `chmod 600` permissions. Tokens are never printed in full — always masked in chat output.
