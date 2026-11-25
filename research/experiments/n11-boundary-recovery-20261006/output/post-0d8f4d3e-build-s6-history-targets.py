#!/usr/bin/env python3
"""Materialize one-row CSVs for the current unresolved s5 parents."""
from __future__ import annotations
import csv, hashlib, json
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
BASE = "post-0d8f4d3e-active-class-10448351135499550722-0"
TARGETS = OUT / "post-0d8f4d3e-dual-tight-ranking-targets.csv"
BOUNDARY = OUT / f"{BASE}-class-boundary-audit.json"
CACHE = OUT / f"{BASE}-merged-s5.cache"
S6_SUMMARY = OUT / f"{BASE}-saved-s6-summary.json"
S6_FULL = OUT / f"{BASE}-saved-s6-full.json.gz"
S6_SOURCE_AUDIT = OUT / "post-1001d051-reconciliation-20261009-augmented-s6-source-audit.json"
TARGET_DIR = OUT / f"{BASE}-s6-history-parent-targets"
MANIFEST = OUT / f"{BASE}-s6-history-targets-manifest.json"

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> None:
    if TARGET_DIR.exists() or MANIFEST.exists():
        raise SystemExit("refusing to overwrite S6 history target inputs")
    rows = [r for r in csv.reader(TARGETS.open(newline="", encoding="utf-8-sig"))
            if r and not r[0].lstrip().startswith("#")]
    boundary = json.loads(BOUNDARY.read_text(encoding="utf-8"))["boundary"]
    children = {tuple(x["key"]): x["verdict"] for x in boundary["children"]}
    keys = [(int(r[3]), int(r[4])) for r in rows]
    if len(keys) != 11 or len(set(keys)) != len(keys):
        raise SystemExit(f"expected 11 unique ranked UNKNOWN s5 targets, got {len(keys)}")
    if any(len(r) != 11 or int(r[2]) != 5 or int(r[6]) != 0 or int(r[7]) != 0 for r in rows):
        raise SystemExit("target input has an invalid s5 AND row")
    if any(children.get(k, "missing") is not None for k in keys):
        raise SystemExit("target list does not exactly consist of UNKNOWN children from audited class boundary")
    TARGET_DIR.mkdir()
    outputs = []
    for row in rows:
        key = (int(row[3]), int(row[4]))
        path = TARGET_DIR / f"s5-{key[0]}-{key[1]}.csv"
        with path.open("w", newline="", encoding="utf-8") as stream:
            stream.write("# current canonical UNKNOWN s5 parent; generated for S6 boundary audit\n")
            csv.writer(stream, lineterminator="\n").writerow(row)
        outputs.append({"path": path.relative_to(ROOT).as_posix(),
                        "sha256": sha(path), "bytes": path.stat().st_size, "key": list(key)})
    sources = [TARGETS, BOUNDARY, CACHE, S6_SUMMARY, S6_FULL, S6_SOURCE_AUDIT, Path(__file__).resolve()]
    doc = {
        "schema": "n11-reply27-current-s6-history-targets-v1",
        "class_key": [10448351135499550722, 0],
        "canonical_s5_unknown_targets": len(keys),
        "sources": [{"path": p.relative_to(ROOT).as_posix(),
                     "sha256": sha(p), "bytes": p.stat().st_size} for p in sources],
        "targets": outputs,
        "claim": "One-row audit inputs reproduce the exact currently UNKNOWN s5 parent set; no outcome is inferred.",
    }
    MANIFEST.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"targets": len(outputs), "manifest": MANIFEST.name,
                      "manifest_sha256": sha(MANIFEST)}, sort_keys=True))

if __name__ == "__main__":
    main()
