#!/usr/bin/env python3
"""All <=6-edge pure-triple cores: exact normal and misere values, free parity 0/1."""
from collections import Counter
from functools import lru_cache
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parents[3]


def cell_values(signature,free):
    h=(len(signature)+1).bit_length()-1
    cells=[(mask,count) for mask,count in enumerate(signature,1) if count]
    if free:cells.append((0,free))
    def mex(values):
        answer=0
        while answer in values:answer+=1
        return answer
    @lru_cache(None)
    def game(chosen):
        usage=[sum(chosen[i] for i,(mask,count) in enumerate(cells) if mask>>e&1) for e in range(h)]
        options=[]
        for i,(mask,count) in enumerate(cells):
            if chosen[i]==count or any(usage[e]==2 for e in range(h) if mask>>e&1):continue
            child=list(chosen);child[i]+=1;options.append(game(tuple(child)))
        return mex({g for g,aux in options}),mex({aux for g,aux in options}) if options else 1
    return game((0,)*len(cells))


def main():
    directory=Path(__file__).resolve().parent
    old=json.loads((ROOT/'research/experiments/pure-triple-few-edge-grundy-20261107/output/audit.json').read_text())['records']
    six=json.loads((directory/'output/audit.json').read_text())['records']
    inputs=[dict(h=r['h'],**{k:r[k] for k in ('n','edges','signature')}) for r in old]
    inputs.extend(dict(h=6,**{k:r[k] for k in ('n','edges','signature')}) for r in six)
    records=[];summaries=[]
    for h in range(1,7):
        histogram=Counter()
        for row in inputs:
            if row['h']!=h:continue
            for free in (0,1):
                g,aux=cell_values(tuple(row['signature']),free)
                records.append(dict(n=row['n']+free,edges=row['edges'],normal=g,misere_aux=aux,edge_count=h,free_parity=free))
                histogram[g,aux]+=1
        summaries.append(dict(edges=h,cases=sum(histogram.values()),maximum_normal=max(g for g,aux in histogram),
                              maximum_misere=max(aux for g,aux in histogram),
                              pair_histogram={str(g)+','+str(aux):count for (g,aux),count in sorted(histogram.items())}))
        print(summaries[-1],flush=True)
    compiler=shutil.which('g++')
    if compiler is None:raise SystemExit('g++ is required')
    cpp=ROOT/'research/experiments/common-pivot-misere-bound-20261108/independent.cpp'
    with tempfile.TemporaryDirectory(prefix='kyouen-six-edge-misere-') as scratch:
        temp=Path(scratch).resolve();assert temp.parent==Path(tempfile.gettempdir()).resolve()
        data=temp/'cases.txt';exe=temp/'verify.exe';values=temp/'values.bin';meta=temp/'meta.json'
        data.write_text(str(len(records))+'\n'+'\n'.join(' '.join(map(str,[r['n'],len(r['edges']),*r['edges']])) for r in records)+'\n',encoding='ascii')
        subprocess.run([compiler,'-std=c++17','-O3',str(cpp),'-o',str(exe)],check=True)
        subprocess.run([str(exe),str(data),str(values),str(meta)],check=True)
        assert values.read_bytes()==bytes(x for r in records for x in (r['normal'],r['misere_aux']))
        native=json.loads(meta.read_text())
    witnesses=[]
    for h in range(1,7):
        maximum=summaries[h-1]['maximum_misere']
        witnesses.append(next(r for r in records if r['edge_count']==h and r['misere_aux']==maximum))
    output=dict(audit='PASS',scope='all <=6-edge pure-triple cores and 0/1 free points; arbitrary free counts by period two',
                kernel_types=len(inputs),cases_compared=len(records),cpp_safe_states=native['safe_states'],
                summaries=summaries,misere_maximum_witnesses=witnesses)
    (directory/'output/misere.json').write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in output.items() if k not in ('summaries','misere_maximum_witnesses')},indent=2),flush=True)


if __name__=='__main__':main()
