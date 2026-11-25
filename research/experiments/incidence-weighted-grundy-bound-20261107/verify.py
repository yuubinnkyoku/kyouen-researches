#!/usr/bin/env python3
"""Raw all-clutter/all-safe-state audit of an incidence-packing Grundy bound."""
from collections import Counter
from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path


def clutters(n):
    by_size={k:[sum(1<<i for i in e) for e in combinations(range(n),k)] for k in range(2,n+1)}
    def walk(size,chosen):
        if size>n:
            yield tuple(chosen);return
        possible=[e for e in by_size[size] if not any(f&e==f for f in chosen)]
        for mask in range(1<<len(possible)):
            yield from walk(size+1,chosen+[e for j,e in enumerate(possible) if mask>>j&1])
    yield from walk(2,[])


def safe_values(n,edges):
    values={}
    for s in range((1<<n)-1,-1,-1):
        if any(s&e==e for e in edges):continue
        options={values[s|1<<v] for v in range(n) if not s>>v&1 and s|1<<v in values}
        g=0
        while g in options:g+=1
        values[s]=g
    return values


def residual(n,edges,s,values):
    legal=sum(1<<v for v in range(n) if not s>>v&1 and s|1<<v in values)
    candidates={e&~s for e in edges if not (e&~s)&~legal}
    minimal=tuple(sorted(e for e in candidates if not any(f!=e and f&e==f for f in candidates)))
    assert all(e.bit_count()>=2 for e in minimal)
    active=0
    for e in minimal:active|=e
    return legal,active,minimal


def main():
    root_counts={};states=0;improvements=0;local_improvements=0;hist=Counter()
    for n in range(1,6):
        count=0
        for edges in clutters(n):
            count+=1
            values=safe_values(n,edges)
            for s,g in values.items():
                legal,active,family=residual(n,edges,s,values)
                free=legal&~active
                assert s|free in values
                kernel_g=values[s|free]
                assert g==kernel_g^(free.bit_count()%2)
                if not family:
                    assert kernel_g==0 and g<=1
                    continue
                degree={v:sum(bool(e>>v&1) for e in family) for v in range(n) if active>>v&1}
                excess=sum(e.bit_count()-1 for e in family)
                delta=min(degree.values())
                uniform_k=excess//delta
                assert kernel_g<=uniform_k and g<=uniform_k|1
                # w_e = 1/min_{v in e}degree(v) is a nonuniform feasible cover.
                weights={e:Fraction(1,min(degree[v] for v in degree if e>>v&1)) for e in family}
                assert all(sum(w for e,w in weights.items() if e>>v&1)>=1 for v in degree)
                cost=sum(weights[e]*(e.bit_count()-1) for e in family)
                local_k=cost.numerator//cost.denominator
                assert kernel_g<=local_k and g<=local_k|1
                assert local_k<=uniform_k
                improvements+=(local_k|1)<legal.bit_count()
                local_improvements+=local_k<uniform_k
                states+=1;hist[(delta,local_k)]+=1
        root_counts[n]=count
    assert root_counts=={1:1,2:2,3:9,4:114,5:6894}
    output=dict(audit='PASS',all_rank_clutters_by_vertices=root_counts,
                root_clutters=sum(root_counts.values()),nontrivial_safe_states=states,
                stronger_than_legal_point_count=improvements,
                nonuniform_improves_uniform_cases=local_improvements,
                bound_certificate='w(e)=1/min degree on e; exact Fractions; isolated points removed first')
    target=Path(__file__).with_name('output')/'audit.json';target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(output,indent=2))


if __name__=='__main__':main()
