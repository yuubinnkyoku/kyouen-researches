from functools import lru_cache
from itertools import combinations
N=11
X=[i%11 for i in range(121)];Y=[i//11 for i in range(121)];R=[X[i]**2+Y[i]**2 for i in range(121)]
T=[[11*yy+xx for i in range(121) for x,y in [(X[i],Y[i])] for xx,yy in [((x,y),(10-y,x),(10-x,10-y),(y,10-x),(10-x,y),(10-y,10-x),(x,10-y),(y,x))[t]]] for t in range(8)]

def points(m):
 while m:
  l=m&-m;p=l.bit_length()-1
  yield p
  m^=l

@lru_cache(maxsize=1000000)
def canonical(m):
 ps=list(points(m));v=m
 for t in T[1:]:
  z=0
  for p in ps:z|=1<<t[p]
  if z<v:v=z
 return v

@lru_cache(maxsize=500000)
def forbidden(a,b,c):
 # det[(x,y,r,1) rows a,b,c,d] == 0 => A*r_d+B*x_d+C*y_d+D
 # derive using a as base: (xb-xa,yb-ya,rb-ra) and (xc-xa,...)
 ux=X[b]-X[a];uy=Y[b]-Y[a];ur=R[b]-R[a]
 vx=X[c]-X[a];vy=Y[c]-Y[a];vr=R[c]-R[a]
 # cross product = (uy*vr-ur*vy, ur*vx-ux*vr, ux*vy-uy*vx)
 A=ux*vy-uy*vx
 B=uy*vr-ur*vy
 C=ur*vx-ux*vr
 D=-(A*R[a]+B*X[a]+C*Y[a])
 mask=0
 for d in range(121):
  if A*R[d]+B*X[d]+C*Y[d]+D==0:mask|=1<<d
 return mask

def legal(m):
 ps=list(points(m));ban=m
 for a,b,c in combinations(ps,3):ban|=forbidden(a,b,c)
 return [i for i in range(121) if not (ban>>i&1)]

def children(m):return {canonical(m|(1<<p)) for p in legal(m)}
