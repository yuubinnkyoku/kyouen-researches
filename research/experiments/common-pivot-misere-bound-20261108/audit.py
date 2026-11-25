#!/usr/bin/env python3
"""Misere auxiliary mex (terminal=1), with no xor assumption for free points."""
from collections import Counter
from functools import lru_cache
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parents[3]
SPEC=importlib.util.spec_from_file_location('normal_common',ROOT/
    'research/experiments/common-pivot-residual-game-20261108/audit.py')
# Its local probe import must be available without importing unrelated packages.
import sys
sys.path.insert(0,str(ROOT/'research/experiments/common-pivot-residual-game-20261108'))
NORMAL=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(NORMAL)


def mex(options):
    result=0
    while result in options:result+=1
    return result


def graph_misere(m,pairs):
    adjacency=[1<<v for v in range(m)]+[1<<m]
    for a,b in pairs:adjacency[a]|=1<<b;adjacency[b]|=1<<a
    @lru_cache(None)
    def h(remaining):
        options={h(remaining&~adjacency[v]) for v in range(m+1) if remaining>>v&1}
        return mex(options) if options else 1
    @lru_cache(None)
    def t(remaining):
        if h(remaining)>=2:return None
        return mex({t(remaining&~adjacency[v]) for v in range(m+1)
                    if remaining>>v&1 and h(remaining&~adjacency[v])<2})
    full=(1<<m)-1
    return h(full),h(full|1<<m),[h(full&~adjacency[v]) for v in range(m)],\
           [h((full&~adjacency[v])|1<<m) for v in range(m)],\
           t(full),t(full|1<<m),[t(full&~adjacency[v]) for v in range(m)],\
           [t((full&~adjacency[v])|1<<m) for v in range(m)]


def f(parity,a,t):
    if parity==0:return 2+t if a==1 else 1
    return 2+t if a==0 else 0


def formula(m,poison,pairs):
    if poison:
        vertices=[v for v in range(m) if not poison>>v&1];index={v:i for i,v in enumerate(vertices)}
        a,_,_,_,t,*_=graph_misere(len(vertices),[(index[u],index[v]) for u,v in pairs])
        return f(m%2,a,t)
    active=sorted({v for pair in pairs for v in pair});free=m-len(active)
    if not active:return m%2
    index={v:i for i,v in enumerate(active)}
    a,b,children_a,children_b,t,u,children_t,children_u=graph_misere(len(active),[(index[u],index[v]) for u,v in pairs])
    assert a!=b and all(x!=y for x,y in zip(children_a,children_b))
    parity=len(active)%2
    q0=mex({a,*[f(1-parity,x,y) for x,y in zip(children_a,children_t)]})
    q1=mex({b,q0,*[f(parity,x,y) for x,y in zip(children_b,children_u)]})
    return q1 if free%2 else q0


def main():
    directory=Path(__file__).resolve().parent
    records=[];histogram=Counter();summaries=[]
    for m in range(7):
        local=Counter()
        for poison in range(1<<m):
            vertices=[v for v in range(m) if not poison>>v&1]
            candidates=list(combinations(vertices,2))
            for mask in range(1<<len(candidates)):
                pairs=[e for i,e in enumerate(candidates) if mask>>i&1]
                edges=tuple([1|(1<<(v+1)) for v in range(m) if poison>>v&1]+
                            [1|(1<<(u+1))|(1<<(v+1)) for u,v in pairs])
                g=NORMAL.formula(m,poison,pairs);h=formula(m,poison,pairs)
                records.append((m+1,edges,g,h));histogram[g,h]+=1;local[g,h]+=1
        summaries.append(dict(outside_points=m,cases=sum(local.values()),
                              normal_misere_histogram={str(g)+','+str(h):c for (g,h),c in sorted(local.items())}))
    core=[(0,1),(1,2),(3,4),(4,5)]
    selector=core+[(6,7)]+[(7,v) for v in range(6) if v not in (0,1)]
    cone=core+[(8,v) for v in range(8)]
    special=[]
    for name,m,poison,pairs in [('mixed_four',10,(1<<8)|(1<<9),selector),
                               ('mixed_five',11,(1<<8)|(1<<9),selector),
                               ('pure_four',9,0,cone),('pure_five',10,0,cone)]:
        edges=tuple([1|(1<<(v+1)) for v in range(m) if poison>>v&1]+
                    [1|(1<<(u+1))|(1<<(v+1)) for u,v in pairs])
        g=NORMAL.formula(m,poison,pairs);h=formula(m,poison,pairs)
        assert h==(5 if 'five' in name else 4)
        records.append((m+1,edges,g,h));histogram[g,h]+=1
        special.append(dict(name=name,n=m+1,edges=edges,normal=g,misere_aux=h))
    compiler=shutil.which('g++')
    if compiler is None:raise SystemExit('g++ is required')
    with tempfile.TemporaryDirectory(prefix='kyouen-pivot-misere-') as scratch:
        temp=Path(scratch).resolve();assert temp.parent==Path(tempfile.gettempdir()).resolve()
        data=temp/'cases.txt';exe=temp/'verify.exe';result=temp/'values.bin';meta=temp/'meta.json'
        data.write_text(str(len(records))+'\n'+'\n'.join(' '.join(map(str,[n,len(edges),*edges])) for n,edges,g,h in records)+'\n',encoding='ascii')
        subprocess.run([compiler,'-std=c++17','-O2',str(directory/'independent.cpp'),'-o',str(exe)],check=True)
        subprocess.run([str(exe),str(data),str(result),str(meta)],check=True)
        actual=result.read_bytes()
        expected=bytes(x for n,edges,g,h in records for x in (g,h))
        if actual!=expected:
            differences=[dict(n=n,edges=edges,expected_normal=g,expected_misere=h,
                              actual_normal=actual[2*i],actual_misere=actual[2*i+1])
                         for i,(n,edges,g,h) in enumerate(records)
                         if actual[2*i:2*i+2]!=expected[2*i:2*i+2]]
            native_hist=Counter(actual[1::2]);maximum=max(native_hist)
            best=next(i for i in range(len(records)) if actual[2*i+1]==maximum)
            failure=dict(status='FAILED_FORMULA',differences=len(differences),first_differences=differences[:10],
                         native_misere_histogram=dict(sorted(native_hist.items())),
                         native_maximum_witness=dict(n=records[best][0],edges=records[best][1],
                             normal=actual[2*best],misere=maximum))
            target=directory/'output/failed_formula.json';target.parent.mkdir(exist_ok=True)
            target.write_text(json.dumps(failure,indent=2)+'\n',encoding='utf-8')
            print(json.dumps(failure,indent=2),flush=True)
            raise AssertionError('formula disagrees with independent C++')
        native=json.loads(meta.read_text())
    exceptions=[]
    for g,h in sorted(histogram):
        if (g,h) not in ((0,1),(1,0)) and not (g>=2 and g==h):
            n,edges,_,_=next(r for r in records if r[2:]==(g,h))
            exceptions.append(dict(n=n,edges=edges,normal=g,misere_aux=h))
    seven_types=Counter();seven_representatives={}
    for n,edges,g,h in records[:41658]:
        swapped=(1 if g==0 else 0 if g==1 else g)
        if h==swapped:continue
        assert n==7 and (g,h)==(2,1) and all(e.bit_count()==3 for e in edges)
        adjacency=[set() for _ in range(6)]
        for edge in edges:
            u,v=[v for v in range(6) if (edge>>1)>>v&1]
            adjacency[u].add(v);adjacency[v].add(u)
        components=[];pending=set(range(6))
        while pending:
            reached={next(iter(pending))}
            while True:
                enlarged=reached|set().union(*(adjacency[v] for v in reached))
                if enlarged==reached:break
                reached=enlarged
            components.append(len(reached));pending-=reached
        degrees=sorted(map(len,adjacency))
        if sorted(components)==[6] and degrees==[2]*6:kind='C6'
        else:
            assert sorted(components)==[3,3] and degrees==[1,1,1,1,2,2]
            kind='P3+P3'
        seven_types[kind]+=1;seven_representatives.setdefault(kind,edges)
    assert seven_types==Counter({'C6':60,'P3+P3':90})
    output=dict(audit='PASS',terminal_misere_aux=1,summaries=summaries,
                cases_compared=len(records),cpp_safe_states=native['safe_states'],
                maximum_misere_aux=max(h for g,h in histogram),
                normal_misere_histogram={str(g)+','+str(h):c for (g,h),c in sorted(histogram.items())},
                exceptions_to_normal_misere_exchange=exceptions,
                seven_point_exchange_exception_types=dict(seven_types),
                seven_point_exchange_exception_representatives=seven_representatives,
                special_witnesses=special,
                limitation='misere auxiliary mex is not an additive Sprague-Grundy invariant')
    target=directory/'output/audit.json';target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in output.items() if k!='summaries'},indent=2),flush=True)


if __name__=='__main__':main()
