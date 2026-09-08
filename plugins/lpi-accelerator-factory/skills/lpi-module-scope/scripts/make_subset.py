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

# yaml key on a module  ->  metadata type in package.xml
KEYS=[
    ("objects","CustomObject"),
    ("record_types","RecordType"),
    ("tabs","CustomTab"),
    ("permission_sets","PermissionSet"),
    ("apps","CustomApplication"),
    ("custom_permissions","CustomPermission"),
    ("quick_actions","QuickAction"),
    ("list_views","ListView"),
    ("flexipages","FlexiPage"),
    ("components","LightningComponentBundle"),
    ("apex","ApexClass"),
    ("message_channels","LightningMessageChannel"),
    ("named_credentials","NamedCredential"),
    ("custom_metadata_records","CustomMetadata"),
    ("briefcases","BriefcaseDefinition"),
    ("report_types","ReportType"),
    ("reports","Report"),          # include the folder itself as a member (e.g. LPI_Reports)
    ("dashboards","Dashboard"),    # include the folder itself as a member (e.g. LPI_Dashboards)
]
# order types are written to package.xml
ORDER=["CustomObject","CustomField","RecordType","CustomTab","CustomApplication",
       "QuickAction","ListView","FlexiPage","CustomPermission","PermissionSet",
       "LightningComponentBundle","ApexClass","LightningMessageChannel","NamedCredential","CustomMetadata",
       "BriefcaseDefinition","ReportType","Report","Dashboard"]

def resolve(enabled, mods):
    seen=set()
    def add(m):
        if m in seen: return
        seen.add(m)
        for dep in mods[m].get("depends_on",[]) or []:
            add(dep)
    for m in enabled: add(m)
    for m,v in mods.items():
        if v.get("always"): add(m)
    return seen

def collect(enabled, mods):
    buckets={t:set() for _,t in KEYS}
    buckets["CustomField"]=set()
    manual=[]
    for m in sorted(enabled):
        d=mods[m]
        for key,typ in KEYS:
            for member in d.get(key,[]) or []:
                buckets[typ].add(member)
        if d.get("manual_steps"):
            manual.append((m, d.get("experience_site")))
    return buckets, manual

def package_xml(buckets):
    out=['<?xml version="1.0" encoding="UTF-8"?>',
         '<Package xmlns="http://soap.sforce.com/2006/04/metadata">']
    for name in ORDER:
        members=sorted(buckets.get(name,set()))
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
    for k in ORDER:
        v=buckets.get(k,set())
        if v: print(f"  {k}: {len(v)} -> {', '.join(sorted(v))}")
    if manual:
        print("\nMANUAL STEPS REQUIRED (see 04_Experience_Cloud_and_Deployment_Runbook.md):")
        for m,site in manual: print(f"  - module '{m}': Experience site '{site}' is not a clean CLI deploy")
    print("\nwrote",a.out)

if __name__=="__main__":
    main()
