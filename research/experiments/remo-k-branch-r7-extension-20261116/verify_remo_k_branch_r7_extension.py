#!/usr/bin/env python3
"""K0866 audit: 3-branch REMO determinacy r-dependent boundary at r=7
(cap<=10; the first r beyond the K0864 r=2..6 sweep).

Self-contained. Deterministic (no randomness, no wall clock, no network).
Python 3.11+ / stdlib only. Engine (region/cell games, profile enumeration,
Theorem D recursion, K0859 published uniform-elimination table, Burnside
counting) is verbatim from the K0864 verifier
(research/experiments/remo-k-branch-r-boundary-20261116/
verify_remo_k_branch_r_boundary.py, commit 3138e0e3, sha256
43adec69c0a6c5da0a43f6db6405c11376fda6c7eec8e7055f17b274c35a1edf),
itself verbatim from the K0862/K0861 verifiers.

Checked claims (proof text: report.md in this directory /
research/knowledge/items/K0866-remo-k-branch-r7-boundary.md):

I7 (Theorem I, r=7, cap<=10, finite complete)  Over the same 15863
    canonical profiles / 715 keys: the keys at which survivor determinacy
    fails to collapse are EXACTLY the 6 keys (4,4,9) and (4,9,9) with
    gamma = 0..2. This is a THIRD family pair, different from both the
    r=3,4,5 pair (8,8,9)/(8,9,9) and the r=6 pair (4,4,8)/(4,8,8). Every
    failing key contains a size-9 branch AND a size-4 branch; NO failing
    key contains a size-8 branch (first r where size-8 necessity breaks),
    and no key with a size-10 branch fails. In every failing key the
    chain profile is DETERMINED with survivor P_3, all determined
    profiles have the same survivor as the chain (P_3), and every
    non-determined possible-survivor set is exactly {1,2,3}.
F89/F48 (fate of the previous failing families at r=7)  The 12 keys
    (8,8,9),(8,9,9) gamma=0..5 (failing at r=3,4,5) and the 6 keys
    (4,4,8),(4,8,8) gamma=0..2 (failing at r=6) are non-determined for
    EVERY profile at r=7 AND their chains are non-determined: both
    collapse to uniformly-ndet. The r=6 family's determined side
    vanishes exactly as the r=3 small-branch family's did at r>=4.
PE (pre-echo, finite observation)  The new r=7 failing families
    (4,4,9),(4,9,9) were uniformly-ndet (every profile AND the chain)
    for ALL r=2..6, gamma=0..3, mirroring how (4,4,8)/(4,8,8) slept at
    r=3,4,5 before failing at r=6. Each family pair so far has a single
    active window: {3,4,5} for the 8/9 pair, {6} for the 4/8 pair, {7}
    for the 4/9 pair (gamma=3 of the new pair already collapses at r=7:
    chain ndet).
FL7 (Lemma FL at r=7, redundant machine anchor)  Possible first losers
    == {C_i mod 7} on all 15863 profiles (0 violations); the lemma itself
    is universal (proved in K0864/report.md for all k, r).
GP7 (Theorem G' at r=7)  Every uniformly-determined key (98) has
    survivor == chain survivor and a determined chain; every uniformly
    order-determined key (55) has order == chain order. 0 mismatches.
D0 (Delta=0 anchor)  All 728 uniform profiles match the K0859 Theorem D
    recursion at r=7, and the recursion matches the published (C,r)
    table for C=1..12 x r=2..8 (84 entries, 0 mismatches).

Scope / limits (do not over-read):
- All I7/F89/F48/PE/GP7 claims are COMPLETE only over branch sizes <= 10
  and r=7 (or r=2..6 where stated); branch sizes >= 11 and r >= 8 are
  NOT covered. Whether further non-collapse keys exist there is open.
- The family-window observation (PE) is a finite observation over
  r=2..7; the structural characterization of the r-dependence (why the
  4/9 pair at r=7, whether r=8 brings (4,4,10)/(4,10,10)) is OPEN.
  The (4,4,10)/(4,10,10) gamma=0..2 prediction is a two-point
  extrapolation, NOT a theorem.
- Cell-level (Theorem E') spot anchors are NOT run at r=7: the minimal
  failing-key witnesses carry 13-18 cells and the cell game OOMs at r=7
  (even 13 cells). Theorem E' itself is universal (K0861), so the
  region-level verdicts transfer to every realizing board regardless.
- 11x11 empty board / class frontiers remain UNKNOWN, unrelated.
- solved head is manifest bookkeeping only.
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
# expected values (first computed 2026-11-16, re-derived on every run)

# K0862/K0864 anchor: Burnside fixed-point counts of the cap<=10 profile
# domain (same constant as the K0864 verifier).
EXPECTED_BURNSIDE_CAP10 = {
    "fix_id": 84494, "fix_trans": 3478, "fix_cyc": 125, "orbits": 15863,
}

EXPECTED_FAILING_R7 = [
    ([4, 4, 9], g) for g in range(3)
] + [([4, 9, 9], g) for g in range(3)]

# per-key determined-profile counts on the 6 failing keys at r=7
EXPECTED_PART_49 = {
    ("4,4,9", 0): (16, 20), ("4,4,9", 1): (7, 10), ("4,4,9", 2): (2, 4),
    ("4,9,9", 0): (39, 45), ("4,9,9", 1): (22, 28), ("4,9,9", 2): (7, 13),
}

# published profile totals (K0864 audit) for the fate checks at r=7
EXPECTED_TOTALS_89 = {
    ("8,8,9", 0): 100, ("8,8,9", 1): 70, ("8,8,9", 2): 48,
    ("8,8,9", 3): 30, ("8,8,9", 4): 18, ("8,8,9", 5): 9,
    ("8,9,9", 0): 110, ("8,9,9", 1): 80, ("8,9,9", 2): 54,
    ("8,9,9", 3): 36, ("8,9,9", 4): 21, ("8,9,9", 5): 12,
}
EXPECTED_TOTALS_48 = {
    ("4,4,8", 0): 20, ("4,4,8", 1): 10, ("4,4,8", 2): 4, ("4,4,8", 3): 1,
    ("4,8,8", 0): 39, ("4,8,8", 1): 24, ("4,8,8", 2): 11, ("4,8,8", 3): 5,
}

R7 = 7
PRE_ECHO_R = (2, 3, 4, 5, 6)


# ---------------------------------------------------------------------------
# sweep + targeted pre-echo computation.
# main() = constrained_profiles + sweep_r7 + targeted_49 + assemble.
# assemble is a pure function of its inputs.

def sweep_r7(prof10):
    verd = {}
    for a in prof10:
        v, _ = region_verdict_cached(a, 3, R7)
        assert v is not None, "budget skip at r=7 for %s" % (a,)
        verd[a] = v
    return verd


def targeted_49(prof10):
    """(4,4,9),(4,9,9) gamma=0..3 verdicts at r=2..6 (pre-echo check)."""
    t49 = {}
    for fam in ((4, 4, 9), (4, 9, 9)):
        for g in range(4):
            key = (fam, g)
            profs = [a for a in prof10 if key_of(a) == key]
            row = {}
            for r in PRE_ECHO_R:
                ndet = 0
                for a in profs:
                    v, _ = region_verdict_cached(a, 3, r)
                    assert v is not None, "budget skip at r=%d for %s" % (r, a)
                    if v["determined"]:
                        ndet += 1
                ch = chain_verdict(key, r)
                assert ch is not None
                row[str(r)] = {
                    "n_det": ndet,
                    "chain_determined": ch["determined"],
                }
            t49["%s|%d" % (",".join(map(str, fam)), g)] = {
                "profiles": len(profs), "by_r": row}
    return t49


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


def key_str(k):
    return "%s|%d" % (",".join(map(str, k[0])), k[1])


def min_witness(avs, side):
    sel = [(a, v) for a, v in avs if v["determined"] == side]
    return min(sel, key=lambda av: (sum(av[0]), av[0]))


def assemble(prof10, verd, t49):
    audit = {}
    checks = []

    def record(name, ok, data):
        checks.append({"name": name, "ok": bool(ok), "data": data})

    # ---- C1: enumeration == Burnside (K0862/K0864 anchor)
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
        "(15863, K0862/K0864 anchor)",
        ok,
        {"fix_id": fi, "fix_trans": ft, "fix_cyc": fc, "orbits": orbits,
         "enum_count": len(prof10)},
    )
    audit["burnside_cap10"] = {
        "fix_id": fi, "fix_trans": ft, "fix_cyc": fc, "orbits": orbits}

    # ---- C2: r=7 sweep completeness + key totals
    byk = group_by_key(verd)
    det_keys = sum(
        1 for k, avs in byk.items()
        if len({v["determined"] for _, v in avs}) == 1
        and avs[0][1]["determined"]
    )
    odet_keys = sum(
        1 for k, avs in byk.items()
        if len({v["order_determined"] for _, v in avs}) == 1
        and avs[0][1]["order_determined"]
    )
    record(
        "r=7 sweep: 15863 profiles, 715 keys, 0 budget skips; "
        "98 uniformly-determined keys, 55 uniformly-order-determined keys",
        len(verd) == 15863 and len(byk) == 715
        and det_keys == 98 and odet_keys == 55,
        {"profiles": len(verd), "keys": len(byk), "det_keys": det_keys,
         "odet_keys": odet_keys},
    )

    # ---- C3: Theorem I r=7 (exact 6-key boundary)
    fail = sorted(
        k for k, avs in byk.items()
        if len({v["determined"] for _, v in avs}) > 1
    )
    fl = sorted([list(k[0]), k[1]] for k in fail)
    el = sorted([list(sp), g] for sp, g in EXPECTED_FAILING_R7)
    has9 = all(9 in k[0] for k in fail)
    has4 = all(4 in k[0] for k in fail)
    no8 = all(8 not in k[0] for k in fail)
    no10 = all(10 not in k[0] for k in fail)
    uni_ok = True
    witnesses = {}
    part49 = {}
    for k in fail:
        avs = byk[k]
        vch = chain_verdict(k, R7)
        if not vch["determined"] or vch["survivors"] != [3]:
            uni_ok = False
        det = [(a, v) for a, v in avs if v["determined"]]
        ndet = [(a, v) for a, v in avs if not v["determined"]]
        if not det or not ndet:
            uni_ok = False
        if {tuple(v["survivors"]) for _, v in det} != {(3,)}:
            uni_ok = False
        if {tuple(sorted(v["survivors"])) for _, v in ndet} != {(1, 2, 3)}:
            uni_ok = False
        dmin = min_witness(avs, True)
        nmin = min_witness(avs, False)
        witnesses["%s#%d" % (key_str(k), R7)] = {
            "det_atoms": list(dmin[0]),
            "det_cells": sum(dmin[0]),
            "det_survivors": dmin[1]["survivors"],
            "ndet_atoms": list(nmin[0]),
            "ndet_cells": sum(nmin[0]),
            "ndet_survivors": nmin[1]["survivors"],
            "chain_survivors": vch["survivors"],
        }
        exp = EXPECTED_PART_49[("%s" % ",".join(map(str, k[0])), k[1])]
        nprof = len(avs)
        part49[key_str(k)] = {
            "profiles": nprof, "n_det": len(det),
            "n_ndet": len(ndet)}
        if (len(det), nprof) != exp:
            uni_ok = False
    record(
        "Theorem I r=7: non-collapse keys are exactly the 6 keys "
        "(4,4,9),(4,9,9) x g=0..2; every failing key has a 9-branch and a "
        "4-branch, NO failing key has an 8-branch (size-8 necessity "
        "breaks at r=7), none has a 10-branch; chain determined with "
        "survivor P_3; determined side uniform P_3; ndet survivor sets "
        "== {{1,2,3}}; per-key partitions match published counts",
        fl == el and has9 and has4 and no8 and no10 and uni_ok,
        {"failing": fl, "has_9": has9, "has_4": has4, "no_8": no8,
         "no_10": no10},
    )

    # ---- C4: Lemma FL at r=7
    fl_bad = 0
    for a, v in verd.items():
        sizes = profile_sizes(a, 3)
        if v["first_losers"] != sorted({c % R7 for c in sizes}):
            fl_bad += 1
    record(
        "Lemma FL at r=7: possible first losers == {C_i mod 7} on all "
        "15863 profiles (0 violations; the lemma is universal, K0864)",
        fl_bad == 0,
        {"violations": fl_bad},
    )
    audit["first_loser_violations_r7"] = fl_bad

    # ---- C5: Theorem G' at r=7
    surv_mism = 0
    ord_mism = 0
    uni_det = 0
    uni_odet = 0
    for k, avs in byk.items():
        dets = {v["determined"] for _, v in avs}
        if len(dets) == 1 and dets == {True}:
            uni_det += 1
            vch = chain_verdict(k, R7)
            if not vch["determined"]:
                surv_mism += 1
                continue
            survs = {tuple(v["survivors"]) for _, v in avs}
            if len(survs) > 1 or survs != {tuple(vch["survivors"])}:
                surv_mism += 1
        odets = {v["order_determined"] for _, v in avs}
        if len(odets) == 1 and odets == {True}:
            uni_odet += 1
            vch = chain_verdict(k, R7)
            ords = {tuple(v["orders"][0]) for _, v in avs}
            if len(ords) > 1 or ords != {tuple(vch["orders"][0])}:
                ord_mism += 1
    record(
        "Theorem G' at r=7: every uniformly-determined key has survivor "
        "== chain survivor (and a determined chain); every uniformly-"
        "order-determined key has order == chain order",
        uni_det == 98 and uni_odet == 55
        and surv_mism == 0 and ord_mism == 0,
        {"uniformly_determined_keys": uni_det,
         "uniformly_order_determined_keys": uni_odet,
         "survivor_mismatch": surv_mism, "order_mismatch": ord_mism},
    )
    audit["theorem_g_prime_r7"] = {
        "uniformly_determined_keys": uni_det,
        "uniformly_order_determined_keys": uni_odet,
        "survivor_mismatch": surv_mism, "order_mismatch": ord_mism}

    # ---- C6: Delta=0 profiles == Theorem D at r=7 + published table
    n = 0
    bad = 0
    for a, v in verd.items():
        sizes = tuple(sorted(profile_sizes(a, 3)))
        if len(set(sizes)) != 1:
            continue
        n += 1
        _, surv = theorem_d(sizes[0], R7)
        if not (v["determined"] and v["survivors"] == [surv]):
            bad += 1
    entries, mism = theorem_d_table()
    record(
        "Delta=0 profiles (cap<=10, 728) == Theorem D survivor at r=7; "
        "Theorem D recursion == K0859 published (C,r) table "
        "(84 entries incl. r=7, 0 mismatches)",
        n == 728 and bad == 0 and mism == 0 and entries == 84,
        {"profiles": n, "mismatches": bad, "table_entries": entries,
         "table_mismatches": mism},
    )
    audit["delta0_r7"] = {"profiles": n, "mismatches": bad}

    # ---- C7: fate of the (8,8,9)/(8,9,9) families at r=7
    f89 = {}
    f89_ok = True
    for fam in ((8, 8, 9), (8, 9, 9)):
        for g in range(6):
            key = (fam, g)
            profs = [a for a in prof10 if key_of(a) == key]
            ndet = sum(1 for a in profs if verd[a]["determined"])
            ch = chain_verdict(key, R7)
            if ndet != 0 or ch["determined"]:
                f89_ok = False
            if len(profs) != EXPECTED_TOTALS_89[
                    ("%s" % ",".join(map(str, fam)), g)]:
                f89_ok = False
            f89["%s|%d" % (",".join(map(str, fam)), g)] = {
                "profiles": len(profs), "n_det": ndet,
                "chain_determined": ch["determined"],
                "chain_survivors": ch["survivors"]}
    record(
        "F89: the 12 keys (8,8,9),(8,9,9) g=0..5 (failing at r=3,4,5) "
        "are non-determined for EVERY profile at r=7 and their chains "
        "are non-determined (collapse to uniformly-ndet; published "
        "profile totals reproduced)",
        f89_ok,
        {"per_key": f89},
    )
    audit["fate_89_families_r7"] = f89

    # ---- C8: fate of the (4,4,8)/(4,8,8) families at r=7
    f48 = {}
    f48_ok = True
    for fam in ((4, 4, 8), (4, 8, 8)):
        for g in range(4):
            key = (fam, g)
            profs = [a for a in prof10 if key_of(a) == key]
            ndet = sum(1 for a in profs if verd[a]["determined"])
            ch = chain_verdict(key, R7)
            if ndet != 0 or ch["determined"]:
                f48_ok = False
            if len(profs) != EXPECTED_TOTALS_48[
                    ("%s" % ",".join(map(str, fam)), g)]:
                f48_ok = False
            f48["%s|%d" % (",".join(map(str, fam)), g)] = {
                "profiles": len(profs), "n_det": ndet,
                "chain_determined": ch["determined"],
                "chain_survivors": ch["survivors"]}
    record(
        "F48: the 6 keys (4,4,8),(4,8,8) g=0..2 (failing at r=6) plus "
        "g=3 are non-determined for EVERY profile at r=7 and their "
        "chains are non-determined (the r=6 failing family collapses; "
        "its determined side vanishes exactly as the r=3 small-branch "
        "family's did at r>=4)",
        f48_ok,
        {"per_key": f48},
    )
    audit["fate_48_families_r7"] = f48

    # ---- C9: pre-echo of the new families at r=2..6
    pe_ok = True
    for name, row in t49.items():
        if row["profiles"] == 0:
            pe_ok = False
        for r in PRE_ECHO_R:
            cell = row["by_r"][str(r)]
            if cell["n_det"] != 0 or cell["chain_determined"]:
                pe_ok = False
    record(
        "PE: the new r=7 failing families (4,4,9),(4,9,9) g=0..3 were "
        "uniformly-ndet (every profile AND the chain) for ALL r=2..6 "
        "(40 key x r sweeps) - the same dormant state the (4,4,8)/(4,8,8) "
        "pair kept at r=3,4,5 before failing at r=6",
        pe_ok,
        {"targeted": t49},
    )
    audit["pre_echo_49_r2_6"] = t49

    audit["sweep_r7"] = {
        "profiles": len(verd), "keys": len(byk),
        "det_keys": det_keys, "odet_keys": odet_keys,
        "failing_keys": fl,
    }
    audit["failing_witnesses_r7"] = witnesses
    audit["partition_49_r7"] = part49
    audit["meta"] = {
        "engine_source": (
            "verbatim from research/experiments/"
            "remo-k-branch-r-boundary-20261116/"
            "verify_remo_k_branch_r_boundary.py (K0864, commit 3138e0e3)"),
        "engine_sha256": (
            "43adec69c0a6c5da0a43f6db6405c11376fda6c7"
            "eec8e7055f17b274c35a1edf"),
        "r": R7,
        "cap": 10,
        "profiles": len(prof10),
    }
    audit["machine_checks"] = checks
    audit["summary"] = {
        "n_checks": len(checks),
        "n_ok": sum(1 for c in checks if c["ok"]),
        "all_ok": all(c["ok"] for c in checks),
    }
    return audit


def main():
    prof10 = constrained_profiles(10)
    verd = sweep_r7(prof10)
    t49 = targeted_49(prof10)
    return assemble(prof10, verd, t49)


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
        "remo_k_branch_r7_extension_audit.json",
    )
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    if os.path.exists(out_path):
        with open(out_path, "rb") as f:
            committed = f.read().decode()
        if committed != blob1:
            sys.stderr.write(
                "FATAL: regenerated audit differs from committed file "
                "(sha256 %s)\n" % d1)
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
    if not all_ok:
        sys.exit(1)


if __name__ == "__main__":
    run()
