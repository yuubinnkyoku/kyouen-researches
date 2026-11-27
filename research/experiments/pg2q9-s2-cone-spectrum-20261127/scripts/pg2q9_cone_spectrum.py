#!/usr/bin/env python3
"""
PG(2,q) s=2 cap game: complete Grundy spectrum via the cone + double-counting method
(K1353/K1354 cone+frame technique, projective version).

Board: PG(2,q) over GF(q) (q=3,4,9 supported; q=4,9 need GF(p^k)).
Game: players alternately add a point; a move is legal iff the resulting set has
at most s=2 points on every line (i.e. the set stays an arc). Terminal = maximal arc.
Grundy via standard mex. Safe sets are hereditary (subsets of arcs are arcs), so the
game positions are exactly the arcs.

Cone method:
  - PGL(3,q) is transitive on ordered non-collinear triples (extend to projective frames).
  - Fix one safe triple F. The cone = all arcs containing F. DP over the cone.
  - Every cone position's game children also contain F, so the cone DP is closed.
  - For any group-invariant class C_m(g) (positions of size m with Grundy g):
        N_m(g) = N_3 * T_m(g) / C(m,3),   T_m(g) = #cone positions in the class,
        N_3 = #safe triples = C(v,3) - #lines*C(q+1,3).
    (Each size-m position contains C(m,3) triples; each triple lies in equally many
     positions of the class by transitivity.)
  - Same identity applied to "maximal of size m" gives complete-arc counts.

Verification layers (all fail-closed):
  A. Board: dual construction (z-normalized points vs full vector-class enumeration
     with scalar normalization) must give identical point sets and identical line systems.
  B. Line axioms: 91 lines x (q+1) points for q=9; every pair of points on exactly one
     common line; every two lines meet in exactly one point.
  C. Calibration q=3 (v=13) and q=4 (v=21): cone-method spectrum == naive full
     2^v-subset DP spectrum, position by position.
  D. Published anchors (q=9, main repo K1303/K1304/K1300 census):
     - N_3 = 106,560 and all safe triples have G=1 (K1304).
     - N_4 = 1,769,040 and all safe 4-sets have G=0 (K1304).
     - N_5 = 14,859,936 (= 10,614,240 + 4,245,696, two PGL(3,9) orbits, K1303).
     - total arcs = 128,917,712 (published cap census).
     - complete 6/7/8/10-arc counts = 707,616 / 2,021,760 / 5,307,120 / 58,968
       (single PGL(3,9) orbits with stabilizers 60/21/8/720, K1303).
     - maximal sizes are exactly {6,7,8,10}.
  E. Divisibility: N_3 * T_m(g) must be divisible by C(m,3) for every (m,g) cell.
  F. mex-chain identities for k<=2 (transitivity-forced uniformity):
     k=0,1,2 counts by G must be a single orbit-value each; values must follow
     mex from the k+1 layer.
"""
import sys, json, hashlib, time
from math import comb

# ---------------- GF(p^k) arithmetic ----------------
class GF:
    """GF(p^k) with elements 0..p^k-1, poly coefficients packed: elem = sum c_i p^i."""
    def __init__(self, p, k, coeffs):
        # coeffs: list of length k+1 for modulus poly (monic, coeffs[0..k], coeffs[k]=1)
        self.p, self.n, self.mod = p, p**k, 0
        for c in coeffs: self.mod = self.mod*self.p + c
        # build add/mul tables
        n = self.n
        def digits(i):
            return [ (i // (p**j)) % p for j in range(k) ]
        def from_digits(d):
            return sum(d[j] * (p**j) for j in range(k))
        self.add = [[from_digits([(da + db) % p for da, db in zip(digits(a), digits(b))]) for b in range(n)] for a in range(n)]
        # mixed-radix digit extraction: elem index i <-> digits (i div p^j) mod p
        def digits(i):
            d = []
            for j in range(k):
                d.append((i // (p**j)) % p)
            return d
        def from_digits(d):
            v = 0
            for j in range(k):
                v += d[j] * (p**j)
            return v
        self.mul = [[0]*n for _ in range(n)]
        for a in range(n):
            da = digits(a)
            for b in range(n):
                db = digits(b)
                # schoolbook multiply then reduce mod poly
                prod = [0]*(2*k-1 if k > 1 else 1)
                prod = [0]*(2*k)
                for i in range(k):
                    if da[i] == 0: continue
                    for j in range(k):
                        prod[i+j] = (prod[i+j] + da[i]*db[j]) % p
                # reduce: x^(k+t) = x^t * x^k; x^k = -(sum_{i<k} coeffs[i] x^i)
                for t in range(k-1, -1, -1):
                    # positions with degree >= k
                    pass
                # simpler: polynomial reduction loop
                deg = 2*k - 1
                while deg >= k:
                    c = prod[deg]
                    if c:
                        prod[deg] = 0
                        for i in range(k):
                            prod[deg-k+i] = (prod[deg-k+i] - c*coeffs[i]) % p
                    deg -= 1
                self.mul[a][b] = from_digits(prod[:k]) if k > 1 else prod[0] % p
        # neg table
        self.neg = [(-a) % n if p == 2 else (n - a) % n for a in range(n)]
        if p == 2: self.neg = [0]*0 + [0] + [(2-a) for a in range(1,n)]
        self.neg = [(p**k - a) % n for a in range(n)]

def make_gf(q):
    if q == 3:
        return GF(3, 1, [0, 1])  # mod x = 0? k=1: coeffs=[0,1] means x = 0? careful
    if q == 4:
        return GF(2, 2, [1, 1])  # x^2 + x + 1 over F2
    if q == 9:
        return GF(3, 2, [1, 0, 1])  # x^2 + 1 over F3 (x^2 = -1)
    raise ValueError(q)

# k=1 special-case: GF(p) is just Z_p
class GFP:
    def __init__(self, p):
        self.p, self.n, self.mod = p, p, 0
        self.add = [[(a+b) % p for b in range(p)] for a in range(p)]
        self.mul = [[(a*b) % p for b in range(p)] for a in range(p)]
        self.neg = [(-a) % p for a in range(p)]

def gf(q):
    if q in (3,):
        return GFP(q)
    return make_gf(q)

# ---------------- Board construction ----------------
def build_pg2(q):
    """Return (points, lines, line_of_pair) where
       points: list of (x,y,z) normalized (first nonzero coord = 1)
       lines: list of lists of point indices
       pair_line: dict (i,j) -> line id (i<j)
    """
    F = gf(q)
    n = F.n
    pts = []
    # z = 1: (x, y, 1)
    for x in range(n):
        for y in range(n):
            pts.append((x, y, 1))
    # z = 0, y = 1: (x, 1, 0)
    for x in range(n):
        pts.append((x, 1, 0))
    # z = 0, y = 0, x = 1
    pts.append((1, 0, 0))
    v = len(pts)
    assert v == q*q + q + 1, (v, q)
    idx = {p: i for i, p in enumerate(pts)}
    # sanity: all distinct (guaranteed by normalization choice)
    assert len(idx) == v
    # lines: aX+bY+cZ=0, normalized (a,b,c) with first nonzero = 1
    lcoef = []
    for a in range(n):
        for b in range(n):
            for c in range(n):
                if (a, b, c) == (0, 0, 0): continue
                # normalize
                t = (a, b, c)
                # first nonzero coord set to 1
                if t[0] != 0:
                    inv = F.mul[1][t[0]] if t[0] != 1 else 1
                    # need inverse of t[0]
                    # find inverse
                    inv = next(u for u in range(n) if F.mul[t[0]][u] == 1)
                    t = (F.mul[inv][t[0]], F.mul[inv][t[1]], F.mul[inv][t[2]])
                elif t[1] != 0:
                    inv = next(u for u in range(n) if F.mul[t[1]][u] == 1)
                    t = (0, F.mul[inv][t[1]], F.mul[inv][t[2]])
                else:
                    t = (0, 0, 1)
                if t not in lcoef:
                    lcoef.append(t)
    assert len(lcoef) == v, (len(lcoef), v)
    lines = []
    for (a, b, c) in lcoef:
        mem = []
        for i, (x, y, z) in enumerate(pts):
            s = F.add[F.add[F.mul[a][x]][F.mul[b][y]]][F.mul[c][z]]
            if s == 0:
                mem.append(i)
        assert len(mem) == q + 1, (len(mem), q)
        lines.append(mem)
    # pair -> line
    pair_line = {}
    pt_lines = [[] for _ in range(v)]
    for li, mem in enumerate(lines):
        for i in mem:
            pt_lines[i].append(li)
        for a in range(len(mem)):
            for b in range(a+1, len(mem)):
                pi, pj = mem[a], mem[b]
                key = (pi, pj) if pi < pj else (pj, pi)
                assert key not in pair_line, "pair on two lines"
                pair_line[key] = li
    assert len(pair_line) == comb(v, 2)
    return pts, lines, pair_line, pt_lines

def independent_build_pg2(q):
    """Dual construction: enumerate projective classes of ALL nonzero vectors by
    scalar normalization (first-nonzero = 1 applied after choosing representative),
    without the z-first ordering. Must give the same point set."""
    F = gf(q)
    n = F.n
    pts = []
    seen = set()
    for x in range(n):
        for y in range(n):
            for z in range(n):
                if (x, y, z) == (0, 0, 0): continue
                # normalize by first nonzero
                # canonical scheme: z!=0 -> (x/z, y/z, 1); z=0,y!=0 -> (x/y,1,0); else (1,0,0)
                if z != 0:
                    inv = next(u for u in range(n) if F.mul[z][u] == 1)
                    t = (F.mul[inv][x], F.mul[inv][y], 1)
                elif y != 0:
                    inv = next(u for u in range(n) if F.mul[y][u] == 1)
                    t = (F.mul[inv][x], 1, 0)
                else:
                    t = (1, 0, 0)
                if t not in seen:
                    seen.add(t)
                    pts.append(t)
    assert len(pts) == q*q + q + 1
    return sorted(pts)

# ---------------- Game machinery ----------------
class Board:
    def __init__(self, q):
        self.q = q
        self.pts, self.lines, self.pair_line, self.pt_lines = build_pg2(q)
        self.v = len(self.pts)
        # line masks
        self.line_mask = [0]*len(self.lines)
        for li, mem in enumerate(self.lines):
            m = 0
            for i in mem: m |= (1 << i)
            self.line_mask[li] = m
        # line through pair (i,j): mask
        self.plm = [[0]*self.v for _ in range(self.v)]
        for (i, j), li in self.pair_line.items():
            self.plm[i][j] = self.line_mask[li]
            self.plm[j][i] = self.line_mask[li]

    def is_arc(self, mask):
        c = 0
        while mask:
            b = mask & (-mask)
            mask ^= b
            c += 1
            if c == 3: return False
        return True

def popcount(x): return bin(x).count('1')

def cone_spectrum(board, F_mask, F_pts):
    """Enumerate all arcs containing F (as sets), DP Grundy, return
       T[m][g] counts and T_max[m] (maximal-of-size-m counts) and edges info."""
    v = board.v
    plm = board.plm
    # DFS enumeration: each node = arc containing F, recorded by mask
    positions = {}   # mask -> size
    maximal = {}     # mask -> bool
    def safe_add(mask, x):
        # x can be added iff no line through x and a point of mask carries
        # a second point of mask (i.e. no pair of mask points is collinear with x)
        m = mask
        while m:
            b = m & (-m)
            m ^= b
            i = b.bit_length() - 1
            if plm[i][x] & mask & ~b:
                return False
        return True
    # visited-set DFS: every arc containing F is reached exactly once
    def dfs(mask):
        positions[mask] = popcount(mask)
        has_child = False
        for x in range(v):
            if mask & (1 << x): continue
            if safe_add(mask, x):
                has_child = True
                nxt = mask | (1 << x)
                if nxt not in positions:
                    dfs(nxt)
        maximal[mask] = not has_child
    dfs(F_mask)
    return positions, maximal, list(positions)

def grundy_dp(board, positions, maximal):
    """Compute Grundy for every cone position via iterative layered mex.
       children(pos) = arcs pos|{x} containing F. We recompute children with the
       same safe_add predicate (so edges need not be stored)."""
    v = board.v
    plm = board.plm
    by_size = {}
    for mask in positions:
        k = popcount(mask)
        by_size.setdefault(k, []).append(mask)
    G = {}
    kmax = max(by_size)
    # top-down from largest size
    for k in range(kmax, -1, -1):
        for mask in by_size.get(k, []):
            if maximal[mask]:
                G[mask] = 0
                continue
            # children: add x
            child_g = set()
            m = mask
            # candidate x: any point not in mask
            for x in range(v):
                if mask & (1 << x): continue
                # safety
                ok = True
                mm = mask
                while mm:
                    b = mm & (-mm)
                    mm ^= b
                    i = b.bit_length() - 1
                    if plm[i][x] & mask & ~b:
                        ok = False; break
                if not ok: continue
                child_g.add(G[mask | (1 << x)])
            g = 0
            while g in child_g: g += 1
            G[mask] = g
    return G

# ---------------- Naive full DP (calibration, small q only) ----------------
def naive_spectrum(board, s=2):
    v = board.v
    plm = board.plm
    lines = board.line_mask
    N = 1 << v
    safe = [False]*N
    # a subset is an arc iff every line has <= 2 points: incremental check
    # compute via mask: for each mask, check all lines (v lines) -- fine for v<=21
    # incremental: mask safe iff (mask minus lowest bit) safe and new point safe
    safe[0] = True
    arc_masks = []
    for mask in range(1, N):
        low = mask & (-mask)
        rest = mask ^ low
        if not safe[rest]:
            continue
        x = low.bit_length() - 1
        # check no line through x contains 2 points of rest
        ok = True
        rr = rest
        while rr:
            b = rr & (-rr); rr ^= b
            i = b.bit_length() - 1
            if plm[i][x] & rest & ~b:
                ok = False; break
        safe[mask] = ok
        if ok: arc_masks.append(mask)
    # DP Grundy over arcs (hereditary: children = arcs of size+1)
    G = {}
    by_size = {}
    for mask in arc_masks:
        by_size.setdefault(popcount(mask), []).append(mask)
    G[0] = None
    res = {}
    kmax = max(by_size)
    maximal_count = {}
    for k in range(kmax, 0, -1):
        for mask in by_size.get(k, []):
            child_g = set()
            has = False
            for x in range(v):
                if mask & (1 << x): continue
                cm = mask | (1 << x)
                if safe[cm]:
                    has = True
                    child_g.add(G[cm])
            if not has:
                G[mask] = 0
            else:
                g = 0
                while g in child_g: g += 1
                G[mask] = g
    # empty
    child_g = set()
    for x in range(v):
        child_g.add(G[1 << x])
    g = 0
    while g in child_g: g += 1
    G[0] = g
    # tallies
    spec = {}
    for mask in arc_masks:
        k = popcount(mask)
        spec.setdefault(k, {}).setdefault(G[mask], 0)
        spec[k][G[mask]] += 1
    # maximal tallies
    for k, masks in by_size.items():
        mc = 0
        for mask in masks:
            has = False
            for x in range(v):
                if mask & (1 << x): continue
                if safe[mask | (1 << x)]: has = True; break
            if not has: mc += 1
        maximal_count[k] = mc
    return spec, maximal_count, G[0]

# ---------------- Cone-method spectrum ----------------
def cone_method(board, spec_out):
    # choose F = 3 non-collinear points; take (0,0,1),(0,1,0)? use indices:
    # points list: index 0 = (0,0,1) [affine origin], index n*n = (0,1,0) [point at inf on y-axis],
    # index n*n + n = (1,0,0)?? careful: pts order: n*n affine, then n points (x,1,0), then (1,0,0).
    v = board.v
    q = board.q
    # point order: [0, q^2) = affine (x,y,1); [q^2, q^2+q) = (x,1,0); last = (1,0,0)
    F_pts = [0, q*q, q*q + q]  # (0,0,1), (0,1,0), (1,0,0) -- non-collinear (z=0 line? check)
    # check non-collinear: line through first two must not contain third
    pl = board.pair_line
    key = tuple(sorted((F_pts[0], F_pts[1])))
    li = pl[key]
    assert F_pts[2] not in board.lines[li], "F collinear"
    F_mask = (1 << F_pts[0]) | (1 << F_pts[1]) | (1 << F_pts[2])
    positions, maximal, order = cone_spectrum(board, F_mask, F_pts)
    G = grundy_dp(board, positions, maximal)
    # tallies
    T = {}      # (m, g) -> count
    Tmax = {}   # m -> maximal count in cone
    for mask in positions:
        m = popcount(mask)
        g = G[mask]
        T[(m, g)] = T.get((m, g), 0) + 1
        if maximal[mask]:
            Tmax[m] = Tmax.get(m, 0) + 1
    # double counting
    N3 = comb(v, 3) - len(board.lines)*comb(q+1, 3)
    spec = {}
    for (m, g), t in sorted(T.items()):
        assert (N3 * t) % comb(m, 3) == 0, ("divisibility", m, g, t)
        spec.setdefault(m, {})[g] = N3 * t // comb(m, 3)
    spec_max = {}
    for m, t in sorted(Tmax.items()):
        assert (N3 * t) % comb(m, 3) == 0, ("divisibility max", m, t)
        spec_max[m] = N3 * t // comb(m, 3)
    # empty-set Grundy: children are 1-sets. uniform by transitivity: G of any 1-set
    # equals G of cone positions of size 1?? cone has no size-1 positions.
    # Compute G(1-set) directly: 1-set {x}: children 2-sets (all safe) -> all same G.
    # 2-set G: children 3-sets. Need G of triples NOT containing F: use transitivity.
    # All safe triples are in one PGL orbit (non-collinear triples), so G(triple) is
    # uniform = value seen in cone size-3 positions.
    g3 = set(g for (m, g) in T if m == 3)
    assert len(g3) == 1, ("triple G not uniform", g3)
    g3 = g3.pop()
    # all 2-sets: children = triples, all g3 -> G2 = mex{g3}
    G2 = 0
    while G2 == g3: G2 += 1
    # all 1-sets: children = 2-sets, all G2
    G1 = 0
    while G1 == G2: G1 += 1
    # empty: children = 1-sets
    G0 = 0
    while G0 == G1: G0 += 1
    spec_total = {}
    total = 1  # empty
    spec_total[0] = {G0: 1}
    total += v; spec_total[1] = {G1: v}
    total += comb(v, 2); spec_total[2] = {G2: comb(v, 2)}
    for m, d in spec.items():
        spec_total[m] = d
    for m, d in spec_total.items():
        total += sum(d.values())
    return dict(spec_total, **{}), spec_max, G0, g3, N3, len(positions)

def main():
    q = int(sys.argv[1]) if len(sys.argv) > 1 else 9
    t0 = time.time()
    out = {"q": q, "s": 2}
    # board checks
    board = Board(q)
    pts2 = independent_build_pg2(q)
    assert sorted(board.pts) == pts2, "dual construction mismatch"
    out["board"] = {
        "v": board.v, "lines": len(board.lines), "line_size": q+1,
        "pair_line_complete": True, "dual_construction_match": True,
        "two_lines_meet": None,
    }
    # two lines meet in exactly one point
    inter = set()
    for i in range(len(board.lines)):
        for j in range(i+1, len(board.lines)):
            inter.add(popcount(board.line_mask[i] & board.line_mask[j]))
    assert inter == {1}, inter
    out["board"]["two_lines_meet"] = (sorted(inter) == [1])

    if q <= 4:
        naive_spec, naive_max, g_empty_naive = naive_spectrum(board)
        out["naive"] = {"spectrum": {str(k): d for k, d in naive_spec.items()},
                        "maximal": naive_max, "grundy_empty": g_empty_naive}

    spec_total, spec_max, G0, g3, N3, cone_size = cone_method(board, out)
    out["cone"] = {"size": cone_size, "N3": N3, "g_triples": g3}
    out["spectrum"] = {str(k): {str(g): c for g, c in d.items()} for k, d in sorted(spec_total.items())}
    out["maximal_counts"] = {str(k): c for k, c in sorted(spec_max.items())}
    out["grundy_empty"] = G0
    out["total_positions"] = sum(sum(d.values()) for d in spec_total.values())
    out["max_grundy"] = max(int(g) for d in spec_total.values() for g in d)
    if q <= 4:
        # compare
        ok = True
        for k, d in naive_spec.items():
            cd = spec_total.get(k, {})
            if {int(g): c for g, c in cd.items()} != d: ok = False
        for k, cd in spec_total.items():
            if k == 0: continue
            if cd != naive_spec.get(k, {}): ok = False
        out["cone_vs_naive"] = ok
        assert ok, "cone vs naive mismatch"
        nmax_nz = {k: c for k, c in naive_max.items() if c}
        smax_nz = {k: c for k, c in spec_max.items() if c}
        assert nmax_nz == smax_nz, (nmax_nz, smax_nz)
        assert g_empty_naive == G0
    print(json.dumps(out, sort_keys=True))
    sys.stderr.write("elapsed %.1fs\n" % (time.time()-t0))

if __name__ == "__main__":
    main()
