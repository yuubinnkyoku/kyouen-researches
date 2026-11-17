#!/usr/bin/env python3
"""Recompute the cost66i bit-19 receipt fold from a pinned compact input snapshot."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
INPUT = OUT / "class2-lane-cost66i-bit19-parent-incidence-input-20261118.json"
INPUT_BLOB_SHA = "1c6514cf8c5268e06e32743def489ce2573e7ce2"


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\\0" % len(data) + data).hexdigest()


def d4(mask: int, transform: int) -> int:
    result = 0
    maps = (
        lambda x, y: (x, y),
        lambda x, y: (y, 10 - x),
        lambda x, y: (10 - x, 10 - y),
        lambda x, y: (10 - y, x),
        lambda x, y: (10 - x, y),
        lambda x, y: (x, 10 - y),
        lambda x, y: (y, x),
        lambda x, y: (10 - y, 10 - x),
    )
    fn = maps[transform]
    for p in range(121):
        if (mask >> p) & 1:
            x, y = p % 11, p // 11
            xx, yy = fn(x, y)
            result |= 1 << (11 * yy + xx)
    return result


def canon(mask: int) -> str:
    return f"{min(d4(mask, t) for t in range(8)):032x}"


def require(checks, name, condition):
    checks[name] = bool(condition)
    if not condition:
        raise AssertionError(name)


def write_json(path: Path, obj) -> bytes:
    data = (json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\\n").encode()
    path.write_bytes(data)
    return data


def main():
    raw = INPUT.read_bytes()
    checks = {}
    require(checks, "input_blob_sha", git_blob_sha(raw) == INPUT_BLOB_SHA)
    x = json.loads(raw)
    require(checks, "input_schema", x["schema"] == "n11-class2-lane-cost66i-bit19-parent-incidence-input-20261118-v1")

    open_parents = x["open_s5_parents"]
    parent_set = set(open_parents)
    require(checks, "open_s5_parent_count", len(open_parents) == 174 and len(parent_set) == 174)

    root_hex = x["root"]["hex"]
    root = int(root_hex, 16)
    root_stones = [p for p in range(121) if (root >> p) & 1]
    subset_canons = sorted({canon(root ^ (1 << p)) for p in root_stones})
    require(checks, "root_has_seven_stones", len(root_stones) == 7 and x["root"]["stones"] == 7)
    require(checks, "seven_unique_s6_subset_orbits", subset_canons == x["root"]["covered_s6_subset_canons"])
    require(checks, "four_manifest_subset_rows", len(set(x["root"]["manifest_closed_rows"] + [r["hex"] for r in x["target_rows"]]) & set(subset_canons)) == 4)

    incidence = {}
    parent_counts = {}
    parent_cost_delta = {}
    work_cost = {}
    for row in x["target_rows"]:
        mask = int(row["hex"], 16)
        stones = [p for p in range(121) if (mask >> p) & 1]
        raw_parents = [canon(mask ^ (1 << p)) for p in stones if canon(mask ^ (1 << p)) in parent_set]
        unique_parents = sorted(set(raw_parents))
        require(checks, "row_" + row["hex"] + "_parent_set", unique_parents == row["parents"])
        require(checks, "row_" + row["hex"] + "_no_duplicate_parent", len(raw_parents) == len(unique_parents))
        require(checks, "row_" + row["hex"] + "_open_parent_count", len(unique_parents) == row["open_parents"])
        require(checks, "row_" + row["hex"] + "_unswept", row["category"] == "unswept")
        incidence[row["hex"]] = unique_parents
        work_cost[row["hex"]] = row["edge_cost"]
        for parent in unique_parents:
            parent_counts[parent] = parent_counts.get(parent, 0) + 1
            parent_cost_delta[parent] = parent_cost_delta.get(parent, 0) + row["edge_cost"]

    expected_parent_states = {p["s5_hex"]: p for p in x["parent_states_head1473"]}
    require(checks, "five_affected_parents", len(parent_counts) == 5 and set(parent_counts) == set(expected_parent_states))
    parents_after = {}
    for parent in sorted(parent_counts):
        state = expected_parent_states[parent]
        lost_rows = parent_counts[parent]
        lost_cost = parent_cost_delta[parent]
        rows_after = state["rows"] - lost_rows
        cost_after = state["cost"] - lost_cost
        require(checks, "parent_" + parent + "_remains_open", rows_after > 0)
        require(checks, "parent_" + parent + "_state_matches_input",
                lost_rows == state["lost_rows"] and lost_cost == state["lost_edge_cost"])
        parents_after[parent] = {
            "s5_hex": parent,
            "classes": state["classes"],
            "rows_before": state["rows"],
            "rows_after": rows_after,
            "edge_cost_before": state["cost"],
            "edge_cost_after": cost_after,
            "lost_rows": lost_rows,
            "lost_edge_cost": lost_cost,
        }

    total_incidences = sum(parent_counts.values())
    total_parent_delta = sum(parent_cost_delta.values())
    require(checks, "seven_parent_row_incidences", total_incidences == 7)
    require(checks, "parent_edge_cost_delta_489", total_parent_delta == 489)
    require(checks, "no_s5_parent_fully_closed", sum(1 for p in parents_after.values() if p["rows_after"] == 0) == 0)

    calibration = x["cost76c_calibration"]
    calibration_delta = sum(p["cost"] for p in calibration["pairs"])
    require(checks, "cost76c_parent_delta_calibration", len(calibration["pairs"]) == 6 and calibration_delta == calibration["expected_parent_edge_cost_delta"] == 458)

    cert = x["certificate"]
    entry = cert["entry"]
    bigint = cert["bigint"]
    require(checks, "bit19_manifest_win7", entry["bit"] == 19 and entry["verdict"] == "WIN7" and entry["depth"] == 10)
    require(checks, "bit19_root_and_canon", entry["root"] == root_hex and entry["d4_canon_root"] == root_hex)
    require(checks, "bit19_bigint_pass", bigint["status"] == "PASS" and bigint["root_safe"] is True)
    require(checks, "bit19_bigint_subroots", bigint["subroots_passed"] == 52 and bigint["strategy_rows"] == 40935)
    require(checks, "bit19_bigint_exact_union", bigint["union_missing"] == 0 and bigint["union_extra"] == 0 and bigint["consumed_winner_rows"] == 40935)
    require(checks, "bit19_bigint_terminal_range", bigint["terminal_range"] == [13, 17])
    require(checks, "certificate_sha256_matches_manifest", entry["sha256"] == cert["joined_sha256"] == "f87df551ab38f73fb34d756fc4be287de42f1538735e7daf6006deb05749b0ac")
    require(checks, "split_part_sizes", cert["part1"]["bytes"] + cert["part2"]["bytes"] == cert["joined_bytes"] == 1478743)
    require(checks, "split_part_pins", cert["part1"]["git_blob_sha"] == "e8f083cd357ce03aaf177f8ee40c868450e11a37" and cert["part2"]["git_blob_sha"] == "53efcd57fbda21c8f5976987a23f55dbd4cad993")
    require(checks, "split_readme_pin", cert["split_readme"]["path"].endswith("README-split-bit19.md") and len(cert["split_readme"]["git_blob_sha"]) == 40)

    conflicts = x["conflict_checks"]
    require(checks, "cost64h_cost66i_conflicts_zero", conflicts["cost64h_cost66i_conflicts"] == 0)
    require(checks, "no_d4_overlap_cost64h", conflicts["d4_overlap_with_cost64h"] == [])
    require(checks, "no_d4_overlap_cost76c", conflicts["d4_overlap_with_cost76c"] == [])
    require(checks, "cost76c_verdict_conflicts_zero", conflicts["cost76c_verdict_conflicts"] == 0)

    before = x["frontier_before"]
    new_rows = len(x["target_rows"])
    new_cost = sum(work_cost.values())
    fully_closed = sum(1 for p in parents_after.values() if p["rows_after"] == 0)
    after = [
        before[0] + new_rows,
        before[1] - fully_closed,
        before[2] - new_rows,
        before[3] - new_cost,
        before[4] - new_rows,
        before[5] - new_cost,
    ]
    require(checks, "frontier_after_matches_projection", after == x["frontier_after_expected"] == [1476, 174, 6372, 504389, 4645, 368303])
    require(checks, "three_new_manifest_rows", new_rows == 3 and new_cost == 207)
    require(checks, "source_pins_present", len(x["source_pins"]) == 9 and x["source_pins"].get(cert["manifest_path"]) == cert["manifest_blob_sha"])

    source_pins = dict(x["source_pins"])
    source_pins["input_snapshot"] = INPUT_BLOB_SHA
    source_pins["certificate_part1"] = cert["part1"]["git_blob_sha"]
    source_pins["certificate_part2"] = cert["part2"]["git_blob_sha"]
    source_pins["certificate_split_readme"] = cert["split_readme"]["git_blob_sha"]

    frontier_before = {
        "solved_s6_in_manifest": before[0], "remaining_s5_orbits": before[1],
        "unique_remaining_s6": before[2], "sum_remaining_cost": before[3],
        "s6_needed_by_open_classes": before[4], "cost_needed_by_open_classes": before[5],
    }
    frontier_after = {
        "solved_s6_in_manifest": after[0], "remaining_s5_orbits": after[1],
        "unique_remaining_s6": after[2], "sum_remaining_cost": after[3],
        "s6_needed_by_open_classes": after[4], "cost_needed_by_open_classes": after[5],
    }
    receipt = {
        "bit": 19, "root_hex": root_hex, "d4_canon_root": root_hex,
        "verdict": "WIN7-D10", "depth": 10,
        "certificate": {
            "path": "class2-lane-cost66i-certificates/" + entry["file"],
            "storage": "two pinned parts; reconstruct by concatenating part1of2 then part2of2",
            "part1_git_blob_sha": cert["part1"]["git_blob_sha"],
            "part2_git_blob_sha": cert["part2"]["git_blob_sha"],
            "split_readme_git_blob_sha": cert["split_readme"]["git_blob_sha"],
            "bytes": cert["joined_bytes"], "sha256": cert["joined_sha256"],
            "strategy_rows": bigint["strategy_rows"], "subroots_passed": bigint["subroots_passed"],
            "root_mobility": bigint["root_mobility"], "visited_states": bigint["visited_states_across_subroots"],
            "loser_reply_edges": bigint["loser_reply_edges"], "terminal_count": bigint["terminal_count"],
            "terminal_range": bigint["terminal_range"], "union_missing": bigint["union_missing"],
            "union_extra": bigint["union_extra"], "bigint_status": bigint["status"],
            "extraction_nodes": entry["extraction_nodes"], "fbt_drops": entry["fbt_drops"],
        },
        "marginal_d4_s6_orbits": len(subset_canons),
        "marginal_manifest_rows": new_rows,
        "marginal_manifest_hexes": [r["hex"] for r in x["target_rows"]],
        "extraction_nodes": entry["extraction_nodes"],
        "fbt_drops": entry["fbt_drops"],
        "fatal": entry.get("fatal"),
    }
    fold = {
        "schema": "n11-class2-lane-cost66i-bit19-receipts-recompute-20261118-v1",
        "date": "2026-11-18", "status": "fold-complete",
        "basis_head": frontier_before, "frontier_after_cost66i_bit19": frontier_after,
        "receipts": [receipt],
        "totals": {
            "receipts": 1, "total_certificate_bytes": cert["joined_bytes"],
            "total_strategy_rows": bigint["strategy_rows"], "total_extraction_nodes": entry["extraction_nodes"],
            "total_visited_states": bigint["visited_states_across_subroots"],
            "total_loser_reply_edges": bigint["loser_reply_edges"], "total_terminals": bigint["terminal_count"],
            "marginal_d4_s6_orbits": len(subset_canons), "marginal_manifest_rows": new_rows,
            "s6_edge_cost_removed": new_cost,
        },
        "parents_after": parents_after,
        "parent_row_incidences": total_incidences,
        "parent_edge_cost_delta": total_parent_delta,
        "parent_count_fully_closed": fully_closed,
        "conflict_census": {
            "cost64h_cost66i_conflicts": conflicts["cost64h_cost66i_conflicts"],
            "d4_overlap_with_cost64h": len(conflicts["d4_overlap_with_cost64h"]),
            "d4_overlap_with_cost76c": len(conflicts["d4_overlap_with_cost76c"]),
            "cost76c_verdict_conflicts": conflicts["cost76c_verdict_conflicts"],
        },
        "source_blob_pins": source_pins,
        "certificate_manifest": {"path": cert["manifest_path"], "git_blob_sha": cert["manifest_blob_sha"]},
        "input_snapshot": {"path": INPUT.name, "git_blob_sha": INPUT_BLOB_SHA},
        "interpretation_guard": "Bookkeeping fold over one independently verified WIN7-D10 receipt. It closes three S6 manifest rows and reduces open frontier demand; it closes no S5 parent, creates no new engine verdict, and does not solve the standard 11x11 empty board.",
        "next_action": "Recompute the remaining eight cost66i receipt marginals and conflict census against head 1476 before folding another receipt.",
    }
    audit = {
        "schema": "n11-class2-lane-cost66i-bit19-receipt-fold-audit-20261118-v1",
        "date": "2026-11-18", "status": "PASS",
        "all_checks_pass": all(checks.values()), "check_count": len(checks), "checks": checks,
        "fold": {
            "basis_head": before, "frontier_after": after, "closed_manifest_rows": new_rows,
            "marginal_d4_s6_orbits": len(subset_canons), "affected_s5_parents": len(parents_after),
            "parent_row_incidences": total_incidences, "parent_edge_cost_delta": total_parent_delta,
            "fully_closed_s5_parents": fully_closed,
        },
        "certificate": {
            "bit": 19, "root": root_hex, "rows": bigint["strategy_rows"],
            "bytes": cert["joined_bytes"], "sha256": cert["joined_sha256"],
            "bigint_subroots": bigint["subroots_passed"], "union_missing": bigint["union_missing"],
            "union_extra": bigint["union_extra"], "terminal_range": bigint["terminal_range"],
        },
        "input_snapshot_blob_sha": INPUT_BLOB_SHA, "source_blob_pins": source_pins,
        "interpretation_guard": fold["interpretation_guard"],
    }
    fold_path = OUT / "class-frontier-cost66i-bit19-receipts-recompute-20261118.json"
    audit_path = OUT / "class2-lane-cost66i-bit19-receipt-fold-audit-20261118.json"
    fold_bytes = write_json(fold_path, fold)
    audit_bytes = write_json(audit_path, audit)
    print(json.dumps({
        "status": audit["status"], "checks": audit["check_count"],
        "passed": sum(checks.values()), "head_before": before, "head_after": after,
        "closed_manifest_rows": new_rows, "parent_row_incidences": total_incidences,
        "parent_edge_cost_delta": total_parent_delta, "fully_closed_s5_parents": fully_closed,
        "fold_git_blob_sha": git_blob_sha(fold_bytes), "audit_git_blob_sha": git_blob_sha(audit_bytes),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
