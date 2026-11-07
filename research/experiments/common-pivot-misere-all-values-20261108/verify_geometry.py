#!/usr/bin/env python3
"""Independent small paired/pure witnesses and exact integer-circle realization."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
from verify import ROOT, graph, paired


def module(name, relative):
    spec=importlib.util.spec_from_file_location(name,ROOT/relative)
    result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result)
    return result


GEOMETRY=module('all_values_geometry','research/experiments/rank-three-residual-universality-20261107/verify.py')
MISERE=module('all_values_residual','research/experiments/misere-legal-count-gap-two-20261108/verify.py')


def main():
    directory=Path(__file__).resolve().parent;cases=[]
    for m in (1,2):
        n,edges=graph(m,1);legal,forbidden,poison=paired(n,edges,1)
        cases.append(dict(kind='paired',m=m,n=legal,edges=forbidden,normal=0,misere_aux=m+2))
    n,edges=graph(2,0);triples=tuple(1|edge<<1 for edge in edges)
    cases.extend([dict(kind='pure',m=2,n=n+1,edges=triples,normal=1,misere_aux=4),
                  dict(kind='pure_one_free',m=2,n=n+2,edges=triples,normal=0,misere_aux=5)])
    geometries=[]
    for row in cases:
        assert MISERE.residual_misere(row['n'],tuple(row['edges']))==row['misere_aux']
        board=GEOMETRY.audit(row['n'],row['edges']);assert board['grundy']==row['normal']
        assert all(0 in quad for quad in board['actual_quads'])
        board.update(kind=row['kind'],misere_aux=row['misere_aux']);geometries.append(board)
        print(dict(kind=row['kind'],n=row['n'],board_points=len(board['points']),h=row['misere_aux']),flush=True)
    compiler=shutil.which('g++')
    if not compiler:raise SystemExit('g++ is required')
    with tempfile.TemporaryDirectory(prefix='kyouen-all-values-geometry-') as scratch:
        temp=Path(scratch).resolve();assert temp.parent==Path(tempfile.gettempdir()).resolve()
        data=temp/'cases.txt';exe=temp/'verify.exe';values=temp/'values.bin';metadata=temp/'raw.json'
        data.write_text(str(len(cases))+'\n'+'\n'.join(' '.join(map(str,[r['n'],len(r['edges']),*r['edges']])) for r in cases)+'\n',encoding='ascii')
        cpp=ROOT/'research/experiments/common-pivot-misere-bound-20261108/independent.cpp'
        subprocess.run([compiler,'-std=c++17','-O3',str(cpp),'-o',str(exe)],check=True)
        subprocess.run([str(exe),str(data),str(values),str(metadata)],check=True)
        assert values.read_bytes()==bytes(x for r in cases for x in (r['normal'],r['misere_aux']))
        native=json.loads(metadata.read_text())
    output=dict(audit='PASS',records=cases,integer_realizations=geometries,
                cpp_safe_states=native['safe_states'],quadruples_checked=sum(r['quadruples'] for r in geometries),
                limitation='Small independent audits; arbitrary values follow from the mutual-induction proof.')
    target=directory/'output/geometry.json';target.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in output.items() if k!='integer_realizations'},indent=2),flush=True)


if __name__=='__main__':main()
