#!/usr/bin/env python3
"""Independent verification audit of K0874: 3-branch REMO 52-key
determinacy-state matrix (r = 2..8).

Self-contained. Deterministic (no randomness, no wall clock, no network).
Python 3.11+ / stdlib only.  Engine (region/cell games, profile
enumeration, Burnside machinery) is verbatim from the K0862 verifier
(research/experiments/remo-k-branch-collapse-boundary-20261116/
verify_remo_k_branch_boundary.py).

This audit independently re-derives, from the engine alone, the full
determinacy-state matrix of the 52 tracked keys (44 published non-collapse
keys of K0862/K0864/K0866/K0869 plus the 8 keys of the (4,4,10)/(4,10,10)
family) over r = 2..8, and compares every published anchor.  It is the
independent-verification companion of K0874
(research/experiments/remo-failure-family-matrix-20261116).

Checked claims (18 machine checks):

W1   cap=10 enumeration anchor: direct canonicalized enumeration (15863
     profiles) == Burnside orbit count with the published fix counts.
W2   tracked key set: 52 keys = 44 published non-collapse keys
     (r=3..8 union) + 8 keys of the (4,4,10)/(4,10,10) family.
W3   full 52 x (r=2..8) matrix: per (key, r): profile count, collapse
     state, uniform-determined survivor / non-determined survivor-set
     variety / mixed decided counts, chain value, first-loser residues.
W4   for each r in 2..8 the mixed keys among the 52 are EXACTLY the
     published non-collapse list of that r (r=2: none; r=3: 22 keys
     K0862; r=4, r=5: 12 keys K0864; r=6: 6 keys K0864; r=7: 6 keys
     K0866; r=8: 10 keys K0869).
W5   Theorem I anchor (r=2): every profile on all 52 keys collapses to
     the chain value (determinacy + possible-survivor set).
W6   Theorem G' anchor: every uniform-determined cell has survivor ==
     chain survivor.
W7   published partition anchors: r=7 (4,4,9)/(4,9,9) (K0866), r=8
     (6,6,8)/(6,8,8) (K0869), r=3 (8,8,9)/(8,9,9) (K0864), and the r=8
     (4,4,10)/(4,10,10) target sweep (K0867: uniform non-determined,
     survivor sets {3,7}).
W8   residue lens (K0872): every mixed cell has exactly the published
     first-loser residue pair of its r.
W9   family activity windows: mixed / uniform-determined /
     uniform-non-determined r-sets match the K0874 published matrix for
     all 15 families.
W10  (4,4,10)/(4,10,10) family: uniformly DETERMINED at r=2,3,4 and
     uniformly NON-determined at r=5..8 (empty mixed window; the full row
     agrees with the K0874 published matrix).

Scope / limits (do not over-read):
- The matrix is complete over the finite domain stated (52 keys, all
  their cap<=10 canonical profiles, r=2..8) - via Theorem E' it applies
  to every board realizing such a profile.  It is NOT a claim about all
  cap<=10 keys or other r.
- Independent verification means: same engine, independently written
  driver; all published constants are machine-extracted from the
  published audit JSONs and byte-verified against main.
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
# byte-verified against main.
PUBLISHED_UNIFORM_ELIMINATION_TABLE_JSON = (
    '{"1":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[1,2],"survivor":0},"4":{"elimination":[1,2,3],"survivor":0},"5":{"elimination":[1,2,3,4],"survivor":0},"6":{"elimination":[1,2,3,4,5],"survivor":0},"7":{"elimination":[1,2,3,4,5,6],"survivor":0},"8":{"elimination":[1,2,3,4,5,6,7],"survivor":0}},"10":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[1,0],"survivor":2},"4":{"elimination":[2,1,0],"survivor":3},"5":{"elimination":[0,3,2,1],"survivor":4},"6":{"elimination":[4,0,3,2,1],"survivor":5},"7":{"elimination":[3,5,0,4,2,1],"survivor":6},"8":{"elimination":[2,4,6,0,5,3,1],"survivor":7}},"11":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[2,1],"survivor":0},"4":{"elimination":[3,2,1],"survivor":0},"5":{"elimination":[1,4,3,2],"survivor":0},"6":{"elimination":[5,1,4,3,2],"survivor":0},"7":{"elimination":[4,6,1,5,3,2],"survivor":0},"8":{"elimination":[3,5,7,1,6,4,2],"survivor":0}},"12":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[0,1],"survivor":2},"4":{"elimination":[0,1,2],"survivor":3},"5":{"elimination":[2,0,1,3],"survivor":4},"6":{"elimination":[0,3,1,2,4],"survivor":5},"7":{"elimination":[5,0,3,1,2,4],"survivor":6},"8":{"elimination":[4,6,0,3,1,2,5],"survivor":7}},"2":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[2,0],"survivor":1},"4":{"elimination":[2,3,0],"survivor":1},"5":{"elimination":[2,3,4,0],"survivor":1},"6":{"elimination":[2,3,4,5,0],"survivor":1},"7":{"elimination":[2,3,4,5,6,0],"survivor":1},"8":{"elimination":[2,3,4,5,6,7,0],"survivor":1}},"3":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[0,2],"survivor":1},"4":{"elimination":[3,0,2],"survivor":1},"5":{"elimination":[3,4,0,2],"survivor":1},"6":{"elimination":[3,4,5,0,2],"survivor":1},"7":{"elimination":[3,4,5,6,0,2],"survivor":1},"8":{"elimination":[3,4,5,6,7,0,2],"survivor":1}},"4":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[1,0],"survivor":2},"4":{"elimination":[0,2,1],"survivor":3},"5":{"elimination":[4,0,2,1],"survivor":3},"6":{"elimination":[4,5,0,2,1],"survivor":3},"7":{"elimination":[4,5,6,0,2,1],"survivor":3},"8":{"elimination":[4,5,6,7,0,2,1],"survivor":3}},"5":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[2,1],"survivor":0},"4":{"elimination":[1,3,2],"survivor":0},"5":{"elimination":[0,2,4,3],"survivor":1},"6":{"elimination":[5,0,2,4,3],"survivor":1},"7":{"elimination":[5,6,0,2,4,3],"survivor":1},"8":{"elimination":[5,6,7,0,2,4,3],"survivor":1}},"6":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[0,1],"survivor":2},"4":{"elimination":[2,0,1],"survivor":3},"5":{"elimination":[1,3,0,2],"survivor":4},"6":{"elimination":[0,2,4,1,3],"survivor":5},"7":{"elimination":[6,0,2,4,1,3],"survivor":5},"8":{"elimination":[6,7,0,2,4,1,3],"survivor":5}},"7":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[1,2],"survivor":0},"4":{"elimination":[3,1,2],"survivor":0},"5":{"elimination":[2,4,1,3],"survivor":0},"6":{"elimination":[1,3,5,2,4],"survivor":0},"7":{"elimination":[0,2,4,6,3,5],"survivor":1},"8":{"elimination":[7,0,2,4,6,3,5],"survivor":1}},"8":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[2,0],"survivor":1},"4":{"elimination":[0,3,1],"survivor":2},"5":{"elimination":[3,0,4,1],"survivor":2},"6":{"elimination":[2,4,0,5,1],"survivor":3},"7":{"elimination":[1,3,5,0,6,2],"survivor":4},"8":{"elimination":[0,2,4,6,1,7,3],"survivor":5}},"9":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[0,2],"survivor":1},"4":{"elimination":[1,0,3],"survivor":2},"5":{"elimination":[4,1,0,3],"survivor":2},"6":{"elimination":[3,5,1,0,4],"survivor":2},"7":{"elimination":[2,4,6,1,0,5],"survivor":3},"8":{"elimination":[1,3,5,7,2,0,6],"survivor":4}}}'
)


class Budget(Exception):
    """Deterministic node-budget guard (machine-independent)."""


# ---------------------------------------------------------------------------
# generic helpers


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


# ---------------------------------------------------------------------------
# atom profiles


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
    # distinctness / maximality: cell in singleton atom i lies in A_i only,
    # so A_i is not a subset of any A_j (i != j) - guaranteed by the assert.
    return sizes


def chain_profile(sizes, gamma, k):
    """Common-core chain: only the all-branches atom and singletons."""
    atoms = [0] * ((1 << k) - 1)
    atoms[(1 << k) - 2] = gamma  # mask (1<<k)-1 (all branches)
    for i in range(1, k + 1):
        atoms[(1 << (i - 1)) - 1] = sizes[i - 1] - gamma
    return tuple(atoms)


def make_atoms(atoms_body, k):
    assert len(atoms_body) == (1 << k) - 1
    return tuple(atoms_body)


# ---------------------------------------------------------------------------
# cell-level REMO on the explicit k-branch point family


def cell_game_k(atoms, k, r, budget=1_500_000):
    check_profile(atoms, k)
    sizes = profile_sizes(atoms, k)
    # cells: atom m occupies [base[m], base[m]+atoms[m])
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


# ---------------------------------------------------------------------------
# region game (Theorem E')
# state: per-atom per-player counts + mover + active set.


def region_game_k(atoms, k, r, budget=1_500_000):
    check_profile(atoms, k)
    sizes = profile_sizes(atoms, k)
    natoms = (1 << k) - 1
    # star masks: star[i] = bitmask of atoms containing branch i
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


# ---------------------------------------------------------------------------
# K0859 Theorem D counting recursion (independent implementation)


def theorem_d(C, r):
    """Theorem D arithmetic recursion: elimination order and survivor.

    Returns (elimination tuple, survivor) for a uniform board (all
    maximal safe sets have size C) with r players, P_0 to move first.
    Deterministic function of (C, r) only.
    """
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


# ---------------------------------------------------------------------------
# closed forms


def closed_form_r3_two_branch(C1, C2, g):
    outcomes = set()
    for (L1, CX) in ((C1, "A"), (C2, "B")):
        lam = L1 % 3
        o = (L1 - lam) // 3
        sp = L1 - o
        dips = ["locked"]
        if o >= (C1 if CX == "A" else C2) - g:
            dips.append("free")
        for dip in dips:
            L2s = [C1 if CX == "A" else C2] if dip == "locked" else [C1, C2]
            for L2 in L2s:
                l2 = L2 - sp
                assert l2 >= 1
                loser2 = (lam + 1 + (l2 % 2)) % 3
                outcomes.add(((lam, loser2), (-lam - loser2) % 3))
    return frozenset(outcomes)


def closed_form_r3_chain3(C1, C2, C3, g):
    """Theorem F': 3-branch chain family, r=3. Requires C1 >= 3."""
    assert min(C1, C2, C3) >= 3 and g < C1
    outcomes = set()
    for L1 in (C1, C2, C3):
        lam = L1 % 3
        o = (L1 - lam) // 3
        sp = L1 - o
        assert o >= 1
        dips = ["locked"]
        if o >= L1 - g:
            dips.append("free")
        for dip in dips:
            L2s = [L1] if dip == "locked" else [C1, C2, C3]
            for L2 in L2s:
                l2 = L2 - sp
                assert l2 >= 1
                loser2 = (lam + 1 + (l2 % 2)) % 3
                outcomes.add(((lam, loser2), (-lam - loser2) % 3))
    return frozenset(outcomes)



# ---------------------------------------------------------------------------
# canonical profile enumeration (branch permutations)


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
    singles = [(1 << (i - 1)) - 1 for i in range(1, k + 1)]  # atom indices
    pair_idx = [m - 1 for m in range(1, 1 << k) if m not in
                [1, 2, 4, 8][:k] and bin(m).count("1") >= 2]
    # recursive enumeration over atom counts
    profiles = []
    seen = set()

    def rec(idx, atoms, total):
        if idx == natoms:
            rep = orbit_representative(tuple(atoms), k, perms)
            if rep not in seen:
                seen.add(rep)
                profiles.append(rep)
            return
        # singles first (indices in `singles`), then pair atoms
        lo = 1 if idx in singles else 0
        for v in range(lo, nmax - total + 1):
            atoms.append(v)
            rec(idx + 1, atoms, total + v)
            atoms.pop()

    rec(0, [], 0)
    return profiles

# ---------------------------------------------------------------------------
# in-process verdict cache (pure memoization of a deterministic function;
# identical results, halves the double-run audit time)

_VERDICT_CACHE = {}


def region_verdict_cached(atoms, k, r, budget=20_000_000):
    key = (atoms, k, r)
    got = _VERDICT_CACHE.get(key)
    if got is None:
        got = region_verdict(atoms, k, r, budget)
        _VERDICT_CACHE[key] = got
    return got


# ---------------------------------------------------------------------------
# K0861 published non-collapse keys (N<=13 census), machine-extracted from
# research/experiments/remo-k-branch-determinism-20261116/output/
#   remo_k_branch_audit.json (pair_scan_r3.sizes_gamma_disagreements),
# byte-verified against main (sha256 598b22ac61dbdea9f30bd8b1e7dabefb2f
#   4a26a1319d53f583c54f7645cc318a).
K0861_FAILING_15 = [
    ([2, 3, 8], 0), ([2, 3, 8], 1), ([2, 8, 9], 0), ([2, 8, 9], 1),
    ([3, 3, 8], 0), ([3, 3, 8], 1), ([3, 8, 8], 0), ([3, 8, 8], 1),
    ([3, 8, 9], 0), ([3, 8, 9], 1), ([8, 8, 9], 3), ([8, 8, 9], 4),
    ([8, 8, 9], 5), ([8, 9, 9], 4), ([8, 9, 9], 5),
]

# Theorem H expected failing keys (complete cap<=10 domain, r=3):
# exactly these 22 (sorted-sizes, gamma) keys have profiles disagreeing on
# REMO survivor determinacy. Every one contains a branch of size exactly 8;
# no key with a size-10 branch (and no key with 9s but no 8) fails.
EXPECTED_FAILING_22 = [
    ([2, 3, 8], 0), ([2, 3, 8], 1), ([2, 8, 9], 0), ([2, 8, 9], 1),
    ([3, 3, 8], 0), ([3, 3, 8], 1), ([3, 8, 8], 0), ([3, 8, 8], 1),
    ([3, 8, 9], 0), ([3, 8, 9], 1),
] + [([8, 8, 9], g) for g in range(6)] + [([8, 9, 9], g) for g in range(6)]

# Burnside cross-check expectations (independent orbit counting).
EXPECTED_BURNSIDE = {
    7: {"fix_id": 9929, "fix_trans": 753, "fix_cyc": 50, "orbits": 2048},
    10: {"fix_id": 84494, "fix_trans": 3478, "fix_cyc": 125, "orbits": 15863},
}


def burnside_fix_counts(cap):
    """Fixed-point counts of the constrained profile set D_cap under S_3.

    D_cap = atom-count vectors v (7 masks: excl-A, excl-B, A&B, excl-C,
    A&C, B&C, core) with v >= 0, singleton atoms v[0], v[1], v[3] >= 1,
    and branch sums |A|, |B|, |C| <= cap.  Burnside over S_3 (branch
    permutations preserve branch sums, so D_cap is invariant).
    """
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
    # transposition (A B): v0=v1>=1, v4=v5, v2 free, v3>=1 free, v6 free
    fix_trans = 0
    for a in range(1, cap + 1):
        for b in range(0, cap + 1):
            for c in range(1, cap + 1):
                for d in range(0, cap + 1):
                    m = min(cap - a - b - d, cap - c - 2 * d)
                    if m >= 0:
                        fix_trans += m + 1
    # 3-cycle: v0=v1=v3>=1, v2=v4=v5, v6 free
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
# driver: independent verification of K0874 (52-key state matrix, r=2..8)

# Published non-collapse (mixed) key lists per r, machine-extracted from
# the K0862/K0864/K0866/K0869 published audits (byte-verified against
# main): r=3 K0862, r=4..6 K0864, r=7 K0866, r=8 K0869.
PUBLISHED_MIXED = {"r2_mixed": [], "r3_mixed": [[[2, 3, 8], 0], [[2, 3, 8], 1], [[2, 8, 9], 0], [[2, 8, 9], 1], [[3, 3, 8], 0], [[3, 3, 8], 1], [[3, 8, 8], 0], [[3, 8, 8], 1], [[3, 8, 9], 0], [[3, 8, 9], 1], [[8, 8, 9], 0], [[8, 8, 9], 1], [[8, 8, 9], 2], [[8, 8, 9], 3], [[8, 8, 9], 4], [[8, 8, 9], 5], [[8, 9, 9], 0], [[8, 9, 9], 1], [[8, 9, 9], 2], [[8, 9, 9], 3], [[8, 9, 9], 4], [[8, 9, 9], 5]], "r4_mixed": [[[8, 8, 9], 0], [[8, 8, 9], 1], [[8, 8, 9], 2], [[8, 8, 9], 3], [[8, 8, 9], 4], [[8, 8, 9], 5], [[8, 9, 9], 0], [[8, 9, 9], 1], [[8, 9, 9], 2], [[8, 9, 9], 3], [[8, 9, 9], 4], [[8, 9, 9], 5]], "r5_mixed": [[[8, 8, 9], 0], [[8, 8, 9], 1], [[8, 8, 9], 2], [[8, 8, 9], 3], [[8, 8, 9], 4], [[8, 8, 9], 5], [[8, 9, 9], 0], [[8, 9, 9], 1], [[8, 9, 9], 2], [[8, 9, 9], 3], [[8, 9, 9], 4], [[8, 9, 9], 5]], "r6_mixed": [[[4, 4, 8], 0], [[4, 4, 8], 1], [[4, 4, 8], 2], [[4, 8, 8], 0], [[4, 8, 8], 1], [[4, 8, 8], 2]], "r7_mixed": [[[4, 4, 9], 0], [[4, 4, 9], 1], [[4, 4, 9], 2], [[4, 9, 9], 0], [[4, 9, 9], 1], [[4, 9, 9], 2]], "r8_mixed": [[[6, 6, 8], 0], [[6, 6, 8], 1], [[6, 6, 8], 2], [[6, 6, 8], 3], [[6, 6, 8], 4], [[6, 8, 8], 0], [[6, 8, 8], 1], [[6, 8, 8], 2], [[6, 8, 8], 3], [[6, 8, 8], 4]]}

# K0872 published first-loser residue pairs per r (cap<=10 non-collapse
# keys all share exactly one residue pair per r).
EXPECTED_RESIDUE_PAIRS = {
    3: [0, 2], 4: [0, 1], 5: [3, 4], 6: [2, 4], 7: [2, 4], 8: [0, 6],
}

# K0866 published r=7 partition counts for the (4,4,9)/(4,9,9) failing
# keys (gamma=0..2), machine-extracted from
# research/experiments/remo-k-branch-r7-extension-20261116/output/
#   remo_k_branch_r7_extension_audit.json (partition_49_r7).
PUBLISHED_R7_PARTITIONS = {"4,4,9|0": {"n_det": 16, "profiles": 20}, "4,4,9|1": {"n_det": 7, "profiles": 10}, "4,4,9|2": {"n_det": 2, "profiles": 4}, "4,9,9|0": {"n_det": 39, "profiles": 45}, "4,9,9|1": {"n_det": 22, "profiles": 28}, "4,9,9|2": {"n_det": 7, "profiles": 13}}

# K0869 published r=8 partition counts for the (6,6,8)/(6,8,8) failing
# keys (gamma=0..4), machine-extracted from
# research/experiments/remo-k-branch-r8-sweep-20261116/output/
#   remo_k_branch_r8_sweep_audit.json (failing_partition_and_witnesses).
PUBLISHED_R8_PARTITIONS = {"6,6,8|0": {"n_det": 48, "profiles": 51}, "6,6,8|1": {"n_det": 30, "profiles": 33}, "6,6,8|2": {"n_det": 16, "profiles": 19}, "6,6,8|3": {"n_det": 7, "profiles": 10}, "6,6,8|4": {"n_det": 2, "profiles": 4}, "6,8,8|0": {"n_det": 63, "profiles": 66}, "6,8,8|1": {"n_det": 42, "profiles": 45}, "6,8,8|2": {"n_det": 24, "profiles": 27}, "6,8,8|3": {"n_det": 13, "profiles": 16}, "6,8,8|4": {"n_det": 4, "profiles": 7}}

# K0867 published r=8 full sweep of the (4,4,10)/(4,10,10) target family
# (gamma=0..3), machine-extracted from
# research/experiments/remo-k-branch-r8-target-refutation-20261116/output/
#   audit.json.
PUBLISHED_R8_TARGET_4_10 = {"4,10,10|0": {"profiles": 51, "survivor_sets": {"3,7": 51}}, "4,10,10|1": {"profiles": 32, "survivor_sets": {"3,7": 32}}, "4,10,10|2": {"profiles": 15, "survivor_sets": {"3,7": 15}}, "4,10,10|3": {"profiles": 7, "survivor_sets": {"3,7": 7}}, "4,4,10|0": {"profiles": 20, "survivor_sets": {"3,7": 20}}, "4,4,10|1": {"profiles": 10, "survivor_sets": {"3,7": 10}}, "4,4,10|2": {"profiles": 4, "survivor_sets": {"3,7": 4}}, "4,4,10|3": {"profiles": 1, "survivor_sets": {"3,7": 1}}}

# K0864 published r=3/r=4/r=5 partition counts for (8,8,9)/(8,9,9).
PUBLISHED_R3_PARTITIONS_89 = {"8,8,9|0": {"n_det_r3_r4_r5": [92, 92, 92], "n_det_r6": 0, "profiles": 100}, "8,8,9|1": {"n_det_r3_r4_r5": [62, 62, 62], "n_det_r6": 0, "profiles": 70}, "8,8,9|2": {"n_det_r3_r4_r5": [40, 40, 40], "n_det_r6": 0, "profiles": 48}, "8,8,9|3": {"n_det_r3_r4_r5": [22, 22, 22], "n_det_r6": 0, "profiles": 30}, "8,8,9|4": {"n_det_r3_r4_r5": [10, 10, 10], "n_det_r6": 0, "profiles": 18}, "8,8,9|5": {"n_det_r3_r4_r5": [3, 3, 3], "n_det_r6": 0, "profiles": 9}, "8,9,9|0": {"n_det_r3_r4_r5": [102, 102, 102], "n_det_r6": 0, "profiles": 110}, "8,9,9|1": {"n_det_r3_r4_r5": [72, 72, 72], "n_det_r6": 0, "profiles": 80}, "8,9,9|2": {"n_det_r3_r4_r5": [46, 46, 46], "n_det_r6": 0, "profiles": 54}, "8,9,9|3": {"n_det_r3_r4_r5": [28, 28, 28], "n_det_r6": 0, "profiles": 36}, "8,9,9|4": {"n_det_r3_r4_r5": [13, 13, 13], "n_det_r6": 0, "profiles": 21}, "8,9,9|5": {"n_det_r3_r4_r5": [4, 4, 4], "n_det_r6": 0, "profiles": 12}}

# Family activity windows over the 52 tracked keys, machine-extracted
# from the K0874 published audit output
# (research/experiments/remo-failure-family-matrix-20261116/output/
#   remo_failure_family_matrix_audit.json, field "matrix").
EXPECTED_WINDOWS = {"2,3,8": {"det": [], "mixed": [3], "ndet": [2, 4, 5, 6, 7, 8]}, "2,8,9": {"det": [], "mixed": [3], "ndet": [2, 4, 5, 6, 7, 8]}, "3,3,8": {"det": [], "mixed": [3], "ndet": [2, 4, 5, 6, 7, 8]}, "3,8,8": {"det": [], "mixed": [3], "ndet": [2, 4, 5, 6, 7, 8]}, "3,8,9": {"det": [], "mixed": [3], "ndet": [2, 4, 5, 6, 7, 8]}, "4,10,10": {"det": [2, 3, 4], "mixed": [], "ndet": [5, 6, 7, 8]}, "4,4,10": {"det": [2, 3, 4], "mixed": [], "ndet": [5, 6, 7, 8]}, "4,4,8": {"det": [2], "mixed": [6], "ndet": [3, 4, 5, 7, 8]}, "4,4,9": {"det": [], "mixed": [7], "ndet": [2, 3, 4, 5, 6, 8]}, "4,8,8": {"det": [2], "mixed": [6], "ndet": [3, 4, 5, 7, 8]}, "4,9,9": {"det": [], "mixed": [7], "ndet": [2, 3, 4, 5, 6, 8]}, "6,6,8": {"det": [2], "mixed": [8], "ndet": [3, 4, 5, 6, 7]}, "6,8,8": {"det": [2], "mixed": [8], "ndet": [3, 4, 5, 6, 7]}, "8,8,9": {"det": [], "mixed": [3, 4, 5], "ndet": [2, 6, 7, 8]}, "8,9,9": {"det": [], "mixed": [3, 4, 5], "ndet": [2, 6, 7, 8]}}


def _tracked_keys():
    keys = []
    seen = set()
    for r in range(3, 9):
        for sp, g in PUBLISHED_MIXED["r%d_mixed" % r]:
            k = (tuple(sp), g)
            if k not in seen:
                seen.add(k)
                keys.append(k)
    for fam in ((4, 4, 10), (4, 10, 10)):
        for g in range(4):
            keys.append((fam, g))
    return keys


def famstr(k):
    return ",".join(map(str, k[0]))


def constrained_vectors(cap):
    """All raw atom vectors (v0,v1,v2,v3,v4,v5,v6) with singleton atoms
    v0,v1,v3 >= 1 and branch sums <= cap (the Burnside fix_id domain)."""
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
                                for v6 in range(0, m + 1):
                                    yield (v0, v1, v2, v3, v4, v5, v6)


def direct_constrained(cap):
    """Canonical profiles with branch sizes <= cap (direct constrained
    enumeration + verbatim orbit canonicalization)."""
    perms = branch_perms(3)
    seen = set()
    profiles = []
    for vec in constrained_vectors(cap):
        rep = orbit_representative(vec, 3, perms)
        if rep not in seen:
            seen.add(rep)
            profiles.append(rep)
    return profiles


def kstr(k):
    return "%s|%d" % (",".join(map(str, k[0])), k[1])


def main():
    audit = {}
    checks = []

    def record(name, ok, data):
        checks.append({"name": name, "ok": bool(ok), "data": data})

    # ---- W1: enumeration anchor (direct == Burnside at cap 10)
    fi, ft, fc, orbits = burnside_fix_counts(10)
    profs10 = direct_constrained(10)
    exp = EXPECTED_BURNSIDE[10]
    record(
        "cap=10 enumeration anchor: direct == Burnside (15863 profiles, "
        "published fix counts)",
        orbits == len(profs10) == exp["orbits"]
        and (fi, ft, fc) == (exp["fix_id"], exp["fix_trans"], exp["fix_cyc"]),
        {"orbits": orbits, "enum": len(profs10)},
    )
    by_key = {}
    for atoms in profs10:
        by_key.setdefault(key_of(atoms), []).append(atoms)

    keys = _tracked_keys()
    record(
        "tracked key set: 52 keys = 44 published non-collapse keys "
        "(r=3..8 union) + 8 keys of the (4,4,10)/(4,10,10) family",
        len(keys) == 52
        and all(k in by_key and by_key[k] for k in keys),
        {"keys": len(keys)},
    )

    # ---- W2/W3: the full 52 x (r=2..8) matrix
    matrix = {}
    for k in keys:
        profs = by_key[k]
        cell = {}
        for r in range(2, 9):
            verd = []
            for atoms in profs:
                v, _ = region_verdict_cached(atoms, 3, r)
                assert v is not None
                verd.append(v)
            dets = {v["determined"] for v in verd}
            entry = {
                "profiles": len(profs),
                "collapsed": len(dets) == 1,
                "uniform_det": dets == {True},
                "uniform_ndet": dets == {False},
            }
            if dets == {True}:
                entry["survivors"] = sorted(
                    {tuple(v["survivors"]) for v in verd}
                )
            else:
                entry["survivor_set_variety"] = sorted(
                    tuple(sorted(v["survivors"])) for v in verd
                )
                entry["survivor_set_varieties"] = len(
                    {tuple(sorted(v["survivors"])) for v in verd}
                )
            if len(dets) > 1:
                entry["decided"] = sum(
                    1 for v in verd if v["determined"]
                )
            ch = chain_profile(k[0], k[1], 3)
            vch, _ = region_verdict_cached(ch, 3, r)
            entry["chain_determined"] = vch["determined"]
            entry["chain_survivors"] = vch["survivors"]
            entry["first_loser_residues"] = sorted(
                {c % r for c in k[0]}
            )
            cell[str(r)] = entry
        matrix[kstr(k)] = cell

    # ---- W4: mixed cells per r == published non-collapse lists
    for r in range(2, 9):
        mixed = sorted(
            k for k in keys
            if not matrix[kstr(k)][str(r)]["collapsed"]
        )
        expected = sorted(
            (tuple(sp), g) for sp, g in PUBLISHED_MIXED["r%d_mixed" % r]
        )
        record(
            "r=%d: mixed keys among the 52 == published non-collapse list "
            "(%d keys)" % (r, len(expected)),
            mixed == expected,
            {"mixed": len(mixed)},
        )

    # ---- W5: Theorem I r=2 anchor: every profile == chain on all 52 keys
    r2_ok = True
    for k in keys:
        c = matrix[kstr(k)]["2"]
        if not c["collapsed"]:
            r2_ok = False
            continue
        ch = chain_profile(k[0], k[1], 3)
        vch, _ = region_verdict_cached(ch, 3, 2)
        for atoms in by_key[k]:
            v, _ = region_verdict_cached(atoms, 3, 2)
            if (
                v["determined"] != vch["determined"]
                or sorted(v["survivors"]) != sorted(vch["survivors"])
            ):
                r2_ok = False
    record(
        "Theorem I r=2 anchor: all 52 keys collapse fully to the chain "
        "value (determinacy + possible-survivor set)",
        r2_ok,
        {"keys": 52},
    )

    # ---- W6: Theorem G' anchor: uniform-det cells agree with the chain
    gp_mism = 0
    gp_cells = 0
    for k in keys:
        for r in range(2, 9):
            c = matrix[kstr(k)][str(r)]
            if c["uniform_det"]:
                gp_cells += 1
                if not (
                    c["chain_determined"]
                    and c["survivors"] == [tuple(c["chain_survivors"])]
                ):
                    gp_mism += 1
    record(
        "Theorem G' anchor: all uniform-determined cells (r=2..8) have "
        "survivor == chain survivor",
        gp_mism == 0,
        {"cells": gp_cells, "mismatches": gp_mism},
    )

    # ---- W7: published partition anchors
    ok7 = True
    for kk, v in PUBLISHED_R7_PARTITIONS.items():
        sp, g = kk.split("|")
        k = (tuple(int(x) for x in sp.split(",")), int(g))
        c = matrix[kstr(k)]["7"]
        if (
            c.get("decided", 0) != v["n_det"]
            or c["profiles"] != v["profiles"]
        ):
            ok7 = False
    record(
        "r=7 partition counts for (4,4,9)/(4,9,9) match the K0866 "
        "published table",
        ok7,
        {"families_checked": len(PUBLISHED_R7_PARTITIONS)},
    )
    ok8 = True
    for kk, v in PUBLISHED_R8_PARTITIONS.items():
        sp, g = kk.split("|")
        k = (tuple(int(x) for x in sp.split(",")), int(g))
        c = matrix[kstr(k)]["8"]
        if (
            c.get("decided", 0) != v["n_det"]
            or c["profiles"] != v["profiles"]
        ):
            ok8 = False
    record(
        "r=8 partition counts for (6,6,8)/(6,8,8) match the K0869 "
        "published table",
        ok8,
        {"families_checked": len(PUBLISHED_R8_PARTITIONS)},
    )
    ok3 = True
    for kk, v in PUBLISHED_R3_PARTITIONS_89.items():
        sp, g = kk.split("|")
        k = (tuple(int(x) for x in sp.split(",")), int(g))
        c = matrix[kstr(k)]["3"]
        if (
            c.get("decided", 0) != v["n_det_r3_r4_r5"][0]
            or c["profiles"] != v["profiles"]
        ):
            ok3 = False
    record(
        "r=3 partition counts for (8,8,9)/(8,9,9) match the K0864 "
        "published table",
        ok3,
        {"families_checked": len(PUBLISHED_R3_PARTITIONS_89)},
    )
    ok_t = True
    for kk, v in PUBLISHED_R8_TARGET_4_10.items():
        sp, g = kk.split("|")
        k = (tuple(int(x) for x in sp.split(",")), int(g))
        c = matrix[kstr(k)]["8"]
        sets = {
            tuple(int(y) for y in s.split(","))
            for s in v["survivor_sets"]
        }
        if not (
            c["uniform_ndet"]
            and c["profiles"] == v["profiles"]
            and {tuple(x) for x in c["survivor_set_variety"]} == sets
        ):
            ok_t = False
    record(
        "r=8 cells for the (4,4,10)/(4,10,10) family match K0867 "
        "(uniform non-determined, survivor sets {3,7})",
        ok_t,
        {"families_checked": len(PUBLISHED_R8_TARGET_4_10)},
    )

    # ---- W8: residue lens (K0872) on mixed cells
    res_ok = True
    for k in keys:
        for r in range(3, 9):
            c = matrix[kstr(k)][str(r)]
            if not c["collapsed"]:
                if c["first_loser_residues"] != EXPECTED_RESIDUE_PAIRS[r]:
                    res_ok = False
    record(
        "residue lens (K0872): every mixed cell has exactly the published "
        "first-loser residue pair of its r",
        res_ok,
        {"pairs": EXPECTED_RESIDUE_PAIRS},
    )

    # ---- W9: family activity windows
    windows = {}
    for k in keys:
        fam = famstr(k)
        w = windows.setdefault(
            fam, {"mixed": [], "det": [], "ndet": []}
        )
        for r in range(2, 9):
            c = matrix[kstr(k)][str(r)]
            if not c["collapsed"]:
                w["mixed"].append(r)
            elif c["uniform_det"]:
                w["det"].append(r)
            else:
                w["ndet"].append(r)
    for w in windows.values():
        for f in ("mixed", "det", "ndet"):
            w[f] = sorted(set(w[f]))
    win_ok = all(
        windows.get(fam) == exp
        for fam, exp in EXPECTED_WINDOWS.items()
    ) and len(windows) == 15
    record(
        "family activity windows: mixed r-sets, uniform-determined r-sets "
        "and uniform-non-determined r-sets match the K0874 published "
        "matrix for all 15 families",
        win_ok,
        {"families": len(windows)},
    )

    # ---- W10: (4,10) family full-row characterization
    ok410 = True
    for fam in ((4, 4, 10), (4, 10, 10)):
        for g in range(4):
            k = (fam, g)
            c = matrix[kstr(k)]
            if not (
                c["2"]["uniform_det"]
                and c["3"]["uniform_det"]
                and c["4"]["uniform_det"]
                and c["5"]["uniform_ndet"]
                and c["6"]["uniform_ndet"]
                and c["7"]["uniform_ndet"]
                and c["8"]["uniform_ndet"]
            ):
                ok410 = False
    record(
        "(4,4,10)/(4,10,10) family: uniformly DETERMINED at r=2,3,4 and "
        "uniformly NON-determined at r=5..8 (empty mixed window; the full "
        "row agrees with the K0874 published matrix)",
        ok410,
        {"keys": 8},
    )

    # ---- audit assembly
    audit["meta"] = {
        "item": "K0874-independent-verification",
        "title": "3-branch REMO 52-key determinacy-state matrix "
            "(r=2..8): family activity windows and the (4,10) family's "
            "empty window (independent verification of K0874)",
        "date": "2026-11-16",
        "engine_provenance": "verbatim from research/experiments/"
            "remo-k-branch-collapse-boundary-20261116/"
            "verify_remo_k_branch_boundary.py (K0862)",
        "keys": 52,
        "r_range": [2, 8],
    }
    audit["matrix"] = matrix
    audit["family_windows"] = windows
    audit["machine_checks"] = checks
    audit["summary"] = {
        "all_ok": all(c["ok"] for c in checks),
        "checks_total": len(checks),
    }
    return audit


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
        "remo_failure_family_matrix_independent_audit.json",
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
    if not all_ok:
        sys.exit(1)


if __name__ == "__main__":
    run()
