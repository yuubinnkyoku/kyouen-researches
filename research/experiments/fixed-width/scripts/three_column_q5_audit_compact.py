"""Independent chord-vs-determinant audit for 3-column 5-point circles."""
from fractions import Fraction as F
from itertools import combinations as choose
from math import gcd, lcm

def key(a,b,c):
    x,y=a; u,v=b; s,t=c
    p=u-x; q=v-y; r=s-x; z=t-y
    D=p*z-q*r
    if not D: return None
    A=-(u*u+v*v-x*x-y*y)*z+q*(s*s+t*t-x*x-y*y)
    B=-p*(s*s+t*t-x*x-y*y)+(u*u+v*v-x*x-y*y)*r
    C=-D*(x*x+y*y)-A*x-B*y
    g=gcd(gcd(abs(D),abs(A)),gcd(abs(B),abs(C)))
    out=tuple(n//g for n in (D,A,B,C))
    return tuple(-n for n in out) if out[0]<0 else out

def audit(h,d,m):
    cols=[[(i*h,j*d) for j in range(m)] for i in range(3)]
    P=sum(cols,[])
    det=set()
    for a,b,c in choose(P,3):
        k=key(a,b,c)
        if k: det.add(k)
    det={k:frozenset(p for p in P if k[0]*(p[0]**2+p[1]**2)+k[1]*p[0]+k[2]*p[1]+k[3]==0) for k in det}
    det={k:v for k,v in det.items() if len(v)>=5}
    chord={}
    for i,j in choose(range(3),2):
        for a,b in choose(cols[i],2):
            for c,e in choose(cols[j],2):
                if a[1]+b[1]!=c[1]+e[1]:continue
                Y=F(a[1]+b[1],2)
                r1=F((a[1]-b[1])**2,4)
                r2=F((c[1]-e[1])**2,4)
                xi,xj=i*h,j*h
                X=(F(xj*xj-xi*xi)+r2-r1)/(2*(xj-xi))
                R=(xi-X)**2+r1
                on=frozenset(p for p in P if (p[0]-X)**2+(p[1]-Y)**2==R)
                if len(on)<5:continue
                A,B,C=-2*X,-2*Y,X*X+Y*Y-R
                L=lcm(A.denominator,B.denominator,C.denominator)
                raw=(L,int(L*A),int(L*B),int(L*C))
                g=gcd(gcd(abs(raw[0]),abs(raw[1])),gcd(abs(raw[2]),abs(raw[3])))
                chord[tuple(z//g for z in raw)]=on
    assert chord==det,(h,d,m)
    if h%d: assert not chord,(h,d,m)
    return [sum(len(v)==n for v in det.values()) for n in (5,6)]

if __name__=='__main__':
    counts=[0,0]; present=0; cases=0
    for h in range(1,6):
        for d in range(1,6):
            for m in range(3,9):
                a,b=audit(h,d,m)
                counts[0]+=a;counts[1]+=b
                present+=bool(a+b);cases+=1
    print(dict(boards=cases,with_circles=present,exactly_five=counts[0],exactly_six=counts[1]))
