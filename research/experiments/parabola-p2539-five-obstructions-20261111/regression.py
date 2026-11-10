"""Compare bounded search to brute force, replay certificates, and reject corrupt controls."""
import argparse
from copy import deepcopy
from itertools import combinations
import json
from pathlib import Path
import random
from produce import solve
from verify import check_tree,check_hitting,HERE,sha,save


def brute(rows,n,k):
    return any(all(set(choice).intersection(row) for row in rows) for size in range(min(n,k)+1) for choice in combinations(range(n),size))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();assert not a.output.exists()
    checked=0;sat=0;unsat=0
    def exercise(rows,n,k):
        nonlocal checked,sat,unsat
        ok,data,_=solve(rows,k);assert ok==brute(rows,n,k)
        if ok:check_hitting(rows,k,data,set(range(n)));sat+=1
        else:check_tree(rows,k,data);unsat+=1
        checked+=1
    subsets=[set(c) for size in range(4) for c in combinations(range(3),size)]
    for mask in range(1<<len(subsets)):
        rows=[row for i,row in enumerate(subsets) if mask&(1<<i)]
        for k in range(4):exercise(rows,3,k)
    rng=random.Random(2539)
    options=[set(c) for size in range(1,4) for c in combinations(range(5),size)]
    for _ in range(200):
        rows=rng.sample(options,rng.randrange(len(options)+1))
        for k in range(6):exercise(rows,5,k)
    rejected=[]
    rows=[{0},{1}];ok,node,_=solve(rows,1);assert not ok
    controls={
        'short-packing':{'type':'packing','edges':[0]},
        'repeated-packing':{'type':'packing','edges':[0,0]},
        'wrong-edge-index':{'type':'packing','edges':[0,2]},
        'bool-edge-index':{'type':'packing','edges':[0,True]},
        'false-empty':{'type':'empty','edge':0},
        'extra-field':dict(node,extra=True),
        'missing-branch-child':{'type':'branch','edge':0,'children':{}},
        'unknown-node':{'type':'unknown'},
    }
    for name,n in controls.items():
        try:check_tree(rows,1,n)
        except (AssertionError,KeyError):rejected.append(name)
        else:raise AssertionError(name)
    for name,w in [('missed-edge',[0]),('exceeds-budget',[0,1]),('outside-allowed',[0,3]),('duplicates',[0,0]),('bool-point',[True])]:
        try:check_hitting(rows,1,w,{0,1})
        except AssertionError:rejected.append(name)
        else:raise AssertionError(name)
    cert=json.loads((HERE/'output/certificate.json').read_bytes())
    branch=next(r for r in cert['entries'] if r['status']=='EXCLUDED' and r['refutation']['type']=='branch')
    node=deepcopy(branch['refutation']);node['children'].pop(next(iter(node['children'])))
    # Generic branch coverage is checked against a real branch's selected point set.
    selected={int(v) for v in branch['refutation']['children']}
    try:check_tree([selected],5,dict(type='branch',edge=0,children=node['children']))
    except AssertionError:rejected.append('actual-branch-omission')
    else:raise AssertionError('actual-branch-omission')
    save(a.output,dict(bruteforce_cases=checked,satisfiable=sat,unsatisfiable=unsat,corruptions_rejected=rejected,
        producer_source_sha256=sha((HERE/'produce.py').read_bytes()),verifier_source_sha256=sha((HERE/'verify.py').read_bytes()),source_sha256=sha(Path(__file__).read_bytes()),
        scope='Finite exhaustive n3 families and deterministic n5 samples, both outcomes replayed against brute force, malformed proof/witness controls. General hitting-tree soundness is a separate inductive argument.'))
    print('PASS',checked,'brute-force comparisons and',len(rejected),'corruptions',flush=True)


if __name__=='__main__':main()
