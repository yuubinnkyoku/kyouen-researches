#!/usr/bin/env python3
"""Exact rational lower bound for S11 terminal-hypergraph quotient witness cost.

The bound covers all 982 S11 LOSS candidates provided the supplied 4,522
candidate terminal classifications are complete and correct. To discharge that
assumption, independently rerun the bundled C++ direct-board verifier and
compare every row; or use --full-python for a second-language check.
No SciPy, NetworkX, MILP solver or floating point is used in this verifier.
"""
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
import argparse,json,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'n11-s11-dual-branch-optimality-20261019'))
from verify_class_cover_189 import high_boundary,minimal_forbidden
import compact_proof184_342 as v

def check_optimality(full_python=False):
    high=sorted(high_boundary())
    parents=defaultdict(set)
    for i,p in enumerate(high):
        for q in v.legal(p):parents[v.canonical(p|(1<<q))].add(i)
    v.check(len(parents)==4522,'candidate universe incomplete')
    table={}
    source=HERE/'n11-s11-dual-branch-optimality-20261019'/'all_s11_cpp.tsv'
    for line in source.read_text().splitlines():
        key,result,states,moves,witness=line.split()
        p=int(key,16)
        v.check(p not in table,'duplicate candidate')
        table[p]=(result,int(states),int(moves))
    v.check(set(table)==set(parents),'candidate table differs from geometry')
    v.check(sum(r[0]=='LOSS' for r in table.values())==982,'LOSS count mismatch')
    v.check(sum(r[1] for r in table.values())==86411,'memoized state sum mismatch')
    if full_python:
        for j,p in enumerate(sorted(parents)):
            win,states=v.next_player_wins_at_s10(p)
            v.check((('WIN' if win else 'LOSS'),states,len(v.legal(p)))==table[p],f'wrong terminal verdict: {p:032x}')
            if (j+1)%500==0:print(f'Python terminal audit {j+1}/4522',flush=True)
    loss={p for p,row in table.items() if row[0]=='LOSS'}
    cert=json.loads((HERE/'s11_all_982_isomorphisms.json').read_text())
    v.check(cert['format']=='n11-s11-terminal-hypergraph-quotient-v1')
    representatives=[int(p,16) for p in cert['class_representatives']]
    v.check(len(representatives)==len(set(representatives))==606,'bad class count')
    classes=[set() for _ in representatives]
    v.check(len(cert['members'])==982,'missing isomorphism member')
    members=set()
    signatures={}
    for key,idx,perm in cert['members']:
        p=int(key,16)
        v.check(p in loss and p not in members,'invalid LOSS candidate')
        members.add(p)
        v.check(isinstance(idx,int) and 0<=idx<606,'invalid class index')
        r=representatives[idx]
        classes[idx].add(p)
        if p not in signatures:signatures[p]=minimal_forbidden(p)
        if r not in signatures:signatures[r]=minimal_forbidden(r)
        n,bad=signatures[p];nr,badr=signatures[r]
        v.check(n==nr and sorted(perm)==list(range(n)),'bad isomorphism permutation')
        mapped={sum(1<<perm[i] for i in range(n) if mask>>i&1) for mask in bad}
        v.check(mapped==badr,'false terminal-game isomorphism')
    v.check(members==loss,'incomplete LOSS class partition')
    from verify_nonisomorphic_classes import distinct_classes
    distinct_classes([signatures[r] for r in representatives])
    for j,group in enumerate(classes):
        r=representatives[j]
        v.check(group and r in group,'invalid representative')
        v.check(table[r][1]==min(table[p][1] for p in group),'representative not cheapest')
    dual=json.loads((HERE/'s11_class_cover_dual.json').read_text())
    weights=[Fraction(0) for _ in high]
    seen=set()
    for idx,value in dual:
        v.check(isinstance(idx,int) and 0<=idx<672 and idx not in seen,'duplicate dual weight')
        seen.add(idx);weights[idx]=Fraction(value)
        v.check(weights[idx]>0,'nonpositive dual weight')
    bound=sum(weights)
    v.check(bound==Fraction(11609,2),'unexpected dual bound')
    for j,group in enumerate(classes):
        covered=set().union(*(parents[p] for p in group))
        v.check(sum((weights[i] for i in covered),Fraction(0))<=table[representatives[j]][1],f'dual constraint fails for class {j}')
    # Since the sum of per-class costs is an integer, a dual bound 5804.5 implies >=5805.
    target=(bound.numerator+bound.denominator-1)//bound.denominator
    v.check(target==5805)
    # Independently check the feasible 349-witness / 189-class certificate.
    from verify_class_cover_189 import run as check_feasible
    check_feasible()
    print(f'PASS exact dual bound={bound}; integer lower bound={target} states over all 606 abstract terminal games')
    print('PASS feasible 5,805-state quotient cover matches the lower bound: GLOBAL MINIMUM for specified quotient-cost metric')
    print('The 11x11 empty-board outcome is UNKNOWN')

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--full-python',action='store_true')
    args=ap.parse_args()
    check_optimality(args.full_python)
