#!/usr/bin/env python3
"""K0862 audit: 3-branch REMO determinacy collapse boundary.

Self-contained. Deterministic (no randomness, no wall clock, no network).
Python 3.11+ / stdlib only.  Engine (region/cell games, profile
enumeration, Theorem D recursion, closed forms) is verbatim from the K0861
verifier (commit 33684f3e).

Checked claims (proof text: report.md in this directory /
research/knowledge/items/K0862-remo-k-branch-collapse-boundary.md):

G (Theorem G, cap<=7, universal over the finite family)  For every
    3-branch point family with ALL branch sizes <= 7 (2048 canonical
    atom profiles, 210 (sorted-sizes, gamma) keys, Burnside-cross-checked)
    and every r in {2,...,6}: survivor determinacy, order determinism,
    the determined survivor, and the order-determined elimination order
    each depend only on (sorted sizes, gamma), and each equals the value
    on the CHAIN profile with the same (sizes, gamma).  I.e. the k=2
    collapse phenomenon of K0860 Theorem E extends to k=3 throughout
    this domain (determinacy level; nondetermined possible-survivor
    sets still vary with atoms).
H (Theorem H, cap<=10, r=3, finite complete)  For every 3-branch family
    with branch sizes <= 10 (15863 canonical profiles, 715 keys):
    the (sizes,gamma) -> determinacy map is complete; determinacy
    fails to collapse at EXACTLY 22 keys (7 size multisets, all
    containing a size-8 branch): (2,3,8) g=0,1; (2,8,9) g=0,1;
    (3,3,8) g=0,1; (3,8,8) g=0,1; (3,8,9) g=0,1; (8,8,9) g=0..5;
    (8,9,9) g=0..5.  All 55 size multisets containing a size-10 branch
    collapse; no key with 9s but no 8 fails.  In every failing key all
    determined profiles have survivor P_1.  The 15 N<=13 keys published
    in K0861 are a subset.  Minimal witnesses cell-verified (E').
D/F' anchors  Delta=0 profiles in the cap<=10 sweep all match K0859
    Theorem D; the F' closed form matches the region game on ALL chain
    families with min C >= 3 and C <= 10.

Scope / limits (do not over-read):
- Theorems E'/F' (K0861) are universal; G and H here are COMPLETE over
  the finite parameter domains stated (all profiles with branch sizes
  <= 7 resp. <= 10, all attainable gamma, r as stated) - via E' they
  apply to every board realizing such a profile.
- Branch sizes >= 11 (and r >= 7) are NOT covered: whether further
  non-collapse keys exist there is open.
- Non-collapse of determinacy does NOT mean the outcome is constant:
  within failing keys the possible-survivor sets still depend on atoms.
- 11x11 empty board / class frontiers remain UNKNOWN, unrelated.
- solved 1407 is manifest bookkeeping only.
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


def main():
    audit = {}
    checks = []

    def record(name, ok, data):
        checks.append({"name": name, "ok": bool(ok), "data": data})

    # ---- C1: enumeration == Burnside (independent orbit counting)
    profiles7 = constrained_profiles(7)
    profiles10 = constrained_profiles(10)
    for cap, profs in ((7, profiles7), (10, profiles10)):
        fi, ft, fc, orbits = burnside_fix_counts(cap)
        exp = EXPECTED_BURNSIDE[cap]
        ok = (
            orbits == len(profs) == exp["orbits"]
            and (fi, ft, fc) == (exp["fix_id"], exp["fix_trans"], exp["fix_cyc"])
        )
        record(
            "cap=%d: canonical profile count == Burnside orbit count" % cap,
            ok,
            {
                "fix_id": fi,
                "fix_trans": ft,
                "fix_cyc": fc,
                "orbits": orbits,
                "enum_count": len(profs),
            },
        )

    # ---- C2: Theorem H sweep (cap<=10, r=3): complete (sizes,gamma) map
    verdicts10 = {}
    skipped = 0
    maxstates = 0
    for atoms in profiles10:
        v, states = region_verdict_cached(atoms, 3, 3)
        if v is None:
            skipped += 1
            continue
        maxstates = max(maxstates, states)
        verdicts10[atoms] = v
    record(
        "cap=10 sweep r=3: completed without budget skips (15863 profiles)",
        skipped == 0 and len(verdicts10) == 15863,
        {"skipped": skipped, "max_states": maxstates},
    )

    by_key = {}
    for atoms, v in verdicts10.items():
        by_key.setdefault(key_of(atoms), []).append((atoms, v))
    record(
        "cap=10 sweep r=3: 715 (sizes,gamma) keys",
        len(by_key) == 715,
        {"keys": len(by_key)},
    )

    failing = sorted(
        k for k, avs in by_key.items()
        if len({v["determined"] for _, v in avs}) > 1
    )
    failing_list = sorted([list(k[0]), k[1]] for k in failing)
    expected_list = sorted([list(sp), g] for sp, g in EXPECTED_FAILING_22)
    record(
        "Theorem H (cap<=10, r=3): non-collapse keys are exactly the 22 "
        "expected keys",
        failing_list == expected_list,
        {"failing": failing_list},
    )
    record(
        "K0861 anchor: the 15 published N<=13 keys are a subset of the 22",
        all(
            [list(sp), g] in failing_list
            for sp, g in K0861_FAILING_15
        ) and len(K0861_FAILING_15) == 15,
        {"k0861_keys": [list(s) + [g] for s, g in K0861_FAILING_15]},
    )
    record(
        "Theorem H: every failing key contains a size-8 branch",
        all(8 in k[0] for k in failing) and len(failing) == 22,
        {"failing_families": sorted({tuple(k[0]) for k in failing})},
    )
    sizes_with_10 = sorted({k[0] for k in by_key if 10 in k[0]})
    record(
        "Theorem H: all 55 size multisets containing a size-10 branch "
        "collapse (no size-10 failure)",
        all(10 not in k[0] for k in failing) and len(sizes_with_10) == 55,
        {"multisets_with_10": len(sizes_with_10)},
    )

    # failing-key uniformity + minimal witnesses
    witnesses = {}
    uni_ok = True
    ndet_sets = {}
    for k in failing:
        avs = by_key[k]
        det_side = [(a, v) for a, v in avs if v["determined"]]
        ndet_side = [(a, v) for a, v in avs if not v["determined"]]
        if {tuple(v["survivors"]) for _, v in det_side} != {(1,)}:
            uni_ok = False
        ndet_sets["%s|%d" % (",".join(map(str, k[0])), k[1])] = sorted(
            {tuple(sorted(v["survivors"])) for _, v in ndet_side}
        )
        dmin = min(det_side, key=lambda av: sum(av[0]))
        nmin = min(ndet_side, key=lambda av: sum(av[0]))
        witnesses["%s|%d" % (",".join(map(str, k[0])), k[1])] = {
            "det_atoms": list(dmin[0]),
            "det_cells": sum(dmin[0]),
            "det_survivors": dmin[1]["survivors"],
            "ndet_atoms": list(nmin[0]),
            "ndet_cells": sum(nmin[0]),
            "ndet_survivors": nmin[1]["survivors"],
        }
    record(
        "Theorem H: in every failing key all determined profiles have "
        "survivor P_1; nondetermined possible-survivor sets ⊆ {{1,2},{0,1,2}}",
        uni_ok and all(
            t in {(1, 2), (0, 1, 2)}
            for s in ndet_sets.values()
            for t in s
        ),
        {"ndet_survivor_sets": {
            k: [list(t) for t in v] for k, v in sorted(ndet_sets.items())
        }},
    )

    # ---- C3: cell-level (Theorem E') spot check on all 44 witnesses
    cell_ok = True
    cell_n = 0
    for w in witnesses.values():
        for atoms_s in (w["det_atoms"], w["ndet_atoms"]):
            atoms = tuple(atoms_s)
            outcomes, _states, skipped_cell = cell_game_k(
                atoms, 3, 3, budget=50_000_000
            )
            if skipped_cell:
                cell_ok = False
                continue
            vcell = outcome_summary(sorted(outcomes))
            vreg = verdicts10[atoms]
            cell_n += 1
            if (
                vcell["determined"] != vreg["determined"]
                or vcell["survivors"] != vreg["survivors"]
            ):
                cell_ok = False
    record(
        "Theorem E' anchor: cell-level game == region game on all 44 "
        "minimal witnesses",
        cell_ok and cell_n == 44,
        {"atoms_checked": cell_n},
    )

    # ---- C4: Theorem G (cap<=7): collapse to chain, r = 2..6
    verdicts7 = {a: verdicts10[a] for a in profiles7}
    theorem_g = {}
    for r in (2, 3, 4, 5, 6):
        if r == 3:
            verd = verdicts7
        else:
            verd = {}
            for atoms in profiles7:
                v, _ = region_verdict_cached(atoms, 3, r)
                assert v is not None
                verd[atoms] = v
        byk = {}
        for atoms, v in verd.items():
            byk.setdefault(key_of(atoms), []).append((atoms, v))
        det_dis = 0
        odet_dis = 0
        det_surv_dis = 0
        odet_value_dis = 0
        chain_det_dis = 0
        chain_odet_dis = 0
        chain_surv_dis = 0
        chain_order_dis = 0
        ndet_variety = 0
        det_keys = 0
        odet_keys = 0
        for k, avs in byk.items():
            ch = chain_profile(k[0], k[1], 3)
            vch, _ = region_verdict_cached(ch, 3, r)
            dets = {v["determined"] for _, v in avs}
            odets = {v["order_determined"] for _, v in avs}
            if len(dets) > 1:
                det_dis += 1
            if len(odets) > 1:
                odet_dis += 1
            if vch["determined"] != list(dets)[0]:
                chain_det_dis += 1
            if vch["order_determined"] != list(odets)[0]:
                chain_odet_dis += 1
            if dets == {True}:
                det_keys += 1
                survs = {tuple(v["survivors"]) for _, v in avs}
                if len(survs) > 1 or survs != {tuple(vch["survivors"])}:
                    det_surv_dis += 1
            else:
                if len({tuple(sorted(v["survivors"])) for _, v in avs}) > 1:
                    ndet_variety += 1
            if odets == {True}:
                odet_keys += 1
                orders = {tuple(v["orders"][0]) for _, v in avs}
                if len(orders) > 1 or orders != {tuple(vch["orders"][0])}:
                    odet_value_dis += 1
        n_profiles = len(verd)
        ok = (
            n_profiles == 2048
            and len(byk) == 210
            and det_dis == 0
            and odet_dis == 0
            and det_surv_dis == 0
            and odet_value_dis == 0
            and chain_det_dis == 0
            and chain_odet_dis == 0
        )
        record(
            "Theorem G (cap<=7, r=%d): determinacy + order-determinism "
            "collapse to (sizes,gamma) and equal the chain values" % r,
            ok,
            {
                "profiles": n_profiles,
                "keys": len(byk),
                "det_keys": det_keys,
                "order_det_keys": odet_keys,
                "ndet_survivor_set_variety_keys": ndet_variety,
            },
        )
        theorem_g[str(r)] = {
            "det_keys": det_keys,
            "order_det_keys": odet_keys,
            "ndet_survivor_set_variety_keys": ndet_variety,
        }

    # ---- C5: Delta=0 profiles (cap<=10, r=3) == Theorem D
    d0_n = 0
    d0_ok = True
    for atoms, v in verdicts10.items():
        sizes = tuple(sorted(profile_sizes(atoms, 3)))
        if len(set(sizes)) != 1:
            continue
        d0_n += 1
        _, surv = theorem_d(sizes[0], 3)
        if not (v["determined"] and v["survivors"] == [surv]):
            d0_ok = False
    record(
        "Delta=0 profiles in cap<=10 sweep: survivor == Theorem D (r=3)",
        d0_ok,
        {"profiles": d0_n},
    )

    # ---- C6: Theorem F' closed form on ALL chain keys (cap<=10, min C>=3)
    fp_n = 0
    fp_mism = 0
    for C1 in range(3, 11):
        for C2 in range(C1, 11):
            for C3 in range(C2, 11):
                for g in range(0, C1):
                    atoms = chain_profile((C1, C2, C3), g, 3)
                    v = verdicts10[atoms]
                    cf = outcome_summary(sorted(closed_form_r3_chain3(C1, C2, C3, g)))
                    fp_n += 1
                    if v != cf:
                        fp_mism += 1
    record(
        "Theorem F' closed form == region game on all cap<=10 chain "
        "families with min C>=3 (r=3)",
        fp_mism == 0,
        {"families": fp_n, "mismatches": fp_mism},
    )

    # ---- audit assembly
    det_map = sorted(
        [[list(k[0]), k[1], avs[0][1]["determined"]] for k, avs in by_key.items()
         if len({v["determined"] for _, v in avs}) == 1]
    )
    audit["meta"] = {
        "item": "K0862",
        "title": "3-branch REMO determinacy collapse boundary "
            "(cap<=7 full collapse, cap<=10 exact 22-key non-collapse list)",
        "date": "2026-11-16",
        "engine_provenance": "verbatim from research/experiments/"
            "remo-k-branch-determinism-20261116/verify_remo_k_branch.py "
            "(K0861, commit 33684f3e)",
        "r_values_swept": [2, 3, 4, 5, 6],
    }
    audit["burnside"] = {}
    for cap in (7, 10):
        fi, ft, fc, orbits = burnside_fix_counts(cap)
        audit["burnside"][str(cap)] = {
            "fix_id": fi,
            "fix_trans": ft,
            "fix_cyc": fc,
            "orbits": orbits,
        }
    audit["sweep_cap10_r3"] = {
        "profiles": len(profiles10),
        "keys": len(by_key),
        "det_keys": sum(
            1 for k, avs in by_key.items()
            if len({v["determined"] for _, v in avs}) == 1
            and avs[0][1]["determined"]
        ),
        "failing_keys": failing_list,
        "failing_witnesses": witnesses,
        "det_map_collapsing_keys": det_map,
    }
    audit["theorem_g_cap7"] = theorem_g
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
        "remo_k_branch_boundary_audit.json",
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
    sw = audit1["sweep_cap10_r3"]
    print("cap10 r=3: keys=%d failing=%d" % (
        sw["keys"], len(sw["failing_keys"])))
    if not all_ok:
        sys.exit(1)


if __name__ == "__main__":
    run()
