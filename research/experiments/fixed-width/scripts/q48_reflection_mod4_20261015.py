from math import isqrt

def by_chords(m):
    ans=set()
    for a in range(1,m):
        for b in range(1,m):
            c2=2*b*b-a*a-8
            d2=3*b*b-2*a*a-24
            if c2<=0 or d2<=0: continue
            c=isqrt(c2); d=isqrt(d2)
            if c*c!=c2 or d*d!=d2: continue
            if (a-b)%2 or (a-c)%2 or (a-d)%2: continue
            D=max(a,b,c,d)
            if D>=m: continue
            for S in range(D,2*(m-1)-D+1,2):
                ans.add(tuple(((S-t)//2,(S+t)//2) for t in (a,b,c,d)))
    return ans

def roots(s,p,m):
    disc=s*s-4*p
    if disc<=0: return None
    d=isqrt(disc)
    if d*d!=disc or (s-d)%2: return None
    a=(s-d)//2; b=(s+d)//2
    return (a,b) if 0<=a<b<m else None

def by_row_pairs(m):
    ans=set()
    for s in range(1,2*m-2):
        pairs=[(a,s-a) for a in range(max(0,s-m+1),(s+1)//2) if s-a<m]
        for a,b in pairs:
            p0=a*b
            for c,d in pairs:
                p1=c*d
                B=p1-p0-1
                r2=roots(s,p0+4+2*B,m)
                if r2 is None: continue
                r3=roots(s,p0+9+3*B,m)
                if r3 is not None: ans.add(((a,b),(c,d),r2,r3))
    return ans

for m in range(1,101):
    a=by_chords(m)
    b=by_row_pairs(m)
    assert a==b,(m,len(a),len(b),list(a-b)[:3],list(b-a)[:3])
    local=max(0,m-3)
    assert (len(a)-local)%2==0
    if m%2: assert (len(a)-local)%4==0
    # Every nonlocal reflection pair of chord patterns gives two(m-D) circles
    pat={tuple(row[1]-row[0] for row in circle) for circle in a}
    nonloc={tuple(sorted((p,p[::-1]))) for p in pat if p!=(1,3,3,1)}
    correction=2*len(nonloc) if m%2==0 else 0
    assert (len(a)-local-correction)%4==0,(m,len(a),len(nonloc))
    if m in (4,5,6,7,8,73,74,75,76,100): print(m,len(a),len(nonloc),len(a)%4)
print('ALL CHECKED: 1..100')
