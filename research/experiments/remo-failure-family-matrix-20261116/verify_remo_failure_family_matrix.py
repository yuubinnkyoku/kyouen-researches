#!/usr/bin/env python3
"""K0874 audit: 3-branch REMO failure-family state matrix, 52 keys x r=2..8.

Self-contained. Deterministic (no randomness, no wall clock, no network).
Python 3.11+ / stdlib only.

The 52 keys are the union of
  - the 44 keys that ever failed survivor-determinacy collapse in the
    published cap<=10 boundaries: the 22 r=3 keys (K0862 Theorem H:
    10 small-branch keys + (8,8,9),(8,9,9) x gamma<=5), the 6 r=6 keys
    (4,4,8),(4,8,8) x gamma<=2 (K0864), the 6 r=7 keys (4,4,9),(4,9,9)
    x gamma<=2 (K0866), and the 10 r=8 keys (6,6,8),(6,8,8) x gamma<=4
    (K0869) [union 44 distinct], and
  - the 8 keys of the refuted r=8 prediction family (4,4,10),(4,10,10)
    x gamma=0..3 (K0867), which never appears in any published failing
    list but is the only other family ever proposed as a candidate.

Every cell (key, r) for r = 2..8 is computed by the region-counting game
(engine verbatim from the K0864 verifier, commit 3138e0e3, sha256
43adec69c0a6c5da0a43f6db6405c11376fda6c7eec8e7055f17b274c35a1edf,
itself verbatim from the K0862 verifier, commit c8bdacc1) over the same
15863 canonical profiles / 715 (sizes,gamma) keys as K0862/K0864/K0866/
K0869 (Burnside orbit count 15863 machine-checked).

Checked claims (proof text: report.md in this directory):

MX1 (domain anchors)  Burnside fixed points (84494, 3478, 125) give
    15863 orbits; constrained_profiles(10) == 15863 canonical profiles,
    715 keys; the 52 matrix keys are distinct, nonempty, 1392 profiles
    in total.
MX2 (r=3, K0862 Theorem H reproduction)  Exactly the 22 published keys
    are mixed at r=3; each has uniform determined-side survivor P_1
    (0-indexed [1]) with the chain determined on the same side and the
    published per-multiset non-determined survivor sets; all 22x2
    published minimal witnesses reproduce at the region level.
MX3 (r=4,5, K0864 reproduction + strengthened PI)  Exactly the 12 keys
    (8,8,9),(8,9,9) x gamma<=5 are mixed; the determined profile SETS
    (not just the counts) are identical for r=3,4,5 in all 12 keys
    (K0864 PI at set level); counts match the published partitions
    (92,62,40,22,10,3 / 102,72,46,28,13,4); determined side uniform P_2;
    non-determined sets within {(1,2,3)} at r=4 and within
    {(1,2,3),(1,2,3,4)} at r=5.
MX4 (r=6, K0864 reproduction)  Exactly the 6 keys (4,4,8),(4,8,8) x
    gamma<=2 are mixed with published partitions (16/20, 7/10, 2/4) and
    (34/39, 19/24, 6/11); determined side uniform P_3; non-determined
    sets {{2,3}}; the 8/9 and small-branch and 4/9 families are
    uniformly non-determined (K0864 PI / K0866 PE).
MX5 (r=7, K0866 reproduction + new small-branch cell)  Exactly the 6
    keys (4,4,9),(4,9,9) x gamma<=2 are mixed with published partitions
    (16/20, 7/10, 2/4) and (39/45, 22/28, 7/13); determined side
    uniform P_3; non-determined sets {{1,2,3}}; the published r=7
    witnesses and the FATE chain values of the 4/8 and 8/9 families
    reproduce.  NEW: the 10 small-branch keys are uniformly
    non-determined at r=7, and their non-determined structure is NOT
    uniform across the family: (2,3,8),(3,3,8),(3,8,8) have survivor
    sets {{1,2,4},{1,4}} with chain set {1,4}; (2,8,9) has sets
    {{1,2,3,4,5},{1,3,4}} with chain set {1,3,4}; (3,8,9) has sets
    {{1,2,3,4},{1,2,3,4,5},{1,3,4}} with chain set {1,3,4} - the
    last unpublished cells of that family's r>=4 column.
MX6 (r=8, K0869 FATE + K0867 reproduction)  Exactly the 10 keys
    (6,6,8),(6,8,8) x gamma<=4 are mixed with published partitions
    (48/51, 30/33, 16/19, 7/10, 2/4) and (63/66, 42/45, 24/27, 13/16,
    4/7); determined side uniform P_5; non-determined sets {{3,4,5}};
    the 34 keys that are mixed at some r<=7 are uniformly
    non-determined with non-determined chains at r=8 (FATE); the 4/10
    family is uniformly
    non-determined with possible-survivor set exactly {3,7} for every
    profile and the chain, with the published profile counts
    (20,10,4,1 / 51,32,15,7) and 0 determined profiles (K0867).
MX7 (r=2, K0864 Theorem I r=2 made explicit on the 52 keys)  Every one
    of the 52 keys collapses completely to its chain value at r=2:
    determinacy, order determinacy, determined survivor, order-determined
    order, and (for non-determined keys) the possible-survivor set each
    equal the chain value, uniformly over all profiles.  Split: the 24
    keys of the 4/8, 6/8 and 4/10 families are uniformly DETERMINED
    with survivor P_1 (the 16 4/8 and 6/8 keys are K0864 I2; the 4/10
    keys are MX8); the other 28 keys are uniformly non-determined
    with possible-survivor set {0,1} = chain.
MX8 (NEW: 4/10-family phase structure)  The 8 keys (4,4,10),(4,10,10)
    x gamma=0..3 are uniformly DETERMINED at r=2,3,4 with survivors
    P_1, P_2, P_3 (chain determined, survivor = chain survivor), and
    uniformly NON-determined at r=5..8 with possible-survivor set
    exactly {3, r-1} for every profile AND the chain ({3,4},{3,5},
    {3,6},{3,7}).  The family never enters the mixed state anywhere in
    r=2..8: it is the only candidate family with determined cells at
    r=3 and r=4, and it stays dormant (uniform) through the whole
    swept range.
MX9 (ECHO / PE reproduction)  The 6/8 family is uniformly determined
    with survivor = chain at r=2 and uniformly non-determined (chain
    non-determined) at r=3..7 (K0869 ECHO); the 4/9 family is uniformly
    non-determined (chain non-determined) at r=2..6 (K0866 PE, on the
    gamma<=2 keys).
MX10 (Lemma FL redundant anchor)  Over all 1392 profiles and all
    7 r-values (plus chains), the possible first losers are exactly
    {C_i mod r}: 0 violations.
MX11 (window table, finite observation)  The mixed-state activity
    windows over r=2..8 are: small-branch {3}; 8/9 {3,4,5};
    4/8 {6}; 4/9 {7}; 6/8 {8}; 4/10 = empty (never mixed in 2..8).

Scope / limits (do not over-read):
- This is a complete computation over the 52 named keys and
  r = 2..8 ONLY.  The full-715-key boundary claims (which keys fail at
  each r) are INHERITED from K0862/K0864/K0866/K0869 and are not
  recomputed here.
- Theorem E' (K0861, universal) transfers every profile verdict to
  every board realizing the profile.
- Non-collapse of determinacy does not mean constant outcome: inside
  mixed cells the possible-survivor sets depend on atoms; inside
  uniform non-determined cells the sets can still depend on r.
- Branch sizes >= 11 and r >= 9 are NOT covered.  No structural
  conjecture about family windows is made (K0867 refuted the
  2-point extrapolation once already).
- 11x11 empty board / class frontiers remain UNKNOWN, unrelated.
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
# matrix keys (provenance: K0862 Theorem H, K0864 Theorem I r=6,
# K0866 Theorem I r=7, K0869 Theorem I r=8, K0867 target family)

def _fam(sizes, gmax):
    return [(sizes, g) for g in range(gmax + 1)]

SMALL_10 = (
    _fam([2, 3, 8], 1) + _fam([2, 8, 9], 1) + _fam([3, 3, 8], 1)
    + _fam([3, 8, 8], 1) + _fam([3, 8, 9], 1)
)
F89_12 = _fam([8, 8, 9], 5) + _fam([8, 9, 9], 5)
F48_6 = _fam([4, 4, 8], 2) + _fam([4, 8, 8], 2)
F49_6 = _fam([4, 4, 9], 2) + _fam([4, 9, 9], 2)
F68_10 = _fam([6, 6, 8], 4) + _fam([6, 8, 8], 4)
F410_8 = _fam([4, 4, 10], 3) + _fam([4, 10, 10], 3)
OLD_44 = SMALL_10 + F89_12 + F48_6 + F49_6 + F68_10
ALL_52 = OLD_44 + F410_8
assert len(OLD_44) == 44 and len(ALL_52) == 52
assert len({(tuple(s), g) for s, g in ALL_52}) == 52

R_VALUES = (2, 3, 4, 5, 6, 7, 8)

# ---------------------------------------------------------------------------
# published anchors (machine-extracted, byte-verified against main)
#
# K0862 (commit c8bdacc1): the 22 r=3 non-collapse keys and their minimal
#   witnesses, from research/experiments/remo-k-branch-collapse-boundary-
#   20261116/output/remo_k_branch_boundary_audit.json
#   (sha256 7dfabd501f389f92f20ed85500708f4edfde63e969358008db05bcf967c6d7bb).
# K0864 (commit 3138e0e3): the r=4/5 and r=6 partitions, from
#   research/experiments/remo-k-branch-r-boundary-20261116/output/
#   remo_k_branch_r_boundary_audit.json
#   (sha256 e69baa471325fd3322b1a146f8760eafa32c824bbec515a41a9d325fed208aad).
# K0866 (commit 4122ea73 is K0863; the r=7 audit): the r=7 partitions,
#   witnesses and FATE chain values, from research/experiments/
#   remo-k-branch-r7-extension-20261116/output/remo_k_branch_r7_extension_
#   audit.json (sha256 53e03f2a76491161c516f36a5c1e78c6f9b6aeb68a4a72e3d87a
#   3c0b2dfde334).
# K0867 (commit 31d0b6e8 lane): the r=8 4/10-family refutation counts,
#   from research/experiments/remo-k-branch-r8-target-refutation-20261116/
#   output/audit.json.
# K0869: the r=8 partitions, from research/experiments/
#   remo-k-branch-r8-sweep-20261116/report.md and its audit JSON
#   (sha256 adc6676506a7d4f3bea544e79b0556ae09ef1c56104d441d2001867aa810a3f0).

K0862_FAILING_22 = (
    [([2, 3, 8], 0), ([2, 3, 8], 1), ([2, 8, 9], 0), ([2, 8, 9], 1),
     ([3, 3, 8], 0), ([3, 3, 8], 1), ([3, 8, 8], 0), ([3, 8, 8], 1),
     ([3, 8, 9], 0), ([3, 8, 9], 1)]
    + [([8, 8, 9], g) for g in range(6)]
    + [([8, 9, 9], g) for g in range(6)]
)

K0862_R3_NDET_SETS = {
    "2,3,8": [[1, 2]],
    "2,8,9": [[0, 1, 2]],
    "3,3,8": [[1, 2]],
    "3,8,8": [[1, 2]],
    "3,8,9": [[0, 1, 2], [1, 2]],
    "8,8,9": [[0, 1, 2]],
    "8,9,9": [[0, 1, 2]],
}

K0862_R3_WITNESSES_JSON = (
'{"2,3,8|0":{"det_atoms":[1,1,1,7,0,1,0],"det_cells":11,"det_survivors":[1],"ndet_atoms":[1,1,0,5,1,2,0],"ndet_cells":10,"ndet_survivors":[1,2]},"2,3,8|1":{"det_atoms":[1,2,0,7,0,0,1],"det_cells":11,"det_survivors":[1],"ndet_atoms":[1,1,0,6,0,1,1],"ndet_cells":10,"ndet_survivors":[1,2]},"2,8,9|0":{"det_atoms":[1,2,1,4,0,5,0],"det_cells":13,"det_survivors":[1],"ndet_atoms":[1,1,0,1,1,7,0],"ndet_cells":11,"ndet_survivors":[0,1,2]},"2,8,9|1":{"det_atoms":[1,3,0,4,0,4,1],"det_cells":13,"det_survivors":[1],"ndet_atoms":[1,1,0,2,0,6,1],"ndet_cells":11,"ndet_survivors":[0,1,2]},"3,3,8|0":{"det_atoms":[1,1,1,6,1,1,0],"det_cells":11,"det_survivors":[1],"ndet_atoms":[1,1,0,4,2,2,0],"ndet_cells":10,"ndet_survivors":[1,2]},"3,3,8|1":{"det_atoms":[1,1,1,7,0,0,1],"det_cells":11,"det_survivors":[1],"ndet_atoms":[1,1,0,5,1,1,1],"ndet_cells":10,"ndet_survivors":[1,2]},"3,8,8|0":{"det_atoms":[1,1,1,1,1,6,0],"det_cells":11,"det_survivors":[1],"ndet_atoms":[1,1,2,3,0,5,0],"ndet_cells":12,"ndet_survivors":[1,2]},"3,8,8|1":{"det_atoms":[1,1,6,2,0,0,1],"det_cells":11,"det_survivors":[1],"ndet_atoms":[1,1,1,2,0,5,1],"ndet_cells":11,"ndet_survivors":[1,2]},"3,8,9|0":{"det_atoms":[1,2,1,3,1,5,0],"det_cells":13,"det_survivors":[1],"ndet_atoms":[1,1,1,2,1,6,0],"ndet_cells":12,"ndet_survivors":[0,1,2]},"3,8,9|1":{"det_atoms":[1,3,0,3,1,4,1],"det_cells":13,"det_survivors":[1],"ndet_atoms":[1,1,0,1,1,6,1],"ndet_cells":11,"ndet_survivors":[0,1,2]},"8,8,9|0":{"det_atoms":[1,1,3,1,4,4,0],"det_cells":14,"det_survivors":[1],"ndet_atoms":[1,1,6,5,1,2,0],"ndet_cells":16,"ndet_survivors":[0,1,2]},"8,8,9|1":{"det_atoms":[1,1,3,2,3,3,1],"det_cells":14,"det_survivors":[1],"ndet_atoms":[1,1,5,4,1,2,1],"ndet_cells":15,"ndet_survivors":[0,1,2]},"8,8,9|2":{"det_atoms":[1,1,2,1,3,3,2],"det_cells":13,"det_survivors":[1],"ndet_atoms":[1,1,4,3,1,2,2],"ndet_cells":14,"ndet_survivors":[0,1,2]},"8,8,9|3":{"det_atoms":[1,1,2,2,2,2,3],"det_cells":13,"det_survivors":[1],"ndet_atoms":[1,1,3,2,1,2,3],"ndet_cells":13,"ndet_survivors":[0,1,2]},"8,8,9|4":{"det_atoms":[1,1,2,3,1,1,4],"det_cells":13,"det_survivors":[1],"ndet_atoms":[1,1,1,1,2,2,4],"ndet_cells":12,"ndet_survivors":[0,1,2]},"8,8,9|5":{"det_atoms":[1,1,2,4,0,0,5],"det_cells":13,"det_survivors":[1],"ndet_atoms":[1,1,1,2,1,1,5],"ndet_cells":12,"ndet_survivors":[0,1,2]},"8,9,9|0":{"det_atoms":[1,1,4,2,3,4,0],"det_cells":15,"det_survivors":[1],"ndet_atoms":[1,1,6,6,1,2,0],"ndet_cells":17,"ndet_survivors":[0,1,2]},"8,9,9|1":{"det_atoms":[1,1,3,1,3,4,1],"det_cells":14,"det_survivors":[1],"ndet_atoms":[1,1,5,5,1,2,1],"ndet_cells":16,"ndet_survivors":[0,1,2]},"8,9,9|2":{"det_atoms":[1,1,3,2,2,3,2],"det_cells":14,"det_survivors":[1],"ndet_atoms":[1,1,4,4,1,2,2],"ndet_cells":15,"ndet_survivors":[0,1,2]},"8,9,9|3":{"det_atoms":[1,1,2,1,2,3,3],"det_cells":13,"det_survivors":[1],"ndet_atoms":[1,1,3,3,1,2,3],"ndet_cells":14,"ndet_survivors":[0,1,2]},"8,9,9|4":{"det_atoms":[1,1,3,2,1,1,4],"det_cells":13,"det_survivors":[1],"ndet_atoms":[1,1,2,2,1,2,4],"ndet_cells":13,"ndet_survivors":[0,1,2]},"8,9,9|5":{"det_atoms":[1,1,3,3,0,0,5],"det_cells":13,"det_survivors":[1],"ndet_atoms":[1,1,1,1,1,2,5],"ndet_cells":12,"ndet_survivors":[0,1,2]}}'
)

K0866_R7_WITNESSES_JSON = (
'{"4,4,9|0#7":{"chain_survivors":[3],"det_atoms":[1,1,1,5,2,2,0],"det_cells":12,"det_survivors":[3],"ndet_atoms":[1,1,0,3,3,3,0],"ndet_cells":11,"ndet_survivors":[1,2,3]},"4,4,9|1#7":{"chain_survivors":[3],"det_atoms":[1,1,1,6,1,1,1],"det_cells":12,"det_survivors":[3],"ndet_atoms":[1,1,0,4,2,2,1],"ndet_cells":11,"ndet_survivors":[1,2,3]},"4,4,9|2#7":{"chain_survivors":[3],"det_atoms":[1,1,1,7,0,0,2],"det_cells":12,"det_survivors":[3],"ndet_atoms":[1,1,0,5,1,1,2],"ndet_cells":11,"ndet_survivors":[1,2,3]},"4,9,9|0#7":{"chain_survivors":[3],"det_atoms":[1,1,2,2,1,6,0],"det_cells":13,"det_survivors":[3],"ndet_atoms":[1,1,3,4,0,5,0],"ndet_cells":14,"ndet_survivors":[1,2,3]},"4,9,9|1#7":{"chain_survivors":[3],"det_atoms":[1,1,1,1,1,6,1],"det_cells":12,"det_survivors":[3],"ndet_atoms":[1,1,2,3,0,5,1],"ndet_cells":13,"ndet_survivors":[1,2,3]},"4,9,9|2#7":{"chain_survivors":[3],"det_atoms":[1,1,6,2,0,0,2],"det_cells":12,"det_survivors":[3],"ndet_atoms":[1,1,1,2,0,5,2],"ndet_cells":12,"ndet_survivors":[1,2,3]}}'
)

K0864_R345_DET = {"8,8,9": [92, 62, 40, 22, 10, 3],
                  "8,9,9": [102, 72, 46, 28, 13, 4]}
K0864_R345_TOTALS = {"8,8,9": [100, 70, 48, 30, 18, 9],
                     "8,9,9": [110, 80, 54, 36, 21, 12]}
K0864_R48 = {"4,4,8": ([16, 7, 2], [20, 10, 4]),
             "4,8,8": ([34, 19, 6], [39, 24, 11])}
K0866_R49 = {"4,4,9": ([16, 7, 2], [20, 10, 4]),
             "4,9,9": ([39, 22, 7], [45, 28, 13])}
K0869_R68 = {"6,6,8": ([48, 30, 16, 7, 2], [51, 33, 19, 10, 4]),
             "6,8,8": ([63, 42, 24, 13, 4], [66, 45, 27, 16, 7])}
K0867_410_TOTALS = {"4,4,10": [20, 10, 4, 1],
                    "4,10,10": [51, 32, 15, 7]}

K0866_FATE_R7_CHAIN = {"4,4,8": [3, 4], "4,8,8": [3, 4],
                       "8,8,9": [3, 4], "8,9,9": [3, 4]}


def kstr(sizes, g):
    return "%d,%d,%d|%d" % (sizes[0], sizes[1], sizes[2], g)


def verdict_of(atoms, r):
    v, _states = region_verdict_cached(tuple(atoms), 3, r)
    assert v is not None, "budget skip at %r r=%d" % (atoms, r)
    return v


def cell_of(byk, sizes, g, r):
    ps = byk[(tuple(sizes), g)]
    verd = [verdict_of(p, r) for p in ps]
    chain = chain_profile(sizes, g, 3)
    cv = verdict_of(chain, r)
    dets = [v["determined"] for v in verd]
    cell = {
        "n": len(ps),
        "n_det": sum(dets),
        "state": ("uniform_det" if all(dets)
                  else "uniform_ndet" if not any(dets) else "mixed"),
        "det_survivors": sorted({tuple(v["survivors"])
                                 for v, d in zip(verd, dets) if d}),
        "ndet_survivor_sets": sorted({tuple(v["survivors"])
                                      for v, d in zip(verd, dets) if not d}),
        "order_det_uniform": len({v["order_determined"] for v in verd}) == 1,
        "chain_determined": cv["determined"],
        "chain_survivors": cv["survivors"],
        "fl_ok": True,
    }
    fl_expect = sorted({c % r for c in sizes})
    for v in verd + [cv]:
        if v["first_losers"] != fl_expect:
            cell["fl_ok"] = False
    cell["_verdicts"] = verd
    cell["_chain_verdict"] = cv
    return cell


def compute_matrix(byk):
    matrix = {}
    for sizes, g in ALL_52:
        for r in R_VALUES:
            matrix[(kstr(sizes, g), r)] = cell_of(byk, sizes, g, r)
    return matrix


def mixed_keys(matrix, r):
    return sorted(k for (k, rr) in matrix if rr == r
                  and matrix[(k, rr)]["state"] == "mixed")


def assemble(byk, matrix):
    checks = []

    def record(name, ok, data=None):
        checks.append({"name": name, "ok": bool(ok),
                       "data": data if data is not None else {}})

    def cell(sizes, g, r):
        return matrix[(kstr(sizes, g), r)]

    # ---- C1: domain anchors
    fix = burnside_fix_counts(10)
    record(
        "MX1: Burnside (84494,3478,125)->15863 orbits; 15863 canonical "
        "profiles; 715 keys; 52 matrix keys; 1392 matrix profiles",
        fix == (84494, 3478, 125, 15863),
        {"fix": list(fix), "matrix_profiles": sum(
            cell(s, g, 2)["n"] for s, g in ALL_52)},
    )

    # ---- C2: r=3 reproduction of K0862 Theorem H on the matrix keys
    mx3 = mixed_keys(matrix, 3)
    exp3 = sorted(kstr(s, g) for s, g in K0862_FAILING_22)
    ok2 = mx3 == exp3
    det_uni = all(cell(s, g, 3)["det_survivors"] == [(1,)]
                  for s, g in K0862_FAILING_22)
    ndet_ok = all(cell(s, g, 3)["ndet_survivor_sets"]
                  == [tuple(x) for x in
                      K0862_R3_NDET_SETS["%d,%d,%d" % tuple(s)]]
                  for s, g in K0862_FAILING_22)
    chain_ok = all(cell(s, g, 3)["chain_determined"]
                  and cell(s, g, 3)["chain_survivors"] == [1]
                  for s, g in K0862_FAILING_22)
    wit = json.loads(K0862_R3_WITNESSES_JSON)
    wit_ok = True
    for name, w in wit.items():
        vd = verdict_of(w["det_atoms"], 3)
        vn = verdict_of(w["ndet_atoms"], 3)
        if not (vd["determined"] and vd["survivors"] == w["det_survivors"]):
            wit_ok = False
        if not ((not vn["determined"])
                and vn["survivors"] == w["ndet_survivors"]):
            wit_ok = False
    record(
        "MX2: r=3 mixed keys are exactly the published 22 (K0862); "
        "determined side uniform P_1; published per-multiset ndet sets; "
        "chain determined with survivor P_1; 22x2 witnesses reproduce",
        ok2 and det_uni and ndet_ok and chain_ok and wit_ok,
        {"mixed": mx3, "witness_checks": 2 * len(wit)},
    )

    # ---- C3: r=4 and r=5 reproduction (K0864) + strengthened PI
    mx4 = mixed_keys(matrix, 4)
    mx5 = mixed_keys(matrix, 5)
    exp89 = sorted(kstr(s, g) for s, g in F89_12)
    ok34 = mx4 == exp89 and mx5 == exp89
    counts_ok = True
    pi_sets_ok = True
    for sizes, gmax in (((8, 8, 9), 5), ((8, 9, 9), 5)):
        name = "%d,%d,%d" % sizes
        for g in range(gmax + 1):
            for r in (4, 5):
                c = cell(list(sizes), g, r)
                if c["n_det"] != K0864_R345_DET[name][g]:
                    counts_ok = False
                if c["n"] != K0864_R345_TOTALS[name][g]:
                    counts_ok = False
                if c["det_survivors"] != [(2,)]:
                    counts_ok = False
                if not c["chain_determined"] or c["chain_survivors"] != [2]:
                    counts_ok = False
            # strengthened PI: the determined profile SETS are identical
            bykkey = (sizes, g)
            det_sets = {
                r: frozenset(p for p in byk[bykkey]
                             if verdict_of(p, r)["determined"])
                for r in (3, 4, 5)
            }
            if not (det_sets[3] == det_sets[4] == det_sets[5]):
                pi_sets_ok = False
    ndet_r4_ok = all(set(map(tuple, cell(s, g, 4)["ndet_survivor_sets"]))
                     <= {(1, 2, 3)}
                     for s, g in F89_12)
    ndet_r5_ok = all(set(map(tuple, cell(s, g, 5)["ndet_survivor_sets"]))
                     <= {(1, 2, 3), (1, 2, 3, 4)}
                     for s, g in F89_12)
    record(
        "MX3: r=4 and r=5 mixed keys are exactly the published 12 "
        "(K0864); partitions match (92,62,40,22,10,3 / 102,72,46,28,13,4); "
        "determined side uniform P_2; ndet sets within published; "
        "determined profile SETS identical for r=3,4,5 (PI at set level)",
        ok34 and counts_ok and ndet_r4_ok and ndet_r5_ok and pi_sets_ok,
        {"mixed_r4": mx4, "mixed_r5": mx5, "pi_set_keys": 12},
    )

    # ---- C4: r=6 reproduction (K0864)
    mx6 = mixed_keys(matrix, 6)
    exp48 = sorted(kstr(s, g) for s, g in F48_6)
    ok6 = mx6 == exp48
    c6_ok = True
    for sizes in ((4, 4, 8), (4, 8, 8)):
        name = "%d,%d,%d" % tuple(sizes)
        dets, totals = K0864_R48[name]
        for g in range(3):
            c = cell(list(sizes), g, 6)
            if (c["n_det"], c["n"]) != (dets[g], totals[g]):
                c6_ok = False
            if c["det_survivors"] != [(3,)]:
                c6_ok = False
            if c["ndet_survivor_sets"] != [(2, 3)]:
                c6_ok = False
            if not c["chain_determined"] or c["chain_survivors"] != [3]:
                c6_ok = False
    uni_r6 = (all(cell(s, g, 6)["state"] == "uniform_ndet"
                   and not cell(s, g, 6)["chain_determined"]
                   for s, g in SMALL_10)
              and all(cell(s, g, 6)["state"] == "uniform_ndet"
                      and not cell(s, g, 6)["chain_determined"]
                      for s, g in F89_12)
              and all(cell(s, g, 6)["state"] == "uniform_ndet"
                      and not cell(s, g, 6)["chain_determined"]
                      for s, g in F49_6))
    record(
        "MX4: r=6 mixed keys are exactly the published 6 (K0864) with "
        "partitions (16/20,7/10,2/4) and (34/39,19/24,6/11); determined "
        "side uniform P_3; ndet sets {{2,3}}; small-branch/8-9/4-9 "
        "families uniformly ndet (K0864 PI / K0866 PE)",
        ok6 and c6_ok and uni_r6,
        {"mixed_r6": mx6},
    )

    # ---- C5: r=7 reproduction (K0866) + new small-branch cell
    mx7 = mixed_keys(matrix, 7)
    exp49 = sorted(kstr(s, g) for s, g in F49_6)
    ok7 = mx7 == exp49
    c7_ok = True
    for sizes in ((4, 4, 9), (4, 9, 9)):
        name = "%d,%d,%d" % tuple(sizes)
        dets, totals = K0866_R49[name]
        for g in range(3):
            c = cell(list(sizes), g, 7)
            if (c["n_det"], c["n"]) != (dets[g], totals[g]):
                c7_ok = False
            if c["det_survivors"] != [(3,)]:
                c7_ok = False
            if c["ndet_survivor_sets"] != [(1, 2, 3)]:
                c7_ok = False
            if not c["chain_determined"] or c["chain_survivors"] != [3]:
                c7_ok = False
    w7 = json.loads(K0866_R7_WITNESSES_JSON)
    w7_ok = True
    for name, w in w7.items():
        vd = verdict_of(w["det_atoms"], 7)
        vn = verdict_of(w["ndet_atoms"], 7)
        if not (vd["determined"] and vd["survivors"] == w["det_survivors"]):
            w7_ok = False
        if not ((not vn["determined"])
                and vn["survivors"] == w["ndet_survivors"]):
            w7_ok = False
        if w["chain_survivors"] != [3]:
            w7_ok = False
    fate7_ok = True
    for sizes in ((4, 4, 8), (4, 8, 8), (8, 8, 9), (8, 9, 9)):
        name = "%d,%d,%d" % tuple(sizes)
        for g in range(6 if name[0] == "8" else 3):
            c = cell(list(sizes), g, 7)
            if (c["state"] != "uniform_ndet" or c["chain_determined"]
                    or c["chain_survivors"] != K0866_FATE_R7_CHAIN[name]):
                fate7_ok = False
    small7_sets = {
        (2, 3, 8): ([(1, 2, 4), (1, 4)], [1, 4]),
        (3, 3, 8): ([(1, 2, 4), (1, 4)], [1, 4]),
        (3, 8, 8): ([(1, 2, 4), (1, 4)], [1, 4]),
        (2, 8, 9): ([(1, 2, 3, 4, 5), (1, 3, 4)], [1, 3, 4]),
        (3, 8, 9): ([(1, 2, 3, 4), (1, 2, 3, 4, 5), (1, 3, 4)], [1, 3, 4]),
    }
    new_small7_ok = True
    for sizes, g in SMALL_10:
        c = cell(sizes, g, 7)
        sets7, chain7 = small7_sets[tuple(sizes)]
        if (c["state"] != "uniform_ndet"
                or c["ndet_survivor_sets"] != sets7
                or c["chain_determined"]
                or c["chain_survivors"] != chain7):
            new_small7_ok = False
    record(
        "MX5: r=7 mixed keys are exactly the published 6 (K0866) with "
        "partitions (16/20,7/10,2/4) and (39/45,22/28,7/13); determined "
        "side uniform P_3; ndet sets {{1,2,3}}; r=7 witnesses and the "
        "4/8 & 8/9 FATE chain values reproduce; NEW: the 10 small-branch "
        "keys are uniformly ndet at r=7 but NOT structurally uniform: "
        "(2,3,8)/(3,3,8)/(3,8,8) sets {{1,2,4},{1,4}} chain {1,4}, "
        "(2,8,9) sets {{1,2,3,4,5},{1,3,4}} chain {1,3,4}, (3,8,9) sets "
        "{{1,2,3,4},{1,2,3,4,5},{1,3,4}} chain {1,3,4}",
        ok7 and c7_ok and w7_ok and fate7_ok and new_small7_ok,
        {"mixed_r7": mx7},
    )

    # ---- C6: r=8 reproduction (K0869 FATE + K0867)
    mx8 = mixed_keys(matrix, 8)
    exp68 = sorted(kstr(s, g) for s, g in F68_10)
    ok8 = mx8 == exp68
    c8_ok = True
    for sizes in ((6, 6, 8), (6, 8, 8)):
        name = "%d,%d,%d" % tuple(sizes)
        dets, totals = K0869_R68[name]
        for g in range(5):
            c = cell(list(sizes), g, 8)
            if (c["n_det"], c["n"]) != (dets[g], totals[g]):
                c8_ok = False
            if c["det_survivors"] != [(5,)]:
                c8_ok = False
            if c["ndet_survivor_sets"] != [(3, 4, 5)]:
                c8_ok = False
            if not c["chain_determined"] or c["chain_survivors"] != [5]:
                c8_ok = False
    fate34 = [kg for kg in OLD_44 if kg not in F68_10]
    assert len(fate34) == 34
    fate8_ok = all(cell(s, g, 8)["state"] == "uniform_ndet"
                   and not cell(s, g, 8)["chain_determined"]
                   for s, g in fate34)
    k0867_ok = True
    for sizes in ((4, 4, 10), (4, 10, 10)):
        name = "%d,%d,%d" % tuple(sizes)
        for g in range(4):
            c = cell(list(sizes), g, 8)
            if (c["state"] != "uniform_ndet" or c["n_det"] != 0
                    or c["n"] != K0867_410_TOTALS[name][g]
                    or c["ndet_survivor_sets"] != [(3, 7)]
                    or c["chain_determined"]
                    or c["chain_survivors"] != [3, 7]):
                k0867_ok = False
    record(
        "MX6: r=8 mixed keys are exactly the published 10 (K0869) with "
        "partitions (48/51,30/33,16/19,7/10,2/4) and "
        "(63/66,42/45,24/27,13/16,4/7); determined side uniform P_5; "
        "ndet sets {{3,4,5}}; the 34 keys mixed at some r<=7 are "
        "uniformly ndet at r=8 with ndet chains (FATE); 4/10 family "
        "reproduces K0867 "
        "(counts, 0 det, sets {3,7}, chain {3,7})",
        ok8 and c8_ok and fate8_ok and k0867_ok,
        {"mixed_r8": mx8, "fate_keys": 34},
    )

    # ---- C7: r=2 explicit chain collapse on the 52 keys (K0864 I2)
    r2_ok = True
    r2_det = []
    r2_ndet = []
    for sizes, g in ALL_52:
        c = cell(sizes, g, 2)
        if c["state"] == "mixed" or not c["order_det_uniform"]:
            r2_ok = False
        cv = c["_chain_verdict"]
        for v in c["_verdicts"]:
            if (v["determined"] != cv["determined"]
                    or v["survivors"] != cv["survivors"]
                    or v["order_determined"] != cv["order_determined"]):
                r2_ok = False
            if v["order_determined"] and v["orders"] != cv["orders"]:
                r2_ok = False
        if c["state"] == "uniform_det":
            r2_det.append(kstr(sizes, g))
            if c["det_survivors"] != [(1,)] or not c["chain_determined"] \
                    or c["chain_survivors"] != [1]:
                r2_ok = False
        else:
            r2_ndet.append(kstr(sizes, g))
            if c["ndet_survivor_sets"] != [(0, 1)] or c["chain_determined"] \
                    or c["chain_survivors"] != [0, 1]:
                r2_ok = False
    record(
        "MX7: at r=2 every one of the 52 keys collapses completely to its "
        "chain value (determinacy, order determinacy, survivor, order, "
        "possible-survivor set); 24 keys (4/8, 6/8 and 4/10 families; "
        "the 16 4/8 and 6/8 keys are K0864 I2) are uniformly "
        "DETERMINED with survivor P_1; the other 28 keys are uniformly "
        "ndet with set {0,1} = chain",
        r2_ok and len(r2_det) == 24 and len(r2_ndet) == 28,
        {"det24": r2_det, "ndet28": r2_ndet},
    )

    # ---- C8: NEW 4/10-family phase structure
    ph_ok = True
    for r, surv in ((2, 1), (3, 2), (4, 3)):
        for sizes, g in F410_8:
            c = cell(sizes, g, r)
            if (c["state"] != "uniform_det"
                    or c["det_survivors"] != [(surv,)]
                    or not c["chain_determined"]
                    or c["chain_survivors"] != [surv]):
                ph_ok = False
    for r, pset in ((5, (3, 4)), (6, (3, 5)), (7, (3, 6)), (8, (3, 7))):
        for sizes, g in F410_8:
            c = cell(sizes, g, r)
            if (c["state"] != "uniform_ndet"
                    or c["ndet_survivor_sets"] != [pset]
                    or c["chain_determined"] or c["chain_survivors"] != [3, r - 1]):
                ph_ok = False
    never_mixed = all(cell(s, g, r)["state"] != "mixed"
                      for s, g in F410_8 for r in R_VALUES)
    record(
        "MX8: 4/10 family phase structure - uniformly DETERMINED at "
        "r=2,3,4 (survivors P_1,P_2,P_3 = chain) and uniformly ndet at "
        "r=5..8 with possible-survivor set exactly {3,r-1} for every "
        "profile and the chain; never mixed anywhere in r=2..8",
        ph_ok and never_mixed,
        {},
    )

    # ---- C9: ECHO (K0869) and PE (K0866)
    echo_ok = all(cell(s, g, 2)["state"] == "uniform_det"
                  and cell(s, g, 2)["det_survivors"] == [(1,)]
                  and cell(s, g, 2)["chain_survivors"] == [1]
                  for s, g in F68_10)
    echo_ok = echo_ok and all(
        cell(s, g, r)["state"] == "uniform_ndet"
        and not cell(s, g, r)["chain_determined"]
        for s, g in F68_10 for r in (3, 4, 5, 6, 7))
    pe_ok = all(cell(s, g, r)["state"] == "uniform_ndet"
               and not cell(s, g, r)["chain_determined"]
               for s, g in F49_6 for r in (2, 3, 4, 5, 6))
    record(
        "MX9: 6/8 family uniformly determined with survivor = chain at "
        "r=2 and uniformly ndet (chain ndet) at r=3..7 (K0869 ECHO); "
        "4/9 family uniformly ndet (chain ndet) at r=2..6 (K0866 PE)",
        echo_ok and pe_ok,
        {},
    )

    # ---- C10: Lemma FL redundant anchor over the whole matrix
    fl_bad = 0
    for (k, r), c in matrix.items():
        if not c["fl_ok"]:
            fl_bad += 1
    record(
        "MX10: Lemma FL anchor - possible first losers == {C_i mod r} "
        "over all 364 cells (1392 profiles x 7 r-values plus chains), "
        "0 violations",
        fl_bad == 0,
        {"cells": len(matrix), "violations": fl_bad},
    )

    # ---- C11: window table (finite observation)
    def window(keys):
        return [r for r in R_VALUES
                if any(cell(s, g, r)["state"] == "mixed"
                       for s, g in keys)]
    win = {
        "small_branch": window(SMALL_10),
        "8/9": window(F89_12),
        "4/8": window(F48_6),
        "4/9": window(F49_6),
        "6/8": window(F68_10),
        "4/10": window(F410_8),
    }
    record(
        "MX11: mixed-state activity windows over r=2..8: "
        "small-branch {3}; 8/9 {3,4,5}; 4/8 {6}; 4/9 {7}; 6/8 {8}; "
        "4/10 empty",
        (win["small_branch"] == [3] and win["8/9"] == [3, 4, 5]
         and win["4/8"] == [6] and win["4/9"] == [7]
         and win["6/8"] == [8] and win["4/10"] == []),
        {"windows": win},
    )

    # ---- assemble the public matrix (drop private verdict fields)
    pub_cells = {}
    for (k, r), c in matrix.items():
        pub_cells["%s|r%d" % (k, r)] = {
            "n": c["n"], "n_det": c["n_det"], "state": c["state"],
            "det_survivors": [list(x) for x in c["det_survivors"]],
            "ndet_survivor_sets": [list(x) for x in c["ndet_survivor_sets"]],
            "order_det_uniform": c["order_det_uniform"],
            "chain_determined": c["chain_determined"],
            "chain_survivors": c["chain_survivors"],
            "fl_ok": c["fl_ok"],
        }
    fam_cells = {
        "small_branch_10": [kstr(s, g) for s, g in SMALL_10],
        "f89_12": [kstr(s, g) for s, g in F89_12],
        "f48_6": [kstr(s, g) for s, g in F48_6],
        "f49_6": [kstr(s, g) for s, g in F49_6],
        "f68_10": [kstr(s, g) for s, g in F68_10],
        "f410_8": [kstr(s, g) for s, g in F410_8],
    }
    audit = {
        "meta": {
            "item": "K0874",
            "title": "3-branch REMO failure-family state matrix "
                "(52 keys x r=2..8)",
            "date": "2026-11-16",
            "engine_provenance": "verbatim from research/experiments/"
                "remo-k-branch-r-boundary-20261116/"
                "verify_remo_k_branch_r_boundary.py (K0864, commit "
                "3138e0e3, sha256 43adec69c0a6c5da0a43f6db6405c11376fda6c"
                "7eec8e7055f17b274c35a1edf)",
            "r_values": list(R_VALUES),
            "full_715_boundary_provenance": "inherited from K0862/K0864/"
                "K0866/K0869 (not recomputed here)",
        },
        "burnside_cap10": {
            "fix_id": fix[0], "fix_trans": fix[1],
            "fix_cyc": fix[2], "orbits": fix[3],
        },
        "families": fam_cells,
        "matrix": pub_cells,
        "windows": win,
        "machine_checks": checks,
        "summary": {
            "all_ok": all(c["ok"] for c in checks),
            "checks_total": len(checks),
        },
    }
    return audit


def compact_lines(byk):
    out = []
    for sizes, g in ALL_52:
        k = kstr(sizes, g)
        for p in sorted(byk[(tuple(sizes), g)]):
            for r in R_VALUES:
                v = verdict_of(p, r)
                out.append(json.dumps(
                    {"k": k, "r": r, "a": list(p), "d": v["determined"],
                     "od": v["order_determined"], "s": v["survivors"],
                     "fl": v["first_losers"]},
                    separators=(",", ":"), sort_keys=True))
    return out


def main():
    fix_id, fix_trans, fix_cyc, orbits = burnside_fix_counts(10)
    assert (fix_id, fix_trans, fix_cyc, orbits) == (
        84494, 3478, 125, 15863)
    profiles = constrained_profiles(10)
    assert len(profiles) == 15863
    byk = {}
    for p in profiles:
        byk.setdefault(key_of(p), []).append(p)
    assert len(byk) == 715
    for sizes, g in ALL_52:
        chain = chain_profile(sizes, g, 3)
        assert chain in byk[(tuple(sizes), g)], (sizes, g)
    matrix = compute_matrix(byk)
    audit = assemble(byk, matrix)
    audit["compact_sha256"] = hashlib.sha256(
        ("\n".join(compact_lines(byk)) + "\n").encode()).hexdigest()
    return audit


def serialize(audit):
    return json.dumps(audit, sort_keys=True, ensure_ascii=False,
                      indent=1) + "\n"


def run():
    here = os.path.dirname(os.path.abspath(__file__))
    audit1 = main()
    blob1 = serialize(audit1)
    audit2 = main()
    blob2 = serialize(audit2)
    d1 = hashlib.sha256(blob1.encode()).hexdigest()
    d2 = hashlib.sha256(blob2.encode()).hexdigest()
    if d1 != d2:
        sys.stderr.write("FATAL: two runs differ (nondeterminism)\n")
        sys.exit(1)
    # compact per-profile record (deterministic; regenerate and compare)
    fix_id, fix_trans, fix_cyc, orbits = burnside_fix_counts(10)
    profiles = constrained_profiles(10)
    byk = {}
    for p in profiles:
        byk.setdefault(key_of(p), []).append(p)
    comp = "\n".join(compact_lines(byk)) + "\n"
    comp_sha = hashlib.sha256(comp.encode()).hexdigest()
    if audit1["compact_sha256"] != comp_sha:
        sys.stderr.write("FATAL: compact regeneration differs\n")
        sys.exit(1)
    all_ok = audit1["summary"]["all_ok"]
    out_dir = os.path.join(here, "output")
    os.makedirs(out_dir, exist_ok=True)
    out_json = os.path.join(out_dir, "remo_failure_family_matrix_audit.json")
    if os.path.exists(out_json):
        with open(out_json, "rb") as f:
            committed = f.read().decode()
        if committed != blob1:
            sys.stderr.write(
                "FATAL: regenerated audit differs from committed file "
                "(sha256 %s)\n" % d1)
            sys.exit(1)
        print("OK: audit byte-identical (sha256 %s)" % d1)
    else:
        with open(out_json, "w", encoding="utf-8") as f:
            f.write(blob1)
        print("wrote %s (sha256 %s)" % (out_json, d1))
    comp_path = os.path.join(here, "matrix_profiles_compact.jsonl")
    if os.path.exists(comp_path):
        with open(comp_path, "rb") as f:
            committed = f.read().decode()
        if committed != comp:
            sys.stderr.write(
                "FATAL: regenerated compact differs from committed file\n")
            sys.exit(1)
        print("OK: compact byte-identical (sha256 %s)" % comp_sha)
    else:
        with open(comp_path, "w", encoding="utf-8") as f:
            f.write(comp)
        print("wrote %s (sha256 %s)" % (comp_path, comp_sha))
    print("AUDIT PASSED" if all_ok else "AUDIT FAILED")
    for c in audit1["machine_checks"]:
        print("  [%s] %s" % ("ok" if c["ok"] else "NG", c["name"]))
    print("audit sha256 %s" % d1)
    for r in R_VALUES:
        print("r=%d: cells=%d" % (r, sum(
            1 for k in audit1["matrix"] if k.endswith("|r%d" % r))))
    if not all_ok:
        sys.exit(1)


if __name__ == "__main__":
    run()
