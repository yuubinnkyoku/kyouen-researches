"""Independent finite check of the rectangular high-q closed form."""
from itertools import combinations, product
from math import comb, gcd, prod

def closed(ns,q):
    return sum(comb(k-2,q-2)*(prod(n+2*max(0,n-k+1) for n in ns)-prod(ns))//2
               for k in range(q,max(ns)+1))

def brute(ns,q):
    pts=list(product(*(range(n) for n in ns)))
    ans=0
    for ids in combinations(range(len(pts)),q):
        a,b=pts[ids[0]],pts[ids[1]]
        v=tuple(y-x for x,y in zip(a,b))
        if all(all((p[i]-a[i])*v[j]==(p[j]-a[j])*v[i]
                   for i in range(len(ns)) for j in range(i+1,len(ns)))
               for p in (pts[t] for t in ids[2:])):
            ans+=1
    return ans

def main():
    count=0
    for d,limit in ((2,4),(3,3)):
        for ns in product(range(1,limit+1),repeat=d):
            if prod(ns)>27: continue
            for q in range(2,max(ns)+1):
                if 2*(q-1)<=max(ns)-1: continue
                assert closed(ns,q)==brute(ns,q),(ns,q)
                count+=1
    print("Independent tuple-determinant checks:",count)

if __name__=="__main__": main()
