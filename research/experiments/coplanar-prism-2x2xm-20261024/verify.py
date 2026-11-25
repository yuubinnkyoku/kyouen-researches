#!/usr/bin/env python3
"""Complete small-m 2x2xm q4 coplanarity game via exact integer determinants."""
from collections import Counter
from itertools import combinations
import json, sys

def coplanar(a,b,c,d):
    u=[b[i]-a[i] for i in range(3)]
    v=[c[i]-a[i] for i in range(3)]
    w=[d[i]-a[i] for i in range(3)]
    return (u[1]*v[2]-u[2]*v[1])*w[0]+(u[2]*v[0]-u[0]*v[2])*w[1]+(u[0]*v[1]-u[1]*v[0])*w[2]==0

def bits(mask):
    while mask:
        b=mask&-mask
        yield b
        mask-=b

def mex(vals):
    i=0
    while i in vals:i+=1
    return i

def solve(m):
    pts=[(x,y,z) for x in range(2) for y in range(2) for z in range(m)]
    n=len(pts)
    block={tri:0 for tri in combinations(range(n),3)}
    forbidden=0
    for a,b,c,d in combinations(range(n),4):
        if coplanar(pts[a],pts[b],pts[c],pts[d]):
            forbidden+=1
            for tri,other in (((a,b,c),d),((a,b,d),c),((a,c,d),b),((b,c,d),a)):
                block[tri]|=1<<other
    layers=[[0]]
    nexts={}
    for size in range(5):
        new=[]
        for mask in layers[-1]:
            indices=[i for i in range(n) if mask>>i&1]
            blocked=0
            for tri in combinations(indices,3):
                blocked |= block[tri]
            legal=((1<<n)-1)&~mask&~blocked
            nexts[mask]=legal
            for bit in bits(legal):
                new.append(mask|bit)
        if not new:break
        layers.append(sorted(set(new)))
    g={};h={}
    layer_stats=[]
    for size in range(len(layers)-1,-1,-1):
        for mask in layers[size]:
            legal=nexts.get(mask,0)
            gg={g[mask|bit] for bit in bits(legal)}
            hh={h[mask|bit] for bit in bits(legal)}
            g[mask]=mex(gg)
            h[mask]=mex(hh) if legal else 1
            if m>=3:
                assert g[mask]==((5-size)&1)
                assert h[mask]==(1-g[mask])
        layer_stats.append({'size':size,'safe':len(layers[size]),
            'maximal':sum(not nexts.get(mask,0) for mask in layers[size]),
            'grundy':dict(sorted(Counter(g[mask] for mask in layers[size]).items())),
            'misere':dict(sorted(Counter(h[mask] for mask in layers[size]).items()))})
    layer_stats.reverse()
    return {'m':m,'points':n,'forbidden':forbidden,'safe':sum(map(len,layers)),
        'K':len(layers)-1,'s':min(x['size'] for x in layer_stats if x['maximal']),
        'g_empty':g[0],'h_empty':h[0],'layers':layer_stats}

if __name__=='__main__':
    for m in map(int,sys.argv[1:] or range(1,8)):
        print(json.dumps(solve(m),ensure_ascii=False,sort_keys=True),flush=True)
