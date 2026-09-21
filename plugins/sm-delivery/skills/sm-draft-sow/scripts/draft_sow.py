#!/usr/bin/env python3
"""Draft the house Statement of Work from the estimate, not alongside it.

Usage:  python draft_sow.py <engagement.json> <expand.json> <estimate.json> <out.docx>

The split this script exists to enforce: every NUMBER comes from the two model
responses, and every FACT about the engagement comes from `engagement.json`,
which a human writes. Nothing here invents either. A SOW assembled by hand from
a workbook drifts from it within one revision — the checkpoint hours get typed
in, the scope table gets re-summarised, and then the fee table and the staffing
plan quietly disagree. That happened, which is why this exists.

What it produces is the house Implementation Services spine, with the fee
language of the T&M / not-to-exceed SOWs:

    1 Overview (with the contract vehicle, when there is one)
    2 Scope of Services, by release
    3 Delivery Approach, project plan, staffing grid by week, workstreams
    4 Checkpoints, Deliverables & Acceptance — hours crossed from the BOE
    5 Term & Fees — basis of estimate, rate schedule
    6 Assumptions & Exclusions
    7 Customer Responsibilities
    8 General Terms
    Acceptance

Rates are left as placeholders unless `engagement.json` supplies them, because
a rate typed into a SOW that does not match the rate card is worse than a blank
someone has to fill.
"""
from __future__ import annotations

import json
import sys
from datetime import date, timedelta

from docx import Document
from docx.enum.section import WD_ORIENT, WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt

ARIAL = "Arial"
BAND = {"Planning/KT": "BDD7EE", "Design": "9DC3E6", "Implementation": "C5E0B4",
        "UAT": "FBE2D5", "Go-Live": "A9D18E", "Support": "F8CBAD"}
#: Delivery phases in run order, with the wording a SOW uses.
DP = [("requirements", "Requirements"), ("design", "Design"),
      ("build", "Build & Configure"), ("system_test", "System Test"),
      ("uat", "UAT"), ("deploy", "Deploy & Go-Live"), ("program", "Programme Mgmt")]
#: Capability rows that are engagement-wide rather than scope the customer picks.
OVERHEAD = {"Dependencies", "Allowances", "Delivery management"}
#: Facts a human must supply. The engine derives every number and no prose, so a missing
#: key here is a SOW with a hole in it; naming all of them at once beats a KeyError on the
#: first one, three sections into a build.
REQUIRED = ("title", "customer", "objective", "objective_clause", "releases",
            "delivery_approach", "checkpoint_notes", "acceptance_process", "assumptions",
            "exclusions", "responsibilities", "general_terms", "rate_schedule")


def check(eng: dict) -> None:
    missing = [k for k in REQUIRED if not eng.get(k)]
    if missing:
        raise SystemExit("engagement.json is missing: " + ", ".join(missing))
    for i, rel in enumerate(eng["releases"]):
        for k in ("name", "short", "items", "capabilities"):
            if not rel.get(k):
                raise SystemExit(f"engagement.json releases[{i}] is missing: {k}")


class Sow:
    def __init__(self, eng, exp, est):
        self.eng, self.exp, self.est = eng, exp, est
        self.d = Document()
        for s in self.d.sections:
            s.page_width, s.page_height = Inches(8.5), Inches(11)
            s.left_margin = s.right_margin = Inches(0.9)
        n = self.d.styles["Normal"]
        n.font.name, n.font.size = ARIAL, Pt(10)
        self.cust = eng["customer"]["short"]

    # ── primitives ────────────────────────────────────────────────────────
    def h(self, text, level):
        return self.d.add_heading(text, level=level)

    def p(self, text="", *, bold=False, italic=False, size=10):
        par = self.d.add_paragraph()
        r = par.add_run(text)
        r.bold, r.italic = bold, italic
        r.font.size, r.font.name = Pt(size), ARIAL
        return par

    def bullets(self, items):
        for t in items:
            par = self.d.add_paragraph(t, style="List Bullet")
            for r in par.runs:
                r.font.size, r.font.name = Pt(10), ARIAL

    def table(self, headers, rows, widths, size=9):
        t = self.d.add_table(rows=1, cols=len(headers))
        t.style = "Table Grid"
        for i, head in enumerate(headers):
            c = t.rows[0].cells[i]
            c.text = ""
            r = c.paragraphs[0].add_run(head)
            r.bold = True
            r.font.size, r.font.name = Pt(size), ARIAL
        for row in rows:
            cells = t.add_row().cells
            for i, v in enumerate(row):
                txt, bold = (v if isinstance(v, tuple) else (v, False))
                cells[i].text = ""
                r = cells[i].paragraphs[0].add_run(str(txt))
                r.bold = bold
                r.font.size, r.font.name = Pt(size), ARIAL
        for row in t.rows:
            for i, w in enumerate(widths):
                row.cells[i].width = Inches(w)
        return t

    @staticmethod
    def shade(cell, colour):
        el = OxmlElement("w:shd")
        el.set(qn("w:val"), "clear")
        el.set(qn("w:fill"), colour)
        cell._tc.get_or_add_tcPr().append(el)

    # ── derived numbers, all from the model responses ─────────────────────
    def capability_hours(self):
        """Capability -> hours, scope only (overheads excluded)."""
        out = {}
        for r in self.exp.get("requirements", []):
            cap = r.get("capability") or "(unassigned)"
            out[cap] = out.get(cap, 0.0) + float(r.get("hours") or 0)
        return out

    def grid(self):
        """(capability, delivery phase) -> hours, from the BOE lines."""
        g = {}
        for ln in self.exp.get("boe_lines", []):
            cap = ln.get("phase") or "(unassigned)"
            dp = (ln.get("delivery_phase") or "").strip() or "build"
            if ln.get("oversight"):
                dp = "program"
            g[(cap, dp)] = g.get((cap, dp), 0.0) + float(ln.get("qty") or 0) * float(
                ln.get("unit_hours") or 0)
        return g

    def release_of(self, cap):
        for rel in self.eng["releases"]:
            if cap in rel["capabilities"]:
                return rel["name"]
        return None

    def phase_at(self, week):
        for ph in self.est["phases"]:
            if ph["start_week"] <= week <= ph["end_week"]:
                return ph["name"]
        return None

    # ── sections ──────────────────────────────────────────────────────────
    def title_block(self):
        e = self.eng
        self.d.add_heading("SuccessMetrics Statement of Work", level=0)
        self.p(e["title"], bold=True, size=12)
        self.p(f"SOW# {e.get('sow_number', '____')}")
        note = (f"DRAFT — for {self.cust} and legal review.")
        v = e.get("vehicle")
        if v:
            note += (f" Issued under {v['name']}. Capitalized terms not defined here "
                     "have the meaning given in the ordering instructions and "
                     "provisions incorporated by the Purchase Order.")
        self.p(note, italic=True, size=9)

    def overview(self):
        e = self.eng
        self.h("1. Overview", 1)
        self.h("1.1 Introduction", 2)
        self.p(f'This Statement of Work ("SOW") describes the professional services '
               f'("Services") SuccessMetrics Corp ("SuccessMetrics") will provide to '
               f'{e["customer"]["name"]} ("Customer" or "{self.cust}") to '
               f'{e["objective_clause"]} The Services are delivered in '
               f'{len(e["releases"])} phases on a {e.get("fee_basis_phrase", "time-and-materials")} '
               f'basis subject to the Not-to-Exceed amount in Section 5.')
        v = e.get("vehicle")
        if v:
            self.h("1.2 Contract Vehicle and Ordering", 2)
            self.p(v["summary"])
            self.bullets(v.get("terms", []))
        self.h("1.3 Definitions" if v else "1.2 Definitions", 2)
        for term, mean in e.get("definitions", []):
            par = self.d.add_paragraph()
            r = par.add_run(f"{term} — ")
            r.bold = True
            r.font.size, r.font.name = Pt(10), ARIAL
            r2 = par.add_run(mean)
            r2.font.size, r2.font.name = Pt(10), ARIAL

    def scope(self):
        e = self.eng
        self.h("2. Scope of Services", 1)
        self.h("2.1 Objective", 2)
        self.p(e["objective"])
        for i, rel in enumerate(e["releases"], start=2):
            self.h(f"2.{i} {rel['name']}", 2)
            if rel.get("summary"):
                self.p(rel["summary"])
            self.bullets(rel["items"])
        n = len(e["releases"]) + 2
        for opt in e.get("options", []):
            self.h(f"2.{n} Priced option — {opt['name']}", 2)
            self.p(f"{opt['description']} It is priced separately as an option "
                   f"({opt['hours']:,.1f} hours in total) and is included only if "
                   f"{self.cust} elects it in writing. It is not part of the NTE Amount "
                   "in Section 5.1 unless elected.")
            n += 1
        if e.get("knowledge_transfer"):
            self.h(f"2.{n} Knowledge transfer and documentation", 2)
            self.p(e["knowledge_transfer"])

    def approach(self):
        e, est = self.eng, self.est
        self.h("3. Delivery Approach", 1)
        self.p(e["delivery_approach"])

        self.h("3.1 Project plan", 2)
        self.p("The plan below is generated from the same basis of estimate as "
               "Section 5.1, so the timeline, the team and the hours are one set of "
               "numbers rather than three.")
        names = {p["name"]: p for p in est["phases"]}
        rows = []
        for ph in est["phases"]:
            a, b = ph["start_week"], ph["end_week"]
            span = f"W{a}" if a == b else f"W{a} – W{b}"
            rows.append([ph["name"], span, e.get("phase_notes", {}).get(ph["name"], "")])
        self.table(["Phase", "Weeks", "What happens"], rows, [1.9, 1.0, 3.8])
        self.p(f"{est['total_weeks']} weeks and {est['implementation_sprints']} "
               f"implementation sprints. Duration drives the programme management "
               f"line in Section 5.1.", italic=True, size=9)
        assert names  # phases are named, or the plan above is meaningless

    def staffing(self):
        """The weekly staffing grid, landscape, in the house layout."""
        est = self.est
        sec = self.d.add_section(WD_SECTION.NEW_PAGE)
        sec.orientation = WD_ORIENT.LANDSCAPE
        sec.page_width, sec.page_height = Inches(11), Inches(8.5)
        sec.left_margin = sec.right_margin = Inches(0.6)
        sec.top_margin = sec.bottom_margin = Inches(0.6)

        self.h("3.2 Staffing plan by week", 2)
        self.p("Each row is a resource, each column a week. The figure in a cell is "
               "that resource's hours for that week; the phase band and sprint number "
               "run across the top.")
        weeks = est["total_weeks"]
        team = est["team"]
        start = self.eng.get("start_date")
        start = date(*(int(x) for x in start.split("-"))) if start else None

        ncol = 2 + weeks + 2
        t = self.d.add_table(rows=4 + len(team) + 1, cols=ncol)
        t.style = "Table Grid"
        t.autofit = False
        layout = OxmlElement("w:tblLayout")
        layout.set(qn("w:type"), "fixed")
        t._tbl.tblPr.append(layout)
        mar = OxmlElement("w:tblCellMar")
        for side in ("left", "right"):
            m = OxmlElement(f"w:{side}")
            m.set(qn("w:w"), "8")
            m.set(qn("w:type"), "dxa")
            mar.append(m)
        t._tbl.tblPr.append(mar)

        def cell(c, text, *, size=5, bold=False, fill=None, center=True):
            c.text = ""
            r = c.paragraphs[0].add_run(str(text))
            r.bold = bold
            r.font.size, r.font.name = Pt(size), ARIAL
            if center:
                c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            if fill:
                self.shade(c, fill)

        rows = t.rows
        # date / phase / sprint / week
        cell(rows[0].cells[0], "Date" if start else "Phase", size=7, bold=True, center=False)
        cell(rows[1].cells[0], "Phase", size=7, bold=True, center=False)
        cell(rows[2].cells[0], "Sprint", size=7, bold=True, center=False)
        cell(rows[3].cells[0], "Resource", size=7, bold=True, center=False)
        cell(rows[3].cells[1], "Rate", size=6, bold=True)
        for w in range(1, weeks + 1):
            col = 1 + w
            ph = self.phase_at(w)
            fill = BAND.get(ph, "D9D9D9")
            cell(rows[0].cells[col],
                 (start + timedelta(weeks=w - 1)).strftime("%-m/%-d") if start else "",
                 size=4)
            cell(rows[1].cells[col], "", fill=fill)
            cell(rows[2].cells[col], (w - 1) // 2 + 1, size=4, fill="F2F2F2")
            cell(rows[3].cells[col], w, size=5, bold=True, fill="F2F2F2")
        # The band label is MERGED across the weeks it covers. Written into the band's
        # first week it had one 0.2-inch column to live in, so "Planning/KT" rendered as
        # "Planni n" and "Implementation" as "Impleme e" — the row that tells a reader
        # which phase a sprint falls in, unreadable.
        for ph in est["phases"]:
            a, b = 1 + ph["start_week"], 1 + min(ph["end_week"], weeks)
            merged = rows[1].cells[a].merge(rows[1].cells[b]) if b > a else rows[1].cells[a]
            cell(merged, ph["name"], size=5, bold=True,
                 fill=BAND.get(ph["name"], "D9D9D9"))
        cell(rows[3].cells[ncol - 2], "Total hrs", size=6, bold=True)
        cell(rows[3].cells[ncol - 1], "Amount", size=6, bold=True)

        grand = 0.0
        for i, m in enumerate(team):
            row = rows[4 + i].cells
            cell(row[0], f"{m['label']}  ({m.get('location', '')})", size=6, center=False)
            cell(row[1], self.eng.get("rates", {}).get(m["label"], "[rate]"), size=5)
            total = 0.0
            for w in range(1, weeks + 1):
                on = m["start_week"] <= w <= m["end_week"]
                if on:
                    total += m["hours_per_week"]
                    cell(row[1 + w], f"{m['hours_per_week']:.0f}", size=5,
                         fill=BAND.get(self.phase_at(w), "FFFFFF"))
                else:
                    cell(row[1 + w], "")
            grand += total
            cell(row[ncol - 2], f"{total:,.0f}", size=6, bold=True)
            cell(row[ncol - 1], "$[    ]", size=5)
        last = rows[-1].cells
        cell(last[0], "Total", size=7, bold=True, center=False)
        cell(last[1], "")
        for w in range(1, weeks + 1):
            cell(last[1 + w], "")
        cell(last[ncol - 2], f"{grand:,.0f}", size=7, bold=True, fill="D9E2F3")
        cell(last[ncol - 1], "$[NTE]", size=6, bold=True, fill="D9E2F3")

        colw = ([Inches(1.35), Inches(0.30)] + [Inches(0.208)] * weeks
                + [Inches(0.45), Inches(0.50)])
        # 27 weeks fits; wider projects get narrower week columns rather than
        # spilling off the page.
        if weeks > 27:
            colw = ([Inches(1.2), Inches(0.28)]
                    + [Inches(min(0.208, 7.6 / weeks))] * weeks
                    + [Inches(0.42), Inches(0.46)])
        for r_ in t.rows:
            # The phase row has merged cells and so fewer of them; its widths come from
            # the column pass below. zip stops at the shorter of the two by design.
            for c_, w_ in zip(r_.cells, colw):
                c_.width = w_
        for i, w_ in enumerate(colw):
            t.columns[i].width = w_
        self.grand_staffed = grand
        self.reconcile_staffing(grand)

    def reconcile_staffing(self, staffed):
        """Say in the document how the grid relates to the fee.

        A staffing grid and a fee table in the same SOW that do not visibly agree is the
        first thing a procurement reviewer picks up, and the honest answer is not that
        one of them is wrong — it is that capacity is booked to whole sprints while the
        fee is the priced effort. Unsaid, that reads as padding.
        """
        base = float(self.exp.get("totals", {}).get("base") or 0)
        if not base:
            return
        slack = staffed - base
        pct = slack / base
        self.p(f"The grid assigns {staffed:,.0f} hours of capacity against the "
               f"{base:,.1f} priced hours in Section 5.1, a difference of "
               f"{slack:+,.0f} hours ({pct:+.1%}). Capacity is booked to whole sprints "
               "and whole phase bands, so a team is on the plan for the sprint it is "
               "needed in rather than for the exact hours inside it. The fee follows "
               "the priced hours, not the grid: hours assigned and not worked are not "
               "charged.", italic=True, size=9)

    def checkpoints(self):
        """Hours per checkpoint, crossed from the BOE rather than typed in."""
        sec = self.d.add_section(WD_SECTION.NEW_PAGE)
        sec.orientation = WD_ORIENT.PORTRAIT
        sec.page_width, sec.page_height = Inches(8.5), Inches(11)
        sec.left_margin = sec.right_margin = Inches(0.9)

        g, e = self.grid(), self.eng
        rels = e["releases"]

        # The total is accumulated from the rows this table actually emits, not from the
        # whole grid. Summing the grid made the reconciliation in main() unfalsifiable: a
        # capability left out of every release dropped its hours from every printed row
        # while the total stayed put, which is the one drift the check exists to catch.
        booked: list[float] = []

        def hours(caps, phases):
            v = sum(g.get((c, p), 0.0) for c in caps for p in phases)
            booked.append(v)
            return v

        scope_caps = [c for (c, _p) in g if c not in OVERHEAD]
        allc = sorted(set(scope_caps))
        rows, n = [], 1
        rows.append([str(n), "Requirements confirmed",
                     e["checkpoint_notes"].get("requirements", ""),
                     f"{hours(allc, ['requirements']):,.1f}"])
        n += 1
        rows.append([str(n), "High-level design accepted",
                     e["checkpoint_notes"].get("design", ""),
                     f"{hours(allc, ['design']):,.1f}"])
        for rel in rels:
            caps = rel["capabilities"]
            n += 1
            rows.append([str(n), f"{rel['short']} build complete",
                         rel.get("build_note", ""), f"{hours(caps, ['build']):,.1f}"])
            n += 1
            rows.append([str(n), f"{rel['short']} tested and accepted",
                         rel.get("test_note", ""),
                         f"{hours(caps, ['system_test', 'uat']):,.1f}"])
            n += 1
            rows.append([str(n), f"{rel['short']} live", rel.get("live_note", ""),
                         f"{hours(caps, ['deploy']):,.1f}"])
        overhead = sum(v for (c, _p), v in g.items() if c in OVERHEAD)
        rows.append(["", ("Across the engagement", True),
                     e["checkpoint_notes"].get("overhead", ""),
                     (f"{overhead:,.1f}", True)])
        total = sum(booked) + overhead
        rows.append(["", ("Total", True), "", (f"{total:,.1f}", True)])

        self.h("4. Checkpoints, Deliverables & Acceptance", 1)
        self.h("4.1 Delivery checkpoints", 2)
        self.p("Progress is reviewed and accepted at the following Checkpoints. "
               "Estimated hours are per the basis of estimate in Section 5.1.")
        self.table(["#", "Checkpoint", "Key Deliverables / acceptance criteria",
                    "Est. hours"], rows, [0.4, 1.9, 3.5, 0.9])
        self.p("Checkpoint hours are each capability group crossed with its delivery "
               "phase in the basis of estimate, and reconcile to the total in "
               "Section 5.1. Individual figures are rounded to one decimal place and "
               "may not sum exactly.", italic=True, size=9)
        self.h("4.2 Acceptance process", 2)
        self.p(self.eng["acceptance_process"])
        self.checkpoint_total = total

    def fees(self):
        e, exp = self.eng, self.exp
        caps = self.capability_hours()
        totals = exp.get("totals", {})
        overlay = exp.get("oversight_overlay") or {}
        self.h("5. Term & Fees", 1)
        self.h("5.1 Time & Materials, capped at a Not-to-Exceed amount", 2)
        base = float(totals.get("base") or 0)
        self.p("The Services are provided on a time-and-materials (T&M) basis at the "
               "Rate Schedule in Section 5.2, subject to a Not-to-Exceed (NTE) Amount "
               f"of $[NTE]. The NTE is based on the estimate of {base:,.1f} hours "
               f"below. {self.cust} pays only for hours actually worked; if the scope "
               "is delivered in fewer hours, the Customer pays less. The total charged "
               "for the Section 2 scope will not exceed the NTE Amount without a "
               "Change Order.")
        self.p("Basis of estimate", bold=True)
        rows, scope_sub = [], 0.0
        for rel in e["releases"]:
            rows.append([(rel["name"], True), "", "", ""])
            sub = 0.0
            for cap in rel["capabilities"]:
                h = caps.get(cap, 0.0)
                if not h:
                    continue
                sub += h
                rows.append([e.get("capability_labels", {}).get(cap, cap),
                             f"{h:,.1f}", "[rate]", "$[    ]"])
            scope_sub += sub
            rows.append([(f"{rel['short']} subtotal", True), (f"{sub:,.1f}", True), "", ""])
        rows.append([("Scope items subtotal", True), (f"{scope_sub:,.1f}", True), "", ""])
        for label, key in (("Verification reserve (defects found in acceptance testing)",
                            "verification_reserve"),
                           ("Shared dependencies (environments, access, licences, "
                            "deliverability)", "dependencies")):
            v = float(totals.get(key) or 0)
            if v:
                rows.append([label, f"{v:,.1f}", "[rate]", "$[    ]"])
        pm = float(totals.get("delivery_management") or 0)
        if pm:
            rows.append([f"Programme management ({overlay.get('allocation', 0):.0%} FTE "
                         f"across {overlay.get('weeks', 0)} weeks)",
                         f"{pm:,.1f}", "[rate]", "$[    ]"])
        rows.append([("Total estimated hours", True), (f"{base:,.1f}", True), "",
                     ("$[NTE]", True)])
        for opt in e.get("options", []):
            rows.append([f"Priced option — {opt['name']}, only if elected",
                         f"{opt['hours']:,.1f}", "[rate]", "$[    ]"])
        self.table(["Work item", "Est. hours", "Rate $/hr", "Amount"], rows,
                   [3.5, 0.9, 0.9, 1.1])
        self.p("Hours are built from the Customer's requirements rather than from a "
               "rate card: each requirement is expanded through the layers it touches "
               "and multiplied by the counts that make this project this size. Each "
               "work item's hours already include its share of requirements, design, "
               "build, system test, UAT and release. Programme management is priced "
               "from the project's duration, not as a percentage of effort, so it does "
               "not fall in proportion if scope is reduced.", italic=True, size=9)
        self.p("A companion Scope and Priorities workbook lists every scope item "
               "individually with its hours, so the Customer can decide what to include "
               "within each phase and see the total move.", italic=True, size=9)
        self.base_hours = base

        self.h("5.2 Rate Schedule", 2)
        if e.get("rate_schedule"):
            self.p(e.get("rate_schedule_note", ""))
            heads = list(e["rate_schedule"][0].keys())
            self.table([h.replace("_", " ").title() for h in heads],
                       [[r[h] for h in heads] for r in e["rate_schedule"]],
                       [1.9, 1.9, 0.8, 0.9, 1.0][:len(heads)])
        for key, title in (("invoicing", "5.3 Invoicing"),
                           ("flexible_resourcing", "5.4 Flexible resourcing & prioritization"),
                           ("out_of_scope", "5.5 Out-of-scope & change-order work"),
                           ("travel", "5.6 Travel & expenses")):
            if e.get(key):
                self.h(title, 2)
                self.p(e[key])

    def tail(self):
        e = self.eng
        self.h("6. Assumptions & Exclusions", 1)
        self.h("6.1 Key assumptions", 2)
        self.bullets(e["assumptions"])
        self.h("6.2 Exclusions", 2)
        self.p(e.get("exclusions_preamble", "The following are outside this SOW and "
                                            "may be added by Change Order:"))
        self.bullets(e["exclusions"])
        self.h("7. Customer Responsibilities", 1)
        self.p(e.get("responsibilities_preamble", ""))
        self.bullets(e["responsibilities"])
        self.h("8. General Terms", 1)
        for i, (title, body) in enumerate(e["general_terms"], start=1):
            self.h(f"8.{i} {title}", 2)
            self.p(body)
        self.h("Acceptance", 1)
        self.p("Agreed and accepted by the authorized representatives of the parties:")
        self.table(["SuccessMetrics Corp", e["customer"]["name"]],
                   [["Signature: ______________________",
                     "Signature: ______________________"],
                    [f"Name: {e.get('signatory', 'Gurumurthy Ramasubramanian')}",
                     "Name: ______________________"],
                    [f"Title: {e.get('signatory_title', 'Managing Partner')}",
                     "Title: ______________________"],
                    ["Date: ______________________", "Date: ______________________"]],
                   [3.3, 3.3])
        if e.get("footer"):
            self.p()
            self.p(e["footer"], italic=True, size=9)

    def build(self, out_path):
        self.title_block()
        self.overview()
        self.scope()
        self.approach()
        self.staffing()
        self.checkpoints()
        self.fees()
        self.tail()
        self.d.save(out_path)
        return self


def main(argv):
    if len(argv) != 5:
        sys.exit("usage: draft_sow.py <engagement.json> <expand.json> "
                 "<estimate.json> <out.docx>")
    eng = json.load(open(argv[1]))
    exp = json.load(open(argv[2]))
    est = json.load(open(argv[3]))
    check(eng)
    sow = Sow(eng, exp, est).build(argv[4])
    base = getattr(sow, "base_hours", 0.0)
    ck = getattr(sow, "checkpoint_total", 0.0)
    print(f"Wrote {argv[4]}")
    print(f"  fee basis        {base:,.1f} h")
    print(f"  checkpoints sum  {ck:,.1f} h")
    if abs(base - ck) > 0.5:
        print("  WARNING: the checkpoint table and the fee basis disagree. Both are "
              "derived from the same BOE lines, so this means the release map in "
              "engagement.json does not cover every capability.")
    staffed = getattr(sow, "grand_staffed", 0.0)
    slack = (staffed - base) / base if base else 0.0
    print(f"  staffed hours    {staffed:,.0f} h ({slack:+.1%} vs the fee basis — "
          "sprint-boundary capacity, reconciled in Section 3.2)")
    if base and abs(slack) > 0.15:
        print("  WARNING: the staffing grid and the fee basis differ by more than sprint "
              "rounding explains. Check sm_estimate's reconciliation warnings — a role "
              "staffed independently of its BOE category, or a team size that does not "
              "match the effort, will show up here first.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
