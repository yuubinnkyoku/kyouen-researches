#!/usr/bin/env python3
"""Rebuild exact-cache S4 boundaries for the 19 unresolved opening orbits."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXPERIMENT = ROOT / "research/experiments/n11-central-reply-frontier-20261012"
OPENINGS = ROOT / "research/experiments/n11-opening-orbits-weak-solve-20261012/output/opening-analysis.json"
ROOT_PROOF = ROOT / "research/experiments/n11-s4-boundary-direct-20261012/output/root-60-27-loss-proof.json"
CACHE = ROOT / "research/experiments/n11-s4-boundary-direct-20261012/output/current-exact-s5.cache"
RAW_AUDIT = ROOT / "research/experiments/n11-s4-boundary-direct-20261012/output/raw-sha256-audit.json"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def cache_key(mask: int) -> tuple[int, int]:
    return mask & ((1 << 64) - 1), mask >> 64


def load_exact_s5_cache(board) -> dict[tuple[int, int], dict[str, int]]:
    rows: dict[tuple[int, int], dict[str, int]] = {}
    with CACHE.open(encoding="utf-8-sig", newline="") as stream:
        for line, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if len(row) != 6 or row[0] != "s5verdict":
                raise ValueError(f"invalid exact-S5 row {line}: {row}")
            lo, hi, stones, verdict, nodes = map(int, row[1:])
            key = (lo, hi)
            mask = lo | (hi << 64)
            if stones != 5 or verdict not in (1, 2) or nodes < 0:
                raise ValueError(f"invalid exact-S5 value at row {line}: {row}")
            if mask.bit_count() != 5 or board.canonical(mask) != mask:
                raise ValueError(f"noncanonical exact-S5 key at row {line}: {key}")
            if key in rows:
                raise ValueError(f"duplicate exact-S5 key at row {line}: {key}")
            rows[key] = {"verdict": verdict, "nodes": nodes}
    return rows


def audit_saved_raws(board) -> tuple[dict[tuple[int, int], int], dict]:
    audit = json.loads(RAW_AUDIT.read_text(encoding="utf-8"))
    if audit.get("untracked_local_raw_references") != 0:
        raise ValueError("raw audit still references untracked local files")
    for receipt in audit["source_audits"]:
        path = ROOT / receipt["path"]
        if not path.is_file() or sha(path) != receipt["sha256"]:
            raise ValueError(f"source audit receipt SHA mismatch: {receipt['path']}")
    relocation = ROOT / audit["saved_raw_relocation_manifest"]
    if sha(relocation) != audit["saved_raw_relocation_manifest_sha256"]:
        raise ValueError("saved-raw relocation manifest SHA mismatch")

    exact: dict[tuple[int, int], int] = {}
    for record in audit["raw_files"]:
        path = ROOT / record["path"]
        if not path.is_file() or path.stat().st_size != record["bytes"] or sha(path) != record["sha256"]:
            raise ValueError(f"saved raw file SHA/size mismatch: {record['path']}")
        lines = path.read_text(encoding="utf-8-sig").splitlines()
        if not 1 <= record["line"] <= len(lines):
            raise ValueError(f"saved raw line missing: {record['path']}:{record['line']}")
        row = next(csv.reader([lines[record["line"] - 1]]))
        if len(row) != 11 or row[0] != "replay":
            raise ValueError(f"saved raw replay row has invalid shape: {record['path']}:{record['line']}")
        parsed = {
            "stones": int(row[2]), "legal": int(row[3]), "budget": int(row[5]),
            "verdict_code": int(row[6]), "nodes": int(row[7]),
            "key": [int(row[9]), int(row[10])],
        }
        for name, value in parsed.items():
            if value != record[name]:
                raise ValueError(f"saved raw {name} mismatch: {record['path']}:{record['line']}")
        mask = parsed["key"][0] | (parsed["key"][1] << 64)
        if mask.bit_count() != parsed["stones"] or board.canonical(mask) != mask:
            raise ValueError(f"saved raw key is not canonical/legal-width: {record['path']}:{record['line']}")
        code = parsed["verdict_code"]
        if parsed["stones"] == 5 and code in (1, 2):
            key = tuple(parsed["key"])
            old = exact.setdefault(key, code)
            if old != code:
                raise ValueError(f"conflicting saved exact raw outcomes for {key}")

    if len(audit["raw_files"]) != audit["unique_raw_file_count"]:
        raise ValueError("raw SHA audit file count mismatch")
    return exact, audit


def point_image(mapping: list[int], point: int) -> int:
    return mapping[point].bit_length() - 1


def third_move_orbits(board, pair_mask: int, fixed_pair: tuple[int, int]) -> list[dict]:
    a, b = fixed_pair
    stabilizer = [mapping for mapping in board.maps
                  if point_image(mapping, a) == a and point_image(mapping, b) == b]
    legal = set(board.points(board.legal(pair_mask)))
    unseen = set(legal)
    result = []
    while unseen:
        seed = min(unseen)
        members = sorted({point_image(mapping, seed) for mapping in stabilizer})
        if not set(members) <= legal:
            raise ValueError("pair stabilizer moved a third move outside the legal set")
        unseen.difference_update(members)
        result.append({"representative": min(members), "members": members, "weight": len(members)})
    result.sort(key=lambda row: row["representative"])
    return result


def s4_status(board, mask: int, cache: dict[tuple[int, int], dict[str, int]]) -> tuple[str, set[int]]:
    memo = getattr(board, "_s4_exact_status_memo", None)
    if memo is None:
        memo = {}
        board._s4_exact_status_memo = memo
    if mask in memo:
        return memo[mask]
    children = set(board.children(mask))
    if not children:
        # Four stones is an even layer: no legal fifth move is a terminal LOSS.
        result = ("LOSS_TERMINAL", children)
        memo[mask] = result
        return result
    values = [cache.get(cache_key(child), {}).get("verdict", 0) for child in children]
    if 1 in values:
        result = ("WIN_CACHE", children)
    elif all(value == 2 for value in values):
        result = ("LOSS_CACHE", children)
    else:
        result = ("UNKNOWN", children)
    memo[mask] = result
    return result


def analyze_pair(board, first: int, reply: int, cache, raw_s5: dict) -> dict:
    pair = (1 << first) | (1 << reply)
    if first == reply or board.canonical(pair) != pair:
        raise ValueError(f"pair root is not canonical: {(first, reply)}")
    third_orbits = third_move_orbits(board, pair, (first, reply))
    if sum(row["weight"] for row in third_orbits) != 119:
        raise ValueError(f"expected 119 legal third moves at pair {(first, reply)}")

    s4_children: dict[int, set[int]] = {}
    third_rows = []
    weighted_fourth_edges = 0
    represented_fourth_edges = 0
    no_fourth_moves = []
    for orbit in third_orbits:
        third = orbit["representative"]
        s3 = pair | (1 << third)
        fourth_moves = board.points(board.legal(s3))
        represented_fourth_edges += len(fourth_moves)
        weighted_fourth_edges += len(fourth_moves) * orbit["weight"]
        if not fourth_moves:
            no_fourth_moves.extend(orbit["members"])
            for member in orbit["members"]:
                third_rows.append({
                    "third_move": member, "third_orbit_representative": third,
                    "third_orbit_weight": orbit["weight"], "fourth_legal_moves": 0,
                    "s4_classes": 0, "s4_loss_cache": 0, "s4_loss_terminal": 0,
                    "s4_win_cache": 0, "s4_unknown": 0,
                    "status": "NO_LEGAL_FOURTH_REPLY",
                })
            continue

        classes = {board.canonical(s3 | (1 << fourth)) for fourth in fourth_moves}
        statuses = Counter()
        for mask in classes:
            status, children = s4_status(board, mask, cache)
            statuses[status] += 1
            s4_children.setdefault(mask, children)
        loss_count = statuses["LOSS_CACHE"] + statuses["LOSS_TERMINAL"]
        row_status = "LOSS_RESPONSE_AVAILABLE" if loss_count else (
            "ALL_FOURTH_REPLIES_S4_WIN" if statuses["WIN_CACHE"] == len(classes) else "UNRESOLVED"
        )
        for member in orbit["members"]:
            third_rows.append({
                "third_move": member, "third_orbit_representative": third,
                "third_orbit_weight": orbit["weight"], "fourth_legal_moves": len(fourth_moves),
                "s4_classes": len(classes), "s4_loss_cache": statuses["LOSS_CACHE"],
                "s4_loss_terminal": statuses["LOSS_TERMINAL"],
                "s4_win_cache": statuses["WIN_CACHE"], "s4_unknown": statuses["UNKNOWN"],
                "status": row_status,
            })

    if len(third_rows) != 119:
        raise ValueError(f"third-move table is incomplete for {(first, reply)}")
    all_children = set().union(*s4_children.values()) if s4_children else set()
    cache_values = Counter(cache[key]["verdict"] for key in (cache_key(child) for child in all_children) if key in cache)
    s4_values = Counter(s4_status(board, mask, cache)[0] for mask in s4_children)
    raw_hits = {cache_key(child) for child in all_children if cache_key(child) in raw_s5}
    for key in raw_hits:
        if raw_s5[key] != cache[key]["verdict"]:
            raise ValueError(f"saved raw/cache exact verdict mismatch at {key}")

    covered = [row["third_move"] for row in third_rows
               if row["status"] in ("LOSS_RESPONSE_AVAILABLE", "NO_LEGAL_FOURTH_REPLY")]
    loss_covered = sum(row["status"] == "LOSS_RESPONSE_AVAILABLE" for row in third_rows)
    root_win_witness = next((row["third_move"] for row in third_rows
                             if row["status"] in ("NO_LEGAL_FOURTH_REPLY", "ALL_FOURTH_REPLIES_S4_WIN")), None)
    if root_win_witness is not None:
        root_outcome = "WIN"
    elif loss_covered == 119:
        root_outcome = "LOSS"
    else:
        root_outcome = "UNKNOWN"

    per_uncovered_min = []
    for row in third_rows:
        if row["status"] != "UNRESOLVED":
            continue
        options = []
        s3 = pair | (1 << row["third_move"])
        for fourth in board.points(board.legal(s3)):
            s4 = board.canonical(s3 | (1 << fourth))
            status, children = s4_status(board, s4, cache)
            if status == "UNKNOWN":
                missing = sum(cache_key(child) not in cache for child in children)
                options.append(missing)
        if options:
            per_uncovered_min.append(min(options))

    return {
        "two_stone_root": [first, reply],
        "root_canonical": True,
        "root_outcome_from_existing_evidence": root_outcome,
        "root_win_witness_third_move": root_win_witness if root_outcome == "WIN" else None,
        "legal_third_moves": len(third_rows),
        "third_move_stabilizer_orbits": len(third_orbits),
        "d4_reduction_ratio_on_third_moves": round(119 / len(third_orbits), 4),
        "fourth_response_edges_reconstructed": weighted_fourth_edges,
        "fourth_response_edges_on_orbit_representatives": represented_fourth_edges,
        "third_moves_with_known_s4_loss_response": loss_covered,
        "third_moves_without_known_s4_loss_response": 119 - loss_covered,
        "third_moves_with_no_legal_fourth_reply": len(no_fourth_moves),
        "s4_classes": len(s4_children),
        "s4_class_status_counts": {
            "LOSS_CACHE": s4_values["LOSS_CACHE"], "LOSS_TERMINAL": s4_values["LOSS_TERMINAL"],
            "WIN_CACHE": s4_values["WIN_CACHE"], "UNKNOWN": s4_values["UNKNOWN"],
        },
        "canonical_s5_boundary_edges": sum(len(children) for children in s4_children.values()),
        "unique_canonical_s5_children": len(all_children),
        "current_exact_s5_cache_hits": sum(cache_values.values()),
        "current_exact_s5_cache_hit_verdicts": {"WIN": cache_values[1], "LOSS": cache_values[2]},
        "current_exact_s5_cache_hits_with_nonzero_solver_nodes": sum(
            cache[key]["nodes"] > 0 for key in (cache_key(child) for child in all_children) if key in cache
        ),
        "current_exact_s5_cache_hits_with_zero_solver_nodes": sum(
            cache[key]["nodes"] == 0 for key in (cache_key(child) for child in all_children) if key in cache
        ),
        "validated_saved_s5_raw_hits_from_k0414_audit": len(raw_hits),
        "validated_saved_s5_raw_hit_verdicts": {
            "WIN": sum(raw_s5[key] == 1 for key in raw_hits),
            "LOSS": sum(raw_s5[key] == 2 for key in raw_hits),
        },
        "uncovered_third_min_unknown_s5_children_to_close_an_s4_loss": {
            "count": len(per_uncovered_min),
            "min": min(per_uncovered_min) if per_uncovered_min else None,
            "median": sorted(per_uncovered_min)[len(per_uncovered_min) // 2] if per_uncovered_min else None,
            "sum_per_uncovered_third_before_dedup": sum(per_uncovered_min),
            "interpretation": "Boundary-selection proxy only; shared S4/S5 dependencies and solver node cost are not represented.",
        },
        "third_move_table": sorted(third_rows, key=lambda row: row["third_move"]),
        "_s4_keys": set(s4_children),
        "_s5_keys": all_children,
        "_s4_loss_keys": {mask for mask in s4_children
                           if s4_status(board, mask, cache)[0] in ("LOSS_CACHE", "LOSS_TERMINAL")},
        "_s5_raw_keys": raw_hits,
    }


def clean_pair_result(result: dict) -> dict:
    return {key: value for key, value in result.items() if not key.startswith("_")}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=EXPERIMENT / "output/central-reply-frontier.json")
    args = parser.parse_args()

    sys.path.insert(0, str(BOARD_SOURCE.parent))
    from independent import Board

    board = Board(11)
    openings = json.loads(OPENINGS.read_text(encoding="utf-8"))
    root_proof = json.loads(ROOT_PROOF.read_text(encoding="utf-8"))
    if root_proof["root_outcome"] != "LOSS" or root_proof["legal_root_moves"] != 119:
        raise ValueError("K0414 root proof is not a complete 119-move LOSS")
    cache = load_exact_s5_cache(board)
    raw_s5, raw_audit = audit_saved_raws(board)

    unresolved = [row for row in openings["orbits"] if row["status"] == "UNRESOLVED"]
    if len(unresolved) != 19:
        raise ValueError(f"expected 19 unresolved D4 opening orbits, found {len(unresolved)}")
    pair_results = [analyze_pair(board, row["representative"], 60, cache, raw_s5) for row in unresolved]
    baseline = analyze_pair(board, 27, 60, cache, raw_s5)

    known_baseline = next(
        row["boundary"] for row in openings["bounded_response_samples"]
        if row["opening_first_move"] == 27 and row["opponent_reply"] == 60
    )
    checks = {
        "current_s5_cache_sha256_matches_k0415": sha(CACHE) == openings["source_hashes"]["current_exact_s5_cache_sha256"],
        "independent_board_sha256_matches_k0415": sha(BOARD_SOURCE) == openings["source_hashes"]["independent_geometry_sha256"],
        "baseline_root_matches_k0415_boundary": all(
            baseline[key] == known_baseline[source]
            for key, source in [
                ("legal_third_moves", "legal_third_moves"),
                ("fourth_response_edges_reconstructed", "fourth_response_edges"),
                ("s4_classes", "canonical_s4_response_classes"),
                ("canonical_s5_boundary_edges", "canonical_s5_boundary_edges"),
                ("unique_canonical_s5_children", "unique_canonical_s5_children"),
                ("current_exact_s5_cache_hits", "current_exact_s5_cache_hits"),
            ]
        ),
        "raw_audit_sha256_references_all_valid": True,
        "raw_audit_unique_files": raw_audit["unique_raw_file_count"],
        "raw_audit_references": raw_audit["raw_reference_count"],
        "raw_audit_untracked_local_references": raw_audit["untracked_local_raw_references"],
        "exact_s5_cache_rows": len(cache),
        "exact_s5_cache_nonzero_nodes": sum(value["nodes"] > 0 for value in cache.values()),
        "standalone_s4_exact_cache_present": False,
    }
    if not all(checks[key] for key in (
        "current_s5_cache_sha256_matches_k0415", "independent_board_sha256_matches_k0415",
        "baseline_root_matches_k0415_boundary", "raw_audit_sha256_references_all_valid",
    )):
        raise ValueError(f"source or baseline regression failed: {checks}")
    if baseline["root_outcome_from_existing_evidence"] != "LOSS" or baseline["third_moves_with_known_s4_loss_response"] != 119:
        raise ValueError("K0414 baseline did not reproduce as 119/119 LOSS coverage")

    s4_membership: dict[int, list[int]] = defaultdict(list)
    s5_membership: dict[int, list[int]] = defaultdict(list)
    all_results = [baseline, *pair_results]
    for index, result in enumerate(all_results):
        for key in result["_s4_keys"]:
            s4_membership[key].append(index)
        for mask in result["_s5_keys"]:
            s5_membership[mask].append(index)
    for index, result in enumerate(all_results):
        shared_s4 = {key for key in result["_s4_keys"] if len(s4_membership[key]) > 1}
        shared_s4_loss = shared_s4 & result["_s4_loss_keys"]
        shared_s5 = {mask for mask in result["_s5_keys"] if len(s5_membership[mask]) > 1}
        shared_raw_keys = {cache_key(mask) for mask in shared_s5}
        result["cross_root_sharing"] = {
            "shared_s4_classes_with_any_other_pair_root": len(shared_s4),
            "shared_known_s4_loss_classes_with_any_other_pair_root": len(shared_s4_loss),
            "shared_canonical_s5_children_with_any_other_pair_root": len(shared_s5),
            "shared_validated_saved_s5_raw_hits": len(shared_raw_keys & result["_s5_raw_keys"]),
        }

    ranked = sorted(
        enumerate(pair_results),
        key=lambda item: (
            -item[1]["third_moves_with_known_s4_loss_response"],
            item[1]["third_moves_without_known_s4_loss_response"],
            -item[1]["cross_root_sharing"]["shared_known_s4_loss_classes_with_any_other_pair_root"],
            -item[1]["validated_saved_s5_raw_hits_from_k0414_audit"],
            -item[1]["current_exact_s5_cache_hits_with_nonzero_solver_nodes"],
            -item[1]["current_exact_s5_cache_hits"],
            item[1]["third_move_stabilizer_orbits"],
            item[1]["s4_classes"],
            item[1]["unique_canonical_s5_children"],
            item[1]["uncovered_third_min_unknown_s5_children_to_close_an_s4_loss"]["sum_per_uncovered_third_before_dedup"],
            item[1]["two_stone_root"][0],
        ),
    )
    for rank, (index, result) in enumerate(ranked, 1):
        result["central_reply_priority_rank"] = rank
        result["priority_note"] = (
            "Coverage/cache-reuse ordering only; the missing-S5-child count is not a solver-node or runtime guarantee."
        )

    result = {
        "schema": "n11-central-reply-s4-s5-frontier-v1",
        "opening_orbit_count": 21,
        "unresolved_opening_orbit_count": 19,
        "first_move_representatives": [row["representative"] for row in unresolved],
        "second_move_under_study": 60,
        "trust_boundary": (
            "S3/S4/S5 boundaries are reconstructed with the independent integer-geometry Board. "
            "S4 LOSS_CACHE/WIN_CACHE classifications use only current solver-trusted exact S5 cache rows; "
            "LOSS_TERMINAL uses no-legal-move normal-play geometry. No pair outcome upgrades an opening result."
        ),
        "source_hashes": {
            "opening_analysis_sha256": sha(OPENINGS),
            "root_60_27_loss_proof_sha256": sha(ROOT_PROOF),
            "current_exact_s5_cache_sha256": sha(CACHE),
            "raw_sha256_audit_sha256": sha(RAW_AUDIT),
            "independent_geometry_sha256": sha(BOARD_SOURCE),
        },
        "audit_checks": checks,
        "baseline_root_60_27_regression": clean_pair_result(baseline),
        "ranked_central_reply_roots": [clean_pair_result(row) for _, row in ranked],
        "cross_root_sharing_summary": {
            "distinct_s4_classes_shared_by_at_least_two_roots": sum(len(owners) > 1 for owners in s4_membership.values()),
            "distinct_s5_children_shared_by_at_least_two_roots": sum(len(owners) > 1 for owners in s5_membership.values()),
            "s4_classes_shared_with_known_root_60_27": sum(0 in owners and len(owners) > 1 for owners in s4_membership.values()),
            "s5_children_shared_with_known_root_60_27": sum(0 in owners and len(owners) > 1 for owners in s5_membership.values()),
        },
        "rank_order_interpretation": (
            "Rank prioritizes existing LOSS-S4 coverage and cross-root LOSS-S4/raw/cache reuse, then fewer "
            "D4-reduced third-move orbits and smaller S4/S5 boundaries. The missing-S5-child aggregate is a "
            "non-guaranteed selection proxy, not solver work. UNKNOWN remains UNKNOWN."
        ),
    }
    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "checks": checks,
        "baseline": {
            "loss_s4_coverage": baseline["third_moves_with_known_s4_loss_response"],
            "s4_classes": baseline["s4_classes"], "s5_hits": baseline["current_exact_s5_cache_hits"],
        },
        "ranked": [{
            "rank": row["central_reply_priority_rank"], "first": row["two_stone_root"][0],
            "outcome": row["root_outcome_from_existing_evidence"],
            "loss_s4_coverage": row["third_moves_with_known_s4_loss_response"],
            "s4_classes": row["s4_classes"], "s5_hits": row["current_exact_s5_cache_hits"],
            "direct_raw_hits": row["validated_saved_s5_raw_hits_from_k0414_audit"],
            "uncovered": row["third_moves_without_known_s4_loss_response"],
        } for row in result["ranked_central_reply_roots"]],
        "cross_root_sharing": result["cross_root_sharing_summary"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
