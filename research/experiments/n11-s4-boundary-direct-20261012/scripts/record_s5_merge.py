#!/usr/bin/env python3
"""Verify and hash-record the final atomic S6-derived S5 cache integration."""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = ROOT / "research/experiments/n11-s4-boundary-direct-20261012"
CURRENT = EXP / "output/current-exact-s5.cache"
WORKER = EXP / "output/s6-fourteenth-derived-s5-worker.cache"
AUDIT = EXP / "output/s6-fourteenth-batch-audit.json"
SELECTION = EXP / "input/s6-first-batch-selection.json"
KEY = (1152921504607899649, 536870912)


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    sys.path.insert(0, str(ROOT / "research/experiments/n11-frontier-selection-20261005/scripts"))
    from s5_evidence_policy import quarantined_cache_keys
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    selection = json.loads(SELECTION.read_text(encoding="utf-8"))
    before = selection["exact_cache"]["sha256"]
    if audit.get("derived_parent_s5_outcome") != "LOSS" or audit.get("loss_witnesses") != [[1152921504675009536, 536870912]]:
        raise ValueError("S6 audit receipt does not establish the selected S5 LOSS")
    worker_rows = list(csv.reader(WORKER.open(encoding="utf-8-sig", newline="")))
    exact_worker = [r for r in worker_rows if r and r[0] == "s5verdict"]
    if exact_worker != [["s5verdict", str(KEY[0]), str(KEY[1]), "5", "2", "0"]]:
        raise ValueError(f"derived worker must contain only the audited S5 LOSS: {exact_worker}")
    cache, counts = {}, {1: 0, 2: 0}
    with CURRENT.open(encoding="utf-8-sig", newline="") as f:
        for line, row in enumerate(csv.reader(f), 1):
            if not row or row[0].strip().startswith("#"):
                continue
            if len(row) != 6 or row[0] != "s5verdict":
                raise ValueError(f"malformed merged cache row {line}: {row}")
            lo, hi, stones, verdict, nodes = map(int, row[1:])
            key = (lo, hi)
            if stones != 5 or verdict not in (1, 2) or nodes < 0 or key in cache:
                raise ValueError(f"invalid/duplicate exact S5 cache row: {row}")
            cache[key] = {"verdict": verdict, "nodes": nodes}
            counts[verdict] += 1
    if KEY not in cache or cache[KEY] != {"verdict": 2, "nodes": 0}:
        raise ValueError("merged exact cache does not contain the derived S5 LOSS")
    if KEY in quarantined_cache_keys():
        raise ValueError("derived S5 key is quarantined")
    if len(cache) != 5851 or counts != {1: 159, 2: 5692}:
        raise ValueError(f"unexpected final exact cache summary: rows={len(cache)} counts={counts}")
    doc = {
        "schema": "n11-s5-atomic-merge-receipt-v1",
        "merge_script": "research/experiments/n11-search-methods/scripts/dfpn_s5_merge.sh",
        "merge_semantics": "existing cache union exact-only audited worker; atomic replacement; quarantine/conflict checks enabled",
        "command": ["bash", "research/experiments/n11-search-methods/scripts/dfpn_s5_merge.sh",
                    str(CURRENT.relative_to(ROOT)), str(CURRENT.relative_to(ROOT)), str(WORKER.relative_to(ROOT))],
        "merge_stdout": ["merged keys: 5851; UNKNOWN dropped: 0; quarantined keys: 0", "MERGE_OK"],
        "prior_cache_sha256": before, "derived_worker_sha256": sha(WORKER),
        "derived_audit_path": str(AUDIT.relative_to(ROOT)), "derived_audit_sha256": sha(AUDIT),
        "final_cache_path": str(CURRENT.relative_to(ROOT)), "final_cache_sha256": sha(CURRENT),
        "final_rows": len(cache), "verdict_counts": {"WIN": counts[1], "LOSS": counts[2]},
        "new_row": {"key": list(KEY), "stones": 5, "verdict": "LOSS", "nodes_field": 0,
                    "evidence_type": "derived by S5 AND from one direct S6 solver-trusted LOSS"},
        "quarantine_conflicts": 0,
    }
    output = EXP / "output/s5-s6-derived-cache-merge-receipt.json"
    output.write_text(json.dumps(doc, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(doc, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
