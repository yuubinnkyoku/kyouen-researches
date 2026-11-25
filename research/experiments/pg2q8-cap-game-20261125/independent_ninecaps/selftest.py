"""Self-tests for the field arithmetic and the Schreier-chain order code.

These validate the verifier itself on groups of known order before its results
are used for PGL(3,8).
"""
import random

from pg8 import MUL, INV, gf_mul, PTS, PTIDX, cross, dot
from group import compose, inverse, IDENT, N


def schreier_chain_order_n(gens, base, n):
    """Same algorithm as check_group.schreier_chain_order, on n points."""
    def comp(f, g):
        return tuple(f[g[i]] for i in range(n))

    def inv(p):
        q = [0] * n
        for i, v in enumerate(p):
            q[v] = i
        return tuple(q)

    ident = tuple(range(n))
    cur = list(dict.fromkeys(gens))
    order = 1
    b_idx = 0
    while True:
        if b_idx < len(base):
            b = base[b_idx]
        else:
            b = None
            for g in cur:
                if g != ident:
                    b = next(i for i in range(n) if g[i] != i)
                    break
            if b is None:
                break
        orb = {b: ident}
        queue = [b]
        while queue:
            x = queue.pop()
            ux = orb[x]
            for g in cur:
                y = g[x]
                if y not in orb:
                    orb[y] = comp(g, ux)
                    queue.append(y)
        order *= len(orb)
        new = []
        seen = set()
        for x, ux in orb.items():
            for g in cur:
                y = g[x]
                s = comp(inv(orb[y]), comp(g, ux))
                if s != ident and s not in seen:
                    seen.add(s)
                    new.append(s)
        cur = new
        b_idx += 1
        assert b_idx < 100
    return order


def main():
    # ---- field ----
    assert gf_mul(2, 2) == 4 and gf_mul(4, 2) == 3  # x^3 = x+1
    for a in range(8):
        for b in range(8):
            assert MUL[a][b] == MUL[b][a]
            if a and b:
                assert MUL[a][INV[a]] == 1
    for a in range(8):
        for b in range(8):
            for c in range(8):
                assert MUL[a][b ^ c] == MUL[a][b] ^ MUL[a][c]
                assert MUL[MUL[a][b]][c] == MUL[a][MUL[b][c]]
    print("field: OK (x^3 = x+1, commutativity, inverses, associativity,"
          " distributivity)")

    # ---- geometry: 73 points, each line 9 points, unique line per pair ----
    lof = {}
    for i in range(73):
        for j in range(i + 1, 73):
            n = cross(PTS[i], PTS[j])
            L = frozenset(k for k in range(73) if dot(n, PTS[k]) == 0)
            lof[(i, j)] = L
    assert len({v for v in lof.values()}) == 73
    assert all(len(v) == 9 for v in lof.values())
    print("geometry from field: 73 distinct lines of 9 points: OK")

    # ---- Schreier order on known groups ----
    # S3 on 3 points
    a = (1, 0, 2)          # transposition (0 1)
    b = (1, 2, 0)          # 3-cycle (0 1 2)
    assert schreier_chain_order_n([a, b], [0, 1], 3) == 6
    # C7
    c7 = tuple((i + 1) % 7 for i in range(7))
    assert schreier_chain_order_n([c7], [0], 7) == 7
    # S4 on 4 points
    t = (1, 0, 2, 3)
    q = (1, 2, 3, 0)
    assert schreier_chain_order_n([t, q], [0, 1, 2], 4) == 24
    # D8 (symmetries of a square) on 4 points, order 8
    r = (1, 2, 3, 0)       # rotation
    s = (1, 0, 3, 2)       # reflection
    assert schreier_chain_order_n([r, s], [0, 1], 4) == 8
    # A5 on 5 points, order 60: (0 1)(2 3) and (0 1 2 3 4) are both even
    g1 = (1, 0, 3, 2, 4)
    g2 = (1, 2, 3, 4, 0)
    val = schreier_chain_order_n([g1, g2], [0, 1], 5)
    assert val == 60, val  # <(0 1)(2 3), (0 1 2 3 4)> = A5
    print("Schreier chain: S3=6, C7=7, S4=24, D8=8, A5=60: OK")

    # ---- random permutation group vs brute force ----
    rng = random.Random(7)
    for trial in range(5):
        n = 7
        gens = []
        for _ in range(2):
            p = list(range(n))
            rng.shuffle(p)
            gens.append(tuple(p))
        # brute force closure
        G = {tuple(range(n))}
        frontier = [tuple(range(n))]
        while frontier:
            nf = []
            for x in frontier:
                for g in gens:
                    y = tuple(g[x[i]] for i in range(n))
                    if y not in G:
                        G.add(y)
                        nf.append(y)
            frontier = nf
        got = schreier_chain_order_n(gens, [0, 1, 2], n)
        assert got == len(G), (got, len(G), gens)
    print("Schreier chain matches brute-force closure on 5 random subgroups"
          " of S7: OK")

    # ---- permutation helpers (full 73-point permutations) ----
    pl = list(range(N))
    pl[0], pl[1], pl[2] = 1, 2, 0
    p = tuple(pl)
    assert compose(p, inverse(p)) == IDENT
    print("compose/inverse: OK")


if __name__ == "__main__":
    main()
    print("\nALL SELF-TESTS PASS")
