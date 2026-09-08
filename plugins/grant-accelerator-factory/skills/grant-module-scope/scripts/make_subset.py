#!/usr/bin/env python3
"""
Emit a tailored package.xml (and a deploy plan) containing ONLY the modules a
client enabled in modules.yaml. Resolves module dependencies automatically.

Usage:
  python3 make_subset.py [--modules modules.yaml] [--out subset-package.xml]
  python3 make_subset.py --enable core,permitting,inspections,portal
"""
import argparse, sys
try:
    import yaml
except ImportError:
    sys.exit("pip install pyyaml")

API="62.0"

def resolve(enabled, mods):
    seen=set()
    def add(m):
        if m in seen: return
        seen.add(m)
        for dep in mods[m].get("depends_on",[]) or []:
            add(dep)
    for m in enabled: add(m)
    # always-on modules
    for m,v in mods.items():
        if v.get("always"): add(m)
    return seen

def collect(enabled, mods):
    buckets={"CustomObject":set(),"CustomField":set(),"RecordType":set(),"CustomTab":set(),
             "PermissionSet":set(),"CustomApplication":set(),"CustomPermission":set(),
             "LightningComponentBundle":set(),"ApexClass":set(),"LightningMessageChannel":set()}
    manual=[]
    for m in sorted(enabled):
        d=mods[m]
        for o in d.get("objects",[]): buckets["CustomObject"].add(o)
        for rt in d.get("record_types",[]): buckets["RecordType"].add(rt)
        for t in d.get("tabs",[]): buckets["CustomTab"].add(t)
        for ps in d.get("permission_sets",[]): buckets["PermissionSet"].add(ps)
        for a in d.get("apps",[]): buckets["CustomApplication"].add(a)
        for cp in d.get("custom_permissions",[]): buckets["CustomPermission"].add(cp)
        for c in d.get("components",[]): buckets["LightningComponentBundle"].add(c)
        for c in d.get("apex",[]): buckets["ApexClass"].add(c)
        for mc in d.get("message_channels",[]): buckets["LightningMessageChannel"].add(mc)
        if d.get("manual_steps"):
            manual.append((m, d.get("experience_site")))
    return buckets, manual

def package_xml(buckets):
    out=['<?xml version="1.0" encoding="UTF-8"?>',
         '<Package xmlns="http://soap.sforce.com/2006/04/metadata">']
    for name in ["CustomObject","CustomField","RecordType","CustomTab","CustomApplication",
                 "CustomPermission","PermissionSet","LightningComponentBundle","ApexClass",
                 "LightningMessageChannel"]:
        members=sorted(buckets[name])
        if not members: continue
        out.append("    <types>")
        for mem in members: out.append(f"        <members>{mem}</members>")
        out.append(f"        <name>{name}</name>")
        out.append("    </types>")
    out.append(f"    <version>{API}</version>")
    out.append("</Package>")
    return "\n".join(out)+"\n"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--modules",default="modules.yaml")
    ap.add_argument("--enable",default=None,help="comma list to override modules.yaml 'enabled'")
    ap.add_argument("--out",default="subset-package.xml")
    a=ap.parse_args()
    doc=yaml.safe_load(open(a.modules))
    mods=doc["modules"]
    enabled=a.enable.split(",") if a.enable else doc.get("enabled",[])
    enabled=[e.strip() for e in enabled]
    for m in enabled:
        if m not in mods: sys.exit(f"unknown module '{m}'")
    full=resolve(enabled, mods)
    buckets, manual=collect(full, mods)
    open(a.out,"w").write(package_xml(buckets))
    print("enabled (with deps):", ", ".join(sorted(full)))
    print("package types:")
    for k,v in buckets.items():
        if v: print(f"  {k}: {len(v)} -> {', '.join(sorted(v))}")
    if manual:
        print("\nMANUAL STEPS REQUIRED (see docs/03_Org_Setup_Runbook.md and docs/06_Experience_Cloud_Grantee_Portal_Runbook.md):")
        for m,site in manual:
            note=f"Experience site '{site}' is not a clean CLI deploy" if site else "has Setup-toggle/manual steps (see modules.yaml manual_steps)"
            print(f"  - module '{m}': {note}")
    print("\nwrote",a.out)

if __name__=="__main__":
    main()
