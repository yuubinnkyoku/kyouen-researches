#!/usr/bin/env python3
"""K0897 audit: 3-branch REMO determinacy r=11 boundary, branch sizes <= 10
(the third r >= 9 column of the r x size grid: r=11 combined with the
standard cap<=10 domain of 15863 canonical profiles / 715 keys).

Self-contained verifier. Deterministic (no randomness, no wall clock, no
network). Python 3.11+ / stdlib only.

Data provenance. The full-domain sweep record committed under output/
(js_cap10_r11.packed.jsonl - packed publication format, one JSON array
per canonical cap<=10 profile: [index, survivor_mask, first_loser_mask,
states]) was produced by the JavaScript mask engine committed in this
directory (mask_engine_fast_r11.js), a byte-identical copy of the K0893
committed fixed engine (the K0876 engine with the pack encoding shift
generalized from the fixed 8 bits to r; for r<=8 the encoding is
unchanged, and the K0893 publication regression-checked it against the
K0881 committed packed sweep records at r=2,7,8). Each record is a pure
function of (profile, r), so sweep segments are byte-concatenable. In
the packed format atoms are not stored: they are a pure function of the
index via the canonical cap<=10 enumeration re-derived inside this
verifier, so the packing is lossless. The mask engine carries
(survivorMask, firstLoserMask) per state instead of the verbatim
frozenset of (order, survivor) outcomes; determined / survivors /
first_losers agree with the verbatim engine's outcome_summary by
induction on the state DAG, and the reachable state space (hence the
per-record "states" count) is identical. This equivalence is
re-verified live in every run of this verifier:

- full cap<=7 domain (2048 canonical profiles) x r=11: verbatim engine
  == Python mask twin == committed JS records (2048 verdicts, verdict
  and state-count equality, 0 mismatches);
- stratified cap<=10 sample (every 32nd profile) x r=11: Python mask
  twin == committed JS records;
- all failing-key witnesses (det / ndet / chain per failing key) and
  the chains of the 56 published r=3..10 failing keys re-run with the
  verbatim engine and compared with the committed records and the
  pinned FATE rows.

The enumeration, Burnside machinery, Theorem D recursion, verbatim
region/cell game engine and the Python mask twin are verbatim from the
K0862 verifier via the K0875, K0876, K0881, K0893 and K0895 verifiers
(research/experiments/remo-k-branch-cap10-r10-boundary-20261117/
verify_remo_k_branch_cap10_r10_boundary.py).

Checked claims (proof text: report.md / item):

B    (Burnside vs direct enumeration, cap 10)  Identical to K0862/
     K0864/K0866/K0869/K0893/K0895 (r-independent): fix counts
     (84494,3478,125) -> 15863 orbits.
I11  (Theorem I r=11, cap<=10, finite complete)  The determinacy
     non-collapse (mixed) key set at r=11 is EXACTLY the pinned
     constant set (machine-extracted from the committed sweep records
     and re-derived by this verifier from them); every structural
     field (per-key partitions, det-side survivors, ndet possible-
     survivor sets, first-loser residue pairs, witness verdicts) is
     checked against the pinned constants. The set is IDENTICAL to
     the r=9 AND r=10 boundary sets (the 7 families of K0893/K0895):
     no new family wakes at r=11 and no family collapses. The (6,8,9)
     x gamma=0..3 family stays THREE-residue. FL violations 0 (Lemma
     FL is universally proved in K0864; here a redundant r=11
     anchor). Delta=0 uniform profiles (728) all Theorem D at r=11
     (the K0859 published (C,r) table covers r=2..8; the r=11 column
     is computed by the verbatim K0859 recursion inside this
     verifier).
RES  (r=11 residue arithmetic census, new column)  715 keys split
     into 55 single-residue / 330 two-residue / 330 three-residue
     keys (arithmetic only, no outcome data; K0872 published r=3..9,
     K0895 added r=10). The split is IDENTICAL to r=10: since r=11
     exceeds every branch size (<= 10) there is no modular
     wraparound, and the 55 single-residue keys are exactly the
     equal triples.
FATE  The 56 published r=3..10 failing keys' fates at r=11 are pinned
     as DATA (uniform_det / uniform_ndet / n_det / chain verdict per
     key) and re-derived twice (records + verbatim engine on chains).
     Outcome: ALL 34 keys that were mixed at r=9 and r=10 REMAIN
     mixed at r=11 (the 10 keys of the 6/8 family, the 12 keys of
     the 8/9 family, the 12 keys of the 6/9 family - the third
     consecutive identical column), while the other 22 keys stay
     uniformly non-determined with the same chain verdicts and chain
     survivor labels as at r=10: no collapse, no revival, no uniform
     determination.
STASIS (check C11)  The committed K0895 r=10 records
     (../remo-k-branch-cap10-r10-boundary-20261117/output/
     js_cap10_r10.packed.jsonl) and the committed r=11 records agree
     on the determined flag of EVERY ONE of the 15863 profiles
     (0 differences) AND on the full survivor mask of EVERY profile
     (0 survivor-mask differences: a full-column label fixpoint,
     strictly stronger than the r=9 -> r=10 det-flag-only fixpoint of
     K0895); the committed K0893 r=9 records also agree on every
     determined flag: THREE consecutive columns (r=9,10,11) with an
     identical determinacy classification of the whole cap<=10 domain
     (finite observation; the first-loser labels are NOT fixed: 7328
     first-loser masks differ between r=10 and r=11, and 7328/11533
     differ between r=9 and r=10/r=11).
G-prime  Theorem G' survivor level at r=11: every uniformly determined
     key's survivor equals the chain survivor (mismatch count pinned
     to 0).

Scope / limits (do not over read):
- I11 is COMPLETE over the finite parameter domain stated (all
  canonical 3-branch profiles with branch sizes <= 10, r=11) - via
  Theorem E' (K0861) it applies to every board realizing such a
  profile.
- Branch sizes 11, 12 at r=9,10,11 are NOT covered here (the K0881
  cap<=12 extension covered r=7,8; sizes 11,12 x r>=9 remains open).
- r >= 12 is NOT covered here.
- STASIS is a finite observation over three columns; it does NOT claim
  the boundary is stationary for all r >= 9.
- The mask engine does not reproduce elimination-order fields; order
  determinacy claims are NOT re-derived here.
- Uniformly non-determined does NOT mean "outcome-free": possible
  survivor sets still depend on atoms outside the failing families.
- The FATE rows are observations of the finite swept domain, not a
  general law about family windows.
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


# Machine-extracted constants: every field below was derived from the
# committed full sweep records (js_cap10_r9.jsonl -> output/r9_constants_extraction.json)
# by analyze_r9.py and is re-derived independently inside this verifier.
R11_SWEEP = {'delta0_mismatches': 0, 'delta0_profiles': 728, 'failing_det_survivors': [[5]], 'failing_keys': [[[6, 6, 8], 0], [[6, 6, 8], 1], [[6, 6, 8], 2], [[6, 6, 8], 3], [[6, 6, 8], 4], [[6, 6, 9], 0], [[6, 6, 9], 1], [[6, 6, 9], 2], [[6, 6, 9], 3], [[6, 8, 8], 0], [[6, 8, 8], 1], [[6, 8, 8], 2], [[6, 8, 8], 3], [[6, 8, 8], 4], [[6, 8, 9], 0], [[6, 8, 9], 1], [[6, 8, 9], 2], [[6, 8, 9], 3], [[6, 9, 9], 0], [[6, 9, 9], 1], [[6, 9, 9], 2], [[6, 9, 9], 3], [[8, 8, 9], 0], [[8, 8, 9], 1], [[8, 8, 9], 2], [[8, 8, 9], 3], [[8, 8, 9], 4], [[8, 8, 9], 5], [[8, 9, 9], 0], [[8, 9, 9], 1], [[8, 9, 9], 2], [[8, 9, 9], 3], [[8, 9, 9], 4], [[8, 9, 9], 5]], 'failing_keys_families': '(6,6,8) x gamma=0..4; (6,6,9) x gamma=0..3; (6,8,8) x gamma=0..4; (6,8,9) x gamma=0..3; (6,9,9) x gamma=0..3; (8,8,9) x gamma=0..5; (8,9,9) x gamma=0..5', 'failing_keys_two_residue': False, 'failing_ndet_sets': [[3, 4, 5], [3, 4, 5, 6, 7], [3, 4, 5, 7], [3, 5], [3, 5, 7]], 'failing_ndet_sets_by_key': {'6,6,8|0': [[3, 4, 5]], '6,6,8|1': [[3, 4, 5]], '6,6,8|2': [[3, 4, 5]], '6,6,8|3': [[3, 4, 5]], '6,6,8|4': [[3, 4, 5]], '6,6,9|0': [[3, 4, 5], [3, 5]], '6,6,9|1': [[3, 4, 5], [3, 5]], '6,6,9|2': [[3, 4, 5], [3, 5]], '6,6,9|3': [[3, 4, 5], [3, 5]], '6,8,8|0': [[3, 4, 5]], '6,8,8|1': [[3, 4, 5]], '6,8,8|2': [[3, 4, 5]], '6,8,8|3': [[3, 4, 5]], '6,8,8|4': [[3, 4, 5]], '6,8,9|0': [[3, 4, 5], [3, 4, 5, 7], [3, 5], [3, 5, 7]], '6,8,9|1': [[3, 4, 5], [3, 4, 5, 7], [3, 5], [3, 5, 7]], '6,8,9|2': [[3, 4, 5], [3, 4, 5, 7], [3, 5], [3, 5, 7]], '6,8,9|3': [[3, 4, 5], [3, 4, 5, 7], [3, 5], [3, 5, 7]], '6,9,9|0': [[3, 4, 5], [3, 5]], '6,9,9|1': [[3, 4, 5], [3, 5]], '6,9,9|2': [[3, 4, 5], [3, 5]], '6,9,9|3': [[3, 4, 5], [3, 5]], '8,8,9|0': [[3, 4, 5, 7], [3, 5, 7]], '8,8,9|1': [[3, 4, 5, 7], [3, 5, 7]], '8,8,9|2': [[3, 4, 5, 7], [3, 5, 7]], '8,8,9|3': [[3, 4, 5, 7], [3, 5, 7]], '8,8,9|4': [[3, 4, 5, 7], [3, 5, 7]], '8,8,9|5': [[3, 4, 5, 6, 7], [3, 4, 5, 7], [3, 5, 7]], '8,9,9|0': [[3, 4, 5, 7], [3, 5, 7]], '8,9,9|1': [[3, 4, 5, 7], [3, 5, 7]], '8,9,9|2': [[3, 4, 5, 7], [3, 5, 7]], '8,9,9|3': [[3, 4, 5, 7], [3, 5, 7]], '8,9,9|4': [[3, 4, 5, 7], [3, 5, 7]], '8,9,9|5': [[3, 4, 5, 7], [3, 5, 7]]}, 'failing_residue_pairs': [[6, 8], [6, 8, 9], [6, 9], [8, 9]], 'failing_three_residue_keys': [[[6, 8, 9], 0], [[6, 8, 9], 1], [[6, 8, 9], 2], [[6, 8, 9], 3]], 'fl_violations': 0, 'gprime_mismatches': 0, 'max_states': 590430, 'mixed_keys': 34, 'two_residue_keys': 330, 'uniformly_determined_keys': 98, 'uniformly_ndet_keys': 583}  # @@R11_CONSTANTS@@
R11_PARTITIONS = {'6,6,8|0': {'n_det': 48, 'n_ndet': 3, 'profiles': 51}, '6,6,8|1': {'n_det': 30, 'n_ndet': 3, 'profiles': 33}, '6,6,8|2': {'n_det': 16, 'n_ndet': 3, 'profiles': 19}, '6,6,8|3': {'n_det': 7, 'n_ndet': 3, 'profiles': 10}, '6,6,8|4': {'n_det': 2, 'n_ndet': 2, 'profiles': 4}, '6,6,9|0': {'n_det': 40, 'n_ndet': 14, 'profiles': 54}, '6,6,9|1': {'n_det': 22, 'n_ndet': 12, 'profiles': 34}, '6,6,9|2': {'n_det': 10, 'n_ndet': 10, 'profiles': 20}, '6,6,9|3': {'n_det': 3, 'n_ndet': 7, 'profiles': 10}, '6,8,8|0': {'n_det': 63, 'n_ndet': 3, 'profiles': 66}, '6,8,8|1': {'n_det': 42, 'n_ndet': 3, 'profiles': 45}, '6,8,8|2': {'n_det': 24, 'n_ndet': 3, 'profiles': 27}, '6,8,8|3': {'n_det': 13, 'n_ndet': 3, 'profiles': 16}, '6,8,8|4': {'n_det': 4, 'n_ndet': 3, 'profiles': 7}, '6,8,9|0': {'n_det': 95, 'n_ndet': 25, 'profiles': 120}, '6,8,9|1': {'n_det': 53, 'n_ndet': 25, 'profiles': 78}, '6,8,9|2': {'n_det': 24, 'n_ndet': 23, 'profiles': 47}, '6,8,9|3': {'n_det': 6, 'n_ndet': 19, 'profiles': 25}, '6,9,9|0': {'n_det': 64, 'n_ndet': 14, 'profiles': 78}, '6,9,9|1': {'n_det': 40, 'n_ndet': 14, 'profiles': 54}, '6,9,9|2': {'n_det': 19, 'n_ndet': 14, 'profiles': 33}, '6,9,9|3': {'n_det': 6, 'n_ndet': 14, 'profiles': 20}, '8,8,9|0': {'n_det': 92, 'n_ndet': 8, 'profiles': 100}, '8,8,9|1': {'n_det': 62, 'n_ndet': 8, 'profiles': 70}, '8,8,9|2': {'n_det': 40, 'n_ndet': 8, 'profiles': 48}, '8,8,9|3': {'n_det': 22, 'n_ndet': 8, 'profiles': 30}, '8,8,9|4': {'n_det': 10, 'n_ndet': 8, 'profiles': 18}, '8,8,9|5': {'n_det': 3, 'n_ndet': 6, 'profiles': 9}, '8,9,9|0': {'n_det': 102, 'n_ndet': 8, 'profiles': 110}, '8,9,9|1': {'n_det': 72, 'n_ndet': 8, 'profiles': 80}, '8,9,9|2': {'n_det': 46, 'n_ndet': 8, 'profiles': 54}, '8,9,9|3': {'n_det': 28, 'n_ndet': 8, 'profiles': 36}, '8,9,9|4': {'n_det': 13, 'n_ndet': 8, 'profiles': 21}, '8,9,9|5': {'n_det': 4, 'n_ndet': 8, 'profiles': 12}}
R11_WITNESSES = {'6,6,8|0': {'chain_survivors': [5], 'det_atoms': [1, 1, 2, 2, 3, 3, 0], 'det_survivors': [5], 'ndet_atoms': [1, 1, 5, 4, 0, 2, 0], 'ndet_survivors': [3, 4, 5]}, '6,6,8|1': {'chain_survivors': [5], 'det_atoms': [1, 1, 1, 1, 3, 3, 1], 'det_survivors': [5], 'ndet_atoms': [1, 1, 4, 3, 0, 2, 1], 'ndet_survivors': [3, 4, 5]}, '6,6,8|2': {'chain_survivors': [5], 'det_atoms': [1, 1, 1, 2, 2, 2, 2], 'det_survivors': [5], 'ndet_atoms': [1, 1, 3, 2, 0, 2, 2], 'ndet_survivors': [3, 4, 5]}, '6,6,8|3': {'chain_survivors': [5], 'det_atoms': [1, 1, 1, 3, 1, 1, 3], 'det_survivors': [5], 'ndet_atoms': [1, 1, 0, 1, 2, 2, 3], 'ndet_survivors': [3, 4, 5]}, '6,6,8|4': {'chain_survivors': [5], 'det_atoms': [1, 1, 1, 4, 0, 0, 4], 'det_survivors': [5], 'ndet_atoms': [1, 1, 0, 2, 1, 1, 4], 'ndet_survivors': [3, 4, 5]}, '6,6,9|0': {'chain_survivors': [5], 'det_atoms': [1, 1, 2, 3, 3, 3, 0], 'det_survivors': [5], 'ndet_atoms': [1, 1, 1, 1, 4, 4, 0], 'ndet_survivors': [3, 5]}, '6,6,9|1': {'chain_survivors': [5], 'det_atoms': [1, 1, 2, 4, 2, 2, 1], 'det_survivors': [5], 'ndet_atoms': [1, 1, 1, 2, 3, 3, 1], 'ndet_survivors': [3, 5]}, '6,6,9|2': {'chain_survivors': [5], 'det_atoms': [1, 1, 2, 5, 1, 1, 2], 'det_survivors': [5], 'ndet_atoms': [1, 1, 0, 1, 3, 3, 2], 'ndet_survivors': [3, 4, 5]}, '6,6,9|3': {'chain_survivors': [5], 'det_atoms': [1, 1, 2, 6, 0, 0, 3], 'det_survivors': [5], 'ndet_atoms': [1, 1, 0, 2, 2, 2, 3], 'ndet_survivors': [3, 4, 5]}, '6,8,8|0': {'chain_survivors': [5], 'det_atoms': [1, 1, 3, 2, 2, 4, 0], 'det_survivors': [5], 'ndet_atoms': [1, 1, 5, 6, 0, 2, 0], 'ndet_survivors': [3, 4, 5]}, '6,8,8|1': {'chain_survivors': [5], 'det_atoms': [1, 1, 2, 1, 2, 4, 1], 'det_survivors': [5], 'ndet_atoms': [1, 1, 4, 5, 0, 2, 1], 'ndet_survivors': [3, 4, 5]}, '6,8,8|2': {'chain_survivors': [5], 'det_atoms': [1, 1, 2, 2, 1, 3, 2], 'det_survivors': [5], 'ndet_atoms': [1, 1, 3, 4, 0, 2, 2], 'ndet_survivors': [3, 4, 5]}, '6,8,8|3': {'chain_survivors': [5], 'det_atoms': [1, 1, 1, 1, 1, 3, 3], 'det_survivors': [5], 'ndet_atoms': [1, 1, 2, 3, 0, 2, 3], 'ndet_survivors': [3, 4, 5]}, '6,8,8|4': {'chain_survivors': [5], 'det_atoms': [1, 1, 3, 2, 0, 0, 4], 'det_survivors': [5], 'ndet_atoms': [1, 1, 1, 2, 0, 2, 4], 'ndet_survivors': [3, 4, 5]}, '6,8,9|0': {'chain_survivors': [5], 'det_atoms': [1, 1, 2, 1, 3, 5, 0], 'det_survivors': [5], 'ndet_atoms': [1, 1, 4, 3, 1, 4, 0], 'ndet_survivors': [3, 5]}, '6,8,9|1': {'chain_survivors': [5], 'det_atoms': [1, 1, 2, 2, 2, 4, 1], 'det_survivors': [5], 'ndet_atoms': [1, 1, 3, 2, 1, 4, 1], 'ndet_survivors': [3, 5]}, '6,8,9|2': {'chain_survivors': [5], 'det_atoms': [1, 1, 2, 3, 1, 3, 2], 'det_survivors': [5], 'ndet_atoms': [1, 1, 1, 1, 2, 4, 2], 'ndet_survivors': [3, 5, 7]}, '6,8,9|3': {'chain_survivors': [5], 'det_atoms': [2, 2, 1, 4, 0, 2, 3], 'det_survivors': [5], 'ndet_atoms': [1, 1, 1, 2, 1, 3, 3], 'ndet_survivors': [3, 5, 7]}, '6,9,9|0': {'chain_survivors': [5], 'det_atoms': [1, 1, 3, 2, 2, 5, 0], 'det_survivors': [5], 'ndet_atoms': [1, 1, 4, 4, 1, 4, 0], 'ndet_survivors': [3, 5]}, '6,9,9|1': {'chain_survivors': [5], 'det_atoms': [1, 1, 2, 1, 2, 5, 1], 'det_survivors': [5], 'ndet_atoms': [1, 1, 3, 3, 1, 4, 1], 'ndet_survivors': [3, 5]}, '6,9,9|2': {'chain_survivors': [5], 'det_atoms': [1, 1, 5, 2, 1, 1, 2], 'det_survivors': [5], 'ndet_atoms': [1, 1, 2, 2, 1, 4, 2], 'ndet_survivors': [3, 5]}, '6,9,9|3': {'chain_survivors': [5], 'det_atoms': [1, 1, 5, 3, 0, 0, 3], 'det_survivors': [5], 'ndet_atoms': [1, 1, 1, 1, 1, 4, 3], 'ndet_survivors': [3, 5]}, '8,8,9|0': {'chain_survivors': [5], 'det_atoms': [1, 1, 3, 1, 4, 4, 0], 'det_survivors': [5], 'ndet_atoms': [1, 1, 6, 5, 1, 2, 0], 'ndet_survivors': [3, 5, 7]}, '8,8,9|1': {'chain_survivors': [5], 'det_atoms': [1, 1, 3, 2, 3, 3, 1], 'det_survivors': [5], 'ndet_atoms': [1, 1, 5, 4, 1, 2, 1], 'ndet_survivors': [3, 5, 7]}, '8,8,9|2': {'chain_survivors': [5], 'det_atoms': [1, 1, 2, 1, 3, 3, 2], 'det_survivors': [5], 'ndet_atoms': [1, 1, 4, 3, 1, 2, 2], 'ndet_survivors': [3, 5, 7]}, '8,8,9|3': {'chain_survivors': [5], 'det_atoms': [1, 1, 2, 2, 2, 2, 3], 'det_survivors': [5], 'ndet_atoms': [1, 1, 3, 2, 1, 2, 3], 'ndet_survivors': [3, 5, 7]}, '8,8,9|4': {'chain_survivors': [5], 'det_atoms': [1, 1, 2, 3, 1, 1, 4], 'det_survivors': [5], 'ndet_atoms': [1, 1, 1, 1, 2, 2, 4], 'ndet_survivors': [3, 5, 7]}, '8,8,9|5': {'chain_survivors': [5], 'det_atoms': [1, 1, 2, 4, 0, 0, 5], 'det_survivors': [5], 'ndet_atoms': [1, 1, 1, 2, 1, 1, 5], 'ndet_survivors': [3, 5, 7]}, '8,9,9|0': {'chain_survivors': [5], 'det_atoms': [1, 1, 4, 2, 3, 4, 0], 'det_survivors': [5], 'ndet_atoms': [1, 1, 6, 6, 1, 2, 0], 'ndet_survivors': [3, 5, 7]}, '8,9,9|1': {'chain_survivors': [5], 'det_atoms': [1, 1, 3, 1, 3, 4, 1], 'det_survivors': [5], 'ndet_atoms': [1, 1, 5, 5, 1, 2, 1], 'ndet_survivors': [3, 5, 7]}, '8,9,9|2': {'chain_survivors': [5], 'det_atoms': [1, 1, 3, 2, 2, 3, 2], 'det_survivors': [5], 'ndet_atoms': [1, 1, 4, 4, 1, 2, 2], 'ndet_survivors': [3, 5, 7]}, '8,9,9|3': {'chain_survivors': [5], 'det_atoms': [1, 1, 2, 1, 2, 3, 3], 'det_survivors': [5], 'ndet_atoms': [1, 1, 3, 3, 1, 2, 3], 'ndet_survivors': [3, 5, 7]}, '8,9,9|4': {'chain_survivors': [5], 'det_atoms': [1, 1, 3, 2, 1, 1, 4], 'det_survivors': [5], 'ndet_atoms': [1, 1, 2, 2, 1, 2, 4], 'ndet_survivors': [3, 5, 7]}, '8,9,9|5': {'chain_survivors': [5], 'det_atoms': [1, 1, 3, 3, 0, 0, 5], 'det_survivors': [5], 'ndet_atoms': [1, 1, 1, 1, 1, 2, 5], 'ndet_survivors': [3, 5, 7]}}
R11_FATE_PUB56_KEYS = [[[2, 3, 8], 0], [[2, 3, 8], 1], [[2, 8, 9], 0], [[2, 8, 9], 1], [[3, 3, 8], 0], [[3, 3, 8], 1], [[3, 8, 8], 0], [[3, 8, 8], 1], [[3, 8, 9], 0], [[3, 8, 9], 1], [[4, 4, 8], 0], [[4, 4, 8], 1], [[4, 4, 8], 2], [[4, 4, 9], 0], [[4, 4, 9], 1], [[4, 4, 9], 2], [[4, 8, 8], 0], [[4, 8, 8], 1], [[4, 8, 8], 2], [[4, 9, 9], 0], [[4, 9, 9], 1], [[4, 9, 9], 2], [[6, 6, 8], 0], [[6, 6, 8], 1], [[6, 6, 8], 2], [[6, 6, 8], 3], [[6, 6, 8], 4], [[6, 6, 9], 0], [[6, 6, 9], 1], [[6, 6, 9], 2], [[6, 6, 9], 3], [[6, 8, 8], 0], [[6, 8, 8], 1], [[6, 8, 8], 2], [[6, 8, 8], 3], [[6, 8, 8], 4], [[6, 8, 9], 0], [[6, 8, 9], 1], [[6, 8, 9], 2], [[6, 8, 9], 3], [[6, 9, 9], 0], [[6, 9, 9], 1], [[6, 9, 9], 2], [[6, 9, 9], 3], [[8, 8, 9], 0], [[8, 8, 9], 1], [[8, 8, 9], 2], [[8, 8, 9], 3], [[8, 8, 9], 4], [[8, 8, 9], 5], [[8, 9, 9], 0], [[8, 9, 9], 1], [[8, 9, 9], 2], [[8, 9, 9], 3], [[8, 9, 9], 4], [[8, 9, 9], 5]]
R11_FATE_PUB56 = {'2,3,8|0': {'chain_determined': False, 'chain_survivors': [1, 5], 'mixed': False, 'n_det': 0, 'profiles': 8, 'uniform_det': False, 'uniform_ndet': True}, '2,3,8|1': {'chain_determined': False, 'chain_survivors': [1, 5], 'mixed': False, 'n_det': 0, 'profiles': 2, 'uniform_det': False, 'uniform_ndet': True}, '2,8,9|0': {'chain_determined': False, 'chain_survivors': [1, 5], 'mixed': False, 'n_det': 0, 'profiles': 23, 'uniform_det': False, 'uniform_ndet': True}, '2,8,9|1': {'chain_determined': False, 'chain_survivors': [1, 5], 'mixed': False, 'n_det': 0, 'profiles': 7, 'uniform_det': False, 'uniform_ndet': True}, '3,3,8|0': {'chain_determined': False, 'chain_survivors': [1, 5], 'mixed': False, 'n_det': 0, 'profiles': 10, 'uniform_det': False, 'uniform_ndet': True}, '3,3,8|1': {'chain_determined': False, 'chain_survivors': [1, 5], 'mixed': False, 'n_det': 0, 'profiles': 4, 'uniform_det': False, 'uniform_ndet': True}, '3,8,8|0': {'chain_determined': False, 'chain_survivors': [1, 5], 'mixed': False, 'n_det': 0, 'profiles': 28, 'uniform_det': False, 'uniform_ndet': True}, '3,8,8|1': {'chain_determined': False, 'chain_survivors': [1, 5], 'mixed': False, 'n_det': 0, 'profiles': 13, 'uniform_det': False, 'uniform_ndet': True}, '3,8,9|0': {'chain_determined': False, 'chain_survivors': [1, 5], 'mixed': False, 'n_det': 0, 'profiles': 43, 'uniform_det': False, 'uniform_ndet': True}, '3,8,9|1': {'chain_determined': False, 'chain_survivors': [1, 5], 'mixed': False, 'n_det': 0, 'profiles': 20, 'uniform_det': False, 'uniform_ndet': True}, '4,4,8|0': {'chain_determined': False, 'chain_survivors': [3, 5], 'mixed': False, 'n_det': 0, 'profiles': 20, 'uniform_det': False, 'uniform_ndet': True}, '4,4,8|1': {'chain_determined': False, 'chain_survivors': [3, 5], 'mixed': False, 'n_det': 0, 'profiles': 10, 'uniform_det': False, 'uniform_ndet': True}, '4,4,8|2': {'chain_determined': False, 'chain_survivors': [3, 5], 'mixed': False, 'n_det': 0, 'profiles': 4, 'uniform_det': False, 'uniform_ndet': True}, '4,4,9|0': {'chain_determined': False, 'chain_survivors': [3, 5], 'mixed': False, 'n_det': 0, 'profiles': 20, 'uniform_det': False, 'uniform_ndet': True}, '4,4,9|1': {'chain_determined': False, 'chain_survivors': [3, 5], 'mixed': False, 'n_det': 0, 'profiles': 10, 'uniform_det': False, 'uniform_ndet': True}, '4,4,9|2': {'chain_determined': False, 'chain_survivors': [3, 5], 'mixed': False, 'n_det': 0, 'profiles': 4, 'uniform_det': False, 'uniform_ndet': True}, '4,8,8|0': {'chain_determined': False, 'chain_survivors': [3, 5], 'mixed': False, 'n_det': 0, 'profiles': 39, 'uniform_det': False, 'uniform_ndet': True}, '4,8,8|1': {'chain_determined': False, 'chain_survivors': [3, 5], 'mixed': False, 'n_det': 0, 'profiles': 24, 'uniform_det': False, 'uniform_ndet': True}, '4,8,8|2': {'chain_determined': False, 'chain_survivors': [3, 5], 'mixed': False, 'n_det': 0, 'profiles': 11, 'uniform_det': False, 'uniform_ndet': True}, '4,9,9|0': {'chain_determined': False, 'chain_survivors': [3, 5], 'mixed': False, 'n_det': 0, 'profiles': 45, 'uniform_det': False, 'uniform_ndet': True}, '4,9,9|1': {'chain_determined': False, 'chain_survivors': [3, 5], 'mixed': False, 'n_det': 0, 'profiles': 28, 'uniform_det': False, 'uniform_ndet': True}, '4,9,9|2': {'chain_determined': False, 'chain_survivors': [3, 5], 'mixed': False, 'n_det': 0, 'profiles': 13, 'uniform_det': False, 'uniform_ndet': True}, '6,6,8|0': {'chain_determined': True, 'chain_survivors': [5], 'mixed': True, 'n_det': 48, 'profiles': 51, 'uniform_det': False, 'uniform_ndet': False}, '6,6,8|1': {'chain_determined': True, 'chain_survivors': [5], 'mixed': True, 'n_det': 30, 'profiles': 33, 'uniform_det': False, 'uniform_ndet': False}, '6,6,8|2': {'chain_determined': True, 'chain_survivors': [5], 'mixed': True, 'n_det': 16, 'profiles': 19, 'uniform_det': False, 'uniform_ndet': False}, '6,6,8|3': {'chain_determined': True, 'chain_survivors': [5], 'mixed': True, 'n_det': 7, 'profiles': 10, 'uniform_det': False, 'uniform_ndet': False}, '6,6,8|4': {'chain_determined': True, 'chain_survivors': [5], 'mixed': True, 'n_det': 2, 'profiles': 4, 'uniform_det': False, 'uniform_ndet': False}, '6,6,9|0': {'chain_determined': True, 'chain_survivors': [5], 'mixed': True, 'n_det': 40, 'profiles': 54, 'uniform_det': False, 'uniform_ndet': False}, '6,6,9|1': {'chain_determined': True, 'chain_survivors': [5], 'mixed': True, 'n_det': 22, 'profiles': 34, 'uniform_det': False, 'uniform_ndet': False}, '6,6,9|2': {'chain_determined': True, 'chain_survivors': [5], 'mixed': True, 'n_det': 10, 'profiles': 20, 'uniform_det': False, 'uniform_ndet': False}, '6,6,9|3': {'chain_determined': True, 'chain_survivors': [5], 'mixed': True, 'n_det': 3, 'profiles': 10, 'uniform_det': False, 'uniform_ndet': False}, '6,8,8|0': {'chain_determined': True, 'chain_survivors': [5], 'mixed': True, 'n_det': 63, 'profiles': 66, 'uniform_det': False, 'uniform_ndet': False}, '6,8,8|1': {'chain_determined': True, 'chain_survivors': [5], 'mixed': True, 'n_det': 42, 'profiles': 45, 'uniform_det': False, 'uniform_ndet': False}, '6,8,8|2': {'chain_determined': True, 'chain_survivors': [5], 'mixed': True, 'n_det': 24, 'profiles': 27, 'uniform_det': False, 'uniform_ndet': False}, '6,8,8|3': {'chain_determined': True, 'chain_survivors': [5], 'mixed': True, 'n_det': 13, 'profiles': 16, 'uniform_det': False, 'uniform_ndet': False}, '6,8,8|4': {'chain_determined': True, 'chain_survivors': [5], 'mixed': True, 'n_det': 4, 'profiles': 7, 'uniform_det': False, 'uniform_ndet': False}, '6,8,9|0': {'chain_determined': True, 'chain_survivors': [5], 'mixed': True, 'n_det': 95, 'profiles': 120, 'uniform_det': False, 'uniform_ndet': False}, '6,8,9|1': {'chain_determined': True, 'chain_survivors': [5], 'mixed': True, 'n_det': 53, 'profiles': 78, 'uniform_det': False, 'uniform_ndet': False}, '6,8,9|2': {'chain_determined': True, 'chain_survivors': [5], 'mixed': True, 'n_det': 24, 'profiles': 47, 'uniform_det': False, 'uniform_ndet': False}, '6,8,9|3': {'chain_determined': True, 'chain_survivors': [5], 'mixed': True, 'n_det': 6, 'profiles': 25, 'uniform_det': False, 'uniform_ndet': False}, '6,9,9|0': {'chain_determined': True, 'chain_survivors': [5], 'mixed': True, 'n_det': 64, 'profiles': 78, 'uniform_det': False, 'uniform_ndet': False}, '6,9,9|1': {'chain_determined': True, 'chain_survivors': [5], 'mixed': True, 'n_det': 40, 'profiles': 54, 'uniform_det': False, 'uniform_ndet': False}, '6,9,9|2': {'chain_determined': True, 'chain_survivors': [5], 'mixed': True, 'n_det': 19, 'profiles': 33, 'uniform_det': False, 'uniform_ndet': False}, '6,9,9|3': {'chain_determined': True, 'chain_survivors': [5], 'mixed': True, 'n_det': 6, 'profiles': 20, 'uniform_det': False, 'uniform_ndet': False}, '8,8,9|0': {'chain_determined': True, 'chain_survivors': [5], 'mixed': True, 'n_det': 92, 'profiles': 100, 'uniform_det': False, 'uniform_ndet': False}, '8,8,9|1': {'chain_determined': True, 'chain_survivors': [5], 'mixed': True, 'n_det': 62, 'profiles': 70, 'uniform_det': False, 'uniform_ndet': False}, '8,8,9|2': {'chain_determined': True, 'chain_survivors': [5], 'mixed': True, 'n_det': 40, 'profiles': 48, 'uniform_det': False, 'uniform_ndet': False}, '8,8,9|3': {'chain_determined': True, 'chain_survivors': [5], 'mixed': True, 'n_det': 22, 'profiles': 30, 'uniform_det': False, 'uniform_ndet': False}, '8,8,9|4': {'chain_determined': True, 'chain_survivors': [5], 'mixed': True, 'n_det': 10, 'profiles': 18, 'uniform_det': False, 'uniform_ndet': False}, '8,8,9|5': {'chain_determined': True, 'chain_survivors': [5], 'mixed': True, 'n_det': 3, 'profiles': 9, 'uniform_det': False, 'uniform_ndet': False}, '8,9,9|0': {'chain_determined': True, 'chain_survivors': [5], 'mixed': True, 'n_det': 102, 'profiles': 110, 'uniform_det': False, 'uniform_ndet': False}, '8,9,9|1': {'chain_determined': True, 'chain_survivors': [5], 'mixed': True, 'n_det': 72, 'profiles': 80, 'uniform_det': False, 'uniform_ndet': False}, '8,9,9|2': {'chain_determined': True, 'chain_survivors': [5], 'mixed': True, 'n_det': 46, 'profiles': 54, 'uniform_det': False, 'uniform_ndet': False}, '8,9,9|3': {'chain_determined': True, 'chain_survivors': [5], 'mixed': True, 'n_det': 28, 'profiles': 36, 'uniform_det': False, 'uniform_ndet': False}, '8,9,9|4': {'chain_determined': True, 'chain_survivors': [5], 'mixed': True, 'n_det': 13, 'profiles': 21, 'uniform_det': False, 'uniform_ndet': False}, '8,9,9|5': {'chain_determined': True, 'chain_survivors': [5], 'mixed': True, 'n_det': 4, 'profiles': 12, 'uniform_det': False, 'uniform_ndet': False}}


# ---------------------------------------------------------------------------
# constants (machine-extracted from the committed sweep records; the
# analysis below re-derives every pinned field from the records and
# the live checks recompute witness verdicts with the verbatim engine)
# ---------------------------------------------------------------------------

R = 11
CAP = 10
N_PROFILES = 15863
N_KEYS = 715
DELTA0_EXPECTED = 728  # cap<=10 uniform-profile count (K0866/K0869 anchor)
SAMPLE_STRIDE = 32

# Burnside / enumeration expectation (K0862..K0869, r-independent).
EXPECTED_BURNSIDE = {
    10: {"fix_id": 84494, "fix_trans": 3478, "fix_cyc": 125, "orbits": 15863},
}

# r=11 arithmetic residue census over the same 715 cap<=10 keys
# (residue classes by Lemma FL, no outcome data; NEW r=11 column,
# self-derived - K0872 published r=3..9 and K0895 added r=10; the
# split is identical to r=10 because r=11 exceeds every branch size
# (<= 10), so there is no modular wraparound and the single-residue
# keys are exactly the 55 equal triples).
R11_RESIDUE_CENSUS = {"single_residue_keys": 55,
                      "two_residue_keys": 330,
                      "three_residue_keys": 330}

# (r=11 constants injected by transform_to_r11.py)

# STASIS anchors (K0895 published r=10 values, machine-verified against
# the committed r=10 packed records in check C11): the r=10 failing key
# set and per-key partitions, identical to the r=11 values above. The
# K0893 r=9 packed records are also read for the three-column det-flag
# observation (r=9, r=10, r=11).
K0895_FAILING_KEYS = [[[6, 6, 8], 0], [[6, 6, 8], 1], [[6, 6, 8], 2], [[6, 6, 8], 3], [[6, 6, 8], 4], [[6, 6, 9], 0], [[6, 6, 9], 1], [[6, 6, 9], 2], [[6, 6, 9], 3], [[6, 8, 8], 0], [[6, 8, 8], 1], [[6, 8, 8], 2], [[6, 8, 8], 3], [[6, 8, 8], 4], [[6, 8, 9], 0], [[6, 8, 9], 1], [[6, 8, 9], 2], [[6, 8, 9], 3], [[6, 9, 9], 0], [[6, 9, 9], 1], [[6, 9, 9], 2], [[6, 9, 9], 3], [[8, 8, 9], 0], [[8, 8, 9], 1], [[8, 8, 9], 2], [[8, 8, 9], 3], [[8, 8, 9], 4], [[8, 8, 9], 5], [[8, 9, 9], 0], [[8, 9, 9], 1], [[8, 9, 9], 2], [[8, 9, 9], 3], [[8, 9, 9], 4], [[8, 9, 9], 5]]
K0895_PARTITIONS = {'6,6,8|0': {'n_det': 48, 'n_ndet': 3, 'profiles': 51}, '6,6,8|1': {'n_det': 30, 'n_ndet': 3, 'profiles': 33}, '6,6,8|2': {'n_det': 16, 'n_ndet': 3, 'profiles': 19}, '6,6,8|3': {'n_det': 7, 'n_ndet': 3, 'profiles': 10}, '6,6,8|4': {'n_det': 2, 'n_ndet': 2, 'profiles': 4}, '6,6,9|0': {'n_det': 40, 'n_ndet': 14, 'profiles': 54}, '6,6,9|1': {'n_det': 22, 'n_ndet': 12, 'profiles': 34}, '6,6,9|2': {'n_det': 10, 'n_ndet': 10, 'profiles': 20}, '6,6,9|3': {'n_det': 3, 'n_ndet': 7, 'profiles': 10}, '6,8,8|0': {'n_det': 63, 'n_ndet': 3, 'profiles': 66}, '6,8,8|1': {'n_det': 42, 'n_ndet': 3, 'profiles': 45}, '6,8,8|2': {'n_det': 24, 'n_ndet': 3, 'profiles': 27}, '6,8,8|3': {'n_det': 13, 'n_ndet': 3, 'profiles': 16}, '6,8,8|4': {'n_det': 4, 'n_ndet': 3, 'profiles': 7}, '6,8,9|0': {'n_det': 95, 'n_ndet': 25, 'profiles': 120}, '6,8,9|1': {'n_det': 53, 'n_ndet': 25, 'profiles': 78}, '6,8,9|2': {'n_det': 24, 'n_ndet': 23, 'profiles': 47}, '6,8,9|3': {'n_det': 6, 'n_ndet': 19, 'profiles': 25}, '6,9,9|0': {'n_det': 64, 'n_ndet': 14, 'profiles': 78}, '6,9,9|1': {'n_det': 40, 'n_ndet': 14, 'profiles': 54}, '6,9,9|2': {'n_det': 19, 'n_ndet': 14, 'profiles': 33}, '6,9,9|3': {'n_det': 6, 'n_ndet': 14, 'profiles': 20}, '8,8,9|0': {'n_det': 92, 'n_ndet': 8, 'profiles': 100}, '8,8,9|1': {'n_det': 62, 'n_ndet': 8, 'profiles': 70}, '8,8,9|2': {'n_det': 40, 'n_ndet': 8, 'profiles': 48}, '8,8,9|3': {'n_det': 22, 'n_ndet': 8, 'profiles': 30}, '8,8,9|4': {'n_det': 10, 'n_ndet': 8, 'profiles': 18}, '8,8,9|5': {'n_det': 3, 'n_ndet': 6, 'profiles': 9}, '8,9,9|0': {'n_det': 102, 'n_ndet': 8, 'profiles': 110}, '8,9,9|1': {'n_det': 72, 'n_ndet': 8, 'profiles': 80}, '8,9,9|2': {'n_det': 46, 'n_ndet': 8, 'profiles': 54}, '8,9,9|3': {'n_det': 28, 'n_ndet': 8, 'profiles': 36}, '8,9,9|4': {'n_det': 13, 'n_ndet': 8, 'profiles': 21}, '8,9,9|5': {'n_det': 4, 'n_ndet': 8, 'profiles': 12}}
K0895_PACKED_R10 = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..",
    "remo-k-branch-cap10-r10-boundary-20261117", "output",
    "js_cap10_r10.packed.jsonl")
K0893_PACKED_R9 = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..",
    "remo-k-branch-cap10-r9-boundary-20261117", "output",
    "js_cap10_r9.packed.jsonl")
STASIS_DET_FLAG_DIFFERENCES = 0
STASIS_R9_DET_FLAG_DIFFERENCES = 0
STASIS_SURVIVOR_MASK_DIFFERENCES = 0
STASIS_FL_MASK_DIFFERENCES = 7328

AUDIT_NAME = "remo_k_branch_cap10_r11_boundary_audit.json"


def load_jsonl():
    """Committed sweep records (packed publication format preferred).

    Full format first (js_cap10_r9.jsonl[.gz]), then packed
    (js_cap10_r9.packed.jsonl). Packed records store [i, sv_mask,
    fl_mask, states]; atoms are a pure function of i via the canonical
    cap<=10 enumeration below, re-derived by the caller."""
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "output", "js_cap10_r11.jsonl")
    if os.path.exists(base + ".gz"):
        with gzip.open(base + ".gz", "rt", encoding="utf-8") as f:
            lines = f.read().splitlines()
        return [json.loads(line) for line in lines if line.strip()], "full"
    if os.path.exists(base):
        with open(base, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
        return [json.loads(line) for line in lines if line.strip()], "full"
    packed_path = base[:-6] + ".packed.jsonl" if base.endswith(".jsonl") \
        else base + ".packed.jsonl"
    packed_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "output", "js_cap10_r11.packed.jsonl")
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
                    "atoms": None,  # re-derived by the caller
                    "determined": len(survivors) == 1,
                    "survivors": survivors,
                    "first_losers": first_losers,
                    "states": states,
                })
        return out, "packed"
    raise FileNotFoundError(base + "[.gz] / " + packed_path)


def analyze_r11(profiles, pidx, records):
    byk = {}
    for i, atoms in enumerate(profiles):
        byk.setdefault(key_of(atoms), []).append(records[i])
    out = {}
    out["keys"] = len(byk)
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
        part[kstr(k)] = {"n_det": len(det), "n_ndet": len(ndet),
                         "profiles": len(rs)}
        det_surv |= {tuple(rec["survivors"]) for rec in det}
        sets_k = sorted(list(t) for t in
                        {tuple(sorted(rec["survivors"])) for rec in ndet})
        ndet_by_key[kstr(k)] = sets_k
        ndet_sets |= {tuple(s) for s in sets_k}
    out["failing_partitions"] = part
    out["failing_det_survivors"] = sorted(list(t) for t in det_surv)
    out["failing_ndet_sets"] = sorted(list(t) for t in ndet_sets)
    out["failing_ndet_sets_by_key"] = ndet_by_key
    uni_det = 0
    uni_ndet = 0
    for k, rs in byk.items():
        flags = {rec["determined"] for rec in rs}
        if len(flags) > 1:
            continue
        if flags.pop():
            uni_det += 1
        else:
            uni_ndet += 1
    out["uniformly_determined_keys"] = uni_det
    out["uniformly_ndet_keys"] = uni_ndet
    out["mixed_keys"] = len(failing)
    # G' survivor level (chain agreement)
    gprime_mism = 0
    for k, rs in byk.items():
        flags = {rec["determined"] for rec in rs}
        if flags == {True}:
            chain = records[pidx[chain_profile(k[0], k[1], 3)]]
            if any(rec["survivors"] != chain["survivors"] for rec in rs):
                gprime_mism += 1
    out["gprime_survivor_mismatches"] = gprime_mism
    # FL anchor
    fl_viol = 0
    for i, atoms in enumerate(profiles):
        want = sorted({c % R for c in profile_sizes(atoms, 3)})
        if records[i]["first_losers"] != want:
            fl_viol += 1
    out["first_loser_violations"] = fl_viol
    # Delta=0 anchor (Theorem D at r=11 via the verbatim recursion)
    d0 = 0
    d0_mism = 0
    for i, atoms in enumerate(profiles):
        sizes = profile_sizes(atoms, 3)
        if len(set(sizes)) != 1:
            continue
        d0 += 1
        _, surv = theorem_d(sizes[0], R)
        rec = records[i]
        if not (rec["determined"] and rec["survivors"] == [surv]):
            d0_mism += 1
    out["delta0_profiles"] = d0
    out["delta0_mismatches"] = d0_mism
    # residue lens
    out["two_residue_keys"] = sum(
        1 for k in byk if len({c % R for c in k[0]}) == 2)
    out["failing_residue_pairs"] = sorted(
        [list(t) for t in
         {tuple(sorted({c % R for c in k[0]})) for k in failing}])
    out["failing_keys_two_residue"] = all(
        len({c % R for c in k[0]}) == 2 for k in failing)
    out["failing_three_residue_keys"] = sorted(
        [list(k[0]), k[1]] for k in failing
        if len({c % R for c in k[0]}) == 3)
    out["residue_class_census"] = {}
    for k in byk:
        n = len({c % R for c in k[0]})
        out["residue_class_census"][str(n)] = \
            out["residue_class_census"].get(str(n), 0) + 1
    # FATE rows: the 56 published r=3..10 failing keys at r=11 (data)
    fate = {}
    for sp, g in R11_FATE_PUB56_KEYS:
        kk = (tuple(sp), g)
        rs = byk.get(kk)
        if rs is None:
            fate[kstr(kk)] = {"key_absent": True}
            continue
        dets = {rec["determined"] for rec in rs}
        chain = records[pidx[chain_profile(kk[0], kk[1], 3)]]
        fate[kstr(kk)] = {
            "uniform_det": dets == {True},
            "uniform_ndet": dets == {False},
            "mixed": len(dets) > 1,
            "n_det": sum(1 for rec in rs if rec["determined"]),
            "profiles": len(rs),
            "chain_determined": chain["determined"],
            "chain_survivors": chain["survivors"],
        }
    out["fate_pub56"] = fate
    out["max_states"] = max(rec["states"] for rec in records.values())
    return out, byk


def assemble_audit():
    checks = []

    def record(name, ok, data):
        checks.append({"name": name, "ok": bool(ok), "data": data})

    audit = {"meta": {
        "item": "K0897",
        "title": "3-branch REMO determinacy r=11 boundary (branch sizes "
            "<= 10): the third r >= 9 column; identical mixed-key "
            "boundary as r=9 and r=10 (STASIS over three columns, "
            "survivor-mask fixpoint vs r=10)",
        "date": "2026-11-17",
        "engine_provenance": "verbatim region game / enumeration / "
            "Burnside / Theorem D from the K0862 verifier via K0875, "
            "K0876, K0881, K0893 and K0895; full-domain records "
            "produced by the committed JavaScript mask engine "
            "(mask_engine_fast_r11.js: byte-identical copy of the "
            "K0893 committed fixed engine with the pack encoding "
            "shift generalized to r); Python mask twin "
            "cross-validated live in every run",
        "r_swept": [11],
    }}

    # ---- C1: enumeration / Burnside (r-independent anchor)
    fi, ft, fc, orbits = burnside_fix_counts(CAP)
    profiles = direct_constrained(CAP)
    exp = EXPECTED_BURNSIDE[CAP]
    audit["burnside"] = {str(CAP): {
        "fix_id": fi, "fix_trans": ft, "fix_cyc": fc, "orbits": orbits}}
    record(
        "cap=10: Burnside orbit count == direct canonical enumeration "
        "(%d profiles, fix counts %d/%d/%d)" % (exp["orbits"], fi, ft, fc),
        orbits == len(profiles) == exp["orbits"]
        and (fi, ft, fc) == (exp["fix_id"], exp["fix_trans"], exp["fix_cyc"]),
        {"fix_id": fi, "fix_trans": ft, "fix_cyc": fc,
         "orbits": orbits, "enum_count": len(profiles)},
    )
    pidx = {atoms: i for i, atoms in enumerate(profiles)}

    # ---- C2: JSONL integrity
    recs, fmt = load_jsonl()
    if fmt == "packed":
        for rec in recs:
            rec["atoms"] = list(profiles[rec["i"]])
    ok = (
        len(recs) == N_PROFILES
        and [rec["i"] for rec in recs] == list(range(N_PROFILES))
        and all(not rec.get("skipped") for rec in recs)
        and all(tuple(rec["atoms"]) == profiles[rec["i"]] for rec in recs)
        and all(
            rec["determined"] == (len(rec["survivors"]) == 1)
            and sorted(set(rec["survivors"])) == rec["survivors"]
            and sorted(set(rec["first_losers"])) == rec["first_losers"]
            and all(0 <= p < R
                   for p in rec["survivors"] + rec["first_losers"])
            and rec["states"] > 0
            for rec in recs)
    )
    blob = "\n".join(json.dumps(rec, sort_keys=True) for rec in recs)
    digest = hashlib.sha256(blob.encode()).hexdigest()
    packed_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "output", "js_cap10_r11.packed.jsonl")
    packed_digest = None
    if os.path.exists(packed_path):
        with open(packed_path, "rb") as f:
            packed_digest = hashlib.sha256(f.read()).hexdigest()
    audit["sweep_inputs"] = {"r11": {
        "records": len(recs),
        "format": fmt,
        "skipped": sum(1 for rec in recs if rec.get("skipped")),
        "sha256_uncompressed": digest,
        "sha256_packed": packed_digest,
        "max_states": max(rec["states"] for rec in recs),
    }}
    record(
        "r=11 committed sweep records: 15863 records, index-complete, "
        "atoms == enumeration, no budget skips",
        ok,
        {"records": len(recs), "sha256": digest, "format": fmt,
         "sha256_packed": packed_digest},
    )
    records = {rec["i"]: rec for rec in recs}

    # ---- C3: analysis census
    analysis, byk = analyze_r11(profiles, pidx, records)
    a = analysis
    audit["sweep"] = a
    record(
        "r=11 key census: %d keys, %d uniformly determined, %d uniformly "
        "non-determined, %d mixed" % (
            a["keys"], a["uniformly_determined_keys"],
            a["uniformly_ndet_keys"], a["mixed_keys"]),
        a["keys"] == N_KEYS
        and a["uniformly_determined_keys"] == R11_SWEEP["uniformly_determined_keys"]
        and a["uniformly_ndet_keys"] == R11_SWEEP["uniformly_ndet_keys"]
        and a["mixed_keys"] == R11_SWEEP["mixed_keys"]
        and a["uniformly_determined_keys"] + a["uniformly_ndet_keys"]
        + a["mixed_keys"] == N_KEYS,
        {"uniformly_determined_keys": a["uniformly_determined_keys"],
         "uniformly_ndet_keys": a["uniformly_ndet_keys"],
         "mixed_keys": a["mixed_keys"]},
    )

    # ---- C4: Theorem I9 (failing keys + structure == pinned constants)
    ok = (
        a["failing_keys"] == sorted(R11_SWEEP["failing_keys"])
        and a["first_loser_violations"] == 0
        and a["delta0_profiles"] == DELTA0_EXPECTED
        and a["delta0_mismatches"] == 0
        and a["failing_det_survivors"] == R11_SWEEP["failing_det_survivors"]
        and a["failing_ndet_sets"] == R11_SWEEP["failing_ndet_sets"]
        and a["failing_keys_two_residue"]
            == R11_SWEEP["failing_keys_two_residue"]
        and a["failing_three_residue_keys"]
            == R11_SWEEP["failing_three_residue_keys"]
        and a["failing_residue_pairs"] == R11_SWEEP["failing_residue_pairs"]
        and a["max_states"] == R11_SWEEP["max_states"]
    )
    record(
        "Theorem I11 (cap<=10, r=11): non-collapse keys are exactly the "
        "%d pinned keys %s - IDENTICAL to the r=9 AND r=10 boundary "
        "sets (K0893/K0895), no new family and no collapse for the "
        "third consecutive column; FL violations 0; Delta=0 %d "
        "profiles all Theorem D at r=11 (verbatim recursion); "
        "det-side survivors %s; ndet possible-survivor sets within "
        "%s; residue pairs %s (the three-residue mixed family "
        "(6,8,9) x gamma=0..3 persists at r=11); max_states %d" % (
            len(R11_SWEEP["failing_keys"]),
            R11_SWEEP["failing_keys_families"],
            DELTA0_EXPECTED,
            R11_SWEEP["failing_det_survivors"],
            R11_SWEEP["failing_ndet_sets"],
            R11_SWEEP["failing_residue_pairs"],
            R11_SWEEP["max_states"]),
        ok,
        {"failing": len(a["failing_keys"]),
         "fl_violations": a["first_loser_violations"],
         "delta0_mismatches": a["delta0_mismatches"]},
    )

    # ---- C5: per-key partitions == pinned
    part_ok = True
    for kk, v in R11_PARTITIONS.items():
        got = a["failing_partitions"].get(kk)
        if got is None or got["n_det"] != v["n_det"] \
                or got["n_ndet"] != v["n_ndet"] \
                or got["profiles"] != v["profiles"]:
            part_ok = False
    record(
        "r=11 failing-key partition counts match the pinned table "
        "(%d keys)" % len(R11_PARTITIONS),
        part_ok and len(a["failing_partitions"]) == len(R11_PARTITIONS),
        {"keys": len(R11_PARTITIONS)},
    )

    # ---- C6: witnesses valid inside the committed records
    wit_ok = True
    for kk, w in R11_WITNESSES.items():
        for tag in ("det", "ndet"):
            atoms = tuple(w[tag + "_atoms"])
            idx = pidx.get(atoms)
            if idx is None:
                wit_ok = False
                continue
            rec = records[idx]
            want_det = tag == "det"
            if not (rec["determined"] == want_det
                    and rec["survivors"] == w[tag + "_survivors"]):
                wit_ok = False
        sp, g = kk.split("|")
        sizes = tuple(int(x) for x in sp.split(","))
        crec = records[pidx[chain_profile(sizes, int(g), 3)]]
        if not (crec["determined"]
                and crec["survivors"] == w["chain_survivors"]):
            wit_ok = False
    record(
        "r=11 failing-key witnesses (det/ndet atoms + chain survivors) "
        "are valid inside the committed records (%d keys)" % len(R11_WITNESSES),
        wit_ok,
        {"witness_keys": len(R11_WITNESSES)},
    )

    # ---- C7: r=11 residue arithmetic census (new column; K0872
    # published r=3..9 and K0895 added r=10; the split is identical
    # to r=10 because r=11 exceeds every branch size (<= 10): no
    # modular wraparound, single-residue keys are exactly the equal
    # triples)
    pref = a["residue_class_census"]
    sing_equal = sorted(
        [list(k[0]), k[1]] for k in byk
        if len({c % R for c in k[0]}) == 1 and k[0][0] == k[0][1] == k[0][2])
    sing_mixed = sorted(
        [list(k[0]), k[1]] for k in byk
        if len({c % R for c in k[0]}) == 1
        and not (k[0][0] == k[0][1] == k[0][2]))
    pref_ok = (
        pref == {"1": R11_RESIDUE_CENSUS["single_residue_keys"],
                 "2": R11_RESIDUE_CENSUS["two_residue_keys"],
                 "3": R11_RESIDUE_CENSUS["three_residue_keys"]}
        and len(sing_equal) == 55
        and sing_mixed == []
        and a["two_residue_keys"] == R11_RESIDUE_CENSUS["two_residue_keys"]
    )
    record(
        "r=11 residue arithmetic census (new column, arithmetic only): "
        "715 keys split into 55/330/330 single/two/three-residue keys, "
        "IDENTICAL to the r=10 split; since r=11 exceeds every branch "
        "size (<= 10) there is no modular wraparound, so the 55 "
        "single-residue keys are exactly the equal triples; mixed keys "
        "are NOT all two-residue at r=11 either: family (6,8,9) x "
        "gamma=0..3 stays three-residue and mixed (K0893/K0895 "
        "counterexample persists)",
        pref_ok,
        {"residue_class_census": pref,
         "singleton_mixed": sing_mixed},
    )

    # ---- C8: Theorem G' survivor level at r=11
    record(
        "r=11 Theorem G' survivor level: every uniformly determined key's "
        "survivor equals the chain survivor (%d keys, %d mismatches)" % (
            a["uniformly_determined_keys"],
            a["gprime_survivor_mismatches"]),
        a["gprime_survivor_mismatches"] == 0,
        {"uniformly_determined_keys": a["uniformly_determined_keys"],
         "mismatches": a["gprime_survivor_mismatches"]},
    )

    # ---- C9: FATE rows (56 published r=3..10 failing keys at r=11)
    fate_ok = True
    for kk, v in R11_FATE_PUB56.items():
        got = a["fate_pub56"].get(kk)
        if got != v:
            fate_ok = False
    n_ndet_fate = sum(1 for v in R11_FATE_PUB56.values()
                      if v.get("uniform_ndet"))
    n_mixed_fate = sum(1 for v in R11_FATE_PUB56.values()
                       if v.get("mixed"))
    record(
        "FATE rows: the 56 published r=3..10 failing keys' r=11 fates "
        "match the pinned data (%d uniformly non-determined, %d STILL "
        "MIXED at r=11: every r=9/r=10 mixed key - all 10 of the 6/8 "
        "family, all 12 of the 8/9 family, all 12 of the 6/9 family - "
        "remains mixed for the THIRD consecutive column; no collapse, "
        "no revival, no uniform determination; the 22 collapsed keys "
        "keep the same chain verdicts and chain survivor labels as "
        "at r=10): recorded as DATA (finite observation)"
        % (n_ndet_fate, n_mixed_fate),
        fate_ok and len(a["fate_pub56"]) == 56,
        {"keys": 56, "uniformly_ndet_at_r11": n_ndet_fate,
         "still_mixed_at_r11": n_mixed_fate},
    )

    # ---- C10: Theorem D table regression (r=2..8, 84 entries)
    entries, mism = theorem_d_table()
    record(
        "Theorem D recursion == K0859 published (C,r) table "
        "(84 entries, r=2..8; the r=11 column used above is computed by "
        "the same verbatim recursion)",
        mism == 0 and entries == 84,
        {"entries": entries, "mismatches": mism},
    )

    # ---- C11: STASIS (committed r=10 records vs committed r=11
    # records; committed r=9 records for the three-column observation)
    r10_det = {}
    r10_sv = {}
    r10_fl = {}
    with open(K0895_PACKED_R10, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            i, sv, fl, st = json.loads(line)
            r10_det[i] = bin(sv).count("1") == 1
            r10_sv[i] = sv
            r10_fl[i] = fl
    stasis_diff = sum(1 for i in range(N_PROFILES)
                      if r10_det.get(i) != records[i]["determined"])
    sv_diff = sum(1 for i in range(N_PROFILES)
                  if r10_sv.get(i) != sum(1 << p
                                          for p in records[i]["survivors"]))
    fl_diff = sum(1 for i in range(N_PROFILES)
                  if r10_fl.get(i) != sum(1 << p
                                          for p in records[i]["first_losers"]))
    r9_det = {}
    with open(K0893_PACKED_R9, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            i, sv, fl, st = json.loads(line)
            r9_det[i] = bin(sv).count("1") == 1
    stasis_r9_diff = sum(1 for i in range(N_PROFILES)
                         if r9_det.get(i) != records[i]["determined"])
    part_same = all(
        a["failing_partitions"].get(kk) == v
        for kk, v in K0895_PARTITIONS.items())
    stasis_ok = (
        len(r10_det) == N_PROFILES
        and len(r9_det) == N_PROFILES
        and stasis_diff == STASIS_DET_FLAG_DIFFERENCES == 0
        and stasis_r9_diff == STASIS_R9_DET_FLAG_DIFFERENCES == 0
        and sv_diff == STASIS_SURVIVOR_MASK_DIFFERENCES == 0
        and fl_diff == STASIS_FL_MASK_DIFFERENCES
        and part_same
        and sorted(R11_SWEEP["failing_keys"]) == sorted(K0895_FAILING_KEYS)
    )
    record(
        "STASIS: the committed K0895 r=10 records and the committed "
        "r=11 records agree on the determined flag of EVERY ONE of "
        "the %d profiles (0 differences) AND on the full survivor "
        "mask of every profile (%d survivor-mask differences: a "
        "full-column label fixpoint, strictly stronger than the "
        "r=9 -> r=10 det-flag-only fixpoint); the committed K0893 "
        "r=9 records also agree on every determined flag: THREE "
        "consecutive columns (r=9,10,11) with an identical "
        "determinacy classification of the whole cap<=10 domain; "
        "the 34-key failing set, the per-key partition table, "
        "det-side survivor and ndet possible-survivor sets are "
        "field-identical to the K0895 published values (%d "
        "first-loser masks differ between r=10 and r=11; finite "
        "observation)" % (
            N_PROFILES, sv_diff, fl_diff),
        stasis_ok,
        {"profiles": N_PROFILES,
         "det_flag_differences_vs_r10": stasis_diff,
         "det_flag_differences_vs_r9": stasis_r9_diff,
         "survivor_mask_differences": sv_diff,
         "first_loser_mask_differences": fl_diff,
         "partitions_identical": part_same},
    )

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
    profiles = direct_constrained(CAP)
    pidx = {atoms: i for i, atoms in enumerate(profiles)}
    recs = {rec["i"]: rec for rec in load_jsonl()[0]}

    # L1: full cap<=7 domain, verbatim == mask twin == committed JS
    profs7 = direct_constrained(7)
    mism = 0
    n = 0
    for atoms in profs7:
        idx10 = pidx[atoms]
        v1, s1 = region_verdict(atoms, 3, R, budget=20_000_000)
        v2, s2 = mask_verdict(atoms, 3, R, budget=20_000_000)
        j = recs[idx10]
        n += 1
        if verdict_triple(v1) != verdict_triple(v2):
            mism += 1
        if verdict_triple(v2) != (j["determined"], j["survivors"],
                                  j["first_losers"]):
            mism += 1
        if s1 != s2 or s2 != j["states"]:
            mism += 1
    if mism != 0 or n != 2048:
        sys.stderr.write("LIVE FAIL: cap<=7 triple check %d mismatches / %d\n"
                         % (mism, n))
        sys.exit(1)
    print("LIVE OK: cap<=7 full domain: verbatim == mask twin == committed "
          "JS records (verdicts and state counts) on %d verdicts (r=11)" % n)

    # L2: stratified cap<=10 sample, mask twin == committed JS records
    mism = 0
    n = 0
    for i in range(0, len(profiles), SAMPLE_STRIDE):
        atoms = profiles[i]
        v2, _ = mask_verdict(atoms, 3, R, budget=50_000_000)
        j = recs[i]
        n += 1
        if verdict_triple(v2) != (j["determined"], j["survivors"],
                                   j["first_losers"]):
            mism += 1
    if mism != 0:
        sys.stderr.write("LIVE FAIL: stratified sample %d mismatches / %d\n"
                         % (mism, n))
        sys.exit(1)
    print("LIVE OK: stratified cap<=10 sample (stride %d): mask twin == "
          "committed JS records on %d verdicts" % (SAMPLE_STRIDE, n))

    # L3: failing-key witnesses re-run with the verbatim engine
    wit_fail = 0
    js_cmp = 0

    def check_witness(atoms, want_det, want_surv):
        nonlocal wit_fail, js_cmp
        v, _ = region_verdict(atoms, 3, R, budget=50_000_000)
        if not (v["determined"] == want_det
                and v["survivors"] == want_surv):
            wit_fail += 1
        idx = pidx.get(atoms)
        if idx is not None:
            j = recs[idx]
            js_cmp += 1
            if verdict_triple(v) != (j["determined"], j["survivors"],
                                    j["first_losers"]):
                wit_fail += 1

    for kk, w in R11_WITNESSES.items():
        sp, g = kk.split("|")
        sizes = tuple(int(x) for x in sp.split(","))
        check_witness(tuple(w["det_atoms"]), True, w["det_survivors"])
        check_witness(tuple(w["ndet_atoms"]), False, w["ndet_survivors"])
        check_witness(chain_profile(sizes, int(g), 3), True,
                      w["chain_survivors"])

    # L4: FATE chains of the 56 published r=3..10 failing keys re-run
    for kk, v in R11_FATE_PUB56.items():
        sp, g = kk.split("|")
        sizes = tuple(int(x) for x in sp.split(","))
        catoms = chain_profile(sizes, int(g), 3)
        cv, _ = region_verdict(catoms, 3, R, budget=50_000_000)
        if cv["determined"] != v["chain_determined"] \
                or cv["survivors"] != v["chain_survivors"]:
            wit_fail += 1
        j = recs[pidx[catoms]]
        js_cmp += 1
        if verdict_triple(cv) != (j["determined"], j["survivors"],
                                  j["first_losers"]):
            wit_fail += 1

    if wit_fail != 0:
        sys.stderr.write("LIVE FAIL: witness re-verification %d failures\n"
                         % wit_fail)
        sys.exit(1)
    print("LIVE OK: all r=11 failing-key witnesses re-verified with the "
          "verbatim engine (%d keys), FATE chains of the 56 published "
          "r=3..10 failing keys re-run at r=11; %d witness verdicts also "
          "cross-checked against the committed JS records"
          % (len(R11_WITNESSES), js_cmp))


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
        os.path.dirname(os.path.abspath(__file__)), "output", AUDIT_NAME)
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
    if not all_ok:
        sys.exit(1)
    live_checks(audit1)


if __name__ == "__main__":
    run()
