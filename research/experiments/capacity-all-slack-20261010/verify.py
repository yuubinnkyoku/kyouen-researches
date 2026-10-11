#!/usr/bin/env python3
"""Independent all-slack capacity game check: profile-signature theorem vs direct mex.
Finite exhaustive ranges: 3<=w<=8, 2<=h<w, 1<=m<=6, 1<=r<h*m.
"""
from functools import lru_cache
from itertools import combinations_with_replacement
from collections import Counter

def upper_children(u,m):
    out=set()
    for i,v in enumerate(u):
        if v==m:continue
        z=list(u);z[i]+=1;z.sort(reverse=True)
        out.add(tuple(z))
    return out

def check(wmax=8,mmax=6):
    counts=Counter();examples={}
    for w in range(3,wmax+1):
        for h in range(2,w):
            n=w-h
            for m in range(1,mmax+1):
                states=[tuple(reversed(z)) for z in combinations_with_replacement(range(m+1),w)]
                for r in range(1,h*m):
                    @lru_cache(None)
                    def signature(u):
                        sigma=r-sum(u)
                        if sigma==0:return ('even',0)
                        children=upper_children(u,m)
                        assert children, (w,h,m,r,u,sigma)
                        if sigma%2:
                            bits={((n*(v[-1]-u[-1])+signature(v)[1])%2) for v in children}
                            assert all(signature(v)[0]=='even' for v in children)
                            return ('odd-single',next(iter(bits))) if len(bits)==1 else ('odd-mixed',None)
                        else:
                            low=[]
                            for v in children:
                                typ,bit=signature(v)
                                if typ=='odd-single':low.append((n*(v[-1]-u[-1])+bit+1)%2)
                            assert len(set(low))<=1,(w,h,m,r,u,low)
                            return ('even',(low[0]+1)%2 if low else 0)
                    @lru_cache(None)
                    def exact(x):
                        child_values=set()
                        for i,v in enumerate(x):
                            if v==m or (i and x[i-1]==v):continue
                            z=list(x);z[i]+=1;z.sort(reverse=True);z=tuple(z)
                            if sum(z[:h])<=r:child_values.add(exact(z))
                        mex=0
                        while mex in child_values:mex+=1
                        return mex
                    for x in states:
                        if sum(x[:h])>r:continue
                        u=x[:h];b=u[-1];R=n*b-sum(x[h:]);sigma=r-sum(u)
                        typ,bit=signature(u)
                        predicted=(R+bit)%2 if typ=='even' else ((R+bit+1)%2 if typ=='odd-single' else 2+(R%2))
                        observed=exact(x)
                        assert predicted==observed,(w,h,m,r,x,typ,bit,R,observed,predicted)
                        counts['positions']+=1
                        counts['sigma_even' if sigma%2==0 else 'sigma_odd']+=1
                        counts[f'g{observed}']+=1
                        counts[f'sigma{sigma}']+=1
                        if observed>=2 and f'g{observed}' not in examples:
                            examples[f'g{observed}']=(w,h,m,r,x,sigma,R)
    print('PASS',dict(counts))
    print('EXAMPLES',examples)
if __name__=='__main__':check()
