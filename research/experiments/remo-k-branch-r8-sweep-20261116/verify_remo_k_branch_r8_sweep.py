#!/usr/bin/env python3
"""K0869 audit: 3-branch REMO determinacy collapse boundary at r=8
(the full cap<=10 sweep; K0864 covered r=2..6, K0866 covered r=7, and
K0867 refuted the (4,4,10)/(4,10,10) extrapolation by a targeted check).

Self-contained. Deterministic (no randomness, no wall clock, no network).
Python 3.11+ / stdlib only. Engine (region game, profile enumeration,
Theorem D recursion, Burnside counting, the K0862/K0864 published anchor
constants) is verbatim from research/experiments/
remo-k-branch-r-boundary-20261116/verify_remo_k_branch_r_boundary.py
(K0864, commit 6230f93b, sha256
43adec69c0a6c5da0a43f6db6405c11376fda6c7eec8e7055f17b274c35a1edf,
itself verbatim from the K0862 verifier c8bdacc1 / K0861 33684f3e).

Checked claims (proof text: report.md in this directory /
research/knowledge/items/K0869-remo-k-branch-r8-boundary.md):

I8 (Theorem I, r=8, cap<=10, finite complete)  For every 3-branch family
    with branch sizes <= 10 (15863 canonical profiles, 715 keys): the keys
    at which survivor determinacy fails to collapse are EXACTLY the 10 keys
    (6,6,8) and (6,8,8) with gamma = 0..4 -- a NEW family pair, different
    from r=3..5's (8,8,9)/(8,9,9), r=6's (4,4,8)/(4,8,8) and r=7's
    (4,4,9)/(4,9,9), and NOT the (4,4,10)/(4,10,10) extrapolation refuted
    by K0867. Every failing key contains a size-6 and a size-8 branch; no
    key with a size-10 branch fails. In every failing key the chain profile
    is DETERMINED with survivor P_5 (0-based), all determined profiles
    have survivor P_5, and every non-determined profile has the
    possible-survivor set {P_3,P_4,P_5}. The gamma range 0..4 is the first
    failing range beyond gamma<=2 in the r>=6 families; gamma=5 keys are
    uniformly non-determined.
X67 (K0867 cross-check)  The full sweep independently reproduces K0867's
    targeted refutation: (4,4,10),(4,10,10) x gamma=0..3 are uniformly
    non-determined at r=8 with possible-survivor set {P_3,P_7} and the
    published profile counts (20,10,4,1 / 51,32,15,7).
FATE  All 34 previously failing keys (K0862 r=3 22, K0864 r=4/5 12, r=6 6,
    K0866 r=7 6 -- union 34) are uniformly non-determined at r=8 and their
    chains are non-determined (complete collapse to uniformly-ndet).
ECHO  The new failing keys (6,6,8),(6,8,8) x gamma=0..4 were dormant at
    r=3..7 (every profile AND chain non-determined) and fully determined
    at r=2 with survivor == chain survivor (the r=2 total collapse of
    K0864 corroborated on these keys).
G5   (6,6,8) and (6,8,8) at gamma=5 are uniformly non-determined with
    non-determined chains.
FL8  Lemma FL machine anchor at r=8: possible first losers == {C_i mod 8}
    on all 15863 profiles (0 violations; the lemma itself is universal,
    proved in K0864).
GP8  Theorem G' at r=8: all 98 uniformly determined keys have survivor ==
    chain survivor; all 55 uniformly order-determined keys have
    elimination order == chain order (0 mismatches).
D0   Delta=0 profiles (728) match the Theorem D recursion at r=8; the
    recursion matches the K0859 published (C,r) table (84 entries,
    r=2..8 -- r=8 is the last column of that table).
CPT  The committed compact per-profile sweep record
    (sweep_r8_verdicts_compact.jsonl) covers all 15863 profiles exactly
    once and every field agrees with the recomputed verdicts.

Scope / limits (do not over-read):
- Theorem E' (K0861, universal) transfers every profile verdict to every
  board realizing the profile. I8/X67/FATE/ECHO/G5/FL8/GP8/D0 are
  COMPLETE only over the finite domain stated (branch sizes <= 10,
  r = 8); branch sizes >= 11, r >= 9 and the (6,6,8)/(6,8,8) fate at
  r >= 9 are NOT covered.
- Non-collapse of determinacy does not mean constant outcome: within
  failing keys the possible-survivor sets still depend on atoms.
- Cell-level (Theorem E') anchors are not run at r=8 (the cell game
  exceeded memory already at r=7 on 13-cell witnesses, K0866); E' itself
  is universal, so the region verdicts transfer to realizing boards.
- 11x11 empty board / class frontiers remain UNKNOWN, unrelated.
- solved head is manifest bookkeeping only.
"""

import hashlib
import json
import os
import sys

sys.setrecursionlimit(100000)


PUBLISHED_UNIFORM_ELIMINATION_TABLE_JSON = (
    '{"1":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[1,2],"survivor":0},"4":{"elimination":[1,2,3],"survivor":0},"5":{"elimination":[1,2,3,4],"survivor":0},"6":{"elimination":[1,2,3,4,5],"survivor":0},"7":{"elimination":[1,2,3,4,5,6],"survivor":0},"8":{"elimination":[1,2,3,4,5,6,7],"survivor":0}},"10":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[1,0],"survivor":2},"4":{"elimination":[2,1,0],"survivor":3},"5":{"elimination":[0,3,2,1],"survivor":4},"6":{"elimination":[4,0,3,2,1],"survivor":5},"7":{"elimination":[3,5,0,4,2,1],"survivor":6},"8":{"elimination":[2,4,6,0,5,3,1],"survivor":7}},"11":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[2,1],"survivor":0},"4":{"elimination":[3,2,1],"survivor":0},"5":{"elimination":[1,4,3,2],"survivor":0},"6":{"elimination":[5,1,4,3,2],"survivor":0},"7":{"elimination":[4,6,1,5,3,2],"survivor":0},"8":{"elimination":[3,5,7,1,6,4,2],"survivor":0}},"12":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[0,1],"survivor":2},"4":{"elimination":[0,1,2],"survivor":3},"5":{"elimination":[2,0,1,3],"survivor":4},"6":{"elimination":[0,3,1,2,4],"survivor":5},"7":{"elimination":[5,0,3,1,2,4],"survivor":6},"8":{"elimination":[4,6,0,3,1,2,5],"survivor":7}},"2":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[2,0],"survivor":1},"4":{"elimination":[2,3,0],"survivor":1},"5":{"elimination":[2,3,4,0],"survivor":1},"6":{"elimination":[2,3,4,5,0],"survivor":1},"7":{"elimination":[2,3,4,5,6,0],"survivor":1},"8":{"elimination":[2,3,4,5,6,7,0],"survivor":1}},"3":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[0,2],"survivor":1},"4":{"elimination":[3,0,2],"survivor":1},"5":{"elimination":[3,4,0,2],"survivor":1},"6":{"elimination":[3,4,5,0,2],"survivor":1},"7":{"elimination":[3,4,5,6,0,2],"survivor":1},"8":{"elimination":[3,4,5,6,7,0,2],"survivor":1}},"4":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[1,0],"survivor":2},"4":{"elimination":[0,2,1],"survivor":3},"5":{"elimination":[4,0,2,1],"survivor":3},"6":{"elimination":[4,5,0,2,1],"survivor":3},"7":{"elimination":[4,5,6,0,2,1],"survivor":3},"8":{"elimination":[4,5,6,7,0,2,1],"survivor":3}},"5":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[2,1],"survivor":0},"4":{"elimination":[1,3,2],"survivor":0},"5":{"elimination":[0,2,4,3],"survivor":1},"6":{"elimination":[5,0,2,4,3],"survivor":1},"7":{"elimination":[5,6,0,2,4,3],"survivor":1},"8":{"elimination":[5,6,7,0,2,4,3],"survivor":1}},"6":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[0,1],"survivor":2},"4":{"elimination":[2,0,1],"survivor":3},"5":{"elimination":[1,3,0,2],"survivor":4},"6":{"elimination":[0,2,4,1,3],"survivor":5},"7":{"elimination":[6,0,2,4,1,3],"survivor":5},"8":{"elimination":[6,7,0,2,4,1,3],"survivor":5}},"7":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[1,2],"survivor":0},"4":{"elimination":[3,1,2],"survivor":0},"5":{"elimination":[2,4,1,3],"survivor":0},"6":{"elimination":[1,3,5,2,4],"survivor":0},"7":{"elimination":[0,2,4,6,3,5],"survivor":1},"8":{"elimination":[7,0,2,4,6,3,5],"survivor":1}},"8":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[2,0],"survivor":1},"4":{"elimination":[0,3,1],"survivor":2},"5":{"elimination":[3,0,4,1],"survivor":2},"6":{"elimination":[2,4,0,5,1],"survivor":3},"7":{"elimination":[1,3,5,0,6,2],"survivor":4},"8":{"elimination":[0,2,4,6,1,7,3],"survivor":5}},"9":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[0,2],"survivor":1},"4":{"elimination":[1,0,3],"survivor":2},"5":{"elimination":[4,1,0,3],"survivor":2},"6":{"elimination":[3,5,1,0,4],"survivor":2},"7":{"elimination":[2,4,6,1,0,5],"survivor":3},"8":{"elimination":[1,3,5,7,2,0,6],"survivor":4}}}'
)
#!/usr/bin/env python3
import sys
sys.setrecursionlimit(100000)
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
# ---------------------------------------------------------------------------
# this item (K0869): r=8 full-sweep boundary

R8 = 8

# K0866 (r=7) failing keys: (4,4,9),(4,9,9) x gamma=0..2 (6 keys).
K0866_FAILING_R7 = (
    [([4, 4, 9], g) for g in range(3)] + [([4, 9, 9], g) for g in range(3)]
)

# K0867: at r=8 the (4,4,10),(4,10,10) x gamma=0..3 keys are uniformly
# non-determined with possible-survivor set {3,7} (0-based) and profile
# counts (n_det, n_profiles) = (0,20),(0,10),(0,4),(0,1) and
# (0,51),(0,32),(0,15),(0,7).
K0867_NDET_4_10 = {
    ("4,4,10", 0): (0, 20), ("4,4,10", 1): (0, 10),
    ("4,4,10", 2): (0, 4), ("4,4,10", 3): (0, 1),
    ("4,10,10", 0): (0, 51), ("4,10,10", 1): (0, 32),
    ("4,10,10", 2): (0, 15), ("4,10,10", 3): (0, 7),
}

# This item, first computed 2026-11-16 by the full r=8 sweep (chunked
# 2-worker shard driver, engine verbatim, 0 budget skips), then re-derived
# deterministically by this verifier on every run.
EXPECTED_FAILING_R8 = (
    [([6, 6, 8], g) for g in range(5)] + [([6, 8, 8], g) for g in range(5)]
)

# per-key determined-profile counts on the two new failing families
# (gamma=0..4 failing with a det/ndet split; gamma=5 uniformly ndet).
EXPECTED_PARTITION_68 = {
    ("6,6,8", 0): (48, 51), ("6,6,8", 1): (30, 33), ("6,6,8", 2): (16, 19),
    ("6,6,8", 3): (7, 10), ("6,6,8", 4): (2, 4), ("6,6,8", 5): (0, 1),
    ("6,8,8", 0): (63, 66), ("6,8,8", 1): (42, 45), ("6,8,8", 2): (24, 27),
    ("6,8,8", 3): (13, 16), ("6,8,8", 4): (4, 7), ("6,8,8", 5): (0, 3),
}

COMPACT_NAME = "sweep_r8_verdicts_compact.jsonl"
AUDIT_NAME = "remo_k_branch_r8_sweep_audit.json"


def sweep_r8(prof10):
    verd = {}
    for a in prof10:
        v, _ = region_verdict_cached(a, 3, R8)
        assert v is not None, "budget skip at r=8 for %s" % (a,)
        verd[a] = v
    return verd


def load_compact(path):
    """Load the committed compact per-profile sweep record (or None)."""
    if not os.path.exists(path):
        return None
    recs = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            j = json.loads(line)
            i = j["i"]
            assert i not in recs, "duplicate compact record %d" % i
            recs[i] = j
    return recs


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

    byk = {}
    for a in prof10:
        byk.setdefault(key_of(a), []).append(a)
    n_keys = len(byk)

    # ---- C2: full-sweep coverage
    record(
        "r=8 sweep coverage: 15863 profiles, 715 keys, 0 budget skips",
        len(verd) == 15863 and n_keys == 715,
        {"profiles": len(verd), "keys": n_keys},
    )

    fail = failing_keys(group_by_key(verd))

    def det_counts(key):
        profs = byk[key]
        ndet = sum(1 for a in profs if verd[a]["determined"])
        return ndet, len(profs)

    # ---- C3: Theorem I r=8
    fl8 = sorted([list(k[0]), k[1]] for k in fail)
    e8 = sorted([list(sp), g] for sp, g in EXPECTED_FAILING_R8)
    size68 = all(6 in k[0] and 8 in k[0] for k in fail)
    no10 = all(10 not in k[0] for k in fail)
    uni_ok = True
    part = {}
    for k in fail:
        profs = byk[k]
        vch = chain_verdict(k, R8)
        if not vch["determined"] or vch["survivors"] != [5]:
            uni_ok = False
        det = [a for a in profs if verd[a]["determined"]]
        ndet = [a for a in profs if not verd[a]["determined"]]
        if {tuple(verd[a]["survivors"]) for a in det} != {(5,)}:
            uni_ok = False
        for a in ndet:
            if tuple(sorted(verd[a]["survivors"])) != (3, 4, 5):
                uni_ok = False
        dmin = min_witness([(a, verd[a]) for a in profs], True)
        nmin = min_witness([(a, verd[a]) for a in profs], False)
        part[key_str(k)] = {
            "profiles": len(profs),
            "n_det": len(det),
            "det_witness": {"atoms": list(dmin[0]), "cells": sum(dmin[0]),
                            "survivors": dmin[1]["survivors"]},
            "ndet_witness": {"atoms": list(nmin[0]), "cells": sum(nmin[0]),
                             "survivors": nmin[1]["survivors"]},
            "chain_survivors": vch["survivors"],
        }
    pc_ok = True
    for fam in ((6, 6, 8), (6, 8, 8)):
        for g in range(6):
            key = (fam, g)
            cnts = det_counts(key)
            exp = EXPECTED_PARTITION_68[("%s" % ",".join(map(str, fam)), g)]
            if cnts != exp:
                pc_ok = False
    record(
        "Theorem I r=8: non-collapse keys are exactly the 10 keys "
        "(6,6,8),(6,8,8) x g=0..4; every failing key contains sizes 6 and "
        "8; no size-10 key fails; chain determined with survivor P_5; "
        "determined-side uniform P_5; ndet possible-survivor sets "
        "{(3,4,5)}; partition counts match the published constants",
        fl8 == e8 and size68 and no10 and uni_ok and pc_ok and len(fail) == 10,
        {"failing": fl8, "size_6_and_8_in_every_failing_key": size68,
         "failing_with_10": 0, "partition": part},
    )

    # ---- C4: K0867 cross-check
    cross = {}
    cross_ok = True
    for fam in ((4, 4, 10), (4, 10, 10)):
        for g in range(4):
            key = (fam, g)
            profs = byk[key]
            ndet = sum(1 for a in profs if verd[a]["determined"])
            sets_ = {tuple(sorted(verd[a]["survivors"])) for a in profs}
            vch = chain_verdict(key, R8)
            exp = K0867_NDET_4_10[("%s" % ",".join(map(str, fam)), g)]
            okk = (
                (ndet, len(profs)) == exp
                and sets_ == {(3, 7)}
                and not vch["determined"]
            )
            cross_ok = cross_ok and okk
            cross["%s|%d" % (",".join(map(str, fam)), g)] = {
                "profiles": len(profs), "n_det": ndet,
                "ndet_survivor_sets": sorted(list(s) for s in sets_),
                "chain_determined": vch["determined"],
            }
    record(
        "K0867 cross-check: the full sweep independently reproduces the "
        "targeted refutation -- (4,4,10),(4,10,10) x g=0..3 uniformly "
        "non-determined at r=8 with possible-survivor sets {(3,7)} and "
        "the published profile counts",
        cross_ok,
        {"per_key": cross},
    )

    # ---- C5: fate of all previously failing keys at r=8
    prev = []
    for sp, g in (K0862_FAILING_22 + EXPECTED_FAILING_R4 + EXPECTED_FAILING_R5
                  + EXPECTED_FAILING_R6 + K0866_FAILING_R7):
        k = (tuple(sp), g)
        if k not in prev:
            prev.append(k)
    fate = {}
    fate_ok = True
    for k in prev:
        profs = byk[k]
        ndet = sum(1 for a in profs if verd[a]["determined"])
        vch = chain_verdict(k, R8)
        if ndet != 0 or vch["determined"]:
            fate_ok = False
        fate[key_str(k)] = {"profiles": len(profs), "n_det": ndet,
                            "chain_determined": vch["determined"]}
    record(
        "FATE: all %d previously failing keys (r=3 22 / r=4,5 12 / r=6 6 / "
        "r=7 6, union 34) are uniformly non-determined at r=8 with "
        "non-determined chains (complete collapse to uniformly-ndet)" % len(prev),
        fate_ok and len(prev) == 34,
        {"keys": len(prev), "per_key": fate},
    )

    # ---- C6: dormancy (pre-echo) of the new failing keys
    echo = {}
    echo_ok = True
    for fam in ((6, 6, 8), (6, 8, 8)):
        for g in range(5):
            key = (fam, g)
            profs = byk[key]
            for r in (3, 4, 5, 6, 7):
                ndet = 0
                for a in profs:
                    v, _ = region_verdict_cached(a, 3, r)
                    assert v is not None
                    if v["determined"]:
                        ndet += 1
                vch = chain_verdict(key, r)
                if ndet != 0 or vch["determined"]:
                    echo_ok = False
                echo["%s#%d" % (key_str(key), r)] = {
                    "profiles": len(profs), "n_det": ndet}
            ndet2 = 0
            surv_mism = 0
            vch2 = chain_verdict(key, 2)
            for a in profs:
                v, _ = region_verdict_cached(a, 3, 2)
                assert v is not None
                if v["determined"]:
                    ndet2 += 1
                    if v["survivors"] != vch2["survivors"]:
                        surv_mism += 1
            if ndet2 != len(profs) or not vch2["determined"] or surv_mism:
                echo_ok = False
            echo["%s#2" % key_str(key)] = {
                "profiles": len(profs), "n_det": ndet2,
                "survivor_mismatch": surv_mism,
                "chain_survivors": vch2["survivors"]}
    record(
        "ECHO: the new failing keys (6,6,8),(6,8,8) x g=0..4 were dormant "
        "at r=3..7 (every profile and chain non-determined) and fully "
        "determined at r=2 with survivor == chain survivor",
        echo_ok,
        {"per_key_r": echo},
    )

    # ---- C7: gamma=5 keys are uniformly non-determined
    g5_ok = True
    for fam in ((6, 6, 8), (6, 8, 8)):
        key = (fam, 5)
        profs = byk[key]
        if any(verd[a]["determined"] for a in profs):
            g5_ok = False
        if chain_verdict(key, R8)["determined"]:
            g5_ok = False
    record(
        "GAMMA5: (6,6,8),(6,8,8) at gamma=5 are uniformly non-determined "
        "with non-determined chains (the failing range stops at gamma=4)",
        g5_ok,
        {"g5_partition": {key_str((f, 5)): det_counts((f, 5))
                          for f in ((6, 6, 8), (6, 8, 8))}},
    )

    # ---- C8: Lemma FL machine anchor at r=8
    flbad = 0
    for a in prof10:
        sizes = profile_sizes(a, 3)
        if verd[a]["first_losers"] != sorted({c % R8 for c in sizes}):
            flbad += 1
    record(
        "Lemma FL at r=8: possible first losers == {C_i mod 8} on all "
        "15863 profiles (0 violations; universal proof in K0864)",
        flbad == 0,
        {"violations": flbad},
    )

    # ---- C9: Theorem G' at r=8
    gp = {"uniformly_determined_keys": 0,
          "uniformly_order_determined_keys": 0,
          "survivor_mismatch": 0, "order_mismatch": 0}
    gp_ok = True
    for k, profs in byk.items():
        dets = {verd[a]["determined"] for a in profs}
        if dets == {True}:
            gp["uniformly_determined_keys"] += 1
            vch = chain_verdict(k, R8)
            survs = {tuple(verd[a]["survivors"]) for a in profs}
            if (not vch["determined"] or len(survs) > 1
                    or survs != {tuple(vch["survivors"])}):
                gp["survivor_mismatch"] += 1
                gp_ok = False
        odets = {verd[a]["order_determined"] for a in profs}
        if odets == {True}:
            gp["uniformly_order_determined_keys"] += 1
            vch = chain_verdict(k, R8)
            ords = {tuple(verd[a]["orders"][0]) for a in profs}
            if (not vch["order_determined"] or len(ords) > 1
                    or ords != {tuple(vch["orders"][0])}):
                gp["order_mismatch"] += 1
                gp_ok = False
    record(
        "Theorem G' at r=8: all uniformly determined keys have survivor == "
        "chain survivor; all uniformly order-determined keys have order == "
        "chain order (98 resp. 55 keys, 0 mismatches)",
        gp_ok and gp["uniformly_determined_keys"] == 98
        and gp["uniformly_order_determined_keys"] == 55,
        gp,
    )

    # ---- C10: Delta=0 profiles and Theorem D table
    d0n = 0
    d0bad = 0
    for a in prof10:
        sizes = tuple(sorted(profile_sizes(a, 3)))
        if len(set(sizes)) != 1:
            continue
        d0n += 1
        _, surv = theorem_d(sizes[0], R8)
        if not (verd[a]["determined"] and verd[a]["survivors"] == [surv]):
            d0bad += 1
    entries, mism = theorem_d_table()
    record(
        "Delta=0 profiles (cap<=10) == Theorem D survivor at r=8 (728 "
        "profiles); Theorem D recursion == K0859 published (C,r) table "
        "(84 entries, r=2..8)",
        d0n == 728 and d0bad == 0 and mism == 0 and entries == 84,
        {"profiles": d0n, "violations": d0bad,
         "table_entries": entries, "table_mismatches": mism},
    )

    # ---- C11: compact sweep record cross-check
    comp_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), COMPACT_NAME)
    recs = load_compact(comp_path)
    if recs is None:
        record("compact sweep record present and covering all 15863 "
               "profiles exactly once, every field matching", False,
               {"missing": True})
    else:
        mism = 0
        atom_mism = 0
        for i in sorted(recs):
            j = recs[i]
            a = prof10[i]
            if tuple(j["a"]) != a:
                atom_mism += 1
                continue
            v = verd[a]
            o0 = v["orders"][0] if v["order_determined"] else None
            if (j["d"] != v["determined"] or j["od"] != v["order_determined"]
                    or j["s"] != v["survivors"]
                    or j["fl"] != v["first_losers"] or j["o0"] != o0):
                mism += 1
        ok = (len(recs) == 15863 and sorted(recs) == list(range(15863))
              and mism == 0 and atom_mism == 0)
        record(
            "compact sweep record present and covering all 15863 profiles "
            "exactly once, every field matching the recomputed verdicts",
            ok,
            {"records": len(recs), "field_mismatches": mism,
             "atom_mismatches": atom_mism},
        )

    # ---- audit assembly
    audit["meta"] = {
        "item": "K0869",
        "title": "3-branch REMO determinacy collapse boundary at r=8 "
            "(10-key exact list (6,6,8),(6,8,8) x g=0..4, first gamma>=3 "
            "failing range, previous-family total collapse, K0867 "
            "cross-check, FL/G'/Delta=0 r=8 anchors)",
        "date": "2026-11-16",
        "engine_provenance": "verbatim from research/experiments/"
            "remo-k-branch-r-boundary-20261116/"
            "verify_remo_k_branch_r_boundary.py (K0864, commit 3138e0e3, "
            "sha256 43adec69c0a6c5da0a43f6db6405c11376fda6c7eec8e7055f"
            "17b274c35a1edf)",
        "r_values_swept": [R8],
    }
    audit["burnside_cap10"] = {
        "fix_id": fi, "fix_trans": ft, "fix_cyc": fc, "orbits": orbits,
    }
    audit["sweep_r8"] = {
        "profiles": len(prof10),
        "keys": n_keys,
        "uniformly_determined_keys": gp["uniformly_determined_keys"],
        "uniformly_order_determined_keys":
            gp["uniformly_order_determined_keys"],
        "failing_keys": fl8,
    }
    audit["failing_partition_and_witnesses"] = part
    audit["k0867_cross"] = cross
    audit["fate_prev_failing"] = fate
    audit["echo_dormancy"] = echo
    audit["first_loser_violations_r8"] = flbad
    audit["theorem_g_prime_r8"] = gp
    audit["delta0_profiles_r8"] = d0n
    audit["machine_checks"] = checks
    audit["summary"] = {
        "all_ok": all(c["ok"] for c in checks),
        "checks_total": len(checks),
    }
    return audit


def main():
    prof10 = constrained_profiles(10)
    verd = sweep_r8(prof10)
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
        AUDIT_NAME,
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
    sw = audit1["sweep_r8"]
    print("r=8: uni_det=%d uni_odet=%d failing=%d"
          % (sw["uniformly_determined_keys"],
             sw["uniformly_order_determined_keys"],
             len(sw["failing_keys"])))
    if not all_ok:
        sys.exit(1)


if __name__ == "__main__":
    run()
