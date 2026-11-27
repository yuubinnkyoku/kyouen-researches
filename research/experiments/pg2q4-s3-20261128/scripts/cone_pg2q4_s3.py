"""PG(2,4) s=3 complete Grundy spectrum via the cone + frame double counting method.

Board: research/experiments/projective-blocking-kyouen-20261125/output/board_pg2q4.txt
(21 points, 21 lines of 5). s=3 game: safe iff |S cap L| <= 3.

F = {0,1,5} (non-collinear triangle).  PGL(3,4) is transitive on triangles;
caps of size >=4 cannot be collinear, so every cap of size >=4 contains a triangle.
N_m(g) = N3 * T_m(g) / C(m,3), N3 = C(21,3) - 21*C(5,3) = 1120.
Collinear 3-caps (210) are handled by a second cone; k=0,1,2 by the mex chain.
"""
import math
from collections import Counter, defaultdict
from pathlib import Path
HERE = Path(__file__).resolve().parents[1]
BLOCK = HERE.parents[0] / 'projective-blocking-kyouen-20261125' / 'output' / 'board_pg2q4.txt'
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

tri = (1 << 0) | (1 << 1) | (1 << 5)
order, g = cone(tri)
T = Counter(); Tg = defaultdict(Counter)
for m in order:
    T[m.bit_count()] += 1; Tg[m.bit_count()][g[m]] += 1
N3 = math.comb(21, 3) - 21 * math.comb(5, 3)
print('triangle cone', len(order), 'G3', g[tri], 'N3', N3)
res = {'cone_size': len(order), 'G3': g[tri], 'N3': N3, 'sizes': {}}
for m in sorted(T):
    C = math.comb(m, 3)
    assert N3 * T[m] % C == 0
    res['sizes'][str(m)] = {'T': T[m], 'T_g': dict(Tg[m]), 'N': N3 * T[m] // C,
                            'N_g': {str(k): N3 * v // C for k, v in Tg[m].items()}}
# collinear 3-caps: cone of {0,1,2} (on line 0)
col = (1 << 0) | (1 << 1) | (1 << 2)
order2, g2 = cone(col)
print('collinear cone', len(order2), 'G', g2[col])
res['collinear_G'] = g2[col]
# merge the collinear 3-caps (210, G=0) into the size-3 entry
res['sizes']['3']['N'] += 210
res['sizes']['3']['N_g']['0'] = res['sizes']['3']['N_g'].get('0', 0) + 210
# k=0,1,2 by mex chain (all 3-caps G=0)
res['sizes']['2'] = {'N': math.comb(21, 2), 'N_g': {str(1): math.comb(21, 2)}}
res['sizes']['1'] = {'N': 21, 'N_g': {str(0): 21}}
res['sizes']['0'] = {'N': 1, 'N_g': {str(1): 1}}
print(res['sizes'])
import json
(HERE / 'output' / 'pg2q4_s3_spectrum.json').write_text(json.dumps(res, indent=1))
