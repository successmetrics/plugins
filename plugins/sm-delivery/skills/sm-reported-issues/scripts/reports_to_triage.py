#!/usr/bin/env python3
"""A tester's list to an sm_triage_reports request, and the response to a verdict table.

    python3 reports_to_triage.py request docs/issues/uat-round-3.input.yaml > request.json
    python3 reports_to_triage.py table response.json --input docs/issues/uat-round-3.input.yaml

`request` adds design/behaviour.yaml and the trace AS THEY STOOD at the input's
`contract_ref` — the build the tester used, not today's — so a rule written
because of this very round cannot be used to judge it. It prints to stderr
exactly which files it read and at which ref, because they leave the machine.

`table` writes docs/issues/<round>.yaml (the verdicts, each with `approved:`
empty for a person to fill) and docs/issues/<round>.md beside the input.

Standard library and PyYAML only. Reads; never writes outside the input's folder.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import yaml

CONTRACT_NAMES = ("behaviour.yaml",)
TRACE_NAMES = ("trace.yaml",)


def _git(*args: str, cwd: Path) -> str:
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout


def _repo_root(start: Path) -> Path:
    return Path(_git("rev-parse", "--show-toplevel", cwd=start).strip())


def _find(root: Path, names: tuple[str, ...]) -> Path | None:
    hits = sorted(p for n in names for p in root.rglob(n)
                  if "node_modules" not in p.parts and ".sfdx" not in p.parts and "design" in p.parts)
    return hits[0] if hits else None


def _read_at(root: Path, path: Path, ref: str) -> str:
    if not ref:
        return path.read_text()
    try:
        return _git("show", f"{ref}:{path.relative_to(root).as_posix()}", cwd=root)
    except subprocess.CalledProcessError:
        return ""


def _say(label: str, root: Path, path: Path | None, text: str, ref: str) -> None:
    where = path.relative_to(root).as_posix() if path else "none found"
    at = f" at {ref}" if ref else " (working tree)"
    size = f"{len(text)} bytes" if text else "EMPTY"
    print(f"{label}: {where}{at} — {size}", file=sys.stderr)


def request(args) -> int:
    inp = Path(args.input).resolve()
    data = yaml.safe_load(inp.read_text()) or {}
    root = _repo_root(inp.parent)
    ref = str(data.get("contract_ref") or "")
    contract_path = Path(args.contract).resolve() if args.contract else _find(root, CONTRACT_NAMES)
    trace_path = Path(args.trace).resolve() if args.trace else _find(root, TRACE_NAMES)
    contract = _read_at(root, contract_path, ref) if contract_path else ""
    trace = _read_at(root, trace_path, ref) if trace_path else ""
    _say("contract", root, contract_path, contract, ref)
    _say("trace   ", root, trace_path, trace, ref)
    if not contract:
        print("  no contract: nothing can be judged a bug, a regression or by design", file=sys.stderr)

    items = data.get("items") or []
    evidence = data.get("evidence") or []
    print(f"items: {len(items)}; evidence rows: {len(evidence)}", file=sys.stderr)
    if not items:
        print("no items in the input — nothing to triage", file=sys.stderr)
        return 2
    out = {
        "engagement": data.get("engagement", ""),
        "round": data.get("round", ""),
        "product_line": data.get("product_line", ""),
        "items": items,
        "evidence": evidence,
        "contract": contract,
        "trace": trace,
        "notes": data.get("notes", ""),
    }
    json.dump({"request": out}, sys.stdout, indent=2)
    print()
    return 0


def _slug(s: str) -> str:
    return "-".join("".join(c.lower() if c.isalnum() else " " for c in s).split()) or "round"


def _cell(s) -> str:
    return str(s or "").replace("|", "\\|").replace("\n", " ").strip()


def _change(r: dict) -> str:
    test = r.get("regression_test") or {}
    rule = r.get("proposed_rule") or {}
    if r["verdict"] == "gap" and rule.get("says"):
        return "rule: " + rule["says"]
    if test.get("criterion_id"):
        return f"test {test['criterion_id']} ({test.get('kind') or '?'}, {test.get('gate') or '?'})"
    return r.get("needs_to_know") or r.get("reply_to_tester") or ""


def table(args) -> int:
    resp = json.loads(Path(args.response).read_text())
    resp = resp.get("result", resp)
    inp = Path(args.input).resolve()
    data = yaml.safe_load(inp.read_text()) or {}
    titles = {str(i["id"]): i.get("title", "") for i in data.get("items") or []}
    stem = (inp.name[: -len(".input.yaml")] if inp.name.endswith(".input.yaml")
            else _slug(data.get("round", "")))

    rows = [{**v, "title": titles.get(v.get("item_id", ""), ""),
             "approved": None, "by": "", "changed_to": ""}
            for v in resp.get("verdicts") or []]
    doc = {
        "round": resp.get("round") or data.get("round", ""),
        "engagement": resp.get("engagement") or data.get("engagement", ""),
        "contract_ref": data.get("contract_ref", ""),
        "contract_digest": resp.get("contract_digest", ""),
        "prompt_version": resp.get("prompt_version", ""),
        "taxonomy_version": resp.get("taxonomy_version", ""),
        "advisory": True,
        "verdicts": rows,
        "not_triaged": resp.get("not_triaged") or [],
        "warnings": resp.get("warnings") or [],
    }
    yml = inp.parent / f"{stem}.yaml"
    mdp = inp.parent / f"{stem}.md"
    yml.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100))

    md = [f"# {doc['round']} — reported issues", "",
          f"Judged against the behaviour contract at `{doc['contract_ref'] or 'working tree'}` "
          f"({doc['contract_digest'][:19] or 'no contract'}). Advisory until each row is approved.", "",
          "| # | Finding | Verdict | Rule | Evidence | Root cause | Class | Change |",
          "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        verdict = r["verdict"] + (f" (was {r['downgraded_from']})" if r.get("downgraded_from") else "")
        cause = " · ".join(x for x in (r.get("root_cause_layer"), r.get("root_cause_change")) if x)
        md.append("| " + " | ".join(_cell(x) for x in (
            r["item_id"], r["title"], verdict, r.get("rule", ""), ", ".join(r.get("evidence") or []),
            cause, r.get("defect_class", ""), _change(r))) + " |")
    if doc["not_triaged"]:
        md += ["", "**Not triaged — not settled:** " + ", ".join(n["item_id"] for n in doc["not_triaged"])]
    if doc["warnings"]:
        md += ["", "## Warnings", ""] + [f"- {w}" for w in doc["warnings"]]
    mdp.write_text("\n".join(md) + "\n")
    print(f"wrote {yml} and {mdp}", file=sys.stderr)
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("request", help="build the sm_triage_reports request")
    r.add_argument("input")
    r.add_argument("--contract", help="behaviour.yaml path (default: found under a design/ folder)")
    r.add_argument("--trace", help="trace.yaml path (default: found under a design/ folder)")
    t = sub.add_parser("table", help="write <round>.yaml and .md beside the input")
    t.add_argument("response")
    t.add_argument("--input", required=True)
    args = ap.parse_args(argv)
    return request(args) if args.cmd == "request" else table(args)


if __name__ == "__main__":
    sys.exit(main())
