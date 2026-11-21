#!/usr/bin/env python3
"""Build manifest.json (path, bytes, md5) for all experiment files."""
import hashlib, json, os, sys

exp = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EXCLUDE = {"manifest.json", "session-log.md", "seeds/witness_5x25_c0.json", "declaration-note.md", "followup-declaration.md"}
files = []
total_leaves = 162581176
runs = 34
buf = []
for root, dirs, fns in os.walk(exp):
    dirs[:] = [d for d in dirs if d != "__pycache__"]
    for fn in sorted(fns):
        p = os.path.join(root, fn)
        rel = os.path.relpath(p, exp).replace(os.sep, "/")
        if rel in EXCLUDE:
            continue
        with open(p, "rb") as f:
            b = f.read()
        files.append({"path": rel, "bytes": len(b), "md5": hashlib.md5(b).hexdigest()})

files.sort(key=lambda x: x["path"])
recs = [json.loads(l) for l in open(os.path.join(exp, "output/records.jsonl"))]
uniq = [r for r in recs if not r["double"]]
tot = sum(r["nRmLeaves"] for r in uniq)
manifest = {
    "experiment": "five-row-q6-m21-species-m25-5x23-5x27-sd6-surgery-20261121",
    "date": "2026-11-21",
    "pinned_upstream": {
        "surgery4.js": "7dc40fc0f08150692d64241d0c6c4029",
        "sat.js": "0cc6021a4e523a0d7f4d5ea0f5f5d40c",
        "census4_check.js": "dadbeae1b02ad2a9650c6ce86021fb9c",
        "source": "research/experiments/five-row-q6-q5-m23-m27-sd6-surgery-20261121/scripts/ (parent experiment, md5-verified identical)",
    },
    "declaration": "research/log/2026-11-21-five-row-q6-m21-species-m25-5x23-5x27-sd6-surgery-single-owner-note.md (commit 5c4cfca9)",
    "grid_correction": "declaration said 3 classes for 5x23 (span-21); actual m21-species bbox span is 18 -> complete grid is 6 classes per species; the experiment ran the complete 6-class grid (superset)",
    "totals": {
        "unique_config_runs": len(uniq),
        "records_including_doubles": len(recs),
        "nRmLeaves": tot,
        "q6_nRmLeaves": sum(r["nRmLeaves"] for r in uniq if r["campaign"] == "5x23q6-species"),
        "q5_nRmLeaves": sum(r["nRmLeaves"] for r in uniq if r["campaign"] == "5x27q5-species"),
        "nWitness": sum(r["nWitness"] for r in uniq),
        "nMaximal": sum(r["nMaximal"] for r in uniq),
        "cross_class_consistent": "2/2 (m21_m21 t=0, m25 t=0)",
    },
    "files": files,
}
with open(os.path.join(exp, "manifest.json"), "w") as f:
    json.dump(manifest, f, indent=1, sort_keys=False)
    f.write("\n")
print("manifest:", len(files), "files; totals:", json.dumps(manifest["totals"]))
assert manifest["totals"]["nRmLeaves"] == total_leaves, "leaf total mismatch"
assert len(recs) == runs, "record count mismatch"
print("OK")
