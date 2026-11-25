#!/usr/bin/env python3
"""Prep the cost-64c claim: the unswept edge-64 child
00000000000000003800000008002020 at the post-cost-60c canonical head
1410/174/6438/509109/4711/373023.

Motivation (cross-cover lane): this child is the cheapest unswept
one-stone-replacement neighbor of BOTH the STERILE cost-65k child
00000000020000801202000000200000 AND the STERILE cost-70j child
00000000000000801282000000200000 (both remaining rows of the best coverable
class-2 S5 00000000000000801202000000200000, 3 rows / 209, all three rows
STERILE by their own-row sweeps).  The cross-cover pre-check (nearest-
neighbor analysis at head 1410) found that of this child's 64 legal
candidate roots, bits 111 and 119 cover the 70j child and bit 119
additionally covers the 65k child - a WIN7-D10 verdict for bit 119 would
close BOTH STERILE rows via the standard marginal mechanism.

Reproduces the published cost-60c fold end-to-end (which internally
reproduces the cost-75e chain head 1407 byte-identically), then re-derives
the child's open parents, demand and legal candidates at 1410.
Bookkeeping only; 11x11 empty board / two-stone root {49,60} / S2 {59,60} /
class 1 / class 2 / class 4 remain UNKNOWN.
"""
import json
import runpy
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"

CHILD = "00000000000000003800000008002020"
PARENT_BEST = "00000000000000801202000000200000"
TARGET_65K = "00000000020000801202000000200000"
TARGET_70J = "00000000000000801282000000200000"

ns = runpy.run_path(str(HERE / "scripts" /
                         "recompute_frontier_cost60c_receipts_20261116.py"))
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
    (1410, 174, 6438, 509109, 4711, 373023), st_after
cv = int(CHILD, 16)
assert cv in manifest and cv not in s_after, \
    "the child must be genuinely remaining at 1410"
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
assert all(p["child_edge_cost"] == 64 for p in parents), parents
print("child", CHILD, "stones", stones)
print("deletions:", json.dumps(deletions, indent=1))
print("open parents at 1410:", json.dumps(parents, indent=1))
print("demand:", d)

# legal candidates (independent enumeration)
proc = subprocess.run(
    [sys.executable, str(HERE / "scripts" / "legal_candidates.py"), CHILD],
    capture_output=True, text=True, check=True)
lines = [x for x in proc.stdout.splitlines() if x.strip()]
tok = lines[0].split()
assert tok[1] == "occupied" and tok[2] == "6" \
    and tok[3] == "legal", lines[0]
n_cand = int(tok[4])
cand = [int(x) for x in lines[1].split(",")]
assert len(cand) == n_cand, (len(cand), n_cand)
print("legal candidates:", len(cand), cand)


def covers_of(bit):
    root = stones + [bit]
    dels = set()
    for s in root:
        v = 0
        for x in root:
            if x != s:
                v |= 1 << x
        dels.add(canon(v))
    return dels


cover_70j = [b for b in cand if int(TARGET_70J, 16) in covers_of(b)]
cover_65k = [b for b in cand if int(TARGET_65K, 16) in covers_of(b)]
print("candidate roots covering the 70j child:", cover_70j)
print("candidate roots covering the 65k child:", cover_65k)
assert cover_70j == [111, 119], cover_70j
assert cover_65k == [119], cover_65k

# the best coverable S5's remaining rows at 1410 (motivation / coordination)
best_rows = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in rem[PARENT_BEST]}
print("best coverable class-2 S5 rows at 1410:", json.dumps(
    {k: v for k, v in sorted(best_rows.items(),
                             key=lambda kv: (kv[1], kv[0]))}, indent=1))
