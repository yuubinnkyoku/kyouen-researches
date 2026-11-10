"""Independent interpretation of exact-five input plus its exhaustive complete-pair split."""
import importlib.util
from pathlib import Path

HERE=Path(__file__).resolve().parent
COUNTER_SOURCE=HERE.parent/'parabola-p2539-exchange-audit-20261110/schema.py'
spec=importlib.util.spec_from_file_location('exact_loss_prefix',COUNTER_SOURCE)
prefix=importlib.util.module_from_spec(spec);spec.loader.exec_module(prefix)
P,H,SEED_SHA=2539,1269,prefix.SEED_SHA
CASES={'retained':(1,1),'changed':(1,1)}


def size(n,k):
    assert 1<=k<n-1
    m=n-k;return 2*m*k+m-k,m*k


def audit(raw,seed,case):
    assert case in CASES;x,c=CASES[case]
    assert seed==sorted(set(seed)) and len(seed)==1258 and {0,6,2533}<=set(seed)
    nv,clauses=prefix.parse(raw);both=[4*i-3 for i in range(1,H+1)];none=[4*i-2 for i in range(1,H+1)]
    expected=[]
    for i in range(1,H+1):
        b,n,l,h=4*i-3,4*i-2,4*i-1,4*i
        expected.extend([[b,n,l,h],[-b,-n],[-b,-l],[-b,-h],[-n,-l],[-n,-h],[-l,-h]])
    assert clauses[:len(expected)]==expected;at,top,counters=len(expected),4*H,[]
    def consume(inputs,k,name):
        nonlocal at,top
        nc,na=size(len(inputs),k);_,rules=prefix.counter(clauses[at:at+nc],inputs,k,top,top+na)
        counters.append(dict(name=name,clauses=nc,bound=k,inputs=len(inputs),domain=[top+1,top+na],rules=rules));at+=nc;top+=na
    if c:
        assert clauses[at]==both;at+=1;consume(both,1,'BOTH-upper-one')
    else:
        assert clauses[at:at+H]==[[-v] for v in both];at+=H
    e=H+x+c-1259;consume([-v for v in none],H-e,'NONE-lower');consume(none,e,'NONE-upper')
    base,point_start=top,at
    for t in range(1,P):
        i=t if t<=H else P-t;b,side,a=4*i-3,4*i-1 if t<=H else 4*i,base+t
        assert clauses[at:at+3]==[[-a,side,b],[a,-side],[a,-b]];at+=3
    point_end,geometry_start=base+P-1,at;edges=[]
    while at<len(clauses):
        clause=clauses[at]
        if not (len(clause) in ((3,4) if x else (4,)) and all(-point_end<=v<-base for v in clause)):break
        q=sorted(-v-base for v in clause)
        if len(q)==3:q=[0]+q
        assert len(set(q))==4 and sum(q)%P==0;edges.append(tuple(q));at+=1
    loss_start=at;top=point_end
    inputs=[-(base+t) for t in seed if t];k=5-(1-x)
    consume([-v for v in inputs],len(inputs)-k,'nonzero-loss-lower')
    consume(inputs,k,'nonzero-loss-upper')
    assert at==len(clauses)-1 and top==nv and edges
    assert clauses[-1]==[21 if case=='retained' else -21]
    return edges,dict(case=case,p=P,origin=x,complete_pairs=c,target_size=1259,removed_exactly=5,split_unit=21 if case=='retained' else -21,
        origin_deletion_cost=1-x,nonzero_removed_exactly=k,variables=nv,clauses=len(clauses),onehot_clauses=len(expected),
        point_base=base,point_definition_clauses=geometry_start-point_start,geometric_clauses=loss_start-geometry_start,
        deletion_clauses=at-loss_start,counters=counters,
        scope='Every safe exact1259 set in this class losing exactly5 seed points, with B6 iff retained, extends to all recognized clauses. Actual geometric quadruples require independent determinant checks.')
