#!/usr/bin/env python3
import csv
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
OUT = EXP / "output"
REPO = EXP.parents[2]
WORKLIST = REPO / "research/experiments/n11-class2-lane-closability-ranking-20261116/output/class-frontier-remaining-s6-worklist-1410-20261116.csv"
BIT19_AUDIT = OUT / "class2-lane-cost66i-bit19-bigint-independent-reverification-20261117.json"
INPUTS = {
    "marginals": (OUT / "class2-lane-cost66i-candidate-manifest-marginals-20261116.json", "3343325ae7820d3531fd7b877accb86e39da28a3"),
    "cert_manifest": (OUT / "class2-lane-cost66i-win7-certificates-20261116.json", "8a85ecef573bb6234b2ee1d9f7cb747926bd26ca"),
    "fold64h": (OUT / "class-frontier-cost64h-receipts-recompute-20261117.json", "1633be292f6f1862c895009eac29d398d0be7738"),
    "fold76c": (OUT / "class-frontier-cost76c-receipts-recompute-20261117.json", "953beaea054989e8b1de33f48b1f2ebc13ae7e11"),
    "claim76c": (OUT / "class2-lane-cost76c-inflight-20261116.json", "678211c5a35c25cf41b4a56473942860903647f6"),
    "worklist": (WORKLIST, "2fee1d0718547a62e346d35f5858d7913e37c097"),
    "bit19_bigint_audit": (BIT19_AUDIT, "ef1cefe30f6e030a1a0c5a76339d75f3a9514d7d"),
}


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def read_pinned(path: Path, expected: str, label: str) -> bytes:
    data = path.read_bytes()
    actual = git_blob_sha(data)
    if actual != expected:
        raise AssertionError(f"{label} blob SHA mismatch: {actual} != {expected}")
    return data


def d4(mask: int, transform: int) -> int:
    out = 0
    transforms = (
        lambda x, y: (x, y),
        lambda x, y: (y, 10 - x),
        lambda x, y: (10 - x, 10 - y),
        lambda x, y: (10 - y, x),
        lambda x, y: (10 - x, y),
        lambda x, y: (x, 10 - y),
        lambda x, y: (y, x),
        lambda x, y: (10 - y, 10 - x),
    )
    fn = transforms[transform]
    for bit in range(121):
        if (mask >> bit) & 1:
            x, y = bit % 11, bit // 11
            nx, ny = fn(x, y)
            out |= 1 << (11 * ny + nx)
    return out


def canon(mask: int) -> str:
    return f"{min(d4(mask, t) for t in range(8)):032x}"


def main() -> None:
    raw = {name: read_pinned(path, pin, name) for name, (path, pin) in INPUTS.items()}
    marginals = json.loads(raw["marginals"])
    cert_manifest = json.loads(raw["cert_manifest"])
    fold64h = json.loads(raw["fold64h"])
    fold76c = json.loads(raw["fold76c"])
    claim76c = json.loads(raw["claim76c"])
    bit19_audit = json.loads(raw["bit19_bigint_audit"])

    head = fold76c["frontier_after_cost76c"]
    head_vector = [head[k] for k in (
        "solved_s6_in_manifest", "remaining_s5_orbits", "unique_remaining_s6",
        "sum_remaining_cost", "s6_needed_by_open_classes", "cost_needed_by_open_classes"
    )]
    assert head_vector == [1473, 174, 6375, 504596, 4648, 368510]
    assert marginals["basis"]["head_at_projection"] == [1452, 174, 6396, 506144, 4669, 370058]

    closed64 = sorted({h for parent in fold64h["parents_after"].values() for h in parent.get("lost_rows_hexes", [])})
    assert len(closed64) == 20
    child76 = claim76c["s6_child"]
    assert fold76c["receipts"][0]["marginal_manifest_rows"] == 1
    assert child76 in fold76c["receipts"][0]["marginal_manifest_hexes"]
    assert all(child76 not in c["marginal_manifest_hexes"] for c in marginals["single_candidate_projections"])
    closed = set(closed64) | {child76}

    manifest_by_bit = {entry["bit"]: entry for entry in cert_manifest["certificates"]}
    single = []
    for candidate in marginals["single_candidate_projections"]:
        entry = manifest_by_bit[candidate["bit"]]
        assert entry["root"] == candidate["root_hex"]
        root = int(entry["root"], 16)
        assert canon(root) == entry["d4_canon_root"] == candidate["root_canon"]
        subset_canons = {canon(root ^ (1 << bit)) for bit in range(121) if (root >> bit) & 1}
        assert len(subset_canons) == candidate["covers_d4_s6_orbits"] == 7
        closed_overlap = sorted(set(candidate["marginal_manifest_hexes"]) & closed)
        assert closed_overlap == sorted(candidate["overlap_with_pending_64h_fold_rows"])
        assert not candidate["overlap_with_pending_76c_fold_rows"]
        open_rows = sorted(set(candidate["marginal_manifest_hexes"]) - closed)
        assert len(open_rows) == candidate["marginal_manifest_rows_net_of_pending_64h_fold"]
        single.append({
            "bit": candidate["bit"], "root": entry["root"], "d4_canon_root": entry["d4_canon_root"],
            "covered_s6_orbits": len(subset_canons), "old_manifest_marginal_rows": candidate["marginal_manifest_rows"],
            "closed_rows": closed_overlap, "head1473_single_candidate_rows": open_rows, "row_count": len(open_rows)
        })

    order = marginals["combined_projection"]["fold_order_bits"]
    combined = []
    for candidate in marginals["combined_projection"]["per_candidate_marginal"]:
        rows = sorted(set(candidate["marginal_manifest_hexes"]) - closed)
        combined.append({"bit": candidate["bit"], "head1473_sequential_new_rows": rows, "row_count": len(rows)})
    old_combined_rows = [h for c in marginals["combined_projection"]["per_candidate_marginal"] for h in c["marginal_manifest_hexes"]]
    assert len(old_combined_rows) == len(set(old_combined_rows)) == 9
    combined_rows = [h for item in combined for h in item["head1473_sequential_new_rows"]]
    assert len(combined_rows) == len(set(combined_rows)) == 7

    with WORKLIST.open(newline="", encoding="utf-8") as f:
        worklist = {row["s6_canonical_hex"]: row for row in csv.DictReader(f)}
    row_data = []
    for hex_value in combined_rows:
        row = worklist[hex_value]
        cost = int(row["own_candidates_s6_s7_edge_cost"])
        assert row["category"] == "unswept"
        assert int(row["open_candidates_after_transfers"]) == cost
        assert int(row["engine_win7_d10"]) == 0
        assert int(row["engine_refuted_d10"]) == 0
        assert int(row["transferred_refuted_d10"]) == 0
        row_data.append({"hex": hex_value, "category": row["category"], "edge_cost": cost,
                         "open_parents": int(row["open_parents"]), "open_candidates_after_transfers": int(row["open_candidates_after_transfers"]),
                         "engine_win7_d10": 0, "engine_refuted_d10": 0, "transferred_refuted_d10": 0})
    total_cost = sum(row["edge_cost"] for row in row_data)
    assert total_cost == 514
    for item in combined:
        item["edge_cost_sum"] = sum(worklist[h]["own_candidates_s6_s7_edge_cost"] for h in item["head1473_sequential_new_rows"])
        item["edge_cost_sum"] = int(item["edge_cost_sum"])
    bit19_combined = next(x for x in combined if x["bit"] == 19)
    assert bit19_combined["row_count"] == 3 and bit19_combined["edge_cost_sum"] == 207

    assert bit19_audit["independent_bigint_reverification"]["status"] == "PASS"
    assert bit19_audit["certificate"]["bit"] == 19
    assert fold64h["cross_lane"]["cost66i_conflict_scan"]["conflicts"] == 0
    assert fold64h["cross_lane"]["d4_overlap_with_cost66i"] == []
    assert fold64h["cross_lane"]["d4_overlap_with_cost76c"] == []

    projected = {
        "solved_s6_in_manifest": head["solved_s6_in_manifest"] + len(row_data),
        "unique_remaining_s6": head["unique_remaining_s6"] - len(row_data),
        "sum_remaining_cost": head["sum_remaining_cost"] - total_cost,
        "s6_needed_by_open_classes": head["s6_needed_by_open_classes"] - len(row_data),
        "cost_needed_by_open_classes": head["cost_needed_by_open_classes"] - total_cost,
        "remaining_s5_orbits": "not projected; requires parent-incidence closure audit",
    }
    result = {
        "schema": "n11-class2-lane-cost66i-head1473-marginal-rebase-20261117-v1",
        "date": "2026-11-17",
        "basis_head": head_vector,
        "source_pins": {name: pin for name, (_, pin) in INPUTS.items()},
        "closed_since_old_projection": {
            "cost64h_manifest_rows": closed64, "cost64h_unique_rows": len(closed64),
            "cost76c_manifest_row": child76, "cost76c_manifest_rows": 1,
            "overlap_with_cost66i_candidates": [{"bit": x["bit"], "closed_rows": x["closed_rows"]} for x in single],
        },
        "candidate_root_d4_recheck": [{k: x[k] for k in ("bit", "root", "d4_canon_root", "covered_s6_orbits")} for x in single],
        "single_candidate_marginals_at_head1473": single,
        "combined_fold_order": order,
        "combined_sequential_marginals_at_head1473": combined,
        "union_of_new_manifest_rows": row_data,
        "union_rows": len(row_data), "union_edge_cost": total_cost,
        "projected_frontier_if_all_nine_receipts_folded": projected,
        "projected_frontier_after_bit19_only": {
            "solved_s6_in_manifest": head["solved_s6_in_manifest"] + 3,
            "unique_remaining_s6": head["unique_remaining_s6"] - 3,
            "sum_remaining_cost": head["sum_remaining_cost"] - 207,
            "s6_needed_by_open_classes": head["s6_needed_by_open_classes"] - 3,
            "cost_needed_by_open_classes": head["cost_needed_by_open_classes"] - 207,
            "remaining_s5_orbits": "not projected; requires parent-incidence closure audit",
        },
        "best_next_certificate_fold_candidate": {
            "bit": 19, "new_manifest_rows": 3, "edge_cost_sum": 207,
            "reason": "largest sequential marginal at head1473; certificate has the independent BigInt verification recorded in the bit19 audit",
        },
        "conflict_boundary": {
            "cost64h_cross_lane_conflicts": fold64h["cross_lane"]["cost66i_conflict_scan"]["conflicts"],
            "cost64h_d4_overlap_with_cost66i": fold64h["cross_lane"]["d4_overlap_with_cost66i"],
            "cost64h_d4_overlap_with_cost76c": fold64h["cross_lane"]["d4_overlap_with_cost76c"],
        },
        "interpretation_guard": "This is a set-theoretic rebase of already published D4 candidate projections from head1452 to head1473, not a fresh engine search or a new verdict. No receipt is folded by this audit. REFUTED-D10 is not a LOSS proof. The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
