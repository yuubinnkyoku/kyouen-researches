#!/usr/bin/env python3
"""Prep the cost-60c claim: the unswept edge-60 child
00000000000000003800000008008020 at the post-cost-75e canonical head
1407/174/6441/509300/4711/373023.

Motivation (cross-cover lane): this child is a one-stone-replacement
neighbor of the STERILE cost-70j child 00000000000000801282000000200000
(a remaining row of the best coverable class-2 S5
00000000000000801202000000200000, 3 rows / 209, all three rows STERILE by
their own-row sweeps).  Exactly one of this child's 60 legal candidate
roots (bit 119) covers the 70j child; a WIN7-D10 verdict for that root
closes the 70j row via the standard marginal mechanism.

Reproduces the published cost-75e fold end-to-end, then re-derives the
child's open parents, demand and legal candidates at 1407.  Bookkeeping
only; 11x11 empty board / two-stone root {49,60} / S2 {59,60} / class 1 /
class 2 / class 4 remain UNKNOWN.
"""
import json
import runpy
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"

CHILD = "00000000000000003800000008008020"
PARENT_BEST = "00000000000000801202000000200000"
TARGET_70J = "00000000000000801282000000200000"

ns = runpy.run_path(str(HERE / "scripts" /
                         "recompute_frontier_cost75e_receipts_20261116.py"))
s_after = set(ns["s_after"])
rem = ns["rem_after"]
dem = ns["dem_after"]
classes = ns["classes"]
canon = ns["canon"]
manifest = ns["manifest"]
st_after = ns["st_after"]
assert (st_after["solved_s6_in_manifest"], st_after["remaining_s5_orbits"],
        st_after["unique_remaining_s6"], st_after["sum_remaining_cost"],
        st_after["s6_needed_by_open_classes"],
        st_after["cost_needed_by_open_classes"]) == \
    (1407, 174, 6441, 509300, 4711, 373023)
cv = int(CHILD, 16)
assert cv in manifest and cv not in s_after, \
    "the child must be genuinely remaining at 1407"
stones = [s for s in range(121) if (cv >> s) & 1]
assert len(stones) == 6, stones

parents = []
deletions = {}
for s in stones:
    h = f"{canon(cv & ~(1 << s)):032x}"
    deletions[s] = h
    if h in rem:
        rows = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in rem[h]}
        assert CHILD in rows, (h, "an open parent must hold the child row")
        parents.append({
            "s5_hex": h, "classes_bitmask": classes.get(h, 0),
            "remaining_s6_orbits": len(rows),
            "remaining_s7_edge_cost": sum(rows.values()),
            "child_edge_cost": rows[CHILD], "lift_stone": s,
        })
d = dem[CHILD]
assert all(p["child_edge_cost"] == 60 for p in parents), parents
print("child", CHILD, "stones", stones)
print("deletions:", json.dumps(deletions, indent=1))
print("open parents at 1407:", json.dumps(parents, indent=1))
print("demand:", d)

# legal candidates (independent enumeration)
proc = subprocess.run(
    [sys.executable, str(HERE / "scripts" / "legal_candidates.py"), CHILD],
    capture_output=True, text=True, check=True)
lines = [x for x in proc.stdout.splitlines() if x.strip()]
tok = lines[0].split()
assert tok[1] == "occupied" and tok[2] == "6" \
    and tok[3] == "legal" and tok[4] == "60", lines[0]
cand = [int(x) for x in lines[1].split(",")]
print("legal candidates:", len(cand), cand)
assert len(cand) == 60, len(cand)

# cross-cover audit: exactly which candidate roots cover the STERILE
# 70j child (canonical covers: every 6-subset deletion canonicalized)
target = int(TARGET_70J, 16)
cover_bits = []
for b in cand:
    root = stones + [b]
    for s in root:
        v = 0
        for x in root:
            if x != s:
                v |= 1 << x
        if canon(v) == target:
            cover_bits.append(b)
            break
print("candidate roots covering the 70j child:", cover_bits)
assert cover_bits == [119], cover_bits
root_hex = format(cv | (1 << 119), "032x")
print("covering root (bit 119):", root_hex)

# the best coverable S5's remaining rows at 1407 (motivation / coordination)
best_rows = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in rem[PARENT_BEST]}
print("best coverable class-2 S5 rows at 1407:", json.dumps(
    {k: v for k, v in sorted(best_rows.items(), key=lambda kv: (kv[1], kv[0]))},
    indent=1))
