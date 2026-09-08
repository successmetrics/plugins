#!/usr/bin/env bash
# tdd_flow.sh — guided test-first git flow for Field Inspection engagements.
#
# The gate is ALWAYS run before a commit is created and before a branch is pushed. Nothing lands red.
# This is a GUIDE + helper: it prints each step, never force-pushes, and stops on the first failure.
#
# Subcommands:
#   start  <client> <slug>            # worktree ../<repo>.wt/<client>-<slug> on feature/<client>-<slug> (PSS_NO_WORKTREE=1: branch in place)
#   finish <client> <slug>            # remove that worktree once its branch is pushed/merged (refuses on uncommitted work)
#   gate   [<client>] [<org>]         # run the harness (static, or full if <org> given). exit 1 if red
#   tier   [<client>]                 # 1|2|3 from what the diff touches (docs/38 C5). exit 3 on tier 3
#   verify <client> [<org>]           # gate -> tier -> verifier-input.json + mrp.md for the INDEPENDENT Verifier
#   commit <client> "<message>" [org] # stage -> gate -> tier -> mrp checks -> commit -> push (only if all green)
#   status                            # show branch + gate summary
#
# Branch convention:  feature/<client>-<slug>   (e.g. feature/<client>-add-device-type)
# Commit convention:  [<client>] <message>  (+ trailer with the gate result for traceability)
#
# docs/38 (2026-09-06): the session that built a change never judges it. `verify` packages ONLY the
# ACs + diff + gate result for a fresh-context Verifier subagent, which fills the verdicts in mrp.md;
# `commit` refuses without a filled MRP, with an empty "Not verified", on tier 3, or when metadata
# changed and no doc under engagements/<client>/docs changed without an "n/a:" reason in the MRP.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"        # repo root (skill is .claude/skills/fi-test)
[ -d "$ROOT/product/pipeline/testkit" ] || ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
TESTKIT="$ROOT/product/pipeline/testkit"
RUN="python3 $TESTKIT/fi_test.py"

# docs/38 C4 — worktree per Story: ../<repo>.wt/<client>-<slug>. Set PSS_NO_WORKTREE=1 for the
# legacy checkout-in-place behaviour.
worktree_path() { echo "$(dirname "$ROOT")/$(basename "$ROOT").wt/${1}-${2}"; }

default_branch() {
  git -C "$ROOT" symbolic-ref -q --short refs/remotes/origin/HEAD 2>/dev/null | sed 's#^origin/##' || echo main
}
# Every path touched on this branch vs the default branch, plus anything staged/unstaged right now.
changed_files() {
  { git -C "$ROOT" diff --name-only "$(default_branch)"...HEAD 2>/dev/null
    git -C "$ROOT" status --porcelain 2>/dev/null | awk '{print $NF}'; } | sort -u
}

# --- C5: risk tier, computed from the diff, never declared ---------------------------------------
# 3 = product tier / gates / licences / profile floor / contract baseline / any skip var set -> human commits
# 2 = engagement Apex, scope|hook|extension CMDT rows, baseline packs, content library -> human reads MRP
# 1 = additive engagement ext (fields, layouts, pages, flows, seeds, docs)          -> agent-verified + 1 approve
compute_tier() {  # prints "TIER=n" then one reason per line; returns 0
  local tier=1 reasons=()
  if env | grep -qE '^(FI|PSS|LPI|GRANT)_SKIP_[A-Z_]+='; then
    tier=3; reasons+=("skip variable set: $(env | grep -oE '^(FI|PSS|LPI|GRANT)_SKIP_[A-Z_]+' | tr '\n' ' ')")
  fi
  while IFS= read -r f; do
    [ -z "$f" ] && continue
    case "$f" in
      product/sfdx/*|product/pipeline/*|product/scripts/*|product/design/*|.claude/*|*/licenses.yaml|*min_org_profile.yaml|*/test-contract.yaml)
        # engagement contract EXTENSIONS are tier 2; the product baseline contract is tier 3
        if [[ "$f" == engagements/*/design/test-contract.yaml ]]; then
          [ "$tier" -lt 2 ] && tier=2; reasons+=("t2 engagement contract: $f")
        else
          tier=3; reasons+=("t3 product/gate tier: $f")
        fi ;;
      product/baseline-*|product/content-library/*)
        [ "$tier" -lt 2 ] && tier=2; reasons+=("t2 unmanaged pack: $f") ;;
      engagements/*.cls|engagements/*.trigger|engagements/*/customMetadata/*Scope*|engagements/*/customMetadata/*Extension*|engagements/*/customMetadata/*Hook*)
        [ "$tier" -lt 2 ] && tier=2; reasons+=("t2 engagement Apex/scope/hook: $f") ;;
    esac
  done < <(changed_files)
  echo "TIER=$tier"; printf '  %s\n' "${reasons[@]:-additive engagement change only}"
}

# --- C1/C3: package the Verifier's inputs and the merge-readiness pack skeleton ------------------
VERIFY_DIRNAME=".verify"
write_verifier_bundle() {  # args: client org tier gate_json gate_log
  local client="$1" org="${2:-}" tier="$3" gate_json="$4" gate_log="$5"
  local eng="$ROOT/engagements/$client" vdir="$ROOT/engagements/$client/$VERIFY_DIRNAME"
  mkdir -p "$vdir"
  printf '*\n!mrp.md\n!.gitignore\n' > "$vdir/.gitignore"   # only the MRP is traceability; logs/diff are churn
  local branch; branch="$(git -C "$ROOT" rev-parse --abbrev-ref HEAD)"
  git -C "$ROOT" diff "$(default_branch)"...HEAD > "$vdir/diff.patch" 2>/dev/null || true
  git -C "$ROOT" diff HEAD >> "$vdir/diff.patch" 2>/dev/null || true
  # UNTRACKED files are part of the change too (goldenville 2026-09-06: a brand-new engagement produced an EMPTY
  # diff.patch — the Verifier would have had nothing to verify and could still have said "pass").
  while IFS= read -r uf; do
    [ -z "$uf" ] && continue
    # inbox/ is the customer's INPUT, not a change to verify — and it may carry an injection canary the factory
    # eval must never see outside inbox/ (goldenville 2026-09-06: the bundle's diff tripped the eval's canary check).
    case "$uf" in *"/$VERIFY_DIRNAME/"*|*.patch|*.log|*/inbox/*|inbox/*) continue;; esac
    git -C "$ROOT" diff --no-index -- /dev/null "$uf" >> "$vdir/diff.patch" 2>/dev/null || true
  done < <(git -C "$ROOT" ls-files --others --exclude-standard)
  [ -s "$vdir/diff.patch" ] || { echo "✗ diff.patch is EMPTY — nothing to verify; refusing to write a bundle that would verify nothing." >&2; return 1; }
  # ACs: every Gherkin AC-* line the engagement's use cases carry (the Verifier gets the spec, not the plan)
  local uc="$eng/design/use-cases.yaml"
  if [ -f "$uc" ]; then
    python3 - "$uc" > "$vdir/acs.txt" <<'PY2' || grep -nE 'AC-[0-9]' "$uc" > "$vdir/acs.txt"
import sys, yaml
d = yaml.safe_load(open(sys.argv[1])) or {}
n = 0
for uc in d.get("use_cases", []) or []:
    print(f"{uc.get('id')} — {uc.get('title')}  [reqs: {', '.join(uc.get('requirements', []) or [])}]")
    for ac in uc.get("acceptance_criteria", []) or []:
        n += 1; print(f"  {ac.get('id')}: {ac.get('gherkin') or ac}")
if n == 0: print("NO acceptance_criteria found in use-cases.yaml — Verifier must derive ACs from design/requirements.yaml and say so")
PY2
  else
    echo "NO use-cases.yaml — Verifier must read engagements/$client/design/requirements.yaml and derive ACs" > "$vdir/acs.txt"
  fi
  python3 - "$vdir" "$client" "$org" "$tier" "$branch" "$gate_json" "$gate_log" <<'PY'
import json, sys, os
vdir, client, org, tier, branch, gate_json, gate_log = sys.argv[1:8]
gate = None
if gate_json and os.path.exists(gate_json):
    try: gate = json.load(open(gate_json))
    except Exception as e: gate = {"unparseable": str(e)}
bundle = {
  "purpose": "Inputs for the INDEPENDENT Verifier subagent (docs/38 C1). Give it NOTHING else: no transcript, no plan.",
  "client": client, "branch": branch, "org_readonly": org or None, "tier": int(tier),
  "acs_file": os.path.join(vdir, "acs.txt"), "diff_file": os.path.join(vdir, "diff.patch"),
  "gate_log": gate_log, "gate_json": gate,
  "return_contract": "one line per AC: {ac, verdict: pass|fail|unverifiable, evidence: test name+result or file:line (+ org query)}; "
                     "an AC with no traceable file:line in the diff is FAIL even if tests are green (C2 intent trace)."
}
json.dump(bundle, open(os.path.join(vdir, "verifier-input.json"), "w"), indent=2)
PY
  # MRP skeleton — the Verifier fills ACs; the Implementor fills Verified/Not verified/Decided alone/Docs.
  local mrp="$vdir/mrp.md"
  if [ ! -f "$mrp" ] || ! grep -q "^Branch: $branch\$" "$mrp"; then   # (re)generate when missing or from another branch
    cat > "$mrp" <<EOF
## Merge-readiness pack — $client
Branch: $branch
Tier: $tier
ACs:        <Verifier fills: n pass / n fail / n unverifiable; one line each: AC-id | verdict | evidence>
Gates:      $(grep -E '▶ gate|BLOCKED|PASS|FAIL' "$gate_log" 2>/dev/null | tr '\n' ';' | cut -c1-400)
Surface:    $(git -C "$ROOT" diff --quiet "$(default_branch)"...HEAD -- product/design/api-surface.json 2>/dev/null && echo "api-surface diff: none" || echo "api-surface diff: CHANGED — additive (snapshot regenerated) or BREAKING (major bump + migration note)?")
Licences:   $(git -C "$ROOT" diff --quiet "$(default_branch)"...HEAD -- '*licenses.yaml' 'engagements/'"$client"'/design/license-dependencies.*' 2>/dev/null && echo "triggers touched: none" || echo "triggers touched: SEE DIFF")
Coverage:   <new Apex xx% (policy >=75, target >=90) or n/a: no Apex>
Docs:       <admin guide | user guide | design doc | integration spec — updated paths, or n/a: <reason>>
Verified:      <what was observed, and where>
Not verified:  <what was assumed, unreachable, or out of time — never empty>
Decided alone: <judgment calls a reviewer might make differently>
EOF
  fi
  echo "✓ verifier bundle: $vdir/verifier-input.json  (acs.txt, diff.patch, gate log)"
  echo "✓ MRP skeleton:    $mrp"
  echo "  Next: spawn the Verifier with ONLY verifier-input.json; paste its AC verdicts into mrp.md; fill Docs/Verified/Not verified/Decided alone."
}

# --- commit-time checks on the MRP (C3 + docs-as-you-go) -----------------------------------------
check_mrp() {  # args: client ; exit 1 with reasons
  local client="$1" bad=0
  local mrp="$ROOT/engagements/$client/$VERIFY_DIRNAME/mrp.md"
  if [ ! -f "$mrp" ]; then echo "✗ no MRP: run tdd_flow.sh verify $client first" >&2; return 1; fi
  grep -q '^ACs:.*<Verifier fills' "$mrp" && { echo "✗ MRP: ACs not filled by the Verifier" >&2; bad=1; }
  grep -qE '^ACs:.*([1-9][0-9]* fail|\| *fail *\|)' "$mrp" && { echo "✗ MRP: at least one AC verdict is fail" >&2; bad=1; }
  if ! grep -qE '^Not verified:\s*\S' "$mrp" || grep -q '^Not verified:.*<what was assumed' "$mrp"; then
    echo "✗ MRP: 'Not verified' is empty or unfilled — an empty one is never true" >&2; bad=1; fi
  grep -q '^Verified:.*<what was observed' "$mrp" && { echo "✗ MRP: 'Verified' unfilled" >&2; bad=1; }
  # docs-as-you-go: metadata changed on this branch => a doc under engagements/<client>/docs changed, or an explicit n/a reason
  local meta docs
  meta="$(changed_files | grep -E "^engagements/$client/(ext|site|seeds|design)/" | grep -vE '\.verify/' | head -1 || true)"
  docs="$(changed_files | grep -E "^engagements/$client/docs/" | head -1 || true)"
  if [ -n "$meta" ] && [ -z "$docs" ] && ! grep -qE '^Docs:\s*n/a:\s*\S' "$mrp"; then
    echo "✗ docs-as-you-go: $meta changed but nothing under engagements/$client/docs/ did, and MRP 'Docs:' has no 'n/a: <reason>'" >&2
    echo "  (admin guide / user guide / design doc / integration spec are written WITH the Story, not at the end)" >&2; bad=1; fi
  grep -q '^Docs:.*<admin guide' "$mrp" && { echo "✗ MRP: 'Docs' unfilled" >&2; bad=1; }
  return $bad
}

run_gate() {  # args: [client] [org]
  local client="${1:-}" org="${2:-}"
  local args=(--quiet)
  [ -n "$client" ] && args+=(--engagement "$ROOT/engagements/$client")
  if [ -n "$org" ]; then args+=(--mode full --org "$org"); else args+=(--mode static); fi
  # Persist the result so `verify` can hand it to the Verifier without re-running (docs/38 C1).
  local vdir="/tmp/tdd_flow"; [ -n "$client" ] && vdir="$ROOT/engagements/$client/$VERIFY_DIRNAME"
  mkdir -p "$vdir"; GATE_LOG="$vdir/gate.log"; GATE_JSON="$vdir/gate.json"
  printf '*\n!mrp.md\n!.gitignore\n' > "$vdir/.gitignore"   # a BLOCKED gate must not leave untracked churn behind
  args+=(--json-out "$GATE_JSON")
  echo "▶ gate: $RUN ${args[*]}"
  $RUN "${args[@]}" 2>&1 | tee "$GATE_LOG"      # pipefail => exit status is the harness's
}
GATE_LOG=""; GATE_JSON=""

cmd="${1:-}"; shift || true
case "$cmd" in
  start)
    client="${1:?usage: tdd_flow.sh start <client> <slug>}"; slug="${2:?slug required}"
    branch="feature/${client}-${slug}"
    if [ -n "${PSS_NO_WORKTREE:-}" ]; then      # legacy: branch in THIS tree
      echo "▶ creating branch $branch off $(git -C "$ROOT" rev-parse --abbrev-ref HEAD)"
      git -C "$ROOT" checkout -b "$branch" 2>/dev/null || git -C "$ROOT" checkout "$branch"
      echo "✓ on $branch. Now: add the expectation to engagements/$client/design/test-contract.yaml (RED), then build to GREEN."
      exit 0
    fi
    # docs/38 C4: one WORKTREE per Story. Independent Stories build in parallel, the Verifier
    # checks out a tree it did not author, and a failed Story is `finish`, not a reset.
    wt="$(worktree_path "$client" "$slug")"
    if [ -d "$wt" ]; then
      echo "✓ worktree already exists: $wt ($(git -C "$wt" rev-parse --abbrev-ref HEAD))"
    else
      mkdir -p "$(dirname "$wt")"
      echo "▶ worktree $wt on $branch off $(git -C "$ROOT" rev-parse --abbrev-ref HEAD)"
      if git -C "$ROOT" show-ref --verify --quiet "refs/heads/$branch"; then
        git -C "$ROOT" worktree add "$wt" "$branch"
      else
        git -C "$ROOT" worktree add -b "$branch" "$wt"
      fi
      # Jest needs node_modules; a fresh worktree has none. Share the main tree's install.
      [ -d "$ROOT/node_modules" ] && [ ! -e "$wt/node_modules" ] && ln -s "$ROOT/node_modules" "$wt/node_modules"
    fi
    if [ ! -d "$wt/engagements/$client" ]; then
      echo "✗ engagements/$client is NOT in git, so the worktree cannot see it (found on _example-city, 2026-09-06)." >&2
      echo "  Commit the engagement first, or use PSS_NO_WORKTREE=1 to branch in place. Removing the empty worktree." >&2
      git -C "$ROOT" worktree remove --force "$wt"; exit 1
    fi
    echo "✓ $branch in $wt"
    echo "  cd \"$wt\"   # every later step runs THERE (its own tdd_flow.sh); org auth is user-global — pass --target-org explicitly"
    echo "  Now: add the expectation to engagements/$client/design/test-contract.yaml (RED), then build to GREEN."
    echo "  Product-tier edits do not belong in a Story worktree (tier 3 refuses them anyway)."
    ;;
  finish)
    client="${1:?usage: tdd_flow.sh finish <client> <slug>}"; slug="${2:?slug required}"
    branch="feature/${client}-${slug}"; wt="$(worktree_path "$client" "$slug")"
    [ -d "$wt" ] || { echo "✗ no worktree at $wt" >&2; exit 1; }
    if [ -n "$(git -C "$wt" status --porcelain)" ]; then
      echo "✗ $wt has uncommitted changes — commit (tdd_flow.sh commit) or discard them first." >&2; exit 1
    fi
    if ! git -C "$ROOT" branch -r --contains "$(git -C "$wt" rev-parse HEAD)" 2>/dev/null | grep -q .; then
      echo "✗ $branch HEAD is not on any remote branch — push it (or the PR was never opened) before removing the tree." >&2; exit 1
    fi
    git -C "$ROOT" worktree remove "$wt" && echo "✓ removed $wt (branch $branch kept; delete it after the PR merges)"
    ;;
  gate)
    run_gate "${1:-}" "${2:-}"
    ;;
  tier)
    out="$(compute_tier)"; echo "$out"
    t="$(echo "$out" | head -1 | cut -d= -f2)"
    if [ "$t" = 3 ]; then
      echo "✗ TIER 3 — product/gate/licence/profile/contract-baseline change (or a skip variable is set)." >&2
      echo "  A human commits and merges this; author ≠ approver. The agent stops here (docs/38 C5)." >&2; exit 3
    fi
    [ "$t" = 2 ] && echo "ℹ TIER 2 — one human approves after READING the MRP; org-mode gate expected."
    [ "$t" = 1 ] && echo "ℹ TIER 1 — agent-verified + one human approve."
    ;;
  verify)
    client="${1:?usage: tdd_flow.sh verify <client> [org]}"; org="${2:-}"
    echo "== 1/3 gate =="
    if ! run_gate "$client" "$org"; then echo "✗ gate BLOCKED — fix before asking a Verifier to look." >&2; exit 1; fi
    echo "== 2/3 tier =="
    out="$(compute_tier)"; echo "$out"; t="${out%%$'\n'*}"; t="${t#TIER=}"
    echo "== 3/3 verifier bundle + MRP =="
    write_verifier_bundle "$client" "$org" "$t" "$GATE_JSON" "$GATE_LOG"
    if [ "$t" = 3 ]; then echo "✗ TIER 3 — bundle written for the human reviewer; the agent does not commit this." >&2; exit 3; fi
    exit 0
    ;;
  commit)
    client="${1:?usage: tdd_flow.sh commit <client> \"<message>\" [org]}"; msg="${2:?message required}"; org="${3:-}"
    echo "== 1/5 run the gate (must be GREEN before commit) =="
    if ! run_gate "$client" "$org"; then
      echo "✗ gate BLOCKED — not committing. Fix the CRITICAL findings first." >&2; exit 1
    fi
    echo "== 2/5 tier =="
    out="$(compute_tier)"; echo "$out"; t="${out%%$'\n'*}"; t="${t#TIER=}"
    if [ "$t" = 3 ]; then
      echo "✗ TIER 3 — the agent may not commit a product/gate/licence/profile/contract-baseline change or one made with a skip variable set." >&2
      echo "  Hand the branch to a human: they run this same commit; the MRP records who." >&2; exit 3
    fi
    echo "== 3/5 merge-readiness pack =="
    mrp="$ROOT/engagements/$client/$VERIFY_DIRNAME/mrp.md"
    if [ ! -f "$mrp" ]; then write_verifier_bundle "$client" "$org" "$t" "$GATE_JSON" "$GATE_LOG"; fi
    if ! check_mrp "$client"; then echo "✗ MRP incomplete — not committing (docs/38 C3)." >&2; exit 1; fi
    branch="$(git -C "$ROOT" rev-parse --abbrev-ref HEAD)"
    echo "== 4/5 stage + commit on $branch =="
    git -C "$ROOT" add -A
    git -C "$ROOT" commit -m "[$client] $msg" \
      -m "Gate: PASS (fi-test $( [ -n "$org" ] && echo "full/$org" || echo static )) | Tier: $t" \
      -m "$(cat "$mrp")"
    echo "== 5/5 push (no force) =="
    git -C "$ROOT" push -u origin "$branch"
    echo "✓ pushed $branch. Open the PR with $mrp as the body — traceability: contract + code + gate + MRP are in the commit."
    ;;
  status)
    echo "branch: $(git -C "$ROOT" rev-parse --abbrev-ref HEAD)"
    git -C "$ROOT" status --short || true
    run_gate "" "" || true
    ;;
  *)
    sed -n '2,20p' "$0"; exit 2 ;;
esac
