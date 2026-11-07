#!/usr/bin/env python3
"""Regression for the parameterized generator: six-edge signatures must be unchanged."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


def main():
    directory=Path(__file__).resolve().parent;root=directory.parents[2]
    old=json.loads((root/'research/experiments/pure-triple-few-edge-grundy-20261107/output/audit.json').read_text())['records']
    previous=[r for r in old if r['h']==5]
    expected=json.loads((directory/'output/audit.json').read_text())
    compiler=shutil.which('g++')
    if compiler is None:raise SystemExit('g++ is required')
    with tempfile.TemporaryDirectory(prefix='kyouen-six-generation-regression-') as scratch:
        temp=Path(scratch).resolve();assert temp.parent==Path(tempfile.gettempdir()).resolve()
        data=temp/'previous.txt';generated=temp/'signatures.txt';exe=temp/'generate.exe'
        data.write_text(str(len(previous))+'\n'+'\n'.join(' '.join(map(str,r['signature'])) for r in previous)+'\n',encoding='ascii')
        subprocess.run([compiler,'-std=c++17','-O3',str(directory/'generate.cpp'),'-o',str(exe)],check=True)
        report=json.loads(subprocess.check_output([str(exe),str(data),str(generated)],text=True))
        assert report==expected['generation']
        rows=[list(map(int,line.split())) for line in generated.read_text().splitlines()[1:]]
        assert rows==[[r['automorphism_order'],*r['signature']] for r in expected['records']]
    output=dict(audit='PASS',signatures_compared=len(rows),default_edge_count=6,parameterized_generator_preserves_all_inputs=True)
    (directory/'output/generation_regression.json').write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(output,indent=2))


if __name__=='__main__':main()
