#!/usr/bin/env python3
"""Recompute and verify the Q-family remaining D4-root worklist from pinned CSV inputs."""
from __future__ import annotations

import argparse
import csv
import io
import json
import subprocess
from collections import Counter, defaultdict
from functools import lru_cache
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent / "output"

WORKLIST = "research/experiments/n11-class2-lane-closability-ranking-20261116/output/class-frontier-remaining-s6-worklist-1410-20261116.csv"
RANKING = "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-s5-ranking-after-cost65j-receipts-20261116.csv"
CLOSABILITY = "research/experiments/n11-class2-lane-closability-ranking-20261116/output/class-frontier-s5-closability-after-cost60c-20261116.csv"
TOP = "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost65j-receipts-20261116.csv"

EXPECTED_BLOBS = {
    WORKLIST: "2fee1d0718547a62e346d35f5858d7913e37c097",
    RANKING: "cbed4d094b87dc4fe2cc48b2db375d7ddb0776c6",
    CLOSABILITY: "65215b6582de6efedfed8d77d91630edd883a2cb",
    TOP: "08aaf31892680668e7e292848235a154eb746407",
}

Q_HEX = "00000000000000821082000000000000"
P_HEX = "00000000000000403800000008000000"
TOP_FAMILIES = {
    "00000000020000003800000080000000": "class4",
    "00000000000000809082000000000000": "audit_blocked",
    "00000000000000801202000000200000": "best_coverable",
    "00000000000000801202000040000000": "second_coverable",
}
FAMILY_ORDER = ["Q", "P", "class4", "audit_blocked", "best_coverable", "second_coverable"]


def pinned_text(rel: str) -> str:
    result = subprocess.run(
        ["git", "rev-parse", f"HEAD:{rel}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if result != EXPECTED_BLOBS[rel]:
        raise AssertionError(f"source blob changed: {rel}: {result}")
    return (ROOT / rel).read_text(encoding="utf-8")


def bits(mask: int) -> list[int]:
    return [i for i in range(121) if (mask >> i) & 1]


def transform_bit(bit: int, transform: int) -> int:
    x, y = bit % 11, bit // 11
    if transform == 0:
        X, Y = x, y
    elif transform == 1:
        X, Y = 10 - y, x
    elif transform == 2:
        X, Y = 10 - x, 10 - y
    elif transform == 3:
        X, Y = y, 10 - x
    elif transform == 4:
        X, Y = 10 - x, y
    elif transform == 5:
        X, Y = 10 - y, 10 - x
    elif transform == 6:
        X, Y = x, 10 - y
    else:
        X, Y = y, x
    return Y * 11 + X


def transform_mask(mask: int, transform: int) -> int:
    out = 0
    for bit in bits(mask):
        out |= 1 << transform_bit(bit, transform)
    return out


def canonical(mask: int) -> int:
    return min(transform_mask(mask, t) for t in range(8))


def contains_parent(s6: int, parent: int) -> bool:
    return any((transform_mask(s6, t) & parent) == parent for t in range(8))


def bareiss_det(matrix: list[list[int]]) -> int:
    a = [list(map(int, row)) for row in matrix]
    n = len(a)
    sign = 1
    previous = 1
    for k in range(n - 1):
        if a[k][k] == 0:
            swap = next((i for i in range(k + 1, n) if a[i][k] != 0), None)
            if swap is None:
                return 0
            a[k], a[swap] = a[swap], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = a[i][j] * pivot - a[i][k] * a[k][j]
                if numerator % previous:
                    raise AssertionError("Bareiss division was not exact")
                a[i][j] = numerator // previous
        for i in range(k + 1, n):
            a[i][k] = 0
        previous = pivot
    return sign * a[n - 1][n - 1]


def det4_points(points: tuple[int, int, int, int]) -> int:
    matrix = []
    for bit in points:
        x, y = bit % 11, bit // 11
        matrix.append([x * x + y * y, x, y, 1])
    return bareiss_det(matrix)


def legal_candidates(mask: int) -> list[int]:
    stones = bits(mask)
    triples = list(combinations(stones, 3))
    out = []
    for d in range(121):
        if (mask >> d) & 1:
            continue
        if all(det4_points((a, b, c, d)) != 0 for a, b, c in triples):
            out.append(d)
    return out


def build_family(rows, family_id: str, parent_hex: str, s6_field: str, cost_field: str):
    parent = int(parent_hex, 16)
    owners = defaultdict(list)
    occurrences = 0
    for row in rows:
        s6_hex = row[s6_field]
        mask = int(s6_hex, 16)
        if not contains_parent(mask, parent):
            raise AssertionError(f"{family_id}: parent is not a D4 subset of {s6_hex}")
        candidates = legal_candidates(mask)
        expected = int(row[cost_field])
        if len(candidates) != expected:
            raise AssertionError(f"{family_id}: edge cost mismatch at {s6_hex}: {len(candidates)} != {expected}")
        local = set()
        for bit in candidates:
            root = canonical(mask | (1 << bit))
            if root.bit_count() != 7:
                raise AssertionError("candidate root is not seven stones")
            local.add(root)
            owners[root].append({"s6_hex": s6_hex, "bit": bit})
        if len(local) != len(candidates):
            raise AssertionError(f"{family_id}: intra-row D4 collision at {s6_hex}")
        occurrences += expected
    return {"id": family_id, "parent_hex": parent_hex, "rows": len(rows),
            "occurrences": occurrences, "owners": owners}


def multiplicity(owners) -> dict[str, int]:
    counts = Counter(len(v) for v in owners.values())
    return {str(k): counts[k] for k in sorted(counts)}


def summarize(family) -> dict:
    unique = len(family["owners"])
    redundant = family["occurrences"] - unique
    return {
        "rows": family["rows"],
        "candidate_occurrences": family["occurrences"],
        "unique_d4_root_orbits": unique,
        "redundant_occurrences": redundant,
        "saved_pct": round(100 * redundant / family["occurrences"], 3),
        "root_owner_multiplicity": multiplicity(family["owners"]),
    }


def sorted_owners(owners):
    return sorted(owners, key=lambda x: (x["s6_hex"], x["bit"]))


def csv_text(headers, rows) -> str:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=headers, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()


def matching_for_q(q_family, q_row_ids):
    index = {s6_hex: i for i, s6_hex in enumerate(q_row_ids)}
    pair_roots = defaultdict(list)
    for root, owners in q_family["owners"].items():
        if len(owners) == 2:
            a, b = sorted_owners(owners)
            i, j = sorted((index[a["s6_hex"]], index[b["s6_hex"]]))
            pair_roots[(i, j)].append(root)
    for roots in pair_roots.values():
        roots.sort()

    pair_hist = Counter(len(roots) for roots in pair_roots.values())
    missing = []
    for i, j in combinations(range(len(q_row_ids)), 2):
        if (i, j) not in pair_roots:
            missing.append({"row_a_s6_hex": q_row_ids[i], "row_b_s6_hex": q_row_ids[j]})

    n = len(q_row_ids)

    @lru_cache(None)
    def best(mask: int):
        if mask == 0:
            return 0, ()
        i = (mask & -mask).bit_length() - 1
        rest = mask & ~(1 << i)
        best_value = -10**9
        best_pairs = None
        for j in range(i + 1, n):
            if not (rest >> j) & 1:
                continue
            roots = pair_roots.get((i, j))
            if not roots:
                continue
            sub_value, sub_pairs = best(rest & ~(1 << j))
            candidate_pairs = ((i, j),) + sub_pairs
            value = len(roots) + sub_value
            if value > best_value or (
                value == best_value and (best_pairs is None or candidate_pairs < best_pairs)
            ):
                best_value, best_pairs = value, candidate_pairs
        if best_pairs is None:
            return -10**9, ()
        return best_value, best_pairs

    weight, pairs = best((1 << n) - 1)
    if len(pairs) != 9 or weight != 36 or len(missing) != 1:
        raise AssertionError("Q maximum-weight perfect matching control failed")

    seed_rows = []
    seed_map = {}
    matching_audit = []
    for pair_id, (i, j) in enumerate(pairs, 1):
        roots = sorted(pair_roots[(i, j)])
        if len(roots) != 4:
            raise AssertionError("matched pair does not have four alternatives")
        root_hexes = [f"{root:032x}" for root in roots]
        matching_audit.append({
            "pair_id": pair_id,
            "row_a_s6_hex": q_row_ids[i],
            "row_b_s6_hex": q_row_ids[j],
            "shared_root_orbits": len(roots),
            "primary_root_hex": root_hexes[0],
            "alternative_root_hexes": root_hexes,
        })
        for rank, root in enumerate(roots, 1):
            seed_map[root] = {"pair_id": pair_id, "alternative_rank": rank, "is_primary": rank == 1}
            seed_rows.append({
                "pair_id": pair_id,
                "row_a_s6_hex": q_row_ids[i],
                "row_b_s6_hex": q_row_ids[j],
                "pair_weight": len(roots),
                "alternative_rank": rank,
                "canonical_root_hex": f"{root:032x}",
                "is_primary": rank == 1,
            })

    return pair_roots, pair_hist, missing, weight, matching_audit, seed_rows, seed_map


def compute():
    work_text = pinned_text(WORKLIST)
    ranking_text = pinned_text(RANKING)
    closability_text = pinned_text(CLOSABILITY)
    top_text = pinned_text(TOP)

    work_rows = list(csv.DictReader(io.StringIO(work_text)))
    ranking_rows = list(csv.DictReader(io.StringIO(ranking_text)))
    closability_rows = list(csv.DictReader(io.StringIO(closability_text)))

    top_rows = []
    for row in csv.reader(io.StringIO(top_text)):
        if not row or row[0].startswith("#") or row[0] == "s5_hex" or len(row) < 3:
            continue
        top_rows.append({"s5_hex": row[0], "s6_hex": row[1], "cost": int(row[2])})

    q_rows = [r for r in work_rows if contains_parent(int(r["s6_canonical_hex"], 16), int(Q_HEX, 16))]
    p_rows = [r for r in work_rows if contains_parent(int(r["s6_canonical_hex"], 16), int(P_HEX, 16))]

    for family_id, rows in (("Q", q_rows), ("P", p_rows)):
        for row in rows:
            edge = int(row["own_candidates_s6_s7_edge_cost"])
            if row["category"] != "unswept":
                raise AssertionError(f"{family_id}: expected unswept row")
            if int(row["open_candidates_after_transfers"]) != edge:
                raise AssertionError(f"{family_id}: open candidate count differs from edge cost")
            if any(int(row[k]) for k in ("engine_win7_d10", "engine_refuted_d10", "transferred_refuted_d10")):
                raise AssertionError(f"{family_id}: expected no prior verdicts")

    q = build_family(q_rows, "Q", Q_HEX, "s6_canonical_hex", "own_candidates_s6_s7_edge_cost")
    p = build_family(p_rows, "P", P_HEX, "s6_canonical_hex", "own_candidates_s6_s7_edge_cost")

    ranking_by_parent = {r["s5_hex"]: r for r in ranking_rows}
    closability_by_parent = {r["s5_hex"]: r for r in closability_rows}
    for parent, family_id, expected_class, expected_rows, expected_cost in (
        (Q_HEX, "Q", "1", 18, 1238),
        (P_HEX, "P", "2", 24, 1704),
    ):
        rank = ranking_by_parent[parent]
        close = closability_by_parent[parent]
        if (rank["classes"], int(rank["remaining_s6_orbits"]), int(rank["remaining_s7_edge_cost"])) != (
            expected_class, expected_rows, expected_cost
        ):
            raise AssertionError(f"{family_id}: post-cost65j ranking mismatch")
        if close["category"] != "own_closable":
            raise AssertionError(f"{family_id}: expected own_closable")
        if int(close["remaining_s6_orbits"]) != expected_rows or int(close["remaining_s7_edge_cost"]) != expected_cost:
            raise AssertionError(f"{family_id}: head-1410 closability mismatch")

    top_family_rows = defaultdict(list)
    for row in top_rows:
        if row["s5_hex"] not in TOP_FAMILIES:
            raise AssertionError(f"unexpected top family {row['s5_hex']}")
        top_family_rows[row["s5_hex"]].append(row)

    top_families = {}
    for parent, family_id in TOP_FAMILIES.items():
        top_families[family_id] = build_family(
            top_family_rows[parent], family_id, parent, "s6_hex", "cost"
        )

    q_mult = multiplicity(q["owners"])
    p_mult = multiplicity(p["owners"])
    if (q["rows"], q["occurrences"], len(q["owners"]), q_mult) != (
        18, 1238, 687, {"1": 136, "2": 551}
    ):
        raise AssertionError("Q family exact orbit census mismatch")
    if (p["rows"], p["occurrences"], len(p["owners"]), p_mult) != (
        24, 1704, 1468, {"1": 1232, "2": 236}
    ):
        raise AssertionError("P family exact orbit census mismatch")

    q_row_ids = [r["s6_canonical_hex"] for r in q_rows]
    pair_roots, pair_hist, missing, matching_weight, matching_audit, seed_rows, seed_map = matching_for_q(q, q_row_ids)

    q_work_rows = []
    priority_rank = {"seed_primary": 0, "seed_alternative": 1, "shared_two_owner": 2, "single_owner": 3}
    for root, owners0 in q["owners"].items():
        owners = sorted_owners(owners0)
        seed = seed_map.get(root)
        if seed:
            priority = "seed_primary" if seed["is_primary"] else "seed_alternative"
        else:
            priority = "shared_two_owner" if len(owners) == 2 else "single_owner"
        q_work_rows.append({
            "canonical_root_hex": f"{root:032x}",
            "owner_count": len(owners),
            "priority": priority,
            "seed_pair_id": seed["pair_id"] if seed else "",
            "seed_alternative_rank": seed["alternative_rank"] if seed else "",
            "representative_s6_hex": owners[0]["s6_hex"],
            "representative_bit": owners[0]["bit"],
            "owners_json": json.dumps(owners, separators=(",", ":")),
        })
    q_work_rows.sort(key=lambda r: (priority_rank[r["priority"]], r["canonical_root_hex"]))

    family_maps = {"Q": q["owners"], "P": p["owners"]}
    family_maps.update({name: fam["owners"] for name, fam in top_families.items()})
    pairwise = {}
    for i, a in enumerate(FAMILY_ORDER):
        for b in FAMILY_ORDER[i + 1:]:
            pairwise[f"{a}|{b}"] = len(set(family_maps[a]) & set(family_maps[b]))

    all_roots = set().union(*(set(m) for m in family_maps.values()))
    cross_rows = []
    for root in sorted(all_roots):
        names = [name for name in FAMILY_ORDER if root in family_maps[name]]
        if len(names) <= 1:
            continue
        owners = []
        for name in names:
            for owner in sorted_owners(family_maps[name][root]):
                owners.append({"family": name, "s6_hex": owner["s6_hex"], "bit": owner["bit"]})
        cross_rows.append({
            "canonical_root_hex": f"{root:032x}",
            "families": names,
            "owners": owners,
        })

    expected_cross = {
        "Q|P": 0,
        "Q|class4": 0,
        "Q|audit_blocked": 0,
        "Q|best_coverable": 0,
        "Q|second_coverable": 0,
        "P|class4": 2,
        "P|audit_blocked": 4,
        "P|best_coverable": 4,
        "P|second_coverable": 4,
        "class4|audit_blocked": 0,
        "class4|best_coverable": 0,
        "class4|second_coverable": 0,
        "audit_blocked|best_coverable": 0,
        "audit_blocked|second_coverable": 0,
        "best_coverable|second_coverable": 2,
    }
    if pairwise != expected_cross or len(cross_rows) != 16:
        raise AssertionError("cross-family orbit overlap control mismatch")

    family_summaries = {"Q": summarize(q), "P": summarize(p)}
    family_summaries.update({name: summarize(fam) for name, fam in top_families.items()})
    total_occurrences = q["occurrences"] + p["occurrences"] + sum(f["occurrences"] for f in top_families.values())
    global_unique = len(all_roots)
    redundant = total_occurrences - global_unique

    audit = {
        "schema": "n11-frontier-q-family-remaining-orbit-dedup-20261116-v1",
        "date": "2026-11-16",
        "baseline": {
            "worklist_head": 1410,
            "post_cost65j_frontier_head": 1419,
            "note": "Q/P parent counts and costs are rechecked against the post-cost65j ranking; no cost65j receipt changed either family.",
        },
        "inputs": {
            WORKLIST: {"git_blob_sha": EXPECTED_BLOBS[WORKLIST]},
            RANKING: {"git_blob_sha": EXPECTED_BLOBS[RANKING]},
            CLOSABILITY: {"git_blob_sha": EXPECTED_BLOBS[CLOSABILITY]},
            TOP: {"git_blob_sha": EXPECTED_BLOBS[TOP]},
        },
        "candidate_rule": {
            "source": "K0868",
            "definition": "For a six-stone S6 row, enumerate empty cells d for which det4(a,b,c,d) != 0 for every 3-subset of the six stones; canonicalize each resulting seven-stone root under D4.",
            "determinant": "Bareiss 4x4 determinant of rows [x^2+y^2,x,y,1] in the independent verifier; equivalent to the K0868 integer det4 rule.",
            "symmetry": "All eight D4 square isometries; canonical root is the minimum 128-bit mask.",
        },
        "targets": {
            "Q": {
                "s5_hex": Q_HEX,
                "class": 1,
                "category": "own_closable",
                "remaining_s6_rows": q["rows"],
                "legal_candidate_occurrences": q["occurrences"],
                "open_candidates_after_transfers": sum(int(r["open_candidates_after_transfers"]) for r in q_rows),
                "engine_win7_d10": sum(int(r["engine_win7_d10"]) for r in q_rows),
                "engine_refuted_d10": sum(int(r["engine_refuted_d10"]) for r in q_rows),
                "transferred_refuted_d10": sum(int(r["transferred_refuted_d10"]) for r in q_rows),
                "closability_rows_sterile": int(closability_by_parent[Q_HEX]["rows_sterile"]),
                "closability_rows_unswept": int(closability_by_parent[Q_HEX]["rows_unswept"]),
                "note": "The cheapest any-class own-closable parent in the current post-cost65j S5 ranking.",
            },
            "P": {
                "s5_hex": P_HEX,
                "class": 2,
                "category": "own_closable",
                "remaining_s6_rows": p["rows"],
                "legal_candidate_occurrences": p["occurrences"],
                "open_candidates_after_transfers": sum(int(r["open_candidates_after_transfers"]) for r in p_rows),
                "engine_win7_d10": sum(int(r["engine_win7_d10"]) for r in p_rows),
                "engine_refuted_d10": sum(int(r["engine_refuted_d10"]) for r in p_rows),
                "transferred_refuted_d10": sum(int(r["transferred_refuted_d10"]) for r in p_rows),
                "note": "The best own-closable class-2 parent; retained as second priority.",
            },
        },
        "family_summaries": family_summaries,
        "q_pair_graph": {
            "s6_rows": q["rows"],
            "possible_row_pairs": q["rows"] * (q["rows"] - 1) // 2,
            "observed_row_pairs": len(pair_roots),
            "missing_row_pairs": missing,
            "shared_root_orbits": q["occurrences"] - len(q["owners"]),
            "root_owner_multiplicity": q_mult,
            "pair_weight_histogram": {str(k): pair_hist[k] for k in sorted(pair_hist)},
            "maximum_weight_matching": {
                "pair_count": len(matching_audit),
                "total_alternative_weight": matching_weight,
                "alternatives_total": len(seed_rows),
                "alternatives_per_pair": [x["shared_root_orbits"] for x in matching_audit],
                "minimum_candidate_roots_to_cover_all_rows": 9,
                "seed_pairs": matching_audit,
            },
            "interpretation": "Every Q-family canonical root has one or two S6-row owners. A perfect matching gives a 9-root candidate cover of all 18 rows; this is a candidate-incidence result, not a WIN7 result.",
        },
        "cross_family": {
            "pairwise_overlap_counts": pairwise,
            "distinct_shared_root_orbits": len(cross_rows),
            "q_vs_p_overlap": pairwise["Q|P"],
            "q_vs_top4_overlap": sum(pairwise["Q|" + name] for name in FAMILY_ORDER[2:]),
            "p_vs_top4_overlap": sum(pairwise["P|" + name] for name in FAMILY_ORDER[2:]),
            "q_roots_shared_with_other_families": 0,
            "note": "Q's 687 candidate-root orbits are disjoint from P and all four coordinator top families; P shares 14 roots with top4, while top4 has two internal cross-family overlaps.",
        },
        "combined": {
            "candidate_occurrences": total_occurrences,
            "unique_d4_root_orbits": global_unique,
            "redundant_occurrences": redundant,
            "saved_pct": round(100 * redundant / total_occurrences, 3),
            "families": FAMILY_ORDER,
        },
        "trust_boundary": {
            "no_engine_search_run": True,
            "no_new_win7_d10_verdicts": 0,
            "no_new_refuted_d10_verdicts": 0,
            "no_certificate_created": True,
            "meaning": "This is exact candidate legality and D4 orbit dedup only. It does not establish any game-theoretic WIN/LOSS value or game distance.",
        },
        "status": {
            "q_family": "UNKNOWN",
            "p_family": "UNKNOWN",
            "s2_root_59_60": "UNKNOWN",
            "n11_empty_board": "UNKNOWN",
        },
    }

    cross_csv_rows = [{
        "canonical_root_hex": row["canonical_root_hex"],
        "families": ";".join(row["families"]),
        "owners_json": json.dumps(row["owners"], separators=(",", ":")),
    } for row in cross_rows]

    return {
        "audit": audit,
        "worklist_csv": csv_text(
            ["canonical_root_hex", "owner_count", "priority", "seed_pair_id", "seed_alternative_rank",
             "representative_s6_hex", "representative_bit", "owners_json"],
            q_work_rows,
        ),
        "seed_csv": csv_text(
            ["pair_id", "row_a_s6_hex", "row_b_s6_hex", "pair_weight", "alternative_rank",
             "canonical_root_hex", "is_primary"],
            seed_rows,
        ),
        "cross_csv": csv_text(
            ["canonical_root_hex", "families", "owners_json"],
            cross_csv_rows,
        ),
    }


def verify_csv(saved: str, expected: str, label: str) -> None:
    saved_rows = list(csv.reader(io.StringIO(saved)))
    expected_rows = list(csv.reader(io.StringIO(expected)))
    if saved_rows != expected_rows:
        raise AssertionError(f"{label} differs from recomputation")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write recomputed outputs instead of verifying")
    args = parser.parse_args()
    result = compute()
    OUT.mkdir(parents=True, exist_ok=True)
    outputs = {
        "audit.json": json.dumps(result["audit"], ensure_ascii=False, indent=2) + "\n",
        "q-family-canonical-root-worklist.csv": result["worklist_csv"],
        "q-family-pair-cover-seed.csv": result["seed_csv"],
        "cross-family-overlaps.csv": result["cross_csv"],
    }
    if args.write:
        for name, content in outputs.items():
            (OUT / name).write_text(content, encoding="utf-8", newline="")
        print("WROTE_Q_FAMILY_ORBIT_DEDUP")
        return
    saved_audit = json.loads((OUT / "audit.json").read_text(encoding="utf-8"))
    if saved_audit != result["audit"]:
        raise AssertionError("audit.json differs from recomputation")
    verify_csv((OUT / "q-family-canonical-root-worklist.csv").read_text(encoding="utf-8"),
               result["worklist_csv"], "Q worklist")
    verify_csv((OUT / "q-family-pair-cover-seed.csv").read_text(encoding="utf-8"),
               result["seed_csv"], "Q pair-cover seed")
    verify_csv((OUT / "cross-family-overlaps.csv").read_text(encoding="utf-8"),
               result["cross_csv"], "cross-family overlaps")
    print("Q_FAMILY_ORBIT_DEDUP_VERIFIED: 1238 -> 687; 9-pair seed; 16 cross-family overlaps")


if __name__ == "__main__":
    main()
