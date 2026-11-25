#!/usr/bin/env python3
"""K0875 audit: 3-branch REMO determinacy size boundary, cap <= 12 (r=3).

Self-contained. Deterministic (no randomness, no wall clock, no network).
Python 3.11+ / stdlib only.  Engine (region/cell games, profile
enumeration, Burnside machinery, Theorem D recursion, closed forms) is
verbatim from the K0862 verifier
(research/experiments/remo-k-branch-collapse-boundary-20261116/
verify_remo_k_branch_boundary.py).

Checked claims (proof text: report.md in this directory /
research/knowledge/items/K0875-remo-k-branch-cap12-boundary.md):

B    (Burnside vs direct enumeration, caps 10/11/12)  For each cap the
     Burnside fixed-point counts of the constrained profile set D_cap
     under S_3 and the direct canonicalized enumeration agree: cap=10
     (84494, 3478, 125) -> 15863 orbits; cap=11 (152171, 5299, 161) ->
     28065 orbits; cap=12 (261749, 7805, 203) -> 47595 orbits.  The
     canonical profile sets are nested: D_10 < D_11 < D_12.  Key counts
     (sorted sizes, gamma): 715 / 1001 / 1365.
H12  (Theorem H extension, cap<=12, r=3, finite complete)  For every
     3-branch family with branch sizes <= 12 (47595 canonical profiles,
     1365 keys) the determinacy non-collapse key set is EXACTLY the 22
     keys of Theorem H (cap<=10): ZERO new non-collapse keys appear.
     Every failing key contains a size-8 branch; no key containing an
     11- or 12-branch fails.  890 cap<=12 keys are 2-residue keys and all
     but the same 22 collapse.  In every failing key all determined
     profiles have survivor P_1 and the non-determined possible-survivor
     sets stay within {{1,2},{0,1,2}}.  The K0862 published witnesses
     remain valid minimal det/ndet witnesses.
FL   (Lemma FL anchor, r=3)  The possible first losers equal {C_i mod 3}
     on every cap<=12 profile.
D/F' anchors  Delta=0 profiles in the cap<=12 sweep match K0859 Theorem
     D; the F' closed form matches the region game on ALL chain families
     with min C >= 3 and C <= 12; the Theorem D recursion matches the
     K0859 published (C,r) table (84 entries).  Minimal witnesses
     cell-verified against the region game (Theorem E' anchor).

Scope / limits (do not over-read):
- H12 is COMPLETE over the finite parameter domain stated (all profiles
  with branch sizes <= 12, all attainable gamma, r=3) - via Theorem E'
  it applies to every board realizing such a profile.
- Branch sizes >= 13 and r >= 4 are NOT covered by this sweep (the r
  windows r=4..8 are covered by K0864/K0866/K0867/K0869/K0874).
- Non-collapse of determinacy does NOT mean the outcome is constant:
  within failing keys the possible-survivor sets still depend on atoms.
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
# driver: K0875 cap<=12 size boundary extension (r=3)

EXPECTED_BURNSIDE_11_12 = {
    11: {"fix_id": 152171, "fix_trans": 5299, "fix_cyc": 161, "orbits": 28065},
    12: {"fix_id": 261749, "fix_trans": 7805, "fix_cyc": 203, "orbits": 47595},
}
EXPECTED_KEYS_BY_CAP = {10: 715, 11: 1001, 12: 1365}

# K0862 published minimal witnesses (22 keys x det/ndet atom vectors),
# machine-extracted from
# research/experiments/remo-k-branch-collapse-boundary-20261116/output/
#   remo_k_branch_boundary_audit.json (sweep_cap10_r3.failing_witnesses),
# byte-verified against main.
K0862_WITNESSES = {"2,3,8|0": [[1, 1, 1, 7, 0, 1, 0], [1, 1, 0, 5, 1, 2, 0]], "2,3,8|1": [[1, 2, 0, 7, 0, 0, 1], [1, 1, 0, 6, 0, 1, 1]], "2,8,9|0": [[1, 2, 1, 4, 0, 5, 0], [1, 1, 0, 1, 1, 7, 0]], "2,8,9|1": [[1, 3, 0, 4, 0, 4, 1], [1, 1, 0, 2, 0, 6, 1]], "3,3,8|0": [[1, 1, 1, 6, 1, 1, 0], [1, 1, 0, 4, 2, 2, 0]], "3,3,8|1": [[1, 1, 1, 7, 0, 0, 1], [1, 1, 0, 5, 1, 1, 1]], "3,8,8|0": [[1, 1, 1, 1, 1, 6, 0], [1, 1, 2, 3, 0, 5, 0]], "3,8,8|1": [[1, 1, 6, 2, 0, 0, 1], [1, 1, 1, 2, 0, 5, 1]], "3,8,9|0": [[1, 2, 1, 3, 1, 5, 0], [1, 1, 1, 2, 1, 6, 0]], "3,8,9|1": [[1, 3, 0, 3, 1, 4, 1], [1, 1, 0, 1, 1, 6, 1]], "8,8,9|0": [[1, 1, 3, 1, 4, 4, 0], [1, 1, 6, 5, 1, 2, 0]], "8,8,9|1": [[1, 1, 3, 2, 3, 3, 1], [1, 1, 5, 4, 1, 2, 1]], "8,8,9|2": [[1, 1, 2, 1, 3, 3, 2], [1, 1, 4, 3, 1, 2, 2]], "8,8,9|3": [[1, 1, 2, 2, 2, 2, 3], [1, 1, 3, 2, 1, 2, 3]], "8,8,9|4": [[1, 1, 2, 3, 1, 1, 4], [1, 1, 1, 1, 2, 2, 4]], "8,8,9|5": [[1, 1, 2, 4, 0, 0, 5], [1, 1, 1, 2, 1, 1, 5]], "8,9,9|0": [[1, 1, 4, 2, 3, 4, 0], [1, 1, 6, 6, 1, 2, 0]], "8,9,9|1": [[1, 1, 3, 1, 3, 4, 1], [1, 1, 5, 5, 1, 2, 1]], "8,9,9|2": [[1, 1, 3, 2, 2, 3, 2], [1, 1, 4, 4, 1, 2, 2]], "8,9,9|3": [[1, 1, 2, 1, 2, 3, 3], [1, 1, 3, 3, 1, 2, 3]], "8,9,9|4": [[1, 1, 3, 2, 1, 1, 4], [1, 1, 2, 2, 1, 2, 4]], "8,9,9|5": [[1, 1, 3, 3, 0, 0, 5], [1, 1, 1, 1, 1, 2, 5]]}

# K0864 published r=3/r=4/r=5 partition counts for the (8,8,9)/(8,9,9)
# families, machine-extracted from
# research/experiments/remo-k-branch-r-boundary-20261116/output/
#   remo_k_branch_r_boundary_audit.json (partition_89_families),
# byte-verified against main.
K0864_PARTITION_89 = {"8,8,9|0": {"n_det_r3_r4_r5": [92, 92, 92], "n_det_r6": 0, "profiles": 100}, "8,8,9|1": {"n_det_r3_r4_r5": [62, 62, 62], "n_det_r6": 0, "profiles": 70}, "8,8,9|2": {"n_det_r3_r4_r5": [40, 40, 40], "n_det_r6": 0, "profiles": 48}, "8,8,9|3": {"n_det_r3_r4_r5": [22, 22, 22], "n_det_r6": 0, "profiles": 30}, "8,8,9|4": {"n_det_r3_r4_r5": [10, 10, 10], "n_det_r6": 0, "profiles": 18}, "8,8,9|5": {"n_det_r3_r4_r5": [3, 3, 3], "n_det_r6": 0, "profiles": 9}, "8,9,9|0": {"n_det_r3_r4_r5": [102, 102, 102], "n_det_r6": 0, "profiles": 110}, "8,9,9|1": {"n_det_r3_r4_r5": [72, 72, 72], "n_det_r6": 0, "profiles": 80}, "8,9,9|2": {"n_det_r3_r4_r5": [46, 46, 46], "n_det_r6": 0, "profiles": 54}, "8,9,9|3": {"n_det_r3_r4_r5": [28, 28, 28], "n_det_r6": 0, "profiles": 36}, "8,9,9|4": {"n_det_r3_r4_r5": [13, 13, 13], "n_det_r6": 0, "profiles": 21}, "8,9,9|5": {"n_det_r3_r4_r5": [4, 4, 4], "n_det_r6": 0, "profiles": 12}}

# K0862 published exact 22 non-collapse keys (Theorem H, cap<=10),
# machine-extracted from
# research/experiments/remo-k-branch-collapse-boundary-20261116/output/
#   remo_k_branch_boundary_audit.json, byte-verified against main.
EXPECTED_FAILING_22 = [[[2, 3, 8], 0], [[2, 3, 8], 1], [[2, 8, 9], 0], [[2, 8, 9], 1], [[3, 3, 8], 0], [[3, 3, 8], 1], [[3, 8, 8], 0], [[3, 8, 8], 1], [[3, 8, 9], 0], [[3, 8, 9], 1], [[8, 8, 9], 0], [[8, 8, 9], 1], [[8, 8, 9], 2], [[8, 8, 9], 3], [[8, 8, 9], 4], [[8, 8, 9], 5], [[8, 9, 9], 0], [[8, 9, 9], 1], [[8, 9, 9], 2], [[8, 9, 9], 3], [[8, 9, 9], 4], [[8, 9, 9], 5]]


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

    # ---- C1: Burnside vs direct enumeration at caps 10, 11, 12
    enum = {}
    audit["burnside"] = {}
    for cap in (10, 11, 12):
        fi, ft, fc, orbits = burnside_fix_counts(cap)
        profs = direct_constrained(cap)
        enum[cap] = profs
        audit["burnside"][str(cap)] = {
            "fix_id": fi, "fix_trans": ft, "fix_cyc": fc, "orbits": orbits,
        }
        if cap == 10:
            exp = EXPECTED_BURNSIDE[10]
        else:
            exp = EXPECTED_BURNSIDE_11_12[cap]
        ok = (
            orbits == len(profs) == exp["orbits"]
            and (fi, ft, fc)
            == (exp["fix_id"], exp["fix_trans"], exp["fix_cyc"])
        )
        record(
            "cap=%d: direct constrained enumeration count == Burnside orbit "
            "count (%d profiles)" % (cap, exp["orbits"]),
            ok,
            {"fix_id": fi, "fix_trans": ft, "fix_cyc": fc,
             "orbits": orbits, "enum_count": len(profs)},
        )

    # ---- C2: verbatim published enumeration path (K0862 machinery) ==
    #          direct enumeration at cap 10 (set equality)
    verb10 = constrained_profiles(10)
    ok = set(verb10) == set(enum[10]) and len(verb10) == 15863
    record(
        "cap=10: direct enumeration set == verbatim enumerate_profiles "
        "path (K0862 machinery, 15863 profiles)",
        ok,
        {"verbatim": len(verb10), "direct": len(enum[10])},
    )
    del verb10

    # ---- C3: nested inclusion of the canonical profile sets
    ok = (
        set(enum[10]) <= set(enum[11]) and set(enum[11]) <= set(enum[12])
    )
    record(
        "profile-set inclusion: cap10 subset of cap11 subset of cap12",
        ok,
        {"cap10": len(enum[10]), "cap11": len(enum[11]),
         "cap12": len(enum[12])},
    )

    # ---- C4: r=3 sweep over ALL cap<=12 profiles
    verdicts = {}
    skipped = 0
    maxstates = 0
    for atoms in enum[12]:
        v, states = region_verdict_cached(atoms, 3, 3)
        if v is None:
            skipped += 1
            continue
        maxstates = max(maxstates, states)
        verdicts[atoms] = v
    record(
        "cap=12 sweep r=3: completed without budget skips (47595 profiles)",
        skipped == 0 and len(verdicts) == 47595,
        {"skipped": skipped, "max_states": maxstates},
    )

    # ---- C5: per-cap (sizes,gamma) key maps by filtering the sweep
    by_cap = {}
    for cap in (10, 11, 12):
        sel = [a for a in enum[cap]]
        byk = {}
        for atoms in sel:
            byk.setdefault(key_of(atoms), []).append((atoms, verdicts[atoms]))
        by_cap[cap] = byk
        failing = sorted(
            k for k, avs in byk.items()
            if len({v["determined"] for _, v in avs}) > 1
        )
        failing_list = sorted([list(k[0]), k[1]] for k in failing)
        expected_list = sorted(
            [list(sp), g] for sp, g in EXPECTED_FAILING_22
        )
        record(
            "Theorem H extension (cap<=%d, r=3): non-collapse keys are "
            "exactly the published 22 keys (no new keys)" % cap,
            len(byk) == EXPECTED_KEYS_BY_CAP[cap]
            and failing_list == expected_list,
            {"keys": len(byk), "failing": len(failing_list)},
        )

    # failing-key structure at cap=12 (identical to cap<=10 by inclusion)
    byk = by_cap[12]
    failing = sorted(
        k for k, avs in byk.items()
        if len({v["determined"] for _, v in avs}) > 1
    )
    record(
        "every failing key contains a size-8 branch; no key containing an "
        "11- or 12-branch fails (cap<=12)",
        all(8 in k[0] for k in failing)
        and not any(11 in k[0] or 12 in k[0] for k in failing),
        {
            "failing_multisets": sorted({tuple(k[0]) for k in failing}),
            "keys_with_11": sum(
                1 for k in byk if 11 in k[0]
            ),
            "keys_with_12": sum(1 for k in byk if 12 in k[0]),
            "keys_with_11_or_12_failing": sum(
                1 for k in failing if 11 in k[0] or 12 in k[0]
            ),
        },
    )

    # ---- C6: 22-key fine structure (partitions, witnesses, survivors)
    partitions = {}
    witnesses = {}
    uni_ok = True
    ndet_sets = {}
    for k in failing:
        avs = byk[k]
        det = [v for _, v in avs if v["determined"]]
        ndet = [v for _, v in avs if not v["determined"]]
        partitions[kstr(k)] = {
            "n_det": len(det), "profiles": len(avs),
        }
        if {tuple(v["survivors"]) for v in det} != {(1,)}:
            uni_ok = False
        ndet_sets[kstr(k)] = sorted(
            {tuple(sorted(v["survivors"])) for v in ndet}
        )
        dmin = min(
            (a for a, v in avs if v["determined"]), key=lambda a: sum(a)
        )
        nmin = min(
            (a for a, v in avs if not v["determined"]), key=lambda a: sum(a)
        )
        witnesses[kstr(k)] = [list(dmin), list(nmin)]
    record(
        "Theorem H structure at cap<=12: det-side survivor uniformly P_1; "
        "ndet possible-survivor sets subset of {{1,2},{0,1,2}}",
        uni_ok
        and all(
            t in {(1, 2), (0, 1, 2)}
            for s in ndet_sets.values()
            for t in s
        ),
        {"ndet_survivor_sets": {
            k: [list(t) for t in v] for k, v in sorted(ndet_sets.items())
        }},
    )
    # witnesses == K0862 published (validity + minimality; exact vector
    # identity is tie-order dependent, so the published vectors are
    # verified as members with agreeing minimal cell counts)
    wit_pub = K0862_WITNESSES
    wit_ok = len(witnesses) == 22
    for k in failing:
        kk = kstr(k)
        pub = wit_pub.get(kk)
        if pub is None:
            wit_ok = False
            continue
        avs = byk[k]
        atom_set = {a for a, _ in avs}
        pub_det = tuple(pub[0])
        pub_ndet = tuple(pub[1])
        if pub_det not in atom_set or pub_ndet not in atom_set:
            wit_ok = False
            continue
        vd = verdicts[pub_det]
        vn = verdicts[pub_ndet]
        if not (
            vd["determined"]
            and vd["survivors"] == [1]
            and not vn["determined"]
            and sorted(vn["survivors"]) in ([0, 1, 2], [1, 2])
            and sum(pub_det) == sum(witnesses[kk][0])
            and sum(pub_ndet) == sum(witnesses[kk][1])
        ):
            wit_ok = False
    record(
        "K0862 published witnesses are valid minimal det/ndet witnesses "
        "for all 22 keys at cap<=12 (det survivor P_1, ndet set within "
        "{{1,2},{0,1,2}}, cell counts minimal)",
        wit_ok,
        {"witness_keys": len(witnesses)},
    )
    # K0864 published partition counts for (8,8,9)/(8,9,9)
    p89_ok = True
    for kk, v in K0864_PARTITION_89.items():
        if kk not in partitions:
            p89_ok = False
            continue
        if (
            partitions[kk]["n_det"] != v["n_det_r3_r4_r5"][0]
            or partitions[kk]["profiles"] != v["profiles"]
        ):
            p89_ok = False
    record(
        "r=3 partition counts for (8,8,9)/(8,9,9) match the K0864 "
        "published table",
        p89_ok,
        {"families": len(K0864_PARTITION_89)},
    )

    # ---- C7: residue lens (K0872): failing keys have residues {0,2}
    resid_ok = all(
        sorted({c % 3 for c in k[0]}) == [0, 2] for k in failing
    )
    two_res = sum(
        1 for k in byk if len({c % 3 for c in k[0]}) == 2
    )
    record(
        "residue lens (K0872): all 22 failing keys have first-loser "
        "residue pair {0,2} (mod 3); %d of %d cap<=12 keys are 2-residue "
        "keys and all but the 22 collapse" % (two_res, len(byk)),
        resid_ok and all(
            len({c % 3 for c in k[0]}) == 2 for k in failing
        ),
        {"two_residue_keys": two_res,
         "two_residue_collapsing": two_res - 22},
    )

    # ---- C8: Lemma FL redundant anchor (r=3): possible first losers ==
    #          {C_i mod 3} for every cap<=12 profile
    fl_viol = 0
    fl_exact = 0
    for atoms, v in verdicts.items():
        sizes = profile_sizes(atoms, 3)
        want = sorted({c % 3 for c in sizes})
        if sorted(v["first_losers"]) != want:
            fl_viol += 1
        else:
            fl_exact += 1
    record(
        "Lemma FL r=3 anchor: possible first losers == {C_i mod 3} on all "
        "cap<=12 profiles",
        fl_viol == 0 and fl_exact == len(verdicts),
        {"profiles": len(verdicts), "violations": fl_viol},
    )

    # ---- C9: Delta=0 profiles (cap<=12, r=3) == Theorem D
    d0_n = 0
    d0_ok = True
    for atoms, v in verdicts.items():
        sizes = tuple(sorted(profile_sizes(atoms, 3)))
        if len(set(sizes)) != 1:
            continue
        d0_n += 1
        _, surv = theorem_d(sizes[0], 3)
        if not (v["determined"] and v["survivors"] == [surv]):
            d0_ok = False
    record(
        "Delta=0 profiles in cap<=12 sweep: survivor == Theorem D (r=3)",
        d0_ok,
        {"profiles": d0_n},
    )

    # ---- C10: Theorem F' closed form on ALL chain keys (cap<=12, min C>=3)
    fp_n = 0
    fp_mism = 0
    for C1 in range(3, 13):
        for C2 in range(C1, 13):
            for C3 in range(C2, 13):
                for g in range(0, C1):
                    atoms = chain_profile((C1, C2, C3), g, 3)
                    v = verdicts[atoms]
                    cf = outcome_summary(
                        sorted(closed_form_r3_chain3(C1, C2, C3, g))
                    )
                    fp_n += 1
                    if v != cf:
                        fp_mism += 1
    record(
        "Theorem F' closed form == region game on all cap<=12 chain "
        "families with min C>=3 (r=3)",
        fp_mism == 0,
        {"families": fp_n, "mismatches": fp_mism},
    )

    # ---- C11: Theorem D recursion vs the K0859 published (C,r) table
    entries, mism = theorem_d_table()
    record(
        "Theorem D recursion == K0859 published (C,r) table (84 entries)",
        mism == 0 and entries == 84,
        {"entries": entries, "mismatches": mism},
    )

    # ---- C12: cell-level (Theorem E') anchors on the 44 witnesses
    cell_ok = True
    cell_n = 0
    for k in failing:
        for atoms_s in witnesses[kstr(k)]:
            atoms = tuple(atoms_s)
            outcomes, _states, skipped_cell = cell_game_k(
                atoms, 3, 3, budget=50_000_000
            )
            if skipped_cell:
                cell_ok = False
                continue
            vcell = outcome_summary(sorted(outcomes))
            vreg = verdicts[atoms]
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

    # ---- audit assembly
    det_map = sorted(
        [[list(k[0]), k[1], avs[0][1]["determined"]]
         for k, avs in byk.items()
         if len({v["determined"] for _, v in avs}) == 1]
    )
    audit["meta"] = {
        "item": "K0875",
        "title": "3-branch REMO determinacy size boundary: cap<=12 "
            "extends Theorem H with the same exact 22 non-collapse keys",
        "date": "2026-11-16",
        "engine_provenance": "verbatim from research/experiments/"
            "remo-k-branch-collapse-boundary-20261116/"
            "verify_remo_k_branch_boundary.py (K0862)",
        "r_swept": 3,
    }
    audit["sweep_cap12_r3"] = {
        "profiles": len(verdicts),
        "max_states": maxstates,
        "keys_by_cap": {str(c): len(by_cap[c]) for c in (10, 11, 12)},
        "failing_keys": sorted([list(k[0]), k[1]] for k in failing),
        "failing_partitions": partitions,
        "failing_witnesses": witnesses,
        "new_key_census": {
            "keys_with_11": sum(1 for k in byk if 11 in k[0]),
            "keys_with_12": sum(1 for k in byk if 12 in k[0]),
            "failing_with_11_or_12": sum(
                1 for k in failing if 11 in k[0] or 12 in k[0]
            ),
            "two_residue_keys": two_res,
        },
        "det_map_collapsing_keys": det_map,
    }
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
        "remo_k_branch_cap12_boundary_audit.json",
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
    sw = audit1["sweep_cap12_r3"]
    print("cap12 r=3: keys=%d failing=%d" % (
        sw["keys_by_cap"]["12"], len(sw["failing_keys"])))
    if not all_ok:
        sys.exit(1)


if __name__ == "__main__":
    run()
