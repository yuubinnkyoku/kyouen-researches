#!/usr/bin/env python3
"""K0912: three-branch REMO determinacy boundary cap<=12 x r=9 (the
size 11/12 cells of the r=9 column left open by K0893, plus the full
cap<=12 Theorem J r>=max(M,2) anchor at r=9).

Self-contained verifier (stdlib only, deterministic). Verifies the
committed cap<=12 r=9 sweep column (publication form: the packed
record file, one JSON array [i, sv_mask, fl_mask, states] per
canonical profile; atoms are a pure function of i via the canonical
enumeration, so the packing is lossless) against:

  - the canonical cap<=12 enumeration and Burnside fix counts
    (K0875 machinery, verbatim twin block below),
  - the committed K0893 cap<=10 r=9 column at the 15,863 D_10
    subsequence positions (order-preserving, K0882 property),
  - the committed cap<=12 r=2..8 columns (K0881/K0876) for the
    Theorem J (K0906) cap<=12 extension: for every key with
    M = max C_i <= 8 the r=9 det/sv must equal the r=8 column
    (sv/det constant for r >= max(M,2)); for M <= 7 also fl,
  - Lemma FL (K0864, universal): fl == {C_i mod 9} for all profiles,
  - the pinned census / mixed-key / partition / residue-census /
    ECHO constants extracted from this sweep, and
  - live Python mask-twin and verbatim-engine recomputation
    (K0893 twin semantics) on the full cap<=7 sub-range, a
    stride-32 layered cap>=8 sample of the D_10 positions, a
    stratified new-cell (size 11/12) sample, and mixed-key
    witness profiles.

Checked claims (proof text: report.md / item):

B    (Burnside vs direct enumeration, caps 10/11/12)  Identical to
     K0875/K0876/K0893 (r-independent): fix counts
     (84494,3478,125)/(152171,5299,161)/(261749,7805,203) ->
     15863/28065/47595 orbits; key counts 715/1001/1365; cap-set
     inclusion.
I912 (Theorem I r=9, cap<=12 extension; finite complete)  The
     determinacy non-collapse (mixed) key set at cap<=12, r=9 is
     EXACTLY the published K0893 cap<=10 boundary: the 7 families
     (6,6,8),(6,8,8) x g=0..4; (8,8,9),(8,9,9) x g=0..5;
     (6,6,9),(6,8,9),(6,9,9) x g=0..3 (34 keys).  ZERO new mixed
     keys contain an 11 or 12 branch: the 650 new keys split
     45 uniformly determined / 605 uniformly non-determined /
     0 mixed.  Per-key partitions are identical to K0893, det-side
     survivor uniformly P_5, all 34 chain profiles determined,
     cap<=10 sub-census 98/583/34 == K0893 published.
J12  (Theorem J cap<=12 r=9 anchor; K0906 universal theorem)  For
     every key with M = max C_i <= 8: det and survivor set at r=9
     == the committed r=8 column (0 mismatches); for M <= 7 also
     fl (C_i <= 7 < r makes {C_i mod r} = {C_i}).  All r8->r9 det
     differences lie in M=9 profiles (876, exactly the M=9 mixed
     families turning/partially determined at the r=9 threshold;
     the M=9 uniformly determined keys are exactly the Delta=0
     family (9,9,9) x g=0..8).  sv-mask differences r8->r9:
     38070 (M<=8 keys: 0).
FL9  (Lemma FL, K0864 universal; redundant anchor)  first losers
     == {C_i mod 9} for all 47595 profiles: 0 violations.
D    (Theorem D)  All 1512 uniform-size (Delta=0) profiles are
     determined with the Theorem D r=9 survivor (784 of them
     contain an 11/12 branch); Theorem D recursion == the K0859
     published (C,r) table (84 entries, r=2..8).
G9   (Theorem G' survivor level, r=9)  Every determined profile of
     a uniformly determined key carries the chain survivor
     (143 keys, 0 mismatches; includes the 45 new keys).
N    (new-key structure, finite observation)  The 650 new keys
     (363 containing 11, 364 containing 12; 31732 profiles)
     residue-class census is pinned; the 45 uniformly determined
     new keys are exactly (1,1,11)|0, (1,11,11)|0,
     (10,10,12) x g=0..9, (10,12,12) x g=0..9, (11,11,11) x
     g=0..10, (12,12,12) x g=0..11; 167/605 uniformly
     non-determined new keys have chain survivors == the union of
     possible survivors (observation, no claim).
ECHO The r=2..9 determinacy history of the 34 mixed keys across
     the committed r=2..8 columns and this r=9 column is pinned
     (echo / dormancy / revival structure unchanged by the size
     extension: (6,6,8),(6,8,8) revive at r=8-9 levels,
     (8,8,9),(8,9,9) at r=3..5 and r=9, the three 6/9 families
     awaken first at r=9).

Scope / limits (do not over-read):
- I912 is COMPLETE over the finite parameter domain stated (all
  canonical profiles with branch sizes <= 12, r=9) - via Theorem E'
  it applies to every board realizing such a profile.
- Theorem J is a universal theorem (K0906); the r=9 column is a
  machine anchor for its cap<=12 instance, not the proof.
- Branch sizes >= 13 and r >= 10 are NOT covered here.
- The mask engine does not reproduce elimination-order fields;
  order determinacy claims are NOT re-derived here.
- Uniformly non-determined does NOT mean "outcome-free"; N and
  ECHO rows are finite observations, not universal laws.
- 11x11 empty board / class frontiers remain UNKNOWN, unrelated.

The audit JSON is regenerated twice and must be byte-identical, and
byte-identical to the committed audit (fresh-checkout reproducible).

Usage: python3 verify_remo_k_branch_cap12_r9_boundary.py
"""

import hashlib
import json
import os
import sys

sys.setrecursionlimit(100000)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")

ENGINE_PATH = os.path.join(HERE, "mask_engine_fast2.js")
PACKED_PATH = os.path.join(OUT, "js_cap12_r9.packed.jsonl")
AUDIT_PATH = os.path.join(OUT, "remo_k_branch_cap12_r9_boundary_audit.json")

R278_DIR = os.path.join(HERE, "..", "remo-k-branch-cap12-r278-boundary-20261116")
R456_DIR = os.path.join(HERE, "..", "remo-k-branch-cap12-r456-boundary-20261116")
K0893_DIR = os.path.join(HERE, "..", "remo-k-branch-cap10-r9-boundary-20261117")
REF_COLUMNS = {
    r: (os.path.join(R456_DIR if r in (3, 4, 5, 6) else R278_DIR,
                     "output", "js_cap12_r%d.packed.jsonl" % r), None)
    for r in (2, 3, 4, 5, 6, 7, 8)
}
CAP10_R9_PATH = os.path.join(K0893_DIR, "output", "js_cap10_r9.packed.jsonl")


PUBLISHED_UNIFORM_ELIMINATION_TABLE_JSON = (
    '{"1":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[1,2],"survivor":0},"4":{"elimination":[1,2,3],"survivor":0},"5":{"elimination":[1,2,3,4],"survivor":0},"6":{"elimination":[1,2,3,4,5],"survivor":0},"7":{"elimination":[1,2,3,4,5,6],"survivor":0},"8":{"elimination":[1,2,3,4,5,6,7],"survivor":0}},"10":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[1,0],"survivor":2},"4":{"elimination":[2,1,0],"survivor":3},"5":{"elimination":[0,3,2,1],"survivor":4},"6":{"elimination":[4,0,3,2,1],"survivor":5},"7":{"elimination":[3,5,0,4,2,1],"survivor":6},"8":{"elimination":[2,4,6,0,5,3,1],"survivor":7}},"11":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[2,1],"survivor":0},"4":{"elimination":[3,2,1],"survivor":0},"5":{"elimination":[1,4,3,2],"survivor":0},"6":{"elimination":[5,1,4,3,2],"survivor":0},"7":{"elimination":[4,6,1,5,3,2],"survivor":0},"8":{"elimination":[3,5,7,1,6,4,2],"survivor":0}},"12":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[0,1],"survivor":2},"4":{"elimination":[0,1,2],"survivor":3},"5":{"elimination":[2,0,1,3],"survivor":4},"6":{"elimination":[0,3,1,2,4],"survivor":5},"7":{"elimination":[5,0,3,1,2,4],"survivor":6},"8":{"elimination":[4,6,0,3,1,2,5],"survivor":7}},"2":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[2,0],"survivor":1},"4":{"elimination":[2,3,0],"survivor":1},"5":{"elimination":[2,3,4,0],"survivor":1},"6":{"elimination":[2,3,4,5,0],"survivor":1},"7":{"elimination":[2,3,4,5,6,0],"survivor":1},"8":{"elimination":[2,3,4,5,6,7,0],"survivor":1}},"3":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[0,2],"survivor":1},"4":{"elimination":[3,0,2],"survivor":1},"5":{"elimination":[3,4,0,2],"survivor":1},"6":{"elimination":[3,4,5,0,2],"survivor":1},"7":{"elimination":[3,4,5,6,0,2],"survivor":1},"8":{"elimination":[3,4,5,6,7,0,2],"survivor":1}},"4":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[1,0],"survivor":2},"4":{"elimination":[0,2,1],"survivor":3},"5":{"elimination":[4,0,2,1],"survivor":3},"6":{"elimination":[4,5,0,2,1],"survivor":3},"7":{"elimination":[4,5,6,0,2,1],"survivor":3},"8":{"elimination":[4,5,6,7,0,2,1],"survivor":3}},"5":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[2,1],"survivor":0},"4":{"elimination":[1,3,2],"survivor":0},"5":{"elimination":[0,2,4,3],"survivor":1},"6":{"elimination":[5,0,2,4,3],"survivor":1},"7":{"elimination":[5,6,0,2,4,3],"survivor":1},"8":{"elimination":[5,6,7,0,2,4,3],"survivor":1}},"6":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[0,1],"survivor":2},"4":{"elimination":[2,0,1],"survivor":3},"5":{"elimination":[1,3,0,2],"survivor":4},"6":{"elimination":[0,2,4,1,3],"survivor":5},"7":{"elimination":[6,0,2,4,1,3],"survivor":5},"8":{"elimination":[6,7,0,2,4,1,3],"survivor":5}},"7":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[1,2],"survivor":0},"4":{"elimination":[3,1,2],"survivor":0},"5":{"elimination":[2,4,1,3],"survivor":0},"6":{"elimination":[1,3,5,2,4],"survivor":0},"7":{"elimination":[0,2,4,6,3,5],"survivor":1},"8":{"elimination":[7,0,2,4,6,3,5],"survivor":1}},"8":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[2,0],"survivor":1},"4":{"elimination":[0,3,1],"survivor":2},"5":{"elimination":[3,0,4,1],"survivor":2},"6":{"elimination":[2,4,0,5,1],"survivor":3},"7":{"elimination":[1,3,5,0,6,2],"survivor":4},"8":{"elimination":[0,2,4,6,1,7,3],"survivor":5}},"9":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[0,2],"survivor":1},"4":{"elimination":[1,0,3],"survivor":2},"5":{"elimination":[4,1,0,3],"survivor":2},"6":{"elimination":[3,5,1,0,4],"survivor":2},"7":{"elimination":[2,4,6,1,0,5],"survivor":3},"8":{"elimination":[1,3,5,7,2,0,6],"survivor":4}}}'
)

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
    return profile_sizes(atoms, k)


def chain_profile(sizes, gamma, k):
    """Common-core chain: only the all-branches atom and singletons."""
    atoms = [0] * ((1 << k) - 1)
    atoms[(1 << k) - 2] = gamma  # mask (1<<k)-1 (all branches)
    for i in range(1, k + 1):
        atoms[(1 << (i - 1)) - 1] = sizes[i - 1] - gamma
    return tuple(atoms)


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


# ---------------------------------------------------------------------------
# K0859 Theorem D counting recursion (independent implementation, verbatim)
# ---------------------------------------------------------------------------


def theorem_d(C, r):
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
# canonical profile enumeration (verbatim K0862 machinery via K0875)
# ---------------------------------------------------------------------------


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


def burnside_fix_counts(cap):
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


def constrained_vectors(cap):
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
    perms = branch_perms(3)
    seen = set()
    profiles = []
    for vec in constrained_vectors(cap):
        rep = orbit_representative(vec, 3, perms)
        if rep not in seen:
            seen.add(rep)
            profiles.append(rep)
    return profiles


def key_of(atoms):
    return (tuple(sorted(profile_sizes(atoms, 3))), atoms[6])


def kstr(k):
    return "%s|%d" % (",".join(map(str, k[0])), k[1])


def pkstr(p):
    return "%s|%d" % (",".join(map(str, p[0])), p[1])


# ---------------------------------------------------------------------------
# Python mask twin (independently written; cross-validated live against the
# verbatim engine every run; mirrors mask_engine.js / mask_engine_fast.js)
# ---------------------------------------------------------------------------


def mask_game(atoms, k, r, budget=50_000_000):
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

    def rec(counts, mover, active):
        key = (counts, mover, active)
        got = memo.get(key)
        if got is not None:
            return got
        nodes[0] -= 1
        if nodes[0] < 0:
            raise Budget("mask budget")
        occ = 0
        for m in range(natoms):
            if sum(counts[m]):
                occ |= 1 << m
        maximal = False
        for i in range(1, k + 1):
            if occ & ~star[i]:
                continue
            t = 0
            for m in range(natoms):
                if (star[i] >> m) & 1:
                    t += sum(counts[m])
            if t == sizes[i - 1]:
                maximal = True
                break
        if maximal:
            loser = mover
            ncounts = tuple(
                tuple(0 if p == loser else c for p, c in enumerate(counts[m]))
                for m in range(natoms)
            )
            new_active = frozenset(a for a in active if a != loser)
            if len(new_active) == 1:
                sv = 1 << next(iter(new_active))
            else:
                nm = next_active(loser, r, new_active)
                sv, _fl = rec(ncounts, nm, new_active)
            out = (sv, 1 << loser)
        else:
            svm = 0
            flm = 0
            nm = next_active(mover, r, active)
            for m in range(1, 1 << k):
                mi = m - 1
                cap = atoms[mi] - sum(counts[mi])
                if cap <= 0:
                    continue
                if any(
                    (occ & ~star[i]) == 0 and (star[i] >> mi) & 1
                    for i in range(1, k + 1)
                ):
                    inner = counts[mi]
                    bumped = (
                        counts[:mi]
                        + (inner[:mover] + (inner[mover] + 1,) + inner[mover + 1:],)
                        + counts[mi + 1:]
                    )
                    s, f = rec(bumped, nm, active)
                    svm |= s
                    flm |= f
            out = (svm, flm)
        memo[key] = out
        return out

    try:
        sv, fl = rec(zero, 0, frozenset(range(r)))
        return (sv, fl), len(memo), False
    except Budget:
        return None, len(memo), True


def mask_verdict(atoms, k, r, budget=50_000_000):
    (sv, fl), states, skipped = mask_game(atoms, k, r, budget)
    if skipped:
        return None, states
    survivors = sorted(p for p in range(r) if (sv >> p) & 1)
    first_losers = sorted(p for p in range(r) if (fl >> p) & 1)
    return {
        "determined": len(survivors) == 1,
        "survivors": survivors,
        "first_losers": first_losers,
    }, states


def verdict_triple(rec):
    return (rec["determined"], list(rec["survivors"]), list(rec["first_losers"]))

# ====PINNED====

PUBLISHED_UNIFORM_ELIMINATION_TABLE_JSON = (
    '{"1":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[1,2],"survivor":0},"4":{"elimination":[1,2,3],"survivor":0},"5":{"elimination":[1,2,3,4],"survivor":0},"6":{"elimination":[1,2,3,4,5],"survivor":0},"7":{"elimination":[1,2,3,4,5,6],"survivor":0},"8":{"elimination":[1,2,3,4,5,6,7],"survivor":0}},"10":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[1,0],"survivor":2},"4":{"elimination":[2,1,0],"survivor":3},"5":{"elimination":[0,3,2,1],"survivor":4},"6":{"elimination":[4,0,3,2,1],"survivor":5},"7":{"elimination":[3,5,0,4,2,1],"survivor":6},"8":{"elimination":[2,4,6,0,5,3,1],"survivor":7}},"11":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[2,1],"survivor":0},"4":{"elimination":[3,2,1],"survivor":0},"5":{"elimination":[1,4,3,2],"survivor":0},"6":{"elimination":[5,1,4,3,2],"survivor":0},"7":{"elimination":[4,6,1,5,3,2],"survivor":0},"8":{"elimination":[3,5,7,1,6,4,2],"survivor":0}},"12":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[0,1],"survivor":2},"4":{"elimination":[0,1,2],"survivor":3},"5":{"elimination":[2,0,1,3],"survivor":4},"6":{"elimination":[0,3,1,2,4],"survivor":5},"7":{"elimination":[5,0,3,1,2,4],"survivor":6},"8":{"elimination":[4,6,0,3,1,2,5],"survivor":7}},"2":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[2,0],"survivor":1},"4":{"elimination":[2,3,0],"survivor":1},"5":{"elimination":[2,3,4,0],"survivor":1},"6":{"elimination":[2,3,4,5,0],"survivor":1},"7":{"elimination":[2,3,4,5,6,0],"survivor":1},"8":{"elimination":[2,3,4,5,6,7,0],"survivor":1}},"3":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[0,2],"survivor":1},"4":{"elimination":[3,0,2],"survivor":1},"5":{"elimination":[3,4,0,2],"survivor":1},"6":{"elimination":[3,4,5,0,2],"survivor":1},"7":{"elimination":[3,4,5,6,0,2],"survivor":1},"8":{"elimination":[3,4,5,6,7,0,2],"survivor":1}},"4":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[1,0],"survivor":2},"4":{"elimination":[0,2,1],"survivor":3},"5":{"elimination":[4,0,2,1],"survivor":3},"6":{"elimination":[4,5,0,2,1],"survivor":3},"7":{"elimination":[4,5,6,0,2,1],"survivor":3},"8":{"elimination":[4,5,6,7,0,2,1],"survivor":3}},"5":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[2,1],"survivor":0},"4":{"elimination":[1,3,2],"survivor":0},"5":{"elimination":[0,2,4,3],"survivor":1},"6":{"elimination":[5,0,2,4,3],"survivor":1},"7":{"elimination":[5,6,0,2,4,3],"survivor":1},"8":{"elimination":[5,6,7,0,2,4,3],"survivor":1}},"6":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[0,1],"survivor":2},"4":{"elimination":[2,0,1],"survivor":3},"5":{"elimination":[1,3,0,2],"survivor":4},"6":{"elimination":[0,2,4,1,3],"survivor":5},"7":{"elimination":[6,0,2,4,1,3],"survivor":5},"8":{"elimination":[6,7,0,2,4,1,3],"survivor":5}},"7":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[1,2],"survivor":0},"4":{"elimination":[3,1,2],"survivor":0},"5":{"elimination":[2,4,1,3],"survivor":0},"6":{"elimination":[1,3,5,2,4],"survivor":0},"7":{"elimination":[0,2,4,6,3,5],"survivor":1},"8":{"elimination":[7,0,2,4,6,3,5],"survivor":1}},"8":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[2,0],"survivor":1},"4":{"elimination":[0,3,1],"survivor":2},"5":{"elimination":[3,0,4,1],"survivor":2},"6":{"elimination":[2,4,0,5,1],"survivor":3},"7":{"elimination":[1,3,5,0,6,2],"survivor":4},"8":{"elimination":[0,2,4,6,1,7,3],"survivor":5}},"9":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[0,2],"survivor":1},"4":{"elimination":[1,0,3],"survivor":2},"5":{"elimination":[4,1,0,3],"survivor":2},"6":{"elimination":[3,5,1,0,4],"survivor":2},"7":{"elimination":[2,4,6,1,0,5],"survivor":3},"8":{"elimination":[1,3,5,7,2,0,6],"survivor":4}}}'
)

# Burnside / enumeration expectations (K0875, r-independent).
EXPECTED_BURNSIDE = {
    10: {"fix_id": 84494, "fix_trans": 3478, "fix_cyc": 125, "orbits": 15863, "keys": 715},
    11: {"fix_id": 152171, "fix_trans": 5299, "fix_cyc": 161, "orbits": 28065, "keys": 1001},
    12: {"fix_id": 261749, "fix_trans": 7805, "fix_cyc": 203, "orbits": 47595, "keys": 1365},
}
N_PROFILES = 47595

# Committed sweep / engine file pins (packed column is the single
# committed source; atoms are a pure function of i).
ENGINE_SHA256 = (
    "b904760e109e9adf1689b91e7dcbb1aa530704af322ee7808e2304d0377586de"
)
PACKED_SHA256 = (
    "02e771cda84ae5178ee67a905cc9c2148e0c186790cf0562f569d9923110f32d"
)
PACKED_BYTES = 975488
REF_COLUMN_SHA256 = {
    "r2": "1fd9dbf4cb6699c26bab7f6b34a900f5877d3408603a02a2dd121ca71ef8e951",
    "r3": "ea7c66286f728a52d5696d627ce1faf7705e77f9e4222493221f3a4fe79ed134",
    "r4": "04caba43a7c0f7124db1ea81fcad4f170de04bd041699f6659e42f786e9a40b4",
    "r5": "c6dddad7a4ce39d3ebc8765187b0f16961720654918d74f54e608e12975ea693",
    "r6": "65f1cb32a9ecae6bd258056dfe8ab7c59d376d570f1d11c647b6823fd2467f1d",
    "r7": "50eb7c1ba41825dcbf726258cb2c6878a324d58bb17a708cb587d9d2b3b79c78",
    "r8": "0a884b490e28c281166754c1e82aaa73f7515580dea05b4ce023e8a1f079e8dc",
    "cap10_r9": "a2bb16bc8d03f341704d902f0a50ce4352b14ad08043cbced54b8e8f83b9973b",
}

# r=9 cap<=12 key census (this sweep).
CENSUS = {"keys": 1365, "uniform_det": 143, "uniform_ndet": 1188,
          "mixed": 34}
# cap<=10 sub-census == K0893 published.
CAP10_SUBCENSUS = {"keys": 715, "uniform_det": 98, "uniform_ndet": 583,
                   "mixed": 34}

# The 34 mixed keys (K0893 cap<=10 boundary, unchanged at cap<=12).
MIXED_KEYS = [
    [[6, 6, 8], 0],
    [[6, 6, 8], 1],
    [[6, 6, 8], 2],
    [[6, 6, 8], 3],
    [[6, 6, 8], 4],
    [[6, 6, 9], 0],
    [[6, 6, 9], 1],
    [[6, 6, 9], 2],
    [[6, 6, 9], 3],
    [[6, 8, 8], 0],
    [[6, 8, 8], 1],
    [[6, 8, 8], 2],
    [[6, 8, 8], 3],
    [[6, 8, 8], 4],
    [[6, 8, 9], 0],
    [[6, 8, 9], 1],
    [[6, 8, 9], 2],
    [[6, 8, 9], 3],
    [[6, 9, 9], 0],
    [[6, 9, 9], 1],
    [[6, 9, 9], 2],
    [[6, 9, 9], 3],
    [[8, 8, 9], 0],
    [[8, 8, 9], 1],
    [[8, 8, 9], 2],
    [[8, 8, 9], 3],
    [[8, 8, 9], 4],
    [[8, 8, 9], 5],
    [[8, 9, 9], 0],
    [[8, 9, 9], 1],
    [[8, 9, 9], 2],
    [[8, 9, 9], 3],
    [[8, 9, 9], 4],
    [[8, 9, 9], 5],
]

# Per-key partition of the 34 mixed keys at r=9 (n profiles / det /
# ndet / det-side survivor / possible ndet survivor sets) == K0893.
MIXED_PARTITION = json.loads(
"{\"6,6,8|0\": {\"det\": 48, \"dsv\": [[5]], \"n\": 51, \"ndet\": 3, \"ndet_sets\": [[3, 4, 5]]}, \"6,6,8|1\": {\"det\": 30, \"dsv\": [[5]], \"n\": 33, \"ndet\": 3, \"ndet_sets\": [[3, 4, 5]]}, \"6,6,8|2\": {\"det\": 16, \"dsv\": [[5]], \"n\": 19, \"ndet\": 3, \"ndet_sets\": [[3, 4, 5]]}, \"6,6,8|3\": {\"det\": 7, \"dsv\": [[5]], \"n\": 10, \"ndet\": 3, \"ndet_sets\": [[3, 4, 5]]}, \"6,6,8|4\": {\"det\": 2, \"dsv\": [[5]], \"n\": 4, \"ndet\": 2, \"ndet_sets\": [[3, 4, 5]]}, \"6,6,9|0\": {\"det\": 40, \"dsv\": [[5]], \"n\": 54, \"ndet\": 14, \"ndet_sets\": [[3, 4, 5], [3, 5]]}, \"6,6,9|1\": {\"det\": 22, \"dsv\": [[5]], \"n\": 34, \"ndet\": 12, \"ndet_sets\": [[3, 4, 5], [3, 5]]}, \"6,6,9|2\": {\"det\": 10, \"dsv\": [[5]], \"n\": 20, \"ndet\": 10, \"ndet_sets\": [[3, 4, 5], [3, 5]]}, \"6,6,9|3\": {\"det\": 3, \"dsv\": [[5]], \"n\": 10, \"ndet\": 7, \"ndet_sets\": [[3, 4, 5], [3, 5]]}, \"6,8,8|0\": {\"det\": 63, \"dsv\": [[5]], \"n\": 66, \"ndet\": 3, \"ndet_sets\": [[3, 4, 5]]}, \"6,8,8|1\": {\"det\": 42, \"dsv\": [[5]], \"n\": 45, \"ndet\": 3, \"ndet_sets\": [[3, 4, 5]]}, \"6,8,8|2\": {\"det\": 24, \"dsv\": [[5]], \"n\": 27, \"ndet\": 3, \"ndet_sets\": [[3, 4, 5]]}, \"6,8,8|3\": {\"det\": 13, \"dsv\": [[5]], \"n\": 16, \"ndet\": 3, \"ndet_sets\": [[3, 4, 5]]}, \"6,8,8|4\": {\"det\": 4, \"dsv\": [[5]], \"n\": 7, \"ndet\": 3, \"ndet_sets\": [[3, 4, 5]]}, \"6,8,9|0\": {\"det\": 95, \"dsv\": [[5]], \"n\": 120, \"ndet\": 25, \"ndet_sets\": [[3, 4, 5], [3, 4, 5, 7], [3, 5], [3, 5, 7]]}, \"6,8,9|1\": {\"det\": 53, \"dsv\": [[5]], \"n\": 78, \"ndet\": 25, \"ndet_sets\": [[3, 4, 5], [3, 4, 5, 7], [3, 5], [3, 5, 7]]}, \"6,8,9|2\": {\"det\": 24, \"dsv\": [[5]], \"n\": 47, \"ndet\": 23, \"ndet_sets\": [[3, 4, 5], [3, 4, 5, 7], [3, 5], [3, 5, 7]]}, \"6,8,9|3\": {\"det\": 6, \"dsv\": [[5]], \"n\": 25, \"ndet\": 19, \"ndet_sets\": [[3, 4, 5], [3, 4, 5, 7], [3, 5], [3, 5, 7]]}, \"6,9,9|0\": {\"det\": 64, \"dsv\": [[5]], \"n\": 78, \"ndet\": 14, \"ndet_sets\": [[3, 4, 5], [3, 5]]}, \"6,9,9|1\": {\"det\": 40, \"dsv\": [[5]], \"n\": 54, \"ndet\": 14, \"ndet_sets\": [[3, 4, 5], [3, 5]]}, \"6,9,9|2\": {\"det\": 19, \"dsv\": [[5]], \"n\": 33, \"ndet\": 14, \"ndet_sets\": [[3, 4, 5], [3, 5]]}, \"6,9,9|3\": {\"det\": 6, \"dsv\": [[5]], \"n\": 20, \"ndet\": 14, \"ndet_sets\": [[3, 4, 5], [3, 5]]}, \"8,8,9|0\": {\"det\": 92, \"dsv\": [[5]], \"n\": 100, \"ndet\": 8, \"ndet_sets\": [[3, 4, 5, 7], [3, 5, 7]]}, \"8,8,9|1\": {\"det\": 62, \"dsv\": [[5]], \"n\": 70, \"ndet\": 8, \"ndet_sets\": [[3, 4, 5, 7], [3, 5, 7]]}, \"8,8,9|2\": {\"det\": 40, \"dsv\": [[5]], \"n\": 48, \"ndet\": 8, \"ndet_sets\": [[3, 4, 5, 7], [3, 5, 7]]}, \"8,8,9|3\": {\"det\": 22, \"dsv\": [[5]], \"n\": 30, \"ndet\": 8, \"ndet_sets\": [[3, 4, 5, 7], [3, 5, 7]]}, \"8,8,9|4\": {\"det\": 10, \"dsv\": [[5]], \"n\": 18, \"ndet\": 8, \"ndet_sets\": [[3, 4, 5, 7], [3, 5, 7]]}, \"8,8,9|5\": {\"det\": 3, \"dsv\": [[5]], \"n\": 9, \"ndet\": 6, \"ndet_sets\": [[3, 4, 5, 6, 7], [3, 4, 5, 7], [3, 5, 7]]}, \"8,9,9|0\": {\"det\": 102, \"dsv\": [[5]], \"n\": 110, \"ndet\": 8, \"ndet_sets\": [[3, 4, 5, 7], [3, 5, 7]]}, \"8,9,9|1\": {\"det\": 72, \"dsv\": [[5]], \"n\": 80, \"ndet\": 8, \"ndet_sets\": [[3, 4, 5, 7], [3, 5, 7]]}, \"8,9,9|2\": {\"det\": 46, \"dsv\": [[5]], \"n\": 54, \"ndet\": 8, \"ndet_sets\": [[3, 4, 5, 7], [3, 5, 7]]}, \"8,9,9|3\": {\"det\": 28, \"dsv\": [[5]], \"n\": 36, \"ndet\": 8, \"ndet_sets\": [[3, 4, 5, 7], [3, 5, 7]]}, \"8,9,9|4\": {\"det\": 13, \"dsv\": [[5]], \"n\": 21, \"ndet\": 8, \"ndet_sets\": [[3, 4, 5, 7], [3, 5, 7]]}, \"8,9,9|5\": {\"det\": 4, \"dsv\": [[5]], \"n\": 12, \"ndet\": 8, \"ndet_sets\": [[3, 4, 5, 7], [3, 5, 7]]}}")

# r=2..9 determinacy history of the 34 mixed keys (det counts per
# committed column; r=9 from this sweep) - the ECHO table.
ECHO_TABLE = json.loads(
"{\"6,6,8|0\": {\"n\": 51, \"r2\": 51, \"r3\": 0, \"r4\": 0, \"r5\": 0, \"r6\": 0, \"r7\": 0, \"r8\": 48, \"r9\": 48}, \"6,6,8|1\": {\"n\": 33, \"r2\": 33, \"r3\": 0, \"r4\": 0, \"r5\": 0, \"r6\": 0, \"r7\": 0, \"r8\": 30, \"r9\": 30}, \"6,6,8|2\": {\"n\": 19, \"r2\": 19, \"r3\": 0, \"r4\": 0, \"r5\": 0, \"r6\": 0, \"r7\": 0, \"r8\": 16, \"r9\": 16}, \"6,6,8|3\": {\"n\": 10, \"r2\": 10, \"r3\": 0, \"r4\": 0, \"r5\": 0, \"r6\": 0, \"r7\": 0, \"r8\": 7, \"r9\": 7}, \"6,6,8|4\": {\"n\": 4, \"r2\": 4, \"r3\": 0, \"r4\": 0, \"r5\": 0, \"r6\": 0, \"r7\": 0, \"r8\": 2, \"r9\": 2}, \"6,6,9|0\": {\"n\": 54, \"r2\": 0, \"r3\": 0, \"r4\": 0, \"r5\": 0, \"r6\": 0, \"r7\": 0, \"r8\": 0, \"r9\": 40}, \"6,6,9|1\": {\"n\": 34, \"r2\": 0, \"r3\": 0, \"r4\": 0, \"r5\": 0, \"r6\": 0, \"r7\": 0, \"r8\": 0, \"r9\": 22}, \"6,6,9|2\": {\"n\": 20, \"r2\": 0, \"r3\": 0, \"r4\": 0, \"r5\": 0, \"r6\": 0, \"r7\": 0, \"r8\": 0, \"r9\": 10}, \"6,6,9|3\": {\"n\": 10, \"r2\": 0, \"r3\": 0, \"r4\": 0, \"r5\": 0, \"r6\": 0, \"r7\": 0, \"r8\": 0, \"r9\": 3}, \"6,8,8|0\": {\"n\": 66, \"r2\": 66, \"r3\": 0, \"r4\": 0, \"r5\": 0, \"r6\": 0, \"r7\": 0, \"r8\": 63, \"r9\": 63}, \"6,8,8|1\": {\"n\": 45, \"r2\": 45, \"r3\": 0, \"r4\": 0, \"r5\": 0, \"r6\": 0, \"r7\": 0, \"r8\": 42, \"r9\": 42}, \"6,8,8|2\": {\"n\": 27, \"r2\": 27, \"r3\": 0, \"r4\": 0, \"r5\": 0, \"r6\": 0, \"r7\": 0, \"r8\": 24, \"r9\": 24}, \"6,8,8|3\": {\"n\": 16, \"r2\": 16, \"r3\": 0, \"r4\": 0, \"r5\": 0, \"r6\": 0, \"r7\": 0, \"r8\": 13, \"r9\": 13}, \"6,8,8|4\": {\"n\": 7, \"r2\": 7, \"r3\": 0, \"r4\": 0, \"r5\": 0, \"r6\": 0, \"r7\": 0, \"r8\": 4, \"r9\": 4}, \"6,8,9|0\": {\"n\": 120, \"r2\": 0, \"r3\": 0, \"r4\": 0, \"r5\": 0, \"r6\": 0, \"r7\": 0, \"r8\": 0, \"r9\": 95}, \"6,8,9|1\": {\"n\": 78, \"r2\": 0, \"r3\": 0, \"r4\": 0, \"r5\": 0, \"r6\": 0, \"r7\": 0, \"r8\": 0, \"r9\": 53}, \"6,8,9|2\": {\"n\": 47, \"r2\": 0, \"r3\": 0, \"r4\": 0, \"r5\": 0, \"r6\": 0, \"r7\": 0, \"r8\": 0, \"r9\": 24}, \"6,8,9|3\": {\"n\": 25, \"r2\": 0, \"r3\": 0, \"r4\": 0, \"r5\": 0, \"r6\": 0, \"r7\": 0, \"r8\": 0, \"r9\": 6}, \"6,9,9|0\": {\"n\": 78, \"r2\": 0, \"r3\": 0, \"r4\": 0, \"r5\": 0, \"r6\": 0, \"r7\": 0, \"r8\": 0, \"r9\": 64}, \"6,9,9|1\": {\"n\": 54, \"r2\": 0, \"r3\": 0, \"r4\": 0, \"r5\": 0, \"r6\": 0, \"r7\": 0, \"r8\": 0, \"r9\": 40}, \"6,9,9|2\": {\"n\": 33, \"r2\": 0, \"r3\": 0, \"r4\": 0, \"r5\": 0, \"r6\": 0, \"r7\": 0, \"r8\": 0, \"r9\": 19}, \"6,9,9|3\": {\"n\": 20, \"r2\": 0, \"r3\": 0, \"r4\": 0, \"r5\": 0, \"r6\": 0, \"r7\": 0, \"r8\": 0, \"r9\": 6}, \"8,8,9|0\": {\"n\": 100, \"r2\": 0, \"r3\": 92, \"r4\": 92, \"r5\": 92, \"r6\": 0, \"r7\": 0, \"r8\": 0, \"r9\": 92}, \"8,8,9|1\": {\"n\": 70, \"r2\": 0, \"r3\": 62, \"r4\": 62, \"r5\": 62, \"r6\": 0, \"r7\": 0, \"r8\": 0, \"r9\": 62}, \"8,8,9|2\": {\"n\": 48, \"r2\": 0, \"r3\": 40, \"r4\": 40, \"r5\": 40, \"r6\": 0, \"r7\": 0, \"r8\": 0, \"r9\": 40}, \"8,8,9|3\": {\"n\": 30, \"r2\": 0, \"r3\": 22, \"r4\": 22, \"r5\": 22, \"r6\": 0, \"r7\": 0, \"r8\": 0, \"r9\": 22}, \"8,8,9|4\": {\"n\": 18, \"r2\": 0, \"r3\": 10, \"r4\": 10, \"r5\": 10, \"r6\": 0, \"r7\": 0, \"r8\": 0, \"r9\": 10}, \"8,8,9|5\": {\"n\": 9, \"r2\": 0, \"r3\": 3, \"r4\": 3, \"r5\": 3, \"r6\": 0, \"r7\": 0, \"r8\": 0, \"r9\": 3}, \"8,9,9|0\": {\"n\": 110, \"r2\": 0, \"r3\": 102, \"r4\": 102, \"r5\": 102, \"r6\": 0, \"r7\": 0, \"r8\": 0, \"r9\": 102}, \"8,9,9|1\": {\"n\": 80, \"r2\": 0, \"r3\": 72, \"r4\": 72, \"r5\": 72, \"r6\": 0, \"r7\": 0, \"r8\": 0, \"r9\": 72}, \"8,9,9|2\": {\"n\": 54, \"r2\": 0, \"r3\": 46, \"r4\": 46, \"r5\": 46, \"r6\": 0, \"r7\": 0, \"r8\": 0, \"r9\": 46}, \"8,9,9|3\": {\"n\": 36, \"r2\": 0, \"r3\": 28, \"r4\": 28, \"r5\": 28, \"r6\": 0, \"r7\": 0, \"r8\": 0, \"r9\": 28}, \"8,9,9|4\": {\"n\": 21, \"r2\": 0, \"r3\": 13, \"r4\": 13, \"r5\": 13, \"r6\": 0, \"r7\": 0, \"r8\": 0, \"r9\": 13}, \"8,9,9|5\": {\"n\": 12, \"r2\": 0, \"r3\": 4, \"r4\": 4, \"r5\": 4, \"r6\": 0, \"r7\": 0, \"r8\": 0, \"r9\": 4}}")

# New-key (11/12 branch) census.
NEW_KEYS = {"keys": 650, "with_11": 363, "with_12": 364,
            "profiles": 31732, "profiles_with_11": 18740,
            "profiles_with_12": 19530}
NEW_CENSUS = {"uniform_det": 45, "uniform_ndet": 605, "mixed": 0,
              "gprime_mismatch": 0, "chain_union_equal": 167}
NEW_DET_RESIDUE_CLASSES = ["1,2", "1,3", "2", "3"]
NEW_DET_KEYS = ["1,1,11|0", "1,11,11|0", "10,10,12|0", "10,10,12|1", "10,10,12|2", "10,10,12|3", "10,10,12|4", "10,10,12|5", "10,10,12|6", "10,10,12|7", "10,10,12|8", "10,10,12|9", "10,12,12|0", "10,12,12|1", "10,12,12|2", "10,12,12|3", "10,12,12|4", "10,12,12|5", "10,12,12|6", "10,12,12|7", "10,12,12|8", "10,12,12|9", "11,11,11|0", "11,11,11|1", "11,11,11|10", "11,11,11|2", "11,11,11|3", "11,11,11|4", "11,11,11|5", "11,11,11|6", "11,11,11|7", "11,11,11|8", "11,11,11|9", "12,12,12|0", "12,12,12|1", "12,12,12|10", "12,12,12|11", "12,12,12|2", "12,12,12|3", "12,12,12|4", "12,12,12|5", "12,12,12|6", "12,12,12|7", "12,12,12|8", "12,12,12|9"]
NEW_RESIDUE_CENSUS = json.loads(
"{\"0,1,2\": {\"det\": 0, \"keys\": 10, \"mixed\": 0, \"ndet\": 10}, \"0,1,3\": {\"det\": 0, \"keys\": 10, \"mixed\": 0, \"ndet\": 10}, \"0,2\": {\"det\": 0, \"keys\": 20, \"mixed\": 0, \"ndet\": 20}, \"0,2,3\": {\"det\": 0, \"keys\": 14, \"mixed\": 0, \"ndet\": 14}, \"0,2,4\": {\"det\": 0, \"keys\": 4, \"mixed\": 0, \"ndet\": 4}, \"0,2,5\": {\"det\": 0, \"keys\": 5, \"mixed\": 0, \"ndet\": 5}, \"0,2,6\": {\"det\": 0, \"keys\": 6, \"mixed\": 0, \"ndet\": 6}, \"0,2,7\": {\"det\": 0, \"keys\": 7, \"mixed\": 0, \"ndet\": 7}, \"0,2,8\": {\"det\": 0, \"keys\": 8, \"mixed\": 0, \"ndet\": 8}, \"0,3\": {\"det\": 0, \"keys\": 21, \"mixed\": 0, \"ndet\": 21}, \"0,3,4\": {\"det\": 0, \"keys\": 4, \"mixed\": 0, \"ndet\": 4}, \"0,3,5\": {\"det\": 0, \"keys\": 5, \"mixed\": 0, \"ndet\": 5}, \"0,3,6\": {\"det\": 0, \"keys\": 6, \"mixed\": 0, \"ndet\": 6}, \"0,3,7\": {\"det\": 0, \"keys\": 7, \"mixed\": 0, \"ndet\": 7}, \"0,3,8\": {\"det\": 0, \"keys\": 8, \"mixed\": 0, \"ndet\": 8}, \"1,2\": {\"det\": 2, \"keys\": 26, \"mixed\": 0, \"ndet\": 24}, \"1,2,3\": {\"det\": 0, \"keys\": 18, \"mixed\": 0, \"ndet\": 18}, \"1,2,4\": {\"det\": 0, \"keys\": 5, \"mixed\": 0, \"ndet\": 5}, \"1,2,5\": {\"det\": 0, \"keys\": 6, \"mixed\": 0, \"ndet\": 6}, \"1,2,6\": {\"det\": 0, \"keys\": 7, \"mixed\": 0, \"ndet\": 7}, \"1,2,7\": {\"det\": 0, \"keys\": 8, \"mixed\": 0, \"ndet\": 8}, \"1,2,8\": {\"det\": 0, \"keys\": 9, \"mixed\": 0, \"ndet\": 9}, \"1,3\": {\"det\": 20, \"keys\": 27, \"mixed\": 0, \"ndet\": 7}, \"1,3,4\": {\"det\": 0, \"keys\": 5, \"mixed\": 0, \"ndet\": 5}, \"1,3,5\": {\"det\": 0, \"keys\": 6, \"mixed\": 0, \"ndet\": 6}, \"1,3,6\": {\"det\": 0, \"keys\": 7, \"mixed\": 0, \"ndet\": 7}, \"1,3,7\": {\"det\": 0, \"keys\": 8, \"mixed\": 0, \"ndet\": 8}, \"1,3,8\": {\"det\": 0, \"keys\": 9, \"mixed\": 0, \"ndet\": 9}, \"2\": {\"det\": 11, \"keys\": 15, \"mixed\": 0, \"ndet\": 4}, \"2,3\": {\"det\": 0, \"keys\": 41, \"mixed\": 0, \"ndet\": 41}, \"2,3,4\": {\"det\": 0, \"keys\": 9, \"mixed\": 0, \"ndet\": 9}, \"2,3,5\": {\"det\": 0, \"keys\": 10, \"mixed\": 0, \"ndet\": 10}, \"2,3,6\": {\"det\": 0, \"keys\": 11, \"mixed\": 0, \"ndet\": 11}, \"2,3,7\": {\"det\": 0, \"keys\": 12, \"mixed\": 0, \"ndet\": 12}, \"2,3,8\": {\"det\": 0, \"keys\": 13, \"mixed\": 0, \"ndet\": 13}, \"2,4\": {\"det\": 0, \"keys\": 10, \"mixed\": 0, \"ndet\": 10}, \"2,4,5\": {\"det\": 0, \"keys\": 4, \"mixed\": 0, \"ndet\": 4}, \"2,4,6\": {\"det\": 0, \"keys\": 4, \"mixed\": 0, \"ndet\": 4}, \"2,4,7\": {\"det\": 0, \"keys\": 4, \"mixed\": 0, \"ndet\": 4}, \"2,4,8\": {\"det\": 0, \"keys\": 4, \"mixed\": 0, \"ndet\": 4}, \"2,5\": {\"det\": 0, \"keys\": 12, \"mixed\": 0, \"ndet\": 12}, \"2,5,6\": {\"det\": 0, \"keys\": 5, \"mixed\": 0, \"ndet\": 5}, \"2,5,7\": {\"det\": 0, \"keys\": 5, \"mixed\": 0, \"ndet\": 5}, \"2,5,8\": {\"det\": 0, \"keys\": 5, \"mixed\": 0, \"ndet\": 5}, \"2,6\": {\"det\": 0, \"keys\": 14, \"mixed\": 0, \"ndet\": 14}, \"2,6,7\": {\"det\": 0, \"keys\": 6, \"mixed\": 0, \"ndet\": 6}, \"2,6,8\": {\"det\": 0, \"keys\": 6, \"mixed\": 0, \"ndet\": 6}, \"2,7\": {\"det\": 0, \"keys\": 16, \"mixed\": 0, \"ndet\": 16}, \"2,7,8\": {\"det\": 0, \"keys\": 7, \"mixed\": 0, \"ndet\": 7}, \"2,8\": {\"det\": 0, \"keys\": 18, \"mixed\": 0, \"ndet\": 18}, \"3\": {\"det\": 12, \"keys\": 18, \"mixed\": 0, \"ndet\": 6}, \"3,4\": {\"det\": 0, \"keys\": 11, \"mixed\": 0, \"ndet\": 11}, \"3,4,5\": {\"det\": 0, \"keys\": 4, \"mixed\": 0, \"ndet\": 4}, \"3,4,6\": {\"det\": 0, \"keys\": 4, \"mixed\": 0, \"ndet\": 4}, \"3,4,7\": {\"det\": 0, \"keys\": 4, \"mixed\": 0, \"ndet\": 4}, \"3,4,8\": {\"det\": 0, \"keys\": 4, \"mixed\": 0, \"ndet\": 4}, \"3,5\": {\"det\": 0, \"keys\": 13, \"mixed\": 0, \"ndet\": 13}, \"3,5,6\": {\"det\": 0, \"keys\": 5, \"mixed\": 0, \"ndet\": 5}, \"3,5,7\": {\"det\": 0, \"keys\": 5, \"mixed\": 0, \"ndet\": 5}, \"3,5,8\": {\"det\": 0, \"keys\": 5, \"mixed\": 0, \"ndet\": 5}, \"3,6\": {\"det\": 0, \"keys\": 15, \"mixed\": 0, \"ndet\": 15}, \"3,6,7\": {\"det\": 0, \"keys\": 6, \"mixed\": 0, \"ndet\": 6}, \"3,6,8\": {\"det\": 0, \"keys\": 6, \"mixed\": 0, \"ndet\": 6}, \"3,7\": {\"det\": 0, \"keys\": 17, \"mixed\": 0, \"ndet\": 17}, \"3,7,8\": {\"det\": 0, \"keys\": 7, \"mixed\": 0, \"ndet\": 7}, \"3,8\": {\"det\": 0, \"keys\": 19, \"mixed\": 0, \"ndet\": 19}}")

# D_10 subsequence anchor.
D10 = {"positions": 15863, "first": 0, "last": 47562}
D10_MAX_STATES = 363630

# Theorem J (K0906) cap<=12 r=9 anchor values.
THEOREM_J = {"m_le_8_det_mism": 0, "m_le_8_sv_mism": 0,
             "m_le_7_fl_mism": 0, "det_diffs": 876,
             "det_diffs_by_m": {"9": 876}, "sv_mask_diffs": 38070}
M9_UNI_DET_KEYS = ["9,9,9|0", "9,9,9|1", "9,9,9|2", "9,9,9|3", "9,9,9|4", "9,9,9|5", "9,9,9|6", "9,9,9|7", "9,9,9|8"]
DELTA0 = {"profiles": 1512, "with_11_or_12": 784}

# Live-check sample pins (deterministic given the committed records).
SAMPLES = {"d10_stride": 32, "d10_count": 432,
           "new_stride": 37, "new_count": 450}


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def sha256_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def load_full():
    # Single committed source: the packed column.  Each line is
    # [i, sv_mask, fl_mask, states]; atoms are a pure function of i
    # via the canonical enumeration (checked in C2), so this unpacks
    # to the same records the sweep engine emitted (C3 round-trip).
    recs = []
    with open(PACKED_PATH) as f:
        for line in f:
            line = line.strip()
            if line:
                i, svm, flm, st = json.loads(line)
                recs.append({
                    "i": i,
                    "survivors": mask_bits(svm),
                    "first_losers": mask_bits(flm),
                    "states": st,
                    "determined": det_of_mask(svm),
                })
    return recs


def load_packed(path):
    out = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                i, svm, flm, st = json.loads(line)
                out.append((i, svm, flm, st))
    return out


def packed_line(rec):
    svm = sum(1 << p for p in rec["survivors"])
    flm = sum(1 << p for p in rec["first_losers"])
    return json.dumps([rec["i"], svm, flm, rec["states"]],
                      separators=(",", ":"))


def mask_bits(m):
    return sorted(p for p in range(16) if (m >> p) & 1)


def det_of_mask(m):
    return bin(m).count("1") == 1


# ---------------------------------------------------------------------------
# audit assembly (deterministic; regenerate twice, byte-identical)
# ---------------------------------------------------------------------------

def assemble_audit():
    checks = []

    def record(name, ok, data):
        checks.append({"name": name, "ok": bool(ok), "data": data})

    audit = {"meta": {
        "item": "K0912",
        "title": "3-branch REMO determinacy size boundary cap<=12 x "
            "r=9: the K0893 34-key boundary is unchanged by the size "
            "11/12 extension (650 new keys, 0 new mixed); Theorem J "
            "cap<=12 r>=max(M,2) anchor at r=9",
        "date": "2026-11-17",
        "engine_provenance": "verbatim region game / enumeration / "
            "Burnside / Theorem D from the K0862 verifier via K0875, "
            "K0876 and K0893; full-domain records produced by the "
            "committed JavaScript mask engine mask_engine_fast2.js "
            "(game logic, recursion order, budget semantics and record "
            "format verbatim identical to the committed K0893 engine "
            "mask_engine_fast_r9.js; only the memo representation "
            "differs - byte arena + open addressing instead of a JS Map "
            "- which does not affect any record); the sweep was run as "
            "two independent processes (indices 0..24447 and "
            "23798..47594, 650-record overlap byte-identical) and "
            "merged; the committed publication form is the packed "
            "column (lossless: atoms are a pure function of i); "
            "Python mask twin cross-validated live in every run",
        "r_swept": [9],
    }}

    # ---- C1: enumeration / Burnside (r-independent, K0875 anchor)
    enum = {}
    audit["burnside"] = {}
    for cap in (10, 11, 12):
        fi, ft, fc, orbits = burnside_fix_counts(cap)
        profs = direct_constrained(cap)
        enum[cap] = profs
        exp = EXPECTED_BURNSIDE[cap]
        keys = len({key_of(a) for a in profs})
        audit["burnside"][str(cap)] = {
            "fix_id": fi, "fix_trans": ft, "fix_cyc": fc,
            "orbits": orbits, "keys": keys,
        }
        record(
            "cap=%d: Burnside orbit count == direct canonical "
            "enumeration (%d profiles, %d keys)" % (cap, exp["orbits"],
                                                    exp["keys"]),
            orbits == len(profs) == exp["orbits"]
            and (fi, ft, fc)
            == (exp["fix_id"], exp["fix_trans"], exp["fix_cyc"])
            and keys == exp["keys"],
            {"fix_id": fi, "fix_trans": ft, "fix_cyc": fc,
             "orbits": orbits, "keys": keys},
        )
    ok = set(enum[10]) <= set(enum[11]) and set(enum[11]) <= set(enum[12])
    record(
        "profile-set inclusion: cap10 subset of cap11 subset of cap12",
        ok,
        {"cap10": len(enum[10]), "cap11": len(enum[11]),
         "cap12": len(enum[12])},
    )
    del enum[10], enum[11]
    profiles = enum[12]
    pidx = {atoms: i for i, atoms in enumerate(profiles)}
    byk = {}
    for i, atoms in enumerate(profiles):
        byk.setdefault(key_of(atoms), []).append(i)

    # ---- C2: committed packed column integrity (single source)
    recs_list = load_full()
    records = {rec["i"]: rec for rec in recs_list}
    packed_sha = sha256_file(PACKED_PATH)
    packed_bytes = os.path.getsize(PACKED_PATH)
    ok2 = (
        len(recs_list) == N_PROFILES
        and [rec["i"] for rec in recs_list] == list(range(N_PROFILES))
        and all(
            rec["determined"] == (len(rec["survivors"]) == 1)
            and 0 < len(rec["survivors"]) <= 9
            and len(rec["first_losers"]) >= 1
            and all(0 <= p < 9
                   for p in rec["survivors"] + rec["first_losers"])
            and rec["states"] > 0
            for rec in recs_list
        )
        and packed_sha == PACKED_SHA256
        and packed_bytes == PACKED_BYTES
        and sha256_file(ENGINE_PATH) == ENGINE_SHA256
    )
    ms_rec = max(recs_list, key=lambda rec: rec["states"])
    record(
        "r=9 committed packed column: 47595 records [i, sv_mask, "
        "fl_mask, states], index-complete, atoms a pure function of i "
        "via the canonical enumeration, mask/state field invariants, "
        "file sha256 + engine sha256 pinned",
        ok2,
        {"records": len(recs_list), "sha256": packed_sha,
         "bytes": packed_bytes,
         "max_states": ms_rec["states"], "max_states_i": ms_rec["i"],
         "max_states_atoms": profiles[ms_rec["i"]],
         "states_sum": sum(rec["states"] for rec in recs_list)},
    )

    # ---- C3: packed round-trip (parse/serialize lossless)
    derived = "".join(packed_line(rec) + "\n" for rec in recs_list)
    with open(PACKED_PATH, "rb") as f:
        packed_bytes_raw = f.read()
    ok3 = packed_bytes_raw == derived.encode()
    record(
        "packed round-trip: re-serialized [i, sv_mask, fl_mask, "
        "states] from the parsed column reproduce the committed "
        "packed bytes exactly (mask <-> player-set unpacking "
        "lossless, states exact)",
        ok3,
        {"derived_bytes": len(derived),
         "committed_bytes": len(packed_bytes_raw)},
    )

    # reference column sha pins (committed r=2..8 columns, K0893 column)
    ref_shas = {}
    ref_ok = True
    ref_cols = {}
    for r in (2, 3, 4, 5, 6, 7, 8):
        s = sha256_file(REF_COLUMNS[r][0])
        ref_shas["r%d" % r] = s
        ref_ok = ref_ok and s == REF_COLUMN_SHA256["r%d" % r]
        ref_cols[r] = {c[0]: c for c in load_packed(REF_COLUMNS[r][0])}
    s = sha256_file(CAP10_R9_PATH)
    ref_shas["cap10_r9"] = s
    ref_ok = ref_ok and s == REF_COLUMN_SHA256["cap10_r9"]

    # ---- C4: D_10 subsequence == committed K0893 cap<=10 r=9 column
    d10pos = [i for i, a in enumerate(profiles)
              if max(profile_sizes(a, 3)) <= 10]
    embed = [profiles[i] for i in d10pos] == list(direct_constrained(10))
    cap10 = load_packed(CAP10_R9_PATH)
    mism4 = 0
    for k, i in enumerate(d10pos):
        rec = records[i]
        want = cap10[k]
        svm = sum(1 << p for p in rec["survivors"])
        flm = sum(1 << p for p in rec["first_losers"])
        if (svm, flm, rec["states"]) != (want[1], want[2], want[3]):
            mism4 += 1
    d10_max = max(records[i]["states"] for i in d10pos)
    record(
        "D_10 subsequence: the 15863 cap<=10 canonical profiles embed "
        "order-preservingly at pinned positions (first 0, last 47562) "
        "and the r=9 records there equal the committed K0893 cap<=10 "
        "r=9 column byte-wise (sv/fl/states, %d mismatches); D_10 max "
        "states %d == K0893 published" % (mism4, d10_max),
        embed and mism4 == 0 and len(d10pos) == D10["positions"]
        and d10pos[0] == D10["first"] and d10pos[-1] == D10["last"]
        and len(cap10) == D10["positions"]
        and [c[0] for c in cap10] == list(range(D10["positions"]))
        and d10_max == D10_MAX_STATES and ref_ok,
        {"positions": len(d10pos), "mismatches": mism4,
         "first": d10pos[0], "last": d10pos[-1],
         "max_states": d10_max, "ref_column_sha256": ref_shas},
    )

    # ---- C5: Lemma FL (K0864, universal) r=9 anchor
    fl_viol = 0
    for i, atoms in enumerate(profiles):
        want = sorted({c % 9 for c in profile_sizes(atoms, 3)})
        if records[i]["first_losers"] != want:
            fl_viol += 1
    record(
        "Lemma FL (K0864, universal; redundant machine anchor): first "
        "losers == {C_i mod 9} for all 47595 profiles, 0 violations",
        fl_viol == 0,
        {"violations": fl_viol},
    )

    # ---- C6: key census / mixed keys / partitions / chains
    mixed = sorted(k for k in byk
                  if len({records[i]["determined"] for i in byk[k]}) > 1)
    uni_det = sum(1 for k in byk
                  if {records[i]["determined"] for i in byk[k]} == {True})
    uni_ndet = sum(1 for k in byk
                   if {records[i]["determined"] for i in byk[k]} == {False})
    got_mixed = [[list(k[0]), k[1]] for k in mixed]
    ok6 = (
        len(byk) == CENSUS["keys"] and uni_det == CENSUS["uniform_det"]
        and uni_ndet == CENSUS["uniform_ndet"]
        and len(mixed) == CENSUS["mixed"]
        and got_mixed == MIXED_KEYS
    )
    # per-key partition
    part = {}
    dsvs = set()
    chain_det = 0
    for k in mixed:
        idxs = byk[k]
        det = [i for i in idxs if records[i]["determined"]]
        ndet = [i for i in idxs if not records[i]["determined"]]
        for i in det:
            dsvs.add(tuple(records[i]["survivors"]))
        part[kstr(k)] = {
            "n": len(idxs), "det": len(det), "ndet": len(ndet),
            "dsv": sorted([list(x) for x in
                           {tuple(records[i]["survivors"]) for i in det}]),
            "ndet_sets": sorted([list(x) for x in
                                 {tuple(records[i]["survivors"])
                                  for i in ndet}]),
        }
        chain = records[pidx[chain_profile(k[0], k[1], 3)]]
        if chain["determined"]:
            chain_det += 1
    # cap<=10 sub-census == K0893 published
    old = [k for k in byk if max(k[0]) <= 10]
    sub_det = sum(1 for k in old
                  if {records[i]["determined"] for i in byk[k]} == {True})
    sub_ndet = sum(1 for k in old
                   if {records[i]["determined"] for i in byk[k]} == {False})
    ok6 = ok6 and part == MIXED_PARTITION and dsvs == {(5,)}
    ok6 = ok6 and chain_det == len(mixed)
    ok6 = ok6 and (sub_det, sub_ndet, len(mixed), len(old)) == (
        CAP10_SUBCENSUS["uniform_det"], CAP10_SUBCENSUS["uniform_ndet"],
        CAP10_SUBCENSUS["mixed"], CAP10_SUBCENSUS["keys"])
    record(
        "r=9 cap<=12 key census: 1365 keys, 143 uniform-det / 1188 "
        "uniform-ndet / 34 mixed; the 34 mixed keys are EXACTLY the "
        "K0893 cap<=10 boundary (7 families), per-key partitions "
        "pinned-identical, det-side survivor uniformly P_5, all 34 "
        "chain profiles determined, cap<=10 sub-census 98/583/34 == "
        "K0893 published",
        ok6,
        {"keys": len(byk), "uniform_det": uni_det,
         "uniform_ndet": uni_ndet, "mixed": len(mixed),
         "det_survivor_sets": sorted(list(x) for x in dsvs),
         "chain_determined": chain_det,
         "cap10_sub_census": {"keys": len(old), "uniform_det": sub_det,
                              "uniform_ndet": sub_ndet,
                              "mixed": len(mixed)}},
    )

    # ---- C7: new-key census (branches of size 11/12) + G'
    newk = [k for k in byk if 11 in k[0] or 12 in k[0]]
    newidx = [i for i, a in enumerate(profiles)
              if (lambda s: 11 in s or 12 in s)(profile_sizes(a, 3))]
    n_w11 = sum(1 for k in byk if 11 in k[0])
    n_w12 = sum(1 for k in byk if 12 in k[0])
    np11 = sum(1 for a in profiles if 11 in profile_sizes(a, 3))
    np12 = sum(1 for a in profiles if 12 in profile_sizes(a, 3))
    new_det = [k for k in newk
               if {records[i]["determined"] for i in byk[k]} == {True}]
    new_ndet = [k for k in newk
                if {records[i]["determined"] for i in byk[k]} == {False}]
    new_mixed = [k for k in newk
                 if len({records[i]["determined"] for i in byk[k]}) > 1]
    # G' survivor level over ALL uniformly determined keys
    g_mism = 0
    for k in byk:
        if {records[i]["determined"] for i in byk[k]} != {True}:
            continue
        cs = records[pidx[chain_profile(k[0], k[1], 3)]]["survivors"]
        if any(records[i]["survivors"] != cs for i in byk[k]):
            g_mism += 1
    # residue census of the new keys
    cens = {}
    for k in newk:
        pair = ",".join(map(str, sorted({c % 9 for c in k[0]})))
        e = cens.setdefault(pair, {"keys": 0, "det": 0, "ndet": 0,
                                   "mixed": 0})
        e["keys"] += 1
        flags = {records[i]["determined"] for i in byk[k]}
        if flags == {True}:
            e["det"] += 1
        elif flags == {False}:
            e["ndet"] += 1
        else:
            e["mixed"] += 1
    # chain-survivor union equality among uniform-ndet new keys
    cu = 0
    for k in new_ndet:
        cs = records[pidx[chain_profile(k[0], k[1], 3)]]["survivors"]
        union = sorted({p for i in byk[k]
                        for p in records[i]["survivors"]})
        if cs == union:
            cu += 1
    det_classes = sorted(p for p, e in cens.items() if e["det"] > 0)
    ok7 = (
        len(newk) == NEW_KEYS["keys"] and n_w11 == NEW_KEYS["with_11"]
        and n_w12 == NEW_KEYS["with_12"]
        and len(newidx) == NEW_KEYS["profiles"]
        and np11 == NEW_KEYS["profiles_with_11"]
        and np12 == NEW_KEYS["profiles_with_12"]
        and (len(new_det), len(new_ndet), len(new_mixed))
        == (NEW_CENSUS["uniform_det"], NEW_CENSUS["uniform_ndet"],
            NEW_CENSUS["mixed"])
        and g_mism == NEW_CENSUS["gprime_mismatch"]
        and cu == NEW_CENSUS["chain_union_equal"]
        and cens == NEW_RESIDUE_CENSUS
        and sorted(kstr(k) for k in new_det) == NEW_DET_KEYS
        and det_classes == NEW_DET_RESIDUE_CLASSES
    )
    record(
        "new-key census (keys containing an 11 or 12 branch): 650 keys "
        "(363 with 11, 364 with 12; 31732 profiles) split 45 uniform-det "
        "/ 605 uniform-ndet / 0 MIXED - ZERO new non-collapse keys at "
        "sizes 11,12; residue-class census pinned; the 45 uniform-det "
        "new keys are pinned exactly; Theorem G' survivor level holds "
        "for all 143 uniform-det keys (0 mismatches); 167/605 "
        "uniform-ndet new keys have chain survivors == union "
        "(observation)",
        ok7,
        {"keys": len(newk), "with_11": n_w11, "with_12": n_w12,
         "profiles": len(newidx),
         "uniform_det": len(new_det), "uniform_ndet": len(new_ndet),
         "mixed": len(new_mixed), "gprime_mismatches": g_mism,
         "chain_union_equal": cu,
         "det_residue_classes": det_classes},
    )

    # ---- C8: Theorem J (K0906) cap<=12 r=9 anchor vs r=8 column
    r8 = {c[0]: c for c in load_packed(REF_COLUMNS[8][0])}
    jm_det = 0
    jm_sv = 0
    jm_fl = 0
    diff_by_m = {}
    sv_diffs = 0
    for i, atoms in enumerate(profiles):
        M = max(profile_sizes(atoms, 3))
        rec = records[i]
        svm9 = sum(1 << p for p in rec["survivors"])
        flm9 = sum(1 << p for p in rec["first_losers"])
        _, svm8, flm8, _ = r8[i]
        if svm9 != svm8:
            sv_diffs += 1
        if rec["determined"] != det_of_mask(svm8):
            diff_by_m[str(M)] = diff_by_m.get(str(M), 0) + 1
        if M <= 8:
            if rec["determined"] != det_of_mask(svm8):
                jm_det += 1
            if svm9 != svm8:
                jm_sv += 1
            if M <= 7 and flm9 != flm8:
                jm_fl += 1
    m9_det_keys = sorted(
        kstr(k) for k in byk
        if max(k[0]) == 9
        and {records[i]["determined"] for i in byk[k]} == {True})
    # Delta=0 (uniform-size) profiles all Theorem D at r=9
    d0 = 0
    d0_new = 0
    d0_mism = 0
    for i, atoms in enumerate(profiles):
        sizes = profile_sizes(atoms, 3)
        if len(set(sizes)) != 1:
            continue
        d0 += 1
        if max(sizes) > 10:
            d0_new += 1
        _, surv = theorem_d(sizes[0], 9)
        rec = records[i]
        if not (rec["determined"] and rec["survivors"] == [surv]):
            d0_mism += 1
    ok8 = (
        jm_det == 0 and jm_sv == 0 and jm_fl == 0
        and sum(diff_by_m.values()) == THEOREM_J["det_diffs"]
        and diff_by_m == THEOREM_J["det_diffs_by_m"]
        and sv_diffs == THEOREM_J["sv_mask_diffs"]
        and m9_det_keys == M9_UNI_DET_KEYS
        and d0 == DELTA0["profiles"] and d0_new == DELTA0["with_11_or_12"]
        and d0_mism == 0
    )
    record(
        "Theorem J (K0906, universal) cap<=12 r=9 anchor: for M = max "
        "C_i <= 8 the r=9 det/sv equal the committed r=8 column "
        "(det 0 / sv 0 mismatches; M <= 7 fl also 0); all 876 r8->r9 "
        "det differences lie in M=9 profiles (the 34-key families "
        "crossing the r >= max(M,2) threshold); sv-mask diffs 38070 "
        "all in M>=8; the M=9 uniformly determined keys are exactly "
        "the Delta=0 family (9,9,9) x g=0..8; all 1512 Delta=0 "
        "profiles (784 with an 11/12 branch) are determined with the "
        "Theorem D r=9 survivor (0 mismatches)",
        ok8,
        {"m_le_8_det_mismatches": jm_det, "m_le_8_sv_mismatches": jm_sv,
         "m_le_7_fl_mismatches": jm_fl,
         "det_diffs_by_m": diff_by_m, "sv_mask_diffs": sv_diffs,
         "m9_uniform_det_keys": m9_det_keys,
         "delta0_profiles": d0, "delta0_with_11_or_12": d0_new,
         "delta0_mismatches": d0_mism},
    )

    # ---- C9: ECHO table (mixed keys across committed r=2..8 + r=9)
    echo = {}
    for k in mixed:
        e = {"n": len(byk[k])}
        for r in (2, 3, 4, 5, 6, 7, 8):
            col = ref_cols[r]
            e["r%d" % r] = sum(
                1 for i in byk[k] if det_of_mask(col[i][1]))
        e["r9"] = sum(1 for i in byk[k] if records[i]["determined"])
        echo[kstr(k)] = e
    record(
        "ECHO: the r=2..9 determinacy history of the 34 mixed keys "
        "(det counts per committed column) matches the pinned table: "
        "(6,6,8)/(6,8,8) active at r=2, dormant r=3..7, revived r=8-9; "
        "(8,8,9)/(8,9,9) active r=3..5, dormant r=6..8, revived r=9; "
        "the three 6/9 families fully dormant r=2..8, awaken at r=9 - "
        "the size 11/12 extension changes none of it",
        echo == ECHO_TABLE,
        {"rows": len(echo)},
    )
    audit["echo_table"] = echo

    # ---- C10: Theorem D table == K0859 published
    entries, mism = theorem_d_table()
    record(
        "Theorem D recursion == K0859 published (C,r) table "
        "(84 entries, C=1..12, r=2..8)",
        mism == 0 and entries == 84,
        {"entries": entries, "mismatches": mism},
    )

    audit["sweep_inputs"] = {
        "r9_packed": {"sha256": packed_sha, "bytes": packed_bytes,
                      "records": len(recs_list)},
        "engine_sha256": sha256_file(ENGINE_PATH),
        "ref_column_sha256": ref_shas,
    }
    audit["sweeps"] = {
        "census": {"keys": len(byk), "uniform_det": uni_det,
                   "uniform_ndet": uni_ndet, "mixed": len(mixed)},
        "cap10_sub_census": {"keys": len(old), "uniform_det": sub_det,
                             "uniform_ndet": sub_ndet,
                             "mixed": len(mixed)},
        "mixed_partition": part,
        "new_key_census": {
            "keys": len(newk), "with_11": n_w11, "with_12": n_w12,
            "profiles": len(newidx),
            "uniform_det": len(new_det), "uniform_ndet": len(new_ndet),
            "mixed": len(new_mixed),
            "uniform_det_keys": sorted(kstr(k) for k in new_det),
            "residue_census": cens,
        },
        "states": {
            "max": ms_rec["states"], "max_i": ms_rec["i"],
            "sum": sum(rec["states"] for rec in recs_list),
        },
    }
    audit["machine_checks"] = checks
    audit["summary"] = {
        "all_ok": all(c["ok"] for c in checks),
        "checks_total": len(checks),
    }
    return audit


# ---------------------------------------------------------------------------
# live engine re-computations (not part of the audit bytes)
# ---------------------------------------------------------------------------

def live_checks(audit):
    """Engine re-computations (not part of the audit bytes): the Python
    mask twin and the verbatim region engine vs the committed JS
    records on deterministic samples."""
    profiles = direct_constrained(12)
    pidx = {atoms: i for i, atoms in enumerate(profiles)}
    records = {rec["i"]: rec for rec in load_full()}
    byk = {}
    for i, atoms in enumerate(profiles):
        byk.setdefault(key_of(atoms), []).append(i)

    # L1: full cap<=7 domain: verbatim == mask twin == committed JS
    profs7 = direct_constrained(7)
    mism = 0
    n = 0
    for atoms in profs7:
        idx12 = pidx[atoms]
        v1, s1 = region_verdict(atoms, 3, 9, budget=20_000_000)
        v2, s2 = mask_verdict(atoms, 3, 9, budget=20_000_000)
        j = records[idx12]
        n += 1
        if verdict_triple(v1) != verdict_triple(v2):
            mism += 1
        if verdict_triple(v2) != (j["determined"], j["survivors"],
                                  j["first_losers"]):
            mism += 1
        if s1 != s2 or s2 != j["states"]:
            mism += 1
    if mism != 0 or n != 2048:
        sys.stderr.write("LIVE FAIL: cap<=7 triple check %d mismatches "
                         "/ %d\n" % (mism, n))
        sys.exit(1)
    print("LIVE OK: cap<=7 full domain: verbatim == mask twin == "
          "committed JS records (verdicts and state counts) on %d "
          "verdicts (r=9)" % n)

    # L2: stride-32 layered D_10 sample (states <= 50k)
    d10pos = [i for i, a in enumerate(profiles)
              if max(profile_sizes(a, 3)) <= 10]
    samp = [i for i in d10pos[::32] if records[i]["states"] <= 50000]
    if len(samp) != SAMPLES["d10_count"]:
        sys.stderr.write("LIVE FAIL: D_10 sample size %d != %d\n"
                         % (len(samp), SAMPLES["d10_count"]))
        sys.exit(1)
    mism = 0
    for i in samp:
        v2, s2 = mask_verdict(profiles[i], 3, 9, budget=50_000_000)
        j = records[i]
        if verdict_triple(v2) != (j["determined"], j["survivors"],
                                 j["first_losers"]) or s2 != j["states"]:
            mism += 1
    if mism != 0:
        sys.stderr.write("LIVE FAIL: D_10 sample %d mismatches\n" % mism)
        sys.exit(1)
    print("LIVE OK: stride-32 layered D_10 sample (states <= 50k): "
          "mask twin == committed JS records on %d verdicts"
          % len(samp))

    # L3: stratified new-cell (size 11/12) sample (states <= 50k)
    newidx = [i for i, a in enumerate(profiles)
              if (lambda s: 11 in s or 12 in s)(profile_sizes(a, 3))]
    samp = [i for i in newidx[::37] if records[i]["states"] <= 50000]
    if len(samp) != SAMPLES["new_count"]:
        sys.stderr.write("LIVE FAIL: new-cell sample size %d != %d\n"
                         % (len(samp), SAMPLES["new_count"]))
        sys.exit(1)
    mism = 0
    for i in samp:
        v2, s2 = mask_verdict(profiles[i], 3, 9, budget=50_000_000)
        j = records[i]
        if verdict_triple(v2) != (j["determined"], j["survivors"],
                                 j["first_losers"]) or s2 != j["states"]:
            mism += 1
    if mism != 0:
        sys.stderr.write("LIVE FAIL: new-cell sample %d mismatches\n"
                         % mism)
        sys.exit(1)
    print("LIVE OK: stratified new-cell (size 11/12) sample "
          "(stride 37, states <= 50k): mask twin == committed JS "
          "records on %d verdicts" % len(samp))

    # L4: mixed-key witnesses: chain + min-states det + min-states ndet
    wit = 0
    wit_fail = 0
    for sp, g in MIXED_KEYS:
        k = (tuple(sp), g)
        chain_i = pidx[chain_profile(k[0], k[1], 3)]
        dets = [i for i in byk[k] if records[i]["determined"]]
        ndets = [i for i in byk[k] if not records[i]["determined"]]
        pick = [chain_i,
                min(dets, key=lambda i: (records[i]["states"], i)),
                min(ndets, key=lambda i: (records[i]["states"], i))]
        for i in pick:
            v1, s1 = region_verdict(profiles[i], 3, 9, budget=20_000_000)
            v2, s2 = mask_verdict(profiles[i], 3, 9, budget=50_000_000)
            j = records[i]
            wit += 1
            if verdict_triple(v1) != verdict_triple(v2):
                wit_fail += 1
            if verdict_triple(v2) != (j["determined"], j["survivors"],
                                      j["first_losers"]):
                wit_fail += 1
            if s1 != s2 or s2 != j["states"]:
                wit_fail += 1
    if wit_fail != 0 or wit != 3 * 34:
        sys.stderr.write("LIVE FAIL: witness re-verification %d "
                         "failures / %d\n" % (wit_fail, wit))
        sys.exit(1)
    print("LIVE OK: mixed-key witnesses (34 keys x chain + min-states "
          "det + min-states ndet = %d verdicts): verbatim == mask twin "
          "== committed JS records" % wit)


def serialize(audit):
    return json.dumps(audit, sort_keys=True, ensure_ascii=False,
                      indent=1) + "\n"


def run():
    audit1 = assemble_audit()
    blob1 = serialize(audit1)
    audit2 = assemble_audit()
    blob2 = serialize(audit2)
    d1 = hashlib.sha256(blob1.encode()).hexdigest()
    d2 = hashlib.sha256(blob2.encode()).hexdigest()
    if d1 != d2:
        sys.stderr.write("FATAL: two runs differ (nondeterminism)\n")
        sys.exit(1)
    all_ok = audit1["summary"]["all_ok"]
    os.makedirs(os.path.dirname(AUDIT_PATH), exist_ok=True)
    if os.path.exists(AUDIT_PATH):
        with open(AUDIT_PATH, "rb") as f:
            committed = f.read().decode()
        if committed != blob1:
            sys.stderr.write(
                "FATAL: regenerated audit differs from committed file "
                "(sha256 %s)\n" % d1
            )
            sys.exit(1)
        print("OK: audit byte-identical (sha256 %s)" % d1)
    else:
        with open(AUDIT_PATH, "w", encoding="utf-8") as f:
            f.write(blob1)
        print("wrote %s (sha256 %s)" % (AUDIT_PATH, d1))
    print("AUDIT PASSED" if all_ok else "AUDIT FAILED")
    for c in audit1["machine_checks"]:
        print("  [%s] %s" % ("ok" if c["ok"] else "NG", c["name"]))
    if not all_ok:
        sys.exit(1)
    live_checks(audit1)


if __name__ == "__main__":
    run()
