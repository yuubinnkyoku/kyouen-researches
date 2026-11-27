#!/usr/bin/env python3
"""Independent verification that board_ag2q5.txt is the affine plane AG(2,5).

Checks (all from first principles, standard library only):
  1. header "25 30"; 30 lines, each a 5-element subset of {0..24}; no duplicates;
     every point lies on exactly 6 lines.
  2. every unordered pair of distinct points lies on exactly one line.
  3. the "disjoint or equal" relation on lines has exactly 6 parallel classes,
     each of 5 lines, each class a partition of the 25 points (parallelism).
  4. explicit affine coordinates: choose O = point 0, two independent lines
     through O as axes, and brute-force the affine labelling of each axis; the
     30 board lines must be exactly {x=c}, {y=c}, {y=m*x+c} in F_5^2.
     A valid labelling is a constructive certificate that the board is AG(2,5),
     not merely a 2-(25,5,1) design.

Exit code 0 iff every check passes.
"""
import itertools
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
BOARD = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    ROOT, "research", "experiments", "s-parameter-kyouen-20261125",
    "output", "board_ag2q5.txt")

fail = []


def check(cond, msg):
    if not cond:
        fail.append(msg)
    return bool(cond)


def parse(path):
    with open(path, "r", encoding="utf-8") as f:
        tokens = f.read().split()
    it = iter(tokens)
    n = int(next(it))
    b = int(next(it))
    lines = []
    for _ in range(b):
        ln = int(next(it))
        lines.append([int(next(it)) for _ in range(ln)])
    return n, b, lines, list(it)


n, b, lines, leftover = parse(BOARD)
print(f"parsed: n={n} b={b}")
check(not leftover, f"trailing tokens after {b} lines: {leftover}")

# ---- 1. basic design axioms -------------------------------------------------
check(n == 25, f"n != 25 (got {n})")
check(b == 30, f"b != 30 (got {b})")
check(all(len(L) == 5 for L in lines), "some line does not have 5 points")
check(all(len(set(L)) == 5 for L in lines), "some line repeats a point")
check(all(0 <= p < n for L in lines for p in L), "point id out of range")

line_sets = [frozenset(L) for L in lines]
check(len(set(line_sets)) == b, "duplicate lines")

deg = [0] * n
for L in lines:
    for p in L:
        deg[p] += 1
check(all(d == 6 for d in deg), f"point degrees not all 6: {sorted(set(deg))}")

# ---- 2. every pair on exactly one line -------------------------------------
pair_count = {}
for L in lines:
    for a, c in itertools.combinations(sorted(L), 2):
        pair_count[(a, c)] = pair_count.get((a, c), 0) + 1
expected_pairs = n * (n - 1) // 2
check(len(pair_count) == expected_pairs,
      f"covered pairs {len(pair_count)} != {expected_pairs}")
bad = {k: v for k, v in pair_count.items() if v != 1}
check(not bad, f"pairs not on exactly one line: {list(bad)[:10]}")

# ---- 3. parallel classes ----------------------------------------------------
parent = list(range(b))


def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


for i, j in itertools.combinations(range(b), 2):
    if line_sets[i].isdisjoint(line_sets[j]):
        ri, rj = find(i), find(j)
        parent[rj] = ri
classes = {}
for i in range(b):
    classes.setdefault(find(i), []).append(i)
class_list = sorted((sorted(v) for v in classes.values()), key=lambda v: v[0])
print("parallel classes (line indices):", class_list)
check(len(class_list) == 6, f"expected 6 parallel classes, got {len(class_list)}")
check(all(len(c) == 5 for c in class_list),
      "some parallel class does not have 5 lines")
for ci, cls in enumerate(class_list):
    cover = []
    for li in cls:
        cover.extend(lines[li])
    check(sorted(cover) == list(range(n)),
          f"parallel class {ci} is not a partition of the point set")
for ci in range(len(class_list)):
    for cj in range(ci + 1, len(class_list)):
        for li in class_list[ci]:
            for lj in class_list[cj]:
                check(len(line_sets[li] & line_sets[lj]) == 1,
                      f"lines {li},{lj} from distinct classes do not meet once")

# ---- 4. explicit affine coordinates -> AG(2,5) ------------------------------
through_O = [li for li in range(b) if 0 in line_sets[li]]
check(len(through_O) == 6, f"expected 6 lines through point 0, got {len(through_O)}")
dir_of = {}
for ci, cls in enumerate(class_list):
    for li in cls:
        dir_of[li] = ci

ax1 = ax2 = None
for li, lj in itertools.combinations(through_O, 2):
    if dir_of[li] != dir_of[lj]:
        ax1, ax2 = li, lj
        break
check(ax1 is not None, "no two independent lines through O")
e1 = min(p for p in lines[ax1] if p != 0)
e2 = min(p for p in lines[ax2] if p != 0)
print(f"affine frame: O=0, e1={e1} (line {ax1}), e2={e2} (line {ax2})")


def parallel_through(p, line_idx):
    hits = [li for li in class_list[dir_of[line_idx]] if p in line_sets[li]]
    assert len(hits) == 1, (p, line_idx, hits)
    return hits[0]


def meet(l1, l2):
    pts = line_sets[l1] & line_sets[l2]
    assert len(pts) == 1, (l1, l2, pts)
    return next(iter(pts))


def coord_map(order1, order2):
    m = {}
    for x, px in enumerate(order1):
        lp = parallel_through(px, ax2)      # through p_x, parallel to ax2
        for y, qy in enumerate(order2):
            lq = parallel_through(qy, ax1)  # through q_y, parallel to ax1
            m[(x, y)] = meet(lp, lq)
    return m


def line_type(pts):
    xs = {p[0] for p in pts}
    if len(xs) == 1:
        return ("x", next(iter(xs)))
    pts = sorted(pts)
    (x0, y0), (x1, y1) = pts[0], pts[1]
    m = ((y1 - y0) * pow((x1 - x0) % 5, -1, 5)) % 5
    c = (y0 - m * x0) % 5
    if all((m * x + c) % 5 == y for x, y in pts):
        return ("m", m, c)
    return None


expected_types = set()
for c in range(5):
    expected_types.add(("x", c))
for m in range(5):
    for c in range(5):
        expected_types.add(("m", m, c))

order1_opts = [(0,) + perm for perm in
               itertools.permutations([p for p in lines[ax1] if p != 0])]
order2_opts = [(0,) + perm for perm in
               itertools.permutations([p for p in lines[ax2] if p != 0])]

witness = None
for o1 in order1_opts:
    for o2 in order2_opts:
        cm = coord_map(o1, o2)
        if len(set(cm.values())) != 25:
            continue
        inv = {p: xy for xy, p in cm.items()}
        types = [line_type([inv[p] for p in L]) for L in lines]
        if all(t is not None for t in types) and set(types) == expected_types:
            witness = (o1, o2, types, cm)
            break
    if witness:
        break

check(witness is not None,
      "no affine frame/coordinate ordering realises the 30 lines as AG(2,5) lines")
if witness:
    o1, o2, types, cm = witness
    print(f"affine order on axis1: {o1}")
    print(f"affine order on axis2: {o2}")
    print("all 30 lines are exactly the AG(2,5) lines "
          "{x=c}, {y=c}, {y=mx+c}")
    fam_ok = True
    for ci, cls in enumerate(class_list):
        fams = {types[li][0] if types[li][0] != "m" else "m" for li in cls}
        if len(fams) != 1:
            fam_ok = False
    check(fam_ok, "a parallel class mixes equation families")
    with open(os.path.join(HERE, "board_affine_map.json"), "w",
              encoding="utf-8") as f:
        json.dump({
            "board": os.path.relpath(BOARD, ROOT).replace("\\", "/"),
            "O": 0, "e1": e1, "e2": e2,
            "axis1_line": ax1, "axis2_line": ax2,
            "axis1_order": list(o1), "axis2_order": list(o2),
            "line_equations": {
                " ".join(str(x) for x in sorted(L)): list(t)
                for L, t in zip(lines, types)
            },
            "point_coords": {str(p): list(xy) for xy, p in cm.items()},
        }, f, indent=1, ensure_ascii=False)
    print("wrote board_affine_map.json")

print()
if fail:
    print(f"BOARD VERIFICATION: FAIL ({len(fail)} problems)")
    for m in fail:
        print("  -", m)
    sys.exit(1)
print("BOARD VERIFICATION: PASS")
print("  25 points, 30 lines of 5, every pair on exactly one line,")
print("  6 parallel classes of 5 lines (each a point partition),")
print("  explicit affine coordinates: board = AG(2,5).")
