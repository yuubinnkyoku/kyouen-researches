"""Independent standard-library checker for the 156-case polynomial certificate.

No SymPy, polynomial factorizer, numerical root finder, or floating point is used.
"""
from collections import Counter,defaultdict
import copy
from fractions import Fraction as F
from itertools import combinations,product
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
EXPECTED={
    'g1':[(0,),(1,),(1,1),(2,1),(3,1)],
    'g2':[(0,),(1,),(1,1),(2,1),(2,2)],
    'g3':[(0,),(1,1),(2,1),(2,2),(3,2)],
}


def trim(a):
    a=list(map(F,a))
    while len(a)>1 and a[-1]==0:a.pop()
    return tuple(a)


ZERO=(F(0),);ONE=(F(1),)
def add(a,b):return trim([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])
def neg(a):return tuple(-x for x in a)
def sub(a,b):return add(a,neg(b))
def mul(a,b):
    if a==ZERO or b==ZERO:return ZERO
    result=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):result[i+j]+=x*y
    return trim(result)


def remainder(a,b):
    a=list(trim(a));b=trim(b);assert b!=ZERO
    while trim(a)!=ZERO and len(trim(a))>=len(b):
        a=list(trim(a));offset=len(a)-len(b);factor=a[-1]/b[-1]
        for j,x in enumerate(b):a[offset+j]-=factor*x
    return trim(a)


class Q:
    def __init__(self,n=ZERO,d=ONE):
        self.n,self.d=trim(n),trim(d);assert self.d!=ZERO
        if self.n==ZERO:self.d=ONE
    @staticmethod
    def cast(value):return value if isinstance(value,Q) else Q((F(value),))
    def __add__(self,other):
        other=Q.cast(other);return Q(add(mul(self.n,other.d),mul(other.n,self.d)),mul(self.d,other.d))
    __radd__=__add__
    def __neg__(self):return Q(neg(self.n),self.d)
    def __sub__(self,other):return self+-Q.cast(other)
    def __rsub__(self,other):return Q.cast(other)+-self
    def __mul__(self,other):
        other=Q.cast(other);return Q(mul(self.n,other.n),mul(self.d,other.d))
    __rmul__=__mul__
    def __truediv__(self,other):
        other=Q.cast(other);assert other.n!=ZERO;return Q(mul(self.n,other.d),mul(self.d,other.n))
    def __eq__(self,other):
        other=Q.cast(other);return sub(mul(self.n,other.d),mul(other.n,self.d))==ZERO


def read_q(obj):return Q(obj['num'],obj['den'])


def factorization(poly,claim,name,allow_special=False):
    value=trim((F(claim['constant']),));assert value!=ZERO
    special=False
    for item in claim['factors']:
        p=trim(item['poly']);power=item['power'];assert isinstance(power,int) and power>0
        positive=all(c>=0 for c in p) and any(c>0 for c in p)
        excluded=(p==(F(-1),F(1)) and name in ('g1','g2'))
        exceptional=(allow_special and p==(F(-3),F(0),F(1)))
        assert positive or excluded or exceptional,(name,p)
        special|=exceptional
        for _ in range(power):value=mul(value,p)
    assert value==trim(poly),('factorization identity',name,poly)
    return special


def verify(data):
    assert data['parameter']=='t>0' and {f['name'] for f in data['families']}==set(EXPECTED)
    receipts=[]
    for family in data['families']:
        name=family['name'];raw=EXPECTED[name]
        assert [tuple(v) for v in family['points']]==raw
        assert family['excluded_t_one']==(name in ('g1','g2'))
        points=[Q(row) for row in raw];pairs=[];groups=defaultdict(list)
        for i,j in combinations(range(5),2):
            item={'ids':(i,j),'s':points[i]+points[j],'p':points[i]*points[j]}
            assert item['s'].d==ONE
            pairs.append(item);key=tuple(item['s'].n)+(F(0),)*(2-len(item['s'].n));groups[key].append(item)
        collisions=[g for key,g in sorted(groups.items()) if len(g)==2];assert len(collisions)==2
        choices=[]
        for a,b in collisions:
            choices.append([(a['s'],b['p']-a['p'],a['p']),
                            (b['s'],a['p']-b['p'],b['p'])])
        supplied={}
        for record in family['records']:
            key=(tuple(map(tuple,record['self'])),tuple(record['orientations']))
            assert key not in supplied;supplied[key]=record
        expected=set();counts=Counter()
        for left,right in combinations(pairs,2):
            if set(left['ids'])&set(right['ids']):continue
            if left['s']==right['s']:continue
            a=(left['p']-right['p'])/(left['s']-right['s'])
            f=a*a-left['s']*a+left['p']
            for i,j in product(range(2),repeat=2):
                key=((left['ids'],right['ids']),(i,j));expected.add(key);record=supplied[key]
                c,d=choices[0][i],choices[1][j]
                u=((c[0]-left['s'])*a+left['p']-c[2])/c[1]
                h=d[1]*u-((d[0]-left['s'])*a+left['p']-d[2])
                assert a==read_q(record['a']) and u==read_q(record['u']) and h==read_q(record['condition'])
                for field,label in ((record['a'],'a'),(record['u'],'u'),(record['condition'],'condition')):
                    factorization(field['den'],record[label+'_den_factors'],name)
                kind=record['type'];counts[kind]+=1
                if kind=='constant-u':
                    value=F(record['constant_u']);assert value in (0,1,F(1,2)) and h==0 and u==value
                elif kind=='negative-d2':
                    negative=trim(record['negative_d2'])
                    assert h==0 and all(x<=0 for x in negative) and any(x<0 for x in negative)
                    assert f+Q(negative)*u*(u-1)==0
                else:
                    assert kind=='nonzero-condition'
                    special=factorization(record['condition']['num'],record['num_factors'],name,True)
                    assert trim(record['condition']['num'])!=ZERO
                    if special:
                        claim=read_q(record['u']);numerator=sub(mul((F(2),),claim.n),claim.d)
                        assert remainder(numerator,(F(-3),F(0),F(1)))==ZERO
        assert set(supplied)==expected and len(expected)==52
        receipts.append({'family':name,'cases':len(expected),'classifications':dict(sorted(counts.items()))})
    return {'families':receipts,'total_cases':sum(r['cases'] for r in receipts)}


def main():
    data=json.loads((HERE/'symbolic-certificate.json').read_text(encoding='utf-8'))
    receipt=verify(data);rejected=0
    for kind in ('altered-rational-function','missing-case'):
        damaged=copy.deepcopy(data)
        if kind=='missing-case':damaged['families'][0]['records'].pop()
        else:damaged['families'][0]['records'][0]['u']['num'][0]+=1
        try:verify(damaged)
        except (AssertionError,KeyError):rejected+=1
        else:raise AssertionError('damaged certificate accepted')
    assert rejected==2;receipt['negative_controls_rejected']=rejected
    (HERE/'symbolic-audit.json').write_text(json.dumps(receipt,separators=(',',':'))+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(receipt),flush=True)


if __name__=='__main__':main()
