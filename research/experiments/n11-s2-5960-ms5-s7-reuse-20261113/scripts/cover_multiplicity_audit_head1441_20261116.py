#!/usr/bin/env python3
"""Cover-multiplicity / secured-coverage audit of the canonical head 1441
(2026-11-16), built on the same independent whole-chain reconstruction as
independent_cost64g_bit89_fold_agreement_20261116.py: solved set = winners
(498 WIN7 sweep-covered s6 orbits from win7-reuse-hits.csv.gz) UNION
covers(761 published receipt roots).  The bit-89 fold receipt (cost-64g,
root 00000000020100003800000008080000, commit f14f8bdb) is applied and the
resulting head must equal 1441/174/6407/506945/4680/370859 exactly.

For every manifest s6 orbit in the solved set, this script measures how
many independent published receipts cover it (cover multiplicity), how
many orbits are covered by exactly one receipt (single-cover orbits) and
each receipt root's exclusive contribution (the manifest orbits that
would fall out of the solved set if that one receipt were removed).
This quantifies the redundancy of the proof basis; it does not change any
verdict.  Interpretation guard: solved counts measure manifest coverage,
not the game-theoretic value of any position; 11x11 empty board,
two-stone roots {49,60}/{59,60}, S2 {59,60} and classes 1/2/4 remain
UNKNOWN.
"""
import csv, gzip, json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
MS5 = HERE.parent / "n11-s2-5960-milestone5-20261112" / "output"

def images(mask):
    result = [0] * 8
    for p in range(121):
        if mask >> p & 1:
            x, y = p % 11, p // 11
            coords = ((x,y), (y,10-x), (10-x,10-y), (10-y,x),
                      (10-x,y), (x,10-y),(y,x),(10-y,10-x))
            for i, (a,b) in enumerate(coords):
                result[i] |= 1 << (11*b+a)
    return result

IMG = [images(1 << p) for p in range(121)]

def canon(mask):
    best = None
    for r in range(8):
        v = 0
        for p in range(121):
            if mask >> p & 1:
                v |= IMG[p][r]
        if best is None or v < best:
            best = v
    return best

def covers(root):
    return {canon(root ^ (1 << i)) for i in range(121) if root >> i & 1}

def popcount(x): return bin(x).count("1")

def extract_roots(obj, acc):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("root_hex", "root") and isinstance(v, str):
                x = int(v, 16)
                if popcount(x) == 7: acc.add(x)
            elif k == "roots" and isinstance(v, list):
                for e in v:
                    if isinstance(e, str):
                        x = int(e, 16)
                        if popcount(x) == 7: acc.add(x)
            elif isinstance(v, (dict, list)):
                extract_roots(v, acc)
    elif isinstance(obj, list):
        for e in obj:
            extract_roots(e, acc)

BASE_WIN7_ONLY = {
    "priority-certificates-verified.json",
    "class2-certificates-verified.json",
    "class2-next-certificates-verified.json",
    "class2-next2-certificates-verified.json",
    "class2-next3-certificates-verified.json",
    "class2-next4-certificates-verified.json",
    "class2-batch5-certificates-verified.json",
    "class2-batch3-certificates-verified.json",
    "class2-batch2-certificates-verified.json",
    "class2-batch2b-certificates-verified.json",
    "class2-batch1-certificates-verified.json",
    "class2-batch1b-certificates-verified.json",
    "class4-batch1-certificates-verified.json",
    "class4-batch2-certificates-verified.json",
    "class4-batch3-bit37-certificate.json",
    "class4-batch3-win7-certificates-20261114.json",
    "class4-batch3-win7-certificates-child5-20261114.json",
    "class4-batch3-win7-certificates-child7-20261114.json",
    "class2-lane-cost58-win7-certificates-20261114.json",
    "class2-lane-cost60-win7-certificates-20261114.json",
    "class2-lane-cost61-win7-certificates-20261114.json",
    "class2-lane-cost61b-win7-certificates-20261114.json",
    "class2-lane-cost64-win7-certificates-20261114.json",
    "class2-lane-cost65-win7-certificates-20261114.json",
    "class2-lane-cost68-win7-certificates-20261114.json",
    "class2-lane-cost75-win7-certificates-20261114.json",
}

def extract_win7_roots(obj, acc):
    """Base certificate files: records with verdict WIN7* (or no verdict,
    for the win7-certificates manifests whose records are all WIN7)."""
    if isinstance(obj, dict):
        certs = None
        if "certificates" in obj and isinstance(obj["certificates"], list):
            certs = obj["certificates"]
        elif "verdict" in obj:
            certs = [obj]
        if certs is not None:
            for c in certs:
                if isinstance(c, dict):
                    v = c.get("verdict")
                    if v is not None and not str(v).startswith("WIN7"):
                        continue
                    for k in ("root", "root_hex"):
                        if k in c and isinstance(c[k], str):
                            x = int(c[k], 16)
                            if popcount(x) == 7:
                                acc.add(x)
            return
        for v in obj.values():
            if isinstance(v, (dict, list)):
                extract_win7_roots(v, acc)
    elif isinstance(obj, list):
        for e in obj:
            extract_win7_roots(e, acc)

roots = set()
for name in sorted(BASE_WIN7_ONLY):
    extract_win7_roots(json.loads((OUT / name).read_text()), roots)
for p in sorted(OUT.glob("class-frontier-*.json")):
    extract_roots(json.loads(p.read_text()), roots)
for name in ("class2-lane-cost63cd-frontier-recompute-20261114.json",
             "class2-lane-cost65c-frontier-recompute-20261114.json",
             "class2-lane-cost65d-frontier-recompute-20261114.json",
             "class2-lane-cost75-frontier-recompute-20261114.json",
             "class4-lane-cost78b-frontier-recompute-20261114.json",
             "class4-lane-cost80b-frontier-recompute-20261114.json"):
    extract_roots(json.loads((OUT / name).read_text()), roots)
print(f"receipt roots: {len(roots)} distinct")

manifest = {}
for path in sorted(MS5.glob("ms5_s6_manifest_part*.csv")):
    with path.open(newline="") as f:
        for row in csv.DictReader(f):
            manifest[int(row["hex"], 16)] = (int(row["cost"]), int(row["classes"]))
print(f"manifest rows: {len(manifest)}")

winners = set()
with gzip.open(OUT / "win7-reuse-hits.csv.gz", "rt", newline="") as f:
    for row in csv.DictReader(f):
        winners.add(int(row["s6_hex"], 16))
print(f"winners: {len(winners)}")

# ---- solved sets ----
# bit-89 fold receipt (cost-64g WIN7-D10, independently verified certificate
# git blob 1d2cc167, parallel fold receipt f14f8bdb) is a NEW receipt on top
# of the 1438-basis roots; at head 1441 the receipt basis is roots + ROOT89.
CHILD = int("00000000000100003800000008080000", 16)
ROOT89 = CHILD | (1 << 89)
assert popcount(ROOT89) == 7 and ROOT89 not in roots
solved = set(winners)
for r in roots:
    solved |= covers(r)
covered1438 = solved & set(manifest)
assert len(covered1438) == 1438, len(covered1438)

roots1441 = roots | {ROOT89}
solved1441 = solved | covers(ROOT89)
covered1441 = solved1441 & set(manifest)

# ---- multiplicity over manifest orbits in solved1441 ----
orbit_cover_roots = defaultdict(list)   # canon -> [root ints]
for r in roots1441:
    for c in covers(r):
        orbit_cover_roots[c].append(r)

mult_hist = defaultdict(int)
single_cover = []   # (canon, root) pairs, manifest-only orbits
winner_only = []
for c in covered1441:
    m = len(orbit_cover_roots.get(c, []))
    if m == 0 and c in winners:
        winner_only.append(c)
    else:
        mult_hist[m + (1 if c in winners else 0)] += 1
        if m == 1 and c not in winners:
            single_cover.append((c, orbit_cover_roots[c][0]))

# ---- exclusive contribution of each receipt root (at head 1441) ----
root_exclusive = {}
for r in sorted(roots1441):
    excl = [c for c in covers(r)
            if c in manifest and c in covered1441
            and len(orbit_cover_roots.get(c, [])) == 1
            and orbit_cover_roots[c][0] == r and c not in winners]
    if excl:
        root_exclusive[f"{r:032x}"] = {
            "exclusive_manifest_orbits": len(excl),
            "exclusive_hexes": [f"{c:032x}" for c in sorted(excl)],
            "exclusive_cost_sum": sum(manifest[c][0] for c in excl),
        }

top_exclusive = sorted(root_exclusive.items(),
                       key=lambda kv: kv[1]["exclusive_manifest_orbits"],
                       reverse=True)

# ---- winners-only orbits: solved solely by sweep WIN7 coverage ----
# (these are rows whose closure is provided by published WIN7 sweep verdicts
#  rather than by any 7-stone receipt root's covers)

result = {
    "schema": "n11-class2-lane-head1441-cover-multiplicity-audit-20261116-v1",
    "date": "2026-11-16",
    "method": ("independent reconstruction (same inputs and verbatim frontier "
               "semantics as independent_cost64g_bit89_fold_agreement_20261116."
               "py): solved = winners(498) UNION covers(761 published receipt "
               "roots); bit-89 fold receipt applied; manifest-orbit cover "
               "multiplicity and per-root exclusive contribution measured"),
    "head_control": {
        "receipt_roots_1438_basis": len(roots),
        "receipt_roots_1441_basis": len(roots1441),
        "winners": len(winners),
        "covered1438": len(covered1438),
        "covered1441": len(covered1441),
        "expected_1441": 1441,
        "match": len(covered1441) == 1441,
    },
    "multiplicity_histogram_manifest_orbits": {
        "winner_only_sweep_covered": len(winner_only),
        **{f"receipt_covered_mult_{k}": v for k, v in sorted(mult_hist.items())},
    },
    "single_cover_orbits": {
        "count": len(single_cover),
        "cost_sum": sum(manifest[c][0] for c, _ in single_cover),
        "orbits": [
            {"s6_hex": f"{c:032x}", "cost": manifest[c][0],
             "classes": manifest[c][1], "sole_receipt_root": f"{r:032x}"}
            for c, r in sorted(single_cover)
        ],
    },
    "roots_with_exclusive_contribution": len(root_exclusive),
    "top_exclusive_roots": [
        {"root_hex": k, **v} for k, v in top_exclusive[:20]
    ],
    "interpretation_guard": ("bookkeeping over published receipts; solved "
        "counts measure manifest coverage, not the game-theoretic value of "
        "any position; WIN7 certificates prove a first-player win within "
        "depth 10 from individual 7-stone roots only; 11x11 empty board, "
        "two-stone roots {49,60}/{59,60}, S2 {59,60} and classes 1/2/4 "
        "remain UNKNOWN"),
}

with open(OUT / "class2-lane-head1441-cover-multiplicity-audit-20261116.json", "w") as f:
    json.dump(result, f, indent=1, sort_keys=True)
    f.write("\n")

print("head control:", result["head_control"])
print("mult histogram:", result["multiplicity_histogram_manifest_orbits"])
print("single-cover orbits:", len(single_cover),
      "cost sum:", result["single_cover_orbits"]["cost_sum"])
print("roots with exclusive contribution:", len(root_exclusive))
for k, v in top_exclusive[:5]:
    print("  top:", k, v["exclusive_manifest_orbits"], "orbits")
