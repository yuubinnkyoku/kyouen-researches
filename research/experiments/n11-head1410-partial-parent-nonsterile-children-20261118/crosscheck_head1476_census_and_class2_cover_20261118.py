#!/usr/bin/env python3
"""Independent verification-side crosscheck of the published head-1476 parent
census and class-2 candidate cover
(research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/head1476-parent-census-and-class2-cover-20261118.json).

This verifier is a third, independent implementation:
  * parent-child D4 join is computed from the ROW side (each S6 row contributes
    the D4 canonical forms of its six 5-stone subsets, matched against the
    canonical parent hex), not from the parent-side 8-image subset test used by
    the published mjs and by the original 745-check run;
  * the minimum-cover count is computed twice, once by a 2^11 subset DP that
    counts minimum covers directly and once by brute-force enumeration of all
    perfect matchings (11 excluded vertices x 945 matchings), independent of
    the published singleton/perfect-matching recursion;
  * every derived value of the published JSON (per-parent baselines for all 174
    parents, head-1476 reclassification, fully-sterile parents, class-2 ranking,
    selected-parent target rows, the full 757-root candidate table, the
    lexicographically first minimum cover, and the candidate accounting) is
    compared field by field.

Inputs are pinned by git blob SHA-1. No 7-stone search is run and no verdict is
produced. REFUTED-D10 and STERILE are not LOSS proofs.
"""
import hashlib
import json
import os
import sys

N = 11
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
EXP = "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118"

INPUTS = {
    "worklist": "research/experiments/n11-class2-lane-closability-ranking-20261116/output/class-frontier-remaining-s6-worklist-1410-20261116.csv",
    "census": "research/experiments/n11-head1410-receipt-unclosability-census-20261116/output/n11-head1410-receipt-unclosability-census-20261116.json",
    "ledger": EXP + "/output/fold-chain-ledger-1410-1476-crosscheck-20261118.json",
    "published": EXP + "/output/head1476-parent-census-and-class2-cover-20261118.json",
}
PINS = {
    "worklist": "2fee1d0718547a62e346d35f5858d7913e37c097",
    "census": "9c251da3138c5cb0516e097be5e5d0427dfaf5f0",
    "ledger": "e8785d509e8a11a37c0d03cc450455a14708c34d",
    "published": "8e870809251fdc27701518d66d6b8a65ec6798c7",
}

TRANSFORMS = [
    lambda x, y: (x, y),
    lambda x, y: (y, N - 1 - x),
    lambda x, y: (N - 1 - x, N - 1 - y),
    lambda x, y: (N - 1 - y, x),
    lambda x, y: (N - 1 - x, y),
    lambda x, y: (x, N - 1 - y),
    lambda x, y: (y, x),
    lambda x, y: (N - 1 - y, N - 1 - x),
]


def git_blob_sha1(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def read_pinned(name):
    path = os.path.join(ROOT, INPUTS[name])
    with open(path, "rb") as f:
        data = f.read()
    sha = git_blob_sha1(data)
    if sha != PINS[name]:
        raise SystemExit("%s git blob SHA mismatch: %s" % (name, sha))
    return data


def transform_mask(mask, t):
    out = 0
    for i in range(121):
        if (mask >> i) & 1:
            x, y = i % N, i // N
            qx, qy = t(x, y)
            out |= 1 << (qy * N + qx)
    return out


def canon(mask):
    best = None
    for t in TRANSFORMS:
        v = transform_mask(mask, t)
        if best is None or v < best:
            best = v
    return format(best, "032x")


def bits_of(mask):
    return [i for i in range(121) if (mask >> i) & 1]


def popcount(mask):
    return bin(mask).count("1")


def det3(a, b, c):
    x1, y1 = a % N, a // N
    x2, y2 = b % N, b // N
    x3, y3 = c % N, c // N
    A, B, C = x1 * x1 + y1 * y1, x1, y1
    D, E, F = x2 * x2 + y2 * y2, x2, y2
    G, H, I = x3 * x3 + y3 * y3, x3, y3
    return A * (E * I - F * H) - B * (D * I - F * G) + C * (D * H - E * G)


def det4(a, b, c, d):
    return det3(a, b, c) - det3(a, b, d) + det3(a, c, d) - det3(b, c, d)


CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append({"name": name, "pass": bool(ok),
                   "detail": detail if isinstance(detail, str) else json.dumps(detail)})


def classify(rows, sterile):
    if not rows:
        return "closed"
    n = sum(1 for r in rows if r["hex"] in sterile)
    if n == len(rows):
        return "all_remaining_sterile"
    return "no_sterile" if n == 0 else "partial_sterile"


def main():
    worklist_bytes = read_pinned("worklist")
    census = json.loads(read_pinned("census"))
    ledger = json.loads(read_pinned("ledger"))
    published = json.loads(read_pinned("published"))

    lines = worklist_bytes.decode("utf-8").rstrip("\r\n").split("\n")
    headers = [h.strip() for h in lines[0].split(",")]
    rows = []
    for line in lines[1:]:
        values = line.split(",")
        rows.append({h: (values[i].strip() if i < len(values) else "")
                     for i, h in enumerate(headers)})
    for r in rows:
        r["mask"] = int(r["s6_canonical_hex"], 16)
        r["hex"] = r["s6_canonical_hex"]
        r["cost"] = int(r["own_candidates_s6_s7_edge_cost"])
        r["win"] = int(r["engine_win7_d10"])
        r["refuted"] = int(r["engine_refuted_d10"])
        r["transferred"] = int(r["transferred_refuted_d10"])
        r["open_after"] = int(r["open_candidates_after_transfers"])
        r["open_parents_csv"] = int(r["open_parents"])

    row_by_hex = {r["hex"]: r for r in rows}
    parents = census["open_s5_census"]
    sterile = set(x["hex"] for x in census["sterile_row_registry"])
    closed = set(ledger["derived"]["closed_rows_66"])

    # ---- worklist-level input sanity ----
    check("worklist.rows_and_stones", len(rows) == 6438 and all(popcount(r["mask"]) == 6 for r in rows),
          {"rows": len(rows)})
    total_cost = sum(r["cost"] for r in rows)
    check("worklist.total_edge_cost", total_cost == 509109, total_cost)
    check("census.parent_count", len(parents) == 174, len(parents))
    check("census.parent_hex_is_d4_canon", all(p["hex"] == p["d4_canon"] for p in parents), "")
    check("ledger.closed_rows_unique", len(closed) == 66, len(closed))
    check("ledger.closed_rows_in_worklist", all(h in row_by_hex for h in closed), "")
    closed_rows = [row_by_hex[h] for h in closed]
    check("ledger.closed_cost_sum", sum(r["cost"] for r in closed_rows) == 509109 - 504389,
          sum(r["cost"] for r in closed_rows))
    check("ledger.closed_open_parents_sum", sum(r["open_parents_csv"] for r in closed_rows) == 12274 - 12143,
          sum(r["open_parents_csv"] for r in closed_rows))
    check("ledger.closed_sterile_intersection", len(closed & sterile) == 0, "")

    # ---- independent row-side D4 join: 5-subset canonical forms ----
    row_subset_canons = {}
    for r in rows:
        stones = bits_of(r["mask"])
        canons = set()
        for drop in range(6):
            sub = r["mask"] & ~(1 << stones[drop])
            canons.add(canon(sub))
        row_subset_canons[r["hex"]] = canons

    parent_records = {}
    base_class_counts = {"all_remaining_sterile": 0, "partial_sterile": 0, "no_sterile": 0, "closed": 0}
    head_class_counts = {"all_remaining_sterile": 0, "partial_sterile": 0, "no_sterile": 0, "closed": 0}
    base_incidences = base_sterile = head_incidences = head_sterile = 0
    for p in parents:
        pc = canon(int(p["hex"], 16))
        check("parent.canon_hex." + p["hex"], pc == p["hex"], pc)
        base = [r for r in rows if pc in row_subset_canons[r["hex"]]]
        sbase = sorted(r["hex"] for r in base if r["hex"] in sterile)
        check("parent.base.%s.rows" % p["hex"], len(base) == p["remaining_s6_orbits"], len(base))
        check("parent.base.%s.cost" % p["hex"], sum(r["cost"] for r in base) == p["remaining_s7_edge_cost"],
              sum(r["cost"] for r in base))
        check("parent.base.%s.sterile_count" % p["hex"], len(sbase) == p["sterile_refs_count"], len(sbase))
        check("parent.base.%s.sterile_exact" % p["hex"],
              sbase == sorted(x["hex"] for x in (p["sterile_refs"] or [])), "")
        current = [r for r in base if r["hex"] not in closed]
        cur_sterile = [r for r in current if r["hex"] in sterile]
        nonst = [r for r in current if r["hex"] not in sterile]
        bc, hc = classify(base, sterile), classify(current, sterile)
        base_class_counts[bc] += 1
        head_class_counts[hc] += 1
        base_incidences += len(base)
        base_sterile += len(sbase)
        head_incidences += len(current)
        head_sterile += len(cur_sterile)
        parent_records[p["hex"]] = {
            "hex": p["hex"], "classes": p["classes"],
            "base_rows": len(base), "base_cost": sum(r["cost"] for r in base),
            "base_sterile_rows": len(sbase), "base_class": bc,
            "head1476_rows": len(current), "head1476_cost": sum(r["cost"] for r in current),
            "head1476_sterile_rows": len(cur_sterile),
            "nonsterile_rows": len(nonst), "nonsterile_cost": sum(r["cost"] for r in nonst),
            "open_candidates_after_transfers": sum(r["open_after"] for r in nonst),
            "engine_win7_d10": sum(r["win"] for r in nonst),
            "engine_refuted_d10": sum(r["refuted"] for r in nonst),
            "transferred_refuted_d10": sum(r["transferred"] for r in nonst),
            "head1476_class": hc,
            "remaining_rows": sorted(r["hex"] for r in current),
        }

    check("join.baseline_totals", base_incidences == 12274 and base_sterile == 91
          and base_class_counts == {"all_remaining_sterile": 3, "partial_sterile": 57, "no_sterile": 114, "closed": 0},
          {"base_incidences": base_incidences, "base_sterile": base_sterile, "base_class_counts": base_class_counts})
    check("join.incidence_matches_worklist_column",
          sum(len([1 for p in parents if canon(int(p["hex"], 16)) in row_subset_canons[r["hex"]]])
              for r in rows) == sum(r["open_parents_csv"] for r in rows),
          {"csv_open_parents_sum": sum(r["open_parents_csv"] for r in rows)})

    # ---- head-1476 global ----
    remaining = [r for r in rows if r["hex"] not in closed]
    check("head1476.rows_cost", len(remaining) == 6372 and sum(r["cost"] for r in remaining) == 504389,
          {"rows": len(remaining), "cost": sum(r["cost"] for r in remaining)})
    check("head1476.sterile_rows_all_remain", len(sterile) == 35 and all(h in row_by_hex and h not in closed for h in sterile), "")
    check("head1476.parent_class_counts", head_class_counts == {"all_remaining_sterile": 4, "partial_sterile": 56, "no_sterile": 114, "closed": 0}, head_class_counts)
    check("head1476.incidences", head_incidences == 12143 and head_sterile == 91 and head_incidences - head_sterile == 12052,
          {"head_incidences": head_incidences, "head_sterile": head_sterile})

    newly = [v for v in parent_records.values() if v["base_class"] == "partial_sterile" and v["head1476_class"] == "all_remaining_sterile"]
    check("head1476.one_newly_fully_sterile",
          len(newly) == 1 and newly[0]["hex"] == "00000000000000801202000040000000"
          and newly[0]["head1476_rows"] == 2 and newly[0]["head1476_cost"] == 135
          and newly[0]["remaining_rows"] == ["00000000000000801202000040000400", "00000000000000801282000040000000"],
          {"newly": [v["hex"] for v in newly]})
    full_parents = sorted([v for v in parent_records.values() if v["head1476_class"] == "all_remaining_sterile"],
                           key=lambda v: (v["classes"], v["head1476_rows"]))
    check("head1476.four_fully_sterile_parents",
          [v["hex"] for v in full_parents] == ["00000000000000801202000040000000", "00000000000000801202000000200000",
                                                "00000000000000809082000000000000", "00000000020000003800000080000000"],
          [v["hex"] for v in full_parents])

    # ---- compare against the published JSON: head aggregates ----
    pub = published["derived"]
    check("published.all_pass_flag", published["all_pass"] is True and published["check_count"] == 745,
          {"check_count": published["check_count"]})
    check("published.head1410_aggregates",
          pub["head1410"] == {"worklist_rows": 6438, "total_edge_cost": 509109, "open_s5_parents": 174,
                              "parent_row_incidences": 12274, "sterile_parent_incidences": 91,
                              "effective_parent_incidences": 12183,
                              "parent_class_counts": {"all_remaining_sterile": 3, "partial_sterile": 57, "no_sterile": 114, "closed": 0}},
          "")
    pub_h1476_fields = {k: pub["head1476"][k] for k in ("globally_closed_rows", "remaining_s6_rows", "total_edge_cost",
                                                        "open_s5_parents", "parent_row_incidences",
                                                        "sterile_parent_incidences", "effective_parent_incidences",
                                                        "sterile_s6_rows", "parent_class_counts")}
    check("published.head1476_aggregates",
          pub_h1476_fields == {"globally_closed_rows": 66, "remaining_s6_rows": 6372, "total_edge_cost": 504389,
                               "open_s5_parents": 174, "parent_row_incidences": 12143, "sterile_parent_incidences": 91,
                               "effective_parent_incidences": 12052, "sterile_s6_rows": 35,
                               "parent_class_counts": {"all_remaining_sterile": 4, "partial_sterile": 56, "no_sterile": 114, "closed": 0}},
          "")
    check("published.fully_sterile_parent_tables",
          all(full_parents[i]["remaining_rows"] == pub["head1476"]["fully_sterile_parents"][i]["remaining_rows"]
              and full_parents[i]["hex"] == pub["head1476"]["fully_sterile_parents"][i]["hex"]
              for i in range(4)), "")
    check("published.newly_fully_sterile_table",
          [v["hex"] for v in newly] == [x["hex"] for x in pub["head1476"]["newly_fully_sterile_parents"]]
          and newly[0]["remaining_rows"] == pub["head1476"]["newly_fully_sterile_parents"][0]["remaining_rows"], "")

    # ---- class-2 own-closable ranking ----
    class2 = sorted([v for v in parent_records.values() if v["classes"] == 2 and v["head1476_rows"] > 0 and v["head1476_sterile_rows"] == 0],
                    key=lambda v: (v["nonsterile_cost"], v["nonsterile_rows"], v["hex"]))
    pub_ranking = pub["class2_own_closable_ranking"]
    check("ranking.top12_hexes", [v["hex"] for v in class2[:12]] == [x["hex"] for x in pub_ranking],
          [v["hex"] for v in class2[:12]])
    check("ranking.top12_fields",
          all(class2[i]["base_rows"] == pub_ranking[i]["base_rows"]
              and class2[i]["base_cost"] == pub_ranking[i]["base_cost"]
              and class2[i]["head1476_rows"] == pub_ranking[i]["head1476_rows"]
              and class2[i]["head1476_cost"] == pub_ranking[i]["head1476_cost"]
              and class2[i]["nonsterile_cost"] == pub_ranking[i]["nonsterile_cost"]
              and class2[i]["remaining_rows"] == pub_ranking[i]["remaining_rows"]
              for i in range(12)), "")

    target = class2[0]
    check("target.best_class2_own_closable",
          target["hex"] == "00000000000000403800000008000000" and target["base_rows"] == 24
          and target["base_cost"] == 1704 and target["head1476_rows"] == 11 and target["head1476_cost"] == 806,
          {"hex": target["hex"]})
    pub_sp = pub["selected_parent"]
    check("published.selected_parent_fields",
          pub_sp["hex"] == target["hex"] and pub_sp["base_rows"] == 24 and pub_sp["base_cost"] == 1704
          and pub_sp["head1476_rows"] == 11 and pub_sp["head1476_cost"] == 806 and pub_sp["sterile_rows"] == 0
          and pub_sp["open_candidates_after_transfers"] == 806
          and pub_sp["engine_win7_d10"] == 0 and pub_sp["engine_refuted_d10"] == 0
          and pub_sp["transferred_refuted_d10"] == 0, "")

    # ---- target rows: independent det4 candidate enumeration ----
    target_rows = [row_by_hex[h] for h in target["remaining_rows"]]
    root_occ = {}
    row_details = []
    for r in target_rows:
        stones = bits_of(r["mask"])
        count = 0
        for d in range(121):
            if (r["mask"] >> d) & 1:
                continue
            ok = True
            for i in range(6):
                for j in range(i + 1, 6):
                    for k in range(j + 1, 6):
                        if det4(stones[i], stones[j], stones[k], d) == 0:
                            ok = False
                            break
                    if not ok:
                        break
                if not ok:
                    break
            if ok:
                count += 1
                root = canon(r["mask"] | (1 << d))
                root_occ.setdefault(root, []).append({"row": r["hex"], "bit": d})
        check("target.row.%s.det4_count" % r["hex"], count == r["cost"], "%d / %d" % (count, r["cost"]))
        check("target.row.%s.all_open" % r["hex"],
              r["win"] == 0 and r["refuted"] == 0 and r["transferred"] == 0 and r["open_after"] == r["cost"], "")
        row_details.append({"hex": r["hex"], "candidates": count, "engine_win7_d10": r["win"],
                             "engine_refuted_d10": r["refuted"], "transferred_refuted_d10": r["transferred"],
                             "open_after_transfers": r["open_after"]})
    check("target.candidate_occurrences", sum(x["candidates"] for x in row_details) == 806, 806)
    check("published.target_s6_rows",
          all(row_details[i]["hex"] == pub_sp["target_s6_rows"][i]["hex"]
              and row_details[i]["candidates"] == pub_sp["target_s6_rows"][i]["candidates"]
              and row_details[i]["open_after_transfers"] == pub_sp["target_s6_rows"][i]["open_after_transfers"]
              and row_details[i]["engine_win7_d10"] == pub_sp["target_s6_rows"][i]["engine_win7_d10"]
              and row_details[i]["engine_refuted_d10"] == pub_sp["target_s6_rows"][i]["engine_refuted_d10"]
              and row_details[i]["transferred_refuted_d10"] == pub_sp["target_s6_rows"][i]["transferred_refuted_d10"]
              for i in range(11)), "")

    # ---- candidate root table ----
    target_hexes = set(target["remaining_rows"])
    root_table = {}
    for root, occs in root_occ.items():
        rmask = int(root, 16)
        cover = set()
        for b in bits_of(rmask):
            sub = canon(rmask & ~(1 << b))
            if sub in target_hexes:
                cover.add(sub)
        root_table[root] = {"root": root, "cover_rows": sorted(cover),
                            "occurrences": sorted(occs, key=lambda o: (o["row"], o["bit"]))}
    hist = {}
    for v in root_table.values():
        hist[len(v["cover_rows"])] = hist.get(len(v["cover_rows"]), 0) + 1
    check("target.distinct_d4_roots", len(root_table) == 757, len(root_table))
    check("target.root_coverage_histogram", hist == {1: 708, 2: 49}, hist)
    check("target.max_cover_two_rows", max(hist) == 2, max(hist))
    pub_roots = {x["root"]: x for x in pub["candidate_cover"]["all_candidate_roots"]}
    check("published.all_candidate_roots_table",
          set(pub_roots) == set(root_table) and all(
              root_table[r]["cover_rows"] == pub_roots[r]["cover_rows"]
              and root_table[r]["occurrences"] == pub_roots[r]["occurrences"] for r in root_table),
          {"pub_roots": len(pub_roots)})

    # ---- minimum cover: independent subset DP ----
    nrows = 11
    full = (1 << nrows) - 1
    row_index = {h: i for i, h in enumerate(target["remaining_rows"])}
    cover_masks = []
    for v in root_table.values():
        m = 0
        for h in v["cover_rows"]:
            m |= 1 << row_index[h]
        cover_masks.append((v["root"], m))
    INF = 99
    dp = [INF] * (1 << nrows)
    dp[0] = 0
    for root, cm in cover_masks:
        old = dp[:]
        for mask in range(1 << nrows):
            if old[mask] == INF:
                continue
            nxt = mask | cm
            if nxt == mask:
                continue
            if old[mask] + 1 < dp[nxt]:
                dp[nxt] = old[mask] + 1
    minimum = dp[full]
    check("target.minimum_cover", minimum == 6 and (nrows + 1) // 2 == 6, minimum)
    check("target.lower_bound_matches", minimum == 6, minimum)

    # count covers of size exactly `minimum` by an independent counting DP over subsets
    cnt = [[0] * (nrows + 2) for _ in range(1 << nrows)]
    cnt[0][0] = 1
    for root, cm in cover_masks:
        old = [row[:] for row in cnt]
        for mask in range(1 << nrows):
            for k in range(nrows + 1):
                c = old[mask][k]
                if not c:
                    continue
                nxt = mask | cm
                if nxt == mask:
                    continue
                cnt[nxt][k + 1] += c
    total_min_cover_count = cnt[full][minimum]

    # independent brute-force perfect-matching enumeration, split by cover shape.
    # A 6-root minimum cover of 11 rows with all roots covering <= 2 rows is either
    #   (a) 5 disjoint pairs + 1 singleton (partition cover), or
    #   (b) 6 pair roots with exactly one doubly-covered row (overlapping cover).
    pair_ways = {}
    single_ways = [0] * nrows
    for root, cm in cover_masks:
        bits = [i for i in range(nrows) if (cm >> i) & 1]
        if len(bits) == 1:
            single_ways[bits[0]] += 1
        elif len(bits) == 2:
            pair_ways[(bits[0], bits[1])] = pair_ways.get((bits[0], bits[1]), 0) + 1

    def perfect_matchings(vertices):
        if not vertices:
            yield []
            return
        first = vertices[0]
        for j in range(1, len(vertices)):
            other = vertices[j]
            rest = [v for v in vertices[1:] if v != other]
            for m in perfect_matchings(rest):
                yield [(first, other)] + m

    partition_count = 0
    matching_sum = 0
    for i in range(nrows):
        others = [v for v in range(nrows) if v != i]
        for matching in perfect_matchings(others):
            w = 1
            for a, b in matching:
                w *= pair_ways.get((a, b), 0)
            if w:
                matching_sum += w
                partition_count += w * single_ways[i]

    overlapping_count = 0
    for r in range(nrows):
        rest = [v for v in range(nrows) if v != r]
        for a in range(len(rest)):
            for b in range(a + 1, len(rest)):
                ra, rb = rest[a], rest[b]
                w1 = pair_ways.get((min(r, ra), max(r, ra)), 0)
                w2 = pair_ways.get((min(r, rb), max(r, rb)), 0)
                if not w1 or not w2:
                    continue
                pair_rest = [v for v in rest if v not in (ra, rb)]
                for matching in perfect_matchings(pair_rest):
                    w = w1 * w2
                    for x, y in matching:
                        w *= pair_ways.get((x, y), 0)
                    overlapping_count += w

    check("target.partition_minimum_cover_count", partition_count == 337020, partition_count)
    check("target.overlapping_minimum_cover_count", overlapping_count == 22590, overlapping_count)
    check("target.total_minimum_cover_count_dp", total_min_cover_count == 359610, total_min_cover_count)
    check("target.total_equals_partition_plus_overlapping",
          total_min_cover_count == partition_count + overlapping_count,
          {"partition": partition_count, "overlapping": overlapping_count, "sum": partition_count + overlapping_count})
    check("target.weighted_perfect_matchings", matching_sum == 5250, matching_sum)
    check("published.minimum_cover_count_undercounts_total",
          pub["candidate_cover"]["all_minimum_cover_sets"] == 337020
          and pub["candidate_cover"]["all_minimum_cover_sets"] != total_min_cover_count,
          {"published": 337020, "total": total_min_cover_count,
           "missing_overlapping_covers": total_min_cover_count - 337020})
    check("published.minimum_cover_other_aggregates",
          pub["candidate_cover"]["candidate_occurrences"] == 806
          and pub["candidate_cover"]["distinct_d4_canonical_7stone_roots"] == 757
          and pub["candidate_cover"]["roots_covering_one_row"] == 708
          and pub["candidate_cover"]["roots_covering_two_rows"] == 49
          and pub["candidate_cover"]["roots_covering_three_or_more_rows"] == 0
          and pub["candidate_cover"]["minimum_root_count"] == 6
          and pub["candidate_cover"]["lower_bound"] == 6
          and pub["candidate_cover"]["weighted_perfect_matchings"] == 5250, "")

    # concrete counterexample to the published "all minimum covers are disjoint
    # partitions" counting: 6 pair roots, row ...0008 doubly covered
    example_cover = [
        "00000000000000403800000008000028",
        "00000000000000403800000008004008",
        "00000000000000403800000408200000",
        "00000000000000c09002000200001000",
        "00000000010000809003000000000001",
        "00000000020001003810000008000000",
    ]
    example_union = set()
    example_cover_counts = []
    for root in example_cover:
        v = root_table.get(root)
        check("example.root_in_table." + root, v is not None, "")
        if v is None:
            continue
        example_union |= set(v["cover_rows"])
        example_cover_counts.append(len(v["cover_rows"]))
    doubly = [h for h in example_union if sum(1 for root in example_cover
                                              if h in root_table[root]["cover_rows"]) == 2]
    check("example.overlapping_minimum_cover_is_valid",
          len(example_cover) == 6 and len(example_union) == 11 and example_union == target_hexes
          and all(c == 2 for c in example_cover_counts) and doubly == ["00000000000000403800000008000008"],
          {"doubly_covered_rows": doubly})
    check("example.overlapping_cover_not_a_partition",
          sum(len(root_table[r]["cover_rows"]) for r in example_cover) == 12, "")

    # ---- lexicographically first minimum cover (independent) ----
    lex_dp = [None] * (1 << nrows)
    lex_dp[0] = []
    for root, cm in sorted(cover_masks):
        old = lex_dp[:]
        for mask in range(1 << nrows):
            if old[mask] is None:
                continue
            nxt = mask | cm
            if nxt == mask:
                continue
            cand = sorted(old[mask] + [root])
            if lex_dp[nxt] is None or len(cand) < len(lex_dp[nxt]) or (len(cand) == len(lex_dp[nxt]) and cand < lex_dp[nxt]):
                lex_dp[nxt] = cand
    my_lex_cover = lex_dp[full]
    pub_lex_roots = [x["root"] for x in pub["candidate_cover"]["lexicographically_first_minimum_cover"]]
    check("target.lex_first_minimum_cover_matches_published", my_lex_cover == pub_lex_roots, {"mine": my_lex_cover})
    cover_union = set()
    for entry in pub["candidate_cover"]["lexicographically_first_minimum_cover"]:
        v = root_table.get(entry["root"])
        check("cover.root_in_table." + entry["root"], v is not None, "")
        if v is None:
            continue
        check("cover.cover_rows_match." + entry["root"], v["cover_rows"] == entry["cover_rows"], "")
        check("cover.occurrences_match." + entry["root"], v["occurrences"] == entry["occurrences"], "")
        rm = int(entry["root"], 16)
        for o in entry["occurrences"]:
            check("cover.root_is_canon_of_row_bit." + entry["root"],
                  canon(int(o["row"], 16) | (1 << o["bit"])) == entry["root"], "")
        cover_union |= set(entry["cover_rows"])
    check("cover.six_roots_cover_all_11_rows", len(cover_union) == 11 and cover_union == target_hexes,
          {"union": len(cover_union)})

    # ---- candidate accounting ----
    cats = {}
    for r in rows:
        cats[r["category"]] = cats.get(r["category"], 0) + 1
    check("accounting.category_counts",
          cats == {"sterile": 35, "transfer_partial": 2, "win_pending": 2, "win_receipt_scheduled": 9, "unswept": 6390},
          cats)
    scheduled = [r for r in rows if r["category"] == "win_receipt_scheduled"]
    nonscheduled = [r for r in rows if r["category"] != "win_receipt_scheduled"]
    check("accounting.scheduled_rows_reserved",
          len(scheduled) == 9 and sum(r["cost"] for r in scheduled) == 635
          and all(r["win"] + r["refuted"] + r["transferred"] + r["open_after"] == 0 for r in scheduled), "")
    check("accounting.non_scheduled_identity",
          all(r["cost"] == r["win"] + r["refuted"] + r["transferred"] + r["open_after"] for r in nonscheduled), "")
    status_totals = {"engine_win7_d10": sum(r["win"] for r in rows),
                     "engine_refuted_d10": sum(r["refuted"] for r in rows),
                     "transferred_refuted_d10": sum(r["transferred"] for r in rows),
                     "open_candidates_after_transfers": sum(r["open_after"] for r in rows)}
    check("accounting.global_status_totals",
          status_totals == {"engine_win7_d10": 4, "engine_refuted_d10": 2777,
                            "transferred_refuted_d10": 18, "open_candidates_after_transfers": 505675}, status_totals)
    check("published.candidate_accounting",
          pub["candidate_accounting"]["scheduled_rows"] == 9 and pub["candidate_accounting"]["scheduled_edge_cost"] == 635
          and pub["candidate_accounting"]["non_scheduled_rows"] == 6429
          and pub["candidate_accounting"]["status_totals"] == status_totals, "")

    # ---- fold-chain bookkeeping note references the ledger finding ----
    check("published.fold_chain_bookkeeping_note",
          "cost76c" in pub["fold_chain_bookkeeping_note"] and "77e" in pub["fold_chain_bookkeeping_note"]
          and "double-count" in pub["fold_chain_bookkeeping_note"], "")

    all_pass = all(c["pass"] for c in CHECKS)
    output = {
        "schema": "n11-crosscheck-head1476-parent-census-and-class2-cover-20261118-v1",
        "date": "2026-11-18",
        "lane": "standard 11x11 weak-resolution, S2{59,60} class2 long-term lane (verification side)",
        "title": "Independent crosscheck of the published head-1476 parent census and class-2 candidate cover",
        "source_published_commit": "e652dd78b0cbd9f9f8a58f488f1c0fd6734893a9",
        "source_main_at_crosscheck": "3b307854171947aaedfcc83b5d3ea7217b92f84d",
        "inputs": {k: {"path": INPUTS[k], "git_blob_sha1": PINS[k]} for k in INPUTS},
        "method": ("Third independent implementation: row-side D4 join via the six 5-stone subset canonical forms of each S6 row "
                   "(the published records join from the parent side with 8 images); minimum-cover count by a 2^11 counting DP and "
                   "independently by brute-force enumeration of all perfect matchings (11 x 945); the full published 757-root table, "
                   "ranking, per-parent baselines for all 174 parents, and the lexicographic minimum cover are compared field by field."),
        "derived": {
            "baseline_parent_join": {"incidences": base_incidences, "sterile": base_sterile, "class_counts": base_class_counts},
            "head1476": {"rows": len(remaining), "cost": sum(r["cost"] for r in remaining),
                         "incidences": head_incidences, "sterile": head_sterile, "class_counts": head_class_counts},
            "fully_sterile_parents": [v["hex"] for v in full_parents],
            "newly_fully_sterile": [v["hex"] for v in newly],
            "class2_ranking_top12": [v["hex"] for v in class2[:12]],
            "selected_parent": target["hex"],
            "target_rows": [x["hex"] for x in row_details],
            "candidate_occurrences": 806,
            "distinct_d4_roots": len(root_table),
            "coverage_histogram": hist,
            "minimum_roots": minimum,
            "partition_minimum_cover_count": partition_count,
            "overlapping_minimum_cover_count": overlapping_count,
            "total_minimum_cover_count": total_min_cover_count,
            "weighted_perfect_matchings": matching_sum,
            "lexicographically_first_minimum_cover": my_lex_cover,
            "example_overlapping_minimum_cover": example_cover,
            "published_mjs_rerun_note": ("The published mjs (git blob da068262) was run twice cold on a reconstructed checkout of the "
                                          "pinned inputs in this same session: both runs byte-identical, 735/735 checks all PASS, and all "
                                          "headline aggregates agree with the published JSON; the published JSON itself was produced by the "
                                          "earlier 745-check version and is not byte-reproducible from the published mjs (different JSON "
                                          "schema and check naming)."),
        },
        "findings": [
            {"id": "F1",
             "severity": "counting-labeling error in the published record (planning unaffected)",
             "summary": ("The published head-1476 census claims 337,020 minimum 6-root covers "
                         "(all_minimum_cover_sets), but that number counts only the disjoint "
                         "partition-shaped covers (5 disjoint pair roots + 1 singleton root). "
                         "Minimum covers of the overlapping shape (6 pair roots with exactly one "
                         "doubly-covered row) also exist and were missed: 22,590 of them. The total "
                         "number of minimum 6-root covers is 359,610."),
             "evidence": ("2^11 counting DP over the 757 pinned roots: 359,610 covers of size 6; "
                          "independent brute-force decomposition: 337,020 partition covers "
                          "(published number) + 22,590 overlapping covers; three-way agreement. "
                          "Concrete counterexample cover (row 00000000000000403800000008000008 "
                          "doubly covered): 00000000000000403800000008000028, 00000000000000403800000008004008, "
                          "00000000000000403800000408200000, 00000000000000c09002000200001000, "
                          "00000000010000809003000000000001, 00000000020001003810000008000000."),
             "impact": ("The minimum cover size (6), the lower bound, the lexicographically first "
                        "cover, and every planning decision are unaffected: all minimum covers still "
                        "use exactly 6 roots. The published mjs check named "
                        "'candidate.minimum_cover_count' (and the original 745-check run) label the "
                        "partition count as the total minimum-cover count.")},
            {"id": "F2",
             "severity": "reproducibility note (not a computational error)",
             "summary": ("The published mjs (git blob da068262) re-derives and confirms every headline "
                         "aggregate of the published JSON when run on the pinned inputs (735/735 checks "
                         "all PASS, double run byte-identical, including 806/757/708+49/6/337,020/5,250), "
                         "but it does not byte-reproduce the published JSON: the published JSON was "
                         "produced by the earlier 745-check version with a different JSON schema and "
                         "check naming. The log's '745/745 checks' refers to that unpublished version."),
             "impact": "No substantive disagreement between the published JSON and the published mjs was found."},
        ],
        "checks": CHECKS,
        "check_count": len(CHECKS),
        "all_pass": all_pass,
        "interpretation_guard": ("Verification-side crosscheck of published records only. No 7-stone engine search was run, no new "
                                 "WIN7-D10 or REFUTED-D10 verdict was produced, no receipt was folded, and no S5 parent was closed. "
                                 "The six-root cover is a geometric candidate plan conditional on future WIN7-D10 certificates. "
                                 "REFUTED-D10 and STERILE are not LOSS proofs."),
        "unknown_status": ("Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN."),
    }
    out_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, EXP, "output", "crosscheck-head1476-parent-census-and-class2-cover-20261118.json")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(output, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"out": out_path, "all_pass": all_pass, "checks": len(CHECKS),
                      "failed": [c["name"] for c in CHECKS if not c["pass"]]}, indent=2))
    if not all_pass:
        sys.exit(1)


if __name__ == "__main__":
    main()
