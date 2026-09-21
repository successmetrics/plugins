#!/bin/bash
# Wire an engagement repository so the gate CANNOT be skipped.
#
# WHY THIS EXISTS
# ---------------
# `sm-quality-gates` explains the gate well and fires when a model judges it
# relevant. That is a hope, not a process. On the first engagement taken all the
# way to a deployed org, the rules were all written and none of them ran: six
# objects and 146 fields shipped with four of them on screen, and the build
# reported green.
#
# When this goes to a customer or a contractor there is nobody to remind. The
# reminder has to be in the repository, which means it has to be scaffolded
# rather than remembered — including by the agent doing the scaffolding.
#
# WHAT IT INSTALLS — four layers, because each covers the others' blind spot
#
#   CI          .github/workflows/gate.yml     always; nobody can bypass it
#   git         .githooks/pre-push             before CI, locally
#   Claude      .claude/settings.json          before the deploy command runs
#   convention  scripts/deploy.sh              the only sanctioned path
#
# plus CLAUDE.md, which is the only deterministic lever on WHICH SKILLS get
# used: a skill description is a judgement call every session, CLAUDE.md is
# read unconditionally.
#
# Idempotent. Never overwrites a file you have edited — it writes `.proposed`
# next to it and tells you, because an engagement that has tuned its gate has
# usually tuned it for a reason.

set -euo pipefail

ROOT="${1:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
ROOT="$(cd "$ROOT" && pwd)"
cd "$ROOT"

CHANGED=0
KEPT=()

# Write $1 with content from stdin, unless it exists and differs from what we
# last shipped — in which case leave the edit alone and put ours beside it.
put () {
    local path="$1" mode="${2:-644}"
    mkdir -p "$(dirname "$path")"
    local tmp; tmp="$(mktemp)"
    cat > "$tmp"
    if [ -f "$path" ] && ! cmp -s "$tmp" "$path"; then
        mv "$tmp" "$path.proposed"; chmod "$mode" "$path.proposed"
        KEPT+=("$path")
        return
    fi
    mv "$tmp" "$path"; chmod "$mode" "$path"
    CHANGED=$((CHANGED + 1))
}

# ---------------------------------------------------------------------------
put .githooks/pre-push 755 <<'EOF'
#!/bin/bash
# Nothing leaves this machine that has not passed the gate.
# Installed by scripts/bootstrap.sh via core.hooksPath, so a fresh clone gets it
# with one command instead of a paragraph in a README nobody reads.
echo "pre-push: running the gate…"
if bash "$(git rev-parse --show-toplevel)/scripts/gate.sh"; then
    exit 0
fi
cat <<'MSG'

════════════════════════════════════════════════════════════
 PUSH BLOCKED — the gate failed.

 Fix the build, not the check. To accept a finding, put it in
 test-contract.yaml with a named person and a specific reason.

 --no-verify exists and is logged by CI, which will fail anyway.
════════════════════════════════════════════════════════════
MSG
exit 1
EOF

# ---------------------------------------------------------------------------
# The matcher is the subtle part. A PreToolUse hook on `Bash` alone catches
# nothing when the work runs through an MCP shell — which is how most of it
# runs. Any tool that can spawn a shell is a way around a shell-matched hook.
put .claude/settings.json <<'EOF'
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|mcp__.*[Dd]esktop[_-]?[Cc]ommander.*|mcp__workspace__bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/scripts/preflight.py\"",
            "timeout": 900
          }
        ]
      }
    ]
  }
}
EOF

# ---------------------------------------------------------------------------
# CI discovers the engagement rather than naming it, so this file survives a
# rename and works in a repo carrying several.
put .github/workflows/gate.yml <<'EOF'
# The layer nobody can bypass. Local hooks are a courtesy; this is the rule.
name: gate
on:
  push:
    branches: [main]
  pull_request:
jobs:
  gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: gate
        env:
          SM_API_KEY: ${{ secrets.SM_API_KEY }}
        run: |
          if [ -z "$SM_API_KEY" ]; then
            echo "::error::SM_API_KEY is not set, so the shared canon rules were"
            echo "::error::NOT checked. A gate that cannot fetch its rules is not"
            echo "::error::a gate that passed."
            exit 1
          fi
          pip install sm-gates 2>/dev/null || pip install ./gates
          bash scripts/gate.sh
EOF

# ---------------------------------------------------------------------------
put scripts/bootstrap.sh 755 <<'EOF'
#!/bin/bash
# One command after a clone. Everything a new developer needs wired.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
git config core.hooksPath .githooks
echo "✔ git hooks installed (core.hooksPath = .githooks)"
echo "✔ Claude Code hook present in .claude/settings.json"
echo ""
echo "From here:"
echo "  ./scripts/gate.sh      check the build"
echo "  ./scripts/deploy.sh    gate, then deploy"
echo ""
echo "You cannot deploy or push around the gate. That is deliberate."
EOF

# ---------------------------------------------------------------------------
# CLAUDE.md is the ONLY deterministic lever on which skills get used. A skill
# fires when a model judges it relevant; this file is read every session
# regardless. Where the two disagree, this wins — so it names the pipeline
# explicitly rather than trusting description-matching.
if [ ! -f CLAUDE.md ]; then
put CLAUDE.md <<'EOF'
# How work is done in this repository

Read this before doing anything. It is read every session; a skill firing is a
judgement call every session, and the two are not the same kind of guarantee.

## The gate is not optional

`scripts/baseline_checks.py` runs with no network and no API key, and asserts
the things that are invisible rather than broken: a field on no layout, a layout
assigned to no profile, an app or tab or record type granted to nobody, an
object with no list view. **Wire it as a layer in `scripts/gate.sh`.**

They are all one class — *creating a thing and granting it are separate acts, and
only the first one is loud*. The deploy prints `Created` either way, so every
instance is found by a person opening the org and not seeing something.

`./scripts/gate.sh` is the only sanctioned check and `./scripts/deploy.sh` is
the only sanctioned deploy. Both are enforced four ways — CI, a pre-push hook,
a Claude `PreToolUse` hook, and convention — because the failure this prevents
is silent: a build that deploys clean, reports green, and is missing something
nobody looked for.

**Never deploy with a bare `sf project deploy start`.** It does not run the
gate, and it will not tell you that it did not.

**A layer that did not run is not a layer that passed.** If the gate prints
`NOT CHECKED` or `COVERAGE GAP`, the result is not green — read it, do not skim
to the last line.

## Which skills, and in what order

Use the `sm-delivery` plugin. If an older per-line factory plugin
(`xls-*`, `lpi-*`, `fi-*`, `grant-*`) is also installed, **prefer `sm-delivery`**
— those are its predecessors and their skills overlap it, so leaving the choice
to description-matching means the same job gets done two different ways in two
different sessions.

| doing this | use |
|---|---|
| requirements, RFP, transcript → scope | `sm-scope-engagement` |
| a spreadsheet application → a design | `sm-migrate-workbook` |
| pointing at an org that already has users | `sm-assess-org` **first** |
| pushing back on a design before build | `sm-review-design` |
| checking the build, wiring CI | `sm-quality-gates` |
| a wall of gate findings | `sm-triage-findings` |
| effort, timeline, staffing | `sm-estimate` |

## Suppressions

`test-contract.yaml` carries what this engagement accepts. Every entry names a
person and a specific reason — an unexplained suppression is indistinguishable
from someone silencing a rule they did not understand.

A suppression is signed against a rule-set digest, and the gate reports
**CONTRACT DRIFT** when canon has moved since. Re-triage, or withdraw it. An
acceptance carried across a rule change is a risk nobody has read.

## Verification

Every engagement in this line needs an independent tie-out: recompute the
expected numbers from the SOURCE, not from the org. A check that asks the org
for a number and then asks the org whether it is right proves only that the org
is consistent with itself.
EOF
else
    KEPT+=("CLAUDE.md")
fi

# ---------------------------------------------------------------------------
# Baseline checks. The layers above make a gate RUN; this makes it CHECK
# something. Shipping the layers alone was half a fix and the half that looks
# finished — an engagement got four ways to run a gate that knew nothing.
#
# These are the product-agnostic ones. Line-specific checks stay in the
# engagement's own run_checks.py.
put scripts/baseline_checks.py 755 <<'EOF'
#!/usr/bin/env python3
"""Checks every Salesforce engagement needs, whatever the product line.

THE CLASS THESE EXIST FOR
-------------------------
On this platform, CREATING a thing and GRANTING it are separate acts, and only
the first one is loud. `sf project deploy start` prints Created either way.

On the engagement that raised these, four instances of that one class shipped in
a single build:

    a field on no layout                present, queryable, invisible
    a record type in no permission set  active, assignable, selectable by none
    a layout assigned to no profile     built, deployed, shown to nobody
    an app in no applicationVisibilities   deployed, absent from the App Launcher

Three of the four were found by a person opening the org and not seeing
something, which is the most expensive way to find a defect and the last point
at which it is cheap to fix.

Canon covers the record-type case (SEC-004) and, once the server ships them,
SEC-006..008. This file is the floor underneath that: it runs with no network,
no API key, and no rule fetch, so an engagement is never unprotected because a
service was unreachable.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

FAILURES: list[tuple[str, str, str]] = []      # (check, severity, message)


def add(check: str, severity: str, message: str) -> None:
    FAILURES.append((check, severity, message))


def check_fields_are_on_a_layout(src: pathlib.Path) -> None:
    """A field nobody laid out is present, reportable, queryable and invisible.

    Deploying an object with no Layout does not fail and does not warn —
    Salesforce supplies a default carrying the name, the owner and two audit
    stamps. One build shipped 146 fields with four on screen and said Created
    for all of it.
    """
    surfaces = "\n".join(
        p.read_text(errors="replace")
        for p in list(src.glob("layouts/*.xml")) + list(src.glob("flexipages/*.xml")))
    for f in sorted(src.glob("objects/*/fields/*.field-meta.xml")):
        obj = f.parent.parent.name
        api = f.name[: -len(".field-meta.xml")]
        objx = (src / "objects" / obj / f"{obj}.object-meta.xml")
        if objx.exists() and "<customSettingsType>" in objx.read_text(errors="replace"):
            continue                      # custom settings have no page
        if api not in surfaces:
            add("fields_are_on_a_layout", "warn",
                f"{obj}.{api} is on no layout and no record page")


def check_layouts_are_assigned(src: pathlib.Path) -> None:
    """Only a PROFILE assigns a page — no permission set can.

    Note the %20: a profile spells a space that way, so comparing raw strings
    finds nothing and reports a clean run.
    """
    assigned = set()
    for prof in src.glob("profiles/*.profile-meta.xml"):
        for m in re.finditer(r"<layout>([^<]+)</layout>",
                             prof.read_text(errors="replace")):
            assigned.add(m.group(1).replace("%20", " "))
    for p in sorted(src.glob("layouts/*.layout-meta.xml")):
        stem = p.name[: -len(".layout-meta.xml")]
        if stem in assigned:
            continue
        custom = stem.split("-", 1)[0].endswith("__c")
        add("layouts_are_assigned", "warn" if custom else "critical",
            f"{stem} is assigned in no profile"
            + ("  (custom object: its first layout is auto-assigned, so this is "
               "probably reachable — but a second one would not be)" if custom
               else "  (standard object: it already has assignments, so this "
                    "layout deployed and is shown to nobody)"))


def _grants(src: pathlib.Path) -> str:
    return "\n".join(p.read_text(errors="replace")
                     for p in list(src.glob("permissionsets/*.xml"))
                     + list(src.glob("profiles/*.xml")))


def check_apps_are_visible(src: pathlib.Path) -> None:
    granted = set(re.findall(r"<application>([^<]+)</application>", _grants(src)))
    for p in sorted(src.glob("applications/*.app-meta.xml")):
        api = p.name[: -len(".app-meta.xml")]
        if api not in granted:
            add("apps_are_visible", "critical",
                f"the {api} app is granted by no permission set and no profile, "
                f"so nobody will find it in the App Launcher")


def check_tabs_are_visible(src: pathlib.Path) -> None:
    granted = set(re.findall(r"<tab>([^<]+)</tab>", _grants(src)))
    for p in sorted(src.glob("tabs/*.tab-meta.xml")):
        api = p.name[: -len(".tab-meta.xml")]
        if api not in granted:
            add("tabs_are_visible", "critical",
                f"the {api} tab is visible in no permission set and no profile")


def check_record_types_are_visible(src: pathlib.Path) -> None:
    visible = set(re.findall(r"<recordType>([^<]+)</recordType>", _grants(src)))
    for p in sorted(src.glob("objects/*/*.object-meta.xml")):
        obj = p.parent.name
        for m in re.finditer(r"<recordTypes>(.*?)</recordTypes>",
                             p.read_text(errors="replace"), re.S):
            block = m.group(1)
            if "<active>true</active>" not in block:
                continue
            name = re.search(r"<fullName>([^<]+)</fullName>", block)
            if name and f"{obj}.{name.group(1)}" not in visible:
                add("record_types_are_visible", "critical",
                    f"record type {obj}.{name.group(1)} is active and in no "
                    f"recordTypeVisibilities — nobody can select it")


def check_every_object_has_an_all_list_view(src: pathlib.Path) -> None:
    """A user who cannot find the records has no application."""
    for d in sorted((src / "objects").glob("*__c")):
        objx = d / f"{d.name}.object-meta.xml"
        if objx.exists() and "<customSettingsType>" in objx.read_text(errors="replace"):
            continue
        if not list(d.glob("listViews/*.listView-meta.xml")):
            add("object_has_a_list_view", "critical",
                f"{d.name} has no list view")


CHECKS = [check_fields_are_on_a_layout, check_layouts_are_assigned,
          check_apps_are_visible, check_tabs_are_visible,
          check_record_types_are_visible,
          check_every_object_has_an_all_list_view]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--engagement", default=".")
    a = ap.parse_args()
    src = pathlib.Path(a.engagement).resolve() / "src/main/default"
    if not src.is_dir():
        print(f"baseline: no metadata at {src} — nothing checked, which is NOT a pass")
        return 1

    print(f"baseline checks — {len(CHECKS)} checks")
    for c in CHECKS:
        c(src)

    crit = sum(1 for _, s, _ in FAILURES if s == "critical")
    for check, sev, msg in FAILURES:
        print(f"  [{sev:8}] {check}: {msg}")
    print(f"\n{crit} critical, {len(FAILURES) - crit} warn")
    return 1 if crit else 0


if __name__ == "__main__":
    raise SystemExit(main())
EOF

# ---------------------------------------------------------------------------
git config core.hooksPath .githooks 2>/dev/null || true

echo "scaffold-enforcement: $CHANGED file(s) written into $ROOT"
if [ ${#KEPT[@]} -gt 0 ]; then
    echo
    echo "Left alone because you had edited them (ours is beside it as .proposed):"
    for k in "${KEPT[@]}"; do echo "  $k"; done
fi
echo
echo "Still yours to provide, because they are engagement-specific:"
echo "  scripts/gate.sh        the entry point the four layers all call"
echo "  scripts/preflight.py   what the Claude hook blocks on"
echo "  scripts/deploy.sh      gate, then deploy"
echo "  test-contract.yaml     what this engagement accepts, and why"
echo
echo "  (wire scripts/baseline_checks.py in as a gate layer — it is shipped)"
echo
echo "Then: ./scripts/bootstrap.sh"
