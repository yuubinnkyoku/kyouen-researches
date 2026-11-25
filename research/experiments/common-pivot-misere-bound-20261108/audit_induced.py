#!/usr/bin/env python3
"""Raw verification of the smaller induced h6/h7 witnesses."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
from audit import NORMAL,formula,graph_misere


def main():
    directory=Path(__file__).resolve().parent
    prior=json.loads((directory/'output/induced_high.json').read_text())['best_by_misere_value']
    base=prior['6'];n=base['link_vertices']
    pairs=[tuple(v for v in range(n) if edge>>v&1) for edge in base['link_edges']]
    assert n==12 and base['poison_points']==2
    records=[]
    for free in (0,1):
        outside=n+2+free;poison=(1<<n)|(1<<(n+1))
        edges=tuple([1|(1<<(n+1)),1|(1<<(n+2))]+[1|(1<<(u+1))|(1<<(v+1)) for u,v in pairs])
        g=NORMAL.formula(outside,poison,pairs);h=formula(outside,poison,pairs)
        assert (g,h)==(free,6+free)
        records.append(dict(n=outside+1,edges=edges,normal=g,misere_aux=h))
    compiler=shutil.which('g++')
    if compiler is None:raise SystemExit('g++ is required')
    with tempfile.TemporaryDirectory(prefix='kyouen-induced-high-') as scratch:
        temp=Path(scratch).resolve();assert temp.parent==Path(tempfile.gettempdir()).resolve()
        data=temp/'cases.txt';exe=temp/'verify.exe';values=temp/'values.bin';meta=temp/'meta.json'
        data.write_text(str(len(records))+'\n'+'\n'.join(' '.join(map(str,[r['n'],len(r['edges']),*r['edges']])) for r in records)+'\n',encoding='ascii')
        subprocess.run([compiler,'-std=c++17','-O2',str(directory/'independent.cpp'),'-o',str(exe)],check=True)
        subprocess.run([str(exe),str(data),str(values),str(meta)],check=True)
        assert values.read_bytes()==bytes(x for r in records for x in (r['normal'],r['misere_aux']))
        native=json.loads(meta.read_text())
    output=dict(audit='PASS',link_graph=base,cases_compared=2,cpp_safe_states=native['safe_states'],records=records,
                geometry_board_points=[37,38],occupied_anchors=22,
                geometry_status='constructively realizable by K0683; no separate coordinate census here',
                minimum_status='no global minimality claim')
    (directory/'output/induced_high_audit.json').write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(output,indent=2),flush=True)


if __name__=='__main__':main()
