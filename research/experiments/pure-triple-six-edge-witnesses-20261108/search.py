#!/usr/bin/env python3
"""Targeted witness search; no exhaustive six-edge upper-bound claim."""
from functools import lru_cache
from itertools import combinations
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parents[3]


def mex(options):
    g=0
    while g in options:g+=1
    return g


def direct(n,edges):
    @lru_cache(None)
    def g(s):
        return mex({g(s|1<<v) for v in range(n) if not s>>v&1 and all((s|1<<v)&e!=e for e in edges)})
    return g(0),[g(1<<v) for v in range(n)]


def main():
    directory=Path(__file__).resolve().parent
    prior=json.loads((ROOT/'research/experiments/pure-triple-few-edge-grundy-20261107/output/audit.json').read_text())
    bases=[r for r in prior['records'] if r['h']==5 and r['grundy']>=4]
    cases=[]
    for base in bases:
        n=base['n']
        for overlap in (1,2,3):
            for selected in combinations(range(n),overlap):
                extra=sum(1<<v for v in selected)+sum(1<<(n+j) for j in range(3-overlap))
                if extra in base['edges']:continue
                cases.append((n+3-overlap,tuple(base['edges'])+(extra,)))
    cases=sorted(set(cases))
    compiler=shutil.which('g++')
    if compiler is None:raise SystemExit('g++ is required')
    with tempfile.TemporaryDirectory(prefix='kyouen-pure3-six-edge-') as scratch:
        temp=Path(scratch).resolve();assert temp.parent==Path(tempfile.gettempdir()).resolve()
        data=temp/'cases.txt';executable=temp/'native.exe';result=temp/'values.bin'
        data.write_text(str(len(cases))+'\n'+'\n'.join(' '.join(map(str,[n,6,*edges])) for n,edges in cases)+'\n',encoding='ascii')
        cpp=ROOT/'research/experiments/pure-triple-few-edge-grundy-20261107/independent.cpp'
        subprocess.run([compiler,'-std=c++17','-O2',str(cpp),'-o',str(executable)],check=True)
        report=json.loads(subprocess.check_output([str(executable),str(data),str(result)],text=True))
        values=result.read_bytes();assert len(values)==len(cases)
    maximum=max(values);witnesses=[]
    for value in sorted(set(values)):
        if value<6:continue
        index=next(i for i,g in enumerate(values) if g==value)
        n,edges=cases[index]
        actual,children=direct(n,edges);assert actual==value
        witnesses.append(dict(n=n,edges=edges,grundy=value,child_grundy=children))
    output=dict(scope='one-edge extensions of all five-edge core types with g>=4; not all six-edge families',
                cases=len(cases),cpp_safe_states=report['safe_states'],maximum_found=maximum,
                value_histogram={g:values.count(g) for g in sorted(set(values))},witnesses=witnesses)
    target=directory/'output/search.json';target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(output,indent=2))


if __name__=='__main__':main()
