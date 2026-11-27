"""Task 1: verify the board file really is AG(2,7).

Checks:
  * literal shape (49 points, 56 lines, 7 distinct points per line);
  * every unordered pair of distinct points lies on exactly one line;
  * every point lies on 8 lines;
  * the 56 lines split into 8 parallel classes of 7 disjoint lines;
  * explicit affine coordinatisation: a bijection points -> F_7^2 is searched
    for such that all 56 board lines become exactly the 56 affine lines.
The last check is an explicit isomorphism to AG(2,7), not just an axiom check.
"""

import json
from itertools import permutations

from boardlib import Board, HERE, REPO, read_board

N, M, BLOCKS = read_board()
board = Board(N, BLOCKS)
result = {"pass": False, "checks": {}}
checks = result["checks"]


def check(name, cond, detail=""):
    checks[name] = {"pass": bool(cond), "detail": detail}
    return cond


# ---------------------------------------------------------------- literal shape
check("v=49", N == 49, f"n={N}")
check("b=56", M == 56, f"m={M}")
check("line size 7", all(len(B) == 7 for B in BLOCKS),
      "sizes=" + str(sorted({len(B) for B in BLOCKS})))
check("points in range", all(0 <= p < N for B in BLOCKS for p in B), "")
check("points distinct within line", all(len(set(B)) == 7 for B in BLOCKS), "")
check("no duplicate lines", len({frozenset(B) for B in BLOCKS}) == M, "")

# ------------------------------------------------------------- pair-once axiom
pair_count = [[0] * N for _ in range(N)]
line_sets = [frozenset(B) for B in BLOCKS]
for B in BLOCKS:
    for i, a in enumerate(B):
        for b in B[i + 1:]:
            pair_count[a][b] += 1
            pair_count[b][a] += 1
bad_pairs = [(a, b, pair_count[a][b])
             for a in range(N) for b in range(a + 1, N) if pair_count[a][b] != 1]
check("each pair on exactly one line", not bad_pairs,
      f"violations={len(bad_pairs)}" + (f" first={bad_pairs[0]}" if bad_pairs else ""))

# point degree and line intersections
degrees = [len(board.lines_through[p]) for p in range(N)]
check("every point on 8 lines", set(degrees) == {8}, f"degrees={sorted(set(degrees))}")
meet_ok = True
for i in range(M):
    for j in range(i + 1, M):
        inter = line_sets[i] & line_sets[j]
        if len(inter) not in (0, 1):
            meet_ok = False
check("two lines meet in 0 or 1 point", meet_ok, "")

# -------------------------------------------------------------- parallel classes
disjoint = [[] for _ in range(M)]
for i in range(M):
    for j in range(M):
        if i != j and not (line_sets[i] & line_sets[j]):
            disjoint[i].append(j)
check("each line parallel to 6 others", all(len(d) == 6 for d in disjoint),
      f"counts={sorted({len(d) for d in disjoint})}")

classes = []
class_of = [-1] * M
for i in range(M):
    if class_of[i] != -1:
        continue
    cls = [i] + disjoint[i]
    for li in cls:
        class_of[li] = len(classes)
    classes.append(cls)
check("8 parallel classes", len(classes) == 8, f"got {len(classes)}")
check("each class has 7 lines", all(len(c) == 7 for c in classes),
      f"sizes={sorted(len(c) for c in classes)}")
check("parallel classes partition 56 lines",
      sorted(li for c in classes for li in c) == list(range(M)), "")
part_ok = True
for c in classes:
    pts = set()
    for li in c:
        if pts & line_sets[li]:
            part_ok = False
        pts |= line_sets[li]
    if len(pts) != N:
        part_ok = False
check("each class partitions the 49 points", part_ok, "")
check("distinct classes are not parallel",
      all(not (line_sets[classes[a][0]] & line_sets[classes[b][0]] == set())
          for a in range(len(classes)) for b in range(a + 1, len(classes))), "")

# resolution: mapping point -> line inside a class
class_point_line = []
for c in classes:
    mp = [-1] * N
    for li in c:
        for p in BLOCKS[li]:
            mp[p] = li
    class_point_line.append(mp)

# ------------------------------------------------------------------- coordinates
# Axes: two distinct lines through point 0.
through0 = board.lines_through[0]
check("8 lines through point 0", len(through0) == 8, f"{len(through0)}")
Lx_i, Ly_i = through0[0], through0[1]
Lx = list(BLOCKS[Lx_i])
Ly = list(BLOCKS[Ly_i])
Lx = [0] + [p for p in Lx if p != 0]
Ly = [0] + [p for p in Ly if p != 0]
ix = {p: i for i, p in enumerate(Lx)}
iy = {p: i for i, p in enumerate(Ly)}
Lx_set, Ly_set = set(Lx), set(Ly)
cls_x, cls_y = class_of[Lx_i], class_of[Ly_i]


def intersect(li, lj):
    inter = line_sets[li] & line_sets[lj]
    assert len(inter) == 1, (li, lj, inter)
    return next(iter(inter))


# target_lx[p]: point of Lx on the line through p parallel to Ly
target_lx = []
for p in range(N):
    if p in Lx_set:
        target_lx.append(p)
    else:
        li = class_point_line[cls_y][p]
        target_lx.append(intersect(li, Lx_i))
# target_ly[p]: point of Ly on the line through p parallel to Lx
target_ly = []
for p in range(N):
    if p in Ly_set:
        target_ly.append(p)
    else:
        li = class_point_line[cls_x][p]
        target_ly.append(intersect(li, Ly_i))

x_index = [ix[target_lx[p]] for p in range(N)]
y_index = [iy[target_ly[p]] for p in range(N)]

# A line M0 not through 0 and parallel to neither axis, used to pin down the
# y-axis labels: for every candidate affine equation y = m*x + c of M0 the
# labels of the 7 points of Ly are forced.
M0 = None
for li, B in enumerate(BLOCKS):
    if 0 in B:
        continue
    if class_of[li] in (cls_x, cls_y):
        continue
    M0 = li
    break
check("reference line M0 found", M0 is not None, "")

F7 = range(7)


def check_coords(xc, yc):
    """Return the set of image lines if all images are affine lines, else None."""
    images = []
    for B in BLOCKS:
        pts = [(xc[p], yc[p]) for p in B]
        xs = {x for x, _ in pts}
        if len(xs) == 1:
            ys = [y for _, y in pts]
            if len(set(ys)) != 7:
                return None
        else:
            if len(xs) != 7:
                return None
            x0, y0 = pts[0]
            x1, y1 = pts[1]
            if x0 == x1:
                return None
            a = ((y1 - y0) * pow(x1 - x0, -1, 7)) % 7
            b = (y0 - a * x0) % 7
            for x, y in pts:
                if (a * x + b) % 7 != y:
                    return None
        images.append(frozenset(pts))
    return set(images)


canonical = set()
for c in F7:
    canonical.add(frozenset((c, y) for y in F7))
for a in F7:
    for b in F7:
        canonical.add(frozenset((x, (a * x + b) % 7) for x in F7))
check("canonical AG(2,7) has 56 lines", len(canonical) == 56, f"{len(canonical)}")

found = None
tried = 0
M0_points = list(BLOCKS[M0])
for tail in permutations(range(1, 7)):
    lx = [0] + list(tail)
    xc = [lx[x_index[p]] for p in range(N)]
    for m in range(1, 7):
        for c in F7:
            ly = [None] * 7
            ok = True
            for P in M0_points:
                val = (m * xc[P] + c) % 7
                qi = y_index[P]
                if ly[qi] is not None and ly[qi] != val:
                    ok = False
                    break
                ly[qi] = val
            if not ok or any(v is None for v in ly):
                continue
            if sorted(ly) != list(F7):
                continue
            yc = [ly[y_index[p]] for p in range(N)]
            tried += 1
            images = check_coords(xc, yc)
            if images is not None and images == canonical:
                found = {"lx": lx, "ly": ly, "m": m, "c": c,
                         "bijection": len({(xc[p], yc[p]) for p in range(N)}) == N}
                break
        if found:
            break
    if found:
        break

check("explicit AG(2,7) coordinatisation found", found is not None,
      f"candidate checks={tried}, found={found}")
if found:
    check("coordinate map is a bijection", found["bijection"], "")

result["pass"] = all(v["pass"] for v in checks.values())
(HERE / "task1_board.json").write_text(json.dumps(result, indent=2, sort_keys=True),
                                       encoding="utf-8")
print(json.dumps(result, indent=2, sort_keys=True))
if not result["pass"]:
    raise SystemExit(1)
