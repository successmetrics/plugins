#!/usr/bin/env python3
"""
Detect the Salesforce add-on LICENSE dependencies an engagement's scope triggers.

Scans an engagement requirements.yaml against product/pipeline/licenses.yaml and writes a
license-dependency matrix (markdown + yaml). Every engagement design must call out the add-on
licenses its scope needs (Maps, Field Service, Experience Cloud, Data Cloud, Agentforce, Shield,
etc.) AND the ones it explicitly does NOT need.

Usage:
  python3 detect_license_dependencies.py \
    --requirements engagements/<c>/design/requirements.yaml \
    --licenses product/pipeline/licenses.yaml \
    --out-md engagements/<c>/design/license-dependencies.md \
    --out-yaml engagements/<c>/design/license-dependencies.yaml
"""
import argparse, sys, datetime
try:
    import yaml
except ImportError:
    sys.exit("pip install pyyaml")

def req_text(r):
    parts = [r.get("title",""), r.get("statement",""), r.get("design_notes","")]
    return " ".join(parts).lower()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--requirements", required=True)
    ap.add_argument("--licenses", default="product/pipeline/licenses.yaml")
    ap.add_argument("--out-md", required=True)
    ap.add_argument("--out-yaml", required=True)
    a = ap.parse_args()

    reqs = yaml.safe_load(open(a.requirements))
    lic = yaml.safe_load(open(a.licenses))
    requirements = reqs.get("requirements", [])
    client = reqs.get("client", reqs.get("project", "engagement"))

    triggered, not_triggered = [], []
    for entry in lic.get("licenses", []):
        hits = []
        for r in requirements:
            t = req_text(r)
            matched = [kw for kw in entry.get("triggers", []) if kw.lower() in t]
            if matched:
                hits.append({"req": r["id"], "matched": matched})
        rec = {
            "capability": entry["capability"],
            "license": entry["license"],
            "included_with_pss": entry.get("included_with_pss", False),
            "note": entry.get("note",""),
            "driven_by": [h["req"] for h in hits],
        }
        (triggered if hits else not_triggered).append(rec)

    out = {
        "client": client,
        "generated_by": "grant-license-check",
        "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "baseline": lic.get("baseline", []),
        "required_addons": triggered,
        "not_required": [{"capability": r["capability"], "license": r["license"]} for r in not_triggered],
    }
    with open(a.out_yaml, "w") as f:
        yaml.safe_dump(out, f, sort_keys=False, default_flow_style=False)

    # markdown
    L = []
    L.append(f"# License Dependency Matrix — {client}")
    L.append("")
    L.append("Add-on Salesforce licenses this engagement's scope triggers, and the ones it does not. "
             "Confirm exact SKUs, tiers, and counts with the Salesforce account team.")
    L.append("")
    L.append("## Baseline (assumed)")
    for b in out["baseline"]:
        L.append(f"- **{b['license']}** — {b['capability']}. {b.get('note','')}")
    L.append("")
    L.append("## Required add-ons (triggered by requirements)")
    if triggered:
        L.append("")
        L.append("| Capability | License / entitlement | Included w/ PSS | Driven by |")
        L.append("|---|---|---|---|")
        for r in triggered:
            L.append(f"| {r['capability']} | {r['license']} | {'yes' if r['included_with_pss'] else 'no'} | {', '.join(r['driven_by'])} |")
        L.append("")
        for r in triggered:
            if r["note"]:
                L.append(f"- _{r['capability']}_: {r['note']}")
    else:
        L.append("_None triggered beyond the baseline._")
    L.append("")
    L.append("## Explicitly NOT required (by current scope)")
    for r in not_triggered:
        L.append(f"- {r['capability']} — {r['license']}")
    L.append("")
    L.append("> Re-run this whenever requirements change; scope creep often adds a license dependency.")
    open(a.out_md, "w").write("\n".join(L) + "\n")

    print(f"required add-ons: {len(triggered)} | not required: {len(not_triggered)}")
    for r in triggered:
        print(f"  + {r['capability']} -> {r['license']}  (driven by {', '.join(r['driven_by'])})")
    print("wrote", a.out_md, "and", a.out_yaml)

if __name__ == "__main__":
    main()
