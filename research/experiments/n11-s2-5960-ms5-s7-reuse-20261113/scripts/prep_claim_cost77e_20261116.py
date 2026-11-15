#!/usr/bin/env python3
"""Extract the cost-77e child facts at the reconciled canonical head 1405 for the in-flight claim.

Child: 00000000040000809002000000004000 (the cost-77 row of the second coverable
class-2 candidate S5 00000000000000801202000040000000, unswept and unclaimed on
latest main as of this claim).
"""
import json
import runpy
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
sys.path.insert(0, str(HERE / "scripts"))
from legal_candidates import legal_candidates

CHILD = "00000000040000809002000000004000"
CHILD_V = int(CHILD, 16)

ns = runpy.run_path(str(HERE / "scripts" /
                        "recompute_frontier_reconcile_canonical1400_cost70g_20261116.py"))
rem_new = ns["rem_new"]
dem_new = ns["dem_new"]
manifest = ns["manifest"]
canon = ns["canon"]
st_new = ns["st_new"]
rem_hexes = {r["s6_hex"] for rows in rem_new.values() for r in rows}
assert CHILD_V in manifest and CHILD in rem_hexes and CHILD_V not in ns["s_new"], \
    "the child must be a remaining (unsolved) manifest row at head 1405"
d = dem_new[CHILD]
parents = []
for s5, rows in rem_new.items():
    hexes = {r["s6_hex"] for r in rows}
    if CHILD in hexes:
        cost = sum(int(r["s6_s7_edge_cost"]) for r in rows)
        parents.append({"s5_hex": s5, "rows": len(rows), "edge_cost": cost})
del_orbits = {s: f"{canon(CHILD_V & ~(1 << s)):032x}"
              for s in [i for i in range(121) if (CHILD_V >> i) & 1]}
lifts = {}
for p in parents:
    lifts[p["s5_hex"]] = [s for s, o in del_orbits.items() if o == p["s5_hex"]]
closed_del = {s: o for s, o in del_orbits.items()
              if o not in {p["s5_hex"] for p in parents}}
st, cand = legal_candidates(CHILD)
result = {
    "chain_head": [st_new["solved_s6_in_manifest"], st_new["unique_remaining_s6"],
                   st_new["sum_remaining_cost"], st_new["s6_needed_by_open_classes"],
                   st_new["cost_needed_by_open_classes"]],
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
