"""Exact integer circle geometry on an 11x11 board."""
from functools import lru_cache
from itertools import combinations

N = 11
XY = tuple((v % N, v // N) for v in range(121))
Q = tuple(x*x + y*y for x,y in XY)

def det3(a,b,c):
    return (a[0]*(b[1]*c[2]-b[2]*c[1])
           -a[1]*(b[0]*c[2]-b[2]*c[0])
           +a[2]*(b[0]*c[1]-b[1]*c[0]))

@lru_cache(maxsize=50000)
def circle_triple_mask(a,b,c):
    if not 0 <= a < b < c < 121:
        raise ValueError("invalid triple")
    x1,y1=XY[a];x2,y2=XY[b];x3,y3=XY[c]
    q1,q2,q3=Q[a],Q[b],Q[c]
    d=det3((x1,y1,1),(x2,y2,1),(x3,y3,1))
    aa=-det3((q1,y1,1),(q2,y2,1),(q3,y3,1))
    bb=det3((q1,x1,1),(q2,x2,1),(q3,x3,1))
    cc=-det3((q1,x1,y1),(q2,x2,y2),(q3,x3,y3))
    if not (d or aa or bb or cc):
        raise ValueError("degenerate triple")
    return sum(1<<v for v,(x,y) in enumerate(XY)
               if d*Q[v]+aa*x+bb*y+cc==0)

def legal_points(pts):
    pts=tuple(sorted(pts))
    if len(set(pts))!=len(pts) or any(p<0 or p>=121 for p in pts):
        raise ValueError("invalid occupied cells")
    occupied=sum(1<<p for p in pts)
    blocked=occupied
    for triple in combinations(pts,3):
        mask = circle_triple_mask(*triple)
        if mask & (occupied & ~sum(1 << p for p in triple)):
            raise ValueError("unsafe occupied position")
        blocked |= mask
    return [p for p in range(121) if not (blocked>>p)&1]

def canonical_key(points):
    from dfpn_edge_classes import d4_canonical_key
    return tuple(d4_canonical_key(points))
