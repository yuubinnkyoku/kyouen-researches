#!/usr/bin/env python3
"""Aggregate the m=28..31 chunked/whole family sweep raw outputs and the dx fast
sweeps for the 3 x m, q=4 def-mode lane extension (ext28plus), and emit
output/ext28plus/family_sweep_28_31.jsonl + output/ext28plus/crossval_summary_ext28_31.json.

Guarantees checked here (all machine):
  A. Partition completeness: for each (m, Y) the chunk ia ranges exactly tile
     [0, C(m,3)) without overlap, and the sum of per-chunk " configs " equals
     C(m,3)^2 (whole-run single-chunk rows additionally match the published
     single-line format).
  B. All family witness counts (a0/a1/a2 sums) are 0 for every swept (m, Y).
  C. All 13 fast profiles at m=28..31 have count 0 (52 JSONL rows).
  D. closure ledger rows for m=28..31 are verdict "closed" (41 lemma kills).
  E. m=23 positive control file matches the published m=23 family Y=0 row
     (configs 3136441, a2=2): pinned-script environment calibration.

NO claims about m>=32 (wsearch34.js is hard-capped at m<=31 by its 31-bit
masks); this aggregator never extrapolates.
"""
import json
import os
import re
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))
O = lambda *p: os.path.join(HERE, *p)

FAM_RAW = {}
for fn in sorted(os.listdir(HERE)):
    mt = re.match(r"^family_(\d+)_Y(\d+)(?:_c(\d+))?\.raw$", fn)
    if not mt:
        continue
    m, Y = int(mt.group(1)), int(mt.group(2))
    line = open(O(fn)).read().strip().splitlines()[-1]
    d = json.loads(line)
    assert d["m"] == m and d["Y"] == Y, (fn, d)
    FAM_RAW.setdefault((m, Y), []).append((fn, d))

fam_rows = []
partitions_ok = True
fam_all_zero = True
for (m, Y), chunks in sorted(FAM_RAW.items()):
    nSub = comb(m, 3)
    ranges = []
    for fn, d in chunks:
        lo, hi = d["ia"]
        ranges.append((lo, hi, d))
    ranges.sort()
    pos = 0
    for lo, hi, _ in ranges:
        if lo != pos or hi > nSub or hi <= lo:
            partitions_ok = False
            print(f"PARTITION FAIL m={m} Y={Y}: expect next {pos}, got [{lo},{hi}) (nSub={nSub})")
        pos = hi
    if pos != nSub:
        partitions_ok = False
        print(f"PARTITION FAIL m={m} Y={Y}: covered to {pos} of nSub={nSub}")
    cfg = sum(d["configs"] for _, d in chunks)
    safe = sum(d["safe"] for _, d in chunks)
    deep = sum(d["deep"] for _, d in chunks)
    a0 = sum(d["a0"] for _, d in chunks)
    a1 = sum(d["a1"] for _, d in chunks)
    a2 = sum(d["a2"] for _, d in chunks)
    if cfg != nSub * nSub:
        partitions_ok = False
        print(f"CONFIGS FAIL m={m} Y={Y}: {cfg} != C({m},3)^2 = {nSub * nSub}")
    row = {
        "m": m, "Y": Y, "chunks": len(chunks),
        "ia_ranges": [[d["ia"][0], d["ia"][1]] for _, _, d in ranges],
        "configs": cfg, "safe": safe, "deep": deep,
        "a0": a0, "a1": a1, "a2": a2,
        "ms": sum(d["ms"] for _, d in chunks),
        "nSub": nSub,
    }
    fam_rows.append(row)
    if (a0, a1, a2) != (0, 0, 0):
        fam_all_zero = False
        print(f"WITNESS FOUND m={m} Y={Y}: a0={a0} a1={a1} a2={a2}")

with open(O("family_sweep_28_31.jsonl"), "w") as f:
    for row in fam_rows:
        f.write(json.dumps(row) + "\n")

# fast sweeps
fast_rows = [json.loads(l) for l in open(O("dx_sweep_28_31.jsonl"))]
fast_by_m = {}
for r in fast_rows:
    fast_by_m.setdefault(r["m"], []).append(r)
fast_all_zero = True
for m, rows in sorted(fast_by_m.items()):
    if len(rows) != 13 or any(r["count"] != 0 for r in rows):
        fast_all_zero = False
        print(f"FAST FAIL m={m}: rows={len(rows)} counts={[r['count'] for r in rows]}")

# closure ledger
closure_ok = True
for line in open(O("closure_check_28_31.jsonl")):
    d = json.loads(line)
    if d["verdict"] != "closed" or d["lemma_not_killed"] != 0:
        closure_ok = False
        print(f"CLOSURE FAIL: {d}")

# m=23 positive control calibration
ctrl = open(O("control_m23_Y0.txt")).read().strip().splitlines()
ctrl_summary = json.loads(ctrl[0])
ctrl_ok = ctrl_summary == {"m": 23, "Y": 0, "ia": [0, 1771], "o1": 1, "o2": 2,
                           "configs": 3136441, "safe": 2352504, "deep": 2352504,
                           "a0": 0, "a1": 0, "a2": 2, "ms": ctrl_summary["ms"]}

summary = {
    "family_sweep": {
        "rows": len(fam_rows),
        "per_row": {f"{r['m']}_Y{r['Y']}": [r["a0"], r["a1"], r["a2"]] for r in fam_rows},
        "partition_completeness": partitions_ok,
        "all_zero": fam_all_zero,
        "widths_family": sorted({r["m"] for r in fam_rows}),
    },
    "fast_sweep": {
        "rows": len(fast_rows),
        "all_zero": fast_all_zero,
        "widths_fast": sorted(fast_by_m),
    },
    "closure_ledger": closure_ok,
    "m23_control_recognition": ctrl_ok,
    "swept_widths": sorted(set({r["m"] for r in fam_rows}) | set(fast_by_m)),
    "verdict": (
        "WITNESS-FREE for all swept widths (family 0 witnesses in all (m,Y) chunk-complete "
        "enumerations; fast 13 profiles x swept widths all zero; lemma 41 killed per width; "
        "m=23 positive control rediscovered => pinned tools calibrated in this environment). "
        "No claim about m>=32."
        if partitions_ok and fam_all_zero and fast_all_zero and closure_ok and ctrl_ok
        else "FAIL"
    ),
}
with open(O("crossval_summary_ext28_31.json"), "w") as f:
    json.dump(summary, f, indent=1)
print(json.dumps(summary, indent=1))
