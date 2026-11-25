#!/usr/bin/env python3
"""Replay a mutated graph with a high restricted value, then raw pivot games."""
from itertools import combinations
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
from audit import ROOT,NORMAL,formula,graph_misere


def main():
    directory=Path(__file__).resolve().parent
    discovery=json.loads((directory/'output/restricted_mutations.json').read_text())
    n=14
    pairs=[tuple(v for v in range(n) if edge>>v&1) for edge in discovery['edges']]
    assert all(len(pair)==2 for pair in pairs) and len(set(pairs))==len(pairs)
    normal,_=NORMAL.graph_values(n,pairs)
    h,_,_,_,t,*_=graph_misere(n,pairs)
    assert (normal,h,t)==(discovery['normal'],discovery['misere_aux'],discovery['restricted'])
    assert (normal,h,t)==(7,0,5)
    records=[]
    for free in range(4):
        outside=n+1+free;poison=1<<n
        edges=tuple([1|(1<<(n+1))]+[1|(1<<(u+1))|(1<<(v+1)) for u,v in pairs])
        g=NORMAL.formula(outside,poison,pairs);aux=formula(outside,poison,pairs)
        records.append(dict(n=outside+1,edges=edges,normal=g,misere_aux=aux,free_added=free))
    assert records[0]['misere_aux']==7
    assert [r['misere_aux'] for r in records][::2]==[7,7]
    assert records[1]['misere_aux']==records[3]['misere_aux']
    compiler=shutil.which('g++')
    if compiler is None:raise SystemExit('g++ is required')
    with tempfile.TemporaryDirectory(prefix='kyouen-high-misere-') as scratch:
        temp=Path(scratch).resolve();assert temp.parent==Path(tempfile.gettempdir()).resolve()
        data=temp/'cases.txt';exe=temp/'verify.exe';values=temp/'values.bin';meta=temp/'meta.json'
        data.write_text(str(len(records))+'\n'+'\n'.join(' '.join(map(str,[r['n'],len(r['edges']),*r['edges']])) for r in records)+'\n',encoding='ascii')
        subprocess.run([compiler,'-std=c++17','-O2',str(directory/'independent.cpp'),'-o',str(exe)],check=True)
        subprocess.run([str(exe),str(data),str(values),str(meta)],check=True)
        assert values.read_bytes()==bytes(x for r in records for x in (r['normal'],r['misere_aux']))
        native=json.loads(meta.read_text())
    output=dict(audit='PASS',link_graph=dict(vertices=n,edges=discovery['edges'],normal=normal,misere_aux=h,restricted=t),
                cases_compared=len(records),cpp_safe_states=native['safe_states'],records=records,
                geometry='K0683 applies; higher witnesses have no separate integer-coordinate audit here')
    (directory/'output/high_audit.json').write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in output.items() if k!='link_graph'},indent=2),flush=True)


if __name__=='__main__':main()
