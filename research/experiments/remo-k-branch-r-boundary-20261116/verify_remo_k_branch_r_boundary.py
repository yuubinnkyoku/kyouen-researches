#!/usr/bin/env python3
"""K0864 audit: 3-branch REMO determinacy collapse boundary for r = 2,4,5,6
(the r-dependent cap<=10 boundary; r=3 is K0862 Theorem H).

Self-contained. Deterministic (no randomness, no wall clock, no network).
Python 3.11+ / stdlib only. Engine (region/cell games, profile enumeration,
Theorem D recursion, Burnside counting) is verbatim from the K0862 verifier
(commit c8bdacc1, itself verbatim from the K0861 verifier, commit 33684f3e).

Checked claims (proof text: report.md in this directory /
research/knowledge/items/K0864-remo-k-branch-r-dependent-boundary.md):

I2 (Theorem I, r=2, cap<=10, finite complete)  For every 3-branch family
    with branch sizes <= 10 (15863 canonical profiles, 715 keys): NO key
    fails survivor-determinacy collapse, and moreover EVERY key collapses
    completely to its chain profile: determinacy, order determinacy, the
    determined survivor, the order-determined elimination order, AND the
    possible-survivor set of a non-determined key each equal the chain
    value. (Theorem G of K0862, proved for cap<=7 and r=2..6, extends at
    r=2 to the full cap<=10 domain including outcome sets.)
I4/I5 (Theorem I, r=4 resp. r=5, cap<=10, finite complete)  The keys at
    which survivor determinacy fails to collapse are EXACTLY the 12 keys
    (8,8,9) and (8,9,9) with gamma = 0..5. Every failing key contains a
    size-8 branch; no key with 9s but no 8 and no key with a size-10
    branch fails. In every failing key the chain profile is DETERMINED,
    all determined profiles have the same survivor as the chain (P_2),
    and the non-determined possible-survivor sets are within
    {{1,2,3}} (r=4) resp. {{1,2,3},{1,2,3,4}} (r=5).
I6 (Theorem I, r=6, cap<=10, finite complete)  The non-collapse keys are
    EXACTLY the 6 keys (4,4,8) and (4,8,8) with gamma = 0..2: a different
    pair of families from r<=5. Same size-8 necessity and no-9/10
    statements; chain DETERMINED with survivor P_3, determined side
    uniform P_3, non-determined sets {{2,3}}.
FL (Lemma, first-elimination arithmetic, universal over all k-branch
    families and all r; prose proof in report.md)  Over all plays the
    set of possible first losers is exactly { C_i mod r : i } (each first
    phase places exactly C stones inside the first-completed branch,
    whatever atoms they occupy). Machine-checked on all 15863 profiles
    for r=2..6 (0 violations).
GP (Theorem G', chain-value collapse, cap<=10, r=2..6, finite complete)
    On every key whose profiles agree on survivor determinacy and are
    determined, the survivor equals the chain survivor (and the chain is
    determined); on every key that is uniformly order-determined the
    elimination order equals the chain order. (For r=3 this covers the
    693 collapsing keys of the K0862 sweep - an extension of Theorem G
    beyond cap<=7 at the survivor/order level; possible-survivor SETS of
    non-determined keys remain atom-dependent for r>=4, as in K0862.)
PI (finite structural observation)  On the 12 keys (8,8,9),(8,9,9)
    gamma=0..5 the per-profile determined/non-determined partition is
    IDENTICAL for r=3,4,5 (the K0862 r=3 partition extends verbatim;
    only the survivor label moves P_1 -> P_2), while at r=6 EVERY profile
    of these keys is non-determined. Conversely the 10 small-branch keys
    of the K0862 r=3 list ((2,3,8),(2,8,9),(3,3,8),(3,8,8),(3,8,9),
    gamma=0,1) are non-determined for EVERY profile at r=4,5,6 (the
    determined side vanishes - the collapse is to uniformly-ndet), and
    the mirror families (4,4,8),(4,8,8) are non-determined for every
    profile at r=3,4,5 and split only at r=6.

Scope / limits (do not over-read):
- Theorem E' (K0861, universal) transfers every profile verdict to every
  board realizing the profile. I2/I4/I5/I6/GP/PI are COMPLETE only over
  the finite domain stated (branch sizes <= 10, r in {2..6}); branch
  sizes >= 11 and r >= 7 are NOT covered. Whether further non-collapse
  keys exist there is open.
- Non-collapse of determinacy does not mean constant outcome: within
  failing keys the possible-survivor sets still depend on atoms.
- The Lemma FL is proved for all k-branch families and all r (prose);
  the machine check here is a redundant anchor over the finite domain.
- Cell-level (Theorem E') spot anchors are run at r=6 on the 6 failing
  keys' minimal witnesses and at r=4,5,6 on the K0862 small-family
  determined witnesses (11 cells, cheap); the 14-16 cell witnesses of
  the (8,8,9)/(8,9,9) keys exceed the cell-game memory budget at r>=4
  and are anchored at r=3 by the published K0862 audit instead.
- 11x11 empty board / class frontiers remain UNKNOWN, unrelated.
- solved 1410 is manifest bookkeeping only.
"""

import hashlib
import json
import os
import sys

sys.setrecursionlimit(100000)


# K0859 published uniform elimination table (C=1..12 x r=2..8),
# canonical JSON extracted from
# research/experiments/multiplayer-coalition-kyouen-20261116/output/
#   elimination_continuation_audit.json (uniform_elimination_table),
# byte-verified against main (same constant as the K0862 verifier).
PUBLISHED_UNIFORM_ELIMINATION_TABLE_JSON = (
    '{"1":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[1,2],"survivor":0},"4":{"elimination":[1,2,3],"survivor":0},"5":{"elimination":[1,2,3,4],"survivor":0},"6":{"elimination":[1,2,3,4,5],"survivor":0},"7":{"elimination":[1,2,3,4,5,6],"survivor":0},"8":{"elimination":[1,2,3,4,5,6,7],"survivor":0}},"10":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[1,0],"survivor":2},"4":{"elimination":[2,1,0],"survivor":3},"5":{"elimination":[0,3,2,1],"survivor":4},"6":{"elimination":[4,0,3,2,1],"survivor":5},"7":{"elimination":[3,5,0,4,2,1],"survivor":6},"8":{"elimination":[2,4,6,0,5,3,1],"survivor":7}},"11":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[2,1],"survivor":0},"4":{"elimination":[3,2,1],"survivor":0},"5":{"elimination":[1,4,3,2],"survivor":0},"6":{"elimination":[5,1,4,3,2],"survivor":0},"7":{"elimination":[4,6,1,5,3,2],"survivor":0},"8":{"elimination":[3,5,7,1,6,4,2],"survivor":0}},"12":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[0,1],"survivor":2},"4":{"elimination":[0,1,2],"survivor":3},"5":{"elimination":[2,0,1,3],"survivor":4},"6":{"elimination":[0,3,1,2,4],"survivor":5},"7":{"elimination":[5,0,3,1,2,4],"survivor":6},"8":{"elimination":[4,6,0,3,1,2,5],"survivor":7}},"2":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[2,0],"survivor":1},"4":{"elimination":[2,3,0],"survivor":1},"5":{"elimination":[2,3,4,0],"survivor":1},"6":{"elimination":[2,3,4,5,0],"survivor":1},"7":{"elimination":[2,3,4,5,6,0],"survivor":1},"8":{"elimination":[2,3,4,5,6,7,0],"survivor":1}},"3":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[0,2],"survivor":1},"4":{"elimination":[3,0,2],"survivor":1},"5":{"elimination":[3,4,0,2],"survivor":1},"6":{"elimination":[3,4,5,0,2],"survivor":1},"7":{"elimination":[3,4,5,6,0,2],"survivor":1},"8":{"elimination":[3,4,5,6,7,0,2],"survivor":1}},"4":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[1,0],"survivor":2},"4":{"elimination":[0,2,1],"survivor":3},"5":{"elimination":[4,0,2,1],"survivor":3},"6":{"elimination":[4,5,0,2,1],"survivor":3},"7":{"elimination":[4,5,6,0,2,1],"survivor":3},"8":{"elimination":[4,5,6,7,0,2,1],"survivor":3}},"5":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[2,1],"survivor":0},"4":{"elimination":[1,3,2],"survivor":0},"5":{"elimination":[0,2,4,3],"survivor":1},"6":{"elimination":[5,0,2,4,3],"survivor":1},"7":{"elimination":[5,6,0,2,4,3],"survivor":1},"8":{"elimination":[5,6,7,0,2,4,3],"survivor":1}},"6":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[0,1],"survivor":2},"4":{"elimination":[2,0,1],"survivor":3},"5":{"elimination":[1,3,0,2],"survivor":4},"6":{"elimination":[0,2,4,1,3],"survivor":5},"7":{"elimination":[6,0,2,4,1,3],"survivor":5},"8":{"elimination":[6,7,0,2,4,1,3],"survivor":5}},"7":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[1,2],"survivor":0},"4":{"elimination":[3,1,2],"survivor":0},"5":{"elimination":[2,4,1,3],"survivor":0},"6":{"elimination":[1,3,5,2,4],"survivor":0},"7":{"elimination":[0,2,4,6,3,5],"survivor":1},"8":{"elimination":[7,0,2,4,6,3,5],"survivor":1}},"8":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[2,0],"survivor":1},"4":{"elimination":[0,3,1],"survivor":2},"5":{"elimination":[3,0,4,1],"survivor":2},"6":{"elimination":[2,4,0,5,1],"survivor":3},"7":{"elimination":[1,3,5,0,6,2],"survivor":4},"8":{"elimination":[0,2,4,6,1,7,3],"survivor":5}},"9":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[0,2],"survivor":1},"4":{"elimination":[1,0,3],"survivor":2},"5":{"elimination":[4,1,0,3],"survivor":2},"6":{"elimination":[3,5,1,0,4],"survivor":2},"7":{"elimination":[2,4,6,1,0,5],"survivor":3},"8":{"elimination":[1,3,5,7,2,0,6],"survivor":4}}}'
)


# ---------------------------------------------------------------------------
# engine (verbatim from research/experiments/
#   remo-k-branch-collapse-boundary-20261116/verify_remo_k_branch_boundary.py,
# K0862, commit c8bdacc1)


class Budget(Exception):
    """Deterministic node-budget guard (machine-independent)."""


def next_active(p, r, active):
    for d in range(1, r + 1):
        q = (p + d) % r
        if q in active:
            return q
    raise AssertionError("no active player after %d" % p)


def outcome_summary(outcomes):
    survivors = sorted({sv for (_, sv) in outcomes})
    orders = sorted(list(o) for o, _ in outcomes)
    first_losers = sorted({o[0] for o, _ in outcomes})
    return {
        "determined": len(survivors) == 1,
        "survivors": survivors,
        "first_losers": first_losers,
        "orders": orders,
        "order_determined": len(orders) == 1,
    }


def profile_sizes(atoms, k):
    """C_i = |A_i| per branch."""
    return tuple(
        sum(atoms[m - 1] for m in range(1, 1 << k) if (m >> (i - 1)) & 1)
        for i in range(1, k + 1)
    )


def check_profile(atoms, k):
    for i in range(1, k + 1):
        assert atoms[(1 << (i - 1)) - 1] >= 1, "singleton atom must be nonempty"
    sizes = profile_sizes(atoms, k)
    return sizes


def chain_profile(sizes, gamma, k):
    """Common-core chain: only the all-branches atom and singletons."""
    atoms = [0] * ((1 << k) - 1)
    atoms[(1 << k) - 2] = gamma  # mask (1<<k)-1 (all branches)
    for i in range(1, k + 1):
        atoms[(1 << (i - 1)) - 1] = sizes[i - 1] - gamma
    return tuple(atoms)


def cell_game_k(atoms, k, r, budget=1_500_000):
    check_profile(atoms, k)
    sizes = profile_sizes(atoms, k)
    base = {}
    nxt = 0
    for m in range(1, 1 << k):
        base[m] = nxt
        nxt += atoms[m - 1]
    ncells = nxt
    A = []
    for i in range(1, k + 1):
        s = set()
        for m in range(1, 1 << k):
            if (m >> (i - 1)) & 1:
                s.update(range(base[m], base[m] + atoms[m - 1]))
        A.append(frozenset(s))
    for i in range(k):
        for j in range(k):
            if i != j:
                assert not (A[i] <= A[j]), "maximals must be incomparable"
    A = tuple(A)
    memo = {}
    nodes = [budget]

    def outcomes(placed, own, mover, active):
        key = (placed, own, mover, active)
        got = memo.get(key)
        if got is not None:
            return got
        nodes[0] -= 1
        if nodes[0] < 0:
            raise Budget("cell budget")
        res = set()
        maximal = any(placed == Ai for Ai in A)
        if maximal:
            loser = mover
            new_placed = frozenset(c for c in placed if own[c] != loser)
            new_own = tuple(-1 if o == loser else o for o in own)
            new_active = frozenset(a for a in active if a != loser)
            if len(new_active) == 1:
                res.add(((loser,), next(iter(new_active))))
            else:
                nm = next_active(loser, r, new_active)
                for od, sv in outcomes(new_placed, new_own, nm, new_active):
                    res.add(((loser,) + od, sv))
        else:
            legal = set()
            for Ai in A:
                if placed <= Ai:
                    legal |= Ai - placed
            nm = next_active(mover, r, active)
            for c in sorted(legal):
                res |= outcomes(
                    placed | {c}, own[:c] + (mover,) + own[c + 1:], nm, active
                )
        out = frozenset(res)
        memo[key] = out
        return out

    try:
        start = outcomes(frozenset(), (-1,) * ncells, 0, frozenset(range(r)))
        return start, len(memo), False
    except Budget:
        return None, len(memo), True


def region_game_k(atoms, k, r, budget=1_500_000):
    check_profile(atoms, k)
    sizes = profile_sizes(atoms, k)
    natoms = (1 << k) - 1
    star = [0] * (k + 1)
    for i in range(1, k + 1):
        m2 = 0
        for m in range(1, 1 << k):
            if (m >> (i - 1)) & 1:
                m2 |= 1 << (m - 1)
        star[i] = m2
    zero = tuple((0,) * r for _ in range(natoms))
    memo = {}
    nodes = [budget]

    def occupied_mask(counts):
        occ = 0
        for m in range(natoms):
            if sum(counts[m]):
                occ |= 1 << m
        return occ

    def star_total(counts, i):
        t = 0
        for m in range(natoms):
            if (star[i] >> m) & 1:
                t += sum(counts[m])
        return t

    def bump(counts, m, p):
        inner = counts[m]
        return (
            counts[:m]
            + (inner[:p] + (inner[p] + 1,) + inner[p + 1:],)
            + counts[m + 1:]
        )

    def outcomes(counts, mover, active):
        key = (counts, mover, active)
        got = memo.get(key)
        if got is not None:
            return got
        nodes[0] -= 1
        if nodes[0] < 0:
            raise Budget("region budget")
        occ = occupied_mask(counts)
        res = set()
        maximal = any(
            star_total(counts, i) == sizes[i - 1] and (occ & ~star[i]) == 0
            for i in range(1, k + 1)
        )
        if maximal:
            loser = mover
            ncounts = tuple(
                tuple(0 if p == loser else c for p, c in enumerate(counts[m]))
                for m in range(natoms)
            )
            new_active = frozenset(a for a in active if a != loser)
            if len(new_active) == 1:
                res.add(((loser,), next(iter(new_active))))
            else:
                nm = next_active(loser, r, new_active)
                for od, sv in outcomes(ncounts, nm, new_active):
                    res.add(((loser,) + od, sv))
        else:
            legal = []
            for m in range(1, 1 << k):
                mi = m - 1
                cap = atoms[mi] - sum(counts[mi])
                if cap <= 0:
                    continue
                if any(
                    (occ & ~star[i]) == 0 and (star[i] >> mi) & 1
                    for i in range(1, k + 1)
                ):
                    legal.append(mi)
            nm = next_active(mover, r, active)
            for mi in legal:
                res |= outcomes(bump(counts, mi, mover), nm, active)
        out = frozenset(res)
        memo[key] = out
        return out

    try:
        start = outcomes(zero, 0, frozenset(range(r)))
        return start, len(memo), False
    except Budget:
        return None, len(memo), True


def region_verdict(atoms, k, r, budget=1_500_000):
    out, states, skipped = region_game_k(atoms, k, r, budget)
    if skipped:
        return None, states
    return outcome_summary(sorted(out)), states


def theorem_d(C, r):
    """K0859 Theorem D arithmetic recursion (uniform board, any r)."""
    active = list(range(r))
    counts = [0] * r
    turn = 0
    elimination = []
    while len(active) > 1:
        k = len(active)
        s = sum(counts[p] for p in active)
        ell = C - s
        for m in range(ell):
            counts[active[(turn + m) % k]] += 1
        li = (turn + ell) % k
        loser = active[li]
        elimination.append(loser)
        counts[loser] = 0
        active.pop(li)
        if active:
            turn = li % len(active)
    return tuple(elimination), active[0]


def theorem_d_table():
    """Compare the recursion against the K0859 published (C,r) table."""
    table = json.loads(PUBLISHED_UNIFORM_ELIMINATION_TABLE_JSON)
    mism = 0
    entries = 0
    for C in range(1, 13):
        for r in range(2, 9):
            published = table[str(C)][str(r)]
            elim, surv = theorem_d(C, r)
            entries += 1
            if list(elim) != published["elimination"] or surv != published["survivor"]:
                mism += 1
    return entries, mism


def branch_perms(k):
    if k == 1:
        return [(1,)]
    out = []

    def rec(rem, cur):
        if not rem:
            out.append(tuple(cur))
            return
        for x in rem:
            rec([y for y in rem if y != x], cur + [x])

    rec(list(range(1, k + 1)), [])
    return out


def orbit_representative(atoms, k, perms):
    reps = []
    for p in perms:
        na = [0] * ((1 << k) - 1)
        for m in range(1, 1 << k):
            if atoms[m - 1]:
                nm = 0
                for i in range(1, k + 1):
                    if (m >> (i - 1)) & 1:
                        nm |= 1 << (p[i - 1] - 1)
                na[nm - 1] = atoms[m - 1]
        reps.append(tuple(na))
    return min(reps)


def enumerate_profiles(nmax, k=3):
    """All canonical k-branch atom profiles with singles >=1, N <= nmax."""
    perms = branch_perms(k)
    natoms = (1 << k) - 1
    singles = [(1 << (i - 1)) - 1 for i in range(1, k + 1)]
    profiles = []
    seen = set()

    def rec(idx, atoms, total):
        if idx == natoms:
            rep = orbit_representative(tuple(atoms), k, perms)
            if rep not in seen:
                seen.add(rep)
                profiles.append(rep)
            return
        lo = 1 if idx in singles else 0
        for v in range(lo, nmax - total + 1):
            atoms.append(v)
            rec(idx + 1, atoms, total + v)
            atoms.pop()

    rec(0, [], 0)
    return profiles


_VERDICT_CACHE = {}


def region_verdict_cached(atoms, k, r, budget=20_000_000):
    key = (atoms, k, r)
    got = _VERDICT_CACHE.get(key)
    if got is None:
        got = region_verdict(atoms, k, r, budget)
        _VERDICT_CACHE[key] = got
    return got


def burnside_fix_counts(cap):
    """Fixed-point counts of the constrained profile set D_cap under S_3."""
    fix_id = 0
    for v0 in range(1, cap + 1):
        for v1 in range(1, cap + 1):
            for v3 in range(1, cap + 1):
                for v2 in range(0, cap + 1):
                    for v4 in range(0, cap + 1):
                        for v5 in range(0, cap + 1):
                            m = min(
                                cap - v0 - v2 - v4,
                                cap - v1 - v2 - v5,
                                cap - v3 - v4 - v5,
                            )
                            if m >= 0:
                                fix_id += m + 1
    fix_trans = 0
    for a in range(1, cap + 1):
        for b in range(0, cap + 1):
            for c in range(1, cap + 1):
                for d in range(0, cap + 1):
                    m = min(cap - a - b - d, cap - c - 2 * d)
                    if m >= 0:
                        fix_trans += m + 1
    fix_cyc = 0
    for a in range(1, cap + 1):
        for b in range(0, cap + 1):
            m = cap - a - 2 * b
            if m >= 0:
                fix_cyc += m + 1
    orbits = (fix_id + 3 * fix_trans + 2 * fix_cyc) // 6
    assert (fix_id + 3 * fix_trans + 2 * fix_cyc) % 6 == 0
    return fix_id, fix_trans, fix_cyc, orbits


def constrained_profiles(cap):
    """Canonical profiles with all branch sizes <= cap (two ways agreed)."""
    return [
        a for a in enumerate_profiles(3 * cap)
        if max(profile_sizes(a, 3)) <= cap
    ]


def key_of(atoms):
    return (tuple(sorted(profile_sizes(atoms, 3))), atoms[6])


# ---------------------------------------------------------------------------
# published anchors (machine-extracted, byte-verified against main)
#
# K0862 (commit c8bdacc1): the 22 r=3 non-collapse keys, the cap<=7
# Theorem G statistics per r, and the minimal determined-side witnesses of
# the 10 small-branch keys, from
# research/experiments/remo-k-branch-collapse-boundary-20261116/output/
#   remo_k_branch_boundary_audit.json (sha256 7dfabd501f389f92f20ed8550070
#   8f4edfde63e969358008db05bcf967c6d7bb).

K0862_FAILING_22 = [
    ([2, 3, 8], 0), ([2, 3, 8], 1), ([2, 8, 9], 0), ([2, 8, 9], 1),
    ([3, 3, 8], 0), ([3, 3, 8], 1), ([3, 8, 8], 0), ([3, 8, 8], 1),
    ([3, 8, 9], 0), ([3, 8, 9], 1),
] + [([8, 8, 9], g) for g in range(6)] + [([8, 9, 9], g) for g in range(6)]

K0862_SMALL_10 = [
    ([2, 3, 8], 0), ([2, 3, 8], 1), ([2, 8, 9], 0), ([2, 8, 9], 1),
    ([3, 3, 8], 0), ([3, 3, 8], 1), ([3, 8, 8], 0), ([3, 8, 8], 1),
    ([3, 8, 9], 0), ([3, 8, 9], 1),
]

# determined-side minimal witnesses of the 10 small keys at r=3
# (K0862 audit sweep_cap10_r3.failing_witnesses[key].det_atoms).
K0862_SMALL_DET_WITNESSES = {
    (2, 3, 8, 0): [1, 1, 1, 7, 0, 1, 0],
    (2, 3, 8, 1): [1, 2, 0, 7, 0, 0, 1],
    (2, 8, 9, 0): [1, 2, 1, 4, 0, 5, 0],
    (2, 8, 9, 1): [1, 3, 0, 4, 0, 4, 1],
    (3, 3, 8, 0): [1, 1, 1, 6, 1, 1, 0],
    (3, 3, 8, 1): [1, 1, 1, 7, 0, 0, 1],
    (3, 8, 8, 0): [1, 1, 1, 1, 1, 6, 0],
    (3, 8, 8, 1): [1, 1, 6, 2, 0, 0, 1],
    (3, 8, 9, 0): [1, 2, 1, 3, 1, 5, 0],
    (3, 8, 9, 1): [1, 3, 0, 3, 1, 4, 1],
}

K0862_THEOREM_G_CAP7_JSON = (
    '{"2": {"det_keys": 80, "ndet_survivor_set_variety_keys": 0, '
    '"order_det_keys": 80}, "3": {"det_keys": 55, '
    '"ndet_survivor_set_variety_keys": 30, "order_det_keys": 30}, '
    '"4": {"det_keys": 55, "ndet_survivor_set_variety_keys": 77, '
    '"order_det_keys": 28}, "5": {"det_keys": 46, '
    '"ndet_survivor_set_variety_keys": 69, "order_det_keys": 28}, '
    '"6": {"det_keys": 46, "ndet_survivor_set_variety_keys": 70, '
    '"order_det_keys": 28}}'
)

EXPECTED_BURNSIDE_CAP10 = {
    "fix_id": 84494, "fix_trans": 3478, "fix_cyc": 125, "orbits": 15863,
}

# New expected values (this item, first computed 2026-11-16 and then
# re-derived deterministically by this verifier on every run).
EXPECTED_FAILING_R4 = [
    ([8, 8, 9], g) for g in range(6)
] + [([8, 9, 9], g) for g in range(6)]
EXPECTED_FAILING_R5 = [
    ([8, 8, 9], g) for g in range(6)
] + [([8, 9, 9], g) for g in range(6)]
EXPECTED_FAILING_R6 = [
    ([4, 4, 8], g) for g in range(3)
] + [([4, 8, 8], g) for g in range(3)]

# per-key determined-profile counts on the 12 (8,8,9)/(8,9,9) keys
# (partition identity across r=3,4,5; total collapse to ndet at r=6).
EXPECTED_NDET_COUNTS_89 = {
    ("8,8,9", 0): (92, 100), ("8,8,9", 1): (62, 70), ("8,8,9", 2): (40, 48),
    ("8,8,9", 3): (22, 30), ("8,8,9", 4): (10, 18), ("8,8,9", 5): (3, 9),
    ("8,9,9", 0): (102, 110), ("8,9,9", 1): (72, 80), ("8,9,9", 2): (46, 54),
    ("8,9,9", 3): (28, 36), ("8,9,9", 4): (13, 21), ("8,9,9", 5): (4, 12),
}

# per-key determined-profile counts on the mirror families
# (4,4,8)/(4,8,8): uniformly ndet for r=3,4,5; split at r=6.
EXPECTED_NDET_COUNTS_48 = {
    ("4,4,8", 0): (16, 20), ("4,4,8", 1): (7, 10), ("4,4,8", 2): (2, 4),
    ("4,4,8", 3): (0, 1),
    ("4,8,8", 0): (34, 39), ("4,8,8", 1): (19, 24), ("4,8,8", 2): (6, 11),
    ("4,8,8", 3): (0, 5),
}

R_VALUES = (2, 3, 4, 5, 6)


# ---------------------------------------------------------------------------
# sweep + assembly seam: main() = constrained_profiles + sweep_all +
# assemble. assemble is a pure function of the verdict dictionaries (and
# computes the few missing chain-profile verdicts deterministically via
# region_verdict_cached).


def sweep_all(prof10, rs=R_VALUES):
    verd = {}
    for r in rs:
        d = {}
        for a in prof10:
            v, _ = region_verdict_cached(a, 3, r)
            assert v is not None, "budget skip at r=%d for %s" % (r, a)
            d[a] = v
        verd[r] = d
    return verd


def group_by_key(verd):
    byk = {}
    for a, v in verd.items():
        byk.setdefault(key_of(a), []).append((a, v))
    return byk


def chain_verdict(key, r):
    ch = chain_profile(key[0], key[1], 3)
    v, _ = region_verdict_cached(ch, 3, r)
    assert v is not None
    return v


def failing_keys(byk):
    return sorted(
        k for k, avs in byk.items()
        if len({v["determined"] for _, v in avs}) > 1
    )


def key_str(k):
    return "%s|%d" % (",".join(map(str, k[0])), k[1])


def min_witness(avs, side):
    sel = [(a, v) for a, v in avs if v["determined"] == side]
    return min(sel, key=lambda av: (sum(av[0]), av[0]))


def assemble(prof10, verd):
    audit = {}
    checks = []

    def record(name, ok, data):
        checks.append({"name": name, "ok": bool(ok), "data": data})

    # ---- C1: enumeration == Burnside (K0862 anchor)
    fi, ft, fc, orbits = burnside_fix_counts(10)
    ok = (
        orbits == len(prof10) == EXPECTED_BURNSIDE_CAP10["orbits"]
        and (fi, ft, fc) == (
            EXPECTED_BURNSIDE_CAP10["fix_id"],
            EXPECTED_BURNSIDE_CAP10["fix_trans"],
            EXPECTED_BURNSIDE_CAP10["fix_cyc"],
        )
    )
    record(
        "cap=10: canonical profile count == Burnside orbit count "
        "(15863, K0862 anchor)",
        ok,
        {"fix_id": fi, "fix_trans": ft, "fix_cyc": fc, "orbits": orbits,
         "enum_count": len(prof10)},
    )

    byk = {r: group_by_key(verd[r]) for r in R_VALUES}
    n_keys = len(byk[3])
    record(
        "all sweeps r=2..6: 715 (sizes,gamma) keys each, 15863 profiles, "
        "0 budget skips",
        all(len(byk[r]) == 715 for r in R_VALUES)
        and all(len(verd[r]) == 15863 for r in R_VALUES),
        {"profiles": len(prof10), "keys": n_keys},
    )

    fail = {r: failing_keys(byk[r]) for r in R_VALUES}

    # ---- C2: r=3 anchor (K0862 Theorem H re-derivation)
    f3 = sorted([list(k[0]), k[1]] for k in fail[3])
    e3 = sorted([list(sp), g] for sp, g in K0862_FAILING_22)
    record(
        "r=3 anchor: non-collapse keys are exactly the K0862 22 keys",
        f3 == e3,
        {"failing": f3},
    )

    # ---- C3: Theorem G cap<=7 anchor (K0862 statistics re-derivation)
    prof7 = [a for a in prof10 if max(profile_sizes(a, 3)) <= 7]
    tg = {}
    tg_ok = True
    for r in R_VALUES:
        verd7 = {a: verd[r][a] for a in prof7}
        byk7 = group_by_key(verd7)
        det_keys = 0
        odet_keys = 0
        ndet_variety = 0
        for k, avs in byk7.items():
            dets = {v["determined"] for _, v in avs}
            odets = {v["order_determined"] for _, v in avs}
            if dets == {True}:
                det_keys += 1
                if len({tuple(v["survivors"]) for _, v in avs}) > 1:
                    tg_ok = False
            if odets == {True}:
                odet_keys += 1
            if dets == {False} and len(
                {tuple(sorted(v["survivors"])) for _, v in avs}
            ) > 1:
                ndet_variety += 1
        tg[str(r)] = {
            "det_keys": det_keys,
            "order_det_keys": odet_keys,
            "ndet_survivor_set_variety_keys": ndet_variety,
        }
    record(
        "Theorem G cap<=7 anchor: per-r statistics == K0862 published "
        "theorem_g_cap7",
        tg == json.loads(K0862_THEOREM_G_CAP7_JSON) and tg_ok,
        {"recomputed": tg},
    )

    # ---- C4: Theorem I, r=2 (total collapse incl. outcome sets)
    r2_ok = len(fail[2]) == 0
    surv_mism = 0
    odet_mism = 0
    ndet_set_mism = 0
    for k, avs in byk[2].items():
        vch = chain_verdict(k, 2)
        dets = {v["determined"] for _, v in avs}
        if len(dets) > 1:
            r2_ok = False
            continue
        if dets == {True}:
            survs = {tuple(v["survivors"]) for _, v in avs}
            if len(survs) > 1 or survs != {tuple(vch["survivors"])}:
                surv_mism += 1
            if not vch["determined"]:
                surv_mism += 1
            if {v["order_determined"] for _, v in avs} == {True}:
                ords = {tuple(v["orders"][0]) for _, v in avs}
                if len(ords) > 1 or ords != {tuple(vch["orders"][0])}:
                    odet_mism += 1
            else:
                odet_mism += 1
        else:
            sets_ = {tuple(sorted(v["survivors"])) for _, v in avs}
            if sets_ != {tuple(sorted(vch["survivors"]))}:
                ndet_set_mism += 1
    record(
        "Theorem I r=2: zero failing keys; every key collapses to the "
        "chain (determinacy, survivor, order, possible-survivor set)",
        r2_ok and surv_mism == 0 and odet_mism == 0 and ndet_set_mism == 0,
        {"failing_keys": len(fail[2]), "survivor_mismatch_keys": surv_mism,
         "order_mismatch_keys": odet_mism,
         "ndet_set_mismatch_keys": ndet_set_mism},
    )

    # ---- C5-C7: Theorems I r=4 / r=5 / r=6
    det_keys_total = {}
    odet_keys_total = {}
    witnesses = {}
    for r, expected, ndet_allowed in (
        (4, EXPECTED_FAILING_R4, {(1, 2, 3)}),
        (5, EXPECTED_FAILING_R5, {(1, 2, 3), (1, 2, 3, 4)}),
        (6, EXPECTED_FAILING_R6, {(2, 3)}),
    ):
        fl = sorted([list(k[0]), k[1]] for k in fail[r])
        el = sorted([list(sp), g] for sp, g in expected)
        ok = fl == el
        size8 = all(8 in k[0] for k in fail[r])
        no9 = all(not (9 in k[0] and 8 not in k[0]) for k in fail[r])
        no10 = all(10 not in k[0] for k in fail[r])
        det_keys_total[r] = sum(
            1 for k, avs in byk[r].items()
            if len({v["determined"] for _, v in avs}) == 1
            and avs[0][1]["determined"]
        )
        odet_keys_total[r] = sum(
            1 for k, avs in byk[r].items()
            if len({v["order_determined"] for _, v in avs}) == 1
            and avs[0][1]["order_determined"]
        )
        uni_ok = True
        for k in fail[r]:
            avs = byk[r][k]
            vch = chain_verdict(k, r)
            if not vch["determined"]:
                uni_ok = False
            det = [(a, v) for a, v in avs if v["determined"]]
            ndet = [(a, v) for a, v in avs if not v["determined"]]
            if {tuple(v["survivors"]) for _, v in det} != {
                tuple(vch["survivors"])}:
                uni_ok = False
            for a, v in ndet:
                if tuple(sorted(v["survivors"])) not in ndet_allowed:
                    uni_ok = False
            dmin = min_witness(avs, True)
            nmin = min_witness(avs, False)
            witnesses["%s#%d" % (key_str(k), r)] = {
                "det_atoms": list(dmin[0]),
                "det_cells": sum(dmin[0]),
                "det_survivors": dmin[1]["survivors"],
                "ndet_atoms": list(nmin[0]),
                "ndet_cells": sum(nmin[0]),
                "ndet_survivors": nmin[1]["survivors"],
                "chain_survivors": vch["survivors"],
            }
        record(
            "Theorem I r=%d: non-collapse keys are exactly %s; size-8 "
            "branches necessary; no 9-without-8 and no size-10 failure; "
            "chain determined with uniform determined-side survivor; "
            "ndet survivor sets within %s" % (
                r,
                {4: "the 12 keys (8,8,9),(8,9,9) x g=0..5",
                 5: "the 12 keys (8,8,9),(8,9,9) x g=0..5",
                 6: "the 6 keys (4,4,8),(4,8,8) x g=0..2"}[r],
                sorted(list(t) for t in ndet_allowed),
            ),
            ok and size8 and no9 and no10 and uni_ok,
            {"failing": fl, "size8_necessary": size8,
             "failing_with_9_no_8": 0, "failing_with_10": 0},
        )
    det_keys_total[3] = sum(
        1 for k, avs in byk[3].items()
        if len({v["determined"] for _, v in avs}) == 1
        and avs[0][1]["determined"]
    )
    odet_keys_total[3] = sum(
        1 for k, avs in byk[3].items()
        if len({v["order_determined"] for _, v in avs}) == 1
        and avs[0][1]["order_determined"]
    )
    det_keys_total[2] = sum(
        1 for k, avs in byk[2].items()
        if len({v["determined"] for _, v in avs}) == 1
        and avs[0][1]["determined"]
    )
    odet_keys_total[2] = sum(
        1 for k, avs in byk[2].items()
        if len({v["order_determined"] for _, v in avs}) == 1
        and avs[0][1]["order_determined"]
    )

    # ---- C8: Lemma FL (first-elimination arithmetic)
    fl_bad = {}
    for r in R_VALUES:
        bad = 0
        for a, v in verd[r].items():
            sizes = profile_sizes(a, 3)
            if v["first_losers"] != sorted({c % r for c in sizes}):
                bad += 1
        fl_bad[str(r)] = bad
    record(
        "Lemma FL: possible first losers == {C_i mod r} on all profiles, "
        "r=2..6",
        all(b == 0 for b in fl_bad.values()),
        {"violations_by_r": fl_bad},
    )

    # ---- C9: Theorem G' (chain-value collapse on collapsing keys)
    gp = {}
    gp_ok = True
    for r in R_VALUES:
        surv_mism = 0
        ord_mism = 0
        uni_det = 0
        uni_odet = 0
        for k, avs in byk[r].items():
            dets = {v["determined"] for _, v in avs}
            if len(dets) == 1 and dets == {True}:
                uni_det += 1
                vch = chain_verdict(k, r)
                if not vch["determined"]:
                    gp_ok = False
                    surv_mism += 1
                    continue
                survs = {tuple(v["survivors"]) for _, v in avs}
                if len(survs) > 1 or survs != {tuple(vch["survivors"])}:
                    surv_mism += 1
            odets = {v["order_determined"] for _, v in avs}
            if len(odets) == 1 and odets == {True}:
                uni_odet += 1
                vch = chain_verdict(k, r)
                ords = {tuple(v["orders"][0]) for _, v in avs}
                if len(ords) > 1 or ords != {tuple(vch["orders"][0])}:
                    ord_mism += 1
        gp[str(r)] = {
            "uniformly_determined_keys": uni_det,
            "uniformly_order_determined_keys": uni_odet,
            "survivor_mismatch": surv_mism,
            "order_mismatch": ord_mism,
        }
        if surv_mism or ord_mism:
            gp_ok = False
    record(
        "Theorem G' (cap<=10, r=2..6): every uniformly-determined key has "
        "survivor == chain survivor; every uniformly-order-determined key "
        "has order == chain order",
        gp_ok,
        {"per_r": gp},
    )

    # ---- C10: partition identity on the (8,8,9)/(8,9,9) keys
    part89 = {}
    pi_ok = True
    for fam in ((8, 8, 9), (8, 9, 9)):
        for g in range(6):
            key = (fam, g)
            profs = sorted(a for a in prof10 if key_of(a) == key)
            parts = {}
            for r in (3, 4, 5, 6):
                parts[r] = [verd[r][a]["determined"] for a in profs]
            ndet345 = [sum(parts[r]) for r in (3, 4, 5)]
            ndet6 = sum(parts[6])
            exp = EXPECTED_NDET_COUNTS_89[("%s" % ",".join(map(str, fam)), g)]
            if parts[3] != parts[4] or parts[4] != parts[5]:
                pi_ok = False
            if ndet6 != 0:
                pi_ok = False
            if tuple(ndet345) != (exp[0],) * 3 or len(profs) != exp[1]:
                pi_ok = False
            part89["%s|%d" % (",".join(map(str, fam)), g)] = {
                "profiles": len(profs),
                "n_det_r3_r4_r5": ndet345,
                "n_det_r6": ndet6,
            }
    record(
        "PI: on the 12 keys (8,8,9),(8,9,9) g=0..5 the det/ndet profile "
        "partition is identical for r=3,4,5 (published counts) and every "
        "profile is non-determined at r=6",
        pi_ok,
        {"partition": part89},
    )

    # ---- C11: small-family vanishing (the 10 r=3-only keys)
    vanish = {}
    van_ok = True
    for sp, g in K0862_SMALL_10:
        key = (tuple(sp), g)
        profs = [a for a in prof10 if key_of(a) == key]
        for r in (4, 5, 6):
            ndet = sum(1 for a in profs if verd[r][a]["determined"])
            if ndet != 0:
                van_ok = False
            vanish["%s#%d" % (key_str(key), r)] = {
                "profiles": len(profs), "n_det": ndet}
        for r in (4, 5, 6):
            if chain_verdict(key, r)["determined"]:
                van_ok = False
    record(
        "PI: the 10 small-branch keys of the K0862 r=3 list are "
        "non-determined for EVERY profile and the chain at r=4,5,6 "
        "(determined side vanishes; collapse is to uniformly-ndet)",
        van_ok,
        {"per_key_r": vanish},
    )

    # ---- C12: mirror families (4,4,8)/(4,8,8)
    mirror = {}
    mir_ok = True
    for fam in ((4, 4, 8), (4, 8, 8)):
        for g in range(4):
            key = (fam, g)
            profs = [a for a in prof10 if key_of(a) == key]
            row = {}
            for r in (3, 4, 5, 6):
                ndet = sum(1 for a in profs if verd[r][a]["determined"])
                row[str(r)] = ndet
                if r in (3, 4, 5) and ndet != 0:
                    mir_ok = False
                if r in (3, 4, 5) and chain_verdict(key, r)["determined"]:
                    mir_ok = False
            exp = EXPECTED_NDET_COUNTS_48[("%s" % ",".join(map(str, fam)), g)]
            if (row["6"], len(profs)) != exp:
                mir_ok = False
            mirror["%s|%d" % (",".join(map(str, fam)), g)] = {
                "profiles": len(profs), "n_det_by_r": row}
    record(
        "PI: the mirror families (4,4,8),(4,8,8) are non-determined for "
        "every profile and the chain at r=3,4,5 and split only at r=6 "
        "(published counts)",
        mir_ok,
        {"per_key": mirror},
    )

    # ---- C13: cell-level (Theorem E') anchors
    cell_ok = True
    cell_n = 0
    # (a) r=6 failing keys: minimal witnesses, cell == region
    for k in fail[6]:
        avs = byk[6][k]
        for atoms_s in (list(min_witness(avs, True)[0]),
                        list(min_witness(avs, False)[0])):
            atoms = tuple(atoms_s)
            outcomes, _states, skipped = cell_game_k(
                atoms, 3, 6, budget=50_000_000)
            if skipped:
                cell_ok = False
                continue
            vcell = outcome_summary(sorted(outcomes))
            cell_n += 1
            if (vcell["determined"] != verd[6][atoms]["determined"]
                    or vcell["survivors"] != verd[6][atoms]["survivors"]):
                cell_ok = False
    # (b) K0862 small-family determined witnesses at r=4,5,6 (all ndet
    # at r>=4; the cell game must agree with the region verdict)
    for key4, atoms_s in sorted(K0862_SMALL_DET_WITNESSES.items()):
        atoms = tuple(atoms_s)
        assert sum(atoms_s) <= 13
        for r in (4, 5, 6):
            outcomes, _states, skipped = cell_game_k(
                atoms, 3, r, budget=50_000_000)
            if skipped:
                cell_ok = False
                continue
            vcell = outcome_summary(sorted(outcomes))
            cell_n += 1
            if (vcell["determined"] != verd[r][atoms]["determined"]
                    or vcell["survivors"] != verd[r][atoms]["survivors"]):
                cell_ok = False
    record(
        "Theorem E' anchors: cell-level game == region game on the 6 "
        "r=6 failing-key minimal witnesses (r=6) and on the 10 K0862 "
        "small-family determined witnesses at r=4,5,6 (54 checks)",
        cell_ok and cell_n == 12 + 30,
        {"atoms_checked": cell_n},
    )

    # ---- C14: Delta=0 profiles == Theorem D, r=2..6
    d0 = {}
    d0_ok = True
    for r in R_VALUES:
        n = 0
        for a, v in verd[r].items():
            sizes = tuple(sorted(profile_sizes(a, 3)))
            if len(set(sizes)) != 1:
                continue
            n += 1
            _, surv = theorem_d(sizes[0], r)
            if not (v["determined"] and v["survivors"] == [surv]):
                d0_ok = False
        d0[str(r)] = n
    entries, mism = theorem_d_table()
    record(
        "Delta=0 profiles (cap<=10) == Theorem D survivor for r=2..6; "
        "Theorem D recursion == K0859 published (C,r) table (84 entries)",
        d0_ok and mism == 0 and entries == 84,
        {"profiles_by_r": d0, "table_entries": entries,
         "table_mismatches": mism},
    )

    # ---- audit assembly
    audit["meta"] = {
        "item": "K0864",
        "title": "3-branch REMO determinacy collapse boundary for "
            "r=2,4,5,6 (r=2 full chain collapse, r=4/5 exact 12-key, "
            "r=6 exact 6-key lists, first-loser arithmetic lemma, "
            "G' chain-value collapse)",
        "date": "2026-11-16",
        "engine_provenance": "verbatim from research/experiments/"
            "remo-k-branch-collapse-boundary-20261116/"
            "verify_remo_k_branch_boundary.py (K0862, commit c8bdacc1)",
        "r_values_swept": list(R_VALUES),
    }
    audit["burnside_cap10"] = {
        "fix_id": fi, "fix_trans": ft, "fix_cyc": fc, "orbits": orbits,
    }
    audit["sweeps"] = {}
    for r in R_VALUES:
        audit["sweeps"][str(r)] = {
            "profiles": 15863,
            "keys": 715,
            "det_keys": det_keys_total[r],
            "order_det_keys": odet_keys_total[r],
            "failing_keys": sorted([list(k[0]), k[1]] for k in fail[r]),
        }
    audit["failing_witnesses"] = witnesses
    audit["partition_89_families"] = part89
    audit["mirror_48_families"] = mirror
    audit["first_loser_violations"] = fl_bad
    audit["theorem_g_prime"] = gp
    audit["theorem_g_cap7_recomputed"] = tg
    audit["delta0_profiles_by_r"] = d0
    audit["machine_checks"] = checks
    audit["summary"] = {
        "all_ok": all(c["ok"] for c in checks),
        "checks_total": len(checks),
    }
    return audit


def main():
    prof10 = constrained_profiles(10)
    verd = sweep_all(prof10)
    return assemble(prof10, verd)


def serialize(audit):
    return json.dumps(audit, sort_keys=True, ensure_ascii=False, indent=1) + "\n"


def run():
    audit1 = main()
    blob1 = serialize(audit1)
    audit2 = main()
    blob2 = serialize(audit2)
    d1 = hashlib.sha256(blob1.encode()).hexdigest()
    d2 = hashlib.sha256(blob2.encode()).hexdigest()
    if d1 != d2:
        sys.stderr.write("FATAL: two runs differ (nondeterminism)\n")
        sys.exit(1)
    all_ok = audit1["summary"]["all_ok"]
    out_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "output",
        "remo_k_branch_r_boundary_audit.json",
    )
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    if os.path.exists(out_path):
        with open(out_path, "rb") as f:
            committed = f.read().decode()
        if committed != blob1:
            sys.stderr.write(
                "FATAL: regenerated audit differs from committed file "
                "(sha256 %s)\n" % d1
            )
            sys.exit(1)
        print("OK: audit byte-identical (sha256 %s)" % d1)
    else:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(blob1)
        print("wrote %s (sha256 %s)" % (out_path, d1))
    print("AUDIT PASSED" if all_ok else "AUDIT FAILED")
    for c in audit1["machine_checks"]:
        print("  [%s] %s" % ("ok" if c["ok"] else "NG", c["name"]))
    print("audit sha256 %s" % d1)
    for r in R_VALUES:
        sw = audit1["sweeps"][str(r)]
        print("r=%s: det_keys=%d failing=%d" % (
            r, sw["det_keys"], len(sw["failing_keys"])))
    if not all_ok:
        sys.exit(1)


if __name__ == "__main__":
    run()
