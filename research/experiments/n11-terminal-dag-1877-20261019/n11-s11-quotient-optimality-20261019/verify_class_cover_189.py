#!/usr/bin/env python3
"""Independently check S11 witness hypergraph quotient: 349 positions, 189 games.

Requires Python standard library only. Rebuilds all 672 S10 proof obligations,
checks each selected S11 witness is a legal child, checks exact forbidden-hyperedge
isomorphism via explicit permutations, and solves only 189 representatives.
No optimizer or precomputed verdict table is trusted. Empty-board remains UNKNOWN.
"""
import json
from itertools import combinations
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'n11-s11-dual-branch-optimality-20261019'))
import compact_proof184_342 as v

def minimal_forbidden(m):
    v.check(v.safe(m) and m.bit_count()==11 and v.canonical(m)==m,'invalid S11 position')
    base=v.points(m);moves=v.legal(m);n=len(moves)
    bad=[]
    for i,j in combinations(range(n),2):
        if any(v.circle(a,b,moves[i],moves[j]) for a,b in combinations(base,2)):
            bad.append((1<<i)|(1<<j))
    for i,j,k in combinations(range(n),3):
        mask=(1<<i)|(1<<j)|(1<<k)
        if any(mask&b==b for b in bad):continue
        if any(v.circle(a,moves[i],moves[j],moves[k]) for a in base):bad.append(mask)
    for ids in combinations(range(n),4):
        mask=sum(1<<i for i in ids)
        if any(mask&b==b for b in bad):continue
        if v.circle(*(moves[i] for i in ids)):bad.append(mask)
    return n,set(bad)

def high_boundary():
    roots=v.decode_positions(v.ROOTS_B85)
    obligations=set().union(*(v.children(r) for r in roots))
    v.check(len(roots)==18 and len(obligations)==387)
    packed=v.decode(v.WEIGHTS_B85)
    weights={p:(packed[i//4]>>(2*(i%4)))&3 for i,p in enumerate(sorted(obligations))}
    boundary=set().union(*(v.children(o) for o in obligations))
    v.check(len(boundary)==3044)
    high=[p for p in boundary if sum(weights[q] for q in ({v.canonical(p^(1<<i)) for i in v.points(p)}&obligations))>2]
    v.check(len(high)==672)
    return high

def run():
    cert=json.loads((HERE/'s11_class_cover_189_certificate.json').read_text())
    v.check(cert['format']=='n11-s11-hypergraph-class-cover-v1','wrong certificate format')
    entries=cert['witnesses']
    v.check(len(entries)==349,'wrong number of witness boards')
    selected={int(p,16) for p,r,perm in entries}
    v.check(len(selected)==349,'duplicate witness')
    reps={int(r,16) for r in cert['representatives']}
    v.check(len(reps)==189,'wrong number of representative games')
    v.check({int(r,16) for p,r,perm in entries}==reps,'missing representative')
    # No saved incidence graph is trusted.
    high=high_boundary()
    legal_children=set()
    covered=0
    for p in high:
        kids=v.children(p)
        legal_children.update(kids)
        v.check(bool(kids&selected),f'uncovered S10 obligation: {p:032x}')
        covered+=1
    v.check(selected<=legal_children,'witness is not a legal S11 reply')
    signatures={p:minimal_forbidden(p) for p in selected|reps}
    for p_hex,r_hex,perm in entries:
        p=int(p_hex,16);r=int(r_hex,16)
        n,bad=signatures[p]
        nr,badr=signatures[r]
        v.check(n==nr and sorted(perm)==list(range(n)),'bad permutation')
        mapped={sum(1<<perm[i] for i in range(n) if mask>>i&1) for mask in bad}
        v.check(mapped==badr,'hypergraph isomorphism mismatch')
    states=0
    for r in reps:
        win,used=v.next_player_wins_at_s10(r)
        v.check(not win,f'S11 representative is WIN: {r:032x}')
        states+=used
    v.check(states==5805,'unexpected terminal work')
    print('PASS: all 672 high-weight S10 positions have an S11 witness')
    print('PASS: 349 S11 witnesses certified by 189 exact hypergraph isomorphism classes')
    print('PASS: 189 independent terminal LOSS computations, 5,805 states')
    print('Original 342 independent witnesses: 7,779 states; saved 1,974 (25.38%)')
    print('Standard 11x11 empty-board winner remains UNKNOWN')

if __name__=='__main__':run()
