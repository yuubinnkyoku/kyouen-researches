#!/usr/bin/env python3
"""Compute K0318 curve-packing substitution upper bounds U_{w,q} for w=7 (and w=8 table),
using the repo's own fixed-width implementation (curve_packing_fixed_width.bound).
Controls assert against values already recorded on main (mwq_stabilization.csv)."""
import json, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from curve_packing_fixed_width import bound

# Controls: values recorded on main (K0806; K0318 substitution) and exact thresholds.
controls = {(3, 5): 40, (5, 6): 249, (5, 7): 200, (6, 5): 658, (6, 6): 495, (6, 7): 402, (6, 8): 371}
for (w, q), expect in controls.items():
    got = bound(w, q)["packing_U"]
    assert got == expect, f"CONTROL FAIL w={w} q={q}: got {got} expect {expect}"
    print(f"control w={w} q={q}: U={got} OK")

rows = []
for q in range(4, 13):
    for w in (7, 8):
        b = bound(w, q)
        rows.append({"w": w, "q": q, "packing_U": b["packing_U"], "combined": b["combined"],
                     "Q": b["Q"], "Y": b["Y"], "d0": b["d0"], "d1": b["d1"],
                     "optimizer": b["integer_optimizer"]})
out = {"schema": 1,
       "tool": "research/experiments/fixed-width/scripts/curve_packing_fixed_width.py (main ef039092) bound()",
       "note": "U_{w,q} = packing_U is the K0318 curve-packing substitution upper bound on the stabilization length M_{w,q}",
       "controls_passed": len(controls), "rows": rows}
pathlib.Path(__file__).with_name("w7_upper_bounds.json").write_text(json.dumps(out, indent=2) + "\n")
for r in rows:
    if r["w"] == 7:
        print(f"w=7 q={r['q']}: U={r['packing_U']}")
for r in rows:
    if r["w"] == 8:
        print(f"w=8 q={r['q']}: U={r['packing_U']}")
