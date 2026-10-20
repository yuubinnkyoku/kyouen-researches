#!/usr/bin/env python3
"""Negative controls: altered witness, dual, or coverage must fail."""
import json
from pathlib import Path
import shutil,subprocess,sys,tempfile
B=Path(__file__).resolve().parent
files=['verify_compact385.py','verify_core.py','loss_roots35.txt','selected385.txt','dual_components.json','win_witnesses1561.tsv','win_witnesses1591.tsv','core_gap.py','core_positive78.txt','core_zero24.txt','component0_essential115.json','component6_essential100.json']

def reject(name,modify):
    with tempfile.TemporaryDirectory(prefix='n11-compact385-negative-') as td:
        dst=Path(td)
        for f in files:shutil.copy2(B/f,dst/f)
        modify(dst)
        p=subprocess.run([sys.executable,'-u',str(dst/'verify_compact385.py')],capture_output=True,text=True,timeout=60)
        assert p.returncode!=0,(name,'mutation was accepted',p.stdout)
        assert ('AssertionError' in p.stderr or 'ValueError' in p.stderr), (name,'unexpected rejection',p.stderr)
        print('PASS reject',name)

def missing_high(d):
    p=d/'win_witnesses1561.tsv';a=p.read_text().splitlines();p.write_text('\n'.join(a[1:])+'\n')
def corrupt_dual(d):
    p=d/'dual_components.json';a=json.loads(p.read_text());key=next(iter(a[0]['weights']));a[0]['weights'][key]='-1';p.write_text(json.dumps(a))
def missing_leaf(d):
    p=d/'selected385.txt';a=p.read_text().splitlines();p.write_text('\n'.join(a[1:])+'\n')
def bad_witness(d):
    p=d/'win_witnesses1561.tsv';a=p.read_text().splitlines();h,_=a[0].split('\t');a[0]=h+'\t999';p.write_text('\n'.join(a)+'\n')
for name,mutate in [('missing high-weight exclusion',missing_high),('negative dual weight',corrupt_dual),('missing LOSS leaf',missing_leaf),('illegal WIN witness',bad_witness)]:reject(name,mutate)
