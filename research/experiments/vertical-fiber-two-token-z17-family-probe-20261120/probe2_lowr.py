import sys
from functools import lru_cache
sys.setrecursionlimit(200000)
def mex(v):
    m=0; v=set(v)
    while m in v: m+=1
    return m
@lru_cache(None)
def H(R, X, z):
    if R==0: return 0
    opts=set()
    for i,v in enumerate(X):
        if v>1: opts.add(H(R-1, X[:i]+(v-1,)+X[i+1:], z))
        else: opts.add(H(R-1, X[:i]+X[i+1:], z+1))
    if z: opts.add(1^H(R-1,X,z-1))
    return mex(opts)
z=17
print('== low-R reduction: two tokens (x,y) vs single token (S,) ==')
for y in (6,7,8,9,10,11):
    worst=(10**9,None)
    breaks=[]
    for x in range(y, min(y+25, 50)+1):
        S=x+y; Rmax=x+40
        thr=None
        for R in range(0, Rmax+1):
            if H(R,(x,y),z)!=H(R,(S,),z):
                thr=R; break
        if thr is None: thr=10**9
        elif thr<40:
            breaks.append((x,y,thr))
            if thr<worst[0]: worst=(thr,x)
    print(f'y={y}: min-break={worst[0]} at x={worst[1]}; low breaks(<40): n={len(breaks)} first3={breaks[:3]}')
print('== flat uniform scan: does R<=23 hold everywhere? ==')
bad=[]
for y in range(6,13):
    for x in range(y, min(y+20,45)+1):
        S=x+y
        for R in range(0, min(24, x+40)+1):
            if H(R,(x,y),z)!=H(R,(S,),z):
                bad.append((x,y,R)); break
print('rows breaking R<=23:', len(bad))
for b in bad[:10]: print('  x=%d y=%d first R=%d' % b)
print('cache:', H.cache_info())
