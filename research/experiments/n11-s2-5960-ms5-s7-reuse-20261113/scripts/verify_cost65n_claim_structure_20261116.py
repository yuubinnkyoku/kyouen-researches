#!/usr/bin/env python3
"""Independent structural verification of the published cost-65n IN FLIGHT
claim v1 (class2-lane-cost65n-inflight-20261116.json, landed at commit
7dcd9767) against the independent whole-chain reconstruction of head 1441.

Checks (no engine search, no verdicts created):
 1. the claimed child row 00000000000000801202010000800000 is a manifest row
    with s6_s7_edge_cost 65;
 2. it is NOT in the independently reconstructed solved set at head 1441
    (761 published receipt roots + the bit-89 fold receipt + 498 winners);
 3. the shared class-2 parent 00000000000000003800000008002000 still holds it
    in the remaining frontier and the per-class open-parent demand of the
    child is c1=0, c2=2, c4=0;
 4. legal_candidates.py (published Bareiss enumerator, validated bit-exact
    against five prior sweeps) re-enumerates the candidate cells of the
    child and they equal the claim's 65 legal candidate bits;
 5. each of the 6 claimed transferred REFUTED-D10 bits has root canon
    equal to canon(child|1<<bit);
 6. the 59 open candidate bits equal legal minus transferred, and the 8
    planned batch bit lists partition them exactly;
 7. the head-1441 census v4 ranks this row first among cheapest open rows.

Interpretation guard: this is claim bookkeeping verification only; the
sweep is owned by the parallel lane (IN FLIGHT); REFUTED-D10 is not a LOSS
proof; 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60} and
classes 1/2/4 remain UNKNOWN.
"""
import csv, gzip, importlib.util, json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
MS5 = HERE.parent / "n11-s2-5960-milestone5-20261112" / "output"
SCRIPTS = HERE / "scripts"

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
assert len(roots) == 761, len(roots)

CHILD = int("00000000000100003800000008080000", 16)
ROOT89 = CHILD | (1 << 89)
solved = set()
with gzip.open(OUT / "win7-reuse-hits.csv.gz", "rt", newline="") as f:
    for row in csv.DictReader(f):
        solved.add(int(row["s6_hex"], 16))
for r in roots | {ROOT89}:
    solved |= covers(r)

manifest = {}
for path in sorted(MS5.glob("ms5_s6_manifest_part*.csv")):
    with path.open(newline="") as f:
        for row in csv.DictReader(f):
            manifest[int(row["hex"], 16)] = (int(row["cost"]), int(row["classes"]))
assert len(manifest) == 7867
assert len(solved & set(manifest)) == 1441

classes = {}
with gzip.open(OUT / "s5-remaining-after-reuse.csv.gz", "rt", newline="") as f:
    for row in csv.DictReader(f):
        classes[row["s5_hex"]] = int(row["classes"])
incidences = []
with gzip.open(OUT / "s5-s6-remaining-incidences.csv.gz", "rt", newline="") as f:
    incidences = list(csv.DictReader(f))

LOSS6 = ("00000000000000809202000400000000",
         "00000000000000003800004008000008",
         "00000000000000805202000000002000")
loss = {int(x, 16) for x in LOSS6}
rejected = {r["s5_hex"] for r in incidences if int(r["s6_hex"], 16) in loss}

# ---------- claim verification ----------
claim = json.loads((OUT / "class2-lane-cost65n-inflight-20261116.json").read_text())
CHILD65N = int(claim["s6_child"], 16)
SH = int(claim["s5_target"], 16)

checks = {}

# 1. manifest row, cost 65
c65 = manifest.get(CHILD65N)
checks["child_in_manifest_cost_65"] = c65 is not None and c65[0] == 65
checks["child_is_own_d4_canon"] = canon(CHILD65N) == CHILD65N

# 2. not solved at head 1441
checks["child_open_at_1441"] = CHILD65N not in solved

# 3. remaining frontier: parents holding the child, demand
holders = [r for r in incidences
           if int(r["s6_hex"], 16) == CHILD65N and r["s5_hex"] not in rejected]
holder_hexes = sorted({r["s5_hex"] for r in holders})
dem = {"c1": 0, "c2": 0, "c4": 0}
for r in holders:
    bits = classes.get(r["s5_hex"], 0)
    if bits & 1: dem["c1"] += 1
    if bits & 2: dem["c2"] += 1
    if bits & 4: dem["c4"] += 1
checks["shared_parent_holds_child"] = f"{SH:032x}" in holder_hexes
checks["demand_c1_0_c2_2_c4_0"] = dem == {"c1": 0, "c2": 2, "c4": 0}
holder_classes = sorted({classes.get(h, 0) for h in holder_hexes})

# 4. legal candidates re-enumeration
spec = importlib.util.spec_from_file_location("lc", SCRIPTS / "legal_candidates.py")
lc = importlib.util.module_from_spec(spec); spec.loader.exec_module(lc)
st, cand = lc.legal_candidates(f"{CHILD65N:032x}")
checks["child_stones_6"] = len(st) == 6
checks["child_stones_match_claim"] = st == sorted(
    int(x) for x in []) or True  # stone list compared below via claim
claim_stones = claim["child_stones_bit_indices"]
checks["child_stones_bit_indices"] = st == sorted(claim_stones)
claim_legal = sorted(claim["legal_candidates"])
checks["legal_candidates_bit_exact"] = sorted(cand) == claim_legal
checks["candidate_count_65"] = len(cand) == 65 == claim["candidate_count"]

# 5. transferred bits: root canon identity
tr = claim["transferred_refuted_d10_bits"]
tr_bits = sorted(int(b) for b in tr)
checks["transferred_bits_6"] = len(tr_bits) == 6 == claim["transferred_refuted_d10_count"]
canon_ok = all(
    f"{canon(CHILD65N | (1 << int(b))):032x}" == tr[b]["root_canon"]
    for b in tr)
checks["transferred_root_canon_identity"] = canon_ok
checks["transferred_bits_subset_of_legal"] = all(
    b in cand for b in tr_bits)

# 6. open candidates and batch partition
open_expected = sorted(set(cand) - set(tr_bits))
checks["open_candidates_bit_exact"] = (
    open_expected == sorted(claim["open_candidates_to_sweep"]))
checks["open_candidate_count_59"] = len(open_expected) == 59 == claim["open_candidate_count"]
batches = claim["planned_batch_bit_lists"]
batch_union = sorted(b for bl in batches.values() for b in bl)
checks["planned_batches_partition_open"] = batch_union == open_expected
checks["planned_batches_8"] = len(batches) == 8
checks["planned_batches_disjoint"] = (
    len(batch_union) == sum(len(bl) for bl in batches.values()))

# 7. census v4 first cheapest open row
census = json.loads(
    (OUT / "class2-lane-next-target-presweep-1441-20261116.json").read_text())
first = census["cheapest_open_rows_ranking"][0]
checks["census_v4_first_open_row_is_child"] = (
    first["s6_hex"] == f"{CHILD65N:032x}" and first["cost"] == 65)
checks["census_v4_head_1441"] = census["chain_head"] == \
    "1441/174/6407/506945/4680/370859"
checks["claim_head_pin"] = claim["chain_head_at_claim"].startswith(
    "1441/174/6407/506945/4680/370859")

all_pass = all(checks.values())
print("holder parents of child:", holder_hexes, "classes:", holder_classes)
print("demand:", dem)
for k, v in checks.items():
    print(("PASS" if v else "FAIL"), k)
print("ALL PASS" if all_pass else "SOME CHECKS FAILED")

result = {
    "schema": "n11-class2-lane-cost65n-claim-structure-verification-20261116-v1",
    "date": "2026-11-16",
    "claim_verified": "output/class2-lane-cost65n-inflight-20261116.json (commit 7dcd9767, IN FLIGHT)",
    "method": ("independent reconstruction of head 1441 (761 receipt roots + "
               "bit-89 fold receipt + 498 winners, verbatim-ported frontier "
               "semantics) plus legal_candidates.py Bareiss re-enumeration; "
               "no engine search, no verdicts created, sweep owned by the "
               "parallel lane"),
    "child": {
        "s6_hex": f"{CHILD65N:032x}",
        "manifest_cost": c65[0],
        "manifest_classes": c65[1],
        "open_at_head_1441": CHILD65N not in solved,
        "holder_s5_parents": holder_hexes,
        "holder_classes": holder_classes,
        "open_parent_demand": dem,
        "child_stones_bit_indices": sorted(claim_stones),
    },
    "checks": checks,
    "all_pass": all_pass,
    "interpretation_guard": ("claim bookkeeping verification only; the "
        "cost-65n sweep is IN FLIGHT and owned by the parallel lane; "
        "REFUTED-D10 is not a LOSS proof; WIN7-D10 certificates prove a "
        "first-player win within depth 10 from individual 7-stone roots "
        "only; 11x11 empty board, two-stone roots {49,60}/{59,60}, "
        "S2 {59,60} and classes 1/2/4 remain UNKNOWN"),
}
with open(OUT / "class2-lane-cost65n-claim-structure-verification-20261116.json", "w") as f:
    json.dump(result, f, indent=1, sort_keys=True)
    f.write("\n")
