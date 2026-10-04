"""Extend Q_p equality witnesses beyond p=127.

Searches all odd primes in [131,251].  The SAT encoding is the same pair-choice
reduction as parabola_half_bound.py.  A found witness is independently checked
by a generic Bareiss 4x4 determinant, not by the SAT clauses.
"""
from itertools import combinations
import json

def prime(n):
    return n>=2 and all(n%d for d in range(2,int(n**.5)+1))

def det_fast(ps):
    x0,y0=ps[3]
    a=[]
    for x,y in ps[:3]:
        X=x-x0; Y=y-y0
        a.append((X,Y,X*X+Y*Y))
    return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
           -a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
           +a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))

def bareiss(mat):
    a=[row[:] for row in mat]; n=len(a); prev=1; sign=1
    for k in range(n-1):
        if a[k][k]==0:
            j=next((j for j in range(k+1,n) if a[j][k]),None)
            if j is None:return 0
            a[k],a[j]=a[j],a[k]; sign=-sign
        pivot=a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                a[i][j]=(a[i][j]*pivot-a[i][k]*a[k][j])//prev
        prev=pivot
    return sign*a[-1][-1]

def det_independent(ps):
    return bareiss([[1,x,y,x*x+y*y] for x,y in ps])

def forbidden(p):
    pts=[(t,t*t%p) for t in range(p)]; edges=[]; candidates=0
    for i,j,k in combinations(range(p),3):
        l=(-i-j-k)%p
        if l>k:
            candidates+=1
            if det_fast([pts[t] for t in (i,j,k,l)])==0:
                edges.append((i,j,k,l))
    return pts,edges,candidates

def clauses_for_pair(p,edges,double):
    out=set()
    for edge in edges:
        req={}; impossible=False
        for t in edge:
            if t==0 or min(t,p-t)==double:continue
            v=min(t,p-t); sign=t>p//2
            if v in req and req[v]!=sign:
                impossible=True; break
            req[v]=sign
        if not impossible:
            out.add(tuple(-v if sign else v for v,sign in req.items()))
    return tuple(out)

def solve(clauses,assignment=None,counter=None):
    if assignment is None:assignment={}
    if counter is None:counter=[0]
    counter[0]+=1
    while True:
        rem=[]; unit=None
        for clause in clauses:
            if any(abs(x) in assignment and assignment[abs(x)]==(x>0) for x in clause):continue
            c=tuple(x for x in clause if abs(x) not in assignment)
            if not c:return None
            rem.append(c)
            if len(c)==1:unit=c[0]
        if not rem:return assignment
        if unit is None:break
        assignment=dict(assignment); assignment[abs(unit)]=unit>0; clauses=rem
    counts={}
    for c in rem:
        for x in c:counts[abs(x)]=counts.get(abs(x),0)+1/(2**len(c))
    v=max(counts,key=counts.get)
    for sign in (False,True):
        a=dict(assignment); a[v]=sign
        r=solve(rem,a,counter)
        if r is not None:return r
    return None

def search(p):
    pts,edges,candidates=forbidden(p); h=(p-1)//2
    for d in range(h,0,-1):
        clauses=clauses_for_pair(p,edges,d); counter=[0]
        sol=solve(clauses,counter=counter)
        if sol is None:continue
        ts=[0,d,p-d]+[p-i if sol.get(i,False) else i for i in range(1,h+1) if i!=d]
        ts.sort()
        assert len(ts)==h+2 and len(set(ts))==h+2
        # Independent post-check: generic 4x4 Bareiss determinant.
        for q in combinations(ts,4):
            ps=[pts[t] for t in q]
            assert det_independent(ps)!=0
        return {"p":p,"maximum_proved":h+2,"double_pair":d,"parameters":ts,
                "forbidden_quadruples":len(edges),"candidate_quadruples":candidates,
                "clauses":len(clauses),"sat_calls":counter[0]}
    raise AssertionError(("no equality witness",p))

rows=[]
for p in range(131,252):
    if prime(p):
        r=search(p); rows.append(r); print(p,r["maximum_proved"],r["double_pair"],flush=True)
with open("parabola_equality_131_251.json","w",encoding="utf-8") as f:
    json.dump(rows,f,indent=2); f.write("\n")
