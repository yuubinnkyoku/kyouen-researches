#!/usr/bin/env python3
"""Exact common-pivot rank-three formula vs independent raw subset games."""
from collections import Counter
from functools import lru_cache
import hashlib
from itertools import combinations
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
from probe import value


def graph_values(m,edges):
    adjacency=[1<<v for v in range(m)]
    for a,b in edges:adjacency[a]|=1<<b;adjacency[b]|=1<<a
    @lru_cache(None)
    def g(remaining):
        options={g(remaining&~adjacency[v]) for v in range(m) if remaining>>v&1}
        result=0
        while result in options:result+=1
        return result
    full=(1<<m)-1
    return g(full),[g(full&~adjacency[v]) for v in range(m)]


def formula(m,poison,pairs):
    if poison:
        vertices=[v for v in range(m) if not poison>>v&1]
        index={v:i for i,v in enumerate(vertices)}
        g,_=graph_values(len(vertices),[(index[a],index[b]) for a,b in pairs])
        return (2 if g==0 else 0) if m%2==0 else (3 if g==1 else 1)
    active=sorted(set(v for pair in pairs for v in pair))
    free=m-len(active)
    if not active:return (m+1)%2
    index={v:i for i,v in enumerate(active)}
    g,children=graph_values(len(active),[(index[a],index[b]) for a,b in pairs])
    parity=(len(active)-1)%2
    options={g}
    options.update((2 if child==0 else 0) if parity==0 else
                   (3 if child==1 else 1) for child in children)
    result=0
    while result in options:result+=1
    return result^(free%2)


def main():
    directory=Path(__file__).resolve().parent;root=directory.parents[2]
    records=[];summaries=[];digest=hashlib.sha256()
    for m in range(7):
        histogram=Counter()
        for poison in range(1<<m):
            vertices=[v for v in range(m) if not poison>>v&1]
            possible=list(combinations(vertices,2))
            for mask in range(1<<len(possible)):
                pairs=[pair for i,pair in enumerate(possible) if mask>>i&1]
                edges=tuple([1|(1<<(v+1)) for v in range(m) if poison>>v&1]+
                            [1|(1<<(a+1))|(1<<(b+1)) for a,b in pairs])
                g=formula(m,poison,pairs)
                assert g<=3
                assert g<2 or g==(3^((m+1)%2))
                records.append((m+1,edges,g));histogram[g]+=1
                digest.update((' '.join(map(str,[m+1,len(edges),*edges,g]))+'\n').encode('ascii'))
        summaries.append(dict(outside_points=m,cases=sum(histogram.values()),histogram=dict(sorted(histogram.items()))))
    # All-rank rank-four counterexample: all six edges share vertex 0.
    four_edges=(75,83,101,43,105,51)
    assert value(7,four_edges)==4
    assert 75&83==67 and 75|83==91 and 27&91==27 and 27 not in four_edges
    records.append((7,four_edges,4))
    pure=(7,13,49,97)
    assert value(7,pure)==2 and value(8,pure)==3
    assert value(4,(3,13))==3
    records.extend(((7,pure,2),(8,pure,3),(4,(3,13),3)))
    compiler=shutil.which('g++')
    if compiler is None:raise SystemExit('g++ is required')
    cpp=root/'research/experiments/pure-triple-few-edge-grundy-20261107/independent.cpp'
    with tempfile.TemporaryDirectory(prefix='kyouen-common-pivot-') as scratch:
        temp=Path(scratch).resolve();assert temp.parent==Path(tempfile.gettempdir()).resolve()
        data=temp/'cases.txt';exe=temp/'verify.exe';result=temp/'values.bin'
        data.write_text(str(len(records))+'\n'+'\n'.join(' '.join(map(str,[n,len(edges),*edges])) for n,edges,g in records)+'\n',encoding='ascii')
        subprocess.run([compiler,'-std=c++17','-O2',str(cpp),'-o',str(exe)],check=True)
        native=json.loads(subprocess.check_output([str(exe),str(data),str(result)],text=True))
        assert result.read_bytes()==bytes(g for n,edges,g in records)
    output=dict(audit='PASS',rank_three_summaries=summaries,rank_three_cases=len(records)-4,
                all_case_rows_sha256=digest.hexdigest(),cpp_safe_states=native['safe_states'],
                cpp_roots_compared=len(records),sharp_mixed=dict(n=4,edges=[3,13],grundy=3),
                pure_triple_examples=[dict(n=7,edges=pure,grundy=2),dict(n=8,edges=pure,grundy=3)],
                rank_four_counterexample=dict(n=7,edges=four_edges,grundy=4,
                    geometry_obstruction=dict(shared_triple=67,forced_five_points=91,missing_quad=27),
                    limitation='abstract clutter only; exact q4 realization impossible by shared-triple closure'))
    (directory/'output/audit.json').write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(output,indent=2),flush=True)


if __name__=='__main__':main()
