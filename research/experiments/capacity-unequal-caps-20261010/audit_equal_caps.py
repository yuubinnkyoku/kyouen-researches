from functools import lru_cache
from itertools import product
from collections import Counter

def audit():
    total=0; gmax=0; evmax=0; counts=Counter(); witness=None
    for w in range(2,8):
      for h in range(1,w):
       for m in range(1,5):
        for r in range(h*m):
         @lru_cache(None)
         def grundy(x):
          v=set()
          for i in range(w):
           if x[i]>=m:continue
           nxt=list(x);nxt[i]+=1
           if sum(sorted(nxt,reverse=True)[:h])<=r:
            v.add(grundy(tuple(nxt)))
          k=0
          while k in v:k+=1
          return k
         for x in product(range(m+1),repeat=w):
          if sum(sorted(x,reverse=True)[:h])>r:continue
          g=grundy(x)
          slack=r-sum(sorted(x,reverse=True)[:h]);total+=1
          counts[(slack%2,g)]+=1
          if slack%2==0 and g>1:raise AssertionError((w,h,m,r,x,g))
          if g>3:raise AssertionError((w,h,m,r,x,g))
          if g>gmax:gmax=g;witness=(w,h,m,r,x,slack)
    print('PASS',total,counts,'gmax',gmax,'witness',witness)
if __name__=='__main__':audit()
