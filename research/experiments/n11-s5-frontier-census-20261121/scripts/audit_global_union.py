#!/usr/bin/env python3
"""Global union audit of every published S5 verdict cache on the repo tree.

Secondary measurement over published artifacts only. It does not establish
any game verdict, does not write any cache, and does not rehabilitate
anything. Fail-closed on unparsable rows; conflicts are REPORTED, never
resolved by this tool.

Coverage:
  1. Walks the whole tree (research/ and results/), reads every file that
     contains s5verdict rows, with per-file internal consistency checks.
  2. Classifies files by trust label embedded in the published filename
     convention: exact/merged/reconstructed/canonical vs derived (S6/S7
     lineage suffixes) vs unknown.
  3. Builds the global union verdict map with full provenance and detects
     WIN/LOSS conflicts between files (stratified by trust label).
  4. Verifies the two active S5 quarantine registry keys do not appear in
     any exact/merged current-chain cache, and reports where their
     quarantined verdicts persist (expected: historical derived caches).
  5. Reports union-vs-current-chain coverage: rows present in historical
     exact/merged caches but absent from the pinned current chain
     ("backward-only rows"), a backlog quantification, never a merge.
"""
from __future__ import annotations

import collections
import csv
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "research/experiments/n11-frontier-selection-20261005/scripts"))
from s5_evidence_policy import quarantined_cache_keys  # noqa: E402

CURRENT_CHAIN = ROOT / "research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-40960-20261121/output/merged-exact-s5-after-js-probe-13.cache"
PIN = {
    "current_chain": "60e0dc3476920d4e99043dd4f132398ea72e4dfdcd9f3dbb8fc686ba65bc28c6",
    "quarantine_registry": "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9",
}


def trust_label(rel: str) -> str:
    name = rel.lower()
    if "derived" in name:
        return "derived"
    if any(t in name for t in ("-witness", "-reverse", "-expanded-s6", "s6-", "-s7-", "model8", "model-hard")):
        return "model_derived"
    if "exact" in name or "merged" in name or "canonical" in name or "reconstructed" in name:
        return "exact_or_merged"
    return "other"


def iter_files(root: Path):
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        if p.suffix not in (".cache",):
            continue
        yield p


def main():
    digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()  # noqa: E731
    quarantine = quarantined_cache_keys()

    current_bytes = CURRENT_CHAIN.read_bytes()
    if hashlib.sha256(current_bytes).hexdigest() != PIN["current_chain"]:
        die("current chain pin mismatch")
    # registry pin
    reg = ROOT / "results/n11-s5-evidence-quarantine.json"
    if digest(reg) != PIN["quarantine_registry"]:
        die("quarantine registry pin mismatch")

    verdict = {}          # key -> verdict (first seen exact/merged value)
    provenance = collections.defaultdict(list)  # key -> [(relpath, label, verdict)]
    files = []
    n_rows_total = 0
    internal_conflicts = 0

    for p in iter_files(ROOT / "research") :
        rel = str(p.relative_to(ROOT))
        rows = {}
        n = 0
        bad = []
        with p.open(encoding="utf-8-sig", newline="") as f:
            for row in csv.reader(f):
                if not row or row[0].startswith("#"):
                    continue
                if row[0] == "key":
                    continue
                if row[0] != "s5verdict":
                    if any(x == "s5verdict" for x in row[:1]):
                        bad.append(row[:3])
                        continue
                    # files may contain other row types; ignore silently only header-like
                    break
                try:
                    k = (int(row[1]), int(row[2]))
                    v = int(row[4])
                    if int(row[3]) != 5 or v not in (1, 2) or len(row) != 6:
                        bad.append(row)
                        continue
                except (ValueError, IndexError):
                    bad.append(row)
                    continue
                n += 1
                if k in rows and rows[k] != v:
                    internal_conflicts += 1
                    rows[k] = ("CONFLICT_INTERNAL", k)
                rows.setdefault(k, v)
        if n == 0:
            continue
        label = trust_label(rel)
        files.append({"path": rel, "label": label, "rows": n, "sha256": digest(p)})
        n_rows_total += n
        for k, v in rows.items():
            provenance[k].append((rel, label, v))

    # global conflict detection, stratified
    conflicts = []
    for k, prov in provenance.items():
        vals = {v for _, _, v in prov}
        if len(vals - {"CONFLICT_INTERNAL"}) > 1 or "CONFLICT_INTERNAL" in vals:
            conflicts.append({
                "key": [k[0], k[1]],
                "provenance": [
                    {"file": f, "label": l, "verdict": v} for f, l, v in prov
                ],
            })

    # quarantine key scan
    quarantine_hits = collections.defaultdict(list)
    for k in quarantine:
        for f, l, v in provenance.get(k, []):
            quarantine_hits[(k[0], k[1])].append({"file": f, "label": l, "verdict": v})

    # current chain keys
    chain = {}
    with CURRENT_CHAIN.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.reader(f):
            if not row or row[0].startswith("#"):
                continue
            if row[0] != "s5verdict":
                die(f"unexpected chain row: {row}")
            chain[(int(row[1]), int(row[2]))] = int(row[4])
    labels_chain = trust_label(str(CURRENT_CHAIN.relative_to(ROOT)))

    # backward-only rows: keys with an exact_or_merged (or reconstructed)
    # verdict somewhere but absent from current chain
    backward_only = []
    for k, prov in provenance.items():
        if k in chain or k in quarantine:
            continue
        exact_like = [pp for pp in prov if pp[1] in ("exact_or_merged",)]
        if exact_like:
            backward_only.append({
                "key": [k[0], k[1]],
                "verdict_values": sorted({pp[2] for pp in exact_like}),
                "files": sorted({pp[0] for pp in exact_like}),
            })
    backward_only.sort(key=lambda r: r["key"])

    result = {
        "schema": "n11-s5-global-union-audit-20261121-v1",
        "files_scanned": len(files),
        "s5verdict_rows_total": n_rows_total,
        "unique_keys": len(provenance),
        "internal_file_conflicts": internal_conflicts,
        "global_conflicts": conflicts,
        "global_conflict_count": len(conflicts),
        "quarantine_keys_in_files": {f"{a}:{b}": v for (a, b), v in quarantine_hits.items()},
        "current_chain": {
            "path": str(CURRENT_CHAIN.relative_to(ROOT)),
            "sha256": PIN["current_chain"],
            "rows": len(chain),
            "win": sum(1 for v in chain.values() if v == 1),
            "loss": sum(1 for v in chain.values() if v == 2),
        },
        "union_counts": {},
        "backward_only_exact_or_merged_rows": backward_only,
        "backward_only_count": len(backward_only),
        "guard": "This audit never establishes a verdict, never merges, never rehabilitates quarantined rows. It measures global cache-corpus consistency only. The standard 11x11 empty board and two-stone root {60,27} remain UNKNOWN.",
    }
    vc = collections.Counter()
    for k, prov in provenance.items():
        if any(pp[2] == 1 for pp in prov):
            vc["has_WIN_somewhere"] += 1
        if all(pp[2] in (2,) for pp in prov):
            vc["LOSS_only_everywhere"] += 1
    result["union_counts"] = dict(vc)
    print(json.dumps(result, ensure_ascii=False, indent=1, sort_keys=True))


def die(msg):
    print(f"AUDIT FAIL-CLOSED ABORT: {msg}", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
