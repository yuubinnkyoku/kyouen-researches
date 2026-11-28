import os
"""PG(2,q) board construction over GF(q), q=3,4. Independent construction + design check."""
import json

def gf4_tables():
    # elements 0,1,2(alpha),3(alpha+1); alpha^2 = alpha+1
    mul = [[0]*4 for _ in range(4)]
    for a in range(4):
        for b in range(4):
            if a == 0 or b == 0:
                mul[a][b] = 0
            elif a == 1:
                mul[a][b] = b
            elif b == 1:
                mul[a][b] = a
            elif a == 2:  # alpha * b
                mul[a][b] = {2: 3, 3: 1}[b]
            else:         # (alpha+1)*b
                mul[a][b] = {2: 1, 3: 2}[b]
    return mul

def make_field(q):
    if q == 3:
        mul = [[(a*b) % 3 for b in range(3)] for a in range(3)]
    elif q == 4:
        mul = gf4_tables()
    else:
        raise ValueError(q)
    if q == 4:
        # GF(4) addition is XOR on {0,1,2,3}
        add = [[a ^ b for b in range(4)] for a in range(4)]
    else:
        add = [[(a+b) % q for b in range(q)] for a in range(q)]
    neg = [[(-a) % q for a in range(q)]]
    return add, mul

def inv_table(q, mul):
    inv = {}
    for a in range(1, q):
        for b in range(1, q):
            if mul[a][b] == 1:
                inv[a] = b
                break
    return inv

def build_pg(q):
    add, mul = make_field(q)
    inv = inv_table(q, mul)
    # points: 1-d subspaces, canonical rep: first nonzero coord = 1
    pts = {}
    def canon(v):
        for i in range(3):
            if v[i] != 0:
                s = inv[v[i]]
                return tuple(mul[s][v[i]] for i in range(3))
        return None
    for a in range(q):
        for b in range(q):
            for c in range(q):
                if a == 0 and b == 0 and c == 0:
                    continue
                p = canon([a, b, c])
                if p not in pts:
                    pts[p] = len(pts)
    plist = list(pts.keys())
    n = len(plist)
    assert n == q*q + q + 1, (n, q)
    # lines: span of pairs of distinct points
    lines = set()
    def pt_mul(p, s):
        return tuple(mul[s][p[i]] for i in range(3))
    def pt_add(p, r):
        return tuple(add[p[i]][r[i]] for i in range(3))
    for i in range(n):
        for j in range(i+1, n):
            if pts[plist[i]] == pts[plist[j]]:
                continue
            member = []
            seen = set()
            for a in range(q):
                for b in range(q):
                    if a == 0 and b == 0:
                        continue
                    v = pt_add(pt_mul(plist[i], a), pt_mul(plist[j], b))
                    member.append(pts[canon(list(v))])
            member = tuple(sorted(set(member)))
            if len(member) != q+1:
                raise AssertionError('line size')
            lines.add(member)
    lines = sorted(lines)
    assert len(lines) == n, (len(lines), n)
    # design check: every pair of points on exactly one line
    from collections import defaultdict
    paircount = defaultdict(int)
    for L in lines:
        for i in range(len(L)):
            for j in range(i+1, len(L)):
                paircount[(L[i], L[j])] += 1
    assert len(paircount) == n*(n-1)//2
    assert all(v == 1 for v in paircount.values())
    # incidence: lines through each point
    inc = [[] for _ in range(n)]
    for li, L in enumerate(lines):
        for p in L:
            inc[p].append(li)
    assert all(len(inc[p]) == q+1 for p in range(n))
    return {
        'q': q, 'n': n, 'points': [[int(x) for x in p] for p in plist],
        'lines': [list(L) for L in lines], 'inc': inc,
    }

if __name__ == '__main__':
    out = {}
    for q in (3, 4):
        b = build_pg(q)
        out[f'pg2q{q}'] = b
        print(f'PG(2,{q}): {b["n"]} points, {len(b["lines"])} lines, design check OK')
    with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/out/boards.json', 'w') as f:
        json.dump(out, f)
    print('wrote boards.json')
