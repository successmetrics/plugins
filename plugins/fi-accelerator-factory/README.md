# Field Inspection Accelerator

A reusable Salesforce **Public Sector Solutions (PSS)** accelerator for **asset inventory, recurring
field inspection, condition scoring, GIS, and offline mobility** — the internal, regulator-driven
counterpart to the citizen-facing LPI (Licensing, Permitting & Inspections) accelerator.

It is a **sibling** of the LPI and Grants accelerators: a distinct product and go-to-market, built on
the **same delivery factory and shared base**, not a fork and not a module bolted into LPI.

> Reference/proof case: a state DOT stormwater treatment-device programme — device inventory +
> field inspection + GIS, driven by NPDES permit compliance, replacing a legacy maintenance
> system. Its requirements matrix (210 reqs) seeded this design.

---

## The one-paragraph pitch

Public-sector agencies that inspect physical assets on a schedule — DOTs, public works, water/
stormwater, utilities-in-government — need an **asset register + inspection lifecycle + condition
scoring + map + offline field collection**, with the data landing in a defensible system of record
and flowing to regulators. Salesforce PSS is the system of record; **Axsy** provides best-in-class
offline-first mobile collection (and light dispatch); **ArcGIS** is the Esri interoperability layer;
and the **Field Inspection Accelerator** is the pre-built domain solution + the factory that stands a
whole agency up in weeks, with GIS and mobility already solved as swappable tiers.

## What this accelerator is — and is not

| It IS | It is NOT |
|---|---|
| A pre-built PSS domain solution: asset register, inspection lifecycle, QC/QA, condition scoring, reporting, personas | A mobile app (we partner with Axsy for that) |
| A delivery **factory** that tailors + deploys per agency | An enterprise GIS platform (that's ArcGIS/Esri) |
| The owner of the **thin Salesforce↔ArcGIS bridge** as a productized module | A bespoke integration project rebuilt each deal |
| Domain-named around the customer **outcome** (inspections/assets) | "Field Service Accelerator" — FSL is a specific product, invoked only when true dispatch is primary |

## Document index

| Doc | Purpose |
|---|---|
| [docs/00_Getting_Started.md](docs/00_Getting_Started.md) | Org setup (shared demo org + ArcGIS dev), connect steps, first-run sequence |
| [docs/01_Strategy_and_Positioning.md](docs/01_Strategy_and_Positioning.md) | Value, moat ranking, Axsy partner boundary, differentiation, the vertical play |
| [docs/02_Architecture_and_Approach.md](docs/02_Architecture_and_Approach.md) | Layered architecture, GIS/mobility/dispatch tiering, shared-factory relationship, build-vs-buy-vs-partner |
| [docs/03_Solution_Design.md](docs/03_Solution_Design.md) | Domain data model, modules, GIS bridge design, QC/QA, condition scoring |
| [docs/04_Roadmap_and_Build_Plan.md](docs/04_Roadmap_and_Build_Plan.md) | Phases, MVP, effort bands, what to build/buy/partner, open decisions |
| [docs/05_TBMP_Reference_FitGap.md](docs/05_TBMP_Reference_FitGap.md) | Reference-case requirements coverage |
| [docs/06_Domain_Requirements_Generic.md](docs/06_Domain_Requirements_Generic.md) | Multi-domain generic requirements (NBIS/PCI/PACP/MS4) so the product isn't shaped by one customer |
| [docs/07_Build_Status_and_Learnings.md](docs/07_Build_Status_and_Learnings.md) | What's deployed to the demo org + the hard-won platform learnings ledger |

## Status

Planning / pre-build. This repo currently holds strategy, architecture, design, and roadmap. No
Salesforce metadata is scaffolded yet — the roadmap defines the build order.

## Key decisions locked (as of this draft)

- **Name:** Field Inspection Accelerator (domain-named; not "Field Service").
- **Separate product**, sibling to LPI/Grants, sharing the factory + base.
- **Partner with Axsy** for offline-first mobile collection and light dispatch (partnership outreach in flight).
- **ArcGIS as the Esri interoperability layer**; we build only a thin, productized SF→ArcGIS bridge.
- **FSL is a tier, not the platform** — reserved for when heavy dispatch becomes primary.
