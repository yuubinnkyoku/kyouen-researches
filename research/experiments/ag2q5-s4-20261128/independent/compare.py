#!/usr/bin/env python3
"""Cross-check the K1364 claim against independent computations.

Inputs (all inside this experiment unless noted):
  * ../output/gsize_ag2q5_s4.txt   claimed engine output (SIZE/GRUNDY/GSIZE...)
  * published_run.txt              output of the published engine compiled here
  * my_run.txt                     output of our independent solver
  * complements_run.txt            output of our independent complement counter

The script (1) checks byte identity of the published run with the claim,
(2) checks every SIZE / GRUNDY / GSIZE / maximal value of the claim against the
independent solver, (3) checks all arithmetic and the structural claims,
(4) checks the size counts against a closed-form inclusion-exclusion count for
k <= 10, and (5) checks sizes k >= 11 and the maximal counts against the
independent complement (blocking-set) enumeration.

Exit code 0 iff every check passes.  Writes verification_summary.json.
"""
import hashlib
import itertools
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CLAIM = os.path.join(HERE, "..", "output", "gsize_ag2q5_s4.txt")
PUBLISHED = os.path.join(HERE, "published_run.txt")
MINE = os.path.join(HERE, "my_run.txt")
COMPL = os.path.join(HERE, "complements_run.txt")
SUMMARY = os.path.join(HERE, "verification_summary.json")

checks = []          # (name, ok, detail)


def check(name, ok, detail=""):
    checks.append((name, bool(ok), detail))
    if not ok:
        print(f"FAIL  {name}: {detail}")
    return bool(ok)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_engine(path):
    """Parse the grundy_s_stats output format (tolerant of extra line types)."""
    d = {"points": None, "circles": None, "safe": None, "maxsize": None,
         "root": None, "size": {}, "grundy": {}, "gsize": {},
         "maximal": {}, "firstmove": {}, "probe": {}, "lines": []}
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            t = raw.split()
            if not t:
                continue
            d["lines"].append(t)
            tag = t[0]
            if tag == "POINTS":
                d["points"] = int(t[1])
            elif tag == "CIRCLES":
                d["circles"] = int(t[1])
            elif tag == "SAFE":
                d["safe"] = int(t[1])
            elif tag == "MAXSIZE":
                d["maxsize"] = int(t[1])
            elif tag == "ROOT":
                d["root"] = int(t[1])
            elif tag == "SIZE":
                k, N, mx, g0 = map(int, t[1:5])
                d["size"][k] = (N, mx, g0)
            elif tag == "GRUNDY":
                d["grundy"][int(t[1])] = int(t[2])
            elif tag == "GSIZE":
                d["gsize"][(int(t[1]), int(t[2]))] = int(t[3])
            elif tag == "MAXIMAL":
                d["maximal"][int(t[1])] = int(t[2])
            elif tag == "FIRSTMOVE":
                d["firstmove"][int(t[1])] = int(t[2])
            elif tag == "PROBE":
                d["probe"]["probe"] = tuple(map(int, t[1:4]))
            elif tag == "PROBE_CHILDREN":
                d["probe"]["children_" + t[1]] = int(t[2])
    return d


claim = parse_engine(CLAIM)
pub = parse_engine(PUBLISHED)
mine = parse_engine(MINE)

# ---------------------------------------------------------------------------
# (1) the published engine, run here, reproduces the claim byte for byte
# ---------------------------------------------------------------------------
hc, hp = sha256(CLAIM), sha256(PUBLISHED)
check("published run byte-identical to claim", hc == hp,
      f"claim {hc} vs published {hp}")
print(f"claim sha256     = {hc}")
print(f"published sha256 = {hp}")

# ---------------------------------------------------------------------------
# (2) every claimed number equals the independent solver's number
# ---------------------------------------------------------------------------
check("POINTS", claim["points"] == 25 == mine["points"], str(mine["points"]))
check("CIRCLES", claim["circles"] == 30 == mine["circles"], str(mine["circles"]))
check("SAFE", claim["safe"] == 16249926 == mine["safe"], str(mine["safe"]))
check("ROOT", claim["root"] == 0 == mine["root"], str(mine["root"]))
check("SIZE keys complete 0..16", set(claim["size"]) == set(range(17)),
      str(sorted(claim["size"])))
check("independent SIZE lines identical",
      claim["size"] == mine["size"],
      f"claim={claim['size']} mine={mine['size']}")
check("independent GRUNDY lines identical",
      claim["grundy"] == mine["grundy"],
      f"claim={claim['grundy']} mine={mine['grundy']}")
check("independent GSIZE lines identical",
      claim["gsize"] == mine["gsize"],
      f"claim-only={sorted(set(claim['gsize']) - set(mine['gsize']))} "
      f"mine-only={sorted(set(mine['gsize']) - set(claim['gsize']))}")
check("independent MAXSIZE is 16", mine["maxsize"] == 16, str(mine["maxsize"]))
check("independent MAXIMAL column agrees with claim SIZE maximal column",
      {k: v[1] for k, v in mine["size"].items() if v[1]} == mine["maximal"],
      f"maximal={mine['maximal']}")
check("independent FIRSTMOVE is {1: 25}", mine["firstmove"] == {1: 25},
      str(mine["firstmove"]))

# ---------------------------------------------------------------------------
# (3) arithmetic self-consistency of the claimed table
# ---------------------------------------------------------------------------
stated_sizes = [1, 25, 300, 2300, 12650, 53100, 176500, 475000, 1047375,
                1898000, 2809700, 3340500, 3089000, 2103000, 961500, 252600,
                28375]
for k, want in enumerate(stated_sizes):
    check(f"size k={k} count", claim["size"][k][0] == want,
          f"{claim['size'][k][0]} != {want}")

stated_g = {0: 7967001, 1: 7919925, 2: 159000, 3: 204000}
check("GRUNDY totals", claim["grundy"] == stated_g, str(claim["grundy"]))
check("max Grundy is 3", max(claim["grundy"]) == 3, str(sorted(claim["grundy"])))
check("no Grundy >= 4", all(g <= 3 for g in claim["grundy"]), "")

# per-size G counts sum to N; g0 column; per-value totals
ok_sums = True
for k in range(17):
    N, mx, g0 = claim["size"][k]
    per_k = {g: c for (kk, g), c in claim["gsize"].items() if kk == k}
    ok_sums &= (sum(per_k.values()) == N)
    ok_sums &= (per_k.get(0, 0) == g0)
check("every size's G counts sum to its SIZE count and g0 column matches",
      ok_sums, "")
ok_tot = True
for g in claim["grundy"]:
    ok_tot &= (sum(c for (kk, gg), c in claim["gsize"].items() if gg == g)
               == claim["grundy"][g])
check("per-Grundy totals over sizes equal GRUNDY lines", ok_tot, "")
check("sum of SIZE counts == SAFE",
      sum(v[0] for v in claim["size"].values()) == claim["safe"] == 16249926, "")
check("sum of GRUNDY totals == SAFE",
      sum(claim["grundy"].values()) == claim["safe"], "")

# maximal counts: only 14,15,16 and exactly the stated values
max_by_k = {k: v[1] for k, v in claim["size"].items() if v[1]}
check("maximal counts only at k=14,15,16",
      set(max_by_k) == {14, 15, 16}, str(max_by_k))
check("maximal counts 14:1500, 15:6600, 16:28375",
      max_by_k == {14: 1500, 15: 6600, 16: 28375}, str(max_by_k))

# companion JSON artifact must agree with the text table
json_path = os.path.join(HERE, "..", "output", "ag2q5_s4_gsize.json")
json_ok = True
with open(json_path, encoding="utf-8") as f:
    js = json.load(f)
json_ok &= (js["safe"] == claim["safe"])
for k in range(17):
    rec = js["sizes"][str(k)]
    N, mx, g0 = claim["size"][k]
    per = {g: c for (kk, g), c in claim["gsize"].items() if kk == k}
    json_ok &= (rec["N"] == N)
    json_ok &= (rec["maximal"] == mx)
    json_ok &= ({int(g): c for g, c in rec["N_g"].items()} == per)
check("JSON artifact ag2q5_s4_gsize.json agrees with the txt claim",
      json_ok, "")

# ---------------------------------------------------------------------------
# (4) structural claims
# ---------------------------------------------------------------------------
parity_ok = True
for k in range(11):
    per_k = {g: c for (kk, g), c in claim["gsize"].items() if kk == k}
    want = {0: claim["size"][k][0]} if k % 2 == 0 else {1: claim["size"][k][0]}
    parity_ok &= (per_k == want)
check("k=0..10 parity law (even k all G0, odd k all G1)", parity_ok, "")

g3_sizes = sorted({k for (k, g) in claim["gsize"] if g == 3})
check("G3 occurs only at sizes 11 and 13", g3_sizes == [11, 13], str(g3_sizes))

N16, mx16, g016 = claim["size"][16]
per16 = {g: c for (k, g), c in claim["gsize"].items() if k == 16}
check("all 28,375 size-16 positions are maximal G0",
      N16 == 28375 and mx16 == 28375 and per16 == {0: 28375},
      f"N={N16} maximal={mx16} dist={per16}")

# ---------------------------------------------------------------------------
# (5a) independent closed-form count for k <= 10
# ---------------------------------------------------------------------------
# Safe k-set = subset containing no full line.  For k <= 10 at most two lines
# fit inside one k-set (three lines have union >= 13: concurrent 1+3*4=13,
# otherwise at least 2*5 + 5 - 2 = 13).  Among the C(30,2)=435 line pairs,
# 6 classes * C(5,2) = 60 are parallel (union 10) and 375 meet (union 9).
# Inclusion-exclusion:
#   safe(k) = C(25,k) - 30 C(20,k-5) + 375 C(16,k-9) + 60 C(15,k-10).
from math import comb


def C(a, b):
    return comb(a, b) if 0 <= b <= a else 0


formula_ok = True
formula_rows = {}
for k in range(11):
    f = C(25, k) - 30 * C(20, k - 5) + 375 * C(16, k - 9) + 60 * C(15, k - 10)
    formula_rows[k] = f
    formula_ok &= (f == claim["size"][k][0])
check("closed-form inclusion-exclusion matches size counts k=0..10",
      formula_ok, str(formula_rows))

# also check the ingredients used above on the actual board
with open(os.path.join(HERE, "..", "..", "s-parameter-kyouen-20261125",
                       "output", "board_ag2q5.txt"), encoding="utf-8") as f:
    tok = f.read().split()
n, b = int(tok[0]), int(tok[1])
pos = 2
lines = []
for _ in range(b):
    ln = int(tok[pos]); pos += 1
    lines.append(frozenset(int(x) for x in tok[pos:pos + ln])); pos += ln
lsets = list(lines)
intersect_pairs = sum(1 for i, j in itertools.combinations(range(b), 2)
                      if lsets[i] & lsets[j])
parallel_pairs = sum(1 for i, j in itertools.combinations(range(b), 2)
                     if not (lsets[i] & lsets[j]))
check("board has 375 intersecting and 60 parallel line pairs",
      (intersect_pairs, parallel_pairs) == (375, 60),
      f"{intersect_pairs},{parallel_pairs}")

# ---------------------------------------------------------------------------
# (5b) independent complement / minimal-blocking-set counts
# ---------------------------------------------------------------------------
blocking, minimal = {}, {}
with open(COMPL, encoding="utf-8") as f:
    for raw in f:
        t = raw.split()
        if not t:
            continue
        if t[0] == "BLOCKING":
            blocking[int(t[1])] = int(t[2])
        elif t[0] == "MINIMAL":
            minimal[int(t[1])] = int(t[2])

check("no blocking set of size <= 8 (hence no safe set of size >= 17)",
      all(blocking[m] == 0 for m in range(9)), str(blocking))
check("smallest blocking set has size 9 (hence maximum safe size is 16)",
      blocking[9] > 0 and all(blocking[m] == 0 for m in range(9)),
      f"blocking[9]={blocking[9]}")
for m in range(9, 15):
    k = 25 - m
    check(f"complement blocking count m={m} equals safe count k={k}",
          blocking[m] == claim["size"][k][0],
          f"{blocking[m]} != {claim['size'][k][0]}")
check("minimal blocking sets m=9,10,11 match maximal counts k=16,15,14",
      (minimal[9], minimal[10], minimal[11])
      == (max_by_k[16], max_by_k[15], max_by_k[14]),
      f"{minimal[9]},{minimal[10]},{minimal[11]}")
check("no minimal blocking set of size 12,13,14 (no maximal k=13,12,11)",
      all(minimal[m] == 0 for m in (12, 13, 14)),
      str({m: minimal[m] for m in (12, 13, 14)}))

# ---------------------------------------------------------------------------
# report
# ---------------------------------------------------------------------------
failed = [c for c in checks if not c[1]]
print()
print(f"{len(checks)} checks, {len(checks) - len(failed)} passed, "
      f"{len(failed)} failed")
if failed:
    print("RESULT: FAIL")
    for name, _, detail in failed:
        print(f"  - {name}: {detail}")
    code = 1
else:
    print("RESULT: PASS")
    code = 0

summary = {
    "claim_file": os.path.relpath(CLAIM, HERE).replace("\\", "/"),
    "claim_sha256": hc,
    "published_run_sha256": hp,
    "byte_identical": hc == hp,
    "checks": [{"name": n_, "passed": ok, "detail": d}
               for n_, ok, d in checks],
    "failed": len(failed),
    "passed": len(checks) - len(failed),
    "total_checks": len(checks),
    "result": "PASS" if code == 0 else "FAIL",
    "size_counts": {str(k): claim["size"][k][0] for k in range(17)},
    "maximal_counts": {str(k): v for k, v in max_by_k.items()},
    "grundy_totals": {str(g): c for g, c in claim["grundy"].items()},
    "safe_total": claim["safe"],
    "complement_blocking": {str(m): blocking[m] for m in sorted(blocking)},
    "complement_minimal": {str(m): minimal[m] for m in sorted(minimal)},
    "closed_form_k0_10": {str(k): formula_rows[k] for k in formula_rows},
}
with open(SUMMARY, "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=1)

sys.exit(code)
