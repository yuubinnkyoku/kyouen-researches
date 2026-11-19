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
print('== deep-y skeleton (raw recursion, per-row fresh cache) ==')
for y in (13,20,40):
    for d in (9,17,18,19):
        H.cache_clear()
        x=y+d; S=x+y
        if d==18: Rmax=min(S+30, x+45)+1
        elif d==19: Rmax=min(S+24, x+45)+1
        else: Rmax=min(2*y+44, x+45)+1
        vals=[H(R,(x,y),z) for R in range(Rmax+1)]
        T=[R for R in range(1,Rmax+1) if vals[R]==2]
        r=2*y+(d+z)//2
        if d==17:
            exp=set(range(1,18,2))|({r} if r<=Rmax else set()); okexp=(set(T)==exp)
            print(f'y={y} pin d=17 x={x}: tok={r<=Rmax and vals[r]==2} extras={sorted(set(T)-(set(range(1,18,2))|{r}))[:4]} ok={okexp}')
        elif d==9:
            print(f'y={y} lattice d=9 x={x}: point@{r}={vals[r]} gapclean={all(vals[q]==0 for q in range(19,r,2))}')
        elif d==18:
            exp=set(range(1,18,2))|set(range(2*y+17,S+18,2)); okexp=(set(T)==(exp&set(range(1,Rmax+1))))
            band=[t for t in T if t>17]
            print(f'y={y} sweep d=18 x={x} S={S}: bandok={okexp} band=({band[0] if band else None},{band[-1] if band else None}) want=({2*y+17},{S+17 if S%2==1 else S+16})')
        else:
            Texp=set(range(1,18,2))|({2*y+17} if 2*y+17<=Rmax else set())
            Pset={R for R in range(1,Rmax+1) if vals[R]==1}
            Pexp=set(range(18,2*y+17,2))|{R for R in range(2*y+19,S+18,2)}
            if S%2: Pexp|=set(range(S+18,Rmax+1))
            mism=(set(T)!=(Texp&set(range(1,Rmax+1)))) or (Pset!=(Pexp&set(range(1,Rmax+1))))
            print(f'y={y} steady d=19 x={x} S={S}: mismatch={mism} tailv={vals[-1]} want={S%2}')
print('cache:', H.cache_info())
