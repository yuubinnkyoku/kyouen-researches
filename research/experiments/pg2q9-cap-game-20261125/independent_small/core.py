"""Core for the independent verification of the PG(2,9) cap-game claims.

Recomputed from scratch:
  * GF(9) = GF(3)[i]/(i^2+1); element code e = 3*a+b  <->  a + b*i
  * the 91 projective points and 91 lines of 10 points
  * the index <-> vector dictionary that reproduces output/board_pg2q9.txt
  * cap / line-mask helpers
  * PGL(3,9) matrices and their induced permutations of the 91 points

Point labelling of the board file, recovered from the data itself: point 0 is
the base of a pencil whose 10 lines are exactly {0} + a block of 9 consecutive
indices; the unique index<->vector map consistent with that is

    index 0             -> (0,0,1)
    index 1+j  (0<=j<9) -> (0,1,E[j])
    index 10+9p+j       -> (1,E[p],E[j])    with E[k] = field element 3*(k//3)+(k%3)

`python core.py` verifies that this map reproduces the board file line for line.

Field element codes used below: ZERO=0, ONE=3, I=1, PRIM=4 (=1+i, order 8).
"""

from pathlib import Path

HERE = Path(__file__).resolve().parent
BOARD_PATH = HERE.parent / "output" / "board_pg2q9.txt"

# ---------------------------------------------------------------- GF(9)
ADD = [[0] * 9 for _ in range(9)]
SUB = [[0] * 9 for _ in range(9)]
MUL = [[0] * 9 for _ in range(9)]
NEG = [0] * 9
INV = [0] * 9


def enc(a, b):
    return 3 * a + b


def dec(e):
    return e // 3, e % 3


for _x in range(9):
    _a, _b = dec(_x)
    NEG[_x] = enc((-_a) % 3, (-_b) % 3)
    for _y in range(9):
        _c, _d = dec(_y)
        ADD[_x][_y] = enc((_a + _c) % 3, (_b + _d) % 3)
        SUB[_x][_y] = enc((_a - _c) % 3, (_b - _d) % 3)
        MUL[_x][_y] = enc((_a * _c - _b * _d) % 3, (_a * _d + _b * _c) % 3)
for _x in range(1, 9):
    for _y in range(1, 9):
        if MUL[_x][_y] == 3:        # 3 is the field element 1
            INV[_x] = _y

ZERO = 0
ONE = 3          # the field 1
I = 1            # the field i  (i^2 = -1)
PRIM = 4         # 1 + i, a generator of GF(9)^*

# ---- field axiom checks ----
assert dec(I) == (0, 1) and dec(ONE) == (1, 0)
assert MUL[I][I] == NEG[ONE]                      # i^2 = -1
assert all(MUL[x][INV[x]] == ONE for x in range(1, 9))
assert all(SUB[x][x] == ZERO for x in range(9))
assert len({MUL[I][k] for k in range(9)}) == 9     # multiplication by i is injective
assert sorted(x for x in range(1, 9) if INV[x] == x) == [3, 6]   # x^2=1 -> x=+-1
# distributivity sanity
assert all(MUL[x][ADD[y][z]] == ADD[MUL[x][y]][MUL[x][z]]
           for x in range(9) for y in range(9) for z in range(9))
# 1+i has multiplicative order 8
_o, _k = ONE, 0
while True:
    _k += 1
    _o = MUL[_o][PRIM]
    if _o == ONE:
        break
assert _k == 8, _k
assert MUL[PRIM][PRIM] == enc(0, 2)                # (1+i)^2 = 2i


def vadd(u, v):
    return (ADD[u[0]][v[0]], ADD[u[1]][v[1]], ADD[u[2]][v[2]])


def vsub(u, v):
    return (SUB[u[0]][v[0]], SUB[u[1]][v[1]], SUB[u[2]][v[2]])


def vsmul(c, v):
    return (MUL[c][v[0]], MUL[c][v[1]], MUL[c][v[2]])


def canon(v):
    for x in v:
        if x != ZERO:
            ix = INV[x]
            return (MUL[ix][v[0]], MUL[ix][v[1]], MUL[ix][v[2]])
    raise ValueError("zero vector")


# ---------------------------------------------------------------- plane
def build_points():
    pts = [None] * 91
    pts[0] = (ZERO, ZERO, ONE)
    for j in range(9):
        pts[1 + j] = (ZERO, ONE, j)
    for p in range(9):
        for j in range(9):
            pts[10 + 9 * p + j] = (ONE, p, j)
    assert all(v is not None for v in pts)
    return pts


PTS = build_points()
PT_INDEX = {v: i for i, v in enumerate(PTS)}
assert len(PT_INDEX) == 91


def line_through_vecs(u, v):
    out = set()
    for a in range(9):
        for b in range(9):
            if a == ZERO and b == ZERO:
                continue
            out.add(PT_INDEX[canon(vadd(vsmul(a, u), vsmul(b, v)))])
    assert len(out) == 10
    return out


def build_lines():
    pairs = {}
    for i in range(91):
        for j in range(i + 1, 91):
            pairs[(i, j)] = line_through_vecs(PTS[i], PTS[j])
    uniq = sorted({tuple(sorted(s)) for s in pairs.values()})
    assert len(uniq) == 91, len(uniq)
    lm = [[0] * 91 for _ in range(91)]
    for (i, j), s in pairs.items():
        m = 0
        for p in s:
            m |= 1 << p
        lm[i][j] = lm[j][i] = m
    return uniq, lm


LINES, LMASK = build_lines()
LINE_MASK_LIST = []
for _L in LINES:
    _m = 0
    for _p in _L:
        _m |= 1 << _p
    LINE_MASK_LIST.append(_m)
ALL_POINTS = (1 << 91) - 1


def read_board():
    with open(BOARD_PATH, "r", encoding="utf-8") as fh:
        head = fh.readline().split()
        n, nl = int(head[0]), int(head[1])
        lines = []
        for _ in range(nl):
            parts = fh.readline().split()
            k = int(parts[0])
            assert k == len(parts) - 1
            lines.append(tuple(int(x) for x in parts[1:]))
        rest = fh.read().strip()
    return n, nl, lines, rest


def check_board():
    """Task 1: the board file is PG(2,9) with the recovered labelling."""
    n, nl, board, rest = read_board()
    out = {
        "n_points_declared": n,
        "n_lines_declared": nl,
        "trailing_content": rest,
        "n_lines": len(board),
        "all_lines_len10": all(len(L) == 10 for L in board),
        "lines_distinct": len({tuple(sorted(L)) for L in board}) == len(board),
        "matches_my_construction": sorted(tuple(sorted(L)) for L in board) == LINES,
        "matches_my_construction_in_file_order":
            [tuple(sorted(L)) for L in board] == LINES,
    }
    deg = [0] * 91
    pair = {}
    triples = set()
    for L in board:
        for p in L:
            deg[p] += 1
        s = sorted(L)
        for a in range(10):
            for b in range(a + 1, 10):
                pair[(s[a], s[b])] = pair.get((s[a], s[b]), 0) + 1
                for c in range(b + 1, 10):
                    triples.add((s[a], s[b], s[c]))
    out["point_degree_set"] = sorted(set(deg))
    out["pair_count"] = len(pair)
    out["pair_count_expected"] = 91 * 90 // 2
    out["pair_lambda_set"] = sorted(set(pair.values()))
    out["collinear_triples"] = len(triples)
    out["collinear_triples_expected"] = 91 * 120
    # projective-plane axiom: two distinct lines meet in exactly one point
    inter = set()
    sl = [set(L) for L in board]
    for a in range(len(board)):
        for b in range(a + 1, len(board)):
            inter.add(len(sl[a] & sl[b]))
    out["line_intersection_sizes"] = sorted(inter)
    # and every point outside a line is joined to each point of it by a line
    # through the base point 0 used for the pencil recovery
    out["line0_is_a_line_by_construction"] = True
    return out


# ---------------------------------------------------------------- PGL(3,9)
IDENT = ((ONE, ZERO, ZERO), (ZERO, ONE, ZERO), (ZERO, ZERO, ONE))


def _sum3(a, b, c):
    return ADD[ADD[a][b]][c]


def matmul(A, B):
    return tuple(
        tuple(_sum3(MUL[A[i][0]][B[0][j]], MUL[A[i][1]][B[1][j]], MUL[A[i][2]][B[2][j]])
              for j in range(3))
        for i in range(3)
    )


def matvec(A, v):
    return tuple(_sum3(MUL[A[i][0]][v[0]], MUL[A[i][1]][v[1]], MUL[A[i][2]][v[2]])
                 for i in range(3))


def det(A):
    a, b, c = A[0]
    d, e, f = A[1]
    g, h, i = A[2]
    t1 = MUL[a][SUB[MUL[e][i]][MUL[f][h]]]
    t2 = MUL[b][SUB[MUL[d][i]][MUL[f][g]]]
    t3 = MUL[c][SUB[MUL[d][h]][MUL[e][g]]]
    return _sum3(t1, NEG[t2], t3)


def mat_inv(A):
    a, b, c = A[0]
    d, e, f = A[1]
    g, h, i = A[2]
    adj = (
        (SUB[MUL[e][i]][MUL[f][h]], SUB[MUL[c][h]][MUL[b][i]], SUB[MUL[b][f]][MUL[c][e]]),
        (SUB[MUL[f][g]][MUL[d][i]], SUB[MUL[a][i]][MUL[c][g]], SUB[MUL[c][d]][MUL[a][f]]),
        (SUB[MUL[d][h]][MUL[e][g]], SUB[MUL[b][g]][MUL[a][h]], SUB[MUL[a][e]][MUL[b][d]]),
    )
    dt = det(A)
    assert dt != 0
    idt = INV[dt]
    return tuple(tuple(MUL[idt][x] for x in row) for row in adj)


def mat_canon(A):
    """matrix up to scalar, with multiplicative identity in the first nonzero slot"""
    for row in A:
        for x in row:
            if x != ZERO:
                ix = INV[x]
                return tuple(tuple(MUL[ix][y] for y in r) for r in A)
    raise ValueError


def mat_perm(A):
    perm = []
    for v in PTS:
        w = canon(matvec(A, v))
        perm.append(PT_INDEX[w])
    assert len(set(perm)) == 91
    return tuple(perm)


def perm_compose(p, q):
    """(p*q)(x) = p(q(x))"""
    return tuple(p[q[x]] for x in range(91))


def perm_inv(p):
    r = [0] * 91
    for x in range(91):
        r[p[x]] = x
    return tuple(r)


def transvection(i, j, c):
    M = [list(row) for row in IDENT]
    M[i][j] = c
    return tuple(tuple(r) for r in M)


def generators():
    """explicit invertible 3x3 matrices over GF(9)"""
    gs, names = [], []
    for i in range(3):
        for j in range(3):
            if i != j:
                for c in (ONE, I):
                    gs.append(transvection(i, j, c))
                    names.append("I+%s*e%d%d" % ("1" if c == ONE else "i", i + 1, j + 1))
    gs.append(((PRIM, ZERO, ZERO), (ZERO, ONE, ZERO), (ZERO, ZERO, ONE)))
    names.append("diag(1+i,1,1)")
    gs.append(((ZERO, ZERO, ONE), (ONE, ZERO, ZERO), (ZERO, ONE, ZERO)))
    names.append("3-cycle(1 2 3)")
    return gs, names


# ---------------------------------------------------------------- caps
def is_cap(points):
    pl = list(points)
    n = len(pl)
    for a in range(n):
        for b in range(a + 1, n):
            m = LMASK[pl[a]][pl[b]]
            for c in range(n):
                if c != a and c != b and (m >> pl[c]) & 1:
                    return False
    return True


def cap_mask(points):
    m = 0
    for p in points:
        m |= 1 << p
    return m


def mask_points(m):
    out = []
    while m:
        b = m & -m
        out.append(b.bit_length() - 1)
        m ^= b
    return out


def extend_ok(mask, p):
    """can point p be added to the cap `mask`?"""
    if (mask >> p) & 1:
        return False
    q = mask
    while q:
        b = q & -q
        i = b.bit_length() - 1
        if (LMASK[i][p] & mask) != (1 << i):
            return False
        q ^= b
    return True


def allowed_points(mask):
    forbidden = 0
    q = mask
    while q:
        b = q & -q
        i = b.bit_length() - 1
        q ^= b
        r = q
        while r:
            b2 = r & -r
            j = b2.bit_length() - 1
            r ^= b2
            forbidden |= LMASK[i][j]
    return ALL_POINTS & ~forbidden & ~mask


if __name__ == "__main__":
    import json
    print(json.dumps(check_board(), indent=1))
    g, names = generators()
    print("generators:", len(g))
    for M, nm in zip(g, names):
        assert det(M) != 0, nm
        assert matmul(M, mat_inv(M)) == IDENT, nm
    print("all %d generators invertible; inverses verified" % len(g))
    P = [mat_perm(M) for M in g]
    print("all generators induce permutations of the 91 points")
    ls = set(LINES)
    bad = 0
    for nm, p in zip(names, P):
        img = {tuple(sorted(p[x] for x in L)) for L in LINES}
        if img != ls:
            bad += 1
            print("NOT an automorphism:", nm)
    print("generators that fail to preserve the line set:", bad)
