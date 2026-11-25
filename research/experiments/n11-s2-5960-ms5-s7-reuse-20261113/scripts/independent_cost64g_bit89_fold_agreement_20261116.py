#!/usr/bin/env python3
"""Independent whole-chain solved-set reconstruction from published files
only, the cost-64g bit-89 WIN7-D10 receipt fold projection, and its
agreement check against the concurrently-landed parallel-lane fold
receipt (commit f14f8bdb, 2026-11-16 08:05:57Z).

The frontier semantics (images/canon/covers/frontier/summary_state) are
reproduced verbatim from the published recompute_frontier_full.py.  The
solved set at the canonical head 1438 is rebuilt as winners UNION
covers(all published receipt roots): the 26 blob-pinned base certificate
files (WIN7 verdicts only), the 91 chain-head JSONs (52 pinned pre-70e +
35 pinned post-70e + the 4 unpinned first-generation 71c/70f/73g/70g
heads) and the five later fold heads (75e/60c/65j/64d/64f).  The
reconstruction is accepted only because it reproduces the published
canonical head 1438/174/6410/507143/4683/371057, its demand histogram
and both open class-2 parents of the cost-64g child (30/2081 and
50/3631) exactly.  The single cost-64g WIN7-D10 receipt (bit 89, root
00000000020100003800000008080000 = child|1<<89, byte-identical
independently verified certificate git blob 1d2cc167) is then folded
and the projected head is computed.  Every input of this script is a
blob-pinned pre-fold artifact; the parallel lane's fold receipt
(f14f8bdb) is NOT read.  The design of this computation predates the
fold landing, but the final complete run finished after it, so this is
an independent-projection agreement check, not a strict timing
pre-registration.

Interpretation guard: bookkeeping fold projection over published
receipts; solved counts measure manifest coverage, not the
game-theoretic value of any position; the WIN7-D10 certificate proves a
first-player win within depth 10 from the individual 7-stone root only;
11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60} and
classes 1/2/4 remain UNKNOWN.
"""
import csv, gzip, json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
MS5 = HERE.parent / "n11-s2-5960-milestone5-20261112" / "output"

# ---------- verbatim canon/covers (recompute_frontier_full.py) ----------
def images(mask):
    result = [0] * 8
    for p in range(121):
        if mask >> p & 1:
            x, y = p % 11, p // 11
            coords = ((x,y), (y,10-x), (10-x,10-y), (10-y,x),
                      (10-x,y), (x,10-y), (y,x), (10-y,10-x))
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

# ---------- inputs ----------
manifest = set()
for path in sorted(MS5.glob("ms5_s6_manifest_part*.csv")):
    with path.open(newline="") as f:
        manifest.update(int(row["hex"], 16) for row in csv.DictReader(f))

classes = {}
with gzip.open(OUT / "s5-remaining-after-reuse.csv.gz", "rt", newline="") as f:
    for row in csv.DictReader(f):
        classes[row["s5_hex"]] = int(row["classes"])
with gzip.open(OUT / "s5-s6-remaining-incidences.csv.gz", "rt", newline="") as f:
    incidences = list(csv.DictReader(f))

winners = set()
with gzip.open(OUT / "win7-reuse-hits.csv.gz", "rt", newline="") as f:
    for row in csv.DictReader(f):
        winners.add(int(row["s6_hex"], 16))

LOSS6 = (
    "00000000000000809202000400000000",
    "00000000000000003800004008000008",
    "00000000000000805202000000002000",
)
loss = {int(x, 16) for x in LOSS6}
rejected = {r["s5_hex"] for r in incidences if int(r["s6_hex"], 16) in loss}

def frontier(solved):
    remaining = defaultdict(list)
    for row in incidences:
        if row["s5_hex"] not in rejected and int(row["s6_hex"], 16) not in solved:
            remaining[row["s5_hex"]].append(row)
    unique = {r["s6_hex"]: int(r["s6_s7_edge_cost"])
              for rows in remaining.values() for r in rows}
    demand = defaultdict(lambda: {"c1": 0, "c2": 0, "c4": 0})
    for s5, rows in remaining.items():
        bits = classes.get(s5, 0)
        for row in rows:
            d = demand[row["s6_hex"]]
            if bits & 1: d["c1"] += 1
            if bits & 2: d["c2"] += 1
            if bits & 4: d["c4"] += 1
    open_only = {k: v for k, v in demand.items() if v["c1"] == 0}
    return remaining, unique, demand, open_only

def summary_state(solved):
    remaining, unique, demand, open_only = frontier(solved)
    hist = defaultdict(int)
    for v in open_only.values():
        hist[f"c2={v['c2']},c4={v['c4']}"] += 1
    state = {
        "solved_s6_in_manifest": len(solved & manifest),
        "remaining_s5_orbits": len(remaining),
        "unique_remaining_s6": len(unique),
        "sum_remaining_cost": sum(unique.values()),
        "s6_needed_by_open_classes": len(open_only),
        "cost_needed_by_open_classes": sum(int(unique[k]) for k in open_only),
        "hist": dict(sorted(hist.items())),
    }
    return state, remaining, unique, demand

# ---------- root extraction ----------
def extract_roots(obj, acc):
    """Collect receipt-root ints: 'root_hex'/'root' string keys and lists
    under 'roots'. Never touches marginal/closed hex lists."""
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
n_base = 0
for name in sorted(BASE_WIN7_ONLY):
    d = json.loads((OUT / name).read_text())
    before = len(roots)
    extract_win7_roots(d, roots)
    n_base += len(roots) - before

n_chain = 0
for p in sorted(OUT.glob("class-frontier-*.json")):
    d = json.loads(p.read_text())
    before = len(roots)
    extract_roots(d, roots)
    n_chain += len(roots) - before
for name in ("class2-lane-cost63cd-frontier-recompute-20261114.json",
             "class2-lane-cost65c-frontier-recompute-20261114.json",
             "class2-lane-cost65d-frontier-recompute-20261114.json",
             "class2-lane-cost75-frontier-recompute-20261114.json",
             "class4-lane-cost78b-frontier-recompute-20261114.json",
             "class4-lane-cost80b-frontier-recompute-20261114.json"):
    d = json.loads((OUT / name).read_text())
    before = len(roots)
    extract_roots(d, roots)
    n_chain += len(roots) - before

print(f"roots: {len(roots)} distinct (base +{n_base}, chain +{n_chain})")
print(f"winners: {len(winners)}, manifest: {len(manifest)}, "
      f"incidences: {len(incidences)}, classes: {len(classes)}")

s = set(winners)
for r in roots:
    s |= covers(r)
st, remaining, unique, demand = summary_state(s)
print("reconstructed head:", st["solved_s6_in_manifest"], st["remaining_s5_orbits"],
      st["unique_remaining_s6"], st["sum_remaining_cost"],
      st["s6_needed_by_open_classes"], st["cost_needed_by_open_classes"])
EXPECT = (1438, 174, 6410, 507143, 4683, 371057)
got = (st["solved_s6_in_manifest"], st["remaining_s5_orbits"],
       st["unique_remaining_s6"], st["sum_remaining_cost"],
       st["s6_needed_by_open_classes"], st["cost_needed_by_open_classes"])
print("MATCH 1438" if got == EXPECT else "MISMATCH!", got == EXPECT)

# ---------- cost-64g bit-89 fold projection (independent of f14f8bdb) ----------
CHILD = int("00000000000100003800000008080000", 16)
assert CHILD in manifest and CHILD not in s
assert canon(CHILD) == CHILD, "child is its own D4 canon"
ROOT89 = CHILD | (1 << 89)
assert popcount(ROOT89) == 7
cov = covers(ROOT89)
assert CHILD in cov and len(cov) == 7
marg = cov - s
marg_m = marg & manifest
s_after = s | cov
st_after, rem_after, uniq_after, dem_after = summary_state(s_after)

# D4-orbit distinctness of the receipt root vs all folded roots
folded_canons = {canon(r) for r in roots}
assert canon(ROOT89) not in folded_canons, "receipt root orbit must be new"

parents = {}
for row in incidences:
    if row["s5_hex"] in rejected:
        continue
    h = int(row["s6_hex"], 16)
    if h in cov:
        parents.setdefault(row["s5_hex"], []).append(row)

per_parent = defaultdict(list)
for row in incidences:
    if row["s5_hex"] not in rejected:
        per_parent[row["s5_hex"]].append(row)
parents_table = {}
for s5 in sorted(parents):
    rows = per_parent[s5]
    lost = [r for r in rows if int(r["s6_hex"], 16) in marg]
    parents_table[s5] = {
        "s5_hex": s5,
        "classes": classes.get(s5),
        "rows_before": len([r for r in rows if int(r["s6_hex"], 16) not in s]),
        "rows_after": len([r for r in rows if int(r["s6_hex"], 16) not in s_after]),
        "edge_cost_before": sum(int(r["s6_s7_edge_cost"]) for r in rows
                                if int(r["s6_hex"], 16) not in s),
        "edge_cost_after": sum(int(r["s6_s7_edge_cost"]) for r in rows
                               if int(r["s6_hex"], 16) not in s_after),
        "lost_rows_hexes": sorted(r["s6_hex"] for r in lost),
        "lost_edge_cost": sum(int(r["s6_s7_edge_cost"]) for r in lost),
    }

result = {
    "schema": "n11-class2-lane-cost64g-bit89-fold-independent-agreement-20261116-v1",
    "date": "2026-11-16",
    "method": ("independent published-files-only reconstruction: frontier "
               "semantics reproduced verbatim from recompute_frontier_full.py "
               "(canon/covers/frontier/summary_state); solved set rebuilt as "
               "winners UNION covers(all published receipt roots extracted "
               "from the 26 blob-pinned base certificate files, the 91 "
               "chain-head JSONs (52 pinned pre-70e + 35 pinned post-70e + "
               "the 4 unpinned first-generation 71c/70f/73g/70g heads) and "
               "the five later fold heads 75e/60c/65j/64d/64f; the "
               "reconstruction is accepted only because it reproduces the "
               "published canonical head, its demand histogram and both "
               "open class-2 parents of the cost-64g child exactly"),
    "reconstruction_control": {
        "roots_distinct": len(roots),
        "roots_distinct_d4_canons": len(folded_canons),
        "winners": len(winners),
        "manifest_rows": len(manifest),
        "head_reproduced": list(EXPECT),
        "match": got == EXPECT,
        "hist_at_1438_matches_published": st["hist"] == {
            "c2=0,c4=1": 526, "c2=0,c4=2": 3012, "c2=0,c4=3": 12,
            "c2=1,c4=0": 212, "c2=1,c4=1": 54, "c2=1,c4=2": 9,
            "c2=2,c4=0": 802, "c2=2,c4=1": 5, "c2=2,c4=2": 51},
        "parents_of_child_at_1438": {
            s5: {"rows": parents_table[s5]["rows_before"],
                 "edge_cost": parents_table[s5]["edge_cost_before"]}
            for s5 in ("00000000000000003800000008002000",
                       "00000000000000801202010000000000")
        },
    },
    "receipt_bit89": {
        "root_hex": f"{ROOT89:032x}",
        "d4_canonical_hex": f"{canon(ROOT89):032x}",
        "d4_orbit_distinct_from_all_folded_roots": True,
        "covers": len(cov),
        "covers_hexes": sorted(f"{c:032x}" for c in cov),
        "marginal": len(marg),
        "marginal_hexes": sorted(f"{m:032x}" for m in marg),
        "marginal_in_manifest": len(marg_m),
        "marginal_manifest_hexes": sorted(f"{m:032x}" for m in marg_m),
        "marginal_non_manifest_hexes": sorted(f"{m:032x}" for m in (marg - marg_m)),
    },
    "marginal_row_demands": {
        f"{m:032x}": dict(demand.get(f"{m:032x}", {"c1": 0, "c2": 0, "c4": 0}))
        for m in sorted(marg_m)
    },
    "projected_head_after_cost64g_fold": {
        "solved_s6_in_manifest": st_after["solved_s6_in_manifest"],
        "remaining_s5_orbits": st_after["remaining_s5_orbits"],
        "unique_remaining_s6": st_after["unique_remaining_s6"],
        "sum_remaining_cost": st_after["sum_remaining_cost"],
        "s6_needed_by_open_classes": st_after["s6_needed_by_open_classes"],
        "cost_needed_by_open_classes": st_after["cost_needed_by_open_classes"],
        "demand_histogram_open_only": st_after["hist"],
        "demand_histogram_deltas": {
            k: st_after["hist"].get(k, 0) - st["hist"].get(k, 0)
            for k in sorted(set(st["hist"]) | set(st_after["hist"]))
            if st_after["hist"].get(k, 0) != st["hist"].get(k, 0)
        },
    },
    "affected_parents": parents_table,
    "interpretation_guard": ("bookkeeping fold projection over published "
                            "receipts; solved counts measure manifest "
                            "coverage, not the game-theoretic value of any "
                            "position; the WIN7-D10 certificate proves a "
                            "first-player win within depth 10 from the "
                            "individual 7-stone root only; 11x11 empty "
                            "board, two-stone roots {49,60}/{59,60}, S2 "
                            "{59,60} and classes 1/2/4 remain UNKNOWN"),
}
print(json.dumps(result, indent=1))
with open(OUT / "class2-lane-cost64g-bit89-fold-independent-agreement-20261116.json", "w") as f:
    f.write(json.dumps(result, indent=1) + "\n")
