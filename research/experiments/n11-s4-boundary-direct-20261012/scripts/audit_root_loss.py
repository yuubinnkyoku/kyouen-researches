#!/usr/bin/env python3
"""Build an independent move-by-move LOSS certificate for root {60,27}."""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = ROOT / "research/experiments/n11-s4-boundary-direct-20261012"
CURRENT = EXP / "output/current-exact-s5.cache"
GEOMETRY = ROOT / "research/experiments/n11-strategy-redesign-20261010/output/geometry.json.gz"
S6_AUDIT = EXP / "output/s6-fourteenth-batch-audit.json"
TARGET_S4 = (1297036692683752448, 0)
TARGET_S5 = (1152921504607899649, 536870912)


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def key(mask: int) -> tuple[int, int]:
    return mask & ((1 << 64) - 1), mask >> 64


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output", type=Path, default=EXP / "output/root-60-27-loss-proof.json")
    args = ap.parse_args()
    sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
    from independent import Board
    board = Board(11)
    root = (1 << 60) | (1 << 27)
    if root.bit_count() != 2 or board.canonical(root) != root:
        raise ValueError("root {60,27} must be canonical two-stone position")
    legal_first = board.legal(root)
    moves = [i for i in range(121) if (legal_first >> i) & 1]
    if len(moves) != 119:
        raise ValueError(f"expected 119 legal root moves, got {len(moves)}")

    s5_cache = {}
    with CURRENT.open(encoding="utf-8-sig", newline="") as f:
        for line_no, row in enumerate(csv.reader(f), 1):
            if not row or row[0].strip().startswith("#"):
                continue
            if len(row) != 6 or row[0] != "s5verdict":
                raise ValueError(f"invalid current S5 cache row {line_no}: {row}")
            lo, hi, stones, verdict, nodes = map(int, row[1:])
            k = (lo, hi)
            if stones != 5 or verdict not in (1, 2) or nodes < 0 or k in s5_cache:
                raise ValueError(f"invalid/duplicate exact S5 cache key {k}")
            s5_cache[k] = {"verdict": verdict, "nodes": nodes}

    geometry = {}
    with gzip.open(GEOMETRY, "rt", encoding="utf-8") as f:
        rows = json.load(f)
    if len(rows) != 3384:
        raise ValueError(f"expected 3384 geometry classes, got {len(rows)}")
    for row in rows:
        s4 = tuple(row["key"])
        geometry[s4] = {"coverage": set(row["coverage"]),
                        "children": {tuple(k) for k in row["children"]}}
    if TARGET_S4 not in geometry or TARGET_S5 not in s5_cache or s5_cache[TARGET_S5]["verdict"] != 2:
        raise ValueError("new target S4/S5 LOSS is missing from geometry/cache")
    s6_audit = json.loads(S6_AUDIT.read_text(encoding="utf-8"))
    s6_loss_key = (1152921504675009536, 536870912)
    if s6_audit.get("derived_parent_s5_outcome") != "LOSS" or s6_audit.get("loss_witnesses") != [list(s6_loss_key)]:
        raise ValueError("audited S6 witness for target S5 LOSS is missing")
    s6_record = next((r for r in s6_audit["new_s6_results"] if tuple(r["key"]) == s6_loss_key), None)
    if not s6_record or s6_record["verdict"] != "LOSS":
        raise ValueError("S6 LOSS witness is not present in the audited raw result")
    s6_raw = ROOT / s6_record["raw_path"]
    if sha(s6_raw) != s6_record["raw_sha256"]:
        raise ValueError("S6 LOSS witness raw SHA-256 mismatch")
    with s6_raw.open(encoding="utf-8-sig", newline="") as f:
        raw_rows = [row for row in csv.reader(f) if row and row[0] == "replay"]
    if len(raw_rows) != 1:
        raise ValueError("S6 witness raw must contain one replay row")
    raw_row = raw_rows[0]
    if (tuple(map(int, raw_row[9:11])) != s6_loss_key or int(raw_row[2]) != 6
            or int(raw_row[3]) != 87 or int(raw_row[4]) != 1 or int(raw_row[5]) != 15_000_000
            or int(raw_row[6]) != 2 or int(raw_row[7]) != 5_859_060):
        raise ValueError("S6 loss witness raw row changed or has incorrect polarity/budget")

    # Regenerate the target's full 106-child boundary; this is the new S4 proof.
    target_mask = TARGET_S4[0] | (TARGET_S4[1] << 64)
    target_children = {key(child) for child in board.children(target_mask)}
    if target_children != geometry[TARGET_S4]["children"] or len(target_children) != 106:
        raise ValueError("target S4 child boundary differs from geometry artifact")
    if any(s5_cache.get(child, {}).get("verdict") != 2 for child in target_children):
        raise ValueError("target S4 has a non-LOSS or missing S5 child")

    witnesses = []
    used_s4 = {}
    for move in moves:
        s3 = root | (1 << move)
        if s3.bit_count() != 3 or not board.legal(s3):
            raise ValueError(f"root move {move} is not a legal S3 position")
        legal_reply = board.legal(s3)
        options = []
        for reply in range(121):
            if not (legal_reply >> reply) & 1:
                continue
            s4_mask = s3 | (1 << reply)
            s4_mask = board.canonical(s4_mask)
            s4_key = key(s4_mask)
            geometry_row = geometry.get(s4_key)
            if geometry_row is None or move not in geometry_row["coverage"]:
                raise ValueError(f"S4 class {s4_key} fails reverse incidence for root move {move}")
            child_keys = {key(child) for child in board.children(s4_mask)}
            if child_keys != geometry_row["children"]:
                raise ValueError(f"S4 boundary mismatch for {s4_key}")
            missing = [child for child in child_keys if s5_cache.get(child, {}).get("verdict") != 2]
            if not missing:
                options.append((s4_key, reply, child_keys))
        if not options:
            raise ValueError(f"root move {move} has no exact S4 LOSS reply")
        if move in (100, 108):
            chosen = next((candidate for candidate in options if candidate[0] == TARGET_S4), None)
            if chosen is None:
                raise ValueError(f"new target S4 LOSS does not witness required root move {move}")
        else:
            chosen = min(options, key=lambda x: (x[0][1], x[0][0], x[1]))
        s4_key, reply, child_keys = chosen
        used_s4[s4_key] = child_keys
        witnesses.append({"root_move": move, "s3_stones": 3, "s3_is_or": 0,
                          "s4_reply_move": reply, "s4_class": list(s4_key),
                          "s4_stones": 4, "s4_is_or": 1,
                          "s5_loss_children": len(child_keys)})

    if {w["root_move"] for w in witnesses} != set(moves) or len(witnesses) != 119:
        raise ValueError("root LOSS witness map does not cover every legal root move")
    if not {100, 108} <= {w["root_move"] for w in witnesses}:
        raise ValueError("required previously uncovered moves 100 and 108 are absent")
    if any(next(w for w in witnesses if w["root_move"] == move)["s4_class"] != list(TARGET_S4)
           for move in (100, 108)):
        raise ValueError("target S4 must witness both newly covered root moves 100 and 108")

    output = args.output if args.output.is_absolute() else ROOT / args.output
    doc = {
        "schema": "n11-reply27-root-loss-move-certificate-v1",
        "root_stones": [60, 27], "root_canonical": True,
        "root_fixed_player_polarity": "OR (2 stones)",
        "legal_root_moves": len(moves), "all_root_moves_have_s3_loss_witness": True,
        "s3_fixed_player_polarity": "AND (3 stones); one S4 LOSS reply proves each S3 LOSS",
        "s4_fixed_player_polarity": "OR (4 stones); all canonical S5 children must be exact LOSS",
        "target_s4": list(TARGET_S4), "target_s4_s5_child_count": len(target_children),
        "target_s4_s5_child_verdicts": {"LOSS": len(target_children), "WIN": 0, "UNKNOWN": 0},
        "target_s5_loss_witness": list(TARGET_S5),
        "target_s5_cache_row": s5_cache[TARGET_S5],
        "target_s5_loss_provenance": {
            "s6_key": list(s6_loss_key), "s6_verdict": "LOSS", "s6_legal": 87,
            "s6_budget": 15_000_000, "s6_nodes": 5_859_060,
            "s6_raw_path": s6_record["raw_path"], "s6_raw_sha256": s6_record["raw_sha256"],
            "s6_audit_path": str(S6_AUDIT.relative_to(ROOT)), "s6_audit_sha256": sha(S6_AUDIT),
        },
        "root_move_100_and_108_witness_s4": list(TARGET_S4),
        "distinct_s4_loss_classes_used": len(used_s4),
        "used_s4_loss_classes": [
            {"key": list(s4), "s5_children": len(children),
             "s5_cache_node_field_sum": sum(s5_cache[k]["nodes"] for k in children)}
            for s4, children in sorted(used_s4.items(), key=lambda x: (x[0][1], x[0][0]))
        ],
        "third_move_witnesses": witnesses,
        "third_move_coverage_receipt": "research/experiments/n11-s4-boundary-direct-20261012/output/frontier-after-s6-parent-loss.json",
        "s6_full_boundary_summary": "research/experiments/n11-s4-boundary-direct-20261012/output/s6-final-boundary-summary.json",
        "s5_cache": {"path": str(CURRENT.relative_to(ROOT)), "sha256": sha(CURRENT), "rows": len(s5_cache)},
        "geometry": {"path": str(GEOMETRY.relative_to(ROOT)), "sha256": sha(GEOMETRY)},
        "independent_board_source_sha256": sha(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"),
        "root_outcome": "LOSS",
        "trust": "solver-trusted exact S5 leaves, including a direct S6 LOSS-derived S5 witness; independent Board regenerates every root move, S4 response boundary and S5 child boundary, then checks AND/OR propagation. This is not a terminal-only independent minimax proof.",
    }
    encoded = (json.dumps(doc, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(encoded)
    print(json.dumps({k: v for k, v in doc.items() if k != "third_move_witnesses"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
