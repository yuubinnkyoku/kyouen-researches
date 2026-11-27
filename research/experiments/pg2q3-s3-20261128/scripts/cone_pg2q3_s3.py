"""PG(2,3) s=3 complete Grundy spectrum via the cone + frame double counting method.

Board: research/experiments/projective-blocking-kyouen-20261125/output/board_pg2q3.txt
(13 points, 13 lines of 4). s=3 game: safe iff |S cap L| <= 3.

3-caps split into two PGL(3,3) orbits: triangles (234) and collinear triples (52).
Both orbits enter the double count:
  N_m(g) = (234*T_m(g) + 52*U_m(g)) / C(m,3).
k=0,1,2 by the mex chain.
"""
import math
from collections import Counter, defaultdict
from pathlib import Path
HERE = Path(__file__).resolve().parents[1]
BLOCK = HERE.parents[0] / 'projective-blocking-kyouen-20261125' / 'output' / 'board_pg2q3.txt'
lines = BLOCK.read_text().splitlines()
n, b = map(int, lines[0].split())
blocks = []
for l in lines[1:]:
    m = 0
    for p in list(map(int, l.split()[1:])):
        m |= 1 << p
    blocks.append(m)
pc = [[] for _ in range(n)]
for c, m in enumerate(blocks):
    for p in range(n):
        if (m >> p) & 1:
            pc[p].append(c)
S = 3

def cone(F):
    used = [False] * n
    counts = [0] * len(blocks)
    for p in range(n):
        if (F >> p) & 1:
            used[p] = True
    for p in range(n):
        if used[p]:
            for c in pc[p]:
                counts[c] += 1
    order = []
    def dfs(mask, start):
        order.append(mask)
        for p in range(start, n):
            if used[p]:
                continue
            if any(counts[c] >= S for c in pc[p]):
                continue
            used[p] = True
            for c in pc[p]:
                counts[c] += 1
            dfs(mask | (1 << p), p + 1)
            for c in pc[p]:
                counts[c] -= 1
            used[p] = False
    dfs(F, 0)
    g = {}
    for m in sorted(order, key=lambda x: -x.bit_count()):
        ch = set()
        for p in range(n):
            if (m >> p) & 1:
                continue
            nm = m | (1 << p)
            if nm in g:
                ch.add(g[nm])
        v = 0
        while v in ch:
            v += 1
        g[m] = v
    return order, g

tri = (1 << 0) | (1 << 1) | (1 << 4)
col = (1 << 0) | (1 << 1) | (1 << 2)
o1, g1 = cone(tri); o2, g2 = cone(col)
print('triangle cone', len(o1), 'G', g1[tri], '| collinear cone', len(o2), 'G', g2[col])
Ntri, Ncol = 234, 52
T = Counter(); Tg = defaultdict(Counter); U = Counter(); Ug = defaultdict(Counter)
for m in o1:
    T[m.bit_count()] += 1; Tg[m.bit_count()][g1[m]] += 1
for m in o2:
    U[m.bit_count()] += 1; Ug[m.bit_count()][g2[m]] += 1
res = {'cone_triangle': len(o1), 'cone_collinear': len(o2), 'G3': g1[tri], 'sizes': {}}
for m in sorted(set(T) | set(U)):
    C = math.comb(m, 3)
    num = Ntri * T[m] + Ncol * U[m]
    assert num % C == 0
    vals = set(Tg[m]) | set(Ug[m])
    res['sizes'][str(m)] = {'T': T[m], 'T_g': dict(Tg[m]), 'U': U[m], 'U_g': dict(Ug[m]),
                            'N': num // C,
                            'N_g': {str(v): (Ntri * Tg[m].get(v, 0) + Ncol * Ug[m].get(v, 0)) // C
                                    for v in vals}}
res['sizes']['2'] = {'N': math.comb(13, 2), 'N_g': {str(1): math.comb(13, 2)}}
res['sizes']['1'] = {'N': 13, 'N_g': {str(0): 13}}
res['sizes']['0'] = {'N': 1, 'N_g': {str(1): 1}}
import json
(HERE / 'output' / 'pg2q3_s3_spectrum.json').write_text(json.dumps(res, indent=1))
print(res)
