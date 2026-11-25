#!/usr/bin/env python3
from itertools import combinations
from functools import lru_cache
import json
def check(m):
    pts=[(x,y) for x in range(m) for y in range(2)]
    n=len(pts)
    blocks=[]
    for ids in combinations(range(n),4):
        a=[pts[i][0] for i in ids if pts[i][1]==0]
        b=[pts[i][0] for i in ids if pts[i][1]==1]
        if len(a)==4 or len(b)==4 or (len(a)==len(b)==2 and sum(a)==sum(b)):
            blocks.append(sum(1<<i for i in ids))
    by=[[] for _ in pts]
    for mask in blocks:
        for i in range(n):
            if mask>>i&1:by[i].append(mask^(1<<i))
    def moves(s):
        return [s|(1<<i) for i in range(n) if not s>>i&1 and
                not any((s&t)==t for t in by[i])]
    @lru_cache(None)
    def gh(s):
        children=[gh(t) for t in moves(s)]
        if not children:return 0,1
        gs={a for a,b in children};hs={b for a,b in children}
        g=h=0
        while g in gs:g+=1
        while h in hs:h+=1
        return g,h
    gh(0)
    todo=[0];seen={0};bad=[];hist={}
    while todo:
        s=todo.pop();g,h=gh(s)
        if h!=(1-g if g<2 else g):
            bad.append((s,g,h))
            k=s.bit_count();hist[k]=hist.get(k,0)+1
        for t in moves(s):
            if t not in seen:seen.add(t);todo.append(t)
    witness=None
    if bad:
        s,g,h=min(bad,key=lambda z:(z[0].bit_count(),z[0]))
        witness={'points':[pts[i] for i in range(n) if s>>i&1],'g':g,'h':h}
    return {'m':m,'forbidden':len(blocks),'states':len(seen),
            'mismatches':len(bad),'by_size':hist,'empty':gh(0),'witness':witness}
if __name__=='__main__':
    result=[check(m) for m in range(1,10)]
    print(json.dumps(result,ensure_ascii=False,indent=2))
    assert [r['states'] for r in result]==[4,15,54,169,470,1167,2674,5635,11130]
    assert [r['mismatches'] for r in result]==[0,0,0,0,9,16,0,0,0]
