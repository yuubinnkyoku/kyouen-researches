#!/usr/bin/env python3
"""K0876 follow-up audit: 3-branch REMO determinacy size boundary cap<=12
for r=2, 7, 8 (the remaining cells of the r x size grid left open by
K0875/K0876: r=7,8 combined with branch sizes 11,12, and the r=2 column).

Self-contained verifier. Deterministic (no randomness, no wall clock, no
network). Python 3.11+ / stdlib only.

Data provenance. The full-domain sweep records committed under output/
(js_cap12_r{2,7,8}.packed.jsonl - packed publication format, one JSON
array per canonical cap<=12 profile: [index, survivor_mask, first_loser_
mask, states]) were produced by the JavaScript mask engine committed in
this directory (mask_engine_fast.js, verbatim from the K0876 experiment;
sweep segments are byte-concatenable because each record is a pure
function of (profile, r)). In the packed format atoms are not stored:
they are a pure function of the index via the canonical cap<=12
enumeration re-derived inside this verifier, so the packing is lossless.
The committed r=2 packed record was re-generated in a fresh environment
and is byte-identical (sha256 1fd9dbf4cb6699c26bab7f6b34a900f5877d34\
08603a02a2dd121ca71ef8e951). The mask engine carries (survivorMask,
firstLoserMask) per state instead of the verbatim frozenset of (order,
survivor) outcomes; determined / survivors / first_losers agree with the
verbatim engine's outcome_summary by induction on the state DAG, and the
reachable state space (hence the per-record "states" count) is identical.
This equivalence is re-verified live in every run of this verifier:

- full cap<=7 domain (2048 canonical profiles) x r=2,7,8: verbatim engine
  == Python mask twin == committed JS records (6144 verdicts, verdict
  and state-count equality, 0 mismatches);
- stratified cap<=12 sample (every 24th profile for r=2; every 48th for
  r=7,8) x r=2,7,8: Python mask twin == committed JS records;
- all published failing-key witness atom vectors (K0866 12 at r=7,
  K0869 20 at r=8, plus chain profiles and the r=2 echo-dormancy chain
  profiles) re-run with the verbatim engine and compared with the
  published survivors.

The Python mask twin (mask_game below) is an independent reimplementation
of the same state space; the enumeration, Burnside machinery, Theorem D
recursion and the verbatim region/cell game engine are verbatim from the
K0862 verifier via the K0875 and K0876 verifiers
(research/experiments/remo-k-branch-cap12-r456-boundary-20261116/
verify_remo_k_branch_cap12_r456_boundary.py).

Checked claims (proof text: report.md / item):

B    (Burnside vs direct enumeration, caps 10/11/12)  Identical to
     K0875/K0876 (r-independent): fix counts (84494,3478,125)/
     (152171,5299,161)/(261749,7805,203) -> 15863/28065/47595 orbits;
     key counts 715/1001/1365; cap-set inclusion.
R2   (r=2 closed form via K0864 Lemma FL + cap<=12 anchor)  For r=2 the
     survivor is the complement of the first loser, so K0864's universal
     Lemma FL (possible first losers == {C_i mod r}, any branch count,
     any r, no size bound) gives a closed form: all C_i congruent mod 2
     -> first loser P_p in every play, survivor P_{1-p}, DETERMINED;
     mixed parities -> first losers {P_0,P_1}, survivor set {P_0,P_1},
     NON-determined; gamma and the atom distribution are irrelevant.
     The committed cap<=12 records anchor this universally-proved
     corollary over all 47595 profiles (448 uniformly determined keys /
     917 uniformly non-determined keys / 0 mixed; every profile's
     survivor set == its chain profile's set; uniform-parity profiles
     carry survivor [1-p] and first loser [p], mixed-parity profiles
     carry [0,1]/[0,1]); the cap<=10 sub-census equals the published
     K0864 values (245 determined keys, no failing keys).  The K0869
     echo-dormancy rows (the r=8 failing families are uniformly
     DETERMINED at r=2 with chain survivor P_1) and the K0866 pre-echo
     rows (the r=7 failing families are uniformly non-determined at
     r=2) are re-derived from the records.
I278 (Theorem I278, cap<=12, r=7,8, finite complete)  For r=7 and r=8
     the determinacy non-collapse key set at cap<=12 is EXACTLY the
     published cap<=10 boundary (K0866/K0869): r=7 the 6 keys
     (4,4,9),(4,9,9) x gamma=0..2; r=8 the 10 keys (6,6,8),(6,8,8) x
     gamma=0..4.  ZERO new non-collapse keys appear when the size bound
     is raised from 10 to 12: every key containing an 11- or 12-branch
     collapses.  Failing-key structure is unchanged from K0866/K0869:
     det-side survivor uniformly P_3 (r=7) / P_5 (r=8), ndet possible-
     survivor sets within the published bounds ({1,2,3} / {3,4,5}),
     partition counts equal to the published tables, residue pairs
     {2,4} (r=7) / {0,6} (r=8), FL violations 0, Delta=0 uniform
     profiles (1512) all Theorem D, cap<=10 uniformly-determined
     sub-census 98/98 and two-residue sub-census 362/347 (K0872).
MX   (K0874 52-key matrix cross-artifact)  The committed records
     restricted to the cap<=10 profiles of the 52 tracked keys
     reproduce the published K0874 matrix cells at r=2,7,8 exactly
     (156 cells: collapsed / uniform flags, survivor-set variety,
     decided counts, chain verdicts, first-loser residues).

Scope / limits (do not over-read):
- I278 is COMPLETE over the finite parameter domain stated (all canonical
  profiles with branch sizes <= 12, r=7,8) - via Theorem E' it applies
  to every board realizing such a profile.
- The r=2 closed form is a corollary of the universally proved K0864
  Lemma FL; the cap<=12 sweep is a redundant machine anchor, not the
  proof.  r=2 needs no further sweep at any size bound.
- Branch sizes >= 13 and r >= 9 are NOT covered here.
- The mask engine does not reproduce elimination-order fields; order
  determinacy claims are NOT re-derived here.
- Uniformly non-determined does NOT mean "outcome-free": the possible
  survivor sets still depend on atoms for r>=7 outside the failing
  families; only the failing-family bounds are asserted.
- 11x11 empty board / class frontiers remain UNKNOWN, unrelated.
"""

import gzip
import hashlib
import json
import os
import sys

sys.setrecursionlimit(100000)


# K0859 published uniform elimination table (C=1..12 x r=2..8), canonical
# JSON byte-verified against main (verbatim from the K0875 verifier).
PUBLISHED_UNIFORM_ELIMINATION_TABLE_JSON = (
    '{"1":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[1,2],"survivor":0},"4":{"elimination":[1,2,3],"survivor":0},"5":{"elimination":[1,2,3,4],"survivor":0},"6":{"elimination":[1,2,3,4,5],"survivor":0},"7":{"elimination":[1,2,3,4,5,6],"survivor":0},"8":{"elimination":[1,2,3,4,5,6,7],"survivor":0}},"10":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[1,0],"survivor":2},"4":{"elimination":[2,1,0],"survivor":3},"5":{"elimination":[0,3,2,1],"survivor":4},"6":{"elimination":[4,0,3,2,1],"survivor":5},"7":{"elimination":[3,5,0,4,2,1],"survivor":6},"8":{"elimination":[2,4,6,0,5,3,1],"survivor":7}},"11":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[2,1],"survivor":0},"4":{"elimination":[3,2,1],"survivor":0},"5":{"elimination":[1,4,3,2],"survivor":0},"6":{"elimination":[5,1,4,3,2],"survivor":0},"7":{"elimination":[4,6,1,5,3,2],"survivor":0},"8":{"elimination":[3,5,7,1,6,4,2],"survivor":0}},"12":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[0,1],"survivor":2},"4":{"elimination":[0,1,2],"survivor":3},"5":{"elimination":[2,0,1,3],"survivor":4},"6":{"elimination":[0,3,1,2,4],"survivor":5},"7":{"elimination":[5,0,3,1,2,4],"survivor":6},"8":{"elimination":[4,6,0,3,1,2,5],"survivor":7}},"2":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[2,0],"survivor":1},"4":{"elimination":[2,3,0],"survivor":1},"5":{"elimination":[2,3,4,0],"survivor":1},"6":{"elimination":[2,3,4,5,0],"survivor":1},"7":{"elimination":[2,3,4,5,6,0],"survivor":1},"8":{"elimination":[2,3,4,5,6,7,0],"survivor":1}},"3":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[0,2],"survivor":1},"4":{"elimination":[3,0,2],"survivor":1},"5":{"elimination":[3,4,0,2],"survivor":1},"6":{"elimination":[3,4,5,0,2],"survivor":1},"7":{"elimination":[3,4,5,6,0,2],"survivor":1},"8":{"elimination":[3,4,5,6,7,0,2],"survivor":1}},"4":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[1,0],"survivor":2},"4":{"elimination":[0,2,1],"survivor":3},"5":{"elimination":[4,0,2,1],"survivor":3},"6":{"elimination":[4,5,0,2,1],"survivor":3},"7":{"elimination":[4,5,6,0,2,1],"survivor":3},"8":{"elimination":[4,5,6,7,0,2,1],"survivor":3}},"5":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[2,1],"survivor":0},"4":{"elimination":[1,3,2],"survivor":0},"5":{"elimination":[0,2,4,3],"survivor":1},"6":{"elimination":[5,0,2,4,3],"survivor":1},"7":{"elimination":[5,6,0,2,4,3],"survivor":1},"8":{"elimination":[5,6,7,0,2,4,3],"survivor":1}},"6":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[0,1],"survivor":2},"4":{"elimination":[2,0,1],"survivor":3},"5":{"elimination":[1,3,0,2],"survivor":4},"6":{"elimination":[0,2,4,1,3],"survivor":5},"7":{"elimination":[6,0,2,4,1,3],"survivor":5},"8":{"elimination":[6,7,0,2,4,1,3],"survivor":5}},"7":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[1,2],"survivor":0},"4":{"elimination":[3,1,2],"survivor":0},"5":{"elimination":[2,4,1,3],"survivor":0},"6":{"elimination":[1,3,5,2,4],"survivor":0},"7":{"elimination":[0,2,4,6,3,5],"survivor":1},"8":{"elimination":[7,0,2,4,6,3,5],"survivor":1}},"8":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[2,0],"survivor":1},"4":{"elimination":[0,3,1],"survivor":2},"5":{"elimination":[3,0,4,1],"survivor":2},"6":{"elimination":[2,4,0,5,1],"survivor":3},"7":{"elimination":[1,3,5,0,6,2],"survivor":4},"8":{"elimination":[0,2,4,6,1,7,3],"survivor":5}},"9":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[0,2],"survivor":1},"4":{"elimination":[1,0,3],"survivor":2},"5":{"elimination":[4,1,0,3],"survivor":2},"6":{"elimination":[3,5,1,0,4],"survivor":2},"7":{"elimination":[2,4,6,1,0,5],"survivor":3},"8":{"elimination":[1,3,5,7,2,0,6],"survivor":4}}}'
)

# ---------------------------------------------------------------------------
# verbatim engine block (K0862 verifier via K0875 verifier)
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# published constants
# ---------------------------------------------------------------------------

# Burnside / enumeration expectations (K0875, r-independent).
EXPECTED_BURNSIDE = {
    10: {"fix_id": 84494, "fix_trans": 3478, "fix_cyc": 125, "orbits": 15863},
    11: {"fix_id": 152171, "fix_trans": 5299, "fix_cyc": 161, "orbits": 28065},
    12: {"fix_id": 261749, "fix_trans": 7805, "fix_cyc": 203, "orbits": 47595},
}
EXPECTED_KEYS_BY_CAP = {"10": 715, "11": 1001, "12": 1365}

# --- K0864 (r=2 cap<=10 sweep, published)
K0864_R2_CAP10 = {"det_keys": 245, "failing_keys": [], "keys": 715, "profiles": 15863}
# --- K0866 (r=7 cap<=10 boundary, published)
K0866_SWEEP_R7 = {"det_keys": 98, "failing_keys": [[[4, 4, 9], 0], [[4, 4, 9], 1], [[4, 4, 9], 2], [[4, 9, 9], 0], [[4, 9, 9], 1], [[4, 9, 9], 2]], "keys": 715, "profiles": 15863}
K0866_PARTITION_49_R7 = {"4,4,9|0": {"n_det": 16, "n_ndet": 4, "profiles": 20}, "4,4,9|1": {"n_det": 7, "n_ndet": 3, "profiles": 10}, "4,4,9|2": {"n_det": 2, "n_ndet": 2, "profiles": 4}, "4,9,9|0": {"n_det": 39, "n_ndet": 6, "profiles": 45}, "4,9,9|1": {"n_det": 22, "n_ndet": 6, "profiles": 28}, "4,9,9|2": {"n_det": 7, "n_ndet": 6, "profiles": 13}}
K0866_WITNESSES_R7 = {"4,4,9|0#7": {"chain_survivors": [3], "det_atoms": [1, 1, 1, 5, 2, 2, 0], "det_cells": 12, "det_survivors": [3], "ndet_atoms": [1, 1, 0, 3, 3, 3, 0], "ndet_cells": 11, "ndet_survivors": [1, 2, 3]}, "4,4,9|1#7": {"chain_survivors": [3], "det_atoms": [1, 1, 1, 6, 1, 1, 1], "det_cells": 12, "det_survivors": [3], "ndet_atoms": [1, 1, 0, 4, 2, 2, 1], "ndet_cells": 11, "ndet_survivors": [1, 2, 3]}, "4,4,9|2#7": {"chain_survivors": [3], "det_atoms": [1, 1, 1, 7, 0, 0, 2], "det_cells": 12, "det_survivors": [3], "ndet_atoms": [1, 1, 0, 5, 1, 1, 2], "ndet_cells": 11, "ndet_survivors": [1, 2, 3]}, "4,9,9|0#7": {"chain_survivors": [3], "det_atoms": [1, 1, 2, 2, 1, 6, 0], "det_cells": 13, "det_survivors": [3], "ndet_atoms": [1, 1, 3, 4, 0, 5, 0], "ndet_cells": 14, "ndet_survivors": [1, 2, 3]}, "4,9,9|1#7": {"chain_survivors": [3], "det_atoms": [1, 1, 1, 1, 1, 6, 1], "det_cells": 12, "det_survivors": [3], "ndet_atoms": [1, 1, 2, 3, 0, 5, 1], "ndet_cells": 13, "ndet_survivors": [1, 2, 3]}, "4,9,9|2#7": {"chain_survivors": [3], "det_atoms": [1, 1, 6, 2, 0, 0, 2], "det_cells": 12, "det_survivors": [3], "ndet_atoms": [1, 1, 1, 2, 0, 5, 2], "ndet_cells": 12, "ndet_survivors": [1, 2, 3]}}
K0866_PRE_ECHO_49_R2 = {"4,4,9|0": {"chain_determined": False, "n_det": 0}, "4,4,9|1": {"chain_determined": False, "n_det": 0}, "4,4,9|2": {"chain_determined": False, "n_det": 0}, "4,4,9|3": {"chain_determined": False, "n_det": 0}, "4,9,9|0": {"chain_determined": False, "n_det": 0}, "4,9,9|1": {"chain_determined": False, "n_det": 0}, "4,9,9|2": {"chain_determined": False, "n_det": 0}, "4,9,9|3": {"chain_determined": False, "n_det": 0}}
# --- K0869 (r=8 cap<=10 boundary, published)
K0869_SWEEP_R8 = {"failing_keys": [[[6, 6, 8], 0], [[6, 6, 8], 1], [[6, 6, 8], 2], [[6, 6, 8], 3], [[6, 6, 8], 4], [[6, 8, 8], 0], [[6, 8, 8], 1], [[6, 8, 8], 2], [[6, 8, 8], 3], [[6, 8, 8], 4]], "keys": 715, "profiles": 15863, "uniformly_determined_keys": 98}
K0869_PARTITION_68_R8 = {"6,6,8|0": {"chain_survivors": [5], "det_atoms": [1, 1, 2, 2, 3, 3, 0], "det_survivors": [5], "n_det": 48, "ndet_atoms": [1, 1, 5, 4, 0, 2, 0], "ndet_survivors": [3, 4, 5], "profiles": 51}, "6,6,8|1": {"chain_survivors": [5], "det_atoms": [1, 1, 1, 1, 3, 3, 1], "det_survivors": [5], "n_det": 30, "ndet_atoms": [1, 1, 4, 3, 0, 2, 1], "ndet_survivors": [3, 4, 5], "profiles": 33}, "6,6,8|2": {"chain_survivors": [5], "det_atoms": [1, 1, 1, 2, 2, 2, 2], "det_survivors": [5], "n_det": 16, "ndet_atoms": [1, 1, 3, 2, 0, 2, 2], "ndet_survivors": [3, 4, 5], "profiles": 19}, "6,6,8|3": {"chain_survivors": [5], "det_atoms": [1, 1, 1, 3, 1, 1, 3], "det_survivors": [5], "n_det": 7, "ndet_atoms": [1, 1, 0, 1, 2, 2, 3], "ndet_survivors": [3, 4, 5], "profiles": 10}, "6,6,8|4": {"chain_survivors": [5], "det_atoms": [1, 1, 1, 4, 0, 0, 4], "det_survivors": [5], "n_det": 2, "ndet_atoms": [1, 1, 0, 2, 1, 1, 4], "ndet_survivors": [3, 4, 5], "profiles": 4}, "6,8,8|0": {"chain_survivors": [5], "det_atoms": [1, 1, 3, 2, 2, 4, 0], "det_survivors": [5], "n_det": 63, "ndet_atoms": [1, 1, 5, 6, 0, 2, 0], "ndet_survivors": [3, 4, 5], "profiles": 66}, "6,8,8|1": {"chain_survivors": [5], "det_atoms": [1, 1, 2, 1, 2, 4, 1], "det_survivors": [5], "n_det": 42, "ndet_atoms": [1, 1, 4, 5, 0, 2, 1], "ndet_survivors": [3, 4, 5], "profiles": 45}, "6,8,8|2": {"chain_survivors": [5], "det_atoms": [1, 1, 2, 2, 1, 3, 2], "det_survivors": [5], "n_det": 24, "ndet_atoms": [1, 1, 3, 4, 0, 2, 2], "ndet_survivors": [3, 4, 5], "profiles": 27}, "6,8,8|3": {"chain_survivors": [5], "det_atoms": [1, 1, 1, 1, 1, 3, 3], "det_survivors": [5], "n_det": 13, "ndet_atoms": [1, 1, 2, 3, 0, 2, 3], "ndet_survivors": [3, 4, 5], "profiles": 16}, "6,8,8|4": {"chain_survivors": [5], "det_atoms": [1, 1, 3, 2, 0, 0, 4], "det_survivors": [5], "n_det": 4, "ndet_atoms": [1, 1, 1, 2, 0, 2, 4], "ndet_survivors": [3, 4, 5], "profiles": 7}}
K0869_ECHO_DORMANCY_R2 = {"6,6,8|0#2": {"chain_survivors": [1], "n_det": 51, "profiles": 51, "survivor_mismatch": 0}, "6,6,8|1#2": {"chain_survivors": [1], "n_det": 33, "profiles": 33, "survivor_mismatch": 0}, "6,6,8|2#2": {"chain_survivors": [1], "n_det": 19, "profiles": 19, "survivor_mismatch": 0}, "6,6,8|3#2": {"chain_survivors": [1], "n_det": 10, "profiles": 10, "survivor_mismatch": 0}, "6,6,8|4#2": {"chain_survivors": [1], "n_det": 4, "profiles": 4, "survivor_mismatch": 0}, "6,8,8|0#2": {"chain_survivors": [1], "n_det": 66, "profiles": 66, "survivor_mismatch": 0}, "6,8,8|1#2": {"chain_survivors": [1], "n_det": 45, "profiles": 45, "survivor_mismatch": 0}, "6,8,8|2#2": {"chain_survivors": [1], "n_det": 27, "profiles": 27, "survivor_mismatch": 0}, "6,8,8|3#2": {"chain_survivors": [1], "n_det": 16, "profiles": 16, "survivor_mismatch": 0}, "6,8,8|4#2": {"chain_survivors": [1], "n_det": 7, "profiles": 7, "survivor_mismatch": 0}}
# --- K0872 (cap<=10 two-residue key counts, published)
K0872_TWO_RESIDUE_KEYS_CAP10 = {"7": 362, "8": 347}
# --- K0874 (52-key matrix, published; r=2,7,8 columns)
# K0874 matrix read at runtime from the sibling experiment audit (pinned below)

# K0874 published 52-key determinacy-state matrix (r=2..8), read at run
# time from the sibling experiment audit (same pattern as the K0875 audit
# read in the K0876 verifier). The 52 keys = 44 published non-collapse
# keys (r=3..8 union) + 8 keys of the (4,4,10)/(4,10,10) family.
K0874_AUDIT_RELPATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "remo-failure-family-matrix-independent-20261116",
    "output", "remo_failure_family_matrix_independent_audit.json",
)
K0874_AUDIT_SHA256 = (
    "6e68a86f016dc07600309dbdb992fb7b5eacb11c2fa41f2be0501463c2418e73"
)

# r=2 cap<=12 census values from the committed sweep records (packed
# publication format, sha256-pinned in sweep_inputs; the closed form
# itself is the K0864 Lemma FL corollary stated in the header - these
# constants pin the record content, the live checks validate the
# engine independently).
R2_CAP12_CENSUS = {"uniformly_determined_keys": 448,
                   "uniformly_ndet_keys": 917, "mixed_keys": 0,
                   "two_residue_keys": 917, "max_states": 6526}

R_VALUES = (2, 7, 8)
SAMPLE_STRIDE = {2: 24, 7: 48, 8: 48}

# The 10 small-branch keys and the 6 mirror keys (K0862/K0864 published
# key families; recorded per-key n_det as data in the analysis, their
# r=2,7,8 fates are asserted through the K0874 matrix cross-check).
SMALL_KEYS_10 = sorted(
    [[list(sp), g] for sp, g in zip(
        [[2, 3, 8], [2, 3, 8], [2, 8, 9], [2, 8, 9], [3, 3, 8],
         [3, 3, 8], [3, 8, 8], [3, 8, 8], [3, 8, 9], [3, 8, 9]],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1])]
)
MIRROR_KEYS_6 = [[[4, 4, 8], g] for g in range(3)] \
    + [[[4, 8, 8], g] for g in range(3)]

# K0866/K0869 published failing-key structure at cap<=10 (machine-extracted
# above; summarized here in the shape the audit code consumes).
R_BOUNDARY_FAILING = {
    7: K0866_SWEEP_R7["failing_keys"],
    8: K0869_SWEEP_R8["failing_keys"],
}
R_BOUNDARY_DET_SURVIVOR = {7: [3], 8: [5]}
R_BOUNDARY_NDET_BOUND = {7: [[1, 2, 3]], 8: [[3, 4, 5]]}
R_BOUNDARY_RESIDUE_PAIR = {7: [2, 4], 8: [0, 6]}
DELTA0_EXPECTED = 1512


def load_jsonl(r):
    """Committed sweep records for r -> (records, format).

    Full format first (js_cap12_r{r}.jsonl[.gz], one JSON object per
    line: i, atoms, determined, survivors, first_losers, states), then
    the packed publication format (js_cap12_r{r}.packed.jsonl, one JSON
    array per line: [i, sv_mask, fl_mask, states]). The packed format is
    the one committed under output/: the full-format files exceeded the
    GitHub push transport size limit during the original K0876
    publication (8 of 12 artifacts were lost; repaired by re-publishing
    the same deterministic records in packed form). Packed records store
    everything the checks need; atoms are NOT stored because atoms are a
    pure function of i (canonical cap<=12 enumeration,
    direct_constrained below), so they are re-derived by the caller (C2)
    and the C2 atoms check is vacuous-but-recorded in packed mode (the
    engine-vs-enumeration agreement is instead re-verified live by the
    mask-twin live checks, which never read atoms from the records).
    """
    base = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "output", "js_cap12_r%d.jsonl" % r,
    )
    if os.path.exists(base + ".gz"):
        with gzip.open(base + ".gz", "rt", encoding="utf-8") as f:
            lines = f.read().splitlines()
        return [json.loads(line) for line in lines if line.strip()], "full"
    if os.path.exists(base):
        with open(base, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
        return [json.loads(line) for line in lines if line.strip()], "full"
    packed_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "output", "js_cap12_r%d.packed.jsonl" % r,
    )
    if os.path.exists(packed_path):
        out = []
        with open(packed_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                i, sv, fl, states = json.loads(line)
                survivors = [p for p in range(64) if (sv >> p) & 1]
                first_losers = [p for p in range(64) if (fl >> p) & 1]
                out.append({
                    "i": i,
                    "atoms": None,  # re-derived by the caller (C2)
                    "determined": len(survivors) == 1,
                    "survivors": survivors,
                    "first_losers": first_losers,
                    "states": states,
                })
        return out, "packed"
    raise FileNotFoundError(base + "[.gz] / " + packed_path)


def analyze_r(r, profiles, pidx, records):
    byk = {}
    for i, atoms in enumerate(profiles):
        byk.setdefault(key_of(atoms), []).append(records[r][i])
    out = {}
    out["keys"] = len(byk)
    out["keys_by_cap"] = {
        "10": sum(1 for k in byk if max(k[0]) <= 10),
        "11": sum(1 for k in byk if max(k[0]) <= 11),
        "12": len(byk),
    }
    failing = sorted(k for k, rs in byk.items()
                     if len({rec["determined"] for rec in rs}) > 1)
    out["failing_keys"] = sorted([list(k[0]), k[1]] for k in failing)
    part = {}
    det_surv = set()
    ndet_sets = set()
    ndet_by_key = {}
    for k in failing:
        rs = byk[k]
        det = [rec for rec in rs if rec["determined"]]
        ndet = [rec for rec in rs if not rec["determined"]]
        part[kstr(k)] = {"n_det": len(det), "profiles": len(rs)}
        det_surv |= {tuple(rec["survivors"]) for rec in det}
        sets_k = sorted(list(t) for t in {tuple(sorted(rec["survivors"])) for rec in ndet})
        ndet_by_key[kstr(k)] = sets_k
        ndet_sets |= {tuple(s) for s in sets_k}
    out["failing_partitions"] = part
    out["failing_det_survivors"] = sorted(list(t) for t in det_surv)
    out["failing_ndet_sets"] = sorted(list(t) for t in ndet_sets)
    out["failing_ndet_sets_by_key"] = ndet_by_key
    # det-map census (K0875 convention: non-mixed keys only)
    det_map = []
    uni_det = 0
    uni_ndet = 0
    for k, rs in byk.items():
        flags = {rec["determined"] for rec in rs}
        if len(flags) > 1:
            continue
        b = flags.pop()
        det_map.append([list(k[0]), k[1], b])
        if b:
            uni_det += 1
        else:
            uni_ndet += 1
    det_map.sort(key=lambda e: (e[0], e[1]))
    out["det_map_collapsing_keys"] = det_map
    out["uniformly_determined_keys"] = uni_det
    out["uniformly_ndet_keys"] = uni_ndet
    out["mixed_keys"] = len(failing)
    # G' survivor level (chain agreement), cap<=12 extension
    gprime_mism = 0
    new_uni_det = 0
    new_uni_ndet = 0
    new_gprime_mism = 0
    new_uni_ndet_chain_equal = 0
    for k, rs in byk.items():
        is_new = 11 in k[0] or 12 in k[0]
        flags = {rec["determined"] for rec in rs}
        # every realizable key has gamma < min(sizes) (singleton atoms are
        # >= 1), so the chain profile always exists
        chain = records[r][pidx[chain_profile(k[0], k[1], 3)]]
        if flags == {True}:
            if is_new:
                new_uni_det += 1
            # Theorem G' survivor level: EVERY determined profile of the
            # key must carry the chain survivor (this also forces the
            # determined survivors to be uniform within the key).
            if any(rec["survivors"] != chain["survivors"] for rec in rs):
                gprime_mism += 1
                if is_new:
                    new_gprime_mism += 1
        elif flags == {False}:
            if is_new:
                new_uni_ndet += 1
                union = sorted({p for rec in rs for p in rec["survivors"]})
                if chain["survivors"] == union:
                    new_uni_ndet_chain_equal += 1
    out["gprime_survivor_mismatches"] = gprime_mism
    # cap<=10 sub-census
    cap10_keys = [k for k in byk if max(k[0]) <= 10]
    out["uniformly_determined_keys_cap10"] = sum(
        1 for k in cap10_keys
        if {rec["determined"] for rec in byk[k]} == {True}
    )
    out["two_residue_keys_cap10"] = sum(
        1 for k in cap10_keys if len({c % r for c in k[0]}) == 2
    )
    # new-key census
    out["new_key_census"] = {
        "keys_with_11": sum(1 for k in byk if 11 in k[0]),
        "keys_with_12": sum(1 for k in byk if 12 in k[0]),
        "failing_with_11_or_12": sum(
            1 for k in failing if 11 in k[0] or 12 in k[0]),
        "uniformly_det": new_uni_det,
        "uniformly_ndet": new_uni_ndet,
        "uniformly_det_gprime_mismatch": new_gprime_mism,
        "uniformly_ndet_chain_equals_union": new_uni_ndet_chain_equal,
    }
    # fixed published key families (cap-independent per-key n_det)
    def key_ndet(keys):
        res = {}
        for sp, g in keys:
            k = (tuple(sp), g)
            if k in byk:
                res[kstr(k)] = sum(1 for rec in byk[k] if rec["determined"])
        return res
    out["small_keys_10_ndet"] = key_ndet(SMALL_KEYS_10)
    out["mirror_keys_6_ndet"] = key_ndet(MIRROR_KEYS_6)
    # FL anchor
    fl_viol = 0
    for i, atoms in enumerate(profiles):
        want = sorted({c % r for c in profile_sizes(atoms, 3)})
        if records[r][i]["first_losers"] != want:
            fl_viol += 1
    out["first_loser_violations"] = fl_viol
    # Delta=0 anchor
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
        _, surv = theorem_d(sizes[0], r)
        rec = records[r][i]
        if not (rec["determined"] and rec["survivors"] == [surv]):
            d0_mism += 1
    out["delta0_profiles"] = d0
    out["delta0_with_size_11_or_12"] = d0_new
    out["delta0_mismatches"] = d0_mism
    # residue lens
    out["two_residue_keys"] = sum(
        1 for k in byk if len({c % r for c in k[0]}) == 2)
    out["failing_residue_pairs"] = sorted(
        [list(t) for t in {tuple(sorted({c % r for c in k[0]})) for k in failing}]
    )
    out["failing_keys_two_residue"] = all(
        len({c % r for c in k[0]}) == 2 for k in failing)
    census = {}
    for k in byk:
        if not (11 in k[0] or 12 in k[0]):
            continue
        pair = ",".join(map(str, sorted({c % r for c in k[0]})))
        e = census.setdefault(pair, {"keys": 0, "mixed": 0,
                                     "uniformly_det": 0, "uniformly_ndet": 0})
        e["keys"] += 1
        flags = {rec["determined"] for rec in byk[k]}
        if len(flags) > 1:
            e["mixed"] += 1
        elif flags == {True}:
            e["uniformly_det"] += 1
        else:
            e["uniformly_ndet"] += 1
    out["new_key_residue_census"] = census
    out["new_two_residue_keys"] = sum(
        e["keys"] for p, e in census.items() if "," in p)
    fp = R_BOUNDARY_RESIDUE_PAIR.get(r)
    if fp is not None:
        new_fp = [
            k for k in byk
            if (11 in k[0] or 12 in k[0])
            and sorted({c % r for c in k[0]}) == fp
        ]
        out["new_keys_with_published_failing_pair"] = {
            "pair": fp,
            "keys": len(new_fp),
            "mixed": sum(
                1 for k in new_fp
                if len({rec["determined"] for rec in byk[k]}) > 1),
        }
    out["max_states"] = max(rec["states"] for rec in records[r].values())
    return out, byk


def assemble_audit():
    checks = []

    def record(name, ok, data):
        checks.append({"name": name, "ok": bool(ok), "data": data})

    audit = {"meta": {
        "item": "K0881",
        "title": "3-branch REMO determinacy size boundary cap<=12 for "
            "r=2,7,8: the K0875/K0876 open cells (r=7,8 x sizes 11,12; "
            "the r=2 column as a K0864 Lemma FL closed-form anchor)",
        "date": "2026-11-16",
        "engine_provenance": "verbatim region game / enumeration / "
            "Burnside / Theorem D from the K0862 verifier via K0875 and "
            "K0876; full-domain records produced by the committed "
            "JavaScript mask engine (mask_engine_fast.js, verbatim from "
            "the K0876 experiment); Python mask twin cross-validated "
            "live in every run",
        "r_swept": [2, 7, 8],
    }}

    # ---- C1: enumeration / Burnside (r-independent, K0875 anchor)
    enum = {}
    audit["burnside"] = {}
    for cap in (10, 11, 12):
        fi, ft, fc, orbits = burnside_fix_counts(cap)
        profs = direct_constrained(cap)
        enum[cap] = profs
        exp = EXPECTED_BURNSIDE[cap]
        audit["burnside"][str(cap)] = {
            "fix_id": fi, "fix_trans": ft, "fix_cyc": fc, "orbits": orbits,
        }
        ok = (
            orbits == len(profs) == exp["orbits"]
            and (fi, ft, fc)
            == (exp["fix_id"], exp["fix_trans"], exp["fix_cyc"])
        )
        record(
            "cap=%d: Burnside orbit count == direct canonical enumeration "
            "(%d profiles)" % (cap, exp["orbits"]),
            ok,
            {"fix_id": fi, "fix_trans": ft, "fix_cyc": fc,
             "orbits": orbits, "enum_count": len(profs)},
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

    # ---- C2: JSONL integrity for every r
    records = {}
    audit["sweep_inputs"] = {}
    for r in R_VALUES:
        recs, fmt = load_jsonl(r)
        if fmt == "packed":
            for rec in recs:
                rec["atoms"] = list(profiles[rec["i"]])
        ok = (
            len(recs) == 47595
            and [rec["i"] for rec in recs] == list(range(47595))
            and all(not rec.get("skipped") for rec in recs)
            and all(tuple(rec["atoms"]) == profiles[rec["i"]] for rec in recs)
            and all(
                rec["determined"] == (len(rec["survivors"]) == 1)
                and sorted(set(rec["survivors"])) == rec["survivors"]
                and sorted(set(rec["first_losers"])) == rec["first_losers"]
                and all(0 <= p < r
                       for p in rec["survivors"] + rec["first_losers"])
                and rec["states"] > 0
                for rec in recs
            )
        )
        blob = "\n".join(json.dumps(rec, sort_keys=True) for rec in recs)
        digest = hashlib.sha256(blob.encode()).hexdigest()
        gz_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "output", "js_cap12_r%d.jsonl.gz" % r,
        )
        gz_digest = None
        if os.path.exists(gz_path):
            with open(gz_path, "rb") as f:
                gz_digest = hashlib.sha256(f.read()).hexdigest()
        packed_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "output", "js_cap12_r%d.packed.jsonl" % r,
        )
        packed_digest = None
        if os.path.exists(packed_path):
            with open(packed_path, "rb") as f:
                packed_digest = hashlib.sha256(f.read()).hexdigest()
        audit["sweep_inputs"]["r%d" % r] = {
            "records": len(recs),
            "format": fmt,
            "skipped": sum(1 for rec in recs if rec.get("skipped")),
            "sha256_uncompressed": digest,
            "sha256_gz": gz_digest,
            "sha256_packed": packed_digest,
            "max_states": max(rec["states"] for rec in recs),
        }
        record(
            "r=%d committed sweep records: 47595 records, index-complete, "
            "atoms == enumeration, no budget skips" % r,
            ok,
            {"records": len(recs), "sha256": digest,
             "format": fmt, "sha256_packed": packed_digest},
        )
        records[r] = {rec["i"]: rec for rec in recs}

    # ---- per-r analysis
    analysis = {}
    byks = {}
    for r in R_VALUES:
        a, byk = analyze_r(r, profiles, pidx, records)
        analysis["r%d" % r] = a
        byks[r] = byk
        record(
            "r=%d key census: %d keys (715/1001/1365 by cap), %d uniformly "
            "determined, %d uniformly non-determined, %d mixed" % (
                r, a["keys"], a["uniformly_determined_keys"],
                a["uniformly_ndet_keys"], a["mixed_keys"]),
            a["keys"] == 1365
            and a["keys_by_cap"] == EXPECTED_KEYS_BY_CAP
            and a["uniformly_determined_keys"] + a["uniformly_ndet_keys"]
            + a["mixed_keys"] == 1365,
            {"keys_by_cap": a["keys_by_cap"]},
        )

    # ---- C3: r=2 closed form (K0864 Lemma FL corollary) + cap<=12 anchor
    a2 = analysis["r2"]
    closed_bad = 0
    chain_set_mism = 0
    for k, rs in byks[2].items():
        par = {c % 2 for c in k[0]}
        chain = records[2][pidx[chain_profile(k[0], k[1], 3)]]
        for rec in rs:
            if len(par) == 1:
                p = next(iter(par))
                if not (rec["determined"]
                        and rec["survivors"] == [1 - p]
                        and rec["first_losers"] == [p]):
                    closed_bad += 1
            else:
                if (rec["determined"] or rec["survivors"] != [0, 1]
                        or rec["first_losers"] != [0, 1]):
                    closed_bad += 1
            if rec["survivors"] != chain["survivors"]:
                chain_set_mism += 1
    ok = (
        a2["failing_keys"] == []
        and a2["mixed_keys"] == R2_CAP12_CENSUS["mixed_keys"]
        and a2["uniformly_determined_keys"]
        == R2_CAP12_CENSUS["uniformly_determined_keys"]
        and a2["uniformly_ndet_keys"]
        == R2_CAP12_CENSUS["uniformly_ndet_keys"]
        and a2["two_residue_keys"] == R2_CAP12_CENSUS["two_residue_keys"]
        and a2["max_states"] == R2_CAP12_CENSUS["max_states"]
        and a2["first_loser_violations"] == 0
        and a2["delta0_profiles"] == DELTA0_EXPECTED
        and a2["delta0_mismatches"] == 0
        and a2["gprime_survivor_mismatches"] == 0
        and a2["new_key_census"]["failing_with_11_or_12"] == 0
        and a2["new_key_census"]["uniformly_det_gprime_mismatch"] == 0
    )
    ok = (ok and closed_bad == 0 and chain_set_mism == 0)
    record(
        "r=2 closed form (K0864 Lemma FL corollary, universal): uniform "
        "size parity p -> determined, first loser P_p, survivor P_{1-p}; "
        "mixed parities -> first losers {P_0,P_1}, survivor set "
        "{P_0,P_1}; gamma and atoms irrelevant. Anchored over ALL 47595 "
        "cap<=12 profiles (0 violations) plus census 448/917/0, 917 "
        "two-residue keys, FL 0, Delta=0 1512 profiles, G' 0, no new "
        "11/12-branch keys fail, max_states 6526",
        ok,
        {"closed_form_violations": closed_bad,
         "chain_set_mismatches": chain_set_mism,
         "uniformly_determined_keys": a2["uniformly_determined_keys"],
         "uniformly_ndet_keys": a2["uniformly_ndet_keys"]},
    )
    record(
        "r=2 survivor-set level: every profile's possible-survivor set "
        "equals its chain profile's set over ALL 1365 keys x cap<=12 "
        "profiles (K0862 cap<=7 r=2 collapse extended; K0864 cap<=10 "
        "extension) - for r=2 this is an instance of the closed form "
        "above, recorded as data",
        chain_set_mism == 0,
        {"chain_set_mismatches": chain_set_mism},
    )
    record(
        "r=2 cap<=10 sub-census equals the published K0864 values "
        "(245 uniformly determined keys, 470 uniformly non-determined, "
        "no failing keys; mixed parity <=> uniformly non-determined)",
        a2["uniformly_determined_keys_cap10"] == K0864_R2_CAP10["det_keys"]
        and a2["uniformly_ndet_keys_cap10"] == K0864_R2_CAP10["keys"]
        - K0864_R2_CAP10["det_keys"]
        and a2["failing_keys"] == K0864_R2_CAP10["failing_keys"],
        {"uniformly_determined_cap10": a2["uniformly_determined_keys_cap10"],
         "uniformly_ndet_cap10": a2["uniformly_ndet_keys_cap10"]},
    )
    echo_ok = True
    for kk, v in K0869_ECHO_DORMANCY_R2.items():
        sp, g = kk.split("|")[0], kk.split("|")[1].split("#")[0]
        k = (tuple(int(x) for x in sp.split(",")), int(g))
        rs = byks[2][k]
        chain = records[2][pidx[chain_profile(k[0], k[1], 3)]]
        n_det = sum(1 for rec in rs if rec["determined"])
        if not (n_det == v["n_det"] == v["profiles"]
                and chain["determined"]
                and chain["survivors"] == v["chain_survivors"]
                and all(rec["survivors"] == v["chain_survivors"]
                        for rec in rs)):
            echo_ok = False
    record(
        "r=2 echo dormancy (K0869): the r=8 failing families (6,6,8),"
        "(6,8,8) x gamma=0..4 are uniformly DETERMINED at r=2 with "
        "chain survivor P_1 and zero survivor mismatches (10 keys)",
        echo_ok,
        {"keys": len(K0869_ECHO_DORMANCY_R2)},
    )
    pre_ok = True
    for kk, v in K0866_PRE_ECHO_49_R2.items():
        sp, g = kk.split("|")
        k = (tuple(int(x) for x in sp.split(",")), int(g))
        rs = byks[2][k]
        n_det = sum(1 for rec in rs if rec["determined"])
        if n_det != v["n_det"]:
            pre_ok = False
    record(
        "r=2 pre-echo (K0866): the r=7 failing families (4,4,9),(4,9,9) "
        "x gamma=0..3 are uniformly non-determined at r=2 (n_det == 0, "
        "8 keys incl. gamma=3 beyond the failing range)",
        pre_ok and all(v["n_det"] == 0 for v in K0866_PRE_ECHO_49_R2.values()),
        {"keys": len(K0866_PRE_ECHO_49_R2)},
    )

    # ---- C4: r=7,8 Theorem I278
    for r in (7, 8):
        a = analysis["r%d" % r]
        pub = sorted(R_BOUNDARY_FAILING[r])
        ok = (
            a["failing_keys"] == pub
            and a["failing_keys"] == (K0866_SWEEP_R7["failing_keys"]
                                      if r == 7
                                      else K0869_SWEEP_R8["failing_keys"])
            and a["new_key_census"]["failing_with_11_or_12"] == 0
            and a["new_key_census"]["mixed_keys"] == len(pub)
            and a["first_loser_violations"] == 0
            and a["delta0_profiles"] == DELTA0_EXPECTED
            and a["delta0_mismatches"] == 0
            and a["failing_det_survivors"] == [R_BOUNDARY_DET_SURVIVOR[r]]
            and all(
                t in [list(x) for x in R_BOUNDARY_NDET_BOUND[r]]
                for t in a["failing_ndet_sets"]
            )
            and a["failing_keys_two_residue"]
            and a["failing_residue_pairs"] == [R_BOUNDARY_RESIDUE_PAIR[r]]
        )
        record(
            "Theorem I278 (cap<=12, r=%d): non-collapse keys are exactly "
            "the published %d cap<=10 keys (%s); zero new keys with an "
            "11/12 branch fail; det survivor P_%d uniform; ndet sets "
            "within published bounds; FL violations 0; Delta=0 1512 "
            "profiles all Theorem D; failing residue pair %s" % (
                r, len(pub),
                "(4,4,9),(4,9,9) x g=0..2" if r == 7
                else "(6,6,8),(6,8,8) x g=0..4",
                R_BOUNDARY_DET_SURVIVOR[r][0],
                R_BOUNDARY_RESIDUE_PAIR[r]),
            ok,
            {"failing": len(a["failing_keys"]),
             "failing_with_11_or_12":
                 a["new_key_census"]["failing_with_11_or_12"]},
        )
        # partition counts vs published tables
        part_ok = True
        if r == 7:
            for kk, v in K0866_PARTITION_49_R7.items():
                got = a["failing_partitions"].get(kk)
                if got is None or got["n_det"] != v["n_det"] \
                        or got["profiles"] != v["profiles"]:
                    part_ok = False
        else:
            for kk, v in K0869_PARTITION_68_R8.items():
                got = a["failing_partitions"].get(kk)
                if got is None or got["n_det"] != v["n_det"] \
                        or got["profiles"] != v["profiles"]:
                    part_ok = False
        record(
            "r=%d failing-key partition counts match the published %s "
            "tables (%s)" % (
                r, "K0866" if r == 7 else "K0869",
                "(4,4,9)/(4,9,9)" if r == 7 else "(6,6,8)/(6,8,8)"),
            part_ok,
            {"families_checked": len(K0866_PARTITION_49_R7) if r == 7
             else len(K0869_PARTITION_68_R8)},
        )
        # witnesses valid inside the committed records
        wit_ok = True
        if r == 7:
            wit = {kk[:-2]: {"det_atoms": w["det_atoms"],
                             "ndet_atoms": w["ndet_atoms"],
                             "det_survivors": w["det_survivors"],
                             "ndet_survivors": w["ndet_survivors"],
                             "chain_survivors": w["chain_survivors"]}
                   for kk, w in K0866_WITNESSES_R7.items()}
        else:
            wit = {kk: {"det_atoms": w["det_atoms"],
                        "ndet_atoms": w["ndet_atoms"],
                        "det_survivors": w["det_survivors"],
                        "ndet_survivors": w["ndet_survivors"],
                        "chain_survivors": w["chain_survivors"]}
                   for kk, w in K0869_PARTITION_68_R8.items()}
        for kk, w in wit.items():
            for tag in ("det", "ndet"):
                atoms = tuple(w[tag + "_atoms"])
                idx = pidx.get(atoms)
                if idx is None:
                    wit_ok = False
                    continue
                rec = records[r][idx]
                want_det = tag == "det"
                want_surv = w[tag + "_survivors"]
                if not (rec["determined"] == want_det
                        and rec["survivors"] == want_surv):
                    wit_ok = False
            sp, g = kk.split("|")
            sizes = tuple(int(x) for x in sp.split(","))
            crec = records[r][pidx[chain_profile(sizes, int(g), 3)]]
            if not (crec["determined"]
                    and crec["survivors"] == w["chain_survivors"]):
                wit_ok = False
        record(
            "r=%d published failing-key witnesses (%s) and their chain "
            "survivors are valid inside the committed cap<=12 records" % (
                r, "K0866" if r == 7 else "K0869"),
            wit_ok,
            {"witness_keys": len(wit)},
        )
        # cap<=10 published sub-census
        sub_ok = (
            a["uniformly_determined_keys_cap10"]
            == (K0866_SWEEP_R7["det_keys"] if r == 7
                else K0869_SWEEP_R8["uniformly_determined_keys"])
            and a["two_residue_keys_cap10"]
            == K0872_TWO_RESIDUE_KEYS_CAP10[str(r)]
        )
        record(
            "r=%d cap<=10 sub-census from the committed records equals "
            "the published values (uniformly determined 98 keys, "
            "two-residue %d keys)" % (
                r, K0872_TWO_RESIDUE_KEYS_CAP10[str(r)]),
            sub_ok,
            {"uniformly_determined_cap10":
                 a["uniformly_determined_keys_cap10"],
             "two_residue_cap10": a["two_residue_keys_cap10"]},
        )
        # G' survivor level at cap<=12 (r=7,8)
        record(
            "r=%d Theorem G' survivor level at cap<=12: every uniformly "
            "determined key's survivor equals the chain survivor "
            "(%d keys, %d mismatches; %d of them NEW keys with 11/12 "
            "branches, %d new-key mismatches)" % (
                r, a["uniformly_determined_keys"],
                a["gprime_survivor_mismatches"],
                a["new_key_census"]["uniformly_det"],
                a["new_key_census"]["uniformly_det_gprime_mismatch"]),
            a["gprime_survivor_mismatches"] == 0,
            {"uniformly_determined_keys": a["uniformly_determined_keys"],
             "new_uniformly_det": a["new_key_census"]["uniformly_det"],
             "new_uniformly_ndet": a["new_key_census"]["uniformly_ndet"],
             "new_uniformly_ndet_chain_equals_union":
                 a["new_key_census"]["uniformly_ndet_chain_equals_union"]},
        )
        # residue lens
        fp = R_BOUNDARY_RESIDUE_PAIR[r]
        nfp = a["new_keys_with_published_failing_pair"]
        res_ok = (
            all(e["mixed"] == 0
                for e in a["new_key_residue_census"].values())
            and nfp["mixed"] == 0
        )
        record(
            "r=%d residue lens (K0872 extension): all %d new two-residue "
            "keys collapse, including %d new keys with the published "
            "failing pair %s (out-of-sample signature test)" % (
                r, a["new_two_residue_keys"], nfp["keys"], fp),
            res_ok,
            {"new_keys_with_failing_pair": nfp,
             "new_two_residue_keys": a["new_two_residue_keys"]},
        )

    # ---- C6: K0874 52-key matrix cross-artifact (r=2,7,8 columns)
    with open(K0874_AUDIT_RELPATH, "rb") as f:
        k0874_blob = f.read()
    k0874_sha = hashlib.sha256(k0874_blob).hexdigest()
    matrix_pub = json.loads(k0874_blob.decode())["matrix"]
    profs10 = direct_constrained(10)
    byk10 = {}
    for atoms in profs10:
        byk10.setdefault(key_of(atoms), []).append(atoms)

    def norm(x):
        return json.dumps(x, sort_keys=True)

    cell_mism = 0
    cells_checked = 0
    for kk, row in matrix_pub.items():
        sp, g = kk.split("|")
        k = (tuple(int(x) for x in sp.split(",")), int(g))
        for r in R_VALUES:
            pubc = row[str(r)]
            rs = [records[r][pidx[a]] for a in byk10.get(k, [])]
            dets = {rec["determined"] for rec in rs}
            got = {
                "profiles": len(rs),
                "collapsed": len(dets) == 1,
                "uniform_det": dets == {True},
                "uniform_ndet": dets == {False},
            }
            if dets == {True}:
                got["survivors"] = sorted(
                    {tuple(rec["survivors"]) for rec in rs})
            else:
                got["survivor_set_variety"] = sorted(
                    [list(rec["survivors"]) for rec in rs])
                got["survivor_set_varieties"] = len(
                    {tuple(rec["survivors"]) for rec in rs})
            if len(dets) > 1:
                got["decided"] = sum(1 for rec in rs if rec["determined"])
            chain = records[r][pidx[chain_profile(k[0], k[1], 3)]]
            got["chain_determined"] = chain["determined"]
            got["chain_survivors"] = chain["survivors"]
            got["first_loser_residues"] = sorted({c % r for c in k[0]})
            # normalize both sides through JSON (tuples vs lists)
            gjs = json.loads(norm(got))
            pjs = {key: val for key, val in pubc.items()
                   if key in got}
            # survivor_set_variety is per-profile in enumeration order in
            # the published matrix; compare as sorted multisets
            if "survivor_set_variety" in pjs:
                pjs["survivor_set_variety"] = sorted(
                    pjs["survivor_set_variety"])
                gjs["survivor_set_variety"] = sorted(
                    gjs["survivor_set_variety"])
            cells_checked += 1
            if not rs or norm(gjs) != norm(pjs):
                cell_mism += 1
    record(
        "K0874 52-key matrix cross-artifact: the committed records "
        "restricted to the cap<=10 profiles of the 52 tracked keys "
        "reproduce the published matrix cells at r=2,7,8 exactly "
        "(%d cells: collapsed/uniform flags, survivor-set variety, "
        "decided counts, chain verdicts, first-loser residues); audit "
        "file sha256 %s" % (cells_checked, K0874_AUDIT_SHA256[:12]),
        cell_mism == 0 and cells_checked == 156
        and k0874_sha == K0874_AUDIT_SHA256,
        {"cells": cells_checked, "mismatches": cell_mism,
         "audit_sha256": k0874_sha},
    )


    # ---- C5: Theorem D table
    entries, mism = theorem_d_table()
    record(
        "Theorem D recursion == K0859 published (C,r) table (84 entries)",
        mism == 0 and entries == 84,
        {"entries": entries, "mismatches": mism},
    )

    audit["sweeps"] = analysis
    audit["machine_checks"] = checks
    audit["summary"] = {
        "all_ok": all(c["ok"] for c in checks),
        "checks_total": len(checks),
    }
    return audit


def live_checks(audit):
    """Engine re-computations (not part of the audit bytes): the Python
    mask twin vs the verbatim engine, and both vs the committed JS
    records on deterministic samples."""
    profiles = direct_constrained(12)
    pidx = {atoms: i for i, atoms in enumerate(profiles)}
    recs = {r: {rec["i"]: rec
                for rec in load_jsonl(r)[0]} for r in R_VALUES}

    # L1: full cap<=7 domain, verbatim == mask twin == committed JS
    profs7 = direct_constrained(7)
    mism = 0
    n = 0
    for atoms in profs7:
        idx12 = pidx[atoms]
        for r in R_VALUES:
            v1, s1 = region_verdict(atoms, 3, r, budget=20_000_000)
            v2, s2 = mask_verdict(atoms, 3, r, budget=20_000_000)
            j = recs[r][idx12]
            n += 1
            if verdict_triple(v1) != verdict_triple(v2):
                mism += 1
            if verdict_triple(v2) != (j["determined"], j["survivors"],
                                      j["first_losers"]):
                mism += 1
            if s1 != s2 or s2 != j["states"]:
                mism += 1
    if mism != 0 or n != 3 * 2048:
        sys.stderr.write("LIVE FAIL: cap<=7 triple check %d mismatches / %d\n"
                         % (mism, n))
        sys.exit(1)
    print("LIVE OK: cap<=7 full domain: verbatim == mask twin == committed "
          "JS records (verdicts and state counts) on %d verdicts (r=2,7,8)"
          % n)

    # L2: stratified cap<=12 sample, mask twin == committed JS records
    mism = 0
    n = 0
    for r in R_VALUES:
        stride = SAMPLE_STRIDE[r]
        for i in range(0, len(profiles), stride):
            atoms = profiles[i]
            v2, _ = mask_verdict(atoms, 3, r, budget=50_000_000)
            j = recs[r][i]
            n += 1
            if verdict_triple(v2) != (j["determined"], j["survivors"],
                                     j["first_losers"]):
                mism += 1
    if mism != 0:
        sys.stderr.write("LIVE FAIL: stratified sample %d mismatches / %d\n"
                         % (mism, n))
        sys.exit(1)
    print("LIVE OK: stratified cap<=12 sample x r=2,7,8: mask twin == "
          "committed JS records on %d verdicts (strides %s)"
          % (n, SAMPLE_STRIDE))

    # L3: published witnesses re-run with the verbatim engine
    wit_fail = 0
    js_cmp = 0

    def check_witness(atoms, r, want_det, want_surv):
        nonlocal wit_fail, js_cmp
        v, _ = region_verdict(atoms, 3, r, budget=50_000_000)
        if not (v["determined"] == want_det
                and v["survivors"] == want_surv):
            wit_fail += 1
        idx = pidx.get(atoms)
        if idx is not None:
            j = recs[r][idx]
            js_cmp += 1
            if verdict_triple(v) != (j["determined"], j["survivors"],
                                    j["first_losers"]):
                wit_fail += 1

    # K0866 r=7 failing-key witnesses + chain survivors
    for kk, w in K0866_WITNESSES_R7.items():
        sp, g = kk.split("|")[0], kk.split("|")[1].split("#")[0]
        sizes = tuple(int(x) for x in sp.split(","))
        check_witness(tuple(w["det_atoms"]), 7, True, w["det_survivors"])
        check_witness(tuple(w["ndet_atoms"]), 7, False, w["ndet_survivors"])
        check_witness(chain_profile(sizes, int(g), 3), 7, True,
                      w["chain_survivors"])
    # K0869 r=8 failing-key witnesses + chain survivors
    for kk, w in K0869_PARTITION_68_R8.items():
        sp, g = kk.split("|")
        sizes = tuple(int(x) for x in sp.split(","))
        check_witness(tuple(w["det_atoms"]), 8, True, w["det_survivors"])
        check_witness(tuple(w["ndet_atoms"]), 8, False, w["ndet_survivors"])
        check_witness(chain_profile(sizes, int(g), 3), 8, True,
                      w["chain_survivors"])
    # r=2 echo dormancy: FULL re-run of the 10 K0869 families (278
    # profiles, all det with survivor P_1) + their chains
    byk_atoms = {}
    for atoms in profiles:
        byk_atoms.setdefault(key_of(atoms), []).append(atoms)
    echo_prof = 0
    for kk, v in K0869_ECHO_DORMANCY_R2.items():
        sp, g = kk.split("|")[0], kk.split("|")[1].split("#")[0]
        sizes = tuple(int(x) for x in sp.split(","))
        gamma = int(g)
        check_witness(chain_profile(sizes, gamma, 3), 2, True,
                      v["chain_survivors"])
        for atoms in byk_atoms[(sizes, gamma)]:
            echo_prof += 1
            check_witness(atoms, 2, True, v["chain_survivors"])
    # r=2 pre-echo: the 8 K0866-family chains are non-determined at r=2
    for kk, v in K0866_PRE_ECHO_49_R2.items():
        sp, g = kk.split("|")
        sizes = tuple(int(x) for x in sp.split(","))
        catoms = chain_profile(sizes, int(g), 3)
        cv, _ = region_verdict(catoms, 3, 2, budget=50_000_000)
        if cv["determined"] != v["chain_determined"]:
            wit_fail += 1
        js_cmp += 1
        j = recs[2][pidx[catoms]]
        if verdict_triple(cv) != (j["determined"], j["survivors"],
                                 j["first_losers"]):
            wit_fail += 1
    if wit_fail != 0:
        sys.stderr.write("LIVE FAIL: witness re-verification %d failures\n"
                         % wit_fail)
        sys.exit(1)
    print("LIVE OK: all published witnesses re-verified with the verbatim "
          "engine (K0866 6 keys at r=7, K0869 10 keys at r=8, det/ndet + "
          "chain survivors; r=2 echo dormancy full re-run %d profiles of "
          "the 10 K0869 families all det P_1; r=2 pre-echo 8 chains "
          "non-determined; %d witness verdicts also cross-checked against "
          "the committed JS records)" % (echo_prof, js_cmp))


def serialize(audit):
    return json.dumps(audit, sort_keys=True, ensure_ascii=False, indent=1) + "\n"


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
    out_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "output",
        "remo_k_branch_cap12_r278_boundary_audit.json",
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
    if not all_ok:
        sys.exit(1)
    live_checks(audit1)


if __name__ == "__main__":
    run()
