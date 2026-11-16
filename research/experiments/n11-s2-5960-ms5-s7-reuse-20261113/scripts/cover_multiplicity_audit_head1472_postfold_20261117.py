#!/usr/bin/env python3
"""Post-fold head-1472 cover-multiplicity audit for the class2 lane
(2026-11-17), executed AFTER the cost64h fold receipt landed on main.

This is the post-fold counterpart of the preregistered PREDICTION
(cover_multiplicity_audit_head1472_prediction_20261116.py, prediction JSON
git blob from commit d4f5044f, published before the fold receipt landed).
Semantics are verbatim from the head-1441 audit (fbafd1e1) and the
prediction script:

- the head-1452 receipt basis is reconstructed verbatim from the published
  output files (same extraction semantics, same file set as the prediction,
  excluding the landed cost64h fold receipt itself from the glob so the
  basis stays the pre-fold 775 roots), asserted to give 775 roots and
  covered 1452;
- the 23 cost64h WIN7-D10 receipt roots are now taken FROM THE LANDED FOLD
  RECEIPT (class-frontier-cost64h-receipts-recompute-20261117.json, git blob
  1633be292f6f1862c895009eac29d398d0be7738, commit 828c595c), asserting
  root_hex == child|1<<bit and popcount 7, instead of being derived from
  the sweep;
- the post-fold audit values (head control, multiplicity histogram,
  single-cover orbits, exclusive contributions, per-receipt marginal
  detail) are computed exactly as in the prediction and compared
  field-by-field against the prediction JSON; every field must reproduce
  the predicted value (or the discrepancy is recorded as an experimental
  fact and fails the audit).

Interpretation guard: bookkeeping over published receipts only; no engine
search was run and no verdict was created; solved counts measure manifest
coverage, not the game-theoretic value of any position; WIN7 certificates
prove a first-player win within depth 10 from individual 7-stone roots
only; REFUTED-D10 is not a LOSS proof; the 11x11 empty board, the
two-stone roots {49,60}/{59,60}, S2 {59,60} and classes 1/2/4 remain
UNKNOWN.
"""
import csv, gzip, json, hashlib
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
MS5 = HERE.parent / "n11-s2-5960-milestone5-20261112" / "output"

CHILD_HEX = "00000000000000403800000008100000"
CHILD = int(CHILD_HEX, 16)
EXPECTED_BASIS_ROOTS = 775
EXPECTED_COVERED_1452 = 1452
EXPECTED_COVERED_1472 = 1472
EXPECTED_PROJECTED_HEAD = [1472, 174, 6376, 504672, 4649, 368586]

FOLD_RECEIPT = "class-frontier-cost64h-receipts-recompute-20261117.json"
FOLD_RECEIPT_BLOB = "1633be292f6f1862c895009eac29d398d0be7738"
PREDICTION = "class2-lane-head1472-cover-multiplicity-audit-prediction-20261116.json"


def git_blob_sha(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


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


def popcount(x):
    return bin(x).count("1")


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


# ---- inputs with blob pins ----
fold_data = (OUT / FOLD_RECEIPT).read_bytes()
assert git_blob_sha(fold_data) == FOLD_RECEIPT_BLOB, "fold receipt blob"
fold = json.loads(fold_data.decode())
prediction = json.loads((OUT / PREDICTION).read_text())

# ---- basis (head 1452): same file set as the prediction, minus the landed
# cost64h fold receipt (its 23 roots enter via the receipts instead) ----
roots = set()
for name in sorted(BASE_WIN7_ONLY):
    extract_win7_roots(json.loads((OUT / name).read_text()), roots)
for p in sorted(OUT.glob("class-frontier-*.json")):
    if p.name == FOLD_RECEIPT:
        continue
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

# ---- fold: 23 receipt roots taken from the LANDED fold receipt ----
fold_receipts = fold["receipts"]
assert len(fold_receipts) == 23, len(fold_receipts)
cert_roots = {}
for r in fold_receipts:
    b = r["bit"]
    x = int(r["root_hex"], 16)
    assert x == CHILD | (1 << b), (b, r["root_hex"])
    assert popcount(x) == 7, b
    assert x not in roots, f"bit {b} root already in basis"
    cert_roots[b] = x
assert len(set(cert_roots.values())) == 23

roots1472 = roots | set(cert_roots.values())
solved1472 = solved1452
newly = set()
for b in sorted(cert_roots):
    cv = covers(cert_roots[b]) & set(manifest)
    newly |= cv
    solved1472 |= cv
covered1472 = solved1472 & set(manifest)
assert len(covered1472) == EXPECTED_COVERED_1472, len(covered1472)
marginal_in_manifest = len(newly - covered1452)
assert marginal_in_manifest == 20, marginal_in_manifest

# cross-check against the landed receipt's own frontier numbers
fa = fold["frontier_after_cost64h"]
SUMMARY_KEYS = ("solved_s6_in_manifest", "remaining_s5_orbits",
                "unique_remaining_s6", "sum_remaining_cost",
                "s6_needed_by_open_classes", "cost_needed_by_open_classes")
fold_numbers = [fa[k] for k in SUMMARY_KEYS]
assert fold_numbers == EXPECTED_PROJECTED_HEAD, fold_numbers

# ---- multiplicity over manifest orbits in solved1472 (verbatim semantics) ----
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

per_receipt = []
for r in fold_receipts:
    b = r["bit"]
    x = cert_roots[b]
    cv = covers(x)
    cvm = cv & set(manifest)
    per_receipt.append({
        "bit": b,
        "root_hex": f"{x:032x}",
        "covers": len(cv),
        "covers_in_manifest": len(cvm),
        "marginal_in_manifest_at_1452": len(cvm - covered1452),
        "marginal_hexes": sorted(f"{c:032x}" for c in cvm - covered1452),
    })

audit = {
    "schema": "n11-class2-lane-head1472-cover-multiplicity-audit-20261117-v1",
    "date": "2026-11-17",
    "role": ("post-fold head-1472 cover-multiplicity audit executed after the "
             "cost64h fold receipt landed; receipt roots taken from the landed "
             "fold record (blob 1633be292f...); every field is compared "
             "against the preregistered prediction"),
    "method": ("verbatim frontier extraction of the head-1452 receipt basis "
               "(775 roots, asserted, same file set as the prediction minus "
               "the landed fold receipt), plus the 23 cost64h WIN7-D10 receipt "
               "roots read from the landed fold receipt; solved = winners "
               "UNION covers(receipt roots)"),
    "head_control": {
        "receipt_roots_1452_basis": len(roots),
        "receipt_roots_1472_basis": len(roots1472),
        "winners": len(winners),
        "covered_1452": len(covered1452),
        "expected_1452": EXPECTED_COVERED_1452,
        "covered_1472": len(covered1472),
        "expected_1472": EXPECTED_COVERED_1472,
        "projected_head_numbers": EXPECTED_PROJECTED_HEAD,
        "fold_receipt_frontier_numbers": fold_numbers,
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
    "source_blob_pins": {
        "fold_receipt": FOLD_RECEIPT_BLOB,
        "prediction": git_blob_sha((OUT / PREDICTION).read_bytes()),
    },
    "interpretation_guard": (
        "bookkeeping over published receipts only; no engine search was run "
        "and no verdict was created; solved counts measure manifest coverage, "
        "not the game-theoretic value of any position; WIN7 certificates "
        "prove a first-player win within depth 10 from individual 7-stone "
        "roots only; REFUTED-D10 is not a LOSS proof; the 11x11 empty "
        "board, two-stone roots {49,60}/{59,60}, S2 {59,60} and classes "
        "1/2/4 remain UNKNOWN"),
}

# ---- field-by-field agreement with the prediction ----
agreement = {"fields_compared": 0, "mismatches": [], "checks": {}}


def cmp_field(name, got, want):
    agreement["fields_compared"] += 1
    ok = got == want
    agreement["checks"][name] = ok
    if not ok:
        agreement["mismatches"].append(
            {"field": name, "audit": got, "prediction": want})


ph = prediction["head_control"]
cmp_field("head_control.covered_1452", audit["head_control"]["covered_1452"], ph["covered_1452"])
cmp_field("head_control.covered_1472", audit["head_control"]["covered_1472"], ph["covered_1472"])
cmp_field("head_control.receipt_roots_1452_basis", audit["head_control"]["receipt_roots_1452_basis"], ph["receipt_roots_1452_basis"])
cmp_field("head_control.receipt_roots_1472_basis", audit["head_control"]["receipt_roots_1472_basis"], ph["receipt_roots_1472_basis"])
cmp_field("head_control.winners", audit["head_control"]["winners"], ph["winners"])
cmp_field("head_control.marginal_in_manifest", audit["head_control"]["marginal_in_manifest"], ph["marginal_in_manifest"])
cmp_field("multiplicity_histogram", audit["multiplicity_histogram_manifest_orbits"], prediction["multiplicity_histogram_manifest_orbits"])
cmp_field("single_cover.count", audit["single_cover_orbits"]["count"], prediction["single_cover_orbits"]["count"])
cmp_field("single_cover.cost_sum", audit["single_cover_orbits"]["cost_sum"], prediction["single_cover_orbits"]["cost_sum"])
cmp_field("single_cover.orbits", audit["single_cover_orbits"]["orbits"], prediction["single_cover_orbits"]["orbits"])
cmp_field("roots_with_exclusive_contribution", audit["roots_with_exclusive_contribution"], prediction["roots_with_exclusive_contribution"])
cmp_field("top_exclusive_roots", audit["top_exclusive_roots"], prediction["top_exclusive_roots"])
cmp_field("cost64h_receipts", audit["cost64h_receipts"], prediction["cost64h_receipts"])

agreement["all_fields_agree"] = not agreement["mismatches"]
audit["prediction_agreement"] = {
    "prediction_file": PREDICTION,
    "prediction_blob": git_blob_sha((OUT / PREDICTION).read_bytes()),
    **agreement,
}
audit["status"] = "PASS" if agreement["all_fields_agree"] else "MISMATCH"

with open(OUT / "class2-lane-head1472-cover-multiplicity-audit-20261117.json", "w") as f:
    json.dump(audit, f, indent=1, sort_keys=True)
    f.write("\n")
print(json.dumps(audit["head_control"], indent=1))
print("winner_only:", len(winner_only), "single_cover:", len(single_cover),
      "exclusive roots:", len(root_exclusive))
print("fields_compared:", agreement["fields_compared"],
      "mismatches:", len(agreement["mismatches"]))
print("status:", audit["status"])
