#!/usr/bin/env python3
"""Independent D4 audit of cost-64f parent ownership and receipt marginals.

This is a bookkeeping audit only. It does not run the game solver and does not
apply a fold to the canonical frontier. It independently reconstructs the
head-1410 -> 1419 -> 1435 marginal rows from published files, then projects the
three cost-64f WIN7-D10 receipts onto the head-1435 S6 manifest.
"""
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
WORKLIST = (HERE.parent / "n11-class2-lane-closability-ranking-20261116"
            / "output" / "class-frontier-remaining-s6-worklist-1410-20261116.csv")
RANKING_1410 = OUT / "class-frontier-s5-ranking-after-cost60c-receipts-20261116.csv"
RANKING_1435 = OUT / "class-frontier-s5-ranking-after-cost64d-receipts-20261116.csv"
FOLD_65J = OUT / "class-frontier-cost65j-receipts-recompute-20261116.json"
FOLD_64D = OUT / "class-frontier-cost64d-receipts-recompute-20261116.json"
CERT_64F = OUT / "class2-lane-cost64f-win3-certificates-20261116.json"
PRESWEEP = OUT / "class2-lane-next-target-presweep-1435-v2-20261116.json"
CLAIM = OUT / "class2-lane-cost64f-inflight-20261116.json"

PARENT_ANCHOR = "00000000000000403800000008000000"
SH_PARENT = "00000000000000003800000008002000"
CHILD = "0000000000000080120a000000800000"
DIRECT_PARENT_HEXES = [
    "00000000000000003800000008002000",
    "0000000000000080120a000000000000",
]
PINNED = {
    "worklist_1410": "2fee1d0718547a62e346d35f5858d7913e37c097",
    "ranking_1410": "a01cfd5340fa89c0eaf834dcb96000f9b04d20ae",
    "fold_65j": "e8c835840f2fad8ffd9a9a8e6f1a9f5944470524",
    "fold_64d": "082aa7f25596fe52e89ae4b158adba64a7f0d4c9",
    "ranking_1435": "130cc5ee24dad54e71f8319935ccaad4d43ab1cb",
}


def git_blob_sha(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def read_csv(path):
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_json(path):
    return json.loads(path.read_text())


def points(hexstr):
    value = int(hexstr, 16)
    return [i for i in range(121) if (value >> i) & 1]


def d4_canon_points(stones):
    best = None
    for swap in (0, 1):
        for flip_x in (0, 1):
            for flip_y in (0, 1):
                value = 0
                for cell in stones:
                    x, y = cell % 11, cell // 11
                    a, b = (y, x) if swap else (x, y)
                    if flip_x:
                        a = 10 - a
                    if flip_y:
                        b = 10 - b
                    value |= 1 << (a + 11 * b)
                text = f"{value:032x}"
                if best is None or text < best:
                    best = text
    return best


def d4_canon_hex(hexstr):
    return d4_canon_points(points(hexstr))


def parent_map(rows):
    result = {}
    for row in rows:
        canonical = d4_canon_hex(row["s5_hex"])
        assert canonical == row["s5_hex"]
        assert canonical not in result
        result[canonical] = {
            "s5_hex": row["s5_hex"],
            "classes_mask": int(row["classes"]),
            "remaining_s6_orbits": int(row["remaining_s6_orbits"]),
            "remaining_s7_edge_cost": int(row["remaining_s7_edge_cost"]),
        }
    return result


def parent_members(row_hex, parents):
    stones = points(row_hex)
    found = {}
    for i in range(len(stones)):
        canonical = d4_canon_points(stones[:i] + stones[i + 1:])
        if canonical in parents:
            found[canonical] = parents[canonical]
    return found


def folded_rows(doc, key):
    rows = []
    for receipt in doc[key]:
        for row_hex in receipt["marginal_manifest_hexes"]:
            rows.append(d4_canon_hex(row_hex))
    assert len(rows) == len(set(rows))
    return set(rows)


def build_row_info(worklist, parents):
    result = {}
    for row in worklist:
        row_hex = row["s6_canonical_hex"]
        assert d4_canon_hex(row_hex) == row_hex
        assert row_hex not in result
        members = parent_members(row_hex, parents)
        assert len(members) == int(row["open_parents"]), row_hex
        masks = [entry["classes_mask"] for entry in members.values()]
        result[row_hex] = {
            "cost": int(row["own_candidates_s6_s7_edge_cost"]),
            "open_parents": len(members),
            "parents": sorted(members),
            "c1": sum(bool(mask & 1) for mask in masks),
            "c2": sum(bool(mask & 2) for mask in masks),
            "c4": sum(bool(mask & 4) for mask in masks),
        }
    return result


def parent_frontier(parents, closed, row_info):
    lost = defaultdict(lambda: {"rows": 0, "cost": 0})
    for row_hex in closed:
        info = row_info[row_hex]
        for parent in info["parents"]:
            lost[parent]["rows"] += 1
            lost[parent]["cost"] += info["cost"]
    result = {}
    for canonical, before in parents.items():
        after_rows = before["remaining_s6_orbits"] - lost[canonical]["rows"]
        after_cost = before["remaining_s7_edge_cost"] - lost[canonical]["cost"]
        assert after_rows >= 0 and after_cost >= 0
        result[canonical] = {
            "s5_hex": before["s5_hex"],
            "classes_mask": before["classes_mask"],
            "remaining_s6_orbits": after_rows,
            "remaining_s7_edge_cost": after_cost,
            "lost_rows": lost[canonical]["rows"],
            "lost_parent_edge_cost": lost[canonical]["cost"],
        }
    return result


def frontier_stats(closed, row_info):
    remaining = [info for row_hex, info in row_info.items()
                 if row_hex not in closed]
    open_only = [info for info in remaining
                 if info["c1"] == 0 and info["c2"] + info["c4"] >= 1]
    hist = Counter((info["c2"], info["c4"]) for info in open_only)
    return {
        "unique_remaining_s6": len(remaining),
        "sum_remaining_cost": sum(info["cost"] for info in remaining),
        "s6_needed_by_open_classes": len(open_only),
        "cost_needed_by_open_classes": sum(info["cost"] for info in open_only),
        "demand_histogram_open_only": {
            f"c2={c2},c4={c4}": count
            for (c2, c4), count in sorted(hist.items())
        },
    }


def compare_frontier(actual, published, solved, remaining_s5):
    assert actual["unique_remaining_s6"] == published["unique_remaining_s6"]
    assert actual["sum_remaining_cost"] == published["sum_remaining_cost"]
    assert actual["s6_needed_by_open_classes"] == published["s6_needed_by_open_classes"]
    assert actual["cost_needed_by_open_classes"] == published["cost_needed_by_open_classes"]
    assert actual["demand_histogram_open_only"] == published["demand_histogram_open_only"]
    assert solved == published["solved_s6_in_manifest"]
    assert remaining_s5 == published["remaining_s5_orbits"]


def main():
    source_paths = {
        "worklist_1410": WORKLIST,
        "ranking_1410": RANKING_1410,
        "fold_65j": FOLD_65J,
        "fold_64d": FOLD_64D,
        "ranking_1435": RANKING_1435,
        "presweep_v2_script": (HERE / "scripts" / "next_target_presweep_head1435_v2_20261116.py"),
        "assembler_script": (HERE / "scripts" / "assemble_cost64f_certificates_20261116.py"),
        "cert64f_manifest": CERT_64F,
        "presweep_v2_json": PRESWEEP,
        "claim64f_v3": CLAIM,
        "audit_script": Path(__file__).resolve(),
    }
    source_pins = {name: {"path": str(path.relative_to(HERE.parents[1])),
                          "git_blob_sha": git_blob_sha(path)}
                   for name, path in source_paths.items()}
    for name, expected in PINNED.items():
        assert source_pins[name]["git_blob_sha"] == expected, name

    worklist = read_csv(WORKLIST)
    ranking_1410_rows = read_csv(RANKING_1410)
    ranking_1435_rows = read_csv(RANKING_1435)
    parents_1410 = parent_map(ranking_1410_rows)
    parents_1435 = parent_map(ranking_1435_rows)
    assert len(worklist) == 6438
    assert len(parents_1410) == len(parents_1435) == 174
    row_info = build_row_info(worklist, parents_1410)
    assert len(row_info) == 6438

    fold65j = read_json(FOLD_65J)
    fold64d = read_json(FOLD_64D)
    closed65j = folded_rows(fold65j, "cost65j_additions_on_cost60c_1410")
    closed64d = folded_rows(fold64d, "cost64d_additions_on_cost65j_1419")
    assert len(closed65j) == 9 and len(closed64d) == 16
    assert not (closed65j & closed64d)
    prior_closed = closed65j | closed64d
    assert len(prior_closed) == 25
    assert prior_closed <= set(row_info)

    base = frontier_stats(set(), row_info)
    assert (base["unique_remaining_s6"], base["sum_remaining_cost"],
            base["s6_needed_by_open_classes"],
            base["cost_needed_by_open_classes"]) == (6438, 509109, 4711, 373023)
    head1419 = frontier_stats(closed65j, row_info)
    parent1419 = parent_frontier(parents_1410, closed65j, row_info)
    head1419_solved = 1410 + len(closed65j)
    head1419_s5 = sum(v["remaining_s6_orbits"] > 0
                      for v in parent1419.values())
    compare_frontier(head1419, fold65j["frontier_after_cost65j"],
                     head1419_solved, head1419_s5)
    head1435 = frontier_stats(prior_closed, row_info)
    parent1435 = parent_frontier(parents_1410, prior_closed, row_info)
    head1435_solved = 1410 + len(prior_closed)
    head1435_s5 = sum(v["remaining_s6_orbits"] > 0
                      for v in parent1435.values())
    compare_frontier(head1435, fold64d["frontier_after_cost64d"],
                     head1435_solved, head1435_s5)
    assert head1435_solved == 1435 and head1435_s5 == 174
    for canonical, predicted in parent1435.items():
        actual = parents_1435[canonical]
        assert predicted["remaining_s6_orbits"] == actual["remaining_s6_orbits"]
        assert predicted["remaining_s7_edge_cost"] == actual["remaining_s7_edge_cost"]

    presweep = read_json(PRESWEEP)
    claim = read_json(CLAIM)
    cert_manifest = read_json(CERT_64F)
    corrected_open = []
    for parent, family in presweep["family_census"].items():
        for row in family["rows"]:
            if row["open_after_census"] > 0:
                corrected_open.append({"cost": row["cost"], "s5_hex": parent, **row})
    corrected_open.sort(key=lambda x: (x["open_after_census"], x["cost"],
                                       x["s6_hex"], x["s5_hex"]))
    corrected_open = corrected_open[:12]
    assert presweep["cheapest_open_rows_ranking"] == corrected_open
    assert presweep["ranking_parent_mapping_audit"]["first_entry"]["s5_hex"] == SH_PARENT
    assert presweep["family_census"][SH_PARENT]["rows"]
    assert any(r["s6_hex"] == CHILD
               for r in presweep["family_census"][SH_PARENT]["rows"])
    assert not any(r["s6_hex"] == CHILD
                   for r in presweep["family_census"][PARENT_ANCHOR]["rows"])

    target_parents = parent_members(CHILD, parents_1435)
    target_parent_hexes = sorted(target_parents)
    assert target_parent_hexes == DIRECT_PARENT_HEXES
    assert PARENT_ANCHOR not in target_parent_hexes
    assert SH_PARENT in target_parent_hexes
    assert presweep["receipt_roots"]["count"] == 757
    assert presweep["receipt_roots"]["distinct_canons"] == 743
    assert presweep["harvest"]["distinct_verdict_canons"] == 4182
    assert presweep["harvest"]["conflicts"] == 0
    assert claim["s5_target"] == SH_PARENT
    assert claim["protocol_anchor_s5_parent"] == PARENT_ANCHOR
    assert sorted(x["s5_hex"] for x in claim["direct_s5_parents"]) == DIRECT_PARENT_HEXES
    assert cert_manifest["target"]["s5_parent"] == SH_PARENT
    assert cert_manifest["target"]["protocol_anchor_s5_parent"] == PARENT_ANCHOR
    assert sorted(x["s5_hex"] for x in cert_manifest["target"]["direct_s5_parents"]) == DIRECT_PARENT_HEXES

    certs = cert_manifest["certificates"]
    assert [c["bit"] for c in certs] == [39, 72, 107]
    pre_bit_table = {r["bit"]: r for r in presweep["cheapest_row_bit_tables"][CHILD]}
    receipt_rows = []
    closed_in_order = set(prior_closed)
    per_receipt = []
    for cert in certs:
        bit = cert["bit"]
        root_hex = cert["root_hex"]
        root_stones = points(root_hex)
        assert len(root_stones) == 7
        expected_root = f"{int(CHILD, 16) | (1 << bit):032x}"
        assert root_hex == expected_root
        root_canon = d4_canon_points(root_stones)
        assert root_canon == cert["d4_canonical_hex"]
        assert pre_bit_table[bit]["status"] == "open"
        assert pre_bit_table[bit]["root_canon"] == root_canon
        assert cert["bigint_verify"]["union_missing"] == 0
        assert cert["bigint_verify"]["union_extra"] == 0
        assert cert["bigint_verify"]["subroots_passed"] == cert["sub_roots"]
        assert cert["bareiss_verify"]["all_subroots_pass"] is True
        assert cert["bareiss_verify"]["subroots_verified"] == cert["sub_roots"]
        hits = sorted({d4_canon_points(root_stones[:i] + root_stones[i + 1:])
                       for i in range(len(root_stones))}
                      & set(row_info))
        marginal = [row for row in hits if row not in closed_in_order]
        closed_in_order.update(marginal)
        per_receipt.append({
            "bit": bit,
            "root_hex": root_hex,
            "root_d4_canonical_hex": root_canon,
            "prior_corpus_status": "open",
            "covered_head1410_worklist_rows": hits,
            "marginal_rows_in_receipt_order": marginal,
            "marginal_count": len(marginal),
        })
        receipt_rows.extend(hits)
    new_rows = set(closed_in_order) - prior_closed
    assert len(new_rows) == 3
    assert [r["marginal_count"] for r in per_receipt] == [1, 0, 2]
    assert len(set(r["root_d4_canonical_hex"] for r in per_receipt)) == 3

    row_details = []
    parent_lost = defaultdict(lambda: {"rows": 0, "cost": 0})
    parent_incidences = 0
    for row_hex in sorted(new_rows):
        info = row_info[row_hex]
        members = parent_members(row_hex, parents_1435)
        assert len(members) == info["open_parents"]
        masks = [entry["classes_mask"] for entry in members.values()]
        c1 = sum(bool(mask & 1) for mask in masks)
        c2 = sum(bool(mask & 2) for mask in masks)
        c4 = sum(bool(mask & 4) for mask in masks)
        assert (c1, c2, c4) == (info["c1"], info["c2"], info["c4"])
        row_details.append({
            "s6_hex": row_hex, "own_candidates_edge_cost": info["cost"],
            "open_s5_parent_incidences": len(members),
            "c1": c1, "c2": c2, "c4": c4,
            "direct_s5_parents": [
                {"s5_hex": h, "classes_mask": members[h]["classes_mask"],
                 "remaining_s6_orbits_head1435": members[h]["remaining_s6_orbits"],
                 "remaining_s7_edge_cost_head1435": members[h]["remaining_s7_edge_cost"]}
                for h in sorted(members)
            ],
            "receipt_bits": sorted(c["bit"] for c in certs
                                   if row_hex in {
                                       d4_canon_points(points(c["root_hex"])[:i] +
                                                       points(c["root_hex"])[i + 1:])
                                       for i in range(7)
                                   }),
        })
        for parent in members:
            parent_lost[parent]["rows"] += 1
            parent_lost[parent]["cost"] += info["cost"]
        parent_incidences += len(members)

    parent_deltas = []
    for parent in sorted(parent_lost):
        before = parents_1435[parent]
        lost = parent_lost[parent]
        after_rows = before["remaining_s6_orbits"] - lost["rows"]
        after_cost = before["remaining_s7_edge_cost"] - lost["cost"]
        assert after_rows > 0
        parent_deltas.append({
            "s5_hex": before["s5_hex"], "classes_mask": before["classes_mask"],
            "before_rows": before["remaining_s6_orbits"],
            "before_parent_edge_cost": before["remaining_s7_edge_cost"],
            "lost_rows": lost["rows"], "lost_parent_edge_cost": lost["cost"],
            "after_rows": after_rows, "after_parent_edge_cost": after_cost,
        })
    assert parent_incidences == 7
    assert sum(p["lost_parent_edge_cost"] for p in parent_deltas) == 455
    assert sum(r["own_candidates_edge_cost"] for r in row_details) == 194

    projected_closed = prior_closed | new_rows
    projected = frontier_stats(projected_closed, row_info)
    projected_parents = parent_frontier(parents_1435, new_rows, row_info)
    projected_s5 = sum(v["remaining_s6_orbits"] > 0
                        for v in projected_parents.values())
    projected_head = {
        "solved_s6_in_manifest": 1435 + len(new_rows),
        "remaining_s5_orbits": projected_s5,
        **projected,
    }
    assert projected_head == {
        "solved_s6_in_manifest": 1438,
        "remaining_s5_orbits": 174,
        "unique_remaining_s6": 6410,
        "sum_remaining_cost": 507143,
        "s6_needed_by_open_classes": 4683,
        "cost_needed_by_open_classes": 371057,
        "demand_histogram_open_only": {
            "c2=0,c4=1": 526, "c2=0,c4=2": 3012, "c2=0,c4=3": 12,
            "c2=1,c4=0": 212, "c2=1,c4=1": 54, "c2=1,c4=2": 9,
            "c2=2,c4=0": 802, "c2=2,c4=1": 5, "c2=2,c4=2": 51,
        },
    }

    result = {
        "schema": "n11-class2-lane-cost64f-parent-marginal-audit-20261116-v1",
        "date": "2026-11-16",
        "main_head_before": "e2df2c3583286cb568614c4c145931eef971629e",
        "canonical_head_before_fold": "1435/174/6413/507337/4686/371251",
        "fold_applied": False,
        "parent_mapping_correction": {
            "old_presweep_blob_sha": "e2d12b5bc3701aa11afa297bb50e6df771fb91cf",
            "old_claim_blob_sha": "48d2de0c0cac1656533a99b8b729297ad95a4307",
            "old_manifest_blob_sha": "33a444b97a55f6fb1b19ec9399c04bb9e7e55c18",
            "previous_s5_target": PARENT_ANCHOR,
            "corrected_s5_target": SH_PARENT,
            "protocol_anchor_s5_parent": PARENT_ANCHOR,
            "direct_s5_parents": DIRECT_PARENT_HEXES,
            "finding": "the selected child is in SH_PARENT and in 0000000000000080120a000000000000; it is not a direct child of PARENT_ANCHOR",
            "fix": "preserve (parent,row) pairs in cheapest_open_rows_ranking; correct claim and certificate-manifest parent metadata",
        },
        "target_row": CHILD,
        "target_parent_membership": next(
            row["direct_s5_parents"] for row in row_details
            if row["s6_hex"] == CHILD
        ),
        "prior_receipt_and_verdict_census": {
            "prior_receipt_roots": presweep["receipt_roots"],
            "harvested_verdict_canons": presweep["harvest"]["distinct_verdict_canons"],
            "harvest_conflicts": presweep["harvest"]["conflicts"],
            "new_roots_open_in_presweep": [r["bit"] for r in per_receipt],
            "note": "the three root canons were open in the head-1435 pre-sweep table, so they were absent from its 743 prior receipt canons and 4,182 harvested verdict canons",
        },
        "prior_fold_marginals": {
            "cost65j_rows": len(closed65j), "cost64d_rows": len(closed64d),
            "union_rows": len(prior_closed),
            "disjoint": True,
        },
        "receipt_marginals_in_order": per_receipt,
        "new_marginal_rows": row_details,
        "new_marginal_row_count": len(new_rows),
        "unique_row_cost_delta": 194,
        "parent_row_incidences": parent_incidences,
        "parent_edge_cost_delta": 455,
        "affected_parent_count": len(parent_deltas),
        "affected_parent_deltas": parent_deltas,
        "projected_head_after_cost64f_fold": projected_head,
        "source_pins": source_pins,
        "checks": {
            "all_6438_worklist_rows_d4_canonical_and_unique": True,
            "all_6438_parent_incidence_counts_match": True,
            "head1410_frontier_reconstructed": True,
            "head1419_frontier_matches_published_fold": True,
            "head1435_frontier_matches_published_fold": True,
            "all_174_head1435_parent_counts_and_costs_match": True,
            "three_new_roots_open_against_prior_census": True,
            "three_new_receipts_cover_three_new_manifest_rows": True,
            "per_receipt_marginals_are_1_0_2": True,
            "no_affected_parent_is_closed": True,
            "parent_ranking_metadata_corrected": True,
        },
        "interpretation_guard": "WIN7-D10 proves only a first-player win within depth 10 from each individual 7-stone root. REFUTED-D10 is not a LOSS proof. The projected head is manifest-coverage bookkeeping, not a game-theoretic result. The canonical head remains 1435 until the full fold script reproduces the chain and performs its complete conflict census.",
        "unknown_status": "11x11 empty board, two-stone roots {49,60} and {59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN",
    }
    out = OUT / "class2-lane-cost64f-parent-and-marginal-audit-20261116.json"
    out.write_text(json.dumps(result, indent=1) + "\n")
    print("wrote", out.name, "marginal rows", len(new_rows),
          "projected head", projected_head)


if __name__ == "__main__":
    main()
