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
    "UAT": "B45F06", "Go-Live": "1E7A46", "Support": "C55A11",
}
#: Light tints of the same phases, for cells that carry readable numbers —
#: the sprint and week rows, the weekly staffing cells, and the Staffing tab.
#: A number on top of PHASE_COLOR is unreadable, which is why there are two.
_STAFF_BAND = {
    "Planning/KT": "BDD7EE", "Design": "9DC3E6", "Implementation": "C5E0B4",
    "UAT": "FBE2D5", "Go-Live": "A9D18E", "Support": "F8CBAD",
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
    """Phase band + sprint number + week number, three header rows."""
    for w in range(1, total_weeks + 1):
        col = first_col + w - 1
        name = _phase_of(phases, w)
        band = ws.cell(row=1, column=col, value=name or "")
        band.fill = PatternFill("solid", fgColor=PHASE_COLOR.get(name, "CCCCCC"))
        band.font, band.alignment, band.border = WHITE, CEN, BORD

        # Sprint and week rows are tinted with the same phase colour as the band
        # above them, so a reader can see at a glance which sprints fall in which
        # phase without tracing a column up to the header.
        tint = PatternFill("solid", fgColor=_STAFF_BAND.get(name, "F2F5FA"))
        s = ws.cell(row=2, column=col, value=f"S{(w - 1) // 2 + 1}")
        s.font, s.alignment, s.border, s.fill = SMALL, CEN, BORD, tint

        h = ws.cell(row=3, column=col, value=f"W{w}")
        h.font, h.alignment, h.border, h.fill = BOLD, CEN, BORD, tint
        ws.column_dimensions[get_column_letter(col)].width = 5.5


YELLOW = PatternFill("solid", fgColor="FFFF00")
RED = Font(name="Arial", size=8, color="C00000")


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
                inside = m["start_week"] <= w <= m["end_week"]
                c = ws.cell(row, col, m["hours_per_week"] if inside else None)
                c.font, c.alignment, c.border, c.number_format = SMALL, CEN, BORD, H1
                if inside:
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

    impl = [m for m in est["team"] if str(m.get("category", "")) != "support"]
    support = [m for m in est["team"] if str(m.get("category", "")) == "support"]
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
    r = 2
    for line in est["boe_lines"]:
        ws.cell(row=r, column=1, value=line["phase"]).font = REG
        ws.cell(row=r, column=2, value=line["work_item"]).font = REG
        b = ws.cell(row=r, column=3, value=line["basis"])
        b.font, b.alignment = SMALL, WRAP
        ws.cell(row=r, column=4, value=line["qty"]).font = REG
        ws.cell(row=r, column=5, value=line["unit_hours"]).font = REG
        e = ws.cell(row=r, column=6, value=f"=D{r}*E{r}")
        e.font, e.number_format = REG, H1
        for col in range(1, 7):
            ws.cell(row=r, column=col).border = BORD
        r += 1

    last = r - 1
    for label, formula in (
        ("Total effort", f"=SUM(F2:F{last})"),
        ("Build / delivery effort (excl. oversight)", est["build_effort_hours"]),
        ("Oversight effort", est["oversight_effort_hours"]),
    ):
        ws.cell(row=r, column=5, value=label).font = BOLD
        c = ws.cell(row=r, column=6, value=formula)
        c.font, c.number_format, c.fill = BOLD, H1, GREY
        r += 1
    ws.freeze_panes = "A2"

    # ---------- LOE ----------
    ws = wb.create_sheet("LOE")
    labels = ["Resource", "Category", "Loc", "Rate", "Start Wk", "End Wk", "Hrs-Wk",
              "Total Hrs", "Cost"]
    for i, label in enumerate(labels, start=1):
        c = ws.cell(row=3, column=i, value=label)
        c.fill, c.font, c.border, c.alignment = HEAD, WHITE, BORD, CEN
    for i, w in enumerate([26, 13, 9, 9, 9, 9, 9, 11, 13], start=1):
        ws.column_dimensions[get_column_letter(i)].width = w
    first_week_col = len(labels) + 1
    _week_columns(ws, phases, total_weeks, first_week_col)

    r = 4
    for m in est["team"]:
        ws.cell(row=r, column=1, value=m["label"]).font = REG
        ws.cell(row=r, column=2, value=m["category"]).font = SMALL
        ws.cell(row=r, column=3, value=m["location"]).font = SMALL
        ws.cell(row=r, column=4, value=m["rate"]).number_format = USD
        ws.cell(row=r, column=5, value=m["start_week"]).font = REG
        ws.cell(row=r, column=6, value=m["end_week"]).font = REG
        ws.cell(row=r, column=7, value=m["hours_per_week"]).font = REG
        for w in range(1, total_weeks + 1):
            col = first_week_col + w - 1
            cell = ws.cell(
                row=r, column=col,
                value=f'=IF(AND({w}>=$E{r},{w}<=$F{r}),$G{r},"")',
            )
            cell.font, cell.alignment, cell.border, cell.number_format = SMALL, CEN, BORD, H1
            # Tint the weeks this resource is actually on, in that week's phase
            # colour. The cell value is a formula off editable start/end weeks,
            # so the fill is painted from the member's declared window rather
            # than from the formula's result, which does not exist until the
            # sheet is recalculated.
            if m["start_week"] <= w <= m["end_week"]:
                cell.fill = PatternFill(
                    "solid",
                    fgColor=_STAFF_BAND.get(_phase_of(phases, w), "FFFFFF"))
        lastw = get_column_letter(first_week_col + total_weeks - 1)
        t = ws.cell(row=r, column=8, value=f"=SUM({get_column_letter(first_week_col)}{r}:{lastw}{r})")
        t.font, t.number_format = REG, H1
        cost = ws.cell(row=r, column=9, value=f"=H{r}*D{r}")
        cost.font, cost.number_format = REG, USD
        for col in range(1, 10):
            ws.cell(row=r, column=col).border = BORD
        r += 1

    ws.cell(row=r, column=1, value="TOTAL").font = BOLD
    for col, fmt in ((8, H1), (9, USD)):
        c = ws.cell(row=r, column=col,
                    value=f"=SUM({get_column_letter(col)}4:{get_column_letter(col)}{r-1})")
        c.font, c.number_format, c.fill = BOLD, fmt, GREY
    ws.freeze_panes = ws.cell(row=4, column=first_week_col)

    # ---------- Project Plan ----------
    ws = wb.create_sheet("Project Plan")
    for i, label in enumerate(["Workstream", "Start Wk", "End Wk"], start=1):
        c = ws.cell(row=3, column=i, value=label)
        c.fill, c.font, c.border, c.alignment = HEAD, WHITE, BORD, CEN
    for i, w in enumerate([42, 9, 9], start=1):
        ws.column_dimensions[get_column_letter(i)].width = w
    _week_columns(ws, phases, total_weeks, 4)

    r = 4
    for wsx in est["workstreams"]:
        ws.cell(row=r, column=1, value=wsx["name"]).font = REG
        ws.cell(row=r, column=2, value=wsx["start_week"]).font = REG
        ws.cell(row=r, column=3, value=wsx["end_week"]).font = REG
        for w in range(1, total_weeks + 1):
            cell = ws.cell(row=r, column=3 + w)
            cell.border = BORD
            if wsx["start_week"] <= w <= wsx["end_week"]:
                cell.fill = PatternFill(
                    "solid", fgColor=PHASE_COLOR.get(_phase_of(phases, w), "2E6BD6")
                )
        r += 1
    ws.freeze_panes = "D4"

    # ---------- Staffing (the sheet the customer and the CFO read) ----------
    _staffing_tab(wb, est, start_date)

    # ---------- Scope & Priorities + Checkpoints (need the expand response) ----
    if exp:
        _scope_tab(wb, exp)
        _checkpoints_tab(wb, exp)

    wb.save(out_path)
    extras = ["Staffing"] + (["Scope & Priorities", "Checkpoints"] if exp else [])
    print(f"Wrote {out_path}  (+ {', '.join(extras)})")


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
    build(estimate, args[1], expand, start)
