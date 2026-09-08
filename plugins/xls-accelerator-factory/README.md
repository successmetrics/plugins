# Excel-to-Salesforce Accelerator

Turn a spreadsheet application into a platform application, without guessing
and without reproducing the spreadsheet in a more expensive language.

## The problem it solves

A workbook that has grown into a business system is a requirements document
wearing a grid. Tabs propose objects, columns propose fields, formulas propose
calculations, cross-tab lookups propose relationships. Every one of those
proposals is *usually* wrong in a specific, predictable way — and two
consultants reading the same file rarely reach the same model, or can say what
made the difference.

This accelerator makes the mapping arguable. Each conclusion cites the rule
that produced it, so you can disagree with a rule rather than with a person.

## What it actually does

1. **Reads the workbook on your machine.** `sm-workbook` emits shape — sheet
   and column labels, inferred types, counts, and the formula graph with every
   literal replaced by a placeholder. Cell values never leave the laptop. A
   rate, an address, a salary: none of it travels.
2. **Classifies every tab.** Eight classes, and only two of them become
   objects. The presentation surface that looks exactly like a record and holds
   nothing. The pivot remnant that is a report. The reference ladder that is
   generation logic. The pasted extract that probably should not move at all.
3. **Maps columns to fields**, with types inferred from number formats and
   picklists proposed from the distinct-value count — which the workbook
   already knows, and which is the cheapest quality win in the whole migration.
4. **Assigns every calculation a target**, cheapest first: formula field,
   roll-up summary, Business Rules Engine decision matrix, expression set,
   record-triggered flow, scheduled flow, Apex, or a report. Anything expensive
   comes back with the cheaper options that were ruled out, and why.
5. **Names what stays outside Salesforce.** The section customers least expect
   and most need.
6. **Returns every normalisation as a decision a human signs** — not as
   metadata. A duplicated tab is records. Twelve month columns are one field
   and a missing child. Banded totals are a grouping object. Each comes with
   options and consequences.

## What it deliberately does not do

**It does not generate metadata from the workbook.** A .xlsx-to-package.xml
generator demos extremely well and produces a data model nobody owns — which is
the spreadsheet again, reached faster. Build from the signed design.

**It does not try to reproduce the workbook faithfully.** A migration where
every number matches and every structure survives has failed. A grid
accumulates arithmetic that exists only because a grid was the tool available;
the job is to say which calculations are the business rule and which are the
grid showing through.

## Where things live

Three tiers. `CLAUDE.md` has the rules; the short version:

| Tier | Repo | Holds |
|---|---|---|
| Judgment | `sm-agent-core` vault → `sm_excel_migrate` | the mapping rules, the taxonomy, the licence map |
| Local mechanism | `sm-agent-core/workbook/` → pip `sm-workbook` | the reader, the scrubber, the CLI |
| Product + factory | **this repo** | six reusable patterns, engagement scaffolding, the skills |

No mapping heuristic is ever written into this repo. A skill that *explains*
the taxonomy has leaked it as surely as one that pastes the YAML.

## The six patterns

The objects come from the customer's workbook, so this accelerator ships no
objects. What it ships is the six things a spreadsheet always does that a
platform does differently:

| Pattern | The defect it prevents |
|---|---|
| `program-parameters` | A governed rate buried in four formulas, one of which nobody finds when it changes |
| `period-generation` | A date ladder loaded as data, which stops on the day the load ended, silently |
| `aggregate-provenance` | A number nobody can trace, so a sound decision gets reopened as a data-quality problem |
| `governed-calculation` | A formula field that computes correctly and cannot answer "what was the rule in March" |
| `bulk-entry-grid` | Adoption failing because entering forty rows got slower, and it being read as resistance |
| `document-surface` | Losing the printed artifact the whole workbook existed to produce |

## Getting started

```bash
# 1. the local reader. From an sm-agent-core checkout — neither is on PyPI.
pip install ./gates ./workbook
```

**2. Connect the service.** This plugin ships its own connector declaration
pointing at the hosted sm-agent-core service, so there is nothing to run and
nothing to configure — but it does have to be authorized once, per plugin:

Settings → Plugins → **Xls accelerator factory** → **Connectors** →
`sm-agent-core` → **Connect**, with a customer-tier key or above. Another
plugin's connection to the same service does not count. Start a fresh session
afterwards.

**3. Run it.** `/xls-generate-implementation` for a whole engagement.

Or run the pieces: `xls-read-workbook` → `xls-map-design` →
`xls-license-check` → `xls-module-scope` → `xls-test`.

## The sentence for kickoff

You are not migrating a spreadsheet, you are ending one. Success is that nobody
opens the file again — not that the platform matches it.
