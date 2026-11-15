#!/usr/bin/env python3
"""Extract the cost-76d child facts at the reconciled canonical head 1405
for the in-flight claim (second coverable class-2 candidate S5, the
unclaimed cost-76 row)."""
import json
import runpy
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
sys.path.insert(0, str(HERE / "scripts"))
from legal_candidates import legal_candidates

CHILD = "00000000040000003800080008000000"
CHILD_V = int(CHILD, 16)

ns = runpy.run_path(str(HERE / "scripts" /
                        "recompute_frontier_reconcile_canonical1400_"
                        "cost70g_20261116.py"))
s_f = ns["s_new"]
rem_f = ns["rem_new"]
dem_f = ns["dem_new"]
manifest = ns["manifest"]
canon = ns["canon"]
st_f = ns["st_new"]
assert (st_f["solved_s6_in_manifest"], st_f["unique_remaining_s6"],
        st_f["sum_remaining_cost"], st_f["s6_needed_by_open_classes"],
        st_f["cost_needed_by_open_classes"]) == (1405, 6443, 509457, 4713,
                                                 373180)
assert CHILD_V in manifest and CHILD_V not in s_f
d = dem_f[CHILD]
parents = []
for s5, rows in rem_f.items():
    hexes = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in rows}
    if CHILD in hexes:
        parents.append({"s5_hex": s5, "rows": len(rows),
                       "edge_cost": sum(hexes.values()),
                       "child_edge_cost": hexes[CHILD]})
del_orbits = {s: f"{canon(CHILD_V & ~(1 << s)):032x}"
              for s in [i for i in range(121) if (CHILD_V >> i) & 1]}
lifts = {}
for p in parents:
    lifts[p["s5_hex"]] = [s for s, o in del_orbits.items() if o == p["s5_hex"]]
closed_del = {s: o for s, o in del_orbits.items()
              if o not in {p["s5_hex"] for p in parents}}
st, cand = legal_candidates(CHILD)
result = {
    "chain_head": [st_f["solved_s6_in_manifest"], st_f["unique_remaining_s6"],
                   st_f["sum_remaining_cost"], st_f["s6_needed_by_open_classes"],
                   st_f["cost_needed_by_open_classes"]],
    "child": CHILD,
    "child_stones": st,
    "demand": {"c1": d["c1"], "c2": d["c2"], "c4": d["c4"]},
    "parents": parents,
    "lifts": lifts,
    "closed_deletion_orbits": closed_del,
    "legal_candidates": cand,
    "candidate_count": len(cand),
}
print(json.dumps(result, indent=1))
