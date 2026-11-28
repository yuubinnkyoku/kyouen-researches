"""PG(2,q^2) boards over GF(q^2) for q^2 in {9, 16} + Baer subplane machinery.

GF(9)  = GF(3)[i], i^2 = 2 (= -1).
GF(16) = GF(2)[a], a^4 = a + 1.

Elements are encoded as ints 0..q^2-1 (polynomial coefficients in base p).
Constructions are design-checked (points/lines/pairs/incidence).
"""
import json

def make_gf(p, e, modpoly):
    q = p ** e
    def to_poly(v):
        cs = []
        for _ in range(e):
            cs.append(v % p)
            v //= p
        return cs
    def to_val(cs):
        v = 0
        for i, c in enumerate(cs):
            v += c * (p ** i)
        return v
    def pmul(a, b):
        r = [0] * (2 * e - 1)
        for i, x in enumerate(a):
            for j, y in enumerate(b):
                r[i + j] = (r[i + j] + x * y) % p
        lead = modpoly[-1]
        for d in range(2 * e - 2, e - 1, -1):
            c = (r[d] * lead) % p
            if c:
                r[d] = 0
                for k in range(e + 1):
                    r[d - e + k] = (r[d - e + k] - c * modpoly[k]) % p
        return r[:e]
    tab_add = [[0] * q for _ in range(q)]
    tab_mul = [[0] * q for _ in range(q)]
    for a in range(q):
        for b in range(q):
            tab_add[a][b] = to_val([(x + y) % p for x, y in zip(to_poly(a), to_poly(b))])
            tab_mul[a][b] = to_val(pmul(to_poly(a), to_poly(b)))
    return q, tab_add, tab_mul


def pow_via_mul(mul, x, k):
    r = 1
    for _ in range(k):
        r = mul[r][x]
    return r

def build_pg(q2):
    if q2 == 4:
        p, e, modpoly = 2, 2, [1, 1, 1]
    elif q2 == 9:
        p, e, modpoly = 3, 2, [1, 0, 1]
    elif q2 == 16:
        p, e, modpoly = 2, 4, [1, 1, 0, 0, 1]
    else:
        raise ValueError(q2)
    q, add, mul = make_gf(p, e, modpoly)
    # subfield for the Baer subplane: GF(sqrt(q)) = GF(p^(e/2)) when e even,
    # else prime subfield GF(p).
    if e % 2 == 0:
        half = p ** (e // 2)
        sub = [x for x in range(q) if pow_via_mul(mul, x, half) == x]
        assert len(sub) == half
    else:
        sub = [0]
        x = 1
        while x not in sub:
            sub.append(x)
            x = add[x][1]
        assert len(sub) == p
    inv = {}
    for a in range(1, q):
        for b in range(1, q):
            if mul[a][b] == 1:
                inv[a] = b
                break
    def canon(v):
        for i in range(3):
            if v[i] != 0:
                s = inv[v[i]]
                return tuple(mul[s][v[i]] for i in range(3))
        return None
    pts = {}
    for a in range(q):
        for b in range(q):
            for c in range(q):
                if a == 0 and b == 0 and c == 0:
                    continue
                pnt = canon([a, b, c])
                if pnt not in pts:
                    pts[pnt] = len(pts)
    plist = list(pts.keys())
    n = len(plist)
    assert n == q * q + q + 1
    def sc(pv, s):
        return tuple(mul[s][pv[i]] for i in range(3))
    def ad(x, y):
        return tuple(add[x[i]][y[i]] for i in range(3))
    lines = set()
    for i in range(n):
        for j in range(i + 1, n):
            member = set()
            for a in range(q):
                for b in range(q):
                    if a == 0 and b == 0:
                        continue
                    member.add(pts[canon(list(ad(sc(plist[i], a), sc(plist[j], b))))])
            if len(member) != q + 1:
                raise AssertionError('line size')
            lines.add(tuple(sorted(member)))
    lines = sorted(lines)
    assert len(lines) == n
    from collections import defaultdict
    pc = defaultdict(int)
    for L in lines:
        for i in range(len(L)):
            for j in range(i + 1, len(L)):
                pc[(L[i], L[j])] += 1
    assert len(pc) == n * (n - 1) // 2 and all(v == 1 for v in pc.values())
    inc = [[] for _ in range(n)]
    for li, L in enumerate(lines):
        for pt in L:
            inc[pt].append(li)
    assert all(len(inc[pt]) == q + 1 for pt in range(n))
    base = [i for i, pv in enumerate(plist) if all(pv[k] in sub for k in range(3))]
    return {'q': q, 'p': p, 'n': n, 'points': [list(pv) for pv in plist],
            'lines': [list(L) for L in lines], 'inc': inc,
            'add': add, 'mul': mul, 'inv': inv, 'subfield': sub,
            'baer_base': base, 'plist': plist}

if __name__ == '__main__':
    import os
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = {}
    for q2 in (9, 16):
        b = build_pg(q2)
        print(f'PG(2,{q2}): {b["n"]} pts, {len(b["lines"])} lines, design OK, '
              f'baer_base={len(b["baer_base"])} pts, prime subfield={b["subfield"]}')
        out[f'pg2q{q2}'] = {k: v for k, v in b.items() if k not in ('plist',)}
    with open(os.path.join(root, 'out', 'boards9.json'), 'w') as f:
        json.dump(out, f)
    print('wrote boards9.json')
