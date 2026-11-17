#!/usr/bin/env python3
"""K0906 audit: universal proof of Theorem J (label-closure method).

Theorem J (proved in report.md of this directory; K0902 formulated it as
a conjecture with a proof sketch, K0904 verified it finitely over the
r=2..13 x cap<=10 matrix): for the counting game of the atom profile
(REMO rules of K0859, transfer to boards by Theorem E' of K0861) with
k >= 1 branches, branch capacities C_1..C_k >= 1, M = max C_i, and
r >= max(M, 2) players:

  (i)   the survivor set sv and the determinacy flag det are constant
        in r,
  (ii)  the first-loser set is fl(r) = {C_i mod r} (Lemma FL, K0864;
        re-derived at the root below), hence the constant value {C_i}
        for all r > M,
  (iii) every possible survivor label sigma satisfies sigma <= M - 1.

Proof method (label closure; see report.md): L1 the play tree up to the
first event is r-independent and every first event has depth C_Y <= M
<= r with movers P_0..P_{C_Y-1} distinct; L2 the post-event cascade
eats the phantom labels C_Y..r-1 (stone-less losers do not change the
board, so maximality persists) and the cascade's stone-holder removal
sequence, board evolution and |active| evolution are identical for all
r >= max(M,2) (including the boundary r = C_Y = M), so the normalized
post-cascade result (a terminal survivor sigma < C_Y, or a state with
stones/active/mover inside labels < C_Y) is r-independent; L3 from a
state with active subset of {0..a-1} every transition (legality,
maximality, removal, next_active skipping inactive labels) is
r-independent for r >= a, so sub-game values are r-independent;
L4 gluing gives (i) sv = union of play post-values, (ii) fl =
{C_i mod r} because every branch is first-saturable from the empty
board, (iii) sigma < C_Y <= M. Lemma C1' (rigid form, canonical domain
e_j >= 1): the cascade always stops at P_0, giving the rigid
post-state; its capacity inequality uses e_j >= 1 and FAILS in the
wider C_i >= 1 domain (counterexample battery below), but Theorem J
does not need C1'.

This verifier does NOT verify the prose. It re-derives every finite
prediction of Theorem J on top of the five committed cap<=10 columns
(r=9..13, K0893/K0895/K0897/K0898/K0902 packed records), and it live
verifies the proof's intermediate objects with an independent cascade
simulator (LC1/LC2) plus an independent sub-game DFS (L3/L4 gluing),
cross-checked against the verbatim engine and the Python mask twin
(K0902 machinery, verbatim block below).

Machine checks (assembled into output/theorem_j_audit.json; any
violation aborts):
  THJ-B1  Burnside/orbit enumeration anchors (84494,3478,125 -> 15863).
  THJ-J0  five committed packed columns complete, ordered, 15863 each.
  THJ-J1  sv/det constant on every r >= max(M,2) committed column
          (71987 eligible profile-column judgments, 0 violations).
  THJ-J2  fl == {C_i mod r} on all 5 x 15863 = 79315 committed
          records (0 violations; redundant Lemma FL anchor).
  THJ-J3  fl constant = {C_i} for all committed r > M (0 violations).
  THJ-J4  K0902 ARITH set equalities re-derived from the columns:
          fl diff r13-r10 == maxC=10 set (7328), fl diff r13-r9 ==
          maxC>=9 set (11533), sv diff r13-r9 == the same 7328 set,
          all other sv/det diffs empty.
  THJ-SG  anti-overclaim guard: state counts are NOT r-invariant
          (max states 741630 at r=13 vs 666030 at r=12).

Live checks (recomputed from scratch every run; print, exit 1 on any
violation):
  L0   cap<=7 full domain x r=13: mask twin == committed r=13 records.
  J5   cap<=7 full domain x r in {max(M,2),+1,+2}: sv/det invariance,
       fl closed form, sigma <= M-1 (6144 judgments).
  J5b  cap<=5 full domain x same r values: verbatim engine == mask
       twin (1038 judgments).
  J6   sharpness probe r = M-1 vs r = M on cap<=7, M>=3: 2022 of 2041
       profiles change sv/det (the bound max(M,2) is near-optimal).
  J7a  k=2 battery (56 canonical profiles, sizes <= 6) x same r
       values: Theorem J predictions with the mask twin.
  J7b  k=4 battery (22 profiles: 15 singleton-only + 7 chain) x same
       r values: Theorem J predictions with the mask twin.
  J8   size 11/12 anchor battery (14 profiles, N <= 16 stones) x
       r in {M, M+1, M+2}: NEW anchors outside every committed column
       (r=13,14 for M=12 etc.), Theorem J predictions hold.
  J9   cascade simulator (LC1/LC2, independent implementation):
       first-event play enumeration over cap<=5 full domain + special
       batteries (empty singleton atoms, k=2/k=3/k=4), post-cascade
       normalized results identical across r, rigid form (C1') holds
       on every canonical play, violations confined to the special
       battery, root fl re-derived play-wise: {C_i mod r} on the
       canonical domain, the refined constant-capacity-set form
       {c mod r : c in E} (E = first-saturable capacities) on the
       special battery - the latter exposes the DOMAIN BOUNDARY of
       Lemma FL (its reachability step needs e_j >= 1; witness
       atoms (0,0,0,0,1,1,0), sizes (1,1,2), where every event
       saturates branch 1 or 2 at depth 1 and branch 3 is never
       first-saturated, so fl != {C_i mod r} in the wide domain), and
       Theorem J (i)/(iii) verified on the special battery via the
       simulator + sub-game DFS (sv/det r-invariant, sigma <= M-1).
  L9   gluing: simulator + sub-game DFS (L3, independent
       implementation) reproduces the mask twin root sv/det/fl on the
       cap<=4 full domain + k=2 battery + k=4 battery, and the
       verbatim engine agrees (three independent engines).

Self-contained. Deterministic (no randomness, no wall clock, no
network). Python 3.11+ / stdlib only. No new sweeps: the only data
read are the five committed packed columns of the sibling experiment
directories.
"""

import hashlib
import json
import os
import sys

# ---------------------------------------------------------------------------
# verbatim engine block: K0902 verifier lines 173-599 (which is itself the
# K0862/K0875 verbatim engine + canonical enumeration + the Python mask
# twin). theorem_d / theorem_d_table inside the block belong to the K0859
# recursion and are retained verbatim but unused by the K0906 checks.
# ---------------------------------------------------------------------------
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


def next_active_mask(p, r, active):
    """Bitmask variant of next_active (same semantics)."""
    for d in range(1, r + 1):
        q = (p + d) % r
        if (active >> q) & 1:
            return q
    raise AssertionError("no active player after %d" % p)


def mask_game(atoms, k, r, budget=50_000_000):
    """Mask twin of the verbatim engine (identical state space,
    identical survivor/first-loser masks, identical memo size), with
    the memo state encoded compactly: counts as one flat bytes of
    natoms*r small ints (counts[m*r + p] = stones of player p on atom
    m, values <= cap <= 10) and mover/active as ints. The K0898
    tuple-of-tuples + frozenset keys cost ~1.7 KiB per state, which
    exceeds the 1 GiB audit sandbox at r=13 on the heaviest sampled
    profiles (~742k states); this encoding preserves the exact
    traversal, so len(memo) (the per-record "states" count) and all
    verdicts are unchanged. Equivalence with the verbatim engine and
    the committed JS records is re-verified live by L1/L2 every run.
    """
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
            if sum(counts[m * r:(m + 1) * r]):
                occ |= 1 << m
        maximal = False
        for i in range(1, k + 1):
            if occ & ~star[i]:
                continue
            t = 0
            for m in range(natoms):
                if (star[i] >> m) & 1:
                    t += sum(counts[m * r:(m + 1) * r])
            if t == sizes[i - 1]:
                maximal = True
                break
        if maximal:
            loser = mover
            ba = bytearray(counts)
            ba[loser::r] = bytes(natoms)
            ncounts = bytes(ba)
            new_active = active & ~(1 << loser)
            if new_active.bit_count() == 1:
                sv = new_active
            else:
                nm = next_active_mask(loser, r, new_active)
                sv, _fl = rec(ncounts, nm, new_active)
            out = (sv, 1 << loser)
        else:
            svm = 0
            flm = 0
            nm = next_active_mask(mover, r, active)
            for m in range(1, 1 << k):
                mi = m - 1
                o = mi * r
                cap = atoms[mi] - sum(counts[o:o + r])
                if cap <= 0:
                    continue
                if any(
                    (occ & ~star[i]) == 0 and (star[i] >> mi) & 1
                    for i in range(1, k + 1)
                ):
                    p = o + mover
                    bumped = (
                        counts[:p]
                        + bytes((counts[p] + 1,))
                        + counts[p + 1:]
                    )
                    s2, f = rec(bumped, nm, active)
                    svm |= s2
                    flm |= f
            out = (svm, flm)
        memo[key] = out
        return out

    try:
        sv, fl = rec(bytes(natoms * r), 0, (1 << r) - 1)
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
# K0906 constants and pins
# ---------------------------------------------------------------------------

AUDIT_NAME = "theorem_j_audit.json"
CAP = 10
RS = (9, 10, 11, 12, 13)
N_PROFILES = 15863

PACKED_COLUMNS = {
    9: ("remo-k-branch-cap10-r9-boundary-20261117",
        "js_cap10_r9.packed.jsonl"),
    10: ("remo-k-branch-cap10-r10-boundary-20261117",
         "js_cap10_r10.packed.jsonl"),
    11: ("remo-k-branch-cap10-r11-boundary-20261117",
         "js_cap10_r11.packed.jsonl"),
    12: ("remo-k-branch-cap10-r12-boundary-20261117",
         "js_cap10_r12.packed.jsonl"),
    13: ("remo-k-branch-cap10-r13-invariance-20261117",
         "js_cap10_r13.packed.jsonl"),
}

# machine-check pins (each re-derived below; a mismatch aborts the run)
PIN_BURNSIDE = (84494, 3478, 125, 15863)
PIN_MAXC = {"le8": 4330, "eq9": 4205, "eq10": 7328}
PIN_J1_ELIGIBLE = 71987
PIN_J1_SIGMA_VIOLATIONS = 0
PIN_J2_COMPARISONS = 79315
PIN_J3_COMPARISONS = 60454
PIN_J4 = {"fl_r13_r10": 7328, "fl_r13_r9": 11533, "sv_r13_r9": 7328}
PIN_SG_MAX_STATES = {12: 666030, 13: 741630}

# live pins
PIN_CAP = {4: 117, 5: 346, 7: 2048}
PIN_J5_JUDGMENTS = 6144
PIN_J5B_JUDGMENTS = 1038
PIN_J6 = {"total": 2041, "changed": 2022}
PIN_J7A_PROFILES = 56
PIN_J7B_PROFILES = 22
PIN_J8_PROFILES = 14
PIN_J8_JUDGMENTS = 42
PIN_J8_MAX_N = 17
PIN_L9_PAIRS = 195
# filled in after the first pinned run (structural assertions are
# independent of these pins)
PIN_J9_CANONICAL_PLAYS = 9684
PIN_J9_SPECIAL_PLAYS = 2581
PIN_J9_RIGID_VIOLATIONS = 91


def _exp_dir():
    return os.path.dirname(os.path.abspath(__file__))


def load_packed(r):
    """Committed packed column: [i, sv_mask, fl_mask, states] per line."""
    d, name = PACKED_COLUMNS[r]
    path = os.path.join(_exp_dir(), "..", d, "output", name)
    out = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            i, sv, fl, states = json.loads(line)
            out.append({"i": i, "sv": sv, "fl": fl, "states": states})
    return out


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def fl_prediction(atoms, k, r):
    """Lemma FL: fl(r) = {C_i mod r} as a label bitmask."""
    pred = 0
    for c in profile_sizes(atoms, k):
        pred |= 1 << (c % r)
    return pred


# ---------------------------------------------------------------------------
# cascade simulator (LC1/LC2) - independent implementation of the proof's
# L1/L2 objects. Does NOT call check_profile: the special batteries have
# empty singleton atoms.
# ---------------------------------------------------------------------------


def sim_stars(k):
    """star[i] = bitmask over atom indices m-1 of atoms containing branch i."""
    star = []
    for i in range(1, k + 1):
        m2 = 0
        for m in range(1, 1 << k):
            if (m >> (i - 1)) & 1:
                m2 |= 1 << (m - 1)
        star.append(m2)
    return star


def _board_facts(atoms, k, star, stones):
    """stones[mi] = collection (list) of player labels on atom mi."""
    natoms = (1 << k) - 1
    occ = 0
    totals = [0] * k
    for mi in range(natoms):
        n = len(stones[mi])
        if n:
            occ |= 1 << mi
            for i in range(k):
                if (star[i] >> mi) & 1:
                    totals[i] += n
    return occ, totals


def first_event_plays(atoms, k):
    """Enumerate phase-1 plays (each player 0..t-1 places one stone) that
    reach the FIRST event, plus the dead-end plays are simply not recorded.
    Returns a list of play tuples (play[p] = atom index of player p); the
    event depth len(play) equals C_Y of the saturated branch (L1)."""
    sizes = profile_sizes(atoms, k)
    natoms = (1 << k) - 1
    star = sim_stars(k)
    M = max(sizes)
    out = []

    def rec(stones, depth, play):
        occ, totals = _board_facts(atoms, k, star, stones)
        sat = -1
        for i in range(k):
            if (occ & ~star[i]) == 0 and totals[i] == sizes[i]:
                sat = i
                break
        if sat >= 0:
            out.append(tuple(play))
            return
        if depth >= M:
            return  # L1: no event can occur at depth > M
        for mi in range(natoms):
            if len(stones[mi]) >= atoms[mi]:
                continue
            if any((occ & ~star[i]) == 0 and (star[i] >> mi) & 1
                   for i in range(k)):
                stones[mi].append(depth)
                play.append(mi)
                rec(stones, depth + 1, play)
                play.pop()
                stones[mi].pop()

    stones = [[] for _ in range(natoms)]
    rec(stones, 0, [])
    return out


def cascade_result(atoms, k, play, r):
    """Post-event cascade (LC2). Returns a NORMALIZED result:

      ("term", sigma)                     terminal survivor label
      ("state", counts, active, mover)    counts[mi] = sorted tuple of
                                          player labels on atom mi,
                                          active = frozenset of labels,
                                          mover = next mover label

    All labels in the normalized result are < C_Y = len(play): the
    cascade eats every phantom (stone-less) label before it can stop
    (removing a phantom does not change the board, so maximality
    persists), and stone-holders are labels < C_Y. next_active skips
    inactive labels, so the mover is the same cyclic successor inside
    {0..C_Y-1} for every r >= C_Y (L3 closure)."""
    natoms = (1 << k) - 1
    star = sim_stars(k)
    cyc = len(play)
    stones = [[] for _ in range(natoms)]
    for p, mi in enumerate(play):
        stones[mi].append(p)
    active = set(range(r))
    loser = cyc % r
    while True:
        for mi in range(natoms):
            if loser in stones[mi]:
                stones[mi] = [x for x in stones[mi] if x != loser]
        active.discard(loser)
        if len(active) == 1:
            return ("term", next(iter(active)))
        occ, totals = _board_facts(atoms, k, star, stones)
        sat = any((occ & ~star[i]) == 0 and totals[i] == profile_sizes(
            atoms, k)[i] for i in range(k))
        if not sat:
            mover = next_active(loser, r, frozenset(active))
            counts = tuple(tuple(sorted(stones[mi])) for mi in range(natoms))
            return ("state", counts, frozenset(active), mover)
        loser = next_active(loser, r, frozenset(active))


def rigid_expectation(atoms, k, play):
    """Lemma C1' rigid form for the canonical domain (all singleton atoms
    nonempty): the cascade stops exactly at P_0 after the phantom prefix.
    Returns the expected normalized result, or None when the expectation
    is not the rigid one (never happens for canonical profiles)."""
    cyc = len(play)
    natoms = (1 << k) - 1
    if cyc == 1:
        return ("term", 0)
    if cyc == 2:
        return ("term", 1)
    stones = [[] for _ in range(natoms)]
    for p, mi in enumerate(play):
        if p >= 1:
            stones[mi].append(p)
    counts = tuple(tuple(sorted(stones[mi])) for mi in range(natoms))
    active = frozenset(range(1, cyc))
    return ("state", counts, active, 1)


def sub_game_sv(atoms, k, r, counts, active, mover, budget=2_000_000):
    """Independent sub-game DFS from a post-cascade state (L3/L4 gluing).
    counts[mi] = sorted tuple of player labels (with multiplicity) on
    atom mi; active = frozenset; mover = label. Returns the survivor
    label bitmask reachable from the state (0 for dead-end states)."""
    natoms = (1 << k) - 1
    star = sim_stars(k)
    sizes = profile_sizes(atoms, k)
    memo = {}
    nodes = [budget]

    def board_maximal(counts):
        occ = 0
        totals = [0] * k
        for mi in range(natoms):
            n = len(counts[mi])
            if n:
                occ |= 1 << mi
                for i in range(k):
                    if (star[i] >> mi) & 1:
                        totals[i] += n
        for i in range(k):
            if (occ & ~star[i]) == 0 and totals[i] == sizes[i]:
                return True
        return False

    def rec(counts, active, mover):
        key = (counts, active, mover)
        got = memo.get(key)
        if got is not None:
            return got
        nodes[0] -= 1
        if nodes[0] < 0:
            raise Budget("subgame budget")
        if board_maximal(counts):
            # cascade inside the sub-game (same loop as cascade_result)
            loser = mover
            while True:
                counts2 = tuple(tuple(x for x in counts[mi] if x != loser)
                                for mi in range(natoms))
                active2 = active - {loser}
                if len(active2) == 1:
                    out = 1 << next(iter(active2))
                    break
                if not board_maximal(counts2):
                    mover2 = next_active(loser, r, active2)
                    out = rec(counts2, active2, mover2)
                    break
                counts = counts2
                active = active2
                loser = next_active(loser, r, active2)
        else:
            out = 0
            occ = 0
            for mi in range(natoms):
                if counts[mi]:
                    occ |= 1 << mi
            nm = next_active(mover, r, active)
            for mi in range(natoms):
                if len(counts[mi]) >= atoms[mi]:
                    continue
                if any((occ & ~star[i]) == 0 and (star[i] >> mi) & 1
                       for i in range(k)):
                    counts2 = list(counts)
                    inner = list(counts2[mi])
                    inner.append(mover)
                    counts2[mi] = tuple(sorted(inner))
                    out |= rec(tuple(counts2), active, nm)
        memo[key] = out
        return out

    return rec(tuple(tuple(c) for c in counts), frozenset(active), mover)


# ---------------------------------------------------------------------------
# batteries
# ---------------------------------------------------------------------------


def k2_battery():
    """k=2 canonical profiles, sizes <= 6 (56 profiles)."""
    seen = set()
    out = []
    for a in range(1, 7):
        for b in range(1, 7):
            for s in range(0, 7 - max(a, b)):
                rep = min((a, b), (b, a))
                key = (rep[0], rep[1], s)
                if key in seen:
                    continue
                seen.add(key)
                out.append((rep[0], rep[1], s))
    return out


def k4_battery():
    """k=4 battery: 15 singleton-only profiles (sizes multiset from
    {1,2,3}) + 7 chain profiles (gamma in {1,2}, maxC <= 6)."""
    out = []
    for a in range(1, 4):
        for b in range(1, a + 1):
            for c in range(1, b + 1):
                for d in range(1, c + 1):
                    atoms = [0] * 15
                    atoms[0] = a
                    atoms[1] = b
                    atoms[3] = c
                    atoms[7] = d
                    out.append(tuple(atoms))
    chain = [((6, 2, 2, 2), 1), ((5, 3, 2, 2), 1), ((4, 4, 2, 2), 1),
             ((4, 3, 3, 2), 1), ((3, 3, 3, 3), 1), ((4, 2, 2, 2), 1),
             ((3, 3, 2, 2), 1)]
    for sizes, gamma in chain:
        out.append(chain_profile(sizes, gamma, 4))
    return out


def j8_anchor_battery():
    """Size 11/12 anchors (14 k=3 profiles, total capacity N <= 16)."""
    out = []
    out.append(chain_profile((11, 1, 1), 0, 3))
    out.append(chain_profile((11, 2, 1), 0, 3))
    out.append(chain_profile((11, 2, 2), 0, 3))
    out.append(chain_profile((11, 3, 2), 0, 3))
    out.append(chain_profile((11, 3, 3), 1, 3))
    out.append((10, 1, 1, 1, 0, 0, 0))
    out.append((3, 2, 5, 1, 3, 1, 0))
    out.append(chain_profile((12, 1, 1), 0, 3))
    out.append(chain_profile((12, 2, 1), 0, 3))
    out.append(chain_profile((12, 2, 2), 0, 3))
    out.append(chain_profile((12, 3, 2), 0, 3))
    out.append(chain_profile((12, 3, 3), 1, 3))
    out.append((11, 1, 1, 1, 0, 0, 0))
    out.append((3, 2, 5, 1, 4, 1, 0))
    for atoms in out:
        sizes = profile_sizes(atoms, 3)
        assert max(sizes) in (11, 12), sizes
        assert min(sizes) >= 1
        assert sum(atoms) <= PIN_J8_MAX_N, sum(atoms)
        check_profile(atoms, 3)
    return out


def special_battery_k3():
    """k=3, sizes <= 4, at least one singleton atom EMPTY, all C_i >= 1,
    canonical under S_3 (194 profiles). The C1' capacity inequality
    fails here; Theorem J does not."""
    seen = set()
    out = []
    for e1 in range(0, 5):
        for e2 in range(0, 5):
            for s12 in range(0, 5):
                for e3 in range(0, 5):
                    for s13 in range(0, 5):
                        for s23 in range(0, 5):
                            for s123 in range(0, 5):
                                vec = (e1, e2, s12, e3, s13, s23, s123)
                                c1 = e1 + s12 + s13 + s123
                                c2 = e2 + s12 + s23 + s123
                                c3 = e3 + s13 + s23 + s123
                                if max(c1, c2, c3) > 4:
                                    continue
                                if min(c1, c2, c3) < 1:
                                    continue
                                if min(e1, e2, e3) >= 1:
                                    continue
                                rep = orbit_representative(
                                    vec, 3, branch_perms(3))
                                if rep in seen:
                                    continue
                                seen.add(rep)
                                out.append(rep)
    return out


def special_battery_k2():
    """k=2, sizes <= 4, at least one singleton empty, C_i >= 1 (10)."""
    seen = set()
    out = []
    for e1 in range(0, 5):
        for e2 in range(0, 5):
            for s12 in range(0, 5):
                c1 = e1 + s12
                c2 = e2 + s12
                if max(c1, c2) > 4 or min(c1, c2) < 1:
                    continue
                if e1 >= 1 and e2 >= 1:
                    continue
                rep = min((e1, e2, s12), (e2, e1, s12))
                if rep in seen:
                    continue
                seen.add(rep)
                out.append(rep)
    return out


def special_battery_k4():
    """k=4 chain profiles, maxC <= 5, min singleton EMPTY (gamma = min
    size), canonical sorted sizes (55 profiles)."""
    out = []
    for g in range(0, 3):
        for d in range(max(1, g), 6):
            for c in range(d, 6):
                for b in range(c, 6):
                    for a in range(b, 6):
                        sizes = (a, b, c, d)
                        if min(sizes) != g:
                            continue
                        out.append(chain_profile(sizes, g, 4))
    return out


# ---------------------------------------------------------------------------
# machine checks
# ---------------------------------------------------------------------------


def machine_checks():
    profiles = direct_constrained(CAP)
    assert len(profiles) == N_PROFILES
    atoms_to_idx = {atoms: i for i, atoms in enumerate(profiles)}
    sizes_list = [profile_sizes(a, 3) for a in profiles]

    b1 = {}
    b1["burnside"] = list(burnside_fix_counts(CAP))
    assert tuple(b1["burnside"]) == PIN_BURNSIDE
    b1["profiles"] = len(profiles)

    cols = {}
    packed_info = {}
    j0 = {"columns": {}}
    for r in RS:
        cols[r] = load_packed(r)
        d, name = PACKED_COLUMNS[r]
        path = os.path.join(_exp_dir(), "..", d, "output", name)
        packed_info[str(r)] = {
            "path": "%s/output/%s" % (d, name),
            "sha256": sha256_file(path),
            "records": len(cols[r]),
        }
        assert len(cols[r]) == N_PROFILES
        assert all(rec["i"] == j for j, rec in enumerate(cols[r]))
        assert all(rec["states"] > 0 for rec in cols[r])
        j0["columns"][str(r)] = len(cols[r])

    # J1: sv/det constant for r >= max(M,2); sigma <= M-1
    j1 = {"eligible": 0, "violations": 0, "sigma_violations": 0}
    dist = {"le8": 0, "eq9": 0, "eq10": 0}
    for idx, sizes in enumerate(sizes_list):
        M = max(sizes)
        if M <= 8:
            dist["le8"] += 1
        elif M == 9:
            dist["eq9"] += 1
        else:
            dist["eq10"] += 1
        base = max(M, 2)
        det0 = None
        sv0 = None
        for r in RS:
            if r < base:
                continue
            j1["eligible"] += 1
            rec = cols[r][idx]
            det = rec["sv"].bit_count() == 1
            if det0 is None:
                det0 = det
                sv0 = rec["sv"]
            elif det != det0 or rec["sv"] != sv0:
                j1["violations"] += 1
            if rec["sv"] >> M:
                j1["sigma_violations"] += 1  # any survivor label >= M
    assert dist == PIN_MAXC, dist
    assert j1["eligible"] == PIN_J1_ELIGIBLE
    assert j1["violations"] == 0
    assert j1["sigma_violations"] == PIN_J1_SIGMA_VIOLATIONS
    j1["maxc_distribution"] = dist

    # J2: fl == {C_i mod r} on every committed record
    j2 = {"comparisons": 0, "violations": 0}
    for idx, sizes in enumerate(sizes_list):
        for r in RS:
            j2["comparisons"] += 1
            pred = 0
            for c in sizes:
                pred |= 1 << (c % r)
            if cols[r][idx]["fl"] != pred:
                j2["violations"] += 1
    assert j2["comparisons"] == PIN_J2_COMPARISONS
    assert j2["violations"] == 0

    # J3: fl constant == {C_i} for r > M
    j3 = {"comparisons": 0, "violations": 0}
    for idx, sizes in enumerate(sizes_list):
        M = max(sizes)
        pred = 0
        for c in sizes:
            pred |= 1 << c
        for r in RS:
            if r > M:
                j3["comparisons"] += 1
                if cols[r][idx]["fl"] != pred:
                    j3["violations"] += 1
    assert j3["comparisons"] == PIN_J3_COMPARISONS
    assert j3["violations"] == 0

    # J4: K0902 ARITH set equalities
    def diffset(ra, rb, field):
        return {i for i in range(N_PROFILES)
                if cols[ra][i][field] != cols[rb][i][field]}

    maxc10 = {i for i, s in enumerate(sizes_list) if max(s) == 10}
    maxc9p = {i for i, s in enumerate(sizes_list) if max(s) >= 9}
    d_fl_10 = diffset(13, 10, "fl")
    d_fl_9 = diffset(13, 9, "fl")
    d_sv_9 = diffset(13, 9, "sv")
    j4 = {
        "fl_diff_r13_r10": len(d_fl_10),
        "fl_diff_r13_r10_is_maxc10": d_fl_10 == maxc10,
        "fl_diff_r13_r9": len(d_fl_9),
        "fl_diff_r13_r9_is_maxc9p": d_fl_9 == maxc9p,
        "sv_diff_r13_r9": len(d_sv_9),
        "sv_diff_r13_r9_is_maxc10": d_sv_9 == maxc10,
        "other_sv_diffs": {str(rb): len(diffset(13, rb, "sv"))
                           for rb in (10, 11, 12)},
        # det is a function of the sv mask, so the det difference sets
        # coincide with the sv difference sets above
    }
    assert j4["fl_diff_r13_r10"] == PIN_J4["fl_r13_r10"]
    assert j4["fl_diff_r13_r9"] == PIN_J4["fl_r13_r9"]
    assert j4["sv_diff_r13_r9"] == PIN_J4["sv_r13_r9"]
    assert j4["fl_diff_r13_r10_is_maxc10"]
    assert j4["fl_diff_r13_r9_is_maxc9p"]
    assert j4["sv_diff_r13_r9_is_maxc10"]
    assert all(v == 0 for v in j4["other_sv_diffs"].values())
    assert all(v == 0 for v in j4["other_sv_diffs"].values())

    # SG: anti-overclaim guard
    sg = {"max_states": {str(r): max(rec["states"] for rec in cols[r])
                         for r in RS}}
    assert sg["max_states"]["12"] == PIN_SG_MAX_STATES[12]
    assert sg["max_states"]["13"] == PIN_SG_MAX_STATES[13]
    assert sg["max_states"]["12"] != sg["max_states"]["13"]

    return {
        "packed_columns": packed_info,
        "B1": b1,
        "J0": j0,
        "J1": j1,
        "J2": j2,
        "J3": j3,
        "J4": j4,
        "SG": sg,
    }, profiles, sizes_list, cols, atoms_to_idx


# ---------------------------------------------------------------------------
# live checks
# ---------------------------------------------------------------------------


def r_triple(M):
    return sorted({max(M, 2), max(M, 2) + 1, max(M, 2) + 2})


def check_j_triple(atoms, k, M, verdicts):
    """Theorem J predictions for one profile across its r triple."""
    det0 = None
    sv0 = None
    for r, v in verdicts.items():
        pred = fl_prediction(atoms, k, r)
        assert v["first_losers"] == sorted(p for p in range(r)
                                           if (pred >> p) & 1), \
            (atoms, k, r, v, pred)
        assert v["survivors"] == [p for p in v["survivors"] if p <= M - 1]
        if det0 is None:
            det0 = v["determined"]
            sv0 = tuple(v["survivors"])
        else:
            assert v["determined"] == det0
            assert tuple(v["survivors"]) == sv0
    return 1 if det0 else 0


def live_checks(profiles, cols, atoms_to_idx):
    live = {}

    # L0: cap<=7 x r=13 mask twin == committed r=13 records
    prof7 = direct_constrained(7)
    assert len(prof7) == PIN_CAP[7]
    n = 0
    for atoms in prof7:
        v, states = mask_verdict(atoms, 3, 13)
        rec = cols[13][atoms_to_idx[atoms]]
        assert (v["determined"],
                v["survivors"]) == (rec["sv"].bit_count() == 1,
                                    [p for p in range(13)
                                     if (rec["sv"] >> p) & 1]), atoms
        assert v["first_losers"] == [p for p in range(13)
                                     if (rec["fl"] >> p) & 1], atoms
        n += 1
    live["L0"] = {"profiles": n, "r": 13}
    print("L0: cap<=7 x r=13 mask twin == committed records: %d ok" % n)

    # J5: cap<=7 x r triple
    judgments = 0
    for atoms in prof7:
        M = max(profile_sizes(atoms, 3))
        verdicts = {}
        for r in r_triple(M):
            v, _ = mask_verdict(atoms, 3, r)
            verdicts[r] = v
            judgments += 1
        check_j_triple(atoms, 3, M, verdicts)
    assert judgments == PIN_J5_JUDGMENTS
    live["J5"] = {"judgments": judgments}
    print("J5: cap<=7 x r-triple sv/det invariant + FL + sigma: %d ok"
          % judgments)

    # J5b: cap<=5 verbatim engine == mask twin
    prof5 = direct_constrained(5)
    assert len(prof5) == PIN_CAP[5]
    judgments = 0
    for atoms in prof5:
        M = max(profile_sizes(atoms, 3))
        for r in r_triple(M):
            v1, _ = region_verdict(atoms, 3, r)
            v2, _ = mask_verdict(atoms, 3, r)
            assert verdict_triple(v1) == verdict_triple(v2), (atoms, r)
            judgments += 1
    assert judgments == PIN_J5B_JUDGMENTS
    live["J5b"] = {"judgments": judgments}
    print("J5b: cap<=5 verbatim == mask twin: %d ok" % judgments)

    # J6: sharpness probe r = M-1
    total = 0
    changed = 0
    witness = None
    for atoms in prof7:
        M = max(profile_sizes(atoms, 3))
        if M < 3:
            continue
        total += 1
        v1, _ = mask_verdict(atoms, 3, M - 1)
        v2, _ = mask_verdict(atoms, 3, M)
        if (v1["determined"], v1["survivors"]) != (v2["determined"],
                                                   v2["survivors"]):
            changed += 1
            if witness is None:
                witness = {"atoms": list(atoms), "M": M,
                           "r_eq_M_1": v1, "r_eq_M": v2}
    assert total == PIN_J6["total"] and changed == PIN_J6["changed"]
    live["J6"] = {"profiles": total, "changed": changed, "witness": witness}
    print("J6: r=M-1 sharpness: %d/%d profiles change sv/det" % (changed,
                                                                total))

    # J7a: k=2 battery
    bat2 = k2_battery()
    assert len(bat2) == PIN_J7A_PROFILES
    for atoms in bat2:
        M = max(profile_sizes(atoms, 2))
        verdicts = {}
        for r in r_triple(M):
            v, _ = mask_verdict(atoms, 2, r)
            verdicts[r] = v
        check_j_triple(atoms, 2, M, verdicts)
    live["J7a"] = {"profiles": len(bat2)}
    print("J7a: k=2 battery Theorem J ok: %d profiles" % len(bat2))

    # J7b: k=4 battery
    bat4 = k4_battery()
    assert len(bat4) == PIN_J7B_PROFILES
    for atoms in bat4:
        M = max(profile_sizes(atoms, 4))
        verdicts = {}
        for r in r_triple(M):
            v, _ = mask_verdict(atoms, 4, r)
            verdicts[r] = v
        check_j_triple(atoms, 4, M, verdicts)
    live["J7b"] = {"profiles": len(bat4)}
    print("J7b: k=4 battery Theorem J ok: %d profiles" % len(bat4))

    # J8: size 11/12 anchors (r = M, M+1, M+2; r=13,14 outside all
    # committed columns)
    bat8 = j8_anchor_battery()
    assert len(bat8) == PIN_J8_PROFILES
    judgments = 0
    for atoms in bat8:
        M = max(profile_sizes(atoms, 3))
        verdicts = {}
        for r in (M, M + 1, M + 2):
            v, _ = mask_verdict(atoms, 3, r, budget=50_000_000)
            verdicts[r] = v
            judgments += 1
        check_j_triple(atoms, 3, M, verdicts)
        # constant fl for r > M
        pred = 0
        for c in profile_sizes(atoms, 3):
            pred |= 1 << c
        for r in (M + 1, M + 2):
            assert verdicts[r]["first_losers"] == \
                [p for p in range(r) if (pred >> p) & 1], (atoms, r)
    assert judgments == PIN_J8_JUDGMENTS
    live["J8"] = {"profiles": len(bat8), "judgments": judgments,
                  "max_r": 14, "max_N": max(sum(a) for a in bat8)}
    print("J8: size 11/12 anchors Theorem J ok: %d profiles x 3 r" % len(bat8))

    # J9: cascade simulator (LC1/LC2 + C1' + play-wise FL)
    canon = [(a, 3) for a in direct_constrained(5)]
    special = ([(a, 3) for a in special_battery_k3()]
               + [(a, 2) for a in special_battery_k2()]
               + [(a, 4) for a in special_battery_k4()])
    canon_plays = 0
    special_plays = 0
    rigid_violations = 0
    rigid_witness = None
    fl_witness = None
    special_sv_profiles = 0
    for tag, battery in (("canonical", canon), ("special", special)):
        for atoms, k in battery:
            M = max(profile_sizes(atoms, k))
            sizes = profile_sizes(atoms, k)
            plays = first_event_plays(atoms, k)
            rvals = sorted({max(M, 2), M + 1, M + 2})
            fl_by_r = {}
            for play in plays:
                # structural L1: depth = C_Y is a branch capacity
                assert len(play) in sizes, (atoms, play)
                cyc = len(play)
                results = {}
                for r in rvals:
                    results[r] = cascade_result(atoms, k, play, r)
                vals = list(results.values())
                for other in vals[1:]:
                    assert other == vals[0], (atoms, k, play, results)
                # play-wise FL contribution: fl = {C_Y mod r}
                for r in results:
                    assert (cyc % r) in {c % r for c in sizes}
                if tag == "canonical":
                    canon_plays += 1
                    exp = rigid_expectation(atoms, k, play)
                    if vals[0] != exp:
                        rigid_violations += 1
                        assert False, ("C1' violated on canonical profile",
                                       atoms, play, vals[0], exp)
                else:
                    special_plays += 1
                    exp = rigid_expectation(atoms, k, play)
                    if vals[0] != exp:
                        rigid_violations += 1
                        if rigid_witness is None:
                            rigid_witness = {"atoms": list(atoms),
                                             "k": k, "play": list(play),
                                             "result": repr(vals[0])}
            # root-level FL re-derivation (L4). Canonical domain
            # (e_j >= 1): fl(r) = {C_i mod r} - the reachability step
            # needs e_j >= 1 (a foreign branch j cannot saturate on the
            # shared atoms: their capacity C_j - e_j < C_j). Special
            # battery: the refined Theorem J(ii') form fl(r) =
            # {c mod r : c in E} with the FIRST-SATURABLE capacity set E.
            for r in rvals:
                fl_sim = {len(play) % r for play in plays}
                fl_by_r[r] = fl_sim
                if tag == "canonical":
                    assert fl_sim == {c % r for c in sizes}, \
                        (atoms, k, r, fl_sim)
                else:
                    assert fl_sim <= {c % r for c in sizes}, \
                        (atoms, k, r, fl_sim)
            E = fl_by_r[rvals[-1]]  # rvals[-1] > M: no wraparound
            for r in rvals:
                assert fl_by_r[r] == {c % r for c in E}, (atoms, k, r)
            if tag == "special" and E != set(sizes) and fl_witness is None:
                fl_witness = {"atoms": list(atoms), "k": k,
                              "sizes": list(sizes), "E": sorted(E),
                              "note": "Lemma FL reachability fails at "
                                      "e_j = 0: fl != {C_i mod r}"}
            # Theorem J (i)/(iii) in the WIDE domain: sv/det via
            # simulator + sub-game DFS must be r-invariant and every
            # survivor label <= M-1.
            if tag == "special":
                sv_by_r = {}
                for r in rvals:
                    svm = 0
                    for play in plays:
                        res = cascade_result(atoms, k, play, r)
                        if res[0] == "term":
                            svm |= 1 << res[1]
                        else:
                            svm |= sub_game_sv(atoms, k, r, res[1],
                                               res[2], res[3])
                    sv_by_r[r] = svm
                for other in list(sv_by_r.values())[1:]:
                    assert other == sv_by_r[rvals[0]], (atoms, k, sv_by_r)
                assert not (sv_by_r[rvals[0]] >> M), (atoms, k)
                special_sv_profiles += 1
    live["J9"] = {
        "canonical_profiles": len(canon),
        "special_profiles": len(special),
        "canonical_plays": canon_plays,
        "special_plays": special_plays,
        "rigid_violations": rigid_violations,
        "rigid_violation_witness": rigid_witness,
        "fl_domain_witness": fl_witness,
        "special_sv_profiles": special_sv_profiles,
    }
    if PIN_J9_CANONICAL_PLAYS >= 0:
        assert canon_plays == PIN_J9_CANONICAL_PLAYS
    if PIN_J9_SPECIAL_PLAYS >= 0:
        assert special_plays == PIN_J9_SPECIAL_PLAYS
    if PIN_J9_RIGID_VIOLATIONS >= 0:
        assert rigid_violations == PIN_J9_RIGID_VIOLATIONS
    assert rigid_violations > 0, "special battery must contain C1' " \
        "counterexamples (e_j = 0 capacity leak)"
    assert fl_witness is not None, "special battery must contain an " \
        "fl domain witness (Lemma FL reachability needs e_j >= 1)"
    print("J9: cascade simulator r-invariance ok: %d canonical + %d "
          "special plays, %d C1' violations (all special), fl domain "
          "witness %s" % (canon_plays, special_plays, rigid_violations,
                          fl_witness["sizes"]))

    # L9: gluing (simulator + sub-game DFS == mask twin == verbatim)
    dom = [(a, 3) for a in direct_constrained(4)] \
        + [(a, 2) for a in k2_battery()] \
        + [(a, 4) for a in k4_battery()]
    assert len(dom) == PIN_L9_PAIRS
    pairs = 0
    for atoms, k in dom:
        M = max(profile_sizes(atoms, k))
        r = max(M, 2)
        twin, _ = mask_verdict(atoms, k, r)
        verb, _ = region_verdict(atoms, k, r)
        assert verdict_triple(twin) == verdict_triple(verb), (atoms, r)
        sv_sim = 0
        fl_sim = set()
        for play in first_event_plays(atoms, k):
            fl_sim.add(len(play) % r)
            res = cascade_result(atoms, k, play, r)
            if res[0] == "term":
                sv_sim |= 1 << res[1]
            else:
                sv_sim |= sub_game_sv(atoms, k, r, res[1], res[2], res[3])
        sv_set = {p for p in range(r) if (sv_sim >> p) & 1}
        assert sv_set == set(twin["survivors"]), (atoms, r, sv_set,
                                                  twin["survivors"])
        assert fl_sim == set(twin["first_losers"]), (atoms, r)
        assert (len(sv_set) == 1) == twin["determined"]
        pairs += 1
    live["L9"] = {"pairs": pairs, "r_domain": "max(M,2)"}
    print("L9: gluing simulator+subgame == twin == verbatim: %d pairs ok"
          % pairs)

    return live


# ---------------------------------------------------------------------------
# assemble / serialize / run
# ---------------------------------------------------------------------------


def assemble_audit():
    machine, profiles, sizes_list, cols, atoms_to_idx = machine_checks()
    live = live_checks(profiles, cols, atoms_to_idx)
    audit = {
        "name": "theorem_j_audit",
        "verifier_sha256": sha256_file(os.path.abspath(__file__)),
        "machine_checks": machine,
        "live_checks": live,
        "pins": {
            "burnside": list(PIN_BURNSIDE),
            "maxc_distribution": PIN_MAXC,
            "j1_eligible": PIN_J1_ELIGIBLE,
            "j2_comparisons": PIN_J2_COMPARISONS,
            "j3_comparisons": PIN_J3_COMPARISONS,
            "j4": PIN_J4,
            "sg_max_states": {str(k): v for k, v in PIN_SG_MAX_STATES.items()},
            "j5_judgments": PIN_J5_JUDGMENTS,
            "j5b_judgments": PIN_J5B_JUDGMENTS,
            "j6": PIN_J6,
            "j7a_profiles": PIN_J7A_PROFILES,
            "j7b_profiles": PIN_J7B_PROFILES,
            "j8": {"profiles": PIN_J8_PROFILES,
                   "judgments": PIN_J8_JUDGMENTS,
                   "max_N": PIN_J8_MAX_N},
            "j9": {"canonical_plays": PIN_J9_CANONICAL_PLAYS,
                   "special_plays": PIN_J9_SPECIAL_PLAYS,
                   "rigid_violations": PIN_J9_RIGID_VIOLATIONS},
            "l9_pairs": PIN_L9_PAIRS,
        },
    }
    return audit


def serialize(audit):
    return json.dumps(audit, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def run():
    audit = assemble_audit()
    b1 = serialize(audit)
    # double serialization of the same audit object must be byte-identical
    assert b1 == serialize(audit)
    out = os.path.join(_exp_dir(), "output", AUDIT_NAME)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "wb") as f:
        f.write(b1)
    print("audit: %s (%d bytes)" % (AUDIT_NAME, len(b1)))
    print("audit sha256: %s" % hashlib.sha256(b1).hexdigest())
    print("ALL THEOREM J CHECKS PASSED")


if __name__ == "__main__":
    run()
