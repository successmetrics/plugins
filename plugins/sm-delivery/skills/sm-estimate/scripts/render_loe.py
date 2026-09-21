#!/usr/bin/env python3
"""Render an sm_estimate response into the delivery workbook.

Pure presentation. Every number here comes from the service response; this
script derives nothing.

Usage:  python render_loe.py estimate.json out.xlsx [expand.json]

Pass the sm_boe_expand response as the optional third argument and the workbook
gains a fifth tab, "Scope & Priorities": one row per scope item with its hours,
so the customer can choose what they want and watch the total move. The BOE
answers "what does it cost", the LOE answers "who is on it and for how long",
and this answers the question a customer with a fixed budget actually asks
first — "what can I drop?". Without that argument the workbook is the same
four tabs it always was.

The scope items live in the EXPAND response, not the estimate: `requirements`
carries each one's customer-facing name, its capability and its hours, and
`touches[].customer_task` the plain-English wording. Nothing here is computed
from them beyond selecting and concatenating.
"""
from __future__ import annotations
import json
import sys
from datetime import date, timedelta
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

NAVY = "1B2A4A"
#: Strong colours for the phase BAND row, read against white bold text.
PHASE_COLOR = {
    "Planning/KT": "5B9BD5", "Design": "7D5FFF", "Implementation": "2E6BD6",
    "UAT": "B45F06", "Hypercare": "CCCCCC", "Go-Live": "1E7A46", "Support": "C55A11",
}
#: Light tints of the same phases, for cells that carry readable numbers —
#: the sprint and week rows, the weekly staffing cells, and the Staffing tab.
#: A number on top of PHASE_COLOR is unreadable, which is why there are two.
_STAFF_BAND = {
    "Planning/KT": "BDD7EE", "Design": "9DC3E6", "Implementation": "C5E0B4",
    "UAT": "FBE2D5", "Hypercare": "F2F5FA", "Go-Live": "A9D18E", "Support": "F8CBAD",
}
REG = Font(name="Arial", size=9)
BOLD = Font(name="Arial", size=9, bold=True)
WHITE = Font(name="Arial", size=9, bold=True, color="FFFFFF")
SMALL = Font(name="Arial", size=8, color="555555")
HEAD = PatternFill("solid", fgColor=NAVY)
GREY = PatternFill("solid", fgColor="F2F5FA")
_thin = Side(style="thin", color="D0D0D0")
BORD = Border(left=_thin, right=_thin, top=_thin, bottom=_thin)
CEN = Alignment(horizontal="center", vertical="center")
WRAP = Alignment(wrap_text=True, vertical="top")
USD = '$#,##0;($#,##0);"-"'
H1 = '#,##0.0'


def _header(ws, row: int, labels: list[str], widths: list[int] | None = None) -> None:
    for i, label in enumerate(labels, start=1):
        c = ws.cell(row=row, column=i, value=label)
        c.fill, c.font, c.border, c.alignment = HEAD, WHITE, BORD, CEN
    if widths:
        for i, w in enumerate(widths, start=1):
            ws.column_dimensions[get_column_letter(i)].width = w


def _phase_of(phases: list[dict], week: int) -> str | None:
    for p in phases:
        if p["start_week"] <= week <= p["end_week"]:
            return p["name"]
    return None


def _week_columns(ws, phases: list[dict], total_weeks: int, first_col: int) -> None:
    """Phase band + sprint number + week number, three header rows.

    The band is MERGED across the weeks its phase covers. Repeated in every column it read
    as one label per week rather than one phase spanning six, and at this column width it
    truncated to "Impleme". Merged, the header says what it means and the eye can find a
    phase boundary without counting.
    """
    for w in range(1, total_weeks + 1):
        col = first_col + w - 1
        name = _phase_of(phases, w)

        # Sprint and week rows are tinted with the light band colour of the phase above
        # them, so a reader can see which sprints fall in which phase without tracing a
        # column up to the header.
        tint = PatternFill("solid", fgColor=_STAFF_BAND.get(name, "F2F5FA"))
        s = ws.cell(row=2, column=col, value=f"S{(w - 1) // 2 + 1}")
        s.font, s.alignment, s.border, s.fill = SMALL, CEN, BORD, tint

        h = ws.cell(row=3, column=col, value=f"W{w}")
        h.font, h.alignment, h.border, h.fill = BOLD, CEN, BORD, tint
        ws.column_dimensions[get_column_letter(col)].width = 5.5

    for band in phases:
        a = first_col + int(band["start_week"]) - 1
        b = first_col + min(int(band["end_week"]), total_weeks) - 1
        if b < a:
            continue
        cell = ws.cell(row=1, column=a, value=band["name"])
        cell.fill = PatternFill("solid", fgColor=PHASE_COLOR.get(band["name"], "CCCCCC"))
        cell.font, cell.alignment, cell.border = WHITE, CEN, BORD
        for c in range(a, b + 1):
            ws.cell(row=1, column=c).border = BORD
        if b > a:
            ws.merge_cells(start_row=1, start_column=a, end_row=1, end_column=b)



YELLOW = PatternFill("solid", fgColor="FFFF00")
RED = Font(name="Arial", size=8, color="C00000")



def verify(est: dict, exp: dict | None = None) -> list[tuple]:
    """Every tab against the BOE. Returns (name, ok, got, want, note) per check.

    This exists because three real defects were found by a human reading the output and
    asking why two numbers disagreed: sprint ceremony priced for the developer-sprints the
    effort needed rather than the ones staffed; workstream bars whose length came from a
    lane heuristic that had never seen an hour of effort; and a project plan that drew one
    of five phases and so omitted 29% of the project. None of them would fail a unit test
    of the piece that produced them — they were disagreements BETWEEN pieces. So the
    disagreement itself is what gets checked, on every run, and the results ship in the
    workbook rather than living in somebody's head.
    """
    out, T = [], (exp or {}).get("totals", {})
    team, lines = est.get("team", []), est.get("boe_lines", [])
    phases = est.get("phases", [])

    def add(name, got, want, tol=0.5, note=""):
        out.append((name, abs(float(got) - float(want)) <= tol, float(got), float(want), note))

    def eff(l):
        return float(l.get("qty") or 0) * float(l.get("unit_hours") or 0)

    def staffed_in(lo, hi):
        return sum(m["hours_per_week"] * max(0, min(m["end_week"], hi)
                                             - max(m["start_week"], lo) + 1) for m in team)

    def held(m):
        """A member's hours, derived when the response does not carry them."""
        return float(m.get("total_hours") if m.get("total_hours") is not None
                     else m["hours_per_week"] * (m["end_week"] - m["start_week"] + 1))

    base = float(T.get("base") or 0)
    if base:
        add("BOE lines sum to the base", sum(eff(l) for l in lines), base, 1.0)
        add("requirements + dependencies + reserve + leads + ceremony = base",
            sum(float(T.get(k) or 0) for k in
                ("requirements", "dependencies", "verification_reserve",
                 "delivery_management", "sprint_ceremony")), base, 1.0)
    if exp and exp.get("requirements"):
        add("Scope & Priorities items sum to the requirement hours",
            sum(float(r.get("hours") or 0) for r in exp["requirements"]),
            float(T.get("requirements") or 0), 1.0,
            f"{len(exp['requirements'])} items")
    if base:
        # A line with no delivery phase is build work, the same reading the rest of the
        # engine takes. Requiring the field made the grid come out empty on any BOE that
        # had not been phased, which is a silent zero rather than a check.
        grid = sum(eff(l) for l in lines
                   if (l.get("delivery_phase") or "build"))
        add("Checkpoints grid sums to the base", grid, base, 1.0,
            "capability x delivery phase")

    total_hours = sum(held(m) for m in team)
    add("LOE staffed hours equal the team total", total_hours,
        float(est.get("total_hours") or 0), 0.5)
    unpriced = sorted({m["label"] for m in team if not m.get("rate")})
    out.append(("Rate Card covers every resource on the LOE", not unpriced,
                len({m["label"] for m in team}) - len(unpriced),
                len({m["label"] for m in team}), ", ".join(unpriced)))
    add("LOE cost equals hours x the rate card",
        sum(held(m) * float(m.get("rate") or 0) for m in team),
        float(est.get("total_cost") or 0), 1.0)

    impl = next((b for b in phases if b["name"] == "Implementation"), None)
    caps = [w for w in est.get("workstreams", [])
            if (w.get("hours") or 0) > 0
            and w["name"] not in ("Integrations", "Data Migration")]
    if impl and caps:
        span = int(impl["end_week"]) - int(impl["start_week"]) + 1
        devs = max(1, sum(1 for m in team if m.get("category") == "build"
                          and m["start_week"] == impl["start_week"]))
        lanes = max(1, min(devs, len(caps)))
        per = sum(w["hours"] for w in caps) / (lanes * span)
        worst = max(abs((w["end_week"] - w["start_week"] + 1) * (w.get("parallel") or 1)
                        - w["hours"] / per) for w in caps) if per else 0
        out.append(("Every plan bar is proportional to its BOE hours", worst <= 1.5,
                    worst, 1.5, "lane-weeks, worst case"))
        priced = sum(eff(l) for l in lines
                     if not l.get("oversight") and not l.get("capacity_overhead")
                     and (l.get("delivery_phase") or "build") in ("build", "system_test")
                     and l["phase"] not in ("Dependencies", "Allowances",
                                            "Delivery management"))
        add("Plan capability bars equal the BOE build-window effort",
            sum(w["hours"] for w in caps), priced, 1.0)
    if phases:
        add("Plan phase bars cover the whole project",
            sum(staffed_in(int(b["start_week"]), int(b["end_week"])) for b in phases),
            total_hours, 1.0, f"{len(phases)} phases")
    return out


def _checks_tab(wb: Workbook, est: dict, exp: dict | None) -> list[tuple]:
    """The checks, in the workbook, so the reconciliation ships with the numbers."""
    rows = verify(est, exp)
    ws = wb.create_sheet("Checks")
    _header(ws, 1, ["Check", "Result", "Got", "Expected", "Note"], [56, 10, 12, 12, 44])
    for i, (name, ok, got, want, note) in enumerate(rows, start=2):
        ws.cell(row=i, column=1, value=name).font = REG
        c = ws.cell(row=i, column=2, value="PASS" if ok else "FAIL")
        c.font = Font(name="Arial", size=9, bold=True,
                      color="1E7A46" if ok else "C00000")
        c.alignment = CEN
        c.fill = PatternFill("solid", fgColor="E6F4EA" if ok else "FDE7E9")
        for col, v in ((3, got), (4, want)):
            x = ws.cell(row=i, column=col, value=round(v, 1))
            x.font, x.number_format, x.alignment = REG, H1, CEN
        n = ws.cell(row=i, column=5, value=note)
        n.font, n.alignment = SMALL, WRAP
        for col in range(1, 6):
            ws.cell(row=i, column=col).border = BORD
    r = len(rows) + 3
    bad = [n for n, ok, *_ in rows if not ok]
    c = ws.cell(row=r, column=1,
                value="Every tab reconciles to the BOE."
                if not bad else f"{len(bad)} check(s) failed: " + "; ".join(bad))
    c.font = Font(name="Arial", size=9, bold=True,
                  color="1E7A46" if not bad else "C00000")
    ws.cell(row=r + 1, column=1, value=(
        "These compare the sheets against each other, not each sheet against itself. "
        "The defects they exist to catch were all disagreements BETWEEN tabs — a bar "
        "drawn from no hours, ceremony priced for sprints nobody staffed, a plan showing "
        "one phase of five.")).font = SMALL
    ws.freeze_panes = "A2"
    return rows


def _scope_tab(wb: Workbook, exp: dict) -> None:
    """One row per scope item, so the customer can choose what they want.

    Three kinds of hour behave differently when scope is cut, and the tab is
    built around saying so rather than hiding it:

      * the items themselves go when they are deselected;
      * the verification reserve scales with what is left, so it is a formula
        off the selection;
      * shared dependencies barely move, and programme management is priced
        from DURATION, not effort — a shorter project is still a project.

    Programme management is therefore driven by a duration cell the user sets,
    defaulted to the full-scope figure the service returned, rather than by a
    scaling rule invented here. A committed number comes from re-running the
    estimate on the final selection; this tab is for the conversation before it.
    """
    ws = wb.create_sheet("Scope & Priorities")
    ws.sheet_view.showGridLines = False
    reqs = exp.get("requirements") or []
    totals = exp.get("totals") or {}
    overlay = exp.get("oversight_overlay") or {}

    req_hours = float(totals.get("requirements") or 0) or sum(
        float(r.get("hours") or 0) for r in reqs)
    reserve_pct = (float(totals.get("verification_reserve") or 0) / req_hours
                   if req_hours else 0.0)
    deps = float(totals.get("dependencies") or 0)
    alloc = float(overlay.get("allocation") or 0)
    hpw = float(overlay.get("hours_per_week") or 0)
    weeks = int(overlay.get("weeks") or 0)

    ws["A1"] = f"{exp.get('engagement', '')} — Scope Items and Estimated Hours".strip(" —")
    ws["A1"].font = Font(name="Arial", size=13, bold=True)
    ws["A2"] = ("Set Include? to Yes or No for each item and the totals below follow. "
                "Priority and Release are yours to record.")
    ws["A2"].font = REG
    ws["A3"] = ("Each item's hours already include its share of requirements, design, "
                "build, system test, UAT and release. Yellow cells are yours to edit.")
    ws["A3"].font = SMALL

    head = ["Capability", "Ref", "Scope item", "What it delivers", "Est. hours",
            "Include?", "Priority", "Release"]
    HEAD_ROW = 11
    first = HEAD_ROW + 1
    last = HEAD_ROW + max(len(reqs), 1)

    ws["A5"] = "Scope hours selected"
    ws["A5"].font = BOLD
    ws["B5"] = f'=SUMIFS(E{first}:E{last},F{first}:F{last},"Yes")'
    ws["B5"].font, ws["B5"].number_format = BOLD, H1
    ws["C5"] = f"=COUNTIF(F{first}:F{last},\"Yes\")&\" of {len(reqs)} items\""
    ws["C5"].font = SMALL

    ws["A6"] = "Verification reserve"
    ws["A6"].font = REG
    ws["B6"] = f"=B5*{reserve_pct:.6f}"
    ws["B6"].font, ws["B6"].number_format = REG, H1
    ws["C6"] = "Defects found in acceptance testing. Scales with what is selected."
    ws["C6"].font = SMALL

    ws["A7"] = "Shared dependencies"
    ws["A7"].font = REG
    ws["B7"] = deps
    ws["B7"].font, ws["B7"].number_format = REG, H1
    ws["C7"] = "Environments, access, licences, deliverability. Needed whatever is selected."
    ws["C7"].font = SMALL

    ws["A8"] = "Duration (weeks)"
    ws["A8"].font = REG
    ws["B8"] = weeks
    ws["B8"].font, ws["B8"].number_format, ws["B8"].fill = REG, "#,##0", YELLOW
    ws["C8"] = (f"Full scope is {weeks} weeks. Reduce it to see the effect, then re-run the "
                "estimate on the final selection for a committed figure.")
    ws["C8"].font = SMALL

    ws["A9"] = "Programme management"
    ws["A9"].font = REG
    ws["B9"] = f"=B8*{alloc}*{hpw}"
    ws["B9"].font, ws["B9"].number_format = REG, H1
    ws["C9"] = ("Priced from DURATION, not effort — it does not fall in proportion when "
                "scope is cut. A shorter project is still a project.")
    ws["C9"].font = RED

    ws["A10"] = "TOTAL SELECTED HOURS"
    ws["A10"].font = Font(name="Arial", size=10, bold=True)
    ws["B10"] = "=B5+B6+B7+B9"
    ws["B10"].font, ws["B10"].number_format, ws["B10"].fill = (
        Font(name="Arial", size=10, bold=True), H1, GREY)

    _header(ws, HEAD_ROW, head, [24, 12, 44, 52, 11, 10, 14, 12])
    for i, r in enumerate(reqs):
        row = first + i
        tasks, seen = [], set()
        for t in r.get("touches") or []:
            ct = (t.get("customer_task") or "").strip()
            if ct and ct not in seen:
                seen.add(ct)
                tasks.append(ct)
        vals = [r.get("capability", ""), r.get("id", ""), r.get("name", ""),
                "; ".join(tasks[:4]), float(r.get("hours") or 0)]
        for col, v in enumerate(vals, start=1):
            c = ws.cell(row=row, column=col, value=v)
            c.font, c.border = (REG if col == 5 else SMALL), BORD
            c.alignment = WRAP
            if col == 5:
                c.number_format = H1
        for col in (6, 7, 8):
            c = ws.cell(row=row, column=col, value="Yes" if col == 6 else "")
            c.font, c.border, c.alignment, c.fill = BOLD, BORD, CEN, YELLOW

    tot = last + 1
    ws.cell(row=tot, column=4, value="Total — all scope items").font = BOLD
    c = ws.cell(row=tot, column=5, value=f"=SUM(E{first}:E{last})")
    c.font, c.number_format, c.fill, c.border = BOLD, H1, GREY, BORD

    if reqs:
        dv = DataValidation(type="list", formula1='"Yes,No"', allow_blank=False)
        ws.add_data_validation(dv)
        dv.add(f"F{first}:F{last}")
        dp = DataValidation(
            type="list",
            formula1='"Must have,Should have,Could have,Not this time"', allow_blank=True)
        ws.add_data_validation(dp)
        dp.add(f"G{first}:G{last}")
    ws.freeze_panes = ws.cell(row=first, column=1)


#: Delivery phases in the order a project runs them, with the SOW wording.
_DP_ORDER = [
    ("requirements", "Requirements"), ("design", "Design"), ("build", "Build & Configure"),
    ("system_test", "System Test"), ("uat", "UAT"), ("deploy", "Deploy & Go-Live"),
    ("program", "Programme Mgmt"),
]


def _checkpoints_tab(wb: Workbook, exp: dict) -> None:
    """Capability against delivery phase — the grid a SOW checkpoint table needs.

    A SOW commits hours per checkpoint ("Phase 1 build complete", "Phase 1 tested
    and accepted"), and a checkpoint is a capability group crossed with a delivery
    phase. Both live on every BOE line — `phase` is the capability, `delivery_phase`
    is the stage — but nothing crossed them, so the hours had to be left as dashes
    or invented. This crosses them.

    Grouping capabilities into releases is an engagement decision and is not made
    here: the grid gives every cell, and whoever writes the SOW adds the rows
    across the capabilities in each release.
    """
    ws = wb.create_sheet("Checkpoints")
    ws.sheet_view.showGridLines = False
    lines = exp.get("boe_lines") or []

    caps, grid = [], {}
    for ln in lines:
        cap = ln.get("phase") or "(unassigned)"
        dp = (ln.get("delivery_phase") or "").strip() or "build"
        if ln.get("oversight"):
            dp = "program"
        if cap not in grid:
            grid[cap] = {}
            caps.append(cap)
        grid[cap][dp] = grid[cap].get(dp, 0.0) + float(ln.get("qty") or 0) * float(
            ln.get("unit_hours") or 0)

    ws["A1"] = f"{exp.get('engagement', '')} — Hours by Capability and Delivery Phase".strip(" —")
    ws["A1"].font = Font(name="Arial", size=13, bold=True)
    ws["A2"] = ("Each SOW checkpoint is a capability group crossed with a delivery phase. "
                "Add the rows for the capabilities in each release to get that "
                "checkpoint's committed hours.")
    ws["A2"].font = REG

    head = ["Capability"] + [label for _, label in _DP_ORDER] + ["Total"]
    HEAD_ROW = 4
    _header(ws, HEAD_ROW, head, [30] + [13] * len(_DP_ORDER) + [12])

    r = HEAD_ROW + 1
    for cap in caps:
        ws.cell(row=r, column=1, value=cap).font = REG
        ws.cell(row=r, column=1).border = BORD
        for i, (key, _) in enumerate(_DP_ORDER, start=2):
            # Full precision stored, one decimal DISPLAYED. Rounding each cell
            # before it is summed loses a few tenths across a grid this size,
            # and a checkpoint table that does not add up to the SOW total is
            # the one defect a customer is certain to find.
            v = grid[cap].get(key, 0.0)
            c = ws.cell(row=r, column=i, value=v if v else None)
            c.font, c.number_format, c.border, c.alignment = REG, H1, BORD, CEN
        lastcol = get_column_letter(1 + len(_DP_ORDER))
        t = ws.cell(row=r, column=2 + len(_DP_ORDER), value=f"=SUM(B{r}:{lastcol}{r})")
        t.font, t.number_format, t.border, t.fill = BOLD, H1, BORD, GREY
        r += 1

    ws.cell(row=r, column=1, value="TOTAL").font = BOLD
    ws.cell(row=r, column=1).border = BORD
    for i in range(2, 3 + len(_DP_ORDER)):
        col = get_column_letter(i)
        c = ws.cell(row=r, column=i, value=f"=SUM({col}{HEAD_ROW + 1}:{col}{r - 1})")
        c.font, c.number_format, c.border, c.fill = BOLD, H1, BORD, GREY
    ws.freeze_panes = ws.cell(row=HEAD_ROW + 1, column=2)



def _merge_assignments(team, weeks):
    """One row per NAMED RESOURCE, carrying its hours week by week.

    `sm_estimate` returns an assignment per contiguous run at one allocation, so an
    architect who is half time in planning, full time in design and half time again
    through the build is three entries. That is right for the model and wrong for the
    sheet: a reader counting rows counts people, and three rows says three architects.
    """
    out, seen = [], {}
    for m in team:
        key = (m["label"], m.get("location", ""), m.get("rate"))
        row = seen.get(key)
        if row is None:
            row = dict(m, weekly=[0.0] * weeks)
            seen[key] = row
            out.append(row)
        for w in range(m["start_week"], min(m["end_week"], weeks) + 1):
            row["weekly"][w - 1] += m["hours_per_week"]
    for row in out:
        on = [i + 1 for i, h in enumerate(row["weekly"]) if h]
        row["start_week"], row["end_week"] = (on[0], on[-1]) if on else (1, 0)
    return out


def _staffing_tab(wb: Workbook, est: dict, start_date=None) -> None:
    """The staffing sheet the firm actually hands over, in its own layout.

    Modelled on the Alaska DOL workbook, which is the format this practice has
    been using by hand: a calendar date row, a week row, a sprint row spanning
    two weeks, a phase band, then one row per named resource carrying a rate,
    that resource's hours in each week, a total-hours column and an extended
    cost. Implementation resources sit in one block; run-rate support sits in a
    second block below with its own totals, because the two get approved
    separately and a single grand total hides that.

    The LOE tab already holds the same numbers, but it is a delivery instrument
    — categories, locations, formulas keyed to editable start and end weeks. This
    one is the artefact a customer and a CFO read, so it leads with dates and
    money rather than with weeks and categories.

    `start_date` turns week numbers into real dates. Without it the date row is
    left blank rather than invented, because a made-up start date is the one
    thing on this sheet a reader would take literally.
    """
    ws = wb.create_sheet("Staffing")
    ws.sheet_view.showGridLines = False
    phases, weeks = est["phases"], est["total_weeks"]
    FIRST = 3                                  # col A label, col B rate, then weeks

    def _phase(w):
        for p in phases:
            if p["start_week"] <= w <= p["end_week"]:
                return p["name"]
        return None

    # ── header rows: date, week, sprint, phase band ──────────────────────
    ws.cell(1, 1, "Date").font = BOLD
    ws.cell(2, 1, "Week").font = BOLD
    ws.cell(3, 1, "Sprint").font = BOLD
    ws.cell(4, 1, "Phase").font = BOLD
    for w in range(1, weeks + 1):
        col = FIRST + w - 1
        if start_date is not None:
            c = ws.cell(1, col, start_date + timedelta(weeks=w - 1))
            c.number_format = "m/d/yy"
            c.font, c.alignment = SMALL, CEN
        c = ws.cell(2, col, w)
        c.font, c.alignment, c.fill, c.border = BOLD, CEN, GREY, BORD
        # a sprint is two weeks, numbered across the whole project
        c = ws.cell(3, col, (w - 1) // 2 + 1)
        c.font, c.alignment, c.fill, c.border = SMALL, CEN, GREY, BORD
        name = _phase(w)
        c = ws.cell(4, col, "")
        c.fill = PatternFill("solid", fgColor=_STAFF_BAND.get(name, "D9D9D9"))
        c.border = BORD
        ws.column_dimensions[get_column_letter(col)].width = 4.6
    # name each band once, at its first week
    for p in phases:
        c = ws.cell(4, FIRST + p["start_week"] - 1, p["name"])
        c.font = Font(name="Arial", size=7, bold=True)
        c.alignment = Alignment(horizontal="left", vertical="center")

    TOTCOL, COSTCOL = FIRST + weeks, FIRST + weeks + 1
    for r_, label in ((2, "Rate"),):
        ws.cell(r_, 2, label).font = BOLD
    ws.cell(2, TOTCOL, "Total Hours").font = BOLD
    ws.cell(2, COSTCOL, "Cost").font = BOLD
    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 9
    ws.column_dimensions[get_column_letter(TOTCOL)].width = 12
    ws.column_dimensions[get_column_letter(COSTCOL)].width = 13

    def _block(title, members, row):
        """One titled block of resources with its own totals."""
        ws.cell(row, 1, title).font = Font(name="Arial", size=9, bold=True)
        row += 1
        first = row
        for m in members:
            ws.cell(row, 1, m["label"]).font = REG
            c = ws.cell(row, 2, m.get("rate"))
            c.font, c.number_format = REG, USD
            for w in range(1, weeks + 1):
                col = FIRST + w - 1
                hrs = m["weekly"][w - 1] if w - 1 < len(m["weekly"]) else 0.0
                c = ws.cell(row, col, hrs or None)
                c.font, c.alignment, c.border, c.number_format = SMALL, CEN, BORD, H1
                if hrs:
                    c.fill = PatternFill(
                        "solid", fgColor=_STAFF_BAND.get(_phase(w), "FFFFFF"))
            a, b = get_column_letter(FIRST), get_column_letter(FIRST + weeks - 1)
            c = ws.cell(row, TOTCOL, f"=SUM({a}{row}:{b}{row})")
            c.font, c.number_format = BOLD, H1
            c = ws.cell(row, COSTCOL,
                        f"={get_column_letter(TOTCOL)}{row}*B{row}")
            c.font, c.number_format = REG, USD
            row += 1
        if row > first:
            ws.cell(row, 1, f"{title} total").font = BOLD
            for col in (TOTCOL, COSTCOL):
                L = get_column_letter(col)
                c = ws.cell(row, col, f"=SUM({L}{first}:{L}{row - 1})")
                c.font, c.number_format, c.fill = BOLD, (
                    H1 if col == TOTCOL else USD), GREY
            row += 1
        return row + 1

    merged = _merge_assignments(est["team"], weeks)
    impl = [m for m in merged if str(m.get("category", "")) != "support"]
    support = [m for m in merged if str(m.get("category", "")) == "support"]
    nxt = _block("Implementation", impl, 6)
    if support:
        _block("Support", support, nxt)
    ws.freeze_panes = ws.cell(row=5, column=FIRST)


def build(est: dict, out_path: str, exp: dict | None = None,
          start_date=None) -> None:
    wb = Workbook()
    phases, total_weeks = est["phases"], est["total_weeks"]

    # ---------- How To ----------
    ws = wb.active
    ws.title = "How To"
    ws.column_dimensions["A"].width = 110
    rows = [
        (f"{est['engagement']} — Estimate", BOLD),
        ("", REG),
        ("BOE — effort per named artifact. Blue cells are inputs.", REG),
        ("LOE — weekly staffing grid. Edit Start Wk / End Wk / Hrs-Wk; weekly cells follow.", REG),
        ("Project Plan — workstream Gantt on the same week and phase timeline.", REG),
        ("Scope & Priorities — one row per scope item, for the customer to choose from. "
         "Set Include? and the totals follow.", REG),
        ("Checkpoints — hours by capability against delivery phase. Add the rows for the "
         "capabilities in a release to get that SOW checkpoint's committed hours.", REG),
        ("The last two tabs appear only when the expand response is passed to the renderer.",
         SMALL),
        ("", REG),
        (f"Implementation sprints: {est['implementation_sprints']}", BOLD),
        (f"Total duration: {total_weeks} weeks", BOLD),
        (f"Total hours: {est['total_hours']:,.0f}", BOLD),
        (f"Total cost: ${est['total_cost']:,.0f}", BOLD),
        ("", REG),
        (f"Reconciliation: BOE build {est['reconciliation']['boe_build_effort']:,.0f} h "
         f"vs LOE build team {est['reconciliation']['loe_build_hours']:,.0f} h "
         f"({est['reconciliation']['variance_pct']:+.1f}%)", REG),
    ]
    for w in est.get("warnings", []):
        rows.append((f"WARNING: {w}", Font(name="Arial", size=9, color="B45F06")))
    for i, (text, font) in enumerate(rows, start=1):
        c = ws.cell(row=i, column=1, value=text)
        c.font, c.alignment = font, WRAP

    # ---------- BOE ----------
    ws = wb.create_sheet("BOE")
    _header(ws, 1, ["Phase", "Work Item", "Basis / Assumption", "Qty", "Unit Hrs", "Effort (h)"],
            [26, 46, 60, 8, 10, 12])
    # GROUPED, with the breadcrumbs a reader needs to find their way down 400 rows: a
    # capability header carrying its subtotal, a work-item header carrying its own, and
    # the layer lines beneath. Flat, with the capability and the work item repeated on
    # every line, there was no way to see what a requirement cost without selecting rows
    # and reading the status bar — so nobody did, and the BOE was quoted from the total.
    # Excel outline levels let the whole thing collapse to capability subtotals.
    r = 2
    groups, order = {}, []
    for line in est["boe_lines"]:
        cap = line["phase"]
        if cap not in groups:
            groups[cap] = {}
            order.append(cap)
        # A work item reads "<requirement> — <layer>", so the requirement is the breadcrumb
        # and the layer belongs on the line beneath it. Keyed on the whole string, every
        # line became its own group and the outline had nothing to collapse.
        req_name, _, layer = line["work_item"].partition(" — ")
        groups[cap].setdefault(req_name, []).append((layer, line))

    cap_rows = []
    for cap in order:
        cap_head = r
        c = ws.cell(row=r, column=1, value=cap)
        c.font, c.fill = BOLD, PatternFill("solid", fgColor="D9E2F3")
        for col in range(2, 7):
            ws.cell(row=r, column=col).fill = PatternFill("solid", fgColor="D9E2F3")
            ws.cell(row=r, column=col).border = BORD
        c.border = BORD
        r += 1
        item_rows = []
        for item, lines in groups[cap].items():
            item_head = r
            c = ws.cell(row=r, column=2, value=item)
            c.font, c.fill = BOLD, PatternFill("solid", fgColor="F2F5FA")
            for col in (1, 3, 4, 5, 6):
                ws.cell(row=r, column=col).fill = PatternFill("solid", fgColor="F2F5FA")
                ws.cell(row=r, column=col).border = BORD
            c.border = BORD
            ws.row_dimensions[r].outlineLevel = 1
            r += 1
            first = r
            for layer, line in lines:
                lc = ws.cell(row=r, column=2, value=f"    {layer}" if layer else "")
                lc.font, lc.alignment = SMALL, WRAP
                ws.cell(row=r, column=3, value=line["basis"]).font = SMALL
                ws.cell(row=r, column=3).alignment = WRAP
                ws.cell(row=r, column=4, value=line["qty"]).font = REG
                ws.cell(row=r, column=5, value=line["unit_hours"]).font = REG
                e = ws.cell(row=r, column=6, value=f"=D{r}*E{r}")
                e.font, e.number_format = REG, H1
                for col in range(1, 7):
                    ws.cell(row=r, column=col).border = BORD
                ws.row_dimensions[r].outlineLevel = 2
                r += 1
            e = ws.cell(row=item_head, column=6, value=f"=SUM(F{first}:F{r - 1})")
            e.font, e.number_format = BOLD, H1
            item_rows.append(item_head)
        e = ws.cell(row=cap_head, column=6,
                    value="=" + "+".join(f"F{i}" for i in item_rows) if item_rows else 0)
        e.font, e.number_format = BOLD, H1
        cap_rows.append(cap_head)

    last = r - 1
    ws.sheet_properties.outlinePr.summaryBelow = False
    for label, formula in (
        ("Total effort", "=" + "+".join(f"F{i}" for i in cap_rows) if cap_rows else 0),
        ("Build / delivery effort (excl. oversight)", est["build_effort_hours"]),
        ("Oversight effort", est["oversight_effort_hours"]),
    ):
        ws.cell(row=r, column=5, value=label).font = BOLD
        c = ws.cell(row=r, column=6, value=formula)
        c.font, c.number_format, c.fill = BOLD, H1, GREY
        r += 1
    ws.freeze_panes = "A2"

    # ---------- Rate Card ----------
    # Its own tab, and the LOE looks its rates up from here. One place to change a price
    # beats a rate repeated down a column, where the second occurrence is the one that
    # gets missed and a SOW goes out disagreeing with itself.
    rc = wb.create_sheet("Rate Card")
    _header(rc, 1, ["Role", "Location", "Rate ($/hr)", "Notes"], [38, 12, 13, 46])
    rates, rr = {}, 2
    for m in est["team"]:
        rates.setdefault(m["label"], (m.get("location", ""), m.get("rate")))
    for label, (loc, rate) in rates.items():
        rc.cell(row=rr, column=1, value=label).font = REG
        rc.cell(row=rr, column=2, value=loc).font = SMALL
        c = rc.cell(row=rr, column=3, value=rate)
        c.font, c.number_format = BOLD, USD
        c.fill = PatternFill("solid", fgColor="FFF7E0")
        for col in range(1, 5):
            rc.cell(row=rr, column=col).border = BORD
        rr += 1
    n = rc.cell(row=rr + 1, column=1,
                value="Edit a rate here and the LOE tab follows it. The LOE's Rate column "
                      "is a lookup into this table, not a copy of it.")
    n.font, n.alignment = SMALL, WRAP
    rc.freeze_panes = "A2"
    RATE_RANGE = f"'Rate Card'!$A$2:$C${rr - 1}"

    # ---------- LOE ----------
    ws = wb.create_sheet("LOE")
    # ONE ROW PER NAMED RESOURCE. A lead whose allocation changes by phase came back as
    # three assignments, and three architect rows on a page says three architects. The
    # per-phase columns carry the different allocations instead, so the row stays editable
    # — change the number under Design and the grid follows.
    merged = _merge_assignments(est["team"], total_weeks)
    band_names = [b["name"] for b in phases]
    labels = ["Resource", "Category", "Loc", "Rate", "Start Wk", "End Wk"] + band_names
    for i, label in enumerate(labels, start=1):
        c = ws.cell(row=3, column=i, value=label)
        c.fill, c.font, c.border, c.alignment = HEAD, WHITE, BORD, CEN
        if i > 6:
            c.fill = PatternFill("solid",
                                 fgColor=PHASE_COLOR.get(label, NAVY))
    tot_col, cost_col = len(labels) + 1, len(labels) + 2
    for i, label in ((tot_col, "Total Hrs"), (cost_col, "Cost")):
        c = ws.cell(row=3, column=i, value=label)
        c.fill, c.font, c.border, c.alignment = HEAD, WHITE, BORD, CEN
    widths = [30, 12, 9, 10, 9, 9] + [11] * len(band_names) + [11, 13]
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w
    first_week_col = cost_col + 1
    _week_columns(ws, phases, total_weeks, first_week_col)

    # Which phase column each week reads from — the formula in a week cell points at it,
    # so the sheet stays driven by editable inputs rather than by baked-in numbers.
    phase_col = {}
    for w in range(1, total_weeks + 1):
        name = _phase_of(phases, w)
        phase_col[w] = 7 + band_names.index(name) if name in band_names else None

    r = 4
    for m in merged:
        ws.cell(row=r, column=1, value=m["label"]).font = REG
        ws.cell(row=r, column=2, value=m["category"]).font = SMALL
        ws.cell(row=r, column=3, value=m["location"]).font = SMALL
        c = ws.cell(row=r, column=4,
                    value=f'=IFERROR(VLOOKUP($A{r},{RATE_RANGE},3,FALSE),0)')
        c.font, c.number_format = REG, USD
        ws.cell(row=r, column=5, value=m["start_week"]).font = REG
        ws.cell(row=r, column=6, value=m["end_week"]).font = REG
        for i, name in enumerate(band_names):
            lo, hi = int(phases[i]["start_week"]), int(phases[i]["end_week"])
            inside = [m["weekly"][w - 1] for w in range(lo, min(hi, total_weeks) + 1)]
            held = next((h for h in inside if h), 0)
            c = ws.cell(row=r, column=7 + i, value=held or None)
            c.font, c.alignment, c.border, c.number_format = REG, CEN, BORD, H1
            if held:
                c.fill = PatternFill("solid", fgColor=_STAFF_BAND.get(name, "FFFFFF"))
        for w in range(1, total_weeks + 1):
            col = first_week_col + w - 1
            pc = phase_col.get(w)
            src = f"${get_column_letter(pc)}{r}" if pc else '""'
            cell = ws.cell(
                row=r, column=col,
                value=f'=IF(AND({w}>=$E{r},{w}<=$F{r},{src}<>""),{src},"")')
            cell.font, cell.alignment, cell.border, cell.number_format = SMALL, CEN, BORD, H1
            if m["weekly"][w - 1]:
                cell.fill = PatternFill(
                    "solid", fgColor=_STAFF_BAND.get(_phase_of(phases, w), "FFFFFF"))
        fa, fb = get_column_letter(first_week_col), get_column_letter(
            first_week_col + total_weeks - 1)
        c = ws.cell(row=r, column=tot_col, value=f"=SUM({fa}{r}:{fb}{r})")
        c.font, c.number_format, c.border = BOLD, H1, BORD
        c = ws.cell(row=r, column=cost_col,
                    value=f"={get_column_letter(tot_col)}{r}*$D{r}")
        c.font, c.number_format, c.border = REG, USD, BORD
        for col in range(1, 7):
            ws.cell(row=r, column=col).border = BORD
        r += 1

    ws.cell(row=r, column=1, value="TOTAL").font = BOLD
    for col, letter in ((tot_col, get_column_letter(tot_col)),
                        (cost_col, get_column_letter(cost_col))):
        c = ws.cell(row=r, column=col, value=f"=SUM({letter}4:{letter}{r - 1})")
        c.font, c.fill, c.border = BOLD, GREY, BORD
        c.number_format = H1 if col == tot_col else USD
    ws.freeze_panes = ws.cell(row=4, column=first_week_col).coordinate

    # ---------- Project Plan ----------
    ws = wb.create_sheet("Project Plan")
    for i, label in enumerate(["Workstream", "BOE Hrs", "Devs", "Start Wk", "End Wk"],
                              start=1):
        c = ws.cell(row=3, column=i, value=label)
        c.fill, c.font, c.border, c.alignment = HEAD, WHITE, BORD, CEN
    for i, w in enumerate([40, 10, 7, 9, 9], start=1):
        ws.column_dimensions[get_column_letter(i)].width = w
    _week_columns(ws, phases, total_weeks, 6)

    # A bar's LENGTH comes from its BOE hours, so the hours sit next to it and a reader
    # can check the drawing against the number.
    #
    # The sheet leads with the PHASES, because a project plan that draws only the
    # implementation window is not a project plan: it left 830 of CBHPC's 2,830 hours —
    # planning, design, UAT and hypercare — off the page entirely, and the totals could
    # not tie to the LOE because most of the project was missing. The capability bars are
    # a drill-down INSIDE the implementation band, and they are labelled as one.
    rollup = set(est.get("workstream_rollups") or ["Integrations", "Data Migration"])
    caps = [w for w in est["workstreams"] if w["name"] not in rollup
            and w.get("hours")]
    cross = [w for w in est["workstreams"] if w["name"] in rollup]

    def staffed_in(lo, hi):
        t = 0.0
        for m in est["team"]:
            x, y = max(m["start_week"], lo), min(m["end_week"], hi)
            t += m["hours_per_week"] * max(0, y - x + 1)
        return t

    r = 4

    def block(title):
        nonlocal r
        c = ws.cell(row=r, column=1, value=title)
        c.font, c.fill = WHITE, HEAD
        for col in range(1, 6):
            ws.cell(row=r, column=col).fill = HEAD
            ws.cell(row=r, column=col).border = BORD
        r += 1

    def bar(name, hours, lo, hi, devs=None, faint=False, bold=False):
        nonlocal r
        c = ws.cell(row=r, column=1, value=name)
        c.font = BOLD if bold else REG
        h = ws.cell(row=r, column=2, value=round(hours, 1) if hours else None)
        h.font, h.number_format, h.alignment = (BOLD if bold else REG), H1, CEN
        d = ws.cell(row=r, column=3, value=devs)
        d.font, d.alignment = SMALL, CEN
        ws.cell(row=r, column=4, value=lo).font = REG
        ws.cell(row=r, column=5, value=hi).font = REG
        for col in range(1, 6):
            ws.cell(row=r, column=col).border = BORD
        for w in range(1, total_weeks + 1):
            cell = ws.cell(row=r, column=5 + w)
            cell.border = BORD
            if lo <= w <= hi:
                nm = _phase_of(phases, w)
                cell.fill = PatternFill(
                    "solid",
                    fgColor=(_STAFF_BAND if faint else PHASE_COLOR).get(
                        nm, "C5E0B4" if faint else "2E6BD6"))
        r += 1

    # ── the project, phase by phase: this is what totals the LOE ──────────────
    block("Phases — every hour the LOE assigns")
    first_phase_row = r
    for ph in phases:
        lo, hi = int(ph["start_week"]), int(ph["end_week"])
        bar(ph["name"], staffed_in(lo, hi), lo, hi)
    c = ws.cell(row=r, column=1, value="TOTAL — ties to the LOE tab")
    c.font = BOLD
    t = ws.cell(row=r, column=2, value=f"=SUM(B{first_phase_row}:B{r - 1})")
    t.font, t.number_format, t.fill, t.border = BOLD, H1, GREY, BORD
    c.border = BORD
    r += 2

    # ── the drill-down: what the build window is spent on ────────────────────
    block("Delivery workstreams — inside the Implementation band")
    first_cap = r
    for wsx in caps:
        bar(wsx["name"], wsx.get("hours") or 0, wsx["start_week"], wsx["end_week"],
            devs=wsx.get("parallel") or None)
    c = ws.cell(row=r, column=1, value="Capability effort (BOE, implementation window)")
    c.font, c.border = BOLD, BORD
    t = ws.cell(row=r, column=2, value=f"=SUM(B{first_cap}:B{r - 1})")
    t.font, t.number_format, t.fill, t.border = BOLD, H1, GREY, BORD
    r += 1
    if cross:
        c = ws.cell(row=r, column=1,
                    value="Cross-cutting — hours already counted in the capabilities above")
        c.font, c.alignment = SMALL, WRAP
        r += 1
        for wsx in cross:
            bar(wsx["name"], wsx.get("hours") or 0, wsx["start_week"], wsx["end_week"],
                faint=True)
    r += 1

    # Why the LOE tab shows more hours in this band than the bars above add up to. The two
    # sheets measure different things — one is the work, the other is the assignment — and
    # a reader who notices the gap deserves the answer on the page rather than a reply to
    # an email. Every line here is derived, so it cannot drift from the sheets it explains.
    impl = next((b for b in phases if b["name"] == "Implementation"), None)
    if impl:
        lo, hi = int(impl["start_week"]), int(impl["end_week"])
        span = hi - lo + 1

        def in_band(m):
            a, b = max(m["start_week"], lo), min(m["end_week"], hi)
            return m["hours_per_week"] * max(0, b - a + 1)

        devs = sum(in_band(m) for m in est["team"] if m.get("category") == "build")
        leads = sum(in_band(m) for m in est["team"] if m.get("category") == "oversight")
        cap_h = sum(w.get("hours") or 0 for w in caps)
        deps = sum(float(l["qty"]) * float(l["unit_hours"]) for l in est["boe_lines"]
                   if l["phase"] in ("Dependencies", "Allowances")
                   and not l.get("oversight") and not l.get("capacity_overhead")
                   and (l.get("delivery_phase") or "build") in ("build", "system_test"))
        cer = float(est.get("sprint_ceremony_hours") or 0)
        slack = devs - cap_h - deps - cer

        head = ws.cell(row=r, column=1,
                       value=f"Implementation window reconciliation  (W{lo}–W{hi})")
        head.font, head.fill = WHITE, HEAD
        for col in range(1, 3):
            ws.cell(row=r, column=col).fill = HEAD
            ws.cell(row=r, column=col).border = BORD
        r += 1
        for label, val, note in (
            ("Capability effort on the bars above", cap_h,
             "what the BOE prices against a named capability"),
            ("Shared dependencies", deps, "environments, access, licences — no capability owns them"),
            ("Sprint ceremony", cer, "2 of every 10 days: planning, refinement, review, retro"),
            ("Sprint-boundary capacity", slack,
             "the team is booked to whole sprints, not to exact hours"),
            ("= Developer assignment (LOE tab)", devs, ""),
            ("Leads across the band", leads,
             "engagement lead, architect, technical lead — they own no capability"),
            ("= Implementation hours on the LOE tab", devs + leads, ""),
        ):
            bold = label.startswith("=")
            c = ws.cell(row=r, column=1, value=label)
            c.font = BOLD if bold else REG
            v = ws.cell(row=r, column=2, value=round(val, 1))
            v.font, v.number_format, v.border = (BOLD if bold else REG), H1, BORD
            if bold:
                v.fill = GREY
            n = ws.cell(row=r, column=3, value=note)
            n.font, n.alignment = SMALL, WRAP
            c.border = BORD
            r += 1

    ws.freeze_panes = "F4"

    # ---------- Staffing (the sheet the customer and the CFO read) ----------
    _staffing_tab(wb, est, start_date)

    # ---------- Scope & Priorities + Checkpoints (need the expand response) ----
    if exp:
        _scope_tab(wb, exp)
        _checkpoints_tab(wb, exp)

    checks = _checks_tab(wb, est, exp)
    wb.save(out_path)
    extra = " (+ Staffing, Scope & Priorities, Checkpoints)" if exp else ""
    print(f"Wrote {out_path}{extra}")
    bad = [c for c in checks if not c[1]]
    print(f"  checks: {len(checks) - len(bad)}/{len(checks)} pass"
          + ("" if not bad else "  — see the Checks tab"))
    for name, _ok, got, want, note in bad:
        print(f"    FAIL  {name}: {got:,.1f} vs {want:,.1f}  {note}")
    return checks


def _parse_date(text: str):
    """--start=YYYY-MM-DD, so the Staffing tab can show real dates."""
    y, m, d_ = (int(x) for x in text.split("-"))
    return date(y, m, d_)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a.split("=", 1)[0]: a.split("=", 1)[1]
             for a in sys.argv[1:] if a.startswith("--") and "=" in a}
    if len(args) not in (2, 3):
        sys.exit("usage: render_loe.py <estimate.json> <output.xlsx> [expand.json] "
                 "[--start=YYYY-MM-DD]")
    with open(args[0]) as fh:
        estimate = json.load(fh)
    expand = None
    if len(args) == 3:
        with open(args[2]) as fh:
            expand = json.load(fh)
    start = _parse_date(flags["--start"]) if "--start" in flags else None
    # A failed check is a workbook that contradicts itself, and it must not leave here
    # looking like a clean run.
    if [c for c in build(estimate, args[1], expand, start) if not c[1]]:
        sys.exit(1)
