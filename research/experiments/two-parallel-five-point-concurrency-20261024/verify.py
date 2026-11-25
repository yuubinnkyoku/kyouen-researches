"""Exact polynomial-identity checker for the sharp four-circle concurrency bound.

Only the Python standard library is used. A polynomial has three variables;
after substitution, the first variable denotes alpha with alpha^2=alpha+1.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations,permutations
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent


class P:
    def __init__(self,terms=None):self.terms={e:F(c) for e,c in (terms or {}).items() if c}
    @staticmethod
    def cast(value):return value if isinstance(value,P) else P({(0,0,0):F(value)})
    def __add__(self,other):
        terms=Counter(self.terms)
        for e,c in P.cast(other).terms.items():terms[e]+=c
        return P(terms)
    __radd__=__add__
    def __neg__(self):return P({e:-c for e,c in self.terms.items()})
    def __sub__(self,other):return self+-P.cast(other)
    def __rsub__(self,other):return P.cast(other)+-self
    def __mul__(self,other):
        terms=Counter()
        for e,c in self.terms.items():
            for f,d in P.cast(other).terms.items():terms[tuple(x+y for x,y in zip(e,f))]+=c*d
        return P(terms)
    __rmul__=__mul__
    def __truediv__(self,value):return self*F(1,value)
    def __pow__(self,n):
        assert isinstance(n,int) and n>=0
        value=P.cast(1)
        for _ in range(n):value=value*self
        return value
    def __eq__(self,other):return self.terms==P.cast(other).terms
    def substitute(self,images):
        out=P()
        for e,c in self.terms.items():
            term=P.cast(c)
            for image,power in zip(images,e):term=term*image**power
            out=out+term
        return out
    def golden_reduce(self):
        terms=Counter(self.terms)
        while any(e[0]>=2 and c for e,c in terms.items()):
            e=next(e for e,c in terms.items() if e[0]>=2 and c);c=terms.pop(e)
            for decrement in (1,2):terms[e[0]-decrement,e[1],e[2]]+=c
        return P(terms)


V=P({(1,0,0):1});W=P({(0,1,0):1});Z=P({(0,0,1):1})


def det(matrix):
    n=len(matrix);out=P()
    for p in permutations(range(n)):
        term=P.cast((-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n)))
        for i,j in enumerate(p):term=term*matrix[i][j]
        out=out+term
    return out


def verify(corrupt=False):
    v,w,z=V,W,Z
    b=list(map(P.cast,(0,1,v,w,z)))
    c=[v-z+1,v+w,w+z-1,-v+z,1-w]
    rows=[];identities=0
    for i in range(5):
        s=b[i]+b[(i+1)%5];p=b[i]*b[(i+1)%5];q=c[i]*c[(i-2)%5]
        assert s==c[i]+c[(i-2)%5];identities+=1
        rows.append((s,q-p,p))
    s0,d0,p0=rows[0]
    matrix=[[s0-s,d-d0,p-p0] for s,d,p in rows[1:]]
    f2=v*v*w-v*v-v*w*w-2*v*w*z+2*v*w+2*v*z-v+w*w*z+w*z*z-2*w-2*z+2
    f4=-v*v*w+v*v+v*w*w+2*v*w*z-2*v*w-2*v*z*z+v-w*w*z-w*z*z+2*w*z+2*z**3-2*z*z
    if corrupt:f2=f2+1
    assert det([matrix[i] for i in (0,1,3)])==-v*(-v-w+z)*f2;identities+=1
    assert det([matrix[i] for i in (1,2,3)])==w*(v+w-1)*f4;identities+=1
    assert f2+f4==-2*(z-1)*(v*z-w-z*z+1);identities+=1
    alpha=V;minimal=alpha*alpha-alpha-1
    images=[z+alpha,z*alpha+1,z]
    assert f2.substitute(images)==-z*(alpha+1)*(z-1)*minimal;identities+=1
    a=(alpha+2)*(z+1)/5;u=(4-3*alpha)/5
    assert (u*(u-1)-F(1,5)).golden_reduce()==0;identities+=1
    distance=-(alpha+1)*(z*z+(alpha-1)*z+1)
    for s,d,p in rows:
        residual=distance*u*(u-1)+a*a-s.substitute(images)*a+d.substitute(images)*u+p.substitute(images)
        assert residual.golden_reduce()==0;identities+=1
    assert (z*z+(alpha-1)*z+1-(z+(alpha-1)/2)**2-(alpha+2)/4).golden_reduce()==0
    identities+=1
    # A separate exact root-isolation check, although the proof only needs
    # alpha+1=alpha^2>0 and alpha+2=alpha^2+1>0.
    values={x:x*x-x-1 for x in (-1,0,1,2)}
    assert values=={-1:1,0:-1,1:-1,2:1}
    return {'polynomial_identities':identities,'arithmetic':'Fraction multivariate polynomials',
            'golden_root_intervals':[[-1,0],[1,2]]}


def lower_witness():
    b=(-40,-32,-24,-16,0);c=(-37,-35,-27,-5,13)
    circles=[]
    for x,y in combinations(b,2):
        for z,w in combinations(c,2):
            if x+y==z+w:circles.append((x+y,z*w-x*y,x*y))
    # P=(2*sqrt(71)/5,-154/5), so multiply the circle equation by 25.
    through=[(s,d,p) for s,d,p in circles if 23290+770*s+10*d+25*p==0]
    assert len(circles)==6 and len(through)==4
    return {'B':list(b),'C':list(c),'line_distance_squared':71,
            'point':['2*sqrt(71)/5','-154/5'],'circle_catalog_size':6,
            'circles_through_point':sorted(through)}


def integer_witness():
    b=(-20,-10,0,5,20);c=(-15,-10,-5,0,10)
    circles=[]
    for x,y in combinations(b,2):
        for z,w in combinations(c,2):
            if x+y==z+w:circles.append((x+y,z*w-x*y,x*y))
    through=[(s,d,p) for s,d,p in circles if 200+6*d+20*s+5*p==0]
    assert len(circles)==9 and sorted(through)==[(-15,100,-100),(-10,0,0),(0,300,-400),(5,-50,0)]
    equations=[]
    for s,d,p in through:
        assert (d-100)%10==0
        A=(d-100)//10;B=-s;C=p
        assert 12**2+(-4)**2+A*12+B*(-4)+C==0
        assert sum(y*y+B*y+C==0 for y in b)==2
        assert sum(100+y*y+10*A+B*y+C==0 for y in c)==2
        equations.append([A,B,C])
    return {'B':list(b),'C':list(c),'line_distance':10,'point':[12,-4],
            'circle_catalog_size':9,'equations_x2_y2_Ax_By_C':sorted(equations)}


def exact_table():
    b=(-20,-10,0,5,20);c=(-15,-10,-5,0,10)
    expected=[[1,1,1,1],[1,1,2,2],[1,2,2,3],[1,2,3,4]]
    table=[];examples=[];audited=0
    for nb in range(2,6):
        row=[]
        for nc in range(2,6):
            best=-1;example=None
            for bb in combinations(b,nb):
                for cc in combinations(c,nc):
                    audited+=1;count=0
                    for x,y in combinations(bb,2):
                        for z,w in combinations(cc,2):
                            if x+y!=z+w:continue
                            s=x+y;d=z*w-x*y;p=x*y
                            count+=200+6*d+20*s+5*p==0
                    if count>best:best=count;example={'B':bb,'C':cc}
            assert best==expected[nb-2][nc-2]
            # Exact minimal shared-pair count, rather than a Cauchy approximation.
            forbidden=best+1
            def minimum(n,k):
                q,r=divmod(2*k,n)
                return (n-r)*q*(q-1)//2+r*q*(q+1)//2
            if (nb,nc)!=(5,5):
                assert minimum(nb,forbidden)+minimum(nc,forbidden)>forbidden*(forbidden-1)//2
            row.append(best);examples.append({'sizes':[nb,nc],'maximum':best,**example})
        table.append(row)
    assert audited==676
    return {'row_sizes':[2,3,4,5],'column_sizes':[2,3,4,5],'maximum_circles':table,
            'integer_subset_pairs_audited':audited,'attaining_examples':examples}


def main():
    receipt=verify()
    try:verify(True)
    except AssertionError:receipt['altered_identity_rejected']=True
    else:raise AssertionError('altered identity accepted')
    receipt['sharpness_witness']=integer_witness()
    receipt['low_energy_witness']=lower_witness()
    receipt['sharp_small_size_table']=exact_table()
    (HERE/'audit.json').write_text(json.dumps(receipt,separators=(',',':'))+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(receipt),flush=True)


if __name__=='__main__':main()
