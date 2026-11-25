#!/usr/bin/env python3
"""Independent exact arithmetic checks for the three-parallel-lines q=6 theorem.

No external packages.  The determinant verifier is deliberately separate from
pair-sum counting and does not use the circle centre/roots formula.
"""
import itertools
import json
import random
from collections import Counter


def pair_counts(xs):
    return Counter(a+b for a,b in itertools.combinations(xs, 2))


def energy(xs):
    return sum(v*v for v in pair_counts(xs).values())


def det(a):
    # Exact Bareiss integer determinant (no fractions).
    a=[list(row) for row in a]
    n=len(a)
    sign=1
    prev=1
    for k in range(n-1):
        if a[k][k] == 0:
            j=next((j for j in range(k+1,n) if a[j][k]), None)
            if j is None:
                return 0
            a[k],a[j]=a[j],a[k]
            sign=-sign
        p=a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                z=a[i][j]*p-a[i][k]*a[k][j]
                assert z%prev==0
                a[i][j]=z//prev
        for i in range(k+1,n):
            a[i][k]=0
        prev=p
    return sign*a[-1][-1]


def is_cocircular_six(points):
    # Every lifted 4x4 minor must vanish.  This rejects the false positives
    # from a single 4-point test and handles all exact integer coordinates.
    lifts=[(x*x+y*y,x,y,1) for x,y in points]
    return all(det(rows)==0 for rows in itertools.combinations(lifts,4))


def circle_pairs_via_sums(columns):
    # Given three x-columns, a 6-circle has exactly two points per column.
    # The equal-chord-midpoint condition is necessary; four points on the
    # two outside columns determine a circle, which we test independently.
    out=set()
    x0,x1,x2=sorted(columns)
    for p0 in itertools.combinations(columns[x0],2):
        for p1 in itertools.combinations(columns[x1],2):
            if sum(p0)!=sum(p1):
                continue
            for p2 in itertools.combinations(columns[x2],2):
                if sum(p0)!=sum(p2):
                    continue
                pts=tuple(sorted([(x0,y) for y in p0]+[(x1,y) for y in p1]+[(x2,y) for y in p2]))
                if is_cocircular_six(pts):
                    out.add(pts)
    return out


def circle_pairs_brute(columns):
    points=[(x,y) for x,ys in columns.items() for y in ys]
    return {six for six in itertools.combinations(sorted(points),6)
            if is_cocircular_six(six)}


def bound_one_state(columns, target_x, occupied):
    outside=[x for x in columns if x!=target_x]
    B,C=[occupied[x] for x in outside]
    T=occupied[target_x]
    e=sum(pair_counts(B)[s]*pair_counts(C)[s] for s in pair_counts(B))
    # Directly verify all 6-point completions via independent determinants.
    blocked=set()
    for y in columns[target_x]:
        if y in T:
            continue
        allpts=[(x,z) for x,ys in occupied.items() for z in ys]
        for five in itertools.combinations(allpts,5):
            if is_cocircular_six(five+((target_x,y),)):
                blocked.add(y)
                break
    return e,len(blocked),len(T)


def main():
    # Exhaust all 5-element integer subsets of [0,9] for the sharp
    # additive-energy bound and for Cauchy-Schwarz pair-match bound.
    sets=list(itertools.combinations(range(10),5))
    cnt=Counter(energy(s) for s in sets)
    assert max(cnt)==16
    max_matching=0
    for a in sets:
        ca=pair_counts(a)
        for b in sets:
            cb=pair_counts(b)
            max_matching=max(max_matching,sum(v*cb[s] for s,v in ca.items()))
    assert max_matching==16
    rng=random.Random(20261018)
    circle_tests=0
    states=0
    worst_blockers=0
    worst_e=0
    for case in range(36):
        # Non-equidistant columns and generally nonaligned, irregular sites.
        x0=0
        x1=rng.randint(1,5)
        x2=x1+rng.randint(1,6)
        columns={x:tuple(sorted(rng.sample(range(-6,15),5))) for x in (x0,x1,x2)}
        brute=circle_pairs_brute(columns)
        by_sum=circle_pairs_via_sums(columns)
        assert brute==by_sum, (columns,brute,by_sum)
        circle_tests+=1
        for target in columns:
            for _ in range(3):
                occupied={x:tuple(sorted(rng.sample(columns[x],rng.randrange(0,6)))) for x in columns}
                occupied[target]=tuple(sorted(rng.sample(columns[target],rng.randrange(0,5))))
                # Only safe states have well-defined legal blockers.
                full=[(x,y) for x,ys in occupied.items() for y in ys]
                if any(is_cocircular_six(six) for six in itertools.combinations(full,6)):
                    continue
                e,blocked,a=bound_one_state(columns,target,occupied)
                assert blocked<=e<=16
                assert a+blocked<=a+e<=20
                states+=1
                worst_blockers=max(worst_blockers,blocked)
                worst_e=max(worst_e,e)
    # Known 3x8 extremal deficient terminal position.  All four missing
    # target sites are blocked, so the audit exercises positive blockers.
    witness_columns={0:tuple(range(8)),1:tuple(range(8)),2:tuple(range(8))}
    witness_occupied={0:(0,2,3,7),1:(0,2,3,5,6),2:(0,2,3,4,5)}
    e, blocked, a=bound_one_state(witness_columns,0,witness_occupied)
    assert (a,blocked)==(4,4), (a,blocked)
    assert blocked<=e<=16
    # Every occupied six-set is safe, and every target addition is unsafe.
    full=[(x,y) for x,ys in witness_occupied.items() for y in ys]
    assert not any(is_cocircular_six(six) for six in itertools.combinations(full,6))
    result={
        'positive_blocker_regression':{'board':'3x8','target_occupied':a,'blocked_target_sites':blocked,'pair_matching_bound':e},
        'five_point_subsets_tested':len(sets),
        'five_point_energy_histogram':dict(sorted(cnt.items())),
        'maximum_energy':max(cnt),
        'ordered_pair_of_five_sets_tested':len(sets)**2,
        'maximum_matching_pair_count':max_matching,
        'independent_determinant_geometry_cases':circle_tests,
        'independent_safe_state_blocker_checks':states,
        'largest_blocker_count_in_samples':worst_blockers,
        'largest_matching_pair_count_in_samples':worst_e,
        'universal_threshold_per_line':21,
        'proof_scope':'any three distinct parallel lines, arbitrary finite site sets of at least 21 points each; q=6 complete-call normal play'
    }
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return result

if __name__=='__main__':
    main()
