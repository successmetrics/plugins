#!/usr/bin/env python3
"""
Error-accommodating org API-name resolver for the LPI Accelerator.

Purpose: when you point the accelerator at a real sandbox, the assumed PSS object/
field API names in .sfdesign/design.yaml may differ from what the org actually exposes
(PSS version, licensing, managed-package namespaces, or a pre-existing equivalent field).
This script reconciles the design against the org BEFORE any generation/deploy and writes
.sfdesign/org-map.yaml. The build reads resolved names from that map and REFUSES to
deploy anything still unresolved (status ambiguous/missing) — it degrades to a question,
never a bad deploy.

Match ladder (per object and per field):
  1. exact            assumed == real
  2. caseless         case-insensitive equality
  3. namespace        ignore managed-package prefix (ns__Name__c ~ Name__c)
  4. alias            from pipeline/aliases.yaml (human-curated variants)
  5. fuzzy            difflib close match >= threshold  -> reported as 'ambiguous' (needs human OK)
  else                'missing' -> reviewer decides: map it, or create it as custom

Org metadata source (either works):
  * live: `sf sobject list --json` + `sf sobject describe --sobject X --json` (auto if `sf` present)
  * cached: --org-metadata org-metadata.json  (for CI / offline / repeatability)

Usage:
  python3 resolve_org_api_names.py --design ../.sfdesign/design.yaml \
      --aliases aliases.yaml --org-metadata org-metadata.json \
      --out ../.sfdesign/org-map.yaml [--fuzzy 0.86]
"""
import argparse, json, os, subprocess, sys, difflib, datetime
try:
    import yaml
except ImportError:
    sys.exit("pyyaml required: pip install pyyaml")

def load_yaml(p):
    with open(p) as f: return yaml.safe_load(f)

# ---------- collect assumed names from design.yaml ----------
def collect_assumed(design):
    """Return ({object_api: set(field_api)}, {object_api: kind})."""
    wanted={}; kinds={}
    for o in design.get("data_model",{}).get("objects",[]):
        api=o["api_name"]; wanted.setdefault(api,set()); kinds[api]=o.get("kind","standard")
        for f in o.get("fields",[]) or []:
            wanted[api].add(f["api_name"])
    # objects referenced only in relationships/security/etc. still need to exist
    for r in design.get("data_model",{}).get("relationships",[]):
        tgt=r.get("to")
        if tgt: wanted.setdefault(tgt,set()); kinds.setdefault(tgt,"standard")
    return wanted, kinds

# ---------- org metadata (live or cached) ----------
def org_metadata_live():
    def sf(*a):
        return json.loads(subprocess.check_output(["sf",*a,"--json"]))
    listing=sf("sobject","list","--sobject","all")
    names=listing.get("result",listing)
    meta={}
    for n in names:
        try:
            d=sf("sobject","describe","--sobject",n)
            res=d.get("result",d)
            meta[n]=[fld["name"] for fld in res.get("fields",[])]
        except Exception:
            meta[n]=[]
    return meta

def org_metadata(args):
    if args.org_metadata and os.path.exists(args.org_metadata):
        raw=load_json(args.org_metadata)
        # accept {obj: [fields]} or {objects:[{name,fields:[{name}]}]}
        if isinstance(raw,dict) and "objects" in raw:
            return {o["name"]:[f["name"] if isinstance(f,dict) else f for f in o.get("fields",[])] for o in raw["objects"]}
        return raw
    # live fallback
    from shutil import which
    if which("sf"):
        return org_metadata_live()
    sys.exit("No --org-metadata cache and `sf` CLI not found. Provide one.")

def load_json(p):
    with open(p) as f: return json.load(f)

# ---------- matching ----------
def strip_ns(name):
    # ns__Object__c -> Object__c ; ns__Field__c -> Field__c
    parts=name.split("__")
    if len(parts)>=3:   # namespace present: ns__Base__c
        return "__".join(parts[1:])
    return name

def match_one(assumed, real_names, aliases, fuzzy):
    real_by_lower={r.lower():r for r in real_names}
    real_by_stripped={strip_ns(r).lower():r for r in real_names}
    # 1 exact
    if assumed in real_names:
        return dict(status="matched", resolved=assumed, method="exact", candidates=[])
    # 2 caseless
    if assumed.lower() in real_by_lower:
        return dict(status="matched", resolved=real_by_lower[assumed.lower()], method="caseless", candidates=[])
    # 3 namespace
    key=strip_ns(assumed).lower()
    if key in real_by_stripped:
        return dict(status="matched", resolved=real_by_stripped[key], method="namespace", candidates=[])
    # 4 alias
    for cand in aliases.get(assumed,[]):
        if cand in real_names:
            return dict(status="matched", resolved=cand, method="alias", candidates=[])
        if cand.lower() in real_by_lower:
            return dict(status="matched", resolved=real_by_lower[cand.lower()], method="alias", candidates=[])
        ks=strip_ns(cand).lower()
        if ks in real_by_stripped:
            return dict(status="matched", resolved=real_by_stripped[ks], method="alias-namespace", candidates=[])
    # 5 fuzzy -> ambiguous (never auto-accept)
    close=difflib.get_close_matches(assumed, real_names, n=3, cutoff=fuzzy)
    if close:
        return dict(status="ambiguous", resolved=None, method="fuzzy", candidates=close)
    return dict(status="missing", resolved=None, method="none", candidates=[])

# ---------- main ----------
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--design", default="../.sfdesign/design.yaml")
    ap.add_argument("--aliases", default="aliases.yaml")
    ap.add_argument("--org-metadata", default=None)
    ap.add_argument("--out", default="../.sfdesign/org-map.yaml")
    ap.add_argument("--fuzzy", type=float, default=0.86)
    args=ap.parse_args()

    design=load_yaml(args.design)
    aliases_doc=load_yaml(args.aliases) if os.path.exists(args.aliases) else {}
    obj_aliases=aliases_doc.get("objects",{})
    fld_aliases=aliases_doc.get("fields",{})
    wanted, kinds=collect_assumed(design)
    org=org_metadata(args)
    real_objs=list(org.keys())

    out={"project":design.get("project"),
         "generated_by":"resolve_org_api_names",
         "generated_at":datetime.datetime.now().isoformat(timespec="seconds"),
         "fuzzy_threshold":args.fuzzy,
         "objects":{}}
    counts={"matched":0,"ambiguous":0,"missing":0,"to_create":0}
    field_counts={"matched":0,"ambiguous":0,"missing":0,"to_create":0}

    for obj in sorted(wanted):
        om=match_one(obj, real_objs, obj_aliases, args.fuzzy)
        # our own custom objects are ours to CREATE, not reconcile — absence is not an error
        if kinds.get(obj)=="custom" and om["status"] in ("missing","ambiguous"):
            om={"status":"to_create","resolved":obj,"method":"create","candidates":[]}
        counts[om["status"]]=counts.get(om["status"],0)+1
        entry={**om, "kind":kinds.get(obj,"standard"), "fields":{}}
        real_fields=org.get(om["resolved"],[]) if om["resolved"] else []
        for fld in sorted(wanted[obj]):
            fm=match_one(fld, real_fields, {fld: fld_aliases.get(f"{obj}.{fld}",[])}, args.fuzzy) if real_fields \
               else dict(status="missing",resolved=None,method="none",candidates=[])
            if fld.endswith("__c") and fm["status"]!="matched":
                # a custom field WE create — absence is not an error
                fm={"status":"to_create","resolved":fld,"method":"create","candidates":[]}
            field_counts[fm["status"]]=field_counts.get(fm["status"],0)+1
            entry["fields"][fld]=fm
        out["objects"][obj]=entry

    blocking=[o for o,e in out["objects"].items() if e["status"] in ("ambiguous","missing")]
    out["summary"]={"objects":counts,"fields":field_counts,
                    "build_gate":"PASS" if not blocking else "BLOCKED",
                    "blocking_objects":blocking}

    with open(args.out,"w") as f:
        yaml.safe_dump(out,f,sort_keys=False,default_flow_style=False)

    print(f"objects: {counts}")
    print(f"fields : {field_counts}")
    print(f"build gate: {out['summary']['build_gate']}")
    if blocking:
        print("BLOCKED — resolve these before build (add to aliases.yaml or decide create-custom):")
        for o in blocking:
            e=out["objects"][o]
            print(f"  - {o}: {e['status']} candidates={e['candidates']}")
    print("wrote",args.out)
    sys.exit(0 if not blocking else 2)

if __name__=="__main__":
    main()
