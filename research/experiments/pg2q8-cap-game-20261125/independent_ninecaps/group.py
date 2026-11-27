"""PGL(3,8) generators and permutation-orbit helpers (shared by task scripts)."""
from pg8 import MUL, INV, PTS, PTIDX, canon

N = 73

# Row-vector action v -> v M.
#   P   : (a,b,c) -> (b,c,a)          coordinate 3-cycle
#   S12 : (a,b,c) -> (a+b,b,c)        transvection
#   S23 : (a,b,c) -> (a,b+c,c)        transvection
#   S13 : (a,b,c) -> (a+c,b,c)        transvection
#   D   : (a,b,c) -> (a,2b,c)         diagonal scaling (order 7)
P = ((0, 0, 1), (1, 0, 0), (0, 1, 0))
S12 = ((1, 0, 0), (1, 1, 0), (0, 0, 1))
S23 = ((1, 0, 0), (0, 1, 0), (0, 1, 1))
S13 = ((1, 0, 0), (0, 1, 0), (1, 0, 1))
D = ((1, 0, 0), (0, 2, 0), (0, 0, 1))
MATS = {"P": P, "S12": S12, "S23": S23, "S13": S13, "D": D}


def mat_apply(M, v):
    return tuple(
        MUL[v[0]][M[0][j]] ^ MUL[v[1]][M[1][j]] ^ MUL[v[2]][M[2][j]]
        for j in range(3))


def mat_mul(A, B):
    return tuple(tuple(
        MUL[A[i][0]][B[0][j]] ^ MUL[A[i][1]][B[1][j]] ^ MUL[A[i][2]][B[2][j]]
        for j in range(3)) for i in range(3))


def mat_perm(M):
    perm = []
    for p in range(N):
        w = mat_apply(M, PTS[p])
        perm.append(PTIDX[canon(w)])
    return tuple(perm)


def mat_det(M):
    (a, b, c), (d, e, f), (g, h, i) = M
    return (MUL[a][MUL[e][i] ^ MUL[f][h]]
            ^ MUL[b][MUL[f][g] ^ MUL[d][i]]
            ^ MUL[c][MUL[d][h] ^ MUL[e][g]])


def compose(f, g):
    """(f o g)(i) = f[g[i]]."""
    return tuple(f[g[i]] for i in range(N))


def inverse(p):
    q = [0] * N
    for i, v in enumerate(p):
        q[v] = i
    return tuple(q)


IDENT = tuple(range(N))
GENS = [mat_perm(M) for M in MATS.values()]


def image_mask(perm, mask):
    out = 0
    m = mask
    while m:
        b = m & -m
        p = b.bit_length() - 1
        out |= 1 << perm[p]
        m ^= b
    return out


def orbit_of_mask(mask, gens=None):
    if gens is None:
        gens = GENS
    seen = {mask}
    queue = [mask]
    qi = 0
    while qi < len(queue):
        x = queue[qi]
        qi += 1
        for g in gens:
            y = image_mask(g, x)
            if y not in seen:
                seen.add(y)
                queue.append(y)
    return seen
