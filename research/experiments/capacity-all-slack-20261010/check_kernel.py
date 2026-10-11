from functools import lru_cache
from itertools import combinations_with_replacement
from collections import Counter
stats=Counter()
for h in range(1,8):
 for m in range(1,13):
  for r in sorted(set([max(0,h*m-1),h*m//2,max(0,h*m//3)])):
   @lru_cache(None)
   def F(u):
    b=u[-1]; p=b%2  # n odd, n=1
    vals=set()
    if sum(u)<r:
     for i,x in enumerate(u):
      if x==m or (i and u[i-1]==x):continue
      v=list(u);v[i]+=1;v.sort(reverse=True)
      vals.add(F(tuple(v))^p)
    z=0
    while z in vals:z+=1
    return z^p
   for c in combinations_with_replacement(range(m+1),h):
    u=c[::-1]
    if sum(u)>r:continue
    s=r-sum(u)
    g=F(u)
    stats['profiles']+=1
    if s%2==0 and g>=2 or s%2==1 and g>=4:
     print('COUNTEREXAMPLE',h,m,r,u,s,g);raise SystemExit(1)
 print('h',h,'profiles',stats['profiles'],flush=True)
print('PASS',stats)
