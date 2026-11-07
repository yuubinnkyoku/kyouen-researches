#!/usr/bin/env python3
"""Point-optimal pure-triple g8/g9 witnesses and exact integer geometry."""
import importlib.util
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parents[3]


def module(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result)
    return result


NORMAL=module('cover_two_residual','research/experiments/rank-three-cover-two-grundy-20261108/audit.py')
MISERE=module('mobility_residual','research/experiments/misere-legal-count-gap-two-20261108/verify.py')
GEOMETRY=module('mobility_geometry','research/experiments/common-pivot-misere-bound-20261108/verify_geometry.py')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--pruned',action='store_true');args=parser.parse_args()
    directory=Path(__file__).resolve().parent
    discovery=json.loads((directory/'output/n11_r3-3_c2.json').read_text())
    source=tuple(discovery['witness_edges']);active=0
    for edge in source:active|=edge
    order=[v for v in range(11) if active>>v&1]
    assert len(order)==10 and len(source)==9
    edges=tuple(sorted(sum(1<<j for j,v in enumerate(order) if e>>v&1) for e in source))
    if args.pruned:
        edges=tuple(json.loads((directory/'output/prune.json').read_text())['best_by_grundy']['8']['edges'])
    assert all(e.bit_count()==3 for e in edges)
    records=[];geometry=[]
    for n,target in ((10,8),(11,9)):
        g=NORMAL.grundy(n,edges);h=MISERE.residual_misere(n,edges)
        assert g==h==target
        records.append(dict(n=n,edges=edges,normal=g,misere_aux=h))
        board=GEOMETRY.GEOMETRY.audit(n,edges)
        occupied=sum(1<<v for v in board['occupied'])
        residual=[sum(1<<v for v in quad)&~occupied for quad in board['actual_quads']]
        assert GEOMETRY.misere_values(n,residual)[0]==h
        assert all(any(v in (0,1) for v in quad) for quad in board['actual_quads'])
        board['misere_aux']=h;geometry.append(board)
    compiler=shutil.which('g++')
    if compiler is None:raise SystemExit('g++ is required')
    cpp=ROOT/'research/experiments/common-pivot-misere-bound-20261108/independent.cpp'
    with tempfile.TemporaryDirectory(prefix='kyouen-optimal-eight-') as scratch:
        temp=Path(scratch).resolve();assert temp.parent==Path(tempfile.gettempdir()).resolve()
        data=temp/'cases.txt';exe=temp/'verify.exe';values=temp/'values.bin';meta=temp/'meta.json'
        data.write_text(str(len(records))+'\n'+'\n'.join(' '.join(map(str,[r['n'],len(r['edges']),*r['edges']])) for r in records)+'\n',encoding='ascii')
        subprocess.run([compiler,'-std=c++17','-O2',str(cpp),'-o',str(exe)],check=True)
        subprocess.run([str(exe),str(data),str(values),str(meta)],check=True)
        assert values.read_bytes()==bytes(x for r in records for x in (r['normal'],r['misere_aux']))
        native=json.loads(meta.read_text())
    output=dict(audit='PASS',records=records,cpp_safe_states=native['safe_states'],integer_realizations=geometry,
                minimum_normal_legal_points=dict(grundy_eight=10,grundy_nine=11),
                minimum_misere_legal_points=dict(value_eight=10,value_nine=11),
                lower_bound='K0690: either value >=4 implies legal_points>=value+2',
                edge_count=len(edges),edge_minimum='edge-count sufficiency only; no global edge minimum claimed')
    target=directory/'output'/('audit_pruned.json' if args.pruned else 'audit.json')
    target.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in output.items() if k!='integer_realizations'},indent=2),flush=True)


if __name__=='__main__':main()
