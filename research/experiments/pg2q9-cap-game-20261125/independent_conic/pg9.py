"""PG(2,9) core: points with the claim's coordinate labels, lines, caps, conics,
and projectivity helpers.  Python standard library only.

Field labelling (determined in task1 from the board itself, see REPORT):
the point index k in 0..8 codes the field element a + b*i with
    a = k // 3,  b = k % 3      (i.e. the integer label 3*a + b)
and the points are
    index 0        -> (0:0:1)
    index 1+j      -> (0:1:phi(j))
    index 10+9p+j  -> (1:phi(p):phi(j))
with phi(k) = (k//3) + 3*(k%3) the canonical (a + 3b) label used by gf9.py.
The constant 1 of GF(9), i.e. (1,0), is therefore index 3 in that convention.
"""
import gf9 as F

FULL = (1 << 91) - 1


def phi(k):
    """Board index 0..8 -> canonical field label a+3b with (a,b)=(k//3,k%3)."""
    return (k // 3) + 3 * (k % 3)


def vec(idx):
    if idx == 0:
        return (0, 0, 1)
    if idx <= 9:
        return (0, 1, phi(idx - 1))
    p, j = divmod(idx - 10, 9)
    return (1, phi(p), phi(j))


POINTS = [vec(i) for i in range(91)]
LABEL = {p: i for i, p in enumerate(POINTS)}

LINES = [frozenset(ln) for ln in F.all_lines(POINTS)]
LINE_MASKS = [sum(1 << i for i in ln) for ln in LINES]

# PAIR_LINE[i][j] = bit mask of the (unique) line through points i and j
PAIR_LINE = [[0] * 91 for _ in range(91)]
for _ln, _m in zip(LINES, LINE_MASKS):
    for _i in _ln:
        for _j in _ln:
            PAIR_LINE[_i][_j] = _m

POINT_LINES = [[m for m in LINE_MASKS if (m >> i) & 1] for i in range(91)]


# ------------------------------------------------------------------- bit sets
def bits(mask):
    out = []
    while mask:
        b = mask & -mask
        out.append(b.bit_length() - 1)
        mask ^= b
    return out


def mask_of(seq):
    m = 0
    for i in seq:
        m |= 1 << i
    return m


def forbidden(mask):
    """All points lying on a line through two points of `mask` (includes mask)."""
    pts = bits(mask)
    f = 0
    for a in range(len(pts)):
        pa = PAIR_LINE[pts[a]]
        for b in range(a + 1, len(pts)):
            f |= pa[pts[b]]
    return f


def allowed(mask):
    return FULL & ~forbidden(mask)


def is_cap(mask):
    pts = bits(mask)
    for a in range(len(pts)):
        for b in range(a + 1, len(pts)):
            if bin(PAIR_LINE[pts[a]][pts[b]] & mask).count("1") != 2:
                return False
    return True


# ------------------------------------------------------------ quadratic forms
SQR = [F.MUL[x][x] for x in range(9)]
# monomial basis (x^2, y^2, z^2, xy, xz, yz) evaluated at every point
MONO = [[SQR[p[0]], SQR[p[1]], SQR[p[2]],
         F.MUL[p[0]][p[1]], F.MUL[p[0]][p[2]], F.MUL[p[1]][p[2]]]
        for p in POINTS]


def form_value(c, i):
    row = MONO[i]
    v = 0
    for t in range(6):
        if c[t]:
            v = F.ADD[v][F.MUL[c[t]][row[t]]]
    return v


def form_row(i):
    return list(MONO[i])


def form_zero_mask(c):
    m = 0
    for i in range(91):
        if form_value(c, i) == 0:
            m |= 1 << i
    return m


def form_matrix(c):
    """Symmetric matrix M with Q(x) = (1/2) x^T M x:  [[2a,d,e],[d,2b,f],[e,f,2c]]."""
    a, b, cc, d, e, f = c
    return ((F.ADD[a][a], d, e),
            (d, F.ADD[b][b], f),
            (e, f, F.ADD[cc][cc]))


def form_det(c):
    return mat_det(form_matrix(c))


def form_is_nondegenerate(c):
    return form_det(c) != 0


def all_canonical_forms():
    """All nonzero quadratic forms up to scalar: first nonzero coefficient = 1."""
    out = []
    for code in range(9 ** 6):
        c = []
        t = code
        for _ in range(6):
            c.append(t % 9)
            t //= 9
        for x in c:
            if x == 0:
                continue
            if x != 1:
                break
            out.append(tuple(c))
            break
    return out


def canonical_form(c):
    """Scale a form so its first nonzero coefficient is 1 (None for zero form)."""
    for x in c:
        if x:
            iv = F.INV[x]
            return tuple(F.MUL[iv][y] for y in c)
    return None


# ------------------------------------------------------------------- matrices
def mat_det(M):
    (a, b, c), (d, e, f), (g, h, i) = M
    t1 = F.MUL[a][F.sub(F.MUL[e][i], F.MUL[f][h])]
    t2 = F.MUL[b][F.sub(F.MUL[d][i], F.MUL[f][g])]
    t3 = F.MUL[c][F.sub(F.MUL[d][h], F.MUL[e][g])]
    return F.ADD[F.sub(t1, t2)][t3]


def mat_vec(M, v):
    out = []
    for r in range(3):
        s = 0
        for k in range(3):
            if M[r][k] and v[k]:
                s = F.ADD[s][F.MUL[M[r][k]][v[k]]]
        out.append(s)
    return tuple(out)


def mat_mul(A, B):
    return tuple(tuple(
        _sum3(F.MUL[A[i][0]][B[0][j]], F.MUL[A[i][1]][B[1][j]],
              F.MUL[A[i][2]][B[2][j]]) for j in range(3)) for i in range(3))


def _sum3(x, y, z):
    return F.ADD[F.ADD[x][y]][z]


def mat_scale(M, s):
    return tuple(tuple(F.MUL[s][x] for x in row) for row in M)


def mat_normalize(M):
    for row in M:
        for x in row:
            if x:
                iv = F.INV[x]
                return mat_scale(M, iv)
    return None


def mat_from_columns(c1, c2, c3):
    return ((c1[0], c2[0], c3[0]),
            (c1[1], c2[1], c3[1]),
            (c1[2], c2[2], c3[2]))


def mat_inv(M):
    det = mat_det(M)
    if det == 0:
        return None
    idet = F.INV[det]
    (a, b, c), (d, e, f), (g, h, i) = M
    cof = ((F.sub(F.MUL[e][i], F.MUL[f][h]), F.sub(F.MUL[c][h], F.MUL[b][i]), F.sub(F.MUL[b][f], F.MUL[c][e])),
           (F.sub(F.MUL[f][g], F.MUL[d][i]), F.sub(F.MUL[a][i], F.MUL[c][g]), F.sub(F.MUL[c][d], F.MUL[a][f])),
           (F.sub(F.MUL[d][h], F.MUL[e][g]), F.sub(F.MUL[b][g], F.MUL[a][h]), F.sub(F.MUL[a][e], F.MUL[b][d])))
    return tuple(tuple(F.MUL[idet][x] for x in row) for row in cof)


def projectivity_from_frame(src, dst):
    """Return the (normalised) matrix mapping src[i] -> dst[i] for i=0..3, or
    None if no such projectivity exists.  src[:3] and dst[:3] must be
    linearly independent, and src[3] / dst[3] must not lie on a side line of
    the respective triangle (for a frame this holds automatically).

    A projectivity is fixed by four points: writing p4 = sum alpha_i p_i and
    q4 = sum delta_i q_i, the map M = Q D P^-1 with D = diag(delta_i/alpha_i)
    satisfies M p_i = delta_i q_i ~ q_i and M p4 ~ q4.
    """
    p1, p2, p3, p4 = src
    q1, q2, q3, q4 = dst
    P = mat_from_columns(p1, p2, p3)
    Pinv = mat_inv(P)
    if Pinv is None:
        return None
    Q = mat_from_columns(q1, q2, q3)
    Qinv = mat_inv(Q)
    if Qinv is None:
        return None
    alpha = mat_vec(Pinv, p4)
    delta = mat_vec(Qinv, q4)
    if 0 in alpha or 0 in delta:
        return None
    mu = [F.MUL[delta[i]][F.INV[alpha[i]]] for i in range(3)]
    D = ((mu[0], 0, 0), (0, mu[1], 0), (0, 0, mu[2]))
    M = mat_mul(mat_mul(Q, D), Pinv)
    M = mat_normalize(M)
    if M is None:
        return None
    for u, v in zip(src, dst):
        if not _same_point(mat_vec(M, u), v):
            return None
    return M


def _same_point(u, v):
    return F.det3(u, v, (1, 0, 0)) == 0 and F.det3(u, v, (0, 1, 0)) == 0 \
        and F.det3(u, v, (0, 0, 1)) == 0


def act(M, idx):
    """Image point index of point `idx` under the projectivity M."""
    return LABEL[F.normalise(mat_vec(M, POINTS[idx]))]


# --------------------------------------------------------------- cap counting
def cap_extension_counts(mask, child_size=None):
    """Number of points p such that mask | {p} is again a cap."""
    return bin(allowed(mask)).count("1")
