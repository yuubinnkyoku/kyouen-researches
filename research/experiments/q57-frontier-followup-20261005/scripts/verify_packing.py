#!/usr/bin/env python3
"""Audit the exact finite ingredients of the universal q57 bound 158.

The proof is in proof.md. Finite checks below test implementations; they do
not replace the chain, inversion/Melchior, or five-row arguments.
"""
from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations
import json
from math import comb
from pathlib import Path
import sys

if not __debug__:
    raise SystemExit('Exact validation requires assertions; do not use -O.')

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'research/experiments/fixed-width/scripts'))
from q48_exact_threshold import through_three


CHAINS = (
    ((0,1),(0,2),(0,3),(0,4),(0,5),(1,5),(2,5),(3,5),(4,5)),
    ((1,2),(1,3),(1,4),(2,4),(3,4)),
    ((2,3),),
)


def chains_for_size(r):
    return [tuple([(k,j) for j in range(k+1,r-k)]
                  +[(i,r-1-k) for i in range(k+1,r-1-k)])
            for k in range(r//2)]


def sharp_energy(r):
    return (2*r**3-3*r*r+4*r-3*(r%2))//12


def energy(points):
    counts = Counter(a+b for a,b in combinations(points, 2))
    return sum(c*c for c in counts.values())


def verify_general_energy():
    summaries=[]
    for r in range(1,31):
        chains=chains_for_size(r)
        assert sorted(pair for chain in chains for pair in chain)==list(combinations(range(r),2))
        assert all(len(chain)==2*r-4*k-3 for k,chain in enumerate(chains))
        assert all(a<=c and b<=d and (a,b)!=(c,d)
                   for chain in chains for (a,b),(c,d) in zip(chain,chain[1:]))
        weighted_budget=sum((2*k+1)*len(chain) for k,chain in enumerate(chains))
        assert weighted_budget==sharp_energy(r)==energy(range(r))
        summaries.append(dict(r=r,sharp_energy=sharp_energy(r),chain_lengths=list(map(len,chains))))
    tested=0
    for r in range(1,9):
        chains=chains_for_size(r)
        pair_chain={pair:k for k,chain in enumerate(chains) for pair in chain}
        for points in combinations(range(12),r):
            groups={}
            for i,j in combinations(range(r),2):
                groups.setdefault(points[i]+points[j],[]).append(pair_chain[(i,j)])
            assert all(len(indices)==len(set(indices)) for indices in groups.values())
            assert all(sum(2*k+1 for k in indices)>=len(indices)**2 for indices in groups.values())
            assert energy(points)<=sharp_energy(r)
            tested+=1
    return dict(arithmetic_progressions=summaries,coordinate_subsets=tested,
                formula='(2*r**3-3*r*r+4*r-3*(r%2))//12')


def verify_chains():
    assert list(CHAINS)==chains_for_size(6)
    assert sorted(pair for chain in CHAINS for pair in chain) == list(combinations(range(6),2))
    for chain in CHAINS:
        assert all(a<=c and b<=d and (a,b)!=(c,d)
                   for (a,b),(c,d) in zip(chain, chain[1:]))
    maximum = 0
    witness = None
    tested = 0
    for points in combinations(range(17),6):
        counts = Counter(a+b for a,b in combinations(points,2))
        assert all(len(set(points[a]+points[b] for a,b in chain))==len(chain)
                   for chain in CHAINS)
        c2 = sum(c==2 for c in counts.values())
        c3 = sum(c==3 for c in counts.values())
        assert max(counts.values())<=3 and c3<=1 and c2+2*c3<=6
        e = energy(points)
        assert e==15+2*c2+6*c3 and e<=29
        if e>maximum:
            maximum,witness=e,points
        tested+=1
    assert maximum==29
    # Independently count the common-sum chord pairs for all 924 six-point
    # subsets of a different coordinate universe; retain the worst pair.
    sets = list(combinations(range(12),6))
    profiles = [Counter(a+b for a,b in combinations(points,2)) for points in sets]
    cross_max = 0
    for i,a in enumerate(profiles):
        for b in profiles[i:]:
            common = sum(c*b.get(s,0) for s,c in a.items())
            assert common<=29
            cross_max = max(cross_max,common)
    return dict(chains=[list(c) for c in CHAINS],six_point_sets=tested,
                energy_maximum=maximum,energy_witness=witness,
                cross_pairs=len(sets)*(len(sets)+1)//2,
                cross_common_sum_maximum=cross_max)


def curves_from_triples(m):
    board = [(x,y) for y in range(5) for x in range(m)]
    keys = {through_three(*ps) for ps in combinations(board,3)}
    curves = []
    for key in keys:
        a,b,c,d=key
        if not a:
            continue
        pts = frozenset(i for i,(x,y) in enumerate(board)
                        if a*(x*x+y*y)+b*x+c*y+d==0)
        if len(pts)>=7:
            assert len({board[i][1] for i in pts})<=4
            curves.append((key,pts))
    return board,curves


def verify_state(rows,m,target,curves):
    occupied = {y*m+x for y,row in enumerate(rows) for x in row}
    assert all(len(row)<=6 for row in rows) and len(rows[target])<=5
    assert all(len(pts & occupied)<=6 for _,pts in curves)
    blockers = [(key,pts) for key,pts in curves
                if len(pts & occupied)==6
                and any(p//m==target and p not in occupied for p in pts)]
    x=y=0
    used_pairs=set()
    point_degrees=Counter()
    for key,pts in blockers:
        old = pts & occupied
        on_target = old & set(range(target*m,(target+1)*m))
        assert len(on_target)<=1
        external = old-on_target
        row_points = {j:sorted(p%m for p in external if p//m==j)
                      for j in range(5) if j!=target}
        profile = sorted(len(v) for v in row_points.values() if v)
        if not on_target:
            assert profile==[2,2,2]
            x+=1
        else:
            assert profile==[1,2,2]
            y+=1
            point_degrees.update(on_target)
        chords = [(j,tuple(v)) for j,v in row_points.items() if len(v)==2]
        assert len(set(sum(pair) for _,pair in chords))==1
        for pair in combinations(chords,2):
            assert pair not in used_pairs
            used_pairs.add(pair)
    budget=0
    for i,j in combinations([v for v in range(5) if v!=target],2):
        a=Counter(u+v for u,v in combinations(rows[i],2))
        b=Counter(u+v for u,v in combinations(rows[j],2))
        budget+=sum(c*b.get(s,0) for s,c in a.items())
    assert 3*x+y==len(used_pairs)<=budget<=174
    assert y<=22*len(rows[target])<=110
    assert all(degree<=22 for degree in point_degrees.values())
    return dict(target=target,type_zero=x,type_one=y,
                common_chord_pair_budget=budget,point_degrees=dict(point_degrees),
                unavailable_bound=len(rows[target])+2*x+y)


def verify_examples(source):
    record=json.loads(source.read_text())
    witness=record['lower_bound_witness']
    rows=witness['rows'];m=witness['m']
    board,curves=curves_from_triples(m)
    audit=verify_state(rows,m,0,curves)
    assert audit['unavailable_bound']>=m
    # Exhaust all subsets of the union of the two eight-point circles on
    # 5x4. The six board points not in either circle are absent throughout.
    # This finite audit is nonvacuous and is not a whole-board census.
    small_m=4
    board,curves=curves_from_triples(small_m)
    active=sorted(set().union(*(pts for _,pts in curves)))
    assert len(curves)==2 and len(active)==14
    tested=0;with_blockers=0
    for mask in range(1<<len(active)):
        occupied={p for i,p in enumerate(active) if mask>>i&1}
        if any(len(pts & occupied)>=7 for _,pts in curves):
            continue
        rows2=[[a for a in range(small_m) if (b*small_m+a) in occupied] for b in range(5)]
        for target in range(5):
            a=verify_state(rows2,small_m,target,curves)
            with_blockers+=a['type_zero']+a['type_one']>0
            tested+=1
    return dict(m18_witness=audit,small_board=[5,small_m],
                small_active_points=active,
                small_target_states=tested,small_cases_with_blockers=with_blockers,
                small_seven_point_circles=len(curves))


def optimize():
    best=[]
    for b in range(6):
        value,x,y=max((b+2*x+y,x,y) for x in range(59)
                      for y in range(22*b+1) if 3*x+y<=174)
        best.append(dict(target_stones=b,maximum_unavailable=value,type_zero=x,type_one=y))
    assert best[-1]['maximum_unavailable']==157
    return dict(external_rows=4,row_capacity=6,chord_pair_budget=6*29,
                five_rich_line_bound=(comb(24,2)-3)//12,
                target_cases=best,stabilization_upper_bound=158)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,default=HERE/'output/packing-audit.json')
    ap.add_argument('--witness',type=Path,
                    default=ROOT/'research/experiments/fixed-width-frontier-20261005/output/q57_independent_witness.json')
    args=ap.parse_args()
    # The eight-square-residue obstruction is inspected directly: all five
    # rows would have to satisfy this necessary condition.
    squares={i*i%9 for i in range(9)}
    assert not any(all((n-(2*y+c)**2)%9 in squares for y in range(5))
                   for c in range(9) for n in range(9))
    out=dict(scope='finite audits of a universal mathematical bound; not a finite proof of stabilization',
             modular_pairs=81,chord_energy=verify_chains(),general_energy=verify_general_energy(),
             optimization=optimize(),examples=verify_examples(args.witness))
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(out['optimization'],ensure_ascii=False))


if __name__=='__main__':
    main()
