#!/usr/bin/env python3
"""Universal mobility gap for misere mex: residual recursion vs raw native DP."""
from collections import Counter
from functools import lru_cache
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parents[3]
SPEC=importlib.util.spec_from_file_location('all_rank',ROOT/
    'research/experiments/incidence-weighted-grundy-bound-20261107/verify.py')
GEN=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(GEN)


@lru_cache(None)
def residual_misere(n,edges):
    if n==0:return 1
    options=set()
    for v in range(n):
        reduced=[e&~(1<<v) for e in edges]
        blocked=0
        for edge in reduced:
            if edge.bit_count()==1:blocked|=edge
        remaining=[u for u in range(n) if u!=v and not blocked>>u&1]
        active=sum(1<<u for u in remaining)
        candidates={sum(1<<j for j,u in enumerate(remaining) if e>>u&1)
                    for e in reduced if not e&~active}
        minimal=tuple(sorted(e for e in candidates if not any(f!=e and f&e==f for f in candidates)))
        assert all(e.bit_count()>=2 for e in minimal)
        options.add(residual_misere(len(remaining),minimal))
    result=0
    while result in options:result+=1
    return result


def main():
    directory=Path(__file__).resolve().parent;records=[];summaries=[]
    for n in range(6):
        normal=Counter();misere=Counter()
        for edges in GEN.clutters(n):
            edges=tuple(sorted(edges));g=GEN.safe_values(n,edges)[0];h=residual_misere(n,edges)
            normal[g]+=1;misere[h]+=1;records.append((n,edges,g,h))
        summaries.append(dict(legal_points=n,clutters=sum(normal.values()),normal_histogram=dict(sorted(normal.items())),
                              misere_histogram=dict(sorted(misere.items()))))
    assert [max(s['misere_histogram']) for s in summaries]==[1,0,1,2,3,3]
    six=json.loads((ROOT/'research/experiments/pure-triple-maximum-grundy-six-20261107/output/independent_audit.json').read_text())
    four=tuple(sum(1<<v for v in edge) for edge in six['maximum_four_orbits'][0]['triples'])
    higher=(22,38,41,49,88,146)
    general={0:(1,()),1:(0,()),2:(3,(3,6)),3:(4,(3,6)),4:(6,four),5:(7,four),6:(8,higher),7:(9,higher)}
    pure=dict(general);pure[2]=(6,(19,21,38,56));pure[3]=(7,(19,21,38,56))
    witness_sets={}
    for name,examples in [('arbitrary_rank',general),('pure_triple',pure)]:
        witness_sets[name]=[]
        for target,(n,edges) in examples.items():
            h=residual_misere(n,tuple(sorted(edges)));g=GEN.safe_values(n,edges)[0]
            assert h==target
            records.append((n,tuple(edges),g,h))
            witness_sets[name].append(dict(n=n,edges=edges,normal=g,misere_aux=h))
    compiler=shutil.which('g++')
    if compiler is None:raise SystemExit('g++ is required')
    cpp=ROOT/'research/experiments/common-pivot-misere-bound-20261108/independent.cpp'
    with tempfile.TemporaryDirectory(prefix='kyouen-misere-gap-') as scratch:
        temp=Path(scratch).resolve();assert temp.parent==Path(tempfile.gettempdir()).resolve()
        data=temp/'cases.txt';exe=temp/'verify.exe';values=temp/'values.bin';meta=temp/'meta.json'
        data.write_text(str(len(records))+'\n'+'\n'.join(' '.join(map(str,[n,len(edges),*edges])) for n,edges,g,h in records)+'\n',encoding='ascii')
        subprocess.run([compiler,'-std=c++17','-O2',str(cpp),'-o',str(exe)],check=True)
        subprocess.run([str(exe),str(data),str(values),str(meta)],check=True)
        assert values.read_bytes()==bytes(x for n,edges,g,h in records for x in (g,h))
        native=json.loads(meta.read_text())
    output=dict(audit='PASS',rank_free_bases=summaries,cases_compared=len(records),cpp_safe_states=native['safe_states'],
                universal_theorem='legal_points>=5 implies both g and misere_aux h <= legal_points-2',
                arbitrary_rank_minimum_points_h_zero_through_seven=[1,0,3,4,6,7,8,9],
                pure_triple_minimum_points_h_zero_through_seven=[1,0,6,7,6,7,8,9],witnesses=witness_sets)
    target=directory/'output/audit.json';target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in output.items() if k not in ('rank_free_bases','witnesses')},indent=2),flush=True)


if __name__=='__main__':main()
