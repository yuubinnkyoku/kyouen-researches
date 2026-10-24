"""Generate an exact certificate for all three E=14 equal-set families.

Reproduce with: uv run --no-project --with sympy==1.14.0 python symbolic.py
The checked certificate can be verified without SymPy by check_symbolic.py.
"""
from collections import defaultdict
from itertools import combinations,product
import json
from math import lcm
from pathlib import Path
import sympy as S

HERE=Path(__file__).resolve().parent
t=S.Symbol('t',positive=True)
FAMILIES={
    'g1':[(0,),(1,),(1,1),(2,1),(3,1)],
    'g2':[(0,),(1,),(1,1),(2,1),(2,2)],
    'g3':[(0,),(1,1),(2,1),(2,2),(3,2)],
}


def coefficients(expr):
    p=S.Poly(expr,t,domain=S.QQ)
    return [p.nth(i) for i in range(max(0,p.degree())+1)] if not p.is_zero else [S.Integer(0)]


def rational(expr):
    n,d=S.together(S.cancel(expr)).as_numer_denom()
    a,b=coefficients(n),coefficients(d)
    multiplier=lcm(*(int(x.q) for x in a+b))
    return {'num':[int(x*multiplier) for x in a],
            'den':[int(x*multiplier) for x in b]}


def factor(coeffs):
    expr=sum(S.Integer(x)*t**i for i,x in enumerate(coeffs))
    constant,factors=S.factor_list(expr,t)
    return {'constant':str(constant),
            'factors':[{'poly':[int(x) for x in coefficients(p)],'power':int(power)} for p,power in factors]}


def make_family(name,raw):
    points=[sum(S.Integer(c)*t**i for i,c in enumerate(row)) for row in raw]
    pairs=[];groups=defaultdict(list)
    for i,j in combinations(range(5),2):
        chord={'ids':[i,j],'s':S.expand(points[i]+points[j]),'p':S.expand(points[i]*points[j])}
        pairs.append(chord);groups[tuple(int(chord['s'].coeff(t,k)) for k in range(2))].append(chord)
    collisions=[group for key,group in sorted(groups.items()) if len(group)==2]
    assert len(collisions)==2
    options=[]
    for a,b in collisions:
        options.append([(a['s'],b['p']-a['p'],a['p']),
                        (b['s'],a['p']-b['p'],b['p'])])
    records=[]
    for left,right in combinations(pairs,2):
        if set(left['ids'])&set(right['ids']):continue
        if S.expand(left['s']-right['s'])==0:continue
        y=S.cancel((left['p']-right['p'])/(left['s']-right['s']))
        f=S.cancel(y*y-left['s']*y+left['p'])
        for i,j in product(range(2),repeat=2):
            c,d=options[0][i],options[1][j]
            u=S.cancel(((c[0]-left['s'])*y+left['p']-c[2])/c[1])
            condition=S.cancel(d[1]*u-((d[0]-left['s'])*y+left['p']-d[2]))
            a_rep,u_rep,h_rep=rational(y),rational(u),rational(condition)
            row={'self':[left['ids'],right['ids']],'orientations':[i,j],
                 'a':a_rep,'u':u_rep,'condition':h_rep,
                 'a_den_factors':factor(a_rep['den']),
                 'u_den_factors':factor(u_rep['den']),
                 'condition_den_factors':factor(h_rep['den'])}
            if condition==0:
                if u in (0,1,S.Rational(1,2)):
                    row['type']='constant-u';row['constant_u']=str(u)
                else:
                    value=S.cancel(-f/(u*(u-1)))
                    p=S.Poly(value,t,domain=S.QQ)
                    assert all(c<=0 for c in p.all_coeffs()) and not p.is_zero
                    row['type']='negative-d2';row['negative_d2']=[str(c) for c in coefficients(value)]
            else:
                row['type']='nonzero-condition';row['num_factors']=factor(h_rep['num'])
            records.append(row)
    assert len(records)==52
    return {'name':name,'points':raw,'excluded_t_one':name in ('g1','g2'),'records':records}


def main():
    result={'parameter':'t>0','families':[make_family(name,raw) for name,raw in FAMILIES.items()]}
    path=HERE/'symbolic-certificate.json'
    path.write_text(json.dumps(result,separators=(',',':'))+'\n',encoding='utf-8',newline='\n')
    print('Generated 156 exact symbolic cases:',path,flush=True)


if __name__=='__main__':main()
