#!/usr/bin/env python3
"""All edge subfamilies of two fixed witnesses; no global edge-minimum claim."""
from collections import Counter
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
from verify import ROOT,NORMAL


def main():
    directory=Path(__file__).resolve().parent
    optimal=json.loads((directory/'output/audit.json').read_text())['records'][0]
    other=json.loads((ROOT/'research/experiments/rank-three-cover-two-grundy-20261108/output/audit.json').read_text())['records'][1]
    cases=[];ranges=[]
    for row in (optimal,other):
        begin=len(cases);edges=row['edges'];n=row['n']
        for mask in range(1<<len(edges)):
            cases.append((n,tuple(e for j,e in enumerate(edges) if mask>>j&1)))
        ranges.append((n,begin,len(cases)))
    compiler=shutil.which('g++')
    if compiler is None:raise SystemExit('g++ is required')
    cpp=ROOT/'research/experiments/pure-triple-few-edge-grundy-20261107/independent.cpp'
    with tempfile.TemporaryDirectory(prefix='kyouen-eight-pruning-') as scratch:
        temp=Path(scratch).resolve();assert temp.parent==Path(tempfile.gettempdir()).resolve()
        data=temp/'cases.txt';exe=temp/'scan.exe';values=temp/'values.bin'
        data.write_text(str(len(cases))+'\n'+'\n'.join(' '.join(map(str,[n,len(edges),*edges])) for n,edges in cases)+'\n',encoding='ascii')
        subprocess.run([compiler,'-std=c++17','-O3',str(cpp),'-o',str(exe)],check=True)
        native=json.loads(subprocess.check_output([str(exe),str(data),str(values)],text=True))
        result=values.read_bytes();assert len(result)==len(cases)
    best={};summaries=[]
    for n,begin,end in ranges:
        summaries.append(dict(n=n,subfamilies=end-begin,histogram=dict(sorted(Counter(result[begin:end]).items()))))
    for (n,edges),value in zip(cases,result):
        if value<8:continue
        active=0
        for edge in edges:active|=edge
        free=n-active.bit_count();order=[v for v in range(n) if active>>v&1]
        reduced=tuple(sorted(sum(1<<j for j,v in enumerate(order) if edge>>v&1) for edge in edges))
        reduced_n=len(order)+free%2
        candidate=dict(n=reduced_n,edges=reduced,grundy=value,source_points=n)
        if value not in best or (len(edges),reduced_n)<(len(best[value]['edges']),best[value]['n']):best[value]=candidate
    for value,row in best.items():assert NORMAL.grundy(row['n'],row['edges'])==value
    output=dict(scope='all edge subfamilies of the fixed ten- and twelve-point witnesses',
                cases=len(cases),cpp_safe_states=native['safe_states'],summaries=summaries,
                best_by_grundy=best,limitation='not all families at the reported edge counts')
    (directory/'output/prune.json').write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(output,indent=2),flush=True)


if __name__=='__main__':main()
