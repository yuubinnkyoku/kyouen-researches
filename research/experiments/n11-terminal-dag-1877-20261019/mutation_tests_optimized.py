#!/usr/bin/env python3
"""Ensure independent checker rejects corrupted DAG and witness certificates."""
import copy,json,subprocess,sys,tempfile,shutil
from pathlib import Path
HERE=Path(__file__).resolve().parent
orig=json.loads((HERE/'joint_dag_optimized_final.json').read_text())
cover_path=HERE/'joint_cover_optimized_final.json'
cover=json.loads(cover_path.read_text())

def test(label,mutator):
    with tempfile.TemporaryDirectory() as td:
        t=Path(td)
        shutil.copy(HERE/'verify_joint_dag_optimized.py',t/'verify_joint_dag_optimized.py')
        shutil.copytree(HERE/'n11-s11-quotient-optimality-20261019',t/'n11-s11-quotient-optimality-20261019')
        dag=copy.deepcopy(orig);cov=copy.deepcopy(cover)
        mutator(dag,cov)
        (t/'joint_dag_optimized_final.json').write_text(json.dumps(dag))
        (t/'joint_cover_optimized_final.json').write_text(json.dumps(cov))
        p=subprocess.run([sys.executable,str(t/'verify_joint_dag_optimized.py')],capture_output=True,text=True)
        if p.returncode==0:raise AssertionError('accepted tampered certificate: '+label)
        print('PASS rejected',label,':',p.stderr.strip().splitlines()[-1])

def remove_loss_edge(d,c):
    node=next(n for n in d['nodes'] if not n['win'] and n['n']>1)
    node['edges'].pop()

def flip_win(d,c):
    node=next(n for n in d['nodes'] if n['win'])
    node['win']=False

def corrupt_perm(d,c):
    edge=next(e for n in d['nodes'] for e in n['edges'] if len(e[2])>=2)
    edge[2][0]=edge[2][1]

def remove_witness(d,c):
    c['witnesses'].pop()

if __name__=='__main__':
    for name,fn in [('missing LOSS move',remove_loss_edge),('flipped verdict',flip_win),('false isomorphism',corrupt_perm),('missing S11 witness',remove_witness)]:
        test(name,fn)
    print('PASS: 4/4 certificate mutations rejected')
