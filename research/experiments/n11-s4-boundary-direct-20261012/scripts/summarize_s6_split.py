#!/usr/bin/env python3
"""Recheck all audited S6 batches and summarize the complete 98-child frontier."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = ROOT / "research/experiments/n11-s4-boundary-direct-20261012"
S5 = (1152921504607899649, 536870912)


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def resolve(path: str) -> Path:
    p = Path(path)
    return p if p.is_absolute() else ROOT / p


def replay(path: Path) -> dict:
    rows = []
    with path.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.reader(f):
            if row and row[0] == "replay":
                rows.append(row)
    if len(rows) != 1 or len(rows[0]) != 11:
        raise ValueError(f"expected one raw replay row: {path}")
    r = rows[0]
    return {"sequence": int(r[1]), "stones": int(r[2]), "legal": int(r[3]),
            "is_or": int(r[4]), "budget": int(r[5]), "verdict": int(r[6]),
            "nodes": int(r[7]), "key": [int(r[9]), int(r[10])]}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--audit", type=Path, action="append", required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
    from independent import Board
    board = Board(11)
    parent = S5[0] | (S5[1] << 64)
    children = {}
    for mask in board.children(parent):
        key = (mask & ((1 << 64) - 1), mask >> 64)
        children[key] = board.legal(mask).bit_count()
    if len(children) != 98:
        raise ValueError(f"expected complete independent 98-child boundary, got {len(children)}")

    statuses: dict[tuple[int, int], int] = {}
    receipts = []
    for audit_arg in args.audit:
        path = audit_arg if audit_arg.is_absolute() else ROOT / audit_arg
        audit = json.loads(path.read_text(encoding="utf-8"))
        selection_path = resolve(audit["selection_path"])
        run_path = resolve(audit["run_manifest_path"])
        if sha(selection_path) != audit["selection_sha256"] or sha(run_path) != audit["run_manifest_sha256"]:
            raise ValueError(f"selection/run manifest changed after audit: {path}")
        if audit["parent_s5"] != list(S5) or audit["independently_generated_s6_children"] != 98:
            raise ValueError(f"audit receipt targets a different parent/boundary: {path}")
        selection = json.loads(selection_path.read_text(encoding="utf-8"))
        run = json.loads(run_path.read_text(encoding="utf-8"))
        selected = {int(x["sequence"]): x for x in selection["selected"]}
        records = {int(x["sequence"]): x for x in run["runs"]}
        if run.get("selection_sha256") != sha(selection_path) or set(records) != set(selected):
            raise ValueError(f"audit/run selected sequence mismatch: {path}")
        for result in audit["new_s6_results"]:
            seq = int(result["sequence"])
            target, record = selected[seq], records[seq]
            key = tuple(result["key"])
            raw, log = resolve(result["raw_path"]), resolve(result["log_path"])
            if key in statuses or key not in children or children[key] != result["legal"]:
                raise ValueError(f"duplicate/out-of-boundary S6 result: {key}")
            if sha(raw) != result["raw_sha256"] or sha(log) != result["log_sha256"]:
                raise ValueError(f"S6 raw/log SHA mismatch: {key}")
            parsed = replay(raw)
            code = {"UNKNOWN": 0, "WIN": 1, "LOSS": 2}[result["verdict"]]
            if (parsed["key"] != list(key) or parsed["stones"] != 6 or parsed["is_or"] != 1
                    or parsed["legal"] != children[key] or parsed["budget"] != result["budget"]
                    or parsed["verdict"] != code or parsed["nodes"] != result["nodes"]
                    or record["raw_sha256"] != result["raw_sha256"]):
                raise ValueError(f"S6 raw recheck mismatch: {key}")
            statuses[key] = code
        receipts.append({"path": str(path.relative_to(ROOT)), "sha256": sha(path),
                         "fresh_rows": len(audit["new_s6_results"])})

    history_path = ROOT / "research/experiments/n11-strategy-redesign-20261010/output/history.json"
    history = json.loads(history_path.read_text(encoding="utf-8"))
    saved = {}
    for row in history:
        key = tuple(row["key"])
        if row["stones"] == 6 and key in children and row["verdict"] in (1, 2):
            saved[key] = row["verdict"]
    if set(statuses) != set(children) - set(saved):
        raise ValueError(f"first-pass rows do not partition boundary: saved={len(saved)} raw={len(statuses)}")
    if any(k in statuses and v in (1, 2) and statuses[k] in (1, 2) and statuses[k] != v for k, v in saved.items()):
        raise ValueError("saved and fresh S6 exact outcomes conflict")
    all_status = dict(saved)
    all_status.update({k: v for k, v in statuses.items() if v in (1, 2)})
    counts = Counter(all_status.values())
    unknown_keys = [list(k) for k in sorted(children) if k not in all_status]
    first_pass = [json.loads((ROOT / r["path"]).read_text(encoding="utf-8")) for r in receipts]
    total_nodes = sum(sum(int(x["nodes"]) for x in r["new_s6_results"]) for r in first_pass)
    total_seconds = sum(float(r["new_s6_elapsed_seconds"]) for r in first_pass)
    output = args.output if args.output.is_absolute() else ROOT / args.output
    doc = {
        "schema": "n11-s4-final-s5-s6-first-pass-summary-v1",
        "parent_s5": list(S5), "parent_s5_polarity": "AND (is_or=0)",
        "independent_boundary_children": len(children), "fresh_1m_attempts": len(statuses),
        "fresh_1m_verdict_counts": {"WIN": sum(v == 1 for v in statuses.values()),
                                    "LOSS": sum(v == 2 for v in statuses.values()),
                                    "UNKNOWN": sum(v == 0 for v in statuses.values())},
        "saved_exact_counts": {"WIN": sum(v == 1 for v in saved.values()), "LOSS": sum(v == 2 for v in saved.values())},
        "combined_exact_counts": {"WIN": counts[1], "LOSS": counts[2], "UNKNOWN": len(unknown_keys)},
        "combined_unknown_keys": unknown_keys, "fresh_nodes": total_nodes,
        "fresh_elapsed_seconds": total_seconds, "budget_per_fresh_root": 1_000_000,
        "selection_rule": "twelve 8-child legal-count-stratified batches; one cold profile-off exact solver process per S6 child; saved exact S6 reused",
        "independent_checks": "all 98 canonical S6 children regenerated; every fresh raw row rechecked for key/stones/legal/is_or=1/budget/verdict/nodes and raw/log SHA",
        "trust": "S6 exact leaves are solver-trusted; geometry and parent AND propagation are independently checked; not terminal-only minimax proof",
        "audit_receipts": receipts,
        "history_sha256": sha(history_path),
    }
    encoded = (json.dumps(doc, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and output.read_bytes() != encoded:
        raise ValueError("existing first-pass summary differs; refusing overwrite")
    if not output.exists():
        output.write_bytes(encoded)
    print(json.dumps({k: v for k, v in doc.items() if k not in ("audit_receipts", "combined_unknown_keys")},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
