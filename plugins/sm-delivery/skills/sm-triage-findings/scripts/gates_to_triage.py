#!/usr/bin/env python3
"""Turn `sm-gates run --format json` into an sm_triage_findings request.

The handoff between the two halves of decision §21 — the gate that blocks and
the agent that judges — exists so a caller PIPES rather than transcribes. A
transcription step is where the record drifts from what the gate actually said,
and a triage arguing about a finding nobody emitted is worse than no triage.

    sm-gates run --format json > gates.json
    python3 scripts/gates_to_triage.py gates.json > request.json
    # then call sm_triage_findings with request.json

WHAT LEAVES THIS MACHINE, STATED PLAINLY. Findings alone by default: rule id,
severity, message, path, line. Source excerpts are the difference between a
verdict and a guess — the mechanism a rule misread is usually only visible in
the code — but they are your customer's source, so attaching them is an
explicit `--context` and the script prints what it read. It will not quietly
upload a repository because that produced better verdicts.

    python3 scripts/gates_to_triage.py gates.json --context --lines 40

Severity filtering exists because MAX_FINDINGS is 120 and a real run can exceed
it. Splitting by severity keeps the highest-cost findings in the first call
rather than truncating arbitrarily.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

#: The tool refuses more than this in one call — beyond it a triage is a skim.
MAX_FINDINGS = 120

RANK = {"critical": 3, "error": 3, "warn": 2, "warning": 2, "info": 1}


def flatten(report: dict) -> list[dict]:
    """sm-gates nests findings under layers[]; the tool takes a flat list.

    Layer membership is dropped deliberately: it tells you which gate spoke,
    not anything about the finding, and the tool matches on rule_id + path.
    """
    out = []
    for layer in report.get("layers") or []:
        for f in layer.get("findings") or []:
            out.append({
                "rule_id": f.get("rule_id") or "",
                "severity": f.get("severity") or "",
                "title": f.get("title") or "",
                "message": f.get("message") or "",
                "path": f.get("path") or "",
                "line": f.get("line"),
                "detail": f.get("detail") or "",
            })
    return out


def excerpt(root: Path, path: str, line, span: int) -> str | None:
    p = (root / path) if not Path(path).is_absolute() else Path(path)
    if not p.is_file():
        return None
    try:
        lines = p.read_text(errors="replace").splitlines()
    except OSError:
        return None
    if line and 0 < line <= len(lines):
        lo = max(0, line - 1 - span // 2)
        return "\n".join(lines[lo:lo + span])
    return "\n".join(lines[:span])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("report", help="output of `sm-gates run --format json`")
    ap.add_argument("--engagement", default="")
    ap.add_argument("--context", action="store_true",
                    help="attach source excerpts for the cited paths — reads "
                         "your customer's files and sends them")
    ap.add_argument("--lines", type=int, default=40, help="excerpt size")
    ap.add_argument("--min-severity", choices=("info", "warn", "critical"),
                    default="info")
    ap.add_argument("--notes", default="",
                    help="vendored directories, intended system-context "
                         "services, personas — anything the reader should know")
    a = ap.parse_args()

    report = json.loads(Path(a.report).read_text())
    findings = flatten(report)
    if not findings:
        # Not an empty request — the tool would reject it, and rightly. Say why
        # here, where the reason is still visible.
        print("no findings in that report — there is nothing to triage. "
              "A triage of no findings is not a clean bill of health; the "
              "gate result already is one.", file=sys.stderr)
        return 2

    floor = RANK.get(a.min_severity, 1)
    kept = [f for f in findings if RANK.get(f["severity"].lower(), 1) >= floor]
    if len(kept) > MAX_FINDINGS:
        print(f"{len(kept)} findings exceeds the {MAX_FINDINGS} the tool takes "
              f"in one call. Raise --min-severity or split by directory — "
              "truncating here would hand you a triage that silently covered "
              "part of the run.", file=sys.stderr)
        return 2

    request = {"engagement": a.engagement, "findings": kept, "notes": a.notes}

    if a.context:
        root = Path(report.get("root") or ".")
        seen, ctx = set(), []
        for f in kept:
            if not f["path"] or f["path"] in seen:
                continue
            seen.add(f["path"])
            body = excerpt(root, f["path"], f["line"], a.lines)
            if body is not None:
                ctx.append({"path": f["path"], "excerpt": body})
        request["context"] = ctx
        print(f"attached {len(ctx)} source excerpt(s) from {root}; "
              f"{len(seen) - len(ctx)} cited path(s) could not be read",
              file=sys.stderr)

    json.dump(request, sys.stdout, indent=2)
    print(file=sys.stdout)
    print(f"{len(kept)} of {len(findings)} finding(s) at severity "
          f">= {a.min_severity}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
