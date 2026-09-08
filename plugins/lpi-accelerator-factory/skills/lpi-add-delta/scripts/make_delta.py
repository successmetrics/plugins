#!/usr/bin/env python3
"""
make_delta.py — emit a SCOPED, ADDITIVE package.xml for a single delta to an existing engagement,
and append a row to the engagement's delta-log. Does NOT touch modules.yaml, seeds, or the base.

Usage:
  python3 make_delta.py --engagement <path> --slug analytics \
      --add Report:LPI_Analytics_Standard \
      --add Dashboard:LPI_Analytics_Standard/LPI_Analytics_Overview \
      --add ReportType:LPI_Cases --add PermissionSet:LPI_Analytics_Standard

Writes:
  <engagement>/package/delta-<NN>-<slug>.xml   (NN auto-increments)
  appends to <engagement>/docs/delta-log.md
"""
import argparse, os, re, sys, datetime

API = "63.0"
# stable package.xml type ordering (deps before dependents)
ORDER = ["CustomObject", "CustomField", "RecordType", "CustomTab", "CustomApplication",
         "QuickAction", "ListView", "FlexiPage", "CustomPermission", "PermissionSet",
         "LightningComponentBundle", "ApexClass", "Flow", "CustomMetadata",
         "ReportType", "Report", "Dashboard"]


def next_seq(pkg_dir):
    n = 0
    if os.path.isdir(pkg_dir):
        for f in os.listdir(pkg_dir):
            m = re.match(r"delta-(\d+)-", f)
            if m:
                n = max(n, int(m.group(1)))
    return n + 1


def build_xml(buckets):
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<Package xmlns="http://soap.sforce.com/2006/04/metadata">']
    known = [t for t in ORDER if t in buckets]
    extra = sorted(t for t in buckets if t not in ORDER)
    for typ in known + extra:
        out.append("    <types>")
        for mem in sorted(buckets[typ]):
            out.append(f"        <members>{mem}</members>")
        out.append(f"        <name>{typ}</name>")
        out.append("    </types>")
    out.append(f"    <version>{API}</version>")
    out.append("</Package>")
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--engagement", required=True, help="path to the engagement root")
    ap.add_argument("--slug", required=True, help="short delta name, e.g. analytics")
    ap.add_argument("--add", action="append", default=[], metavar="Type:Member",
                    help="repeatable; e.g. Report:LPI_Analytics_Standard/SA_Fees_Outstanding")
    ap.add_argument("--note", default="", help="optional one-line note for the delta-log")
    a = ap.parse_args()

    eng = os.path.abspath(a.engagement)
    if not os.path.isdir(eng):
        sys.exit(f"engagement not found: {eng}")
    if not a.add:
        sys.exit("nothing to add — pass at least one --add Type:Member")

    buckets = {}
    for item in a.add:
        if ":" not in item:
            sys.exit(f"bad --add '{item}', expected Type:Member")
        typ, mem = item.split(":", 1)
        buckets.setdefault(typ.strip(), set()).add(mem.strip())

    pkg_dir = os.path.join(eng, "package")
    docs_dir = os.path.join(eng, "docs")
    os.makedirs(pkg_dir, exist_ok=True)
    os.makedirs(docs_dir, exist_ok=True)

    seq = next_seq(pkg_dir)
    fname = f"delta-{seq:02d}-{a.slug}.xml"
    fpath = os.path.join(pkg_dir, fname)
    with open(fpath, "w") as fh:
        fh.write(build_xml(buckets))

    # delta-log
    log = os.path.join(docs_dir, "delta-log.md")
    if not os.path.exists(log):
        with open(log, "w") as fh:
            fh.write("# Delta Log\n\n"
                     "Post-generation additions to this engagement (see docs/27_Delta_Management.md).\n"
                     "Each row = one additive deploy. NEVER regenerate to add a delta.\n\n"
                     "| # | Date | Slug | Manifest | Components | Note |\n"
                     "|---|------|------|----------|-----------|------|\n")
    comps = "; ".join(f"{t}:{','.join(sorted(m))}" for t, m in sorted(buckets.items()))
    today = datetime.date.today().isoformat()
    with open(log, "a") as fh:
        fh.write(f"| {seq:02d} | {today} | {a.slug} | package/{fname} | {comps} | {a.note} |\n")

    print(f"wrote {fpath}")
    print(f"logged to {log}")
    print("\nDeploy additively (never engagement_deploy.sh):")
    print(f"  ( cd {a.engagement}/ext && sf project deploy start -x ../package/{fname} "
          f"--target-org <org> --ignore-conflicts )")


if __name__ == "__main__":
    main()
