#!/usr/bin/env python3
"""K0876 audit: 3-branch REMO determinacy size boundary cap<=12 for r=4,5,6.

Self-contained verifier. Deterministic (no randomness, no wall clock, no
network). Python 3.11+ / stdlib only.

Data provenance. The full-domain sweep records committed under output/
(js_cap12_r{3,4,5,6}.jsonl.gz, one JSONL record per canonical cap<=12
profile: index, atoms, determined, survivors, first_losers, states) were
produced by the JavaScript mask engine committed in this directory
(mask_engine_fast.js, with mask_engine.js as its readable base; the sweep
driver resume_sweep.sh segments are byte-concatenable because each record
is a pure function of (profile, r)). The mask engine carries
(survivorMask, firstLoserMask) per state instead of the verbatim
frozenset of (order, survivor) outcomes; determined / survivors /
first_losers agree with the verbatim engine's outcome_summary by
induction on the state DAG (each state's masks are bitwise ORs /
singletons of the same quantities the verbatim recursion unions as
outcome sets), and the reachable state space (hence the per-record
"states" count) is identical. This equivalence is re-verified live in
every run of this verifier:

- full cap<=7 domain (2048 canonical profiles) x r=3..6: verbatim engine
  == Python mask twin == committed JS records (8192 verdicts, verdict
  and state-count equality, 0 mismatches);
- stratified cap<=12 sample (every 24th profile for r=3,4; every 48th
  for r=5,6) x r=3..6: Python mask twin == committed JS records;
- all published failing-key witness atom vectors (K0862 44 at r=3,
  K0864 48 at r=4,5 and 12 at r=6, plus chain profiles) re-run with the
  verbatim engine and compared with the published survivors.

The Python mask twin (mask_game below) is an independent reimplementation
of the same state space; the enumeration, Burnside machinery, Theorem D
recursion and the verbatim region/cell game engine are verbatim from the
K0862 verifier via the K0875 verifier
(research/experiments/remo-k-branch-cap12-boundary-20261116/
verify_remo_k_branch_cap12_boundary.py).

Checked claims (proof text: report.md / K0876 item):

B    (Burnside vs direct enumeration, caps 10/11/12)  Identical to K0875
     (r-independent): fix counts (84494,3478,125)/(152171,5299,161)/
     (261749,7805,203) -> 15863/28065/47595 orbits; key counts
     715/1001/1365; cap-set inclusion.
R3   (r=3 cross-artifact)  The committed r=3 JS records reproduce the
     published K0875 audit exactly: the same 22 non-collapse keys, the
     same per-key partition counts, the same new-key census (363/364/0),
     the same 1343-entry det-map census (232 uniformly determined, 1111
     uniformly non-determined), the same max_states 31699, 890
     two-residue keys, failing residue pair {0,2}, FL violations 0,
     Delta=0 (1512 uniform profiles) all matching Theorem D; the 6
     mirror keys stay uniformly non-determined.
I12  (Theorem I12, cap<=12, r=4,5,6, finite complete)  For every 3-branch
     family with branch sizes <= 12 the determinacy non-collapse key set
     is EXACTLY the published cap<=10 boundary: r=4 and r=5 the 12 keys
     (8,8,9),(8,9,9) x gamma=0..5; r=6 the 6 keys (4,4,8),(4,8,8) x
     gamma=0..2.  ZERO new non-collapse keys appear when the size bound
     is raised from 10 to 12: every key containing an 11- or 12-branch
     collapses.  Failing-key structure is unchanged from K0864: det-side
     survivor uniformly P_2 (r=4,5) / P_3 (r=6), ndet possible-survivor
     sets within the published bounds, partition counts equal to the
     published tables; the 10 small-branch keys (2,3,8),(2,8,9),
     (3,3,8),(3,8,8),(3,8,9) x gamma=0,1 remain uniformly
     non-determined at r=4,5,6 over ALL cap<=12 profiles, and the 6
     mirror keys (4,4,8),(4,8,8) x gamma=0..2 remain uniformly
     non-determined at r=3,4,5 (they split only at r=6).
ANC  (anchors at cap<=12, r=4,5,6)  Lemma FL (possible first losers ==
     {C_i mod r}) violations 0 over all 47595 profiles; Delta=0 uniform
     profiles (1512, incl. the new sizes 11,12) all determined with the
     Theorem D survivor; every uniformly determined key's survivor
     equals the chain-profile survivor (Theorem G' survivor level,
     cap<=12 extension for r=3..6 - including all uniformly determined
     NEW keys with 11/12 branches); cap<=10 sub-census of uniformly
     determined keys equals the published K0864 counts (106/85/85) and
     two-residue key counts equal the K0872 counts (429/400/380).  The
     full cap<=12 key censuses (uniformly determined / non-determined /
     mixed, det-map census) are recorded per r as new published values.
RES  (residue lens, K0872 extension)  All failing keys have exactly two
     size residues mod r with the published pairs (r=4: {0,1}, r=5:
     {3,4}, r=6: {2,4}); the cap<=12 two-residue key census and the
     per-pair census of the 650 new keys (11/12 branches) are recorded;
     every new two-residue key collapses (out-of-sample test of the
     K0872 signature, incl. the new r=4 keys with residue pair {0,1}
     built from 9/12 sizes - none of them fails).

Scope / limits (do not over-read):
- I12 is COMPLETE over the finite parameter domain stated (all canonical
  profiles with branch sizes <= 12, r=4,5,6) - via Theorem E' it applies
  to every board realizing such a profile.
- Branch sizes >= 13 and r >= 7 (combined with sizes 11,12) are NOT
  covered here (K0866/K0869 cover r=7,8 at cap<=10 only).
- The mask engine does not reproduce elimination-order fields; order
  determinacy claims are NOT re-derived here (K0864 G' order level
  remains cap<=10).
- Uniformly non-determined does NOT mean "outcome-free": the possible
  survivor sets still depend on atoms; per-key ndet survivor sets are
  recorded as data, only bounded for the failing keys.
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

# K0862 published exact 22 non-collapse keys (Theorem H, cap<=10, r=3),
# machine-extracted from
# research/experiments/remo-k-branch-collapse-boundary-20261116/output/
#   remo_k_branch_boundary_audit.json (byte-verified against main; same
# constant as the K0875 verifier).
EXPECTED_FAILING_22 = [
    [2, 3, 8], [2, 3, 8], [2, 8, 9], [2, 8, 9], [3, 3, 8], [3, 3, 8],
    [3, 8, 8], [3, 8, 8], [3, 8, 9], [3, 8, 9], [8, 8, 9], [8, 8, 9],
    [8, 8, 9], [8, 8, 9], [8, 8, 9], [8, 8, 9], [8, 9, 9], [8, 9, 9],
    [8, 9, 9], [8, 9, 9], [8, 9, 9], [8, 9, 9],
]
GAMMA_22 = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5]
EXPECTED_FAILING_22_KEYS = sorted(
    [[list(sp), g] for sp, g in zip(EXPECTED_FAILING_22, GAMMA_22)]
)

# The 10 small-branch keys of the K0862 r=3 list (published at cap<=10 by
# K0864 as uniformly non-determined for r=4,5,6: n_det == 0).
SMALL_KEYS_10 = sorted(
    [[list(sp), g] for sp, g in zip(EXPECTED_FAILING_22, GAMMA_22)
     if min(sp) < 8]
)
# The 6 mirror keys (published at cap<=10 by K0864 as uniformly
# non-determined for r=3,4,5, splitting only at r=6).
MIRROR_KEYS_6 = [[[4, 4, 8], g] for g in range(3)] + [[[4, 8, 8], g] for g in range(3)]

# K0862 published minimal witnesses (22 keys x det/ndet atom vectors),
# machine-extracted from
# research/experiments/remo-k-branch-collapse-boundary-20261116/output/
#   remo_k_branch_boundary_audit.json (byte-verified against main; same
# constant as the K0875 verifier; all 44 atom vectors are canonical
# members of the cap<=12 enumeration).
K0862_WITNESSES = {"2,3,8|0": [[1, 1, 1, 7, 0, 1, 0], [1, 1, 0, 5, 1, 2, 0]], "2,3,8|1": [[1, 2, 0, 7, 0, 0, 1], [1, 1, 0, 6, 0, 1, 1]], "2,8,9|0": [[1, 2, 1, 4, 0, 5, 0], [1, 1, 0, 1, 1, 7, 0]], "2,8,9|1": [[1, 3, 0, 4, 0, 4, 1], [1, 1, 0, 2, 0, 6, 1]], "3,3,8|0": [[1, 1, 1, 6, 1, 1, 0], [1, 1, 0, 4, 2, 2, 0]], "3,3,8|1": [[1, 1, 1, 7, 0, 0, 1], [1, 1, 0, 5, 1, 1, 1]], "3,8,8|0": [[1, 1, 1, 1, 1, 6, 0], [1, 1, 2, 3, 0, 5, 0]], "3,8,8|1": [[1, 1, 6, 2, 0, 0, 1], [1, 1, 1, 2, 0, 5, 1]], "3,8,9|0": [[1, 2, 1, 3, 1, 5, 0], [1, 1, 1, 2, 1, 6, 0]], "3,8,9|1": [[1, 3, 0, 3, 1, 4, 1], [1, 1, 0, 1, 1, 6, 1]], "8,8,9|0": [[1, 1, 3, 1, 4, 4, 0], [1, 1, 6, 5, 1, 2, 0]], "8,8,9|1": [[1, 1, 3, 2, 3, 3, 1], [1, 1, 5, 4, 1, 2, 1]], "8,8,9|2": [[1, 1, 2, 1, 3, 3, 2], [1, 1, 4, 3, 1, 2, 2]], "8,8,9|3": [[1, 1, 2, 2, 2, 2, 3], [1, 1, 3, 2, 1, 2, 3]], "8,8,9|4": [[1, 1, 2, 3, 1, 1, 4], [1, 1, 1, 1, 2, 2, 4]], "8,8,9|5": [[1, 1, 2, 4, 0, 0, 5], [1, 1, 1, 2, 1, 1, 5]], "8,9,9|0": [[1, 1, 4, 2, 3, 4, 0], [1, 1, 6, 6, 1, 2, 0]], "8,9,9|1": [[1, 1, 3, 1, 3, 4, 1], [1, 1, 5, 5, 1, 2, 1]], "8,9,9|2": [[1, 1, 3, 2, 2, 3, 2], [1, 1, 4, 4, 1, 2, 2]], "8,9,9|3": [[1, 1, 2, 1, 2, 3, 3], [1, 1, 3, 3, 1, 2, 3]], "8,9,9|4": [[1, 1, 3, 2, 1, 1, 4], [1, 1, 2, 2, 1, 2, 4]], "8,9,9|5": [[1, 1, 3, 3, 0, 0, 5], [1, 1, 1, 1, 1, 2, 5]]}

# K0864 published r=3/r=4/r=5 partition counts for the (8,8,9)/(8,9,9)
# families, machine-extracted from
# research/experiments/remo-k-branch-r-boundary-20261116/output/
#   remo_k_branch_r_boundary_audit.json (partition_89_families),
# byte-verified against main (same constant as the K0875 verifier).
K0864_PARTITION_89 = {"8,8,9|0": {"n_det_r3_r4_r5": [92, 92, 92], "n_det_r6": 0, "profiles": 100}, "8,8,9|1": {"n_det_r3_r4_r5": [62, 62, 62], "n_det_r6": 0, "profiles": 70}, "8,8,9|2": {"n_det_r3_r4_r5": [40, 40, 40], "n_det_r6": 0, "profiles": 48}, "8,8,9|3": {"n_det_r3_r4_r5": [22, 22, 22], "n_det_r6": 0, "profiles": 30}, "8,8,9|4": {"n_det_r3_r4_r5": [10, 10, 10], "n_det_r6": 0, "profiles": 18}, "8,8,9|5": {"n_det_r3_r4_r5": [3, 3, 3], "n_det_r6": 0, "profiles": 9}, "8,9,9|0": {"n_det_r3_r4_r5": [102, 102, 102], "n_det_r6": 0, "profiles": 110}, "8,9,9|1": {"n_det_r3_r4_r5": [72, 72, 72], "n_det_r6": 0, "profiles": 80}, "8,9,9|2": {"n_det_r3_r4_r5": [46, 46, 46], "n_det_r6": 0, "profiles": 54}, "8,9,9|3": {"n_det_r3_r4_r5": [28, 28, 28], "n_det_r6": 0, "profiles": 36}, "8,9,9|4": {"n_det_r3_r4_r5": [13, 13, 13], "n_det_r6": 0, "profiles": 21}, "8,9,9|5": {"n_det_r3_r4_r5": [4, 4, 4], "n_det_r6": 0, "profiles": 12}}

# K0864 published r=6 partition counts for the (4,4,8)/(4,8,8) families
# (mirror_48_families.n_det_by_r["6"], byte-verified against main).
K0864_MIRROR48_R6 = {"4,4,8|0": {"n_det_r6": 16, "profiles": 20}, "4,4,8|1": {"n_det_r6": 7, "profiles": 10}, "4,4,8|2": {"n_det_r6": 2, "profiles": 4}, "4,8,8|0": {"n_det_r6": 34, "profiles": 39}, "4,8,8|1": {"n_det_r6": 19, "profiles": 24}, "4,8,8|2": {"n_det_r6": 6, "profiles": 11}}

# K0864 published cap<=10 failing-key boundary for r=4,5,6 (Theorem I),
# machine-extracted from
# research/experiments/remo-k-branch-r-boundary-20261116/output/
#   remo_k_branch_r_boundary_audit.json (sweeps[r]["failing_keys"]),
# byte-verified against main.
R_BOUNDARY_FAILING = {
    4: [[[8, 8, 9], g] for g in range(6)] + [[[8, 9, 9], g] for g in range(6)],
    5: [[[8, 8, 9], g] for g in range(6)] + [[[8, 9, 9], g] for g in range(6)],
    6: [[[4, 4, 8], g] for g in range(3)] + [[[4, 8, 8], g] for g in range(3)],
}
R_BOUNDARY_DET_SURVIVOR = {4: [2], 5: [2], 6: [3]}
R_BOUNDARY_NDET_BOUND = {4: [[1, 2, 3]], 5: [[1, 2, 3], [1, 2, 3, 4]], 6: [[2, 3]]}
R_BOUNDARY_RESIDUE_PAIR = {4: [0, 1], 5: [3, 4], 6: [2, 4]}

# K0864 published failing-key witnesses for r=4,5,6 (failing_witnesses,
# byte-verified against main): per key#r the det and ndet witness atom
# vectors with their published survivors, plus the chain survivor.
RB_WITNESSES = {
    "4": {
        "8,8,9|0": {"det_atoms": [1, 1, 3, 1, 4, 4, 0], "ndet_atoms": [1, 1, 6, 5, 1, 2, 0], "det_survivors": [2], "ndet_survivors": [1, 2, 3], "chain_survivors": [2]},
        "8,8,9|1": {"det_atoms": [1, 1, 3, 2, 3, 3, 1], "ndet_atoms": [1, 1, 5, 4, 1, 2, 1], "det_survivors": [2], "ndet_survivors": [1, 2, 3], "chain_survivors": [2]},
        "8,8,9|2": {"det_atoms": [1, 1, 2, 1, 3, 3, 2], "ndet_atoms": [1, 1, 4, 3, 1, 2, 2], "det_survivors": [2], "ndet_survivors": [1, 2, 3], "chain_survivors": [2]},
        "8,8,9|3": {"det_atoms": [1, 1, 2, 2, 2, 2, 3], "ndet_atoms": [1, 1, 3, 2, 1, 2, 3], "det_survivors": [2], "ndet_survivors": [1, 2, 3], "chain_survivors": [2]},
        "8,8,9|4": {"det_atoms": [1, 1, 2, 3, 1, 1, 4], "ndet_atoms": [1, 1, 1, 1, 2, 2, 4], "det_survivors": [2], "ndet_survivors": [1, 2, 3], "chain_survivors": [2]},
        "8,8,9|5": {"det_atoms": [1, 1, 2, 4, 0, 0, 5], "ndet_atoms": [1, 1, 1, 2, 1, 1, 5], "det_survivors": [2], "ndet_survivors": [1, 2, 3], "chain_survivors": [2]},
        "8,9,9|0": {"det_atoms": [1, 1, 4, 2, 3, 4, 0], "ndet_atoms": [1, 1, 6, 6, 1, 2, 0], "det_survivors": [2], "ndet_survivors": [1, 2, 3], "chain_survivors": [2]},
        "8,9,9|1": {"det_atoms": [1, 1, 3, 1, 3, 4, 1], "ndet_atoms": [1, 1, 5, 5, 1, 2, 1], "det_survivors": [2], "ndet_survivors": [1, 2, 3], "chain_survivors": [2]},
        "8,9,9|2": {"det_atoms": [1, 1, 3, 2, 2, 3, 2], "ndet_atoms": [1, 1, 4, 4, 1, 2, 2], "det_survivors": [2], "ndet_survivors": [1, 2, 3], "chain_survivors": [2]},
        "8,9,9|3": {"det_atoms": [1, 1, 2, 1, 2, 3, 3], "ndet_atoms": [1, 1, 3, 3, 1, 2, 3], "det_survivors": [2], "ndet_survivors": [1, 2, 3], "chain_survivors": [2]},
        "8,9,9|4": {"det_atoms": [1, 1, 3, 2, 1, 1, 4], "ndet_atoms": [1, 1, 2, 2, 1, 2, 4], "det_survivors": [2], "ndet_survivors": [1, 2, 3], "chain_survivors": [2]},
        "8,9,9|5": {"det_atoms": [1, 1, 3, 3, 0, 0, 5], "ndet_atoms": [1, 1, 1, 1, 1, 2, 5], "det_survivors": [2], "ndet_survivors": [1, 2, 3], "chain_survivors": [2]},
    },
    "5": {
        "8,8,9|0": {"det_atoms": [1, 1, 3, 1, 4, 4, 0], "ndet_atoms": [1, 1, 6, 5, 1, 2, 0], "det_survivors": [2], "ndet_survivors": [1, 2, 3], "chain_survivors": [2]},
        "8,8,9|1": {"det_atoms": [1, 1, 3, 2, 3, 3, 1], "ndet_atoms": [1, 1, 5, 4, 1, 2, 1], "det_survivors": [2], "ndet_survivors": [1, 2, 3], "chain_survivors": [2]},
        "8,8,9|2": {"det_atoms": [1, 1, 2, 1, 3, 3, 2], "ndet_atoms": [1, 1, 4, 3, 1, 2, 2], "det_survivors": [2], "ndet_survivors": [1, 2, 3], "chain_survivors": [2]},
        "8,8,9|3": {"det_atoms": [1, 1, 2, 2, 2, 2, 3], "ndet_atoms": [1, 1, 3, 2, 1, 2, 3], "det_survivors": [2], "ndet_survivors": [1, 2, 3], "chain_survivors": [2]},
        "8,8,9|4": {"det_atoms": [1, 1, 2, 3, 1, 1, 4], "ndet_atoms": [1, 1, 1, 1, 2, 2, 4], "det_survivors": [2], "ndet_survivors": [1, 2, 3, 4], "chain_survivors": [2]},
        "8,8,9|5": {"det_atoms": [1, 1, 2, 4, 0, 0, 5], "ndet_atoms": [1, 1, 1, 2, 1, 1, 5], "det_survivors": [2], "ndet_survivors": [1, 2, 3], "chain_survivors": [2]},
        "8,9,9|0": {"det_atoms": [1, 1, 4, 2, 3, 4, 0], "ndet_atoms": [1, 1, 6, 6, 1, 2, 0], "det_survivors": [2], "ndet_survivors": [1, 2, 3], "chain_survivors": [2]},
        "8,9,9|1": {"det_atoms": [1, 1, 3, 1, 3, 4, 1], "ndet_atoms": [1, 1, 5, 5, 1, 2, 1], "det_survivors": [2], "ndet_survivors": [1, 2, 3], "chain_survivors": [2]},
        "8,9,9|2": {"det_atoms": [1, 1, 3, 2, 2, 3, 2], "ndet_atoms": [1, 1, 4, 4, 1, 2, 2], "det_survivors": [2], "ndet_survivors": [1, 2, 3], "chain_survivors": [2]},
        "8,9,9|3": {"det_atoms": [1, 1, 2, 1, 2, 3, 3], "ndet_atoms": [1, 1, 3, 3, 1, 2, 3], "det_survivors": [2], "ndet_survivors": [1, 2, 3], "chain_survivors": [2]},
        "8,9,9|4": {"det_atoms": [1, 1, 3, 2, 1, 1, 4], "ndet_atoms": [1, 1, 2, 2, 1, 2, 4], "det_survivors": [2], "ndet_survivors": [1, 2, 3], "chain_survivors": [2]},
        "8,9,9|5": {"det_atoms": [1, 1, 3, 3, 0, 0, 5], "ndet_atoms": [1, 1, 1, 1, 1, 2, 5], "det_survivors": [2], "ndet_survivors": [1, 2, 3], "chain_survivors": [2]},
    },
    "6": {
        "4,4,8|0": {"det_atoms": [1, 1, 1, 4, 2, 2, 0], "ndet_atoms": [1, 1, 0, 2, 3, 3, 0], "det_survivors": [3], "ndet_survivors": [2, 3], "chain_survivors": [3]},
        "4,4,8|1": {"det_atoms": [1, 1, 1, 5, 1, 1, 1], "ndet_atoms": [1, 1, 0, 3, 2, 2, 1], "det_survivors": [3], "ndet_survivors": [2, 3], "chain_survivors": [3]},
        "4,4,8|2": {"det_atoms": [1, 1, 1, 6, 0, 0, 2], "ndet_atoms": [1, 1, 0, 4, 1, 1, 2], "det_survivors": [3], "ndet_survivors": [2, 3], "chain_survivors": [3]},
        "4,8,8|0": {"det_atoms": [1, 1, 2, 2, 1, 5, 0], "ndet_atoms": [1, 1, 3, 4, 0, 4, 0], "det_survivors": [3], "ndet_survivors": [2, 3], "chain_survivors": [3]},
        "4,8,8|1": {"det_atoms": [1, 1, 1, 1, 1, 5, 1], "ndet_atoms": [1, 1, 2, 3, 0, 4, 1], "det_survivors": [3], "ndet_survivors": [2, 3], "chain_survivors": [3]},
        "4,8,8|2": {"det_atoms": [1, 1, 5, 2, 0, 0, 2], "ndet_atoms": [1, 1, 1, 2, 0, 4, 2], "det_survivors": [3], "ndet_survivors": [2, 3], "chain_survivors": [3]},
    },
}

# K0875 published r=3 cap<=12 values, machine-extracted from
# research/experiments/remo-k-branch-cap12-boundary-20261116/output/
#   remo_k_branch_cap12_boundary_audit.json (sweep_cap12_r3),
# byte-verified against main.
K0875_NEW_KEY_CENSUS = {
    "keys_with_11": 363,
    "keys_with_12": 364,
    "failing_with_11_or_12": 0,
    "two_residue_keys": 890,
}
K0875_DET_MAP_CENSUS = {"entries": 1343, "uniformly_det": 232,
                         "uniformly_ndet": 1111}
K0875_MAX_STATES_R3 = 31699
K0875_AUDIT_RELPATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "remo-k-branch-cap12-boundary-20261116",
    "output", "remo_k_branch_cap12_boundary_audit.json",
)

# K0864 published cap<=10 uniformly-determined key counts (theorem_g_prime)
# and K0872 published cap<=10 two-residue key counts, machine-extracted and
# byte-verified against main.
K0864_UNIF_DET_KEYS_CAP10 = {4: 106, 5: 85, 6: 85}
K0872_TWO_RESIDUE_KEYS_CAP10 = {4: 429, 5: 400, 6: 380}

R_VALUES = (3, 4, 5, 6)
SAMPLE_STRIDE = {3: 24, 4: 24, 5: 48, 6: 48}
DELTA0_EXPECTED = 1512


def load_jsonl(r):
    base = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "output", "js_cap12_r%d.jsonl" % r,
    )
    if os.path.exists(base + ".gz"):
        with gzip.open(base + ".gz", "rt", encoding="utf-8") as f:
            lines = f.read().splitlines()
    elif os.path.exists(base):
        with open(base, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
    else:
        raise FileNotFoundError(base + "[.gz]")
    return [json.loads(line) for line in lines if line.strip()]


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
        "item": "K0876",
        "title": "3-branch REMO determinacy size boundary cap<=12 for "
            "r=4,5,6: non-collapse keys stay exactly the published "
            "cap<=10 boundary",
        "date": "2026-11-16",
        "engine_provenance": "verbatim region game / enumeration / "
            "Burnside / Theorem D from the K0862 verifier via K0875; "
            "full-domain records produced by the committed JavaScript "
            "mask engine (mask_engine_fast.js, resume_sweep.sh driver); "
            "Python mask twin cross-validated live in every run",
        "r_swept": [3, 4, 5, 6],
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
        recs = load_jsonl(r)
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
        audit["sweep_inputs"]["r%d" % r] = {
            "records": len(recs),
            "skipped": sum(1 for rec in recs if rec.get("skipped")),
            "sha256_uncompressed": digest,
            "sha256_gz": gz_digest,
            "max_states": max(rec["states"] for rec in recs),
        }
        record(
            "r=%d committed sweep records: 47595 records, index-complete, "
            "atoms == enumeration, no budget skips" % r,
            ok,
            {"records": len(recs), "sha256": digest},
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

    # ---- C3: r=3 cross-artifact vs K0875 published audit
    a3 = analysis["r3"]
    with open(K0875_AUDIT_RELPATH, "r", encoding="utf-8") as f:
        sw3 = json.load(f)["sweep_cap12_r3"]
    pub_det_map = sw3["det_map_collapsing_keys"]
    pub_sorted = sorted(pub_det_map, key=lambda e: (e[0], e[1]))
    ok = (
        a3["failing_keys"] == sw3["failing_keys"]
        and a3["failing_keys"] == EXPECTED_FAILING_22_KEYS
        and all(
            a3["failing_partitions"][pkstr(p)]
            == {"n_det": sw3["failing_partitions"][pkstr(p)]["n_det"],
                "profiles": sw3["failing_partitions"][pkstr(p)]["profiles"]}
            for p in sw3["failing_keys"]
        )
        and a3["det_map_collapsing_keys"] == pub_sorted
        and len(pub_sorted) == K0875_DET_MAP_CENSUS["entries"]
        and sum(1 for e in pub_sorted if e[2])
        == K0875_DET_MAP_CENSUS["uniformly_det"]
        and a3["new_key_census"]["keys_with_11"] == K0875_NEW_KEY_CENSUS["keys_with_11"]
        and a3["new_key_census"]["keys_with_12"] == K0875_NEW_KEY_CENSUS["keys_with_12"]
        and a3["new_key_census"]["failing_with_11_or_12"] == 0
        and a3["two_residue_keys"] == K0875_NEW_KEY_CENSUS["two_residue_keys"]
        and a3["failing_residue_pairs"] == [[0, 2]]
        and a3["failing_keys_two_residue"]
        and a3["max_states"] == K0875_MAX_STATES_R3
        and a3["first_loser_violations"] == 0
        and a3["delta0_profiles"] == DELTA0_EXPECTED
        and a3["delta0_mismatches"] == 0
        and a3["failing_det_survivors"] == [[1]]
        and all(t in ([1, 2], [0, 1, 2]) for t in a3["failing_ndet_sets"])
    )
    record(
        "r=3 cross-artifact: committed JS records reproduce the published "
        "K0875 audit exactly (22 failing keys, per-key partitions, "
        "det-map census 232/1111, new-key census 363/364/0, 890 "
        "two-residue keys, failing pair {0,2}, max_states 31699, FL 0, "
        "Delta=0 1512 profiles, det survivor P_1, ndet sets within "
        "{{1,2},{0,1,2}})",
        ok,
        {"failing": len(a3["failing_keys"]),
         "two_residue": a3["two_residue_keys"]},
    )
    record(
        "r=3 Theorem G' survivor level at cap<=12: every uniformly "
        "determined key's survivor equals the chain survivor (232 keys)",
        a3["gprime_survivor_mismatches"] == 0,
        {"uniformly_determined_keys": a3["uniformly_determined_keys"],
         "gprime_survivor_mismatches": a3["gprime_survivor_mismatches"]},
    )
    record(
        "r=3 the 6 mirror keys (4,4,8),(4,8,8) x gamma=0..2 are uniformly "
        "non-determined over ALL cap<=12 profiles (K0864 cap<=10 fact "
        "extended to r=3 at cap<=12)",
        len(a3["mirror_keys_6_ndet"]) == 6
        and all(v == 0 for v in a3["mirror_keys_6_ndet"].values()),
        {"mirror_keys_6_ndet": a3["mirror_keys_6_ndet"]},
    )

    # ---- C4: r=4,5,6 Theorem I12
    for r in (4, 5, 6):
        a = analysis["r%d" % r]
        pub = sorted(R_BOUNDARY_FAILING[r])
        ok = (
            a["failing_keys"] == pub
            and a["new_key_census"]["failing_with_11_or_12"] == 0
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
            "Theorem I12 (cap<=12, r=%d): non-collapse keys are exactly "
            "the published %d cap<=10 keys; zero new keys with an 11/12 "
            "branch fail; det survivor P_%d uniform; ndet sets within "
            "published bounds; FL violations 0; Delta=0 1512 profiles all "
            "Theorem D; failing residue pair %s" % (
                r, len(pub), R_BOUNDARY_DET_SURVIVOR[r][0],
                R_BOUNDARY_RESIDUE_PAIR[r]),
            ok,
            {"failing": len(a["failing_keys"]),
             "failing_with_11_or_12":
                 a["new_key_census"]["failing_with_11_or_12"]},
        )
        # partition counts vs published tables
        part_ok = True
        if r in (4, 5):
            for kk, v in K0864_PARTITION_89.items():
                want_det = v["n_det_r3_r4_r5"][r - 3]
                got = a["failing_partitions"].get(kk)
                if got is None or got["n_det"] != want_det \
                        or got["profiles"] != v["profiles"]:
                    part_ok = False
        else:
            for kk, v in K0864_MIRROR48_R6.items():
                got = a["failing_partitions"].get(kk)
                if got is None or got["n_det"] != v["n_det_r6"] \
                        or got["profiles"] != v["profiles"]:
                    part_ok = False
        record(
            "r=%d failing-key partition counts match the published K0864 "
            "tables (%s)" % (
                r, "8/9 families" if r in (4, 5) else "4/8 mirror families"),
            part_ok,
            {"families_checked": len(K0864_PARTITION_89) if r in (4, 5)
             else len(K0864_MIRROR48_R6)},
        )
        # witnesses valid inside the committed records
        wit_ok = True
        for kk, w in RB_WITNESSES[str(r)].items():
            for tag, atoms_s in (("det", w["det_atoms"]),
                                 ("ndet", w["ndet_atoms"])):
                atoms = tuple(atoms_s)
                idx = pidx.get(atoms)
                if idx is None:
                    wit_ok = False
                    continue
                rec = records[r][idx]
                want_det = tag == "det"
                want_surv = (w["det_survivors"] if want_det
                             else w["ndet_survivors"])
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
            "r=%d published failing-key witnesses (K0864) and their chain "
            "survivors are valid inside the committed cap<=12 records" % r,
            wit_ok,
            {"witness_keys": len(RB_WITNESSES[str(r)])},
        )
        # fixed published families stay uniform where published
        small_ok = all(v == 0 for v in a["small_keys_10_ndet"].values()) \
            and len(a["small_keys_10_ndet"]) == 10
        record(
            "r=%d the 10 small-branch keys (2,3,8),(2,8,9),(3,3,8),"
            "(3,8,8),(3,8,9) x gamma=0,1 are uniformly non-determined "
            "over ALL cap<=12 profiles (K0864 cap<=10 fact extended)" % r,
            small_ok,
            {"keys": 10},
        )
        if r in (4, 5):
            mir_ok = (all(v == 0 for v in a["mirror_keys_6_ndet"].values())
                      and len(a["mirror_keys_6_ndet"]) == 6)
            mir_note = "uniformly non-determined over ALL cap<=12 profiles"
        else:
            mir_ok = len(a["mirror_keys_6_ndet"]) == 6
            mir_note = "all six keys present (split at r=6, published)"
        record(
            "r=%d the 6 mirror keys (4,4,8),(4,8,8) x gamma=0..2: %s" % (
                r, mir_note),
            mir_ok,
            {"mirror_keys_6_ndet": a["mirror_keys_6_ndet"]},
        )
        # cap<=10 published sub-census
        sub_ok = (
            a["uniformly_determined_keys_cap10"] == K0864_UNIF_DET_KEYS_CAP10[r]
            and a["two_residue_keys_cap10"] == K0872_TWO_RESIDUE_KEYS_CAP10[r]
        )
        record(
            "r=%d cap<=10 sub-census from the committed records equals the "
            "published values (uniformly determined %d keys, two-residue "
            "%d keys)" % (
                r, K0864_UNIF_DET_KEYS_CAP10[r],
                K0872_TWO_RESIDUE_KEYS_CAP10[r]),
            sub_ok,
            {"uniformly_determined_cap10":
                 a["uniformly_determined_keys_cap10"],
             "two_residue_cap10": a["two_residue_keys_cap10"]},
        )
        # G' survivor level at cap<=12 (r=4,5,6)
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
    recs = {r: {rec["i"]: rec for rec in load_jsonl(r)} for r in R_VALUES}

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
    if mism != 0 or n != 4 * 2048:
        sys.stderr.write("LIVE FAIL: cap<=7 triple check %d mismatches / %d\n"
                         % (mism, n))
        sys.exit(1)
    print("LIVE OK: cap<=7 full domain: verbatim == mask twin == committed "
          "JS records (verdicts and state counts) on %d verdicts (r=3..6)"
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
    print("LIVE OK: stratified cap<=12 sample x r=3..6: mask twin == "
          "committed JS records on %d verdicts (strides %s)"
          % (n, SAMPLE_STRIDE))

    # L3: published witnesses re-run with the verbatim engine
    wit_fail = 0
    js_cmp = 0
    for kk, pair in K0862_WITNESSES.items():
        for tag, atoms_s in (("det", pair[0]), ("ndet", pair[1])):
            atoms = tuple(atoms_s)
            v, _ = region_verdict(atoms, 3, 3, budget=50_000_000)
            if tag == "det":
                if not (v["determined"] and v["survivors"] == [1]):
                    wit_fail += 1
            else:
                if v["determined"] or sorted(v["survivors"]) not in \
                        ([0, 1, 2], [1, 2]):
                    wit_fail += 1
            idx = pidx.get(atoms)
            if idx is not None:
                j = recs[3][idx]
                js_cmp += 1
                if verdict_triple(v) != (j["determined"], j["survivors"],
                                        j["first_losers"]):
                    wit_fail += 1
    for rs in ("4", "5", "6"):
        for kk, w in RB_WITNESSES[rs].items():
            for tag, atoms_s in (("det", w["det_atoms"]),
                                 ("ndet", w["ndet_atoms"])):
                atoms = tuple(atoms_s)
                v, _ = region_verdict(atoms, 3, int(rs), budget=50_000_000)
                want_surv = (w["det_survivors"] if tag == "det"
                             else w["ndet_survivors"])
                if not (v["determined"] == (tag == "det")
                        and v["survivors"] == want_surv):
                    wit_fail += 1
                idx = pidx.get(atoms)
                if idx is not None:
                    j = recs[int(rs)][idx]
                    js_cmp += 1
                    if verdict_triple(v) != (j["determined"], j["survivors"],
                                            j["first_losers"]):
                        wit_fail += 1
            sp, g = kk.split("|")
            sizes = tuple(int(x) for x in sp.split(","))
            cv, _ = region_verdict(chain_profile(sizes, int(g), 3), 3,
                                   int(rs), budget=50_000_000)
            if not (cv["determined"]
                    and cv["survivors"] == w["chain_survivors"]):
                wit_fail += 1
    if wit_fail != 0:
        sys.stderr.write("LIVE FAIL: witness re-verification %d failures\n"
                         % wit_fail)
        sys.exit(1)
    print("LIVE OK: all published witnesses re-verified with the verbatim "
          "engine (K0862 44 at r=3, K0864 48 at r=4,5, 12 at r=6, chain "
          "survivors included; %d also cross-checked against the committed "
          "JS records)" % js_cmp)


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
        "remo_k_branch_cap12_r456_boundary_audit.json",
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
