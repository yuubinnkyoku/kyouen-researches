"""Conics of PG(2,9): the conic C of the claim, all 58,968 conics, and the
stabiliser of a conic in PGL(3,9).  Results are cached in plain text."""
import os

import gf9 as F
import pg9 as P

C = [0, 1, 10, 20, 31, 45, 51, 62, 75, 88]
C_MASK = P.mask_of(C)
FIVE = [0, 1, 10, 20, 31]

CONIC_CACHE = "cache_conics.txt"
STAB_CACHE = "cache_stab_C.txt"


# ------------------------------------------------------------------ linear alg
def nullspace(rows, n):
    """Basis of the nullspace of the homogeneous system `rows` over GF(9)."""
    M = [list(row) for row in rows]
    piv = []
    r = 0
    for c in range(n):
        pr = None
        for i in range(r, len(M)):
            if M[i][c]:
                pr = i
                break
        if pr is None:
            continue
        M[r], M[pr] = M[pr], M[r]
        inv = F.INV[M[r][c]]
        if inv != 1:
            M[r] = [F.MUL[inv][x] for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [F.sub(M[i][k], F.MUL[f][M[r][k]]) for k in range(n)]
        piv.append(c)
        r += 1
        if r == len(M):
            break
    free = [c for c in range(n) if c not in piv]
    basis = []
    for fc in free:
        v = [0] * n
        v[fc] = 1
        for i, pc in enumerate(piv):
            v[pc] = F.NEG[M[i][fc]]
        basis.append(v)
    return basis, piv


def forms_through(pts):
    rows = [P.form_row(i) for i in pts]
    return nullspace(rows, 6)


def conic_through(pts):
    """Return (canonical form, nullspace dim) for the quadratic forms through
    the given points."""
    basis, _ = forms_through(pts)
    if len(basis) != 1:
        return None, len(basis)
    return P.canonical_form(tuple(basis[0])), 1


# ---------------------------------------------------------------- all conics
def all_conics():
    """All non-degenerate conics of PG(2,9) as point-set bit masks (cached)."""
    if os.path.exists(CONIC_CACHE):
        with open(CONIC_CACHE, "r", encoding="utf-8") as fh:
            return [int(x, 16) for x in fh.read().split()]
    forms = P.all_canonical_forms()
    dets = {}
    conics = []
    degenerate = 0
    ten_point_degenerate = 0
    for c in forms:
        if P.form_det(c) == 0:
            degenerate += 1
            m = P.form_zero_mask(c)
            if bin(m).count("1") == 10:
                ten_point_degenerate += 1
            continue
        m = P.form_zero_mask(c)
        if bin(m).count("1") != 10:
            raise AssertionError("nondegenerate conic with %d points"
                                 % bin(m).count("1"))
        conics.append(m)
    conics = sorted(set(conics))
    with open(CONIC_CACHE, "w", encoding="utf-8") as fh:
        fh.write("\n".join(format(m, "x") for m in conics))
        fh.write("\n")
    return conics


# ------------------------------------------------------------------ stabiliser
def frame_of(mask):
    """Any 4 points of the point set `mask` in general position (no 3 collinear)."""
    pts = P.bits(mask)
    for a in range(len(pts)):
        for b in range(a + 1, len(pts)):
            for c in range(b + 1, len(pts)):
                lab = P.PAIR_LINE[pts[a]][pts[b]]
                if (lab >> pts[c]) & 1:
                    continue
                for d in range(c + 1, len(pts)):
                    if ((lab >> pts[d]) & 1) or ((P.PAIR_LINE[pts[a]][pts[c]] >> pts[d]) & 1) \
                            or ((P.PAIR_LINE[pts[b]][pts[c]] >> pts[d]) & 1):
                        continue
                    return [pts[a], pts[b], pts[c], pts[d]]
    raise AssertionError("no frame found")


def stabiliser(mask, cache=None):
    """All projectivities (normalised matrices) mapping the point set `mask`
    onto itself, by enumerating all images of a fixed frame."""
    if cache and os.path.exists(cache):
        with open(cache, "r", encoding="utf-8") as fh:
            data = fh.read().split()
        mats = []
        i = 0
        while i < len(data) and data[i] != "#":
            vals = [int(x, 16) for x in data[i:i + 9]]
            mats.append(tuple(tuple(vals[3 * r:3 * r + 3]) for r in range(3)))
            i += 9
        return mats
    fr = frame_of(mask)
    src = [P.POINTS[i] for i in fr]
    dst_pts = P.bits(mask)
    mats = []
    seen = set()
    for a in dst_pts:
        for b in dst_pts:
            if b == a:
                continue
            for c in dst_pts:
                if c == a or c == b:
                    continue
                for d in dst_pts:
                    if d == a or d == b or d == c:
                        continue
                    M = P.projectivity_from_frame(
                        src, [P.POINTS[a], P.POINTS[b], P.POINTS[c], P.POINTS[d]])
                    if M is None:
                        continue
                    images = 0
                    good = True
                    for i in P.bits(mask):
                        j = P.LABEL[F.normalise(P.mat_vec(M, P.POINTS[i]))]
                        if not ((mask >> j) & 1):
                            good = False
                            break
                        images |= 1 << j
                    if good and images == mask and M not in seen:
                        seen.add(M)
                        mats.append(M)
    if cache:
        with open(cache, "w", encoding="utf-8") as fh:
            fh.write("\n".join(" ".join(format(x, "x") for row in M for x in row)
                               for M in mats))
            fh.write("\n#\n")
    return mats


def permutations_on(mask, mats):
    """The permutations of the point set `mask` induced by the matrices."""
    pts = P.bits(mask)
    pos = {p: i for i, p in enumerate(pts)}
    out = []
    for M in mats:
        perm = tuple(pos[P.LABEL[F.normalise(P.mat_vec(M, P.POINTS[p]))]] for p in pts)
        out.append(perm)
    return out


# --------------------------------------------------- explicit PGL(2,9) action
def standard_conic_mask():
    """Point mask of the standard conic {(t^2:t:1)} U {(1:0:0)}."""
    m = 0
    for t in range(9):
        p = F.normalise((F.MUL[t][t], t, 1))
        m |= 1 << P.LABEL[p]
    m |= 1 << P.LABEL[(1, 0, 0)]
    return m


def mobius_matrices():
    """The 720 projectivities of the standard conic induced by Moebius maps."""
    out = []
    for a in range(9):
        for b in range(9):
            for c in range(9):
                for d in range(9):
                    if F.sub(F.MUL[a][d], F.MUL[b][c]) == 0:
                        continue
                    M = ((F.MUL[a][a], F.MUL[2][F.MUL[a][b]], F.MUL[b][b]),
                         (F.MUL[a][c], F.ADD[F.MUL[a][d]][F.MUL[b][c]], F.MUL[b][d]),
                         (F.MUL[c][c], F.MUL[2][F.MUL[c][d]], F.MUL[d][d]))
                    out.append(P.mat_normalize(M))
    return sorted(set(out))


def parameterisation():
    """Projectivity T with T(standard conic) = C, plus the inverse."""
    S = standard_conic_mask()
    src = [P.POINTS[i] for i in frame_of(S)]
    dst_pts = P.bits(C_MASK)
    for a in dst_pts:
        for b in dst_pts:
            if b == a:
                continue
            for c in dst_pts:
                if c in (a, b):
                    continue
                for d in dst_pts:
                    if d in (a, b, c):
                        continue
                    T = P.projectivity_from_frame(
                        src, [P.POINTS[a], P.POINTS[b], P.POINTS[c], P.POINTS[d]])
                    if T is None:
                        continue
                    Timg = 0
                    for i in P.bits(S):
                        Timg |= 1 << P.LABEL[F.normalise(P.mat_vec(T, P.POINTS[i]))]
                    if Timg == C_MASK:
                        return T, P.mat_inv(T)
    raise AssertionError("no projectivity standard conic -> C")
