"""Independent reconstruction of PG(2,8) from the board file, plus GF(8),
point ranking, Frobenius, PGL(3,8) generators, and an exact permutation-group
order routine (orbit-stabiliser with Schreier generators).

Standard library only.

Conventions used (all verified against the board in verify_core.py):
  * GF(8) = GF(2)[x]/(x^3+x+1); element a0 + a1*x + a2*x^2 is the int
    a0 | a1<<1 | a2<<2.  So 2 == x is a primitive element.
  * A point of PG(2,8) is a nonzero vector (x,y,z) over GF(8) in canonical
    form: the FIRST nonzero coordinate equals 1.  The board index ("rank")
    is the position of the canonical vector in lexicographically sorted order.
      rank 0      -> (0,0,1)
      ranks 1..8  -> (0,1,c), c = rank-1
      ranks 9..72 -> (1,a,c), a = (rank-9)//8, c = (rank-9)%8
  * A line is {p : a*p0 + b*p1 + c*p2 = 0} for a canonical nonzero dual
    vector (a,b,c) (same canonical rule, same lex order, 73 lines).
  * Frobenius phi: (x,y,z) -> (x^2,y^2,z^2) (entrywise squaring in GF(8)).
  * A matrix M acts on row vectors: p -> p*M, then canonicalise.
  * Permutations are tuples p[0..72] with the image convention
    x -> p[x]; composition (a then b) is tuple(b[x] for x in a).
"""

from itertools import combinations

N = 73
Q = 8

# ---------------------------------------------------------------- GF(8)

def gf_mul(a, b):
    r = 0
    for i in range(3):
        if (b >> i) & 1:
            r ^= a << i
    for i in (5, 4, 3):
        if (r >> i) & 1:
            r ^= 0b1011 << (i - 3)      # x^3 = x + 1
    return r & 7

MUL = [[gf_mul(a, b) for b in range(Q)] for a in range(Q)]

def gf_pow(a, k):
    r = 1
    for _ in range(k):
        r = MUL[r][a]
    return r

INV = [0] * Q
for _a in range(1, Q):
    INV[_a] = gf_pow(_a, 6)            # a^7 = 1, so a^-1 = a^6

ADD = [[a ^ b for b in range(Q)] for a in range(Q)]

def gf_det(M):
    a, b, c = M[0]
    d, e, f = M[1]
    g, h, i = M[2]
    return (MUL[a][MUL[e][i] ^ MUL[f][h]]
            ^ MUL[b][MUL[d][i] ^ MUL[f][g]]
            ^ MUL[c][MUL[d][h] ^ MUL[e][g]])

def gf_square(a):
    return MUL[a][a]

# ------------------------------------------------------- point ranking

def canonical_vectors():
    out = []
    for x in range(Q):
        for y in range(Q):
            for z in range(Q):
                v = (x, y, z)
                if v == (0, 0, 0):
                    continue
                first = x if x else (y if y else z)
                if first != 1:
                    continue
                out.append(v)
    out.sort()
    return out

POINTS = canonical_vectors()
assert len(POINTS) == N
VEC = {p: i for i, p in enumerate(POINTS)}
assert all(VEC[POINTS[i]] == i for i in range(N))

def rank_of(x, y, z):
    if x:
        assert x == 1
        return VEC[(x, y, z)]
    if y:
        assert y == 1
        return VEC[(x, y, z)]
    assert z == 1
    return VEC[(0, 0, 1)]

def canon(x, y, z):
    """Canonicalise a nonzero vector and return its rank."""
    if x:
        inv = INV[x]
        return rank_of(MUL[x][inv], MUL[y][inv], MUL[z][inv])
    if y:
        inv = INV[y]
        return rank_of(0, MUL[y][inv], MUL[z][inv])
    assert z
    return rank_of(0, 0, 1)

# ---------------------------------------------------------- board file

def read_board(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = [ln.split() for ln in f if ln.strip()]
    header = lines[0]
    assert header == ["73", "73"], header
    board = []
    for row in lines[1:]:
        assert int(row[0]) == 9, row
        entries = [int(t) for t in row[1:]]
        assert len(entries) == 9, row
        board.append(tuple(entries))
    assert len(board) == N
    return board

# ------------------------------------------------------------ lines

def generated_lines():
    """All 73 lines from the geometry (dual canonical vectors)."""
    lines = []
    for d in POINTS:
        a, b, c = d
        pts = []
        for p in range(N):
            x, y, z = POINTS[p]
            if MUL[a][x] ^ MUL[b][y] ^ MUL[c][z] == 0:
                pts.append(p)
        assert len(pts) == 9
        lines.append(tuple(pts))
    return lines

# ------------------------------------------------------------- caps

def is_cap(pts, line_of_pair):
    pts = list(pts)
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            for k in range(j + 1, len(pts)):
                if line_of_pair[pts[i]][pts[j]] == line_of_pair[pts[i]][pts[k]] == line_of_pair[pts[j]][pts[k]]:
                    return False
    return True

def addable_points(pts, line_of_pair, lines):
    """Points that can be added to the cap while staying a cap."""
    pts = list(pts)
    forbidden = set(pts)
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            forbidden.update(lines[line_of_pair[pts[i]][pts[j]]])
    return set(range(N)) - forbidden

# ------------------------------------------------------------ matrices

def identity_matrix():
    return [[1 if i == j else 0 for j in range(3)] for i in range(3)]

def elementary(i, j, a):
    M = identity_matrix()
    M[i][j] = a
    return M

def scalar_matrix(a):
    return [[a if i == j else 0 for j in range(3)] for i in range(3)]

def mat_apply(M, p):
    x, y, z = POINTS[p]
    qx = MUL[x][M[0][0]] ^ MUL[y][M[1][0]] ^ MUL[z][M[2][0]]
    qy = MUL[x][M[0][1]] ^ MUL[y][M[1][1]] ^ MUL[z][M[2][1]]
    qz = MUL[x][M[0][2]] ^ MUL[y][M[1][2]] ^ MUL[z][M[2][2]]
    return canon(qx, qy, qz)

def mat_perm(M):
    return tuple(mat_apply(M, p) for p in range(N))

def mat_mul(A, B):
    return [[MUL[A[i][0]][B[0][j]] ^ MUL[A[i][1]][B[1][j]] ^ MUL[A[i][2]][B[2][j]]
             for j in range(3)] for i in range(3)]

def mat_is_scalar(M):
    d = M[0][0]
    return (d != 0 and M[0][1] == 0 and M[0][2] == 0 and M[1][0] == 0
            and M[1][1] == d and M[1][2] == 0 and M[2][0] == 0 and M[2][1] == 0
            and M[2][2] == d)

# --------------------------------------------------------- Frobenius

SQ = [MUL[a][a] for a in range(Q)]
assert [SQ[a] for a in range(8)] == [0, 1, 4, 5, 6, 7, 2, 3]

def phi_perm():
    out = []
    for p in range(N):
        x, y, z = POINTS[p]
        out.append(rank_of(SQ[x], SQ[y], SQ[z]))
    return tuple(out)

# -------------------------------------------------- permutation groups

IDENT = tuple(range(N))

def perm_mul(a, b):
    """a then b."""
    return tuple(b[x] for x in a)

def perm_inv(a):
    inv = [0] * len(a)
    for i, x in enumerate(a):
        inv[x] = i
    return tuple(inv)

def orbit_transversal(gens, b):
    """Return dict point -> permutation t with b -> point, under <gens>."""
    ident = tuple(range(len(gens[0])))
    trans = {b: ident}
    queue = [b]
    for p in queue:                     # list grows while iterating
        t = trans[p]
        for g in gens:
            q = g[p]
            if q not in trans:
                trans[q] = perm_mul(t, g)
                queue.append(q)
    return trans

def group_order(gens, verbose=False):
    """Exact order of <gens> by orbit-stabiliser + Schreier generators."""
    n = len(gens[0]) if gens else 1
    ident = tuple(range(n))
    gs = [g for g in gens if g != ident]
    # dedupe
    seen = set()
    ug = []
    for g in gs:
        if g not in seen:
            seen.add(g)
            ug.append(g)
    gs = ug
    if not gs:
        return 1
    b = None
    for x in range(n):
        if any(g[x] != x for g in gs):
            b = x
            break
    assert b is not None
    trans = orbit_transversal(gs, b)
    inv_trans = {t: perm_inv(t) for t in trans.values()}
    H = set()
    for g in gs:
        for p, t in trans.items():
            q = g[p]
            h = perm_mul(perm_mul(t, g), inv_trans[trans[q]])
            if h != ident:
                H.add(h)
    if verbose:
        print(f"    orbit {len(trans)}, Schreier generators {len(H)}")
    return len(trans) * group_order(list(H), verbose=verbose)

# --------------------------------------------------------------- PGL

def pgl_generators():
    """Generators of GL(3,8); their images generate PGL(3,8).
    Elementary transvections E_ij(1) (i != j) and diag(2,1,1), diag(1,2,1).
    (Conjugating E_ij(1) by the diagonals gives E_ij(alpha^k) for every
    nonzero field element alpha^k, so SL(3,8) is generated; diag(2,1,1) has
    determinant 2, so GL(3,8) is generated.)"""
    mats = []
    for i in range(3):
        for j in range(3):
            if i != j:
                mats.append(elementary(i, j, 1))
    mats.append([[2, 0, 0], [0, 1, 0], [0, 0, 1]])   # diag(alpha,1,1)
    mats.append([[1, 0, 0], [0, 2, 0], [0, 0, 1]])   # diag(1,alpha,1)
    return mats

def gl_order_formula():
    return (Q**3 - 1) * (Q**3 - Q) * (Q**3 - Q**2)

if __name__ == "__main__":
    print("points:", len(POINTS))
    print("GF(8) mul table:")
    for a in range(8):
        print(" ", a, MUL[a])
    ph = phi_perm()
    print("phi permutation:", ph)
    print("phi^3 == id:", perm_mul(perm_mul(ph, ph), ph) == IDENT)
    print("|GL(3,8)| formula:", gl_order_formula(), " /7 =", gl_order_formula() // 7)
