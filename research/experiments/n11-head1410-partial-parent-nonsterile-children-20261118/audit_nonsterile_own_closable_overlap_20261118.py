#!/usr/bin/env python3
"""Follow-up overlap audit for the non-STERILE child enumeration of the 57
partial-STERILE (cross_cover_required) head-1410 S5 parents (2026-11-18).

The published enumeration (n11-head1410-partial-parent-nonsterile-children-20261118.json,
blob 30c8fdc4e7212bafe271662d8dcf0bbbde35b63b) identified the 3,555 distinct
non-STERILE remaining S6 rows through which the 57 partial parents can still
receive depth-10 receipt evidence from their own row sets. This follow-up
computes, for each of those rows, whether it is also orbit-related to at least
one of the 114 own_closable (no_sterile) S5 parents of the same K0865 census.

The routing question answered here: how much of the partial-parent D10
candidate work sits on rows that the frontier planner would consume anyway
on the own-closable sweep path, and how many rows are partial-parent-only
candidates that no own-closable closure route ever touches.

Checks (all must pass before the new content is emitted):
  A. git blob pins of the three inputs.
  B. The 3,555 rows and the 57 parents are exactly the published sets.
  C. For every one of the 3,555 rows the number of orbit-related census
     parents re-derived here equals the published worklist open_parents
     value, and the number of related partial parents equals the published
     per-row membership.
  D. The own_closable parent set is exactly the 114 no_sterile census
     parents; no census parent is both partial and own_closable.

No engine, no float, no new verdict. REFUTED-D10 is not a LOSS proof,
STERILE is not a LOSS proof, non-STERILE is only a necessary condition for
depth-10 cover, and the 11x11 empty board, the two-stone roots {49,60}/{59,60},
S2 {59,60} and classes 1/2/4 all remain UNKNOWN.
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
ENUM = HERE / "output" / "n11-head1410-partial-parent-nonsterile-children-20261118.json"
OUT = HERE / "output" / "nonsterile-own-closable-overlap-20261118.json"

PINS = {
    "census": (str(CENSUS), "9c251da3138c5cb0516e097be5e5d0427dfaf5f0"),
    "worklist": (str(WORKLIST), "2fee1d0718547a62e346d35f5858d7913e37c097"),
    "enumeration": (str(ENUM), "30c8fdc4e7212bafe271662d8dcf0bbbde35b63b"),
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


def gitblob(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def main():
    checks = []

    def check(name, ok, detail=""):
        checks.append({"check": name, "pass": bool(ok), "detail": detail})
        return bool(ok)

    pin_ok = True
    for key, (path, expected) in PINS.items():
        data = Path(path).read_bytes()
        actual = gitblob(data)
        pin_ok = pin_ok and actual == expected
        check(f"A.pin.{key}", actual == expected, actual)
    census = json.loads(Path(PINS["census"][0]).read_text())
    rows = list(csv.DictReader(Path(PINS["worklist"][0]).open()))
    enum = json.loads(Path(PINS["enumeration"][0]).read_text())

    parents = census["open_s5_census"]
    partial_hexes = {p["hex"] for p in parents if p["classification"] == "partial_sterile"}
    own_hexes = {p["hex"] for p in parents if p["classification"] == "no_sterile"}
    rowcat = {r["s6_canonical_hex"]: r["category"] for r in rows}
    rowop = {r["s6_canonical_hex"]: int(r["open_parents"]) for r in rows}

    # B: published sets
    pub_parents = [p["hex"] for p in enum["parents_by_min_child_cost"]]
    pub_rows = set()
    pub_membership = defaultdict(set)
    for p in enum["parents_by_min_child_cost"]:
        for h, c in p["children"]:
            pub_rows.add(h)
            pub_membership[h].add(p["hex"])
    check("B.sets", set(pub_parents) == partial_hexes and len(pub_parents) == 57
          and len(pub_rows) == 3555,
          f"parents={len(pub_parents)} rows={len(pub_rows)}")

    # D: partition sanity
    check("D.parent_partition", len(own_hexes) == 114
          and not (partial_hexes & own_hexes)
          and len(partial_hexes) + len(own_hexes)
          + sum(1 for p in parents if p["classification"] == "all_remaining_sterile")
          == len(parents),
          f"partial={len(partial_hexes)} own={len(own_hexes)} total={len(parents)}")

    # join over the census parents for the 3,555 rows
    pt = []
    for p in parents:
        pm = int(p["hex"], 16)
        pt.append((p["hex"], p["classification"], [t(pm, r) for r in range(8)]))
    related = {}
    for h in sorted(pub_rows):
        rm = int(h, 16)
        rel = set()
        for ph, cls, ts in pt:
            for v in ts:
                if v & ~rm == 0:
                    rel.add(ph)
                    break
        related[h] = rel

    # C: join consistency against the published values
    c_bad = []
    for h, rel in related.items():
        n_partial = len(rel & partial_hexes)
        if not (len(rel) == rowop[h] and n_partial == len(pub_membership[h])
                and rel & partial_hexes == pub_membership[h]):
            c_bad.append(h)
    check("C.join_consistency", not c_bad, f"{len(c_bad)} bad rows of {len(related)}")

    # ---- new content ---------------------------------------------------
    own_related = {h: sorted(rel & own_hexes) for h, rel in related.items()}
    rows_own = sorted(h for h in related if own_related[h])
    rows_partial_only = sorted(h for h in related if not own_related[h])
    profile_hist = Counter((len(pub_membership[h]), len(own_related[h])) for h in related)
    per_parent = []
    for p in enum["parents_by_min_child_cost"]:
        ch = [h for h, c in p["children"]]
        k = sum(1 for h in ch if own_related[h])
        per_parent.append({
            "hex": p["hex"],
            "classes": p["classes"],
            "nonsterile_count": len(ch),
            "own_related_count": k,
            "own_share_pct": round(100.0 * k / len(ch), 1),
        })
    per_parent.sort(key=lambda e: (e["own_share_pct"], e["hex"]))
    special_profiles = [
        {"hex": s["hex"], "category": s["category"], "cost": s["cost"],
         "n_partial_parents": len(s["partial_parents"]),
         "n_own_parents": len(own_related[s["hex"]]),
         "own_parents": own_related[s["hex"]]}
        for s in enum["special_nonsterile_rows"]
    ]
    special_profiles.sort(key=lambda e: (e["cost"], e["hex"]))
    min_child_own = []
    for p in enum["parents_by_min_child_cost"]:
        h = p["min_child_hex"]
        min_child_own.append({
            "hex": p["hex"], "min_child_hex": h, "min_child_cost": p["min_child_cost"],
            "min_child_own_related": bool(own_related[h]),
        })
    n_min_own = sum(1 for e in min_child_own if e["min_child_own_related"])

    totals = {
        "distinct_nonsterile_rows": len(related),
        "rows_also_own_closable": len(rows_own),
        "rows_own_share_pct": round(100.0 * len(rows_own) / len(related), 1),
        "rows_partial_only": len(rows_partial_only),
        "parent_median_own_share_pct": sorted(e["own_share_pct"] for e in per_parent)[len(per_parent) // 2],
        "parents_with_own_related_min_child": n_min_own,
        "profile_histogram": {f"np{npo}_no{now}": c for (npo, now), c in sorted(profile_hist.items())},
    }

    result = {
        "schema": "nonsterile-own-closable-overlap-20261118-v1",
        "date": "2026-11-18",
        "lane": "n11 long-term lane, autonomous session (standard 11x11 weak-resolution)",
        "title": ("overlap of the 3,555 non-STERILE candidate rows with the 114 "
                  "own_closable S5 parents of the K0865 census"),
        "inputs": {
            "census": {"path": str(CENSUS.relative_to(REPO)), "git_blob_sha1": PINS["census"][1]},
            "worklist": {"path": str(WORKLIST.relative_to(REPO)), "git_blob_sha1": PINS["worklist"][1]},
            "enumeration": {"path": str(ENUM.relative_to(REPO)), "git_blob_sha1": PINS["enumeration"][1]},
        },
        "method": (
            "independent python orbit join (exists sigma in D4: sigma(P) subset R) over the "
            "174 census parents restricted to the published 3,555 rows; per-row "
            "related-parent counts and partial-parent memberships re-verified "
            "against the worklist open_parents column and the published "
            "enumeration before the overlap tables are emitted"
        ),
        "checks": checks,
        "all_checks_pass": all(c["pass"] for c in checks),
        "totals": totals,
        "per_parent_own_share": per_parent,
        "partial_only_rows": rows_partial_only,
        "special_row_profiles": special_profiles,
        "min_child_own_related": min_child_own,
        "interpretation_guard": (
            "own_closable sharing means the row sits on both parent types' row "
            "sets, not that any sweep is scheduled; non-STERILE is only a "
            "necessary condition for depth-10 cover (K0863); no closure, "
            "coverage or verdict claim is made here"
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
    OUT.write_text(json.dumps(result, ensure_ascii=True, indent=1, sort_keys=False) + "\n")
    n_pass = sum(1 for c in checks if c["pass"])
    print(f"checks: {n_pass}/{len(checks)} pass; all_pass={result['all_checks_pass']}")
    print(f"totals: {json.dumps(totals, sort_keys=True)}")


if __name__ == "__main__":
    main()
