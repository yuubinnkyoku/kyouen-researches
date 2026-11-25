#!/usr/bin/env python3
"""Independent root-legal-move rederivation for the WIN8 root
00000000000000801202000000901010 (pure-integer lifted 3x3 cofactor geometry,
stdlib only, no engine import).  Writes output/root-legal-moves.txt (comma CSV)."""
ROOT = 0x00000000000000801202000000901010

def lifted(b):
    x, y = b % 11, b // 11
    return (x*x + y*y, x, y, 1)

def det3(m):
    (a,b,c),(d,e,f),(g,h,i) = m
    return a*(e*i-f*h) - b*(d*i-f*g) + c*(d*h-e*g)

_cache = {}
def triple_banned(a, b, c):
    key = (a,b,c)
    v = _cache.get(key)
    if v is not None: return v
    rows = [lifted(q) for q in (a,b,c)]
    coeff = []
    for col in range(4):
        minor = [[rows[r][cc] for cc in range(4) if cc != col] for r in range(3)]
        d3 = det3(minor)
        coeff.append(d3 if col % 2 == 0 else -d3)
    mask = 0
    for d in range(121):
        if d in (a,b,c): continue
        r = lifted(d)
        if coeff[0]*r[0] + coeff[1]*r[1] + coeff[2]*r[2] + coeff[3]*r[3] == 0:
            mask |= 1 << d
    _cache[key] = mask
    return mask

def bits_of(m):
    out = []
    for i in range(121):
        if m >> i & 1: out.append(i)
    return out

pts = bits_of(ROOT)
assert len(pts) == 8
banned = 0
for p in pts: banned |= 1 << p
for i in range(8):
    for j in range(i+1, 8):
        for k in range(j+1, 8):
            banned |= triple_banned(pts[i], pts[j], pts[k])
legal = ((1 << 121) - 1) & ~banned
moves = bits_of(legal)
print('mobility:', len(moves))
with open('output/root-legal-moves.txt', 'w') as f:
    f.write(','.join(str(m) for m in moves) + '\n')
