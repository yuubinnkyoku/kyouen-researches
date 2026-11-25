#!/usr/bin/env python3
"""Aggregate the 1M first pass and 15M escalation without treating UNKNOWN as exact."""
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
HISTORY = ROOT / "research/experiments/n11-strategy-redesign-20261010/output/history.json"
S5 = (1152921504607899649, 536870912)


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def resolve(value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def parse_raw(path: Path) -> dict:
    rows = []
    with path.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.reader(f):
            if row and row[0] == "replay":
                rows.append(row)
    if len(rows) != 1 or len(rows[0]) != 11:
        raise ValueError(f"expected one complete replay row: {path}")
    row = rows[0]
    return {"key": [int(row[9]), int(row[10])], "stones": int(row[2]), "legal": int(row[3]),
            "is_or": int(row[4]), "budget": int(row[5]), "verdict": int(row[6]), "nodes": int(row[7])}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--first-pass-summary", type=Path, required=True)
    ap.add_argument("--audit", type=Path, action="append", required=True,
                    help="15M escalation audit receipt; repeat for each stopped/complete batch")
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    first_path = resolve(args.first_pass_summary)
    first = json.loads(first_path.read_text(encoding="utf-8"))
    if first.get("schema") != "n11-s4-final-s5-s6-first-pass-summary-v1":
        raise ValueError("unexpected 1M first-pass summary schema")
    if first.get("fresh_1m_attempts") != 96 or first.get("combined_exact_counts") != {"WIN": 79, "LOSS": 0, "UNKNOWN": 19}:
        raise ValueError("unexpected first-pass classification; inspect before escalation")
    first_unknown = {tuple(key) for key in first["combined_unknown_keys"]}
    if len(first_unknown) != 19:
        raise ValueError("first-pass UNKNOWN key list mismatch")
    first_exact: dict[tuple[int, int], int] = {}
    first_budget_nodes = Counter()
    for item in first["audit_receipts"]:
        receipt_path = resolve(item["path"])
        if sha(receipt_path) != item["sha256"]:
            raise ValueError(f"first-pass audit receipt SHA mismatch: {receipt_path}")
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        for result in receipt["new_s6_results"]:
            key = tuple(result["key"])
            if key in first_exact:
                raise ValueError(f"duplicate first-pass S6 root: {key}")
            if result["budget"] != 1_000_000:
                raise ValueError(f"non-1M result in first-pass receipts: {key}")
            first_exact[key] = {"UNKNOWN": 0, "WIN": 1, "LOSS": 2}[result["verdict"]]
            first_budget_nodes["nodes"] += int(result["nodes"])
    if len(first_exact) != 96 or {k for k, v in first_exact.items() if v == 0} != first_unknown:
        raise ValueError("first-pass raw set does not match the 19 UNKNOWN keys")

    escalated = {}
    escalation_receipts = []
    escalated_nodes = 0
    escalated_seconds = 0.0
    s6_loss_witnesses = []
    sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
    from independent import Board
    board = Board(11)
    parent_mask = S5[0] | (S5[1] << 64)
    boundary = {(child & ((1 << 64) - 1), child >> 64): board.legal(child).bit_count()
                for child in board.children(parent_mask)}
    for arg in args.audit:
        audit_path = arg if arg.is_absolute() else ROOT / arg
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
        selection_path = resolve(audit["selection_path"])
        run_path = resolve(audit["run_manifest_path"])
        if sha(selection_path) != audit["selection_sha256"] or sha(run_path) != audit["run_manifest_sha256"]:
            raise ValueError(f"escalation selection/run hash mismatch: {audit_path}")
        selection = json.loads(selection_path.read_text(encoding="utf-8"))
        run = json.loads(run_path.read_text(encoding="utf-8"))
        selected = {int(row["sequence"]): row for row in selection["selected"]}
        records = {int(row["sequence"]): row for row in run["runs"]}
        if selection["solver"]["budget"] != 15_000_000 or set(records) != {int(r["sequence"]) for r in audit["new_s6_results"]}:
            raise ValueError("15M escalation batch run/receipt mismatch")
        for result in audit["new_s6_results"]:
            key = tuple(result["key"])
            seq = int(result["sequence"])
            if key not in first_unknown or key in escalated:
                raise ValueError(f"15M escalation was not a unique 1M UNKNOWN: {key}")
            raw, log = resolve(result["raw_path"]), resolve(result["log_path"])
            if sha(raw) != result["raw_sha256"] or sha(log) != result["log_sha256"]:
                raise ValueError(f"15M escalation raw/log SHA mismatch for {key}")
            parsed = parse_raw(raw)
            expected = {"UNKNOWN": 0, "WIN": 1, "LOSS": 2}[result["verdict"]]
            if (key not in boundary or parsed["key"] != list(key) or parsed["stones"] != 6
                    or parsed["is_or"] != 1 or parsed["legal"] != boundary[key]
                    or parsed["legal"] != selected[seq]["legal"] or parsed["budget"] != 15_000_000
                    or parsed["verdict"] != expected or parsed["nodes"] != result["nodes"]
                    or parsed["nodes"] > 15_000_000):
                raise ValueError(f"S6 escalation raw geometry/polarity/budget mismatch: {key}")
            escalated[key] = {"verdict": expected, "nodes": parsed["nodes"], "budget": parsed["budget"],
                              "raw_path": result["raw_path"], "raw_sha256": result["raw_sha256"],
                              "audit_path": str(audit_path.relative_to(ROOT))}
            escalated_nodes += parsed["nodes"]
            escalated_seconds += float(result["elapsed_seconds"])
            if expected == 2:
                s6_loss_witnesses.append(list(key))
        escalation_receipts.append({"path": str(audit_path.relative_to(ROOT)), "sha256": sha(audit_path),
                                    "rows": len(audit["new_s6_results"]), "outcome": audit["derived_parent_s5_outcome"]})
    if not escalated or len(escalated) > len(first_unknown):
        raise ValueError("missing or overlarge 15M escalation set")

    history = json.loads(HISTORY.read_text(encoding="utf-8"))
    saved = {}
    for row in history:
        key = tuple(row["key"])
        if row["stones"] == 6 and key in boundary and row["verdict"] in (1, 2):
            saved[key] = int(row["verdict"])
    if len(boundary) != 98 or len(saved) != 2 or any(v != 1 for v in saved.values()):
        raise ValueError("saved exact S6 baseline changed")
    final = dict(saved)
    final.update({k: v for k, v in first_exact.items() if v in (1, 2)})
    final.update({k: v["verdict"] for k, v in escalated.items() if v["verdict"] in (1, 2)})
    if s6_loss_witnesses:
        parent = "LOSS"
    elif len(final) == len(boundary) and all(v == 1 for v in final.values()):
        parent = "WIN"
    else:
        parent = "UNKNOWN"
    unresolved = sorted(k for k in boundary if k not in final)
    if parent != "LOSS" or s6_loss_witnesses != [[1152921504675009536, 536870912]]:
        raise ValueError("expected audited S6 LOSS witness did not close S5 AND parent")
    if set(unresolved) != first_unknown - set(escalated):
        raise ValueError("remaining UNKNOWN boundary differs from un-escalated 1M UNKNOWNs")

    source_run_total = sum(first_budget_nodes.values()) + escalated_nodes
    final_path = resolve(args.output)
    doc = {
        "schema": "n11-s4-final-s5-s6-complete-evidence-summary-v1",
        "parent_s5": list(S5), "parent_s5_polarity": "AND (is_or=0)",
        "independent_s6_boundary_size": len(boundary),
        "saved_exact_counts": {"WIN": len(saved), "LOSS": 0},
        "first_pass_1m": {"attempts": len(first_exact), "WIN": sum(v == 1 for v in first_exact.values()),
                          "LOSS": sum(v == 2 for v in first_exact.values()),
                          "UNKNOWN": sum(v == 0 for v in first_exact.values()),
                          "nodes": first_budget_nodes["nodes"], "elapsed_seconds": first["fresh_elapsed_seconds"]},
        "escalation_15m": {"attempts": len(escalated),
                           "WIN": sum(v["verdict"] == 1 for v in escalated.values()),
                           "LOSS": sum(v["verdict"] == 2 for v in escalated.values()),
                           "UNKNOWN": sum(v["verdict"] == 0 for v in escalated.values()),
                           "nodes": escalated_nodes, "elapsed_seconds": escalated_seconds,
                           "unique_first_pass_unknowns_attempted": len(escalated)},
        "combined_boundary": {"WIN": sum(v == 1 for v in final.values()),
                              "LOSS": sum(v == 2 for v in final.values()),
                              "UNKNOWN": len(unresolved), "unresolved_keys": [list(k) for k in unresolved]},
        "s6_loss_witnesses": s6_loss_witnesses,
        "derived_parent_s5_outcome": parent,
        "fresh_solver_nodes": source_run_total,
        "derivation": "one exact S6 LOSS proves the odd-layer S5 AND parent LOSS; other unattempted/UNKNOWN S6 children remain UNKNOWN and are not needed",
        "first_pass_summary_path": str(first_path.relative_to(ROOT)), "first_pass_summary_sha256": sha(first_path),
        "first_pass_audit_receipts": first["audit_receipts"],
        "escalation_audit_receipts": escalation_receipts,
        "history_sha256": sha(HISTORY),
        "solver_binary_sha256": "8d0781ce89ad11a7cd8011cf351d627793b5b76351b7639e433875a43f627cb2",
        "trust": "all exact S6 leaves are solver-trusted; independent Board validates canonical/legal S6 boundary and raw polarity; no terminal-only independent minimax DAG",
    }
    encoded = (json.dumps(doc, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    if final_path.exists() and final_path.read_bytes() != encoded:
        raise ValueError("existing final S6 summary differs; refusing overwrite")
    if not final_path.exists():
        final_path.parent.mkdir(parents=True, exist_ok=True)
        final_path.write_bytes(encoded)
    print(json.dumps({k: v for k, v in doc.items() if k not in ("first_pass_audit_receipts", "escalation_audit_receipts")},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
