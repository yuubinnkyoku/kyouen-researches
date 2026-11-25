"""Minimal GF(9) / PG(2,9) core, Python standard library only.

Field encoding used internally ("canonical"): the integer n in 0..8 codes the
field element a + b*i, where i^2 = -1 = 2, with
    a = n % 3,  b = n // 3,   i.e.  n = a + 3*b.
The constant 1 is therefore the integer 1, which is the pair (1,0).
"""


# ---------------------------------------------------------------- GF(9) tables
def _add(x, y):
    return (x % 3 + y % 3) % 3 + 3 * ((x // 3 + y // 3) % 3)


def _mul(x, y):
    a, b = x % 3, x // 3
    c, d = y % 3, y // 3
    return (a * c - b * d) % 3 + 3 * ((a * d + b * c) % 3)


ADD = [[_add(x, y) for y in range(9)] for x in range(9)]
MUL = [[_mul(x, y) for y in range(9)] for x in range(9)]
NEG = [0 if x == 0 else (3 - x % 3) % 3 + 3 * ((3 - x // 3) % 3) for x in range(9)]
INV = [None] + [next(y for y in range(1, 9) if MUL[x][y] == 1) for x in range(1, 9)]
ZERO, ONE = 0, 1


def sub(x, y):
    return ADD[x][NEG[y]]


def cube(x):
    return MUL[MUL[x][x]][x]


def field_checks():
    """Verify that the tables are a field (associativity, distributivity,
    identities, inverses, characteristic 3)."""
    ok = True
    notes = []
    for x in range(9):
        for y in range(9):
            for z in range(9):
                if ADD[ADD[x][y]][z] != ADD[x][ADD[y][z]]:
                    ok = False
                    notes.append(("add-assoc", x, y, z))
                if MUL[MUL[x][y]][z] != MUL[x][MUL[y][z]]:
                    ok = False
                    notes.append(("mul-assoc", x, y, z))
                if MUL[x][ADD[y][z]] != ADD[MUL[x][y]][MUL[x][z]]:
                    ok = False
                    notes.append(("distrib", x, y, z))
    for x in range(9):
        if ADD[x][ZERO] != x or MUL[x][ONE] != x:
            ok = False
            notes.append(("identity", x))
        if x != 0 and MUL[x][INV[x]] != ONE:
            ok = False
            notes.append(("inverse", x))
        if ADD[x][ADD[x][x]] != ZERO:          # 3*x = 0  (characteristic 3)
            ok = False
            notes.append(("char3", x))
    # i^2 = -1, and t^2+1 must be irreducible over GF(3) (no root in 0,1,2)
    if MUL[3][3] != NEG[ONE]:
        ok = False
        notes.append(("i^2 != -1", MUL[3][3]))
    for x in (0, 1, 2):
        if ADD[MUL[x][x]][ONE] == ZERO:
            ok = False
            notes.append(("x^2+1 has root in GF(3)", x))
    # 9 = 3^2 elements, and the 8 nonzero elements form a cyclic group
    nz = list(range(1, 9))
    g = None
    for cand in nz:
        seen, cur = set(), cand
        for _ in range(8):
            seen.add(cur)
            cur = MUL[cur][cand]
        if len(seen) == 8:
            g = cand
            break
    if g is None:
        ok = False
        notes.append(("no primitive element",))
    return ok, notes[:10]


# --------------------------------------------------------- projective geometry
def normalise(v):
    """Normalise a nonzero triple (x,y,z) so that its first nonzero entry is 1."""
    x, y, z = v
    for c in (x, y, z):
        if c != 0:
            iv = INV[c]
            return ((MUL[iv][x], MUL[iv][y], MUL[iv][z]))
    raise ValueError("zero vector")


def all_points():
    """All 91 points of PG(2,9) as normalised triples, in a canonical order."""
    pts = []
    for x in range(9):
        for y in range(9):
            for z in range(9):
                if (x, y, z) == (0, 0, 0):
                    continue
                p = normalise((x, y, z))
                if p not in pts:
                    pts.append(p)
    return pts


def det3(u, v, w):
    """Determinant of the 3x3 matrix with rows u, v, w over GF(9)."""
    (a, b, c), (d, e, f), (g, h, i) = u, v, w
    t1 = MUL[a][sub(MUL[e][i], MUL[f][h])]
    t2 = MUL[b][sub(MUL[d][i], MUL[f][g])]
    t3 = MUL[c][sub(MUL[d][h], MUL[e][g])]
    return ADD[sub(t1, t2)][t3]


def all_lines(points):
    """All 91 lines of PG(2,9) as frozensets of point indices (indices into
    `points`)."""
    n = len(points)
    lines = set()
    for i in range(n):
        for j in range(i + 1, n):
            mem = frozenset(k for k in range(n)
                            if det3(points[i], points[j], points[k]) == 0)
            if len(mem) != 10:
                raise AssertionError("degenerate line %r" % (mem,))
            lines.add(mem)
    return sorted(lines, key=lambda s: sorted(s))


def point_order_of(coords, points):
    """Map a coordinate triple to its index in `points`."""
    return {p: i for i, p in enumerate(points)}


# --------------------------------------------------------------- board loading
def load_board(path):
    with open(path, "r", encoding="utf-8") as fh:
        lines = [ln.strip() for ln in fh if ln.strip()]
    npoints, nlines = map(int, lines[0].split())
    rows = []
    for ln in lines[1:]:
        parts = list(map(int, ln.split()))
        assert parts[0] == len(parts) - 1, ln
        rows.append(parts[1:])
    return npoints, nlines, rows
