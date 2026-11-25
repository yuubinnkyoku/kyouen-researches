"""Known-board and residual smoke checks for the changed cache/replay boundary."""
import argparse
import csv
import json
import subprocess
from audit import ROOT,OUT,dump,digest

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('solver')
    args=ap.parse_args()
    solver=(ROOT/args.solver).resolve()
    results=[]
    # All small known boards plus every publish/UNKNOWN fallback mode on n4/n5.
    configs=[(4,0,'all',200000),(5,0,'all',200000),
             (4,6,'all',200000),(5,6,'all',200000),
             (6,6,'all',200000),(7,6,'all',200000)]
    for publish in ['root','separate']:
        configs += [(4,8,publish,200000),(5,8,publish,200000)]
    configs += [(4,8,'all',1),(5,8,'all',1)]
    expected={4:'LOSS',5:'WIN',6:'WIN',7:'LOSS'}
    for n,legal,publish,budget in configs:
        command=[str(solver),f'--n={n}','--empty','--memo=22','--budget=60',
            f'--exact-legal={legal}',f'--exact-budget={budget}','--exact-retries=2',f'--exact-publish={publish}']
        run=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=70)
        if run.returncode or f'[empty] {expected[n]}' not in run.stdout+run.stderr:
            raise ValueError(('known board regression',command,run.stdout,run.stderr))
        results.append(dict(n=n,exact_legal=legal,publish=publish,budget=budget,outcome=expected[n]))
        print(results[-1],flush=True)
    dump('solver-regression.json',dict(solver_sha256=digest(solver),
        solver_source_sha256=digest(ROOT/'cpp/solvers/kyouen_dfpn_root.cpp'),known_board_cases=results))

if __name__=='__main__': main()
