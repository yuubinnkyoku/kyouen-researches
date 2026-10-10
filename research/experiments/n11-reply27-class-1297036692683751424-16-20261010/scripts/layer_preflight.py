"""Reconcile saved S6/S7 replay and cache evidence against the target frontier."""
from __future__ import annotations

import csv
import argparse
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
from independent import Board, aggregate  # noqa: E402

PREFLIGHT = EXP / "output/preflight.json"
RAW_S5_AUDIT = EXP / "output/raw-s5-history-audit.json"
LEGACY_S6 = ROOT / "research/experiments/n11-independent-exact-audit-20261010/output/legacy-intermediate-s6.json"


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def resolve_path(text: str) -> Path:
    path = Path(text)
    return path if path.is_absolute() else ROOT / path


def pair(mask: int) -> tuple[int, int]:
    return mask & ((1 << 64) - 1), mask >> 64


def safe_raw(board: Board, raw_key: tuple[int, int], stones: int, legal_count: int) -> tuple[int, int]:
    mask = raw_key[0] | (raw_key[1] << 64)
    if mask.bit_count() != stones or board.canonical(mask) != mask:
        # The CSV stores two words but old raw rows need not be canonical; callers
        # canonicalize separately. This branch only rejects malformed masks.
        if mask.bit_count() != stones:
            raise ValueError(f"wrong stone count: {raw_key} as S{stones}")
    if board.legal(mask).bit_count() != legal_count:
        raise ValueError(f"legal-count mismatch for raw board {raw_key}: {legal_count}")
    return pair(board.canonical(mask))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight", type=Path, default=PREFLIGHT)
    parser.add_argument("--raw-s5-audit", type=Path, default=RAW_S5_AUDIT)
    parser.add_argument("--out", type=Path, default=EXP / "output/saved-layer-preflight.json")
    args = parser.parse_args()
    preflight_path = args.preflight if args.preflight.is_absolute() else ROOT / args.preflight
    raw_audit_path = args.raw_s5_audit if args.raw_s5_audit.is_absolute() else ROOT / args.raw_s5_audit
    out_path = args.out if args.out.is_absolute() else ROOT / args.out
    pre = json.loads(preflight_path.read_text(encoding="utf-8"))
    raw_audit = json.loads(raw_audit_path.read_text(encoding="utf-8"))
    ready_s5 = {tuple(key) for key in raw_audit["dispatch_ready_keys"]}
    target_s5 = {tuple(row["key"]) for row in pre["s5_children"] if tuple(row["key"]) in ready_s5}
    preflight_keys = {tuple(row["key"]) for row in pre["s5_children"]}
    if not target_s5 or ready_s5 - preflight_keys:
        raise SystemExit(f"target raw-history eligibility mismatch: ready={len(ready_s5)} selected={len(target_s5)}")

    board = Board(11)
    s5_to_s6: dict[tuple[int, int], set[tuple[int, int]]] = {}
    s6_to_s5: dict[tuple[int, int], set[tuple[int, int]]] = defaultdict(set)
    for parent in sorted(target_s5):
        mask = parent[0] | (parent[1] << 64)
        children = {pair(child) for child in board.children(mask)}
        s5_to_s6[parent] = children
        for child in children:
            s6_to_s5[child].add(parent)
    target_s6 = set(s6_to_s5)

    legacy = json.loads(LEGACY_S6.read_text(encoding="utf-8"))
    legacy_s6 = {tuple(row["key"]) for row in legacy["parents"]}

    # The complete, hash-checked CSV source inventory was produced by the target
    # S5 raw-history audit. Recheck each source hash before reading S6/S7 rows.
    source_inventory = raw_audit["scanned_csv_sources"]
    raw_s6: dict[tuple[int, int], list[dict]] = defaultdict(list)
    raw_s7: dict[tuple[int, int], list[dict]] = defaultdict(list)
    raw_s7_parent_rows: dict[tuple[int, int], list[dict]] = defaultdict(list)
    projection_counts = Counter()
    matching_raw_files: dict[str, dict] = {}
    for receipt in source_inventory:
        path = resolve_path(receipt["path"])
        if sha(path) != receipt["sha256"]:
            raise SystemExit(f"CSV source changed after S5 preflight: {receipt['path']}")
        found = 0
        with path.open(newline="", encoding="utf-8-sig") as stream:
            for line_no, row in enumerate(csv.reader(stream), 1):
                if not row or row[0].lstrip().startswith("#") or row[0] != "replay":
                    continue
                if len(row) != 11 or row[2] not in ("6", "7"):
                    continue
                stones, legal, is_or, budget, verdict, nodes = map(int, row[2:8])
                if stones not in (6, 7) or is_or != int(stones % 2 == 0):
                    raise ValueError(f"fixed-player layer mismatch at {receipt['path']}:{line_no}")
                raw_key = (int(row[9]), int(row[10]))
                if budget <= 0:
                    projection_counts[str(stones)] += 1
                    continue
                mask = raw_key[0] | (raw_key[1] << 64)
                if mask.bit_count() != stones:
                    raise ValueError(f"wrong stone count at {receipt['path']}:{line_no}")
                canonical_key = pair(board.canonical(mask))
                s6_hit = stones == 6 and canonical_key in target_s6
                s7_parents: set[tuple[int, int]] = set()
                if stones == 7:
                    # reverse incidence uses independent safety and D4 geometry
                    s7_parents = board.predecessors(mask) & target_s6
                if not s6_hit and not s7_parents:
                    continue
                if verdict not in (0, 1, 2) or nodes < 0:
                    raise ValueError(f"invalid replay verdict/nodes at {receipt['path']}:{line_no}")
                checked_key = safe_raw(board, raw_key, stones, legal)
                item = {"path": receipt["path"], "row": line_no, "sha256": receipt["sha256"],
                        "raw_key": list(raw_key), "canonical_key": list(checked_key),
                        "budget": budget, "verdict": verdict, "nodes": nodes, "legal_count": legal}
                if s6_hit:
                    raw_s6[canonical_key].append(item)
                else:
                    raw_s7[canonical_key].append(item)
                    for parent in s7_parents:
                        raw_s7_parent_rows[parent].append(item)
                found += 1
        if found:
            matching_raw_files[receipt["path"]] = {"sha256": receipt["sha256"], "matching_rows": found}

    def exact_map(observations: dict[tuple[int, int], list[dict]], layer: int) -> dict[tuple[int, int], int]:
        result = {}
        for key, rows in observations.items():
            values = {row["verdict"] for row in rows if row["verdict"] in (1, 2)}
            if len(values) > 1:
                raise SystemExit(f"raw S{layer} verdict conflict at {key}: {sorted(values)}")
            if values:
                result[key] = next(iter(values))
        return result

    raw_s6_exact = exact_map(raw_s6, 6)
    raw_s7_exact = exact_map(raw_s7, 7)

    # Inspect saved exact S6/S7 cache rows separately from raw-backed results.
    cache_s6: dict[tuple[int, int], list[dict]] = defaultdict(list)
    cache_s7: dict[tuple[int, int], list[dict]] = defaultdict(list)
    matching_cache_files: dict[str, dict] = {}
    cache_paths = sorted((ROOT / "research/experiments").rglob("*.cache")) + sorted((ROOT / ".local").rglob("*.cache"))
    for path in cache_paths:
        rel = path.resolve().relative_to(ROOT.resolve()).as_posix()
        found = 0
        try:
            stream = path.open(encoding="utf-8-sig")
        except (OSError, UnicodeDecodeError):
            continue
        with stream:
            for line_no, line in enumerate(stream, 1):
                if not line.startswith(("s6verdict,", "s7verdict,")):
                    continue
                fields = line.rstrip("\r\n").split(",")
                stones = int(fields[3])
                if stones not in (6, 7) or len(fields) < 5:
                    raise ValueError(f"malformed exact S{stones} cache row at {rel}:{line_no}")
                key = (int(fields[1]), int(fields[2]))
                verdict = int(fields[4])
                if verdict not in (1, 2):
                    continue
                mask = key[0] | (key[1] << 64)
                if mask.bit_count() != stones or board.canonical(mask) != mask:
                    raise ValueError(f"unsafe/noncanonical S{stones} cache row at {rel}:{line_no}: {key}")
                if stones == 6 and key in target_s6:
                    if key in legacy_s6:
                        continue
                    cache_s6[key].append({"path": rel, "line": line_no, "verdict": verdict})
                    found += 1
                elif stones == 7:
                    parents = board.predecessors(mask) & target_s6
                    if parents:
                        cache_s7[key].append({"path": rel, "line": line_no, "verdict": verdict,
                                              "target_s6_parents": [list(x) for x in sorted(parents)]})
                        found += 1
        if found:
            matching_cache_files[rel] = {"sha256": sha(path), "matching_rows": found}

    cache_s6_exact = {}
    for key, rows in cache_s6.items():
        values = {row["verdict"] for row in rows}
        if len(values) > 1:
            raise SystemExit(f"saved S6 cache conflict at {key}: {rows}")
        cache_s6_exact[key] = next(iter(values))
    for key, rows in cache_s7.items():
        if len({row["verdict"] for row in rows}) > 1:
            raise SystemExit(f"saved S7 cache conflict at {key}: {rows}")

    for key, verdict in raw_s6_exact.items():
        if key in cache_s6_exact and cache_s6_exact[key] != verdict:
            raise SystemExit(f"raw/cache S6 conflict at {key}: {verdict} vs {cache_s6_exact[key]}")

    # Propagate raw S7 only with the fixed-player AND/OR rule. A lone S7 LOSS
    # never makes an S6 WIN. Cache-only S7 remains a separately labelled view.
    def derive_s6_from_s7(s7_exact: dict[tuple[int, int], int], parents: set[tuple[int, int]]):
        derived = {}
        touched = sorted({parent for child in s7_exact
                          for parent in board.predecessors(child[0] | (child[1] << 64)) & parents})
        for parent in touched:
            boundary = {pair(child) for child in board.children(parent[0] | (parent[1] << 64))}
            values = [s7_exact.get(child, 0) for child in boundary]
            verdict = aggregate(6, values)
            if verdict:
                derived[parent] = {"verdict": verdict, "boundary_size": len(boundary),
                                   "known_exact_children": sum(value in (1, 2) for value in values),
                                   "s7_loss_children": sum(value == 2 for value in values),
                                   "s7_win_children": sum(value == 1 for value in values)}
        return derived

    s6_from_raw_s7 = derive_s6_from_s7(raw_s7_exact, target_s6)
    cache_s7_exact = {key: rows[0]["verdict"] for key, rows in cache_s7.items()}
    s6_from_cache_s7 = derive_s6_from_s7(cache_s7_exact, target_s6)

    def classify_s5(s6_values: dict[tuple[int, int], int]) -> dict[tuple[int, int], dict]:
        result = {}
        for parent, children in s5_to_s6.items():
            vals = [s6_values.get(child, 0) for child in children]
            verdict = aggregate(5, vals)
            if verdict:
                result[parent] = {"verdict": verdict, "s6_children": len(children),
                                  "known_exact_s6_children": sum(v in (1, 2) for v in vals),
                                  "s6_loss_children": sum(v == 2 for v in vals),
                                  "s6_win_children": sum(v == 1 for v in vals)}
        return result

    combined_raw_s6 = dict(raw_s6_exact)
    for key, row in s6_from_raw_s7.items():
        old = combined_raw_s6.get(key)
        if old is not None and old != row["verdict"]:
            raise SystemExit(f"raw S6/S7-derived conflict at {key}")
        combined_raw_s6[key] = row["verdict"]
    combined_saved_s6 = dict(combined_raw_s6)
    combined_saved_s6.update(cache_s6_exact)
    for key, row in s6_from_cache_s7.items():
        old = combined_saved_s6.get(key)
        if old is not None and old != row["verdict"]:
            raise SystemExit(f"saved S6/S7 cache conflict at {key}")
        combined_saved_s6[key] = row["verdict"]

    result = {
        "schema": "n11-reply27-target-s6-s7-preflight-v1",
        "preflight": {"path": preflight_path.relative_to(ROOT).as_posix(), "sha256": sha(preflight_path)},
        "s5_raw_history_audit": {"path": raw_audit_path.relative_to(ROOT).as_posix(), "sha256": sha(raw_audit_path),
                                 "scanned_csv_files": len(source_inventory), "target_s5_children": len(target_s5)},
        "s6_boundary": {"distinct_canonical_keys": len(target_s6),
                        "s5_to_s6_edges": sum(map(len, s5_to_s6.values())),
                        "legacy_false_s6_win_keys_in_boundary": sorted([list(k) for k in target_s6 & legacy_s6])},
        "raw_s6": {"exact_keys": {f"{a},{b}": v for (a, b), v in sorted(raw_s6_exact.items())},
                   "observations": {f"{a},{b}": rows for (a, b), rows in sorted(raw_s6.items())},
                   "same_or_higher_15m_unknown_keys": [list(k) for k, rows in sorted(raw_s6.items())
                                                       if any(r["verdict"] == 0 and r["budget"] >= 15_000_000 for r in rows)],
                   "matching_sources": matching_raw_files},
        "raw_s7": {"exact_keys": {f"{a},{b}": v for (a, b), v in sorted(raw_s7_exact.items())},
                   "observations": {f"{a},{b}": rows for (a, b), rows in sorted(raw_s7.items())},
                   "target_s6_parent_intersections": {f"{a},{b}": rows for (a, b), rows in sorted(raw_s7_parent_rows.items())},
                   "matching_sources": matching_raw_files},
        "saved_cache_s6": {"exact_keys": {f"{a},{b}": v for (a, b), v in sorted(cache_s6_exact.items())},
                           "cache_only_keys": sorted([list(k) for k in cache_s6_exact if k not in raw_s6_exact]),
                           "matching_sources": matching_cache_files},
        "saved_cache_s7": {"target_intersections": {f"{a},{b}": rows for (a, b), rows in sorted(cache_s7.items())},
                           "matching_sources": matching_cache_files},
        "cache_only_budget_zero_projections_ignored": dict(sorted(projection_counts.items())),
        "s6_derived_from_raw_s7": {f"{a},{b}": row for (a, b), row in sorted(s6_from_raw_s7.items())},
        "s6_derived_from_cache_s7": {f"{a},{b}": row for (a, b), row in sorted(s6_from_cache_s7.items())},
        "s5_results_from_raw_s6_s7_only": {f"{a},{b}": row for (a, b), row in classify_s5(combined_raw_s6).items()},
        "s5_results_with_saved_cache_s6_s7": {f"{a},{b}": row for (a, b), row in classify_s5(combined_saved_s6).items()},
        "interpretation": "Direct positive-budget replay and cache-only rows are separate. Raw S7 propagation uses the fixed original-player AND/OR rule; S7 LOSS alone never implies S6 WIN. The six quarantined false S6 WIN keys are excluded from cache propagation.",
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"s6_boundary_keys": len(target_s6), "s6_raw_exact": len(raw_s6_exact),
                      "s6_cache_exact": len(cache_s6_exact), "s7_raw_exact": len(raw_s7_exact),
                      "s7_cache_intersection": len(cache_s7), "s5_raw_layer_results": len(result["s5_results_from_raw_s6_s7_only"]),
                      "s5_cache_layer_results": len(result["s5_results_with_saved_cache_s6_s7"]),
                      "out_sha256": sha(out_path)}, sort_keys=True))


if __name__ == "__main__":
    main()
