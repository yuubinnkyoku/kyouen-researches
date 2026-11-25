#!/usr/bin/env python3
"""K0861 audit: REMO determinism on 3-branch (and general k-branch) point families.

Self-contained. Deterministic (no randomness, no wall clock, no network).
Python 3.11+ / stdlib only.

Checked claims (proof text: report.md in this directory /
research/knowledge/items/K0861-remo-k-branch-determinism.md):

T1 (Theorem E', orbit reduction)  On any k-branch point family (maximals
    A_1..A_k, atoms = cells lying in exactly the branches in S for each
    nonempty S subset of {1..k}), the cell-level REMO game and the
    region-count game (per-atom per-player counts + mover + active set)
    have identical outcome sets. Machine check: complete enumeration on
    k=3 chain+pair samples (r=3,4), a k=4 mixed profile, and the T5
    disagreement witnesses.
T2 (Theorem F', 3-branch chain closed form, r=3)  Explicit path formula
    reproduces the region game outcome sets exactly on the full chain grid
    (C1 in 3..5, C2 <= 7, C3 <= 9, all gamma).
T3  Chain infinite families (proofs in report.md): (6u,9u,12u) determined
    iff u even (u even => survivor P_2, u odd => {P_1,P_2});
    (6u,12u,18u) always determined with survivor P_2. Instances checked.
T4  Same-size (Delta=0) families: survivor always the K0859 Theorem D
    value regardless of atom structure. Machine-confirmed for k=2/3/4
    chains and for ALL Delta=0 profiles in the pair scan (r=3).
T5  Pair-profile census (finite, N<=13, r=3): (sizes,gamma) non-collapse.
    There exist 15 (sorted-sizes, gamma) keys with two profiles that agree
    on the size multiset and on gamma but differ in REMO survivor
    determinacy. Minimal witnesses cell-verified.

REMO rule (K0859): players 0..r-1 rotate placing stones on empty cells;
    a placement is legal while the occupied set stays inside some maximal;
    the player facing a maximal position is eliminated; ALL stones owned
    by the loser are removed; play continues with the next active player;
    if the position is still maximal the next player is eliminated too
    (chain), until one player survives.

Scope / limits (do not over-read):
- Theorem E'/F' and the quadrant families are universal proofs
  (report.md); this script checks instances and finite grids only.
- The pair scan and the (sizes,gamma) non-collapse list are FINITE
  complete computations over canonical profiles with N<=13 cells.
- r>=4 3-branch chains are census-only (no closed form).
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
# K0860 published anchors (from research/experiments/
#   remo-two-branch-determinism-20261116/output/remo_two_branch_audit.json,
#   byte-verified against main)

K0860_ANCHOR_6_9_3 = {
    2: {"determined": False, "survivors": [0, 1], "first_losers": [0, 1]},
    3: {"determined": False, "survivors": [1, 2], "first_losers": [0]},
    4: {"determined": False, "survivors": [2, 3], "first_losers": [1, 2]},
    5: {"determined": False, "survivors": [2, 4], "first_losers": [1, 4]},
    6: {"determined": False, "survivors": [2, 5], "first_losers": [0, 3]},
}

# (C1, C2) -> gamma -> (determined, survivors); K0860 published family data.
K0860_FAMILIES = {
    (3, 6): {g: (False, [1, 2]) for g in range(3)},
    (5, 7): {g: (True, [0]) for g in range(5)},
    (8, 10): {g: (False, [1, 2]) for g in range(8)},
    (11, 13): {g: (True, [0]) for g in range(11)},
    (14, 16): {g: (False, [1, 2]) for g in range(14)},
    (6, 12): {g: (True, [2]) for g in range(6)},
    (12, 24): {g: (True, [2]) for g in range(12)},
    (6, 9): {g: (False, [1, 2]) for g in range(6)},
    (12, 18): {g: (True, [2]) for g in range(12)},
    (18, 27): {g: (False, [1, 2]) for g in range(18)},
}


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
# main audit


def main():
    checks = []

    def record(name, ok, detail=None):
        entry = {"name": name, "ok": bool(ok)}
        if detail is not None:
            entry["detail"] = detail
        checks.append(entry)
        print("  [%s] %s" % ("ok" if ok else "NG", name))

    audit = {}

    # ---- T0: Theorem D recursion == K0859 published table
    entries, mism = theorem_d_table()
    record(
        "K0859 Theorem D recursion == published uniform elimination table "
        "(C=1..12 x r=2..8)",
        mism == 0,
        {"entries": entries, "mismatches": mism},
    )

    # ---- T1a: k=2 regression: region game == K0860 closed form (r=3 grid)
    mism = 0
    skipped = 0
    fam = 0
    for C1 in range(3, 13):
        for C2 in range(C1 + 1, 13):
            for g in range(0, C1):
                atoms = make_atoms((C1 - g, C2 - g, g), 2)
                v, _ = region_verdict(atoms, 2, 3)
                if v is None:
                    skipped += 1
                    continue
                fam += 1
                cf = outcome_summary(sorted(closed_form_r3_two_branch(C1, C2, g)))
                if v != cf:
                    mism += 1
    record(
        "k=2 regression: region game == K0860 closed form (r=3 grid)",
        mism == 0 and skipped == 0,
        {"families": fam, "mismatches": mism, "skipped": skipped},
    )

    # ---- T1b: K0860 anchor (6,9,g=3), r=2..6
    ok = True
    for r in range(2, 7):
        co, cstates, cskip = cell_game_k(make_atoms((3, 6, 3), 2), 2, r)
        exp = K0860_ANCHOR_6_9_3[r]
        ok = ok and not cskip
        got = outcome_summary(sorted(co))
        ok = ok and got["determined"] == exp["determined"]
        ok = ok and got["survivors"] == exp["survivors"]
        ok = ok and got["first_losers"] == exp["first_losers"]
    record(
        "K0860 anchor (6,9,g=3) r=2..6 survivor sets",
        ok,
    )

    # ---- T1c: K0860 published family verdicts reproduced (all gamma)
    ok = True
    for (C1, C2), bygamma in sorted(K0860_FAMILIES.items()):
        for g, (det, surv) in sorted(bygamma.items()):
            atoms = make_atoms((C1 - g, C2 - g, g), 2)
            v, _ = region_verdict(atoms, 2, 3)
            ok = ok and v is not None
            if v is None:
                continue
            if v["determined"] != det or v["survivors"] != surv:
                ok = False
    record(
        "K0860 published family verdicts reproduced (10 families, all gamma)",
        ok,
        {"families": len(K0860_FAMILIES)},
    )

    # ---- T1d: K0860 r=4 determined example (4,6) all gamma
    ok = True
    for g in range(0, 4):
        atoms = make_atoms((4 - g, 6 - g, g), 2)
        v, _ = region_verdict(atoms, 2, 4)
        ok = ok and v is not None and v["determined"] and v["survivors"] == [3]
    record(
        "K0860 r=4 determined examples (4,6) all gamma",
        ok,
    )

    # ---- T2a: k=2 same-size (Delta=0) chain: region singleton == Theorem D
    ok = True
    inst = 0
    for C in range(2, 9):
        for g in range(0, C):
            atoms = chain_profile((C, C), g, 2)
            for r in (3, 4):
                v, _ = region_verdict(atoms, 2, r)
                elim, surv = theorem_d(C, r)
                inst += 1
                ok = ok and v is not None and v["determined"]
                ok = ok and v["survivors"] == [surv]
                ok = ok and sorted(v["orders"]) == [list(elim)]
    record(
        "k=2 same-size (Delta=0) chain: region singleton == Theorem D "
        "(C=2..8, all gamma, r=3,4)",
        ok,
        {"instances": inst},
    )

    # ---- T3a: k=3 chain r=3: region game == Theorem F' closed form
    grid_stats = {
        "families": 0,
        "determined": 0,
        "nondetermined": 0,
        "determined_and_order_determined": 0,
        "gamma_dependent_size_triples": [],
        "smallest_nondetermined": None,
    }
    by_triple = {}
    mism = 0
    skipped = 0
    for C1 in range(3, 6):
        for C2 in range(C1, 8):
            for C3 in range(C2, 10):
                for g in range(0, C1):
                    atoms = chain_profile((C1, C2, C3), g, 3)
                    v, _ = region_verdict(atoms, 3, 3)
                    if v is None:
                        skipped += 1
                        continue
                    grid_stats["families"] += 1
                    cf = outcome_summary(
                        sorted(closed_form_r3_chain3(C1, C2, C3, g))
                    )
                    if v != cf:
                        mism += 1
                    if v["first_losers"] != sorted(
                        {c % 3 for c in (C1, C2, C3)}
                    ):
                        mism += 1
                    if v["determined"]:
                        grid_stats["determined"] += 1
                        if v["order_determined"]:
                            grid_stats["determined_and_order_determined"] += 1
                    else:
                        grid_stats["nondetermined"] += 1
                        key = (C1 + C2 + C3, C1, C2, C3, g)
                        cand = {
                            "sizes": [C1, C2, C3],
                            "gamma": g,
                            "survivors": v["survivors"],
                            "_key": key,
                        }
                        cur = grid_stats["smallest_nondetermined"]
                        if cur is None or key < cur["_key"]:
                            grid_stats["smallest_nondetermined"] = cand
                    by_triple.setdefault((C1, C2, C3), set()).add(
                        v["determined"]
                    )
    grid_stats["gamma_dependent_size_triples"] = sorted(
        [list(t) for t, d in by_triple.items() if len(d) > 1]
    )
    if grid_stats["smallest_nondetermined"] is not None:
        grid_stats["smallest_nondetermined"].pop("_key")
    record(
        "k=3 chain r=3: region game == Theorem F' closed form",
        mism == 0 and skipped == 0,
        {"families": grid_stats["families"], "mismatches": mism,
         "skipped": skipped},
    )
    audit["chain3_r3_grid"] = grid_stats

    # ---- T3b: chain 3-branch infinite families
    ok = True
    inst = 0
    for u in (1, 2):
        for g in range(0, 6 * u):
            v, _ = region_verdict(chain_profile((6 * u, 9 * u, 12 * u), g, 3), 3, 3)
            cf = outcome_summary(
                sorted(closed_form_r3_chain3(6 * u, 9 * u, 12 * u, g))
            )
            inst += 1
            ok = ok and v == cf and v["determined"] == (u % 2 == 0)
            if u % 2 == 0:
                ok = ok and v["survivors"] == [2]
    for u in (1, 2):
        for g in range(0, 6 * u):
            v, _ = region_verdict(
                chain_profile((6 * u, 12 * u, 18 * u), g, 3), 3, 3
            )
            cf = outcome_summary(
                sorted(closed_form_r3_chain3(6 * u, 12 * u, 18 * u, g))
            )
            inst += 1
            ok = ok and v == cf and v["determined"] and v["survivors"] == [2]
    record(
        "chain 3-branch infinite families: (6u,9u,12u) det iff u even; "
        "(6u,12u,18u) always det P_2",
        ok,
        {"instances": inst},
    )

    # ---- T2b: k=3 same-size (Delta=0) chain: region singleton == Theorem D
    ok = True
    inst = 0
    for C in range(3, 8):
        for g in range(0, C):
            atoms = chain_profile((C, C, C), g, 3)
            for r in (3, 4):
                v, _ = region_verdict(atoms, 3, r)
                elim, surv = theorem_d(C, r)
                inst += 1
                ok = ok and v is not None and v["determined"]
                ok = ok and v["survivors"] == [surv]
                ok = ok and sorted(v["orders"]) == [list(elim)]
    record(
        "k=3 same-size (Delta=0) chain: region singleton == Theorem D "
        "(C=3..7, all gamma, r=3,4)",
        ok,
        {"instances": inst},
    )

    # ---- T2c: k=3 chain r=4,5,6 census
    r456 = {}
    ok = True
    for r in (4, 5, 6):
        fam = 0
        det = 0
        skipped = 0
        smallest = None
        for C1 in range(3, 6):
            for C2 in range(C1, 7):
                for C3 in range(C2, 8):
                    for g in range(0, C1):
                        atoms = chain_profile((C1, C2, C3), g, 3)
                        v, _ = region_verdict(atoms, 3, r)
                        if v is None:
                            skipped += 1
                            continue
                        fam += 1
                        if v["determined"]:
                            det += 1
                        elif smallest is None:
                            smallest = [C1, C2, C3, g]
        r456[str(r)] = {
            "families": fam,
            "determined": det,
            "skipped": skipped,
            "smallest_nondetermined": smallest,
        }
        ok = ok and skipped == 0 and fam == 103 and smallest == [3, 3, 4, 0]
    record(
        "k=3 chain r=4,5,6 census completed (no budget skips)",
        ok,
        {"4": r456["4"]["families"], "5": r456["5"]["families"],
         "6": r456["6"]["families"]},
    )
    audit["chain3_r456_census"] = r456

    # ---- T4a: Theorem E' machine check: cell-level == region game (k=3)
    cell_region_pairs = []
    mism = 0
    skips = 0
    for atoms in [
        chain_profile((4, 5, 6), 2, 3),
        chain_profile((4, 6, 7), 2, 3),
        chain_profile((5, 7, 7), 3, 3),
        chain_profile((3, 3, 4), 1, 3),
        make_atoms((1, 1, 1, 1, 2, 0, 1), 3),  # {12} pair atom present
        make_atoms((2, 1, 1, 1, 2, 1, 1), 3),  # {13},{23} pair atoms present
        make_atoms((1, 1, 0, 1, 2, 2, 2), 3),  # {13},{23} pair atoms, gamma=2
        make_atoms((2, 2, 2, 2, 1, 1, 1), 3),  # all three pair atoms, gamma=1
    ]:
        for r in (3, 4):
            co, cstates, cskip = cell_game_k(atoms, 3, r)
            v, _ = region_verdict(atoms, 3, r)
            if cskip or v is None:
                skips += 1
                continue
            cv = outcome_summary(sorted(co))
            cell_region_pairs.append(
                {
                    "atoms": list(atoms),
                    "r": r,
                    "cell_states": cstates,
                    "match": cv == v,
                }
            )
            if cv != v:
                mism += 1
    record(
        "Theorem E' machine check: cell-level == region game "
        "(k=3, chain+pair samples, r=3,4)",
        mism == 0 and skips == 0,
        {"instances": len(cell_region_pairs), "mismatches": mism,
         "skipped": skips},
    )
    audit["cell_vs_region_k3"] = cell_region_pairs

    # ---- T4b: k=4 same-size (Delta=0) chain: region singleton == Theorem D
    ok = True
    inst = 0
    for C in (2, 3):
        for g in range(0, C):
            atoms = chain_profile((C, C, C, C), g, 4)
            for r in (3, 4):
                v, _ = region_verdict(atoms, 4, r)
                elim, surv = theorem_d(C, r)
                inst += 1
                ok = ok and v is not None and v["determined"]
                ok = ok and v["survivors"] == [surv]
                ok = ok and sorted(v["orders"]) == [list(elim)]
    record(
        "k=4 same-size (Delta=0) chain: region singleton == Theorem D "
        "(C=2,3, all gamma, r=3,4)",
        ok,
        {"instances": inst},
    )

    # ---- T4c: Theorem E' machine check on a k=4 varied profile
    atoms4 = make_atoms((1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1), 4)
    co, cstates, cskip = cell_game_k(atoms4, 4, 3)
    v4, rstates = region_verdict(atoms4, 4, 3)
    ok = (not cskip) and v4 is not None
    if ok:
        ok = outcome_summary(sorted(co)) == v4
    audit["k4_varied_profile"] = {
        "atoms": list(atoms4),
        "r": 3,
        "cell_states": cstates,
        "region_states": rstates,
        "match": ok,
    }
    record(
        "Theorem E' machine check: cell-level == region game "
        "(k=4 varied profile, r=3)",
        ok,
        {"cell_states": cstates},
    )

    # ---- T5a: pair-profile scan (canonical, N<=13)
    NMAX = 13
    profiles = enumerate_profiles(NMAX)
    verdicts = {}
    skipped = 0
    for atoms in profiles:
        v, _ = region_verdict(atoms, 3, 3)
        if v is None:
            skipped += 1
            continue
        sizes = profile_sizes(atoms, 3)
        gamma = atoms[6]
        verdicts[atoms] = (tuple(sorted(sizes)), gamma, v)
    record(
        "pair-profile scan r=3 (N<=%d, canonical): completed without budget "
        "skips" % NMAX,
        skipped == 0,
        {"canonical_profiles": len(profiles), "skipped": skipped},
    )

    # Delta=0 profiles in scan: survivor singleton == Theorem D (r=3)
    d0_ok = True
    d0_n = 0
    for atoms, (sizes, gamma, v) in verdicts.items():
        if len(set(sizes)) != 1:
            continue
        d0_n += 1
        C = sizes[0]
        _, surv = theorem_d(C, 3)
        if not (v["determined"] and v["survivors"] == [surv]):
            d0_ok = False
    record(
        "Delta=0 profiles in scan: all singleton == Theorem D (r=3)",
        d0_ok,
        {"profiles": d0_n},
    )

    # group by (sorted sizes, gamma)
    by_sg = {}
    for atoms, (sizes, gamma, v) in verdicts.items():
        by_sg.setdefault((sizes, gamma), []).append((atoms, v))
    sg_disagreements = []
    for key in sorted(by_sg):
        group = by_sg[key]
        if len({v["determined"] for _, v in group}) > 1:
            det_side = [(a, v) for a, v in group if v["determined"]]
            ndet_side = [(a, v) for a, v in group if not v["determined"]]
            det_min = min(det_side, key=lambda av: sum(av[0]))
            ndet_min = min(ndet_side, key=lambda av: sum(av[0]))
            sg_disagreements.append(
                {
                    "sizes": list(key[0]),
                    "gamma": key[1],
                    "determined_example": {
                        "atoms": list(det_min[0]),
                        "cells": sum(det_min[0]),
                        "survivors": det_min[1]["survivors"],
                    },
                    "nondetermined_example": {
                        "atoms": list(ndet_min[0]),
                        "cells": sum(ndet_min[0]),
                        "survivors": ndet_min[1]["survivors"],
                    },
                }
            )
    # group by sizes only
    by_sizes = {}
    for c, (sizes, gamma, v) in verdicts.items():
        by_sizes.setdefault(sizes, set()).add(v["determined"])
    sizes_disagreements = sorted(
        s for s, d in by_sizes.items() if len(d) > 1
    )
    audit["pair_scan_r3"] = {
        "nmax": NMAX,
        "canonical_profiles": len(profiles),
        "determined_count": sum(
            1 for (_, _, v) in verdicts.values() if v["determined"]
        ),
        "size_multiset_disagreements": [list(s) for s in sizes_disagreements],
        "sizes_gamma_disagreements": sg_disagreements,
        "delta0_profiles_checked": d0_n,
    }

    # ---- T5b: cell-level confirmation of the minimal disagreement witnesses
    witness_profiles = [
        (chain_profile((3, 3, 8), 0, 3), "chain (3,3,8) g=0 (determined side)"),
        ((1, 1, 1, 6, 1, 1, 0), "sizes (3,3,8) g=0 determined witness"),
        ((1, 1, 0, 4, 2, 2, 0), "sizes (3,3,8) g=0 nondetermined witness"),
        ((1, 1, 1, 7, 0, 1, 0), "sizes (2,3,8) g=0 determined witness"),
        ((1, 1, 0, 5, 1, 2, 0), "sizes (2,3,8) g=0 nondetermined witness"),
    ]
    ok_w = True
    for atoms, label in witness_profiles:
        co, cstates, cskip = cell_game_k(atoms, 3, 3)
        v, _ = region_verdict(atoms, 3, 3)
        ok_w = ok_w and (not cskip) and v is not None and outcome_summary(
            sorted(co)
        ) == v
        if label.endswith("nondetermined witness"):
            ok_w = ok_w and not v["determined"]
        elif label.endswith("determined witness"):
            ok_w = ok_w and v["determined"]
    record(
        "Theorem E' + T5 witnesses: cell-level == region game on the minimal "
        "(sizes,gamma) disagreement profiles",
        ok_w,
        {"witnesses": len(witness_profiles)},
    )

    # ---- assemble
    sys.stderr.write("all checks done: %d\n" % len(checks))
    all_ok = all(c["ok"] for c in checks)
    audit["machine_checks"] = checks
    audit["summary"] = {
        "all_ok": all_ok,
        "check_count": len(checks),
        "check_names_ok": {c["name"]: c["ok"] for c in checks},
    }
    audit["meta"] = {
        "deterministic": True,
        "generated_by": "verify_remo_k_branch.py",
        "notes": [
            "Theorem E'/F' are universal proofs in report.md; machine checks instances.",
            "Finite censuses are not promoted to universal claims.",
            "11x11 empty board and class frontiers remain UNKNOWN, unrelated to this audit.",
            "solved 1407 is manifest bookkeeping only.",
        ],
        "rule": "REMO (K0859)",
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
        "remo_k_branch_audit.json",
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
    ps = audit1["pair_scan_r3"]
    print("sizes_gamma_disagreements: %d" % len(ps["sizes_gamma_disagreements"]))
    print("size_multiset_disagreements: %d" % len(
        ps["size_multiset_disagreements"]))
    for d in ps["sizes_gamma_disagreements"][:3]:
        print("  sg: %s" % json.dumps(d, sort_keys=True))
    if not all_ok:
        sys.exit(1)


if __name__ == "__main__":
    run()
