#!/usr/bin/env python3
"""Replay link t6 and verify the full nineteen/twenty-point pivot games."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'research/experiments/common-pivot-misere-bound-20261108'))
SPEC=importlib.util.spec_from_file_location('pivot_misere',ROOT/
    'research/experiments/common-pivot-misere-bound-20261108/audit.py')
M=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(M)


def main():
    directory=Path(__file__).resolve().parent;link_checks=[]
    for n in (14,16,18):
        row=json.loads((directory/'output'/('n'+str(n)+'.json')).read_text())
        pairs=[tuple(v for v in range(n) if edge>>v&1) for edge in row['edges']]
        g,_=M.NORMAL.graph_values(n,pairs);h,b,_,_,t,u,*_=M.graph_misere(n,pairs)
        assert (g,h,t)==(row['normal'],row['misere_aux'],row['restricted'])
        link_checks.append(dict(n=n,normal=g,misere_aux=h,restricted=t,
                                one_free_misere=b,one_free_restricted=u))
    row=json.loads((directory/'output/n16.json').read_text());n=16
    pairs=[tuple(v for v in range(n) if edge>>v&1) for edge in row['edges']]
    records=[]
    for free in (0,1):
        outside=n+2+free;poison=(1<<n)|(1<<(n+1))
        edges=tuple([1|(1<<(n+1)),1|(1<<(n+2))]+[1|(1<<(u+1))|(1<<(v+1)) for u,v in pairs])
        g=M.NORMAL.formula(outside,poison,pairs);h=M.formula(outside,poison,pairs)
        assert (g,h)==(free,8+free)
        records.append(dict(n=outside+1,edges=edges,normal=g,misere_aux=h))
    compiler=shutil.which('g++')
    if compiler is None:raise SystemExit('g++ is required')
    cpp=ROOT/'research/experiments/common-pivot-misere-bound-20261108/independent.cpp'
    with tempfile.TemporaryDirectory(prefix='kyouen-pivot-eight-nine-') as scratch:
        temp=Path(scratch).resolve();assert temp.parent==Path(tempfile.gettempdir()).resolve()
        data=temp/'cases.txt';exe=temp/'verify.exe';values=temp/'values.bin';meta=temp/'meta.json'
        data.write_text(str(len(records))+'\n'+'\n'.join(' '.join(map(str,[r['n'],len(r['edges']),*r['edges']])) for r in records)+'\n',encoding='ascii')
        subprocess.run([compiler,'-std=c++17','-O2',str(cpp),'-o',str(exe)],check=True)
        subprocess.run([str(exe),str(data),str(values),str(meta)],check=True)
        assert values.read_bytes()==bytes(x for r in records for x in (r['normal'],r['misere_aux']))
        native=json.loads(meta.read_text())
    output=dict(audit='PASS',link_checks=link_checks,cases_compared=2,cpp_safe_states=native['safe_states'],
                records=records,geometry_occupied_anchors=34,geometry_board_points=[53,54],
                geometry_status='constructive K0683 realization; no separate coordinate census',
                minimum_status='no global minimum claim')
    (directory/'output/audit.json').write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in output.items() if k!='records'},indent=2),flush=True)


if __name__=='__main__':main()
