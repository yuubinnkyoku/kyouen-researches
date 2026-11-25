#!/usr/bin/env python3
"""Preregistered head-1472 cover-multiplicity audit PREDICTION for the class2
lane (2026-11-16), published BEFORE the cost64h fold receipt lands on main.

This extends the head-1441 audit (cover_multiplicity_audit_head1441_20261116.py,
git blob fbafd1e1) to the post-fold head. The receipt basis is reconstructed
verbatim from the local output directory (same extraction semantics as the
head-1441 audit and the cost64h fold preregistration, which was independently
agreed 12/12 by the second-implementation lane at commit 0330d83d), asserted to
be the head-1452 basis (775 receipt roots, solved 1452), then the 23 cost64h
WIN7-D10 certificate roots (child 00000000000000403800000008100000 | 1<<bit,
all four-way independently verified this session) are added and the resulting
head must equal the preregistration projection 1472/174/6376/504672/4649/
368586. The multiplicity histogram, single-cover orbits and per-root exclusive
contributions at head 1472 are then measured exactly as in the head-1441
audit, producing the PREDICTED audit values the post-fold audit must
reproduce when the fold receipt lands.

Interpretation guard: bookkeeping over published and preregistered receipts
only; no engine search was run and no verdict was created; solved counts
measure manifest coverage, not the game-theoretic value of any position; the
11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60} and classes
1/2/4 remain UNKNOWN.
"""
import csv, gzip, json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
MS5 = HERE.parent / "n11-s2-5960-milestone5-20261112" / "output"

WIN_BITS = [4, 6, 8, 33, 38, 42, 44, 49, 68, 74, 76, 77, 78, 79, 83, 89, 91,
            101, 109, 113, 114, 116, 120]
CHILD_HEX = "00000000000000403800000008100000"
CHILD = int(CHILD_HEX, 16)
EXPECTED_BASIS_ROOTS = 775
EXPECTED_COVERED_1452 = 1452
EXPECTED_COVERED_1472 = 1472
EXPECTED_PROJECTED_HEAD = [1472, 174, 6376, 504672, 4649, 368586]

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
                if popcount(x) == 7:
                    acc.add(x)
            elif k == "roots" and isinstance(v, list):
                for e in v:
                    if isinstance(e, str):
                        x = int(e, 16)
                        if popcount(x) == 7:
                            acc.add(x)
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

# ---- basis (head 1452) ----
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
assert len(roots) == EXPECTED_BASIS_ROOTS, len(roots)

manifest = {}
for path in sorted(MS5.glob("ms5_s6_manifest_part*.csv")):
    with path.open(newline="") as f:
        for row in csv.DictReader(f):
            manifest[int(row["hex"], 16)] = (int(row["cost"]), int(row["classes"]))

winners = set()
with gzip.open(OUT / "win7-reuse-hits.csv.gz", "rt", newline="") as f:
    for row in csv.DictReader(f):
        winners.add(int(row["s6_hex"], 16))

solved1452 = set(winners)
for r in roots:
    solved1452 |= covers(r)
covered1452 = solved1452 & set(manifest)
assert len(covered1452) == EXPECTED_COVERED_1452, len(covered1452)

# ---- fold: 23 cost64h WIN7-D10 certificate roots ----
cert_roots = {}
for b in WIN_BITS:
    r = CHILD | (1 << b)
    assert popcount(r) == 7, b
    assert r not in roots, f"bit {b} root already in basis"
    cert_roots[b] = r
assert len(set(cert_roots.values())) == 23

roots1472 = roots | set(cert_roots.values())
solved1472 = solved1452
newly = set()
for b in WIN_BITS:
    cv = covers(cert_roots[b]) & set(manifest)
    newly |= cv
    solved1472 |= cv
covered1472 = solved1472 & set(manifest)
assert len(covered1472) == EXPECTED_COVERED_1472, len(covered1472)
marginal_in_manifest = len(newly - covered1452)
assert marginal_in_manifest == 20, marginal_in_manifest

# ---- multiplicity over manifest orbits in solved1472 ----
orbit_cover_roots = defaultdict(list)
for r in roots1472:
    for c in covers(r):
        orbit_cover_roots[c].append(r)

mult_hist = defaultdict(int)
single_cover = []
winner_only = []
for c in covered1472:
    m = len(orbit_cover_roots.get(c, []))
    if m == 0 and c in winners:
        winner_only.append(c)
    else:
        mult_hist[m + (1 if c in winners else 0)] += 1
        if m == 1 and c not in winners:
            single_cover.append((c, orbit_cover_roots[c][0]))

# ---- exclusive contribution of each receipt root (at head 1472) ----
root_exclusive = {}
for r in sorted(roots1472):
    excl = [c for c in covers(r)
            if c in manifest and c in covered1472
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

# ---- per-receipt marginal detail for the 23 cost64h roots ----
per_receipt = []
for b in WIN_BITS:
    r = cert_roots[b]
    cv = covers(r)
    cvm = cv & set(manifest)
    per_receipt.append({
        "bit": b,
        "root_hex": f"{r:032x}",
        "covers": len(cv),
        "covers_in_manifest": len(cvm),
        "marginal_in_manifest_at_1452": len(cvm - covered1452),
        "marginal_hexes": sorted(f"{c:032x}" for c in cvm - covered1452),
    })

result = {
    "schema": "n11-class2-lane-head1472-cover-multiplicity-audit-prediction-20261116-v1",
    "date": "2026-11-16",
    "role": ("preregistered PREDICTION of the head-1472 cover-multiplicity audit, "
             "published before the cost64h fold receipt lands; the post-fold audit "
             "must reproduce these values (or record the discrepancy as an "
             "experimental fact)"),
    "method": ("verbatim frontier extraction of the head-1452 receipt basis "
               "(775 roots, asserted; same semantics as the head-1441 audit and "
               "the independently agreed fold preregistration), plus the 23 "
               "cost64h WIN7-D10 certificate roots (child|1<<bit, four-way "
               "independently verified this session); solved = winners UNION "
               "covers(receipt roots)"),
    "head_control": {
        "receipt_roots_1452_basis": len(roots),
        "receipt_roots_1472_basis": len(roots1472),
        "winners": len(winners),
        "covered_1452": len(covered1452),
        "expected_1452": EXPECTED_COVERED_1452,
        "covered_1472": len(covered1472),
        "expected_1472": EXPECTED_COVERED_1472,
        "projected_head_numbers": EXPECTED_PROJECTED_HEAD,
        "match": len(covered1472) == EXPECTED_COVERED_1472,
        "marginal_in_manifest": marginal_in_manifest,
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
    "cost64h_receipts": per_receipt,
    "interpretation_guard": ("bookkeeping over published and preregistered "
        "receipts only; no engine search was run and no verdict was created; "
        "solved counts measure manifest coverage, not the game-theoretic value "
        "of any position; WIN7 certificates prove a first-player win within "
        "depth 10 from individual 7-stone roots only; 11x11 empty board, "
        "two-stone roots {49,60}/{59,60}, S2 {59,60} and classes 1/2/4 remain "
        "UNKNOWN"),
}

with open(OUT / "class2-lane-head1472-cover-multiplicity-audit-prediction-20261116.json", "w") as f:
    json.dump(result, f, indent=1, sort_keys=True)
    f.write("\n")
print(json.dumps(result["head_control"], indent=1))
print("winner_only:", len(winner_only), "single_cover:", len(single_cover),
      "exclusive roots:", len(root_exclusive))
