# 311 Accelerator (`sm311`)

A packaged 311 / citizen service request product for Salesforce **Public
Sector Solutions on Service Cloud**, built by SuccessMetrics so a small or
mid-size city can go live in weeks on a fixed fee instead of a custom build.

Residents report a problem from their phone on a ready-made, city-branded
portal — as a guest or signed in with a Customer Community Login — see it on a
public map, are told if it is already reported, follow it under *My requests*,
and get an email at each step, including a photo of the finished work. Each
report is a PSS **Public Complaint**; the work is a **Case** in the right
department queue, and many reports can roll up to one case. Field crews resolve
it from the Salesforce mobile app.

## What is in the box (Starter tier, v0.2)

The full inventory is in [What comes out of the box](docs/OUT_OF_THE_BOX.md).
In short:

| Area | What it does |
|---|---|
| Resident portal | Prebuilt LWR site — home, report, map, check a request, my requests, sign in, register — branded from one `brand.yaml` (colours, fonts, logo, radius, extra CSS) |
| Resident accounts | Self-registration with Customer Community Login and Person Accounts; *My requests* shows only the resident's own reports |
| Intake | Mobile-first form: type tiles, "use my location" or GIS-checked address, duplicate check, details, contact (prefilled when signed in), photo |
| Reports and work | PublicComplaint per report, Case per problem, ComplaintCase junction, reporter as ComplaintParticipant; report status follows the case |
| Routing | Request type → department queue, target date, 311 record type |
| Close rule | Completion photo required before resolving, per type (supervisor override) |
| Field crews | *Complete Work* — photo, notes, resolve — on desktop and the Salesforce mobile app |
| Notices | Received (with Bookings link for appointment types), status update, resolved with the completion photo — to every reporter |
| Reports | Open by department, open by type, overdue, last 90 days |
| Request library | 29 request types across 9 categories with overridable defaults |

Everything a city decides lives in `city/<city>/city-config.yaml` and
`city/<city>/brand.yaml`, and is generated into the org by
`scripts/setup_city.sh`. The package itself is never edited per city.

**Mobile:** residents use the mobile-first portal (no app-store app); crews use
the Salesforce mobile app. **Office 365:** a Bookings link per appointment type
is built; calendar booking, Entra ID sign-on and Outlook/Teams are to be
discussed (see [Packages](docs/PACKAGES.md)).

## Factory skills (`311-accelerator-factory`)

The repo is also a Claude plugin, built the way the LPI accelerator is: the
skills under `.claude/skills/` are stubs, and their procedures are served by
`sm-agent-core` (decision §29). Install the plugin, connect its `sm-agent-core`
connector, and ask for a city — "stand up 311 for <city> from these notes".

| Skill | What it does |
|---|---|
| `311-generate-implementation` | A new city: requirements → a deployed, gated build |
| `311-org-resolve` | Is this org ready? (`tools/check_org.py`) |
| `311-module-scope` | Which parts the city needs, and what it is told it is not getting |
| `311-license-check` | Licences the scope triggers, and the ones it does not |
| `311-request-library` | Choosing, tuning and authoring request types |
| `311-test` | The build gate after setup (`tools/check_city_build.py`) |
| `311-add-delta` | One change to a live city |

## Layout

```
force-app/            the sm311 package (unlocked 2GP, no namespace, API 66)
portal/template/      the ready-made LWR site, city-neutral
portal/brand/         brand stylesheet template
library/              request-type library (29 types)
city/<city>/          city-config.yaml + brand.yaml (demo = deployable sample, union-city = draft)
tools/                configure_city.py (generator), check_org.py (is the org ready), check_city_build.py (build gate)
scripts/              setup_city.sh, create_demo_org.sh, give_admin_a_role.apex
templates/            decision register and delta log, copied into each city
.claude/, .claude-plugin/  the factory plugin (stub skills over served playbooks)
tests/                generator and org-check tests (pytest)
docs/                 out of the box, enablement, setup, questionnaire, packages, architecture, verification
```

## Quick start (demo org)

```bash
pip install pyyaml pytest
python3 -m pytest tests -q                       # generator tests
scripts/create_demo_org.sh sm311-pss             # PSS scratch org + package + demo city + portal + Apex tests
```

The script prints the portal address at the end.

## Documents

- [What comes out of the box](docs/OUT_OF_THE_BOX.md) — everything a city gets, by audience
- [Enabling a city](docs/CUSTOMER_ENABLEMENT.md) — six-week plan, licences, staff access and training, resident launch
- [Setup guide](docs/SETUP_GUIDE.md) — implementer's step-by-step, prerequisites to go-live
- [City questionnaire](docs/CITY_QUESTIONNAIRE.md) — what to ask the city; every answer maps to a config key
- [Packages](docs/PACKAGES.md) — Starter / Plus / Enterprise, mobile and Office 365 positions
- [Access, notifications and approvals](docs/SECURITY_AND_NOTIFICATIONS.md) — permission sets, emails, staff alerts, scheduled jobs; why no approval process ships
- [Architecture](docs/ARCHITECTURE.md) — data model, flows, security model
- [Third-party notices](docs/THIRD_PARTY_NOTICES.md) — Lucide icons used on the portal
- [Verification](docs/VERIFICATION.md) — what has been proven against a real org, and what has not
