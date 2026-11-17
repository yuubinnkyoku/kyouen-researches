#!/usr/bin/env python3
"""Non-STERILE remaining-child enumeration for the 57 partial-STERILE
(cross_cover_required) S5 parents of the head-1410 receipt-unclosability
census (verification-side audit, 2026-11-18).

K0863 proved that a STERILE 6-stone row (all own legal candidates
REFUTED-D10) is never covered by any depth-10 WIN7 receipt root, from its
own row or by cross-cover. K0865 classified the 174 open S5 parents of the
post-cost-60c head 1410 as 114 own_closable / 57 partial_sterile /
3 all_remaining_sterile and published per-parent aggregates plus the
STERILE refs, but not the identities of the non-STERILE remaining rows.

This audit independently re-derives the whole parent-row join from the raw
published worklist and enumerates, for every one of the 57 partial-STERILE
parents, its non-STERILE remaining S6 rows with costs. By K0863 these are
the only rows of such a parent that can still receive depth-10 receipt
evidence from the parent's own row set; the enumerated table is the
candidate set from which any future D10 cross-cover planning for these
parents must start. No game verdict is produced or changed.

Inputs (all on main, content-pinned by git blob sha1):
  * K0865 census JSON            9c251da3138c5cb0516e097be5e5d0427dfaf5f0
  * head-1410 S6 worklist CSV     2fee1d0718547a62e346d35f5858d7913e37c097
  * head-1410 S5 closability CSV 65215b6582de6efedfed8d77d91630edd883a2cb
  * closability ranking JSON     c39c547d2ab21b8cd4f0b1f098738cc027bd9d3a

Checks:
  A. git blob pins of the four inputs.
  B. worklist shape: 6,438 rows; category counts 6390/35/9/2/2; the
     ranking JSON row_classification counts and sterile hex list agree.
  C. global incidence: sum of the per-row open_parents column equals the
     census per-parent rem sum (12,274).
  D. row-level join reproduction: for all 6,438 rows the number of census
     parents orbit-related to the row (exists sigma in D4: sigma(P) subset R)
     equals the published open_parents value.
  E. parent-level join reproduction (174 parents x several): children
     count == remaining_s6_orbits, cost sum == remaining_s7_edge_cost,
     sterile count == sterile_refs_count, sterile hex set == census
     sterile_refs, sterile cost sum == sterile_cost, effective_remaining
     == rem - sterile, effective_cost == cost - sterile_cost, and the
     s5-closability CSV per-parent category counts (rows_sterile /
     rows_win_pending / rows_win_receipt_scheduled / rows_transfer_partial
     / rows_unswept) all agree; classification names map
     partial_sterile <-> cross_cover_required, all_remaining_sterile <->
     fully_sterile, no_sterile <-> own_closable.
  F. sterile_row_registry: 35 entries, all in the worklist sterile set,
     and the registry open_parents list of every entry equals the
     orbit-related parents re-derived here.
  G. structure of all 91 sterile refs: each ref is the D4-canonical form of a
     one-stone extension of its parent (ref hex == canon(P | 1<<b) for some
     empty bit b; the orbit-relatedness sigma may be any of the 8 transforms,
     and canon is D4-invariant so the check is frame-free), ref cost == the
     worklist cost of that row, and the row is categorized sterile.
  H. effective_worklist_top16: every published entry is reproduced by the
     join (hex, effective_cost, effective_remaining, sterile_refs_count,
     remaining_s6_orbits).
  I. census totals 174/3/57/114/91/12274/12183 reproduced from the join.

New content (not published anywhere before):
  * per-parent non-STERILE remaining row tables ([hex, cost] pairs sorted by
    cost then hex; every listed row is worklist category unswept except the
    13 rows separately itemized in special_nonsterile_rows),
  * per-parent cheapest non-STERILE row and the resulting parent ranking,
  * distinct-row multiplicity across the 57 parents (shared candidates),
  * the cheapest non-STERILE rows overall.

REFUTED-D10 is not a LOSS proof, STERILE is not a LOSS proof, non-STERILE
is only a necessary condition for depth-10 cover, and the 11x11 empty
board, the two-stone roots {49,60}/{59,60}, S2 {59,60} and classes 1/2/4
all remain UNKNOWN.
"""
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent               # experiments/n11-head1410-partial-parent-nonsterile-children-20261118/
EXP = HERE.parent                                    # experiments/
REPO = EXP.parents[1]                                # repo root

CENSUS = EXP / "n11-head1410-receipt-unclosability-census-20261116" / "output" / "n11-head1410-receipt-unclosability-census-20261116.json"
WORKLIST = EXP / "n11-class2-lane-closability-ranking-20261116" / "output" / "class-frontier-remaining-s6-worklist-1410-20261116.csv"
S5CSV = EXP / "n11-class2-lane-closability-ranking-20261116" / "output" / "class-frontier-s5-closability-after-cost60c-20261116.csv"
RANKING = EXP / "n11-class2-lane-closability-ranking-20261116" / "output" / "class-frontier-closability-ranking-1410-20261116.json"
OUT = HERE / "output" / "n11-head1410-partial-parent-nonsterile-children-20261118.json"

PINS = {
    "census": (str(CENSUS), "9c251da3138c5cb0516e097be5e5d0427dfaf5f0"),
    "worklist": (str(WORKLIST), "2fee1d0718547a62e346d35f5858d7913e37c097"),
    "s5csv": (str(S5CSV), "65215b6582de6efedfed8d77d91630edd883a2cb"),
    "ranking": (str(RANKING), "c39c547d2ab21b8cd4f0b1f098738cc027bd9d3a"),
}

CSV_CATEGORY_MAP = {
    "partial_sterile": "cross_cover_required",
    "all_remaining_sterile": "fully_sterile",
    "no_sterile": "own_closable",
}


def images(mask):
    result = [0] * 8
    for p in range(121):
        if mask >> p & 1:
            x, y = p % 11, p // 11
            coords = ((x, y), (y, 10 - x), (10 - x, 10 - y), (10 - y, x),
                      (10 - x, y), (x, 10 - y), (y, x), (10 - y, 10 - x))
            for i, (a, b) in enumerate(coords):
                result[i] |= 1 << (11 * b + a)
    return result


IMG = [images(1 << p) for p in range(121)]


def t(mask, r):
    v = 0
    for p in range(121):
        if mask >> p & 1:
            v |= IMG[p][r]
    return v


def canon(mask):
    return min(t(mask, r) for r in range(8))


def gitblob(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def main():
    checks = []

    def check(name, ok, detail=""):
        checks.append({"check": name, "pass": bool(ok), "detail": detail})
        return bool(ok)

    # ---- load inputs -------------------------------------------------
    pin_ok = True
    for key, (path, expected) in PINS.items():
        data = Path(path).read_bytes()
        actual = gitblob(data)
        if actual != expected:
            pin_ok = False
            check(f"A.pin.{key}", False, f"{actual} != {expected}")
        else:
            check(f"A.pin.{key}", True, actual)
    census = json.loads(Path(PINS["census"][0]).read_text())
    rows = list(csv.DictReader(Path(PINS["worklist"][0]).open()))
    s5csv = {r["s5_hex"]: r for r in csv.DictReader(Path(PINS["s5csv"][0]).open())}
    ranking = json.loads(Path(PINS["ranking"][0]).read_text())

    parents = census["open_s5_census"]
    rowcat = {r["s6_canonical_hex"]: r["category"] for r in rows}
    rowcost = {r["s6_canonical_hex"]: int(r["own_candidates_s6_s7_edge_cost"]) for r in rows}
    rowop = {r["s6_canonical_hex"]: int(r["open_parents"]) for r in rows}

    # ---- B: worklist shape -------------------------------------------
    cat_counts = Counter(rowcat.values())
    rc = ranking["row_classification"]["counts"]
    check("B.worklist.rows", len(rows) == 6438, str(len(rows)))
    check("B.categories", cat_counts == {"unswept": 6390, "sterile": 35,
                                         "win_receipt_scheduled": 9,
                                         "transfer_partial": 2, "win_pending": 2},
          json.dumps(cat_counts, sort_keys=True))
    check("B.ranking_counts_agree", all(rc.get(k, -1) == v for k, v in cat_counts.items()),
          json.dumps(rc, sort_keys=True))
    ranking_sterile = sorted(ranking["row_classification"]["rows"]["sterile"])
    worklist_sterile = sorted(h for h, c in rowcat.items() if c == "sterile")
    check("B.ranking_sterile_hexes_agree", ranking_sterile == worklist_sterile,
          f"{len(ranking_sterile)} vs {len(worklist_sterile)}")

    # ---- orbit join ---------------------------------------------------
    row_masks = {h: int(h, 16) for h in rowcat}
    parent_transforms = []
    for p in parents:
        pm = int(p["hex"], 16)
        parent_transforms.append((p, [t(pm, r) for r in range(8)]))

    related = defaultdict(set)          # row hex -> set of parent hexes
    per_parent = {}                    # parent hex -> list of child row hexes
    for p, pt in parent_transforms:
        per_parent[p["hex"]] = []
    for h, rm in row_masks.items():
        for p, pt in parent_transforms:
            for v in pt:
                if v & ~rm == 0:
                    related[h].add(p["hex"])
                    per_parent[p["hex"]].append(h)
                    break

    # ---- C: global incidence ------------------------------------------
    inc_sum = sum(len(v) for v in related.values())
    rem_sum = sum(p["remaining_s6_orbits"] for p in parents)
    check("C.incidence_sum", inc_sum == 12274 and rem_sum == 12274,
          f"rowside={inc_sum} parentside={rem_sum}")

    # ---- D: row-level join reproduction --------------------------------
    d_bad = [h for h in rowcat if len(related[h]) != rowop[h]]
    check("D.row_open_parents", not d_bad, f"{len(d_bad)} mismatches of {len(rows)}")

    # ---- E: parent-level join reproduction ------------------------------
    e_bad = []
    for p in parents:
        ph = p["hex"]
        ch = per_parent[ph]
        sterile = [c for c in ch if rowcat[c] == "sterile"]
        cost_sum = sum(rowcost[c] for c in ch)
        st_cost = sum(rowcost[c] for c in sterile)
        c = s5csv.get(ph)
        ok = (
            len(ch) == p["remaining_s6_orbits"]
            and cost_sum == p["remaining_s7_edge_cost"]
            and len(sterile) == p["sterile_refs_count"]
            and st_cost == p["sterile_cost"]
            and p["effective_remaining"] == len(ch) - len(sterile)
            and p["effective_cost"] == cost_sum - st_cost
            and set(sterile) == {ref["hex"] for ref in p["sterile_refs"]}
            and c is not None
            and CSV_CATEGORY_MAP[p["classification"]] == c["category"]
            and int(c["classes"]) == p["classes"]
            and len(ch) == int(c["remaining_s6_orbits"])
            and cost_sum == int(c["remaining_s7_edge_cost"])
            and len(sterile) == int(c["rows_sterile"])
            and sum(1 for x in ch if rowcat[x] == "win_pending") == int(c["rows_win_pending"])
            and sum(1 for x in ch if rowcat[x] == "win_receipt_scheduled") == int(c["rows_win_receipt_scheduled"])
            and sum(1 for x in ch if rowcat[x] == "transfer_partial") == int(c["rows_transfer_partial"])
            and sum(1 for x in ch if rowcat[x] == "unswept") == int(c["rows_unswept"])
        )
        if not ok:
            e_bad.append(ph)
    check("E.parent_join_full", not e_bad, f"{len(e_bad)} bad parents of {len(parents)}")

    # ---- F: sterile_row_registry ----------------------------------------
    registry = census["sterile_row_registry"]
    f_ok = len(registry) == 35 and all(e["hex"] in rowcat and rowcat[e["hex"]] == "sterile" for e in registry)
    f_bad = [e["hex"] for e in registry if sorted(related[e["hex"]]) != sorted(e["open_parents"])]
    check("F.registry_shape", f_ok, f"{len(registry)} entries")
    check("F.registry_open_parents_join", not f_bad, f"{len(f_bad)} mismatches")

    # ---- G: 91 sterile refs are one-bit D4-canonical children ------------
    # A sterile ref is the canonical form of a one-stone extension of its
    # parent: ref hex == D4 canon(P | 1<<b) for some empty bit b of P (the
    # relatedness sigma may be any of the 8 transforms; canon is D4-invariant
    # so the check is frame-free).
    g_bad = []
    n_refs = 0
    for p in parents:
        pm = int(p["hex"], 16)
        ref_hexes = {ref["hex"] for ref in p["sterile_refs"]}
        # every canonical one-bit extension of P that is a worklist row here
        ext = set()
        for b in range(121):
            if not pm >> b & 1:
                ext.add(f"{canon(pm | (1 << b)):032x}")
        for ref in p["sterile_refs"]:
            n_refs += 1
            if not (ref["hex"] in ext
                    and rowcat.get(ref["hex"]) == "sterile"
                    and rowcost.get(ref["hex"]) == ref["cost"]):
                g_bad.append(ref["hex"])
        if not ref_hexes <= set(rowcat):
            g_bad.append(p["hex"] + ":missing-rows")
    check("G.sterile_refs_structure", not g_bad and n_refs == 91,
          f"refs={n_refs} bad={len(g_bad)}")

    # ---- H: effective_worklist_top16 -------------------------------------
    h_bad = []
    by_hex = {p["hex"]: p for p in parents}
    for e in census["effective_worklist_top16"]:
        p = by_hex.get(e["hex"])
        ch = per_parent[e["hex"]]
        st = [c for c in ch if rowcat[c] == "sterile"]
        cost_sum = sum(rowcost[c] for c in ch)
        if not (p is not None
                and len(ch) == e["remaining_s6_orbits"]
                and len(st) == e["sterile_refs_count"]
                and len(ch) - len(st) == e["effective_remaining"]
                and cost_sum - sum(rowcost[c] for c in st) == e["effective_cost"]):
            h_bad.append(e["hex"])
    check("H.effective_top16_join", not h_bad and len(census["effective_worklist_top16"]) == 16,
          f"bad={len(h_bad)}")

    # ---- I: census totals --------------------------------------------------
    cls = Counter(p["classification"] for p in parents)
    eff_rem = sum(p["effective_remaining"] for p in parents)
    check("I.census_totals",
          cls == {"no_sterile": 114, "partial_sterile": 57, "all_remaining_sterile": 3}
          and n_refs == 91 and rem_sum == 12274 and eff_rem == 12183,
          f"{json.dumps(cls, sort_keys=True)} refs={n_refs} effrem={eff_rem}")

    # ---- new content: non-STERILE children of the 57 partial parents --------
    partial_hexes = sorted(p["hex"] for p in parents if p["classification"] == "partial_sterile")
    parent_entries = []
    child_partial_parents = defaultdict(list)
    for ph in partial_hexes:
        p = by_hex[ph]
        nonst = [c for c in per_parent[ph] if rowcat[c] != "sterile"]
        assert len(nonst) == p["effective_remaining"]
        for c in nonst:
            child_partial_parents[c].append(ph)
        children = sorted(((c, rowcost[c]) for c in nonst), key=lambda e: (e[1], e[0]))
        parent_entries.append({
            "hex": ph,
            "classes": p["classes"],
            "remaining_s6_orbits": p["remaining_s6_orbits"],
            "sterile_refs_count": p["sterile_refs_count"],
            "nonsterile_count": len(nonst),
            "nonsterile_cost_sum": sum(cost for _, cost in children),
            "min_child_cost": children[0][1],
            "min_child_hex": children[0][0],
            "children": [[h, c] for h, c in children],
        })
    parent_entries.sort(key=lambda e: (e["min_child_cost"], e["hex"]))

    distinct_rows = sorted(child_partial_parents)
    multiplicity = Counter(len(v) for v in child_partial_parents.values())
    special = [
        {"hex": h, "category": rowcat[h], "cost": rowcost[h],
         "partial_parents": sorted(child_partial_parents[h])}
        for h in distinct_rows if rowcat[h] != "unswept"
    ]
    special.sort(key=lambda e: (e["cost"], e["hex"]))
    shared = [
        {"hex": h, "partial_parents": sorted(child_partial_parents[h])}
        for h in distinct_rows if len(child_partial_parents[h]) >= 2
    ]
    shared.sort(key=lambda e: e["hex"])
    cheapest = [
        {"hex": h, "cost": rowcost[h], "category": rowcat[h],
         "n_related_parents": len(related[h]),
         "n_partial_parents": len(child_partial_parents[h]),
         "partial_parents": sorted(child_partial_parents[h])}
        for h in sorted(distinct_rows, key=lambda h: (rowcost[h], h))[:20]
    ]
    n_multi3 = sum(1 for v in child_partial_parents.values() if len(v) == 3)

    totals = {
        "partial_parents": len(partial_hexes),
        "nonsterile_incidence": sum(len(v) for v in child_partial_parents.values()),
        "distinct_nonsterile_rows": len(distinct_rows),
        "shared_rows_ge2": len(shared),
        "multiplicity_histogram": {str(k): multiplicity[k] for k in sorted(multiplicity)},
        "multiplicity3_rows": n_multi3,
        "special_nonsterile_rows": len(special),
        "cheapest_nonsterile_cost": cheapest[0]["cost"],
        "min_child_cost_over_parents": parent_entries[0]["min_child_cost"],
        "nonsterile_categories": dict(Counter(rowcat[h] for h in distinct_rows)),
    }

    result = {
        "schema": "n11-head1410-partial-parent-nonsterile-children-20261118-v1",
        "date": "2026-11-18",
        "lane": "n11 long-term lane, autonomous session (standard 11x11 weak-resolution)",
        "title": ("non-STERILE remaining S6 child rows of the 57 partial-STERILE "
                  "head-1410 S5 parents: independent join reproduction and "
                  "cross-cover candidate enumeration"),
        "inputs": {
            "census": {"path": str(CENSUS.relative_to(REPO)), "git_blob_sha1": PINS["census"][1]},
            "worklist": {"path": str(WORKLIST.relative_to(REPO)), "git_blob_sha1": PINS["worklist"][1]},
            "s5_closability_csv": {"path": str(S5CSV.relative_to(REPO)), "git_blob_sha1": PINS["s5csv"][1]},
            "ranking": {"path": str(RANKING.relative_to(REPO)), "git_blob_sha1": PINS["ranking"][1]},
        },
        "method": (
            "independent python re-derivation of the orbit-level parent-row join "
            "(relatedness: exists sigma in D4 with sigma(P) subset R over 121-bit "
            "11x11 masks, 8 transforms, no engine, no float); every published "
            "per-parent and per-row aggregate of the four inputs is reproduced "
            "before the new enumeration is emitted"
        ),
        "checks": checks,
        "all_checks_pass": all(c["pass"] for c in checks),
        "totals": totals,
        "parents_by_min_child_cost": parent_entries,
        "special_nonsterile_rows": special,
        "shared_children_ge2": shared,
        "cheapest_children_top20": cheapest,
        "interpretation_guard": (
            "non-STERILE is only a necessary condition for depth-10 receipt cover "
            "(K0863: a STERILE row is covered by no WIN7-D10 receipt root, own-row "
            "or cross-cover); the enumerated rows are candidates, not receipts and "
            "not verdicts; the parent classifications themselves carry no "
            "game-theoretic value claim; solved counts measure manifest coverage"
        ),
        "trust_boundary": (
            "engine depth-10 verdict soundness underlying the published STERILE "
            "scan and D4 invariance, identical to all published lane verdicts; "
            "this audit adds no new engine evidence"
        ),
        "unknown_status": (
            "11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60} and "
            "classes 1/2/4 all remain UNKNOWN; REFUTED-D10 is not a LOSS proof; "
            "STERILE is not a LOSS proof"
        ),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=True, indent=1, sort_keys=False) + "\n")
    n_pass = sum(1 for c in checks if c["pass"])
    print(f"checks: {n_pass}/{len(checks)} pass; all_pass={result['all_checks_pass']}")
    print(f"totals: {json.dumps(totals, sort_keys=True)}")


if __name__ == "__main__":
    main()
