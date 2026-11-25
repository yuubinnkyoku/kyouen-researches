"""Cross-check of the key results with a SECOND, independent implementation of
GF(9): field elements are explicit pairs (a,b) meaning a + b*i with i^2 = -1,
all operations written out by hand (no lookup tables, no reuse of pg.py's
tables).  Point/line/vector/matrix code is also rewritten here.

Checked again from scratch:
  * the coordinate map reproduces the board's 91 lines        (Task 1)
  * {0,1,10,20} is a 4-cap and has exactly 42 extensions      (Task 2)
  * the witness matrix M = (8,0,4,5,0,4,5,5,2) really maps
    {0,1,10,20,31} onto {0,1,10,20,41}                        (the fusion)
  * a complete re-run of the 120-image search gives
    |Stab{0,1,10,20,31}| = 4 and no map {0,1,10,20,31} -> {0,1,10,20,42}

Run:  python independent_5caps/t7_indep_field.py
"""

from __future__ import annotations

import itertools
import sys

BOARD = None
try:  # board path, relative to this file
    import pathlib

    BOARD = pathlib.Path(__file__).resolve().parent.parent / "output" / "board_pg2q9.txt"
except Exception:  # pragma: no cover
    pass

RESULTS: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> bool:
    RESULTS.append((name, ok, detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  --  {detail}" if detail else ""))
    return ok


# ---------------------------------------------------------------- GF(9) pairs
F = tuple  # element = (a, b)
ZERO: F = (0, 0)
ONE: F = (1, 0)


def fadd(x, y):
    return ((x[0] + y[0]) % 3, (x[1] + y[1]) % 3)


def fneg(x):
    return ((-x[0]) % 3, (-x[1]) % 3)


def fsub(x, y):
    return fadd(x, fneg(y))


def fmul(x, y):
    # (a+bi)(c+di) = (ac - bd) + (ad + bc) i,  i^2 = -1
    return ((x[0] * y[0] - x[1] * y[1]) % 3, (x[0] * y[1] + x[1] * y[0]) % 3)


def finv(x):
    assert x != ZERO
    # 1/(a+bi) = (a-bi)/(a^2+b^2); note a^2+b^2 is 1 or 2 in GF(3), never 0
    n = (x[0] * x[0] + x[1] * x[1]) % 3
    ninv = {1: 1, 2: 2}[n]
    return ((x[0] * ninv) % 3, ((-x[1]) * ninv) % 3)


def fdiv(x, y):
    return fmul(x, finv(y))


assert fmul((0, 1), (0, 1)) == (2, 0)  # i^2 = -1 = 2
for x in [(a, b) for a in range(3) for b in range(3) if (a, b) != ZERO]:
    assert fmul(x, finv(x)) == ONE
# distributive / associative spot checks
els = [(a, b) for a in range(3) for b in range(3)]
for x in els:
    for y in els:
        for z in els:
            assert fmul(x, fadd(y, z)) == fadd(fmul(x, y), fmul(x, z))
print("GF(9) pair arithmetic: i^2 = -1, inverses, distributivity verified")

ENC2PAIR = {3 * a + b: (a, b) for a in range(3) for b in range(3)}


def pair(e):
    return ENC2PAIR[e]


# ------------------------------------------------------------------- points
def vdiv(v, c):
    return (fdiv(v[0], c), fdiv(v[1], c), fdiv(v[2], c))


def vnorm(v):
    for c in v:
        if c != ZERO:
            return vdiv(v, c)
    raise ValueError("zero vector")


def vcross(u, v):
    return (fsub(fmul(u[1], v[2]), fmul(u[2], v[1])),
            fsub(fmul(u[2], v[0]), fmul(u[0], v[2])),
            fsub(fmul(u[0], v[1]), fmul(u[1], v[0])))


def vdot(l, p):
    return fadd(fadd(fmul(l[0], p[0]), fmul(l[1], p[1])), fmul(l[2], p[2]))


POINTS = [(ZERO, ZERO, ONE)]
POINTS += [(ZERO, ONE, pair(j)) for j in range(9)]
POINTS += [(ONE, pair(p), pair(j)) for p in range(9) for j in range(9)]
INDEX = {vnorm(v): i for i, v in enumerate(POINTS)}
print(f"points built from the coordinate map: {len(INDEX)} distinct")
check("independent rebuild: 91 distinct points", len(INDEX) == 91 and len(POINTS) == 91)

# full set of lines as point-index sets
line_sets = set()
for i, j in itertools.combinations(range(91), 2):
    l = vnorm(vcross(POINTS[i], POINTS[j]))
    s = frozenset(k for k in range(91) if vdot(l, POINTS[k]) == ZERO)
    line_sets.add(s)
print(f"independent rebuild: {len(line_sets)} distinct lines")
rows = [ln.split() for ln in BOARD.read_text(encoding="utf-8").splitlines() if ln.strip()]
board = {frozenset(int(t) for t in r[1:]) for r in rows[1:]}
check("independent rebuild: 91 lines, all of size 10",
      len(line_sets) == 91 and all(len(s) == 10 for s in line_sets))
check("independent rebuild: computed lines == board lines", line_sets == board)

# ------------------------------------------------------------------- caps
def is_cap(pts):
    for t in itertools.combinations(pts, 3):
        if vdot(vnorm(vcross(POINTS[t[0]], POINTS[t[1]])), POINTS[t[2]]) == ZERO:
            return False
    return True


FRAME = [0, 1, 10, 20]
check("independent rebuild: frame {0,1,10,20} is a 4-cap", is_cap(FRAME))


def secants(pts):
    s = set()
    for a, b in itertools.combinations(pts, 2):
        l = vnorm(vcross(POINTS[a], POINTS[b]))
        for k in range(91):
            if vdot(l, POINTS[k]) == ZERO:
                s.add(k)
    return s


cov = secants(FRAME)
ext = sorted(set(range(91)) - cov)
print(f"independent rebuild: |secant cover| = {len(cov)}, extensions = {len(ext)}")
check("independent rebuild: exactly 42 extensions of the frame", len(ext) == 42)
check("independent rebuild: all three representatives are 5-caps",
      all(is_cap(FRAME + [p]) for p in (31, 42, 41)))

# --------------------------------------------------- matrices over the pairs
def mat(rows_):
    return tuple(tuple(pair(c) for c in r) for r in rows_)


def mat_vec(M, v):
    return tuple(fadd(fadd(fmul(M[i][0], v[0]), fmul(M[i][1], v[1])), fmul(M[i][2], v[2]))
                 for i in range(3))


def det(M):
    t1 = fmul(M[0][0], fsub(fmul(M[1][1], M[2][2]), fmul(M[1][2], M[2][1])))
    t2 = fmul(M[0][1], fsub(fmul(M[1][0], M[2][2]), fmul(M[1][2], M[2][0])))
    t3 = fmul(M[0][2], fsub(fmul(M[1][0], M[2][1]), fmul(M[1][1], M[2][0])))
    return fadd(fsub(t1, t2), t3)


def inv3(M):
    a = [list(M[i]) + [ONE if i == j else ZERO for j in range(3)] for i in range(3)]
    for col in range(3):
        piv = next(i for i in range(col, 3) if a[i][col] != ZERO)
        a[col], a[piv] = a[piv], a[col]
        f = finv(a[col][col])
        a[col] = [fmul(f, x) for x in a[col]]
        for i in range(3):
            if i != col and a[i][col] != ZERO:
                g = a[i][col]
                a[i] = [fsub(a[i][k], fmul(g, a[col][k])) for k in range(6)]
    return tuple(tuple(a[i][3 + j] for j in range(3)) for i in range(3))


def solve3(cols, target):
    A = tuple(tuple(cols[j][i] for j in range(3)) for i in range(3))
    Ai = inv3(A)
    return tuple(fadd(fadd(fmul(Ai[i][0], target[0]), fmul(Ai[i][1], target[1])),
                      fmul(Ai[i][2], target[2])) for i in range(3))


def proj_from_frames(src4, tgt4):
    a, b = list(src4), list(tgt4)
    c = solve3(a[:3], a[3])
    d = solve3(b[:3], b[3])
    lam = [fdiv(d[i], c[i]) for i in range(3)]
    A = tuple(tuple(a[j][i] for j in range(3)) for i in range(3))
    Ai = inv3(A)
    B = tuple(tuple(b[j][i] for j in range(3)) for i in range(3))
    Bd = tuple(tuple(fmul(B[i][j], lam[j]) for j in range(3)) for i in range(3))
    M = tuple(tuple(fadd(fadd(fmul(Bd[i][0], Ai[0][j]), fmul(Bd[i][1], Ai[1][j])),
                         fmul(Bd[i][2], Ai[2][j])) for j in range(3)) for i in range(3))
    for k in range(4):
        assert vnorm(mat_vec(M, a[k])) == vnorm(b[k])
    return M


def images(M, pts):
    return frozenset(INDEX[vnorm(mat_vec(M, POINTS[p]))] for p in pts)


# --- the witness map (entries are the encoded values from the main search) --
W = mat([[8, 0, 4], [5, 0, 4], [5, 5, 2]])
print(f"\nwitness M = (8,0,4,5,0,4,5,5,2): det = {det(W)}, "
      f"det != 0: {det(W) != ZERO}")
print(f"  images of {FRAME + [31]}: {sorted(images(W, FRAME + [31]))}")
check("independent field: the witness maps {0,1,10,20,31} onto {0,1,10,20,41}",
      det(W) != ZERO and images(W, FRAME + [31]) == frozenset([0, 1, 10, 20, 41]))
check("independent field: witness does not preserve the frame "
      "(it maps it to {0,10,20,41})", images(W, FRAME) != frozenset(FRAME))

# --- complete 120-image searches, independent code -------------------------
def find_map(src, tgt):
    a = [POINTS[p] for p in src[:4]]
    for b_idx in itertools.permutations(tgt, 4):
        M = proj_from_frames(a, [POINTS[p] for p in b_idx])
        if images(M, src) == frozenset(tgt):
            return M
    return None


R1, R2, R3 = FRAME + [31], FRAME + [42], FRAME + [41]
n_stab = 0
a1 = [POINTS[p] for p in R1[:4]]
for b_idx in itertools.permutations(R1, 4):
    M = proj_from_frames(a1, [POINTS[p] for p in b_idx])
    if images(M, R1) == frozenset(R1):
        n_stab += 1
print(f"\nindependent field: complete search -> |Stab({R1})| = {n_stab}")
check("independent field: |Stab{0,1,10,20,31}| = 4", n_stab == 4)
check("independent field: {0,1,10,20,31} -> {0,1,10,20,41} is EQUIVALENT",
      find_map(R1, R3) is not None)
check("independent field: {0,1,10,20,31} -> {0,1,10,20,42} is INEQUIVALENT",
      find_map(R1, R2) is None)

print("\nCROSS-CHECK:", "PASS" if all(ok for _, ok, _ in RESULTS) else "FAIL")
sys.exit(0 if all(ok for _, ok, _ in RESULTS) else 1)
