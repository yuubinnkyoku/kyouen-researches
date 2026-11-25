"""TASK 1 -- verify the board is PG(2,9) and the coordinate map is consistent.

Run:  python independent_5caps/t1_board.py
"""

from __future__ import annotations

import itertools
import sys

import pg

RESULTS: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> bool:
    RESULTS.append((name, ok, detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  --  {detail}" if detail else ""))
    return ok


board = pg.load_board()
print(f"board file: {pg.BOARD_PATH}")
print(f"  header '91 91'; {len(board)} lines, sizes {sorted({len(l) for l in board})}")
check("board has 91 lines of 10 points each", len(board) == 91 and all(len(l) == 10 for l in board))
check("board lines are 91 distinct point sets", len(set(board)) == 91)

# ---- projective-plane axioms directly on the board (order 9) --------------
pair_count = {}
for line in board:
    for a, b in itertools.combinations(sorted(line), 2):
        pair_count[(a, b)] = pair_count.get((a, b), 0) + 1
n_pairs = 91 * 90 // 2
check("every pair of points lies on exactly one board line",
      len(pair_count) == n_pairs and all(v == 1 for v in pair_count.values()),
      f"{len(pair_count)} pairs, max multiplicity {max(pair_count.values())}")

allpts = set(range(91))
check("board point set is {0..90} and lines cover it", set().union(*board) == allpts)

meet = {}
for l1, l2 in itertools.combinations(range(91), 2):
    inter = board[l1] & board[l2]
    meet[(l1, l2)] = len(inter)
check("every two board lines meet in exactly one point",
      all(v == 1 for v in meet.values()),
      f"min {min(meet.values())}, max {max(meet.values())}")
deg = {p: 0 for p in allpts}
for line in board:
    for p in line:
        deg[p] += 1
check("every point is on exactly 10 board lines", set(deg.values()) == {10})

# ---- rebuild PG(2,9) from the claimed coordinate map ---------------------
plane_report = {}
for reading in ("field_one", "literal"):
    pts = pg.point_vectors(reading)
    idx = {pg.vnorm(v) for v in pts}
    ok_distinct = len(idx) == 91
    plane = pg.Plane(pts)
    computed = {frozenset(pg.bitlist(m)) for m in plane.line_masks}
    ok_lines = computed == set(board)
    plane_report[reading] = (plane, ok_distinct, ok_lines, len(computed))
    print(f"reading '{reading}': 91 distinct points={ok_distinct}, "
          f"{len(computed)} computed lines, line set == board line set: {ok_lines}")

reading = "field_one" if plane_report["field_one"][2] else "literal"
plane, ok_distinct, ok_lines, ncomp = plane_report[reading]
print(f"--> coordinate map reading that reproduces the board: '{reading}'")
check("coordinate map yields 91 distinct points of PG(2,9)", ok_distinct)
check("computed line set equals the board line set", ok_lines,
      f"{ncomp} lines; reading='{reading}'")
check("computed model has 91 lines, each with exactly 10 points",
      ncomp == 91 and all(pg.bitlist(m).__len__() == 10 for m in plane.line_masks))
check("every pair of computed points spans exactly one computed line",
      all(plane.pair_line[a][b] >= 0 for a in range(91) for b in range(91) if a != b))
check("all nonzero 3-vectors of GF(9)^3 give the same 91 points",
      len({pg.vnorm(v) for v in itertools.product(range(9), repeat=3) if any(v)}) == 91)

# explicit spot-check of the index formula against the board
print("\nspot checks of the index -> coordinates map (encoded field elements):")
for i in (0, 1, 2, 10, 11, 19, 20, 31, 41, 42, 90):
    v = plane.vectors[i]
    line_id = plane.point_lines[i]
    print(f"  index {i:2d} -> {v}  (field {tuple(pg.field_name(c) for c in v)});"
          f" 10 lines through it: {len(line_id)}")

print("\nTASK 1:", "PASS" if all(ok for _, ok, _ in RESULTS) else "FAIL")
sys.exit(0 if all(ok for _, ok, _ in RESULTS) else 1)
