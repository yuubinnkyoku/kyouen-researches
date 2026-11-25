#!/usr/bin/env python3
"""K0886 audit: 3-branch REMO determinacy size boundary cap<=15 for r=3.

Self-contained verifier. Deterministic (no randomness, no wall clock, no
network). Python 3.11+ / stdlib only.

Extends Theorem H14 (K0883, cap<=14, r=3: exactly 52 non-collapsing
keys) to cap<=15. The canonical cap<=15 profile enumeration (189,864
orbits, S_3-canonicalized atom vectors) is swept once with the committed
JavaScript mask engine (mask_engine_fast.js, the K0876 lineage engine)
at r=3; the records are committed in the packed publication format
([i, sv_mask, fl_mask, states] - same format as the K0876/K0882/K0883
publications; atoms are re-derived from the canonical enumeration
inside this verifier).

Main finite claims checked here (cap<=15, r=3, complete enumeration):

  - The non-collapsing (mixed) keys are exactly 110: the Theorem H14 52
    keys plus 58 NEW non-collapsing keys, each containing a size-15
    branch (680 keys contain a size-15 branch; 58 of them are mixed).
    The 14-generation of new keys does NOT stop at 14: new
    non-collapsing keys keep appearing at the size-15 boundary
    (15 == 0 mod 3, the same residue as 9).
  - The gamma windows of the new (14,14,15)/(14,15,15) families extend
    to 0..9 (all previously known failing-key families had gamma
    windows <= 5), and the possible survivor set {0,1} appears on the
    non-determined side for the first time (at cap<=14 the possible
    survivor sets were contained in {{1,2},{0,1,2}}).
  - The order-preserving subsequence property: the canonical cap<=14
    list D_14 embeds into D_15, and at the mapped positions the
    committed cap<=15 records reproduce ALL 123,272 published K0883 r=3
    packed records byte-for-byte (cross-artifact, sha256-pinned).
  - The per-key det/ndet partition of the 22 theorem-H keys equals the
    K0876 audit sweeps.r3.failing_partitions, and the partition of the
    52 theorem-H14 keys equals the K0883 audit mixed_partition (both
    sha256-pinned cross-reads).
  - Residue lens (K0872): every mixed key has first-loser residue pair
    {0,2}; all 525 one-residue and 525 three-residue keys collapse;
    2,010 two-residue keys contain exactly the 110 mixed keys.
  - Lemma FL (possible first losers == {C_i mod 3}): 0 violations over
    all 189,864 cap<=15 profiles (extends the K0875/K0882/K0883
    observations).

Live engine re-checks (not part of the audit bytes): verbatim region
engine == Python mask twin == committed JS records on the full cap<=7
domain (2,048 verdicts) and on a stride-32 sample of D_15 (5,934
verdicts); the 44 K0862 published witnesses re-run with the verbatim
engine and cross-checked against the committed records.
"""

import gzip
import hashlib
import json
import os
import sys

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
# constants (machine-extracted; sources noted per constant)
# ---------------------------------------------------------------------------

CAP = 15
R = 3
RECORDS_EXPECTED = 189864

# Burnside / enumeration expectation for cap<=15 (fix counts over the
# S_3 action on the 7-atom vectors, computed with burnside_fix_counts).
BURNSIDE_15 = {"fix_id": 1074198, "fix_trans": 21414, "fix_cyc": 372,
               "orbits": 189864}

# Committed packed sweep records sha256. The joined publication blob
# (output/js_cap15_r3.packed.jsonl) exceeds the pushable single-file
# size, so it is committed as three line-aligned parts (repo precedent:
# the n11 certificate part1of2/part2of2 pattern). The parts join
# byte-exactly: sha256(part1 || part2 || part3) == COMMITTED_PACKED_SHA256.
COMMITTED_PACKED_SHA256 = (
    "7c44da46cc65fbc9a88b93c2e26b2a18531738a7da5e5fcce084d5966c002db4"
)
COMMITTED_PACKED_PART1_SHA256 = (
    "ddda26c93cfc7bc6830f0f6f8a338f854e0cd7b25b6bc598489a8662381b1b34"
)
COMMITTED_PACKED_PART2_SHA256 = (
    "2c30fe0bcf39330b1112deea71b913c5bcf79e2eaa16c0525ca67b3bea44a2d7"
)
COMMITTED_PACKED_PART3_SHA256 = (
    "efa6b55d113378bf7c5ae454882612749b160565ee184a9bfe12c3cabfce1e1f"
)

# Cross-artifact pins (published K0883 artifacts on main).
K0883_R3_PACKED_P1_PATH = os.path.join(
    "..", "remo-k-branch-cap14-boundary-20261116", "output",
    "js_cap14_r3.packed.jsonl.part1of2",
)
K0883_R3_PACKED_P2_PATH = os.path.join(
    "..", "remo-k-branch-cap14-boundary-20261116", "output",
    "js_cap14_r3.packed.jsonl.part2of2",
)
K0883_R3_PACKED_JOINED_SHA256 = (
    "710f328936340c2a2ab4316cde4316942a677207dd29ec1dc52af7c9cb786644"
)
K0883_R3_PACKED_PART1_SHA256 = (
    "f627814d1c8b484d5aab36f6054005b757e49f3e53f491c141e5d9fa5dad5d5d"
)
K0883_R3_PACKED_PART2_SHA256 = (
    "7848e20cfc142db1e3e8fbb754503c15405ef57af5f252f5c5fba009c833d6d0"
)
K0883_AUDIT_PATH = os.path.join(
    "..", "remo-k-branch-cap14-boundary-20261116", "output",
    "remo_k_branch_cap14_boundary_audit.json",
)
K0883_AUDIT_SHA256 = (
    "fae365285964deed238a4995479346cc354b316e6661ffe95e03fab08530f501"
)
K0876_AUDIT_PATH = os.path.join(
    "..", "remo-k-branch-cap12-r456-boundary-20261116", "output",
    "remo_k_branch_cap12_r456_boundary_audit.json",
)
K0876_AUDIT_SHA256 = (
    "19b4d833dd87168b7157bf4f66f8a2704e1453c39eb1dc54c608581b2ecd7067"
)

# K0862 published exact 22 non-collapse keys (Theorem H, cap<=10, r=3),
# same constant as the K0875/K0876 verifiers.
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

# 30 NEW non-collapsing keys first appearing at cap<=14 (each contains
# a size-14 branch); census-sorted the same way as the 22 above.
# (theorem H14 = the 22 + these 30; unchanged at cap<=15.)
NEW_FAILING_30 = [
    [2, 3, 14], [2, 3, 14], [2, 9, 14], [2, 9, 14], [3, 14, 14],
    [3, 14, 14], [3, 3, 14], [3, 3, 14], [3, 8, 14], [3, 8, 14],
    [3, 9, 14], [3, 9, 14], [8, 9, 14], [8, 9, 14], [8, 9, 14],
    [8, 9, 14], [8, 9, 14], [8, 9, 14], [9, 14, 14], [9, 14, 14],
    [9, 14, 14], [9, 14, 14], [9, 14, 14], [9, 14, 14], [9, 9, 14],
    [9, 9, 14], [9, 9, 14], [9, 9, 14], [9, 9, 14], [9, 9, 14],
]
NEW_GAMMA_30 = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1,
                0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5]
EXPECTED_FAILING_52_KEYS = sorted(
    EXPECTED_FAILING_22_KEYS
    + [[list(sp), g] for sp, g in zip(NEW_FAILING_30, NEW_GAMMA_30)]
)

# 58 NEW non-collapsing keys first appearing at cap<=15 (each contains
# a size-15 branch); census-sorted the same way as the 30 above.
NEW_FAILING_58 = [
    [2, 8, 15], [2, 8, 15], [2, 14, 15], [2, 14, 15], [3, 8, 15], [3, 8, 15],
    [3, 14, 15], [3, 14, 15], [8, 8, 15], [8, 8, 15], [8, 8, 15], [8, 8, 15],
    [8, 8, 15], [8, 8, 15], [8, 9, 15], [8, 9, 15], [8, 9, 15], [8, 9, 15],
    [8, 9, 15], [8, 9, 15], [8, 14, 15], [8, 14, 15], [8, 14, 15], [8, 14, 15],
    [8, 14, 15], [8, 14, 15], [8, 15, 15], [8, 15, 15], [8, 15, 15], [8, 15, 15],
    [8, 15, 15], [8, 15, 15], [9, 14, 15], [9, 14, 15], [9, 14, 15], [9, 14, 15],
    [9, 14, 15], [9, 14, 15], [14, 14, 15], [14, 14, 15], [14, 14, 15], [14, 14, 15],
    [14, 14, 15], [14, 14, 15], [14, 14, 15], [14, 14, 15], [14, 14, 15], [14, 14, 15],
    [14, 15, 15], [14, 15, 15], [14, 15, 15], [14, 15, 15], [14, 15, 15], [14, 15, 15],
    [14, 15, 15], [14, 15, 15], [14, 15, 15], [14, 15, 15],
]
NEW_GAMMA_58 = [
    0, 1, 0, 1, 0, 1,
    0, 1, 0, 1, 2, 3,
    4, 5, 0, 1, 2, 3,
    4, 5, 0, 1, 2, 3,
    4, 5, 0, 1, 2, 3,
    4, 5, 0, 1, 2, 3,
    4, 5, 0, 1, 2, 3,
    4, 5, 6, 7, 8, 9,
    0, 1, 2, 3, 4, 5,
    6, 7, 8, 9,
]
EXPECTED_FAILING_110_KEYS = sorted(
    EXPECTED_FAILING_52_KEYS
    + [[list(sp), g] for sp, g in zip(NEW_FAILING_58, NEW_GAMMA_58)]
)

# K0862 published 44 minimal witnesses (det/ndet atom pairs per key),
# same constant as the K0876 verifier.
K0862_WITNESSES = {"2,3,8|0": [[1, 1, 1, 7, 0, 1, 0], [1, 1, 0, 5, 1, 2, 0]], "2,3,8|1": [[1, 2, 0, 7, 0, 0, 1], [1, 1, 0, 6, 0, 1, 1]], "2,8,9|0": [[1, 2, 1, 4, 0, 5, 0], [1, 1, 0, 1, 1, 7, 0]], "2,8,9|1": [[1, 3, 0, 4, 0, 4, 1], [1, 1, 0, 2, 0, 6, 1]], "3,3,8|0": [[1, 1, 1, 6, 1, 1, 0], [1, 1, 0, 4, 2, 2, 0]], "3,3,8|1": [[1, 1, 1, 7, 0, 0, 1], [1, 1, 0, 5, 1, 1, 1]], "3,8,8|0": [[1, 1, 1, 1, 1, 6, 0], [1, 1, 2, 3, 0, 5, 0]], "3,8,8|1": [[1, 1, 6, 2, 0, 0, 1], [1, 1, 1, 2, 0, 5, 1]], "3,8,9|0": [[1, 2, 1, 3, 1, 5, 0], [1, 1, 1, 2, 1, 6, 0]], "3,8,9|1": [[1, 3, 0, 3, 1, 4, 1], [1, 1, 0, 1, 1, 6, 1]], "8,8,9|0": [[1, 1, 3, 1, 4, 4, 0], [1, 1, 6, 5, 1, 2, 0]], "8,8,9|1": [[1, 1, 3, 2, 3, 3, 1], [1, 1, 5, 4, 1, 2, 1]], "8,8,9|2": [[1, 1, 2, 1, 3, 3, 2], [1, 1, 4, 3, 1, 2, 2]], "8,8,9|3": [[1, 1, 2, 2, 2, 2, 3], [1, 1, 3, 2, 1, 2, 3]], "8,8,9|4": [[1, 1, 2, 3, 1, 1, 4], [1, 1, 1, 1, 2, 2, 4]], "8,8,9|5": [[1, 1, 2, 4, 0, 0, 5], [1, 1, 1, 2, 1, 1, 5]], "8,9,9|0": [[1, 1, 4, 2, 3, 4, 0], [1, 1, 6, 6, 1, 2, 0]], "8,9,9|1": [[1, 1, 3, 1, 3, 4, 1], [1, 1, 5, 5, 1, 2, 1]], "8,9,9|2": [[1, 1, 3, 2, 2, 3, 2], [1, 1, 4, 4, 1, 2, 2]], "8,9,9|3": [[1, 1, 2, 1, 2, 3, 3], [1, 1, 3, 3, 1, 2, 3]], "8,9,9|4": [[1, 1, 3, 2, 1, 1, 4], [1, 1, 2, 2, 1, 2, 4]], "8,9,9|5": [[1, 1, 3, 3, 0, 0, 5], [1, 1, 1, 1, 1, 2, 5]]}

# cap<=15, r=3 census totals (from the committed records; this file is
# the new published constant).
CENSUS_15 = {
    "keys": 3060,
    "uniform_det": 399,
    "uniform_ndet": 2551,
    "mixed": 110,
    "det_profiles": 23954,
    "ndet_profiles": 165910,
    "total_states": 1545731088,
    "max_states": 120202,
}

# per-key det/ndet/profile partition of the 110 mixed keys (cap<=15, r=3).
MIXED_PARTITION =  {
 "14,14,15|0": {
 "det": 408,
 "ndet": 40,
 "prof": 448
 },
 "14,14,15|1": {
 "det": 324,
 "ndet": 40,
 "prof": 364
 },
 "14,14,15|2": {
 "det": 254,
 "ndet": 40,
 "prof": 294
 },
 "14,14,15|3": {
 "det": 191,
 "ndet": 40,
 "prof": 231
 },
 "14,14,15|4": {
 "det": 140,
 "ndet": 40,
 "prof": 180
 },
 "14,14,15|5": {
 "det": 95,
 "ndet": 40,
 "prof": 135
 },
 "14,14,15|6": {
 "det": 60,
 "ndet": 40,
 "prof": 100
 },
 "14,14,15|7": {
 "det": 34,
 "ndet": 36,
 "prof": 70
 },
 "14,14,15|8": {
 "det": 16,
 "ndet": 32,
 "prof": 48
 },
 "14,14,15|9": {
 "det": 5,
 "ndet": 25,
 "prof": 30
 },
 "14,15,15|0": {
 "det": 436,
 "ndet": 40,
 "prof": 476
 },
 "14,15,15|1": {
 "det": 352,
 "ndet": 40,
 "prof": 392
 },
 "14,15,15|2": {
 "det": 275,
 "ndet": 40,
 "prof": 315
 },
 "14,15,15|3": {
 "det": 212,
 "ndet": 40,
 "prof": 252
 },
 "14,15,15|4": {
 "det": 155,
 "ndet": 40,
 "prof": 195
 },
 "14,15,15|5": {
 "det": 110,
 "ndet": 40,
 "prof": 150
 },
 "14,15,15|6": {
 "det": 70,
 "ndet": 40,
 "prof": 110
 },
 "14,15,15|7": {
 "det": 40,
 "ndet": 40,
 "prof": 80
 },
 "14,15,15|8": {
 "det": 19,
 "ndet": 35,
 "prof": 54
 },
 "14,15,15|9": {
 "det": 6,
 "ndet": 30,
 "prof": 36
 },
 "2,14,15|0": {
 "det": 30,
 "ndet": 11,
 "prof": 41
 },
 "2,14,15|1": {
 "det": 9,
 "ndet": 4,
 "prof": 13
 },
 "2,3,14|0": {
 "det": 6,
 "ndet": 2,
 "prof": 8
 },
 "2,3,14|1": {
 "det": 1,
 "ndet": 1,
 "prof": 2
 },
 "2,3,8|0": {
 "det": 6,
 "ndet": 2,
 "prof": 8
 },
 "2,3,8|1": {
 "det": 1,
 "ndet": 1,
 "prof": 2
 },
 "2,8,15|0": {
 "det": 18,
 "ndet": 5,
 "prof": 23
 },
 "2,8,15|1": {
 "det": 5,
 "ndet": 2,
 "prof": 7
 },
 "2,8,9|0": {
 "det": 18,
 "ndet": 5,
 "prof": 23
 },
 "2,8,9|1": {
 "det": 5,
 "ndet": 2,
 "prof": 7
 },
 "2,9,14|0": {
 "det": 18,
 "ndet": 8,
 "prof": 26
 },
 "2,9,14|1": {
 "det": 5,
 "ndet": 3,
 "prof": 8
 },
 "3,14,14|0": {
 "det": 40,
 "ndet": 12,
 "prof": 52
 },
 "3,14,14|1": {
 "det": 13,
 "ndet": 12,
 "prof": 25
 },
 "3,14,15|0": {
 "det": 50,
 "ndet": 29,
 "prof": 79
 },
 "3,14,15|1": {
 "det": 18,
 "ndet": 20,
 "prof": 38
 },
 "3,3,14|0": {
 "det": 7,
 "ndet": 3,
 "prof": 10
 },
 "3,3,14|1": {
 "det": 2,
 "ndet": 2,
 "prof": 4
 },
 "3,3,8|0": {
 "det": 7,
 "ndet": 3,
 "prof": 10
 },
 "3,3,8|1": {
 "det": 2,
 "ndet": 2,
 "prof": 4
 },
 "3,8,14|0": {
 "det": 30,
 "ndet": 14,
 "prof": 44
 },
 "3,8,14|1": {
 "det": 7,
 "ndet": 13,
 "prof": 20
 },
 "3,8,15|0": {
 "det": 30,
 "ndet": 14,
 "prof": 44
 },
 "3,8,15|1": {
 "det": 10,
 "ndet": 10,
 "prof": 20
 },
 "3,8,8|0": {
 "det": 22,
 "ndet": 6,
 "prof": 28
 },
 "3,8,8|1": {
 "det": 7,
 "ndet": 6,
 "prof": 13
 },
 "3,8,9|0": {
 "det": 30,
 "ndet": 13,
 "prof": 43
 },
 "3,8,9|1": {
 "det": 10,
 "ndet": 10,
 "prof": 20
 },
 "3,9,14|0": {
 "det": 30,
 "ndet": 20,
 "prof": 50
 },
 "3,9,14|1": {
 "det": 10,
 "ndet": 13,
 "prof": 23
 },
 "8,14,15|0": {
 "det": 320,
 "ndet": 66,
 "prof": 386
 },
 "8,14,15|1": {
 "det": 221,
 "ndet": 65,
 "prof": 286
 },
 "8,14,15|2": {
 "det": 143,
 "ndet": 61,
 "prof": 204
 },
 "8,14,15|3": {
 "det": 84,
 "ndet": 54,
 "prof": 138
 },
 "8,14,15|4": {
 "det": 42,
 "ndet": 45,
 "prof": 87
 },
 "8,14,15|5": {
 "det": 15,
 "ndet": 34,
 "prof": 49
 },
 "8,15,15|0": {
 "det": 204,
 "ndet": 26,
 "prof": 230
 },
 "8,15,15|1": {
 "det": 150,
 "ndet": 26,
 "prof": 176
 },
 "8,15,15|2": {
 "det": 100,
 "ndet": 26,
 "prof": 126
 },
 "8,15,15|3": {
 "det": 64,
 "ndet": 26,
 "prof": 90
 },
 "8,15,15|4": {
 "det": 31,
 "ndet": 26,
 "prof": 57
 },
 "8,15,15|5": {
 "det": 10,
 "ndet": 26,
 "prof": 36
 },
 "8,8,15|0": {
 "det": 98,
 "ndet": 22,
 "prof": 120
 },
 "8,8,15|1": {
 "det": 65,
 "ndet": 19,
 "prof": 84
 },
 "8,8,15|2": {
 "det": 40,
 "ndet": 16,
 "prof": 56
 },
 "8,8,15|3": {
 "det": 22,
 "ndet": 13,
 "prof": 35
 },
 "8,8,15|4": {
 "det": 10,
 "ndet": 10,
 "prof": 20
 },
 "8,8,15|5": {
 "det": 3,
 "ndet": 7,
 "prof": 10
 },
 "8,8,9|0": {
 "det": 92,
 "ndet": 8,
 "prof": 100
 },
 "8,8,9|1": {
 "det": 62,
 "ndet": 8,
 "prof": 70
 },
 "8,8,9|2": {
 "det": 40,
 "ndet": 8,
 "prof": 48
 },
 "8,8,9|3": {
 "det": 22,
 "ndet": 8,
 "prof": 30
 },
 "8,8,9|4": {
 "det": 10,
 "ndet": 8,
 "prof": 18
 },
 "8,8,9|5": {
 "det": 3,
 "ndet": 6,
 "prof": 9
 },
 "8,9,14|0": {
 "det": 188,
 "ndet": 49,
 "prof": 237
 },
 "8,9,14|1": {
 "det": 122,
 "ndet": 45,
 "prof": 167
 },
 "8,9,14|2": {
 "det": 72,
 "ndet": 40,
 "prof": 112
 },
 "8,9,14|3": {
 "det": 36,
 "ndet": 34,
 "prof": 70
 },
 "8,9,14|4": {
 "det": 14,
 "ndet": 26,
 "prof": 40
 },
 "8,9,14|5": {
 "det": 3,
 "ndet": 17,
 "prof": 20
 },
 "8,9,15|0": {
 "det": 206,
 "ndet": 33,
 "prof": 239
 },
 "8,9,15|1": {
 "det": 137,
 "ndet": 31,
 "prof": 168
 },
 "8,9,15|2": {
 "det": 84,
 "ndet": 28,
 "prof": 112
 },
 "8,9,15|3": {
 "det": 45,
 "ndet": 25,
 "prof": 70
 },
 "8,9,15|4": {
 "det": 18,
 "ndet": 22,
 "prof": 40
 },
 "8,9,15|5": {
 "det": 4,
 "ndet": 16,
 "prof": 20
 },
 "8,9,9|0": {
 "det": 102,
 "ndet": 8,
 "prof": 110
 },
 "8,9,9|1": {
 "det": 72,
 "ndet": 8,
 "prof": 80
 },
 "8,9,9|2": {
 "det": 46,
 "ndet": 8,
 "prof": 54
 },
 "8,9,9|3": {
 "det": 28,
 "ndet": 8,
 "prof": 36
 },
 "8,9,9|4": {
 "det": 13,
 "ndet": 8,
 "prof": 21
 },
 "8,9,9|5": {
 "det": 4,
 "ndet": 8,
 "prof": 12
 },
 "9,14,14|0": {
 "det": 206,
 "ndet": 44,
 "prof": 250
 },
 "9,14,14|1": {
 "det": 146,
 "ndet": 44,
 "prof": 190
 },
 "9,14,14|2": {
 "det": 100,
 "ndet": 44,
 "prof": 144
 },
 "9,14,14|3": {
 "det": 58,
 "ndet": 44,
 "prof": 102
 },
 "9,14,14|4": {
 "det": 28,
 "ndet": 44,
 "prof": 72
 },
 "9,14,14|5": {
 "det": 9,
 "ndet": 36,
 "prof": 45
 },
 "9,14,15|0": {
 "det": 376,
 "ndet": 84,
 "prof": 460
 },
 "9,14,15|1": {
 "det": 266,
 "ndet": 84,
 "prof": 350
 },
 "9,14,15|2": {
 "det": 175,
 "ndet": 83,
 "prof": 258
 },
 "9,14,15|3": {
 "det": 105,
 "ndet": 78,
 "prof": 183
 },
 "9,14,15|4": {
 "det": 54,
 "ndet": 69,
 "prof": 123
 },
 "9,14,15|5": {
 "det": 20,
 "ndet": 57,
 "prof": 77
 },
 "9,9,14|0": {
 "det": 119,
 "ndet": 41,
 "prof": 160
 },
 "9,9,14|1": {
 "det": 80,
 "ndet": 38,
 "prof": 118
 },
 "9,9,14|2": {
 "det": 50,
 "ndet": 33,
 "prof": 83
 },
 "9,9,14|3": {
 "det": 28,
 "ndet": 28,
 "prof": 56
 },
 "9,9,14|4": {
 "det": 13,
 "ndet": 22,
 "prof": 35
 },
 "9,9,14|5": {
 "det": 4,
 "ndet": 16,
 "prof": 20
 }
 }

# possible survivor sets on the non-determined side of the 110 mixed keys.
MIXED_NDET_SETS =  {
 "14,14,15|0": [
 [
 0,
 1,
 2
 ]
 ],
 "14,14,15|1": [
 [
 0,
 1,
 2
 ]
 ],
 "14,14,15|2": [
 [
 0,
 1,
 2
 ]
 ],
 "14,14,15|3": [
 [
 0,
 1,
 2
 ]
 ],
 "14,14,15|4": [
 [
 0,
 1,
 2
 ]
 ],
 "14,14,15|5": [
 [
 0,
 1,
 2
 ]
 ],
 "14,14,15|6": [
 [
 0,
 1,
 2
 ]
 ],
 "14,14,15|7": [
 [
 0,
 1,
 2
 ]
 ],
 "14,14,15|8": [
 [
 0,
 1,
 2
 ]
 ],
 "14,14,15|9": [
 [
 0,
 1,
 2
 ]
 ],
 "14,15,15|0": [
 [
 0,
 1,
 2
 ]
 ],
 "14,15,15|1": [
 [
 0,
 1,
 2
 ]
 ],
 "14,15,15|2": [
 [
 0,
 1,
 2
 ]
 ],
 "14,15,15|3": [
 [
 0,
 1,
 2
 ]
 ],
 "14,15,15|4": [
 [
 0,
 1,
 2
 ]
 ],
 "14,15,15|5": [
 [
 0,
 1,
 2
 ]
 ],
 "14,15,15|6": [
 [
 0,
 1,
 2
 ]
 ],
 "14,15,15|7": [
 [
 0,
 1,
 2
 ]
 ],
 "14,15,15|8": [
 [
 0,
 1,
 2
 ]
 ],
 "14,15,15|9": [
 [
 0,
 1,
 2
 ]
 ],
 "2,14,15|0": [
 [
 0,
 1,
 2
 ]
 ],
 "2,14,15|1": [
 [
 0,
 1,
 2
 ]
 ],
 "2,3,14|0": [
 [
 1,
 2
 ]
 ],
 "2,3,14|1": [
 [
 1,
 2
 ]
 ],
 "2,3,8|0": [
 [
 1,
 2
 ]
 ],
 "2,3,8|1": [
 [
 1,
 2
 ]
 ],
 "2,8,15|0": [
 [
 0,
 1
 ]
 ],
 "2,8,15|1": [
 [
 0,
 1
 ]
 ],
 "2,8,9|0": [
 [
 0,
 1,
 2
 ]
 ],
 "2,8,9|1": [
 [
 0,
 1,
 2
 ]
 ],
 "2,9,14|0": [
 [
 1,
 2
 ]
 ],
 "2,9,14|1": [
 [
 1,
 2
 ]
 ],
 "3,14,14|0": [
 [
 1,
 2
 ]
 ],
 "3,14,14|1": [
 [
 1,
 2
 ]
 ],
 "3,14,15|0": [
 [
 0,
 1,
 2
 ],
 [
 1,
 2
 ]
 ],
 "3,14,15|1": [
 [
 0,
 1,
 2
 ],
 [
 1,
 2
 ]
 ],
 "3,3,14|0": [
 [
 1,
 2
 ]
 ],
 "3,3,14|1": [
 [
 1,
 2
 ]
 ],
 "3,3,8|0": [
 [
 1,
 2
 ]
 ],
 "3,3,8|1": [
 [
 1,
 2
 ]
 ],
 "3,8,14|0": [
 [
 1,
 2
 ]
 ],
 "3,8,14|1": [
 [
 1,
 2
 ]
 ],
 "3,8,15|0": [
 [
 0,
 1
 ],
 [
 1,
 2
 ]
 ],
 "3,8,15|1": [
 [
 0,
 1
 ],
 [
 0,
 1,
 2
 ],
 [
 1,
 2
 ]
 ],
 "3,8,8|0": [
 [
 1,
 2
 ]
 ],
 "3,8,8|1": [
 [
 1,
 2
 ]
 ],
 "3,8,9|0": [
 [
 0,
 1,
 2
 ],
 [
 1,
 2
 ]
 ],
 "3,8,9|1": [
 [
 0,
 1,
 2
 ],
 [
 1,
 2
 ]
 ],
 "3,9,14|0": [
 [
 1,
 2
 ]
 ],
 "3,9,14|1": [
 [
 1,
 2
 ]
 ],
 "8,14,15|0": [
 [
 0,
 1
 ],
 [
 0,
 1,
 2
 ]
 ],
 "8,14,15|1": [
 [
 0,
 1
 ],
 [
 0,
 1,
 2
 ]
 ],
 "8,14,15|2": [
 [
 0,
 1
 ],
 [
 0,
 1,
 2
 ]
 ],
 "8,14,15|3": [
 [
 0,
 1
 ],
 [
 0,
 1,
 2
 ]
 ],
 "8,14,15|4": [
 [
 0,
 1
 ],
 [
 0,
 1,
 2
 ]
 ],
 "8,14,15|5": [
 [
 0,
 1
 ],
 [
 0,
 1,
 2
 ]
 ],
 "8,15,15|0": [
 [
 0,
 1
 ]
 ],
 "8,15,15|1": [
 [
 0,
 1
 ]
 ],
 "8,15,15|2": [
 [
 0,
 1
 ]
 ],
 "8,15,15|3": [
 [
 0,
 1
 ]
 ],
 "8,15,15|4": [
 [
 0,
 1
 ]
 ],
 "8,15,15|5": [
 [
 0,
 1
 ]
 ],
 "8,8,15|0": [
 [
 0,
 1
 ]
 ],
 "8,8,15|1": [
 [
 0,
 1
 ]
 ],
 "8,8,15|2": [
 [
 0,
 1
 ]
 ],
 "8,8,15|3": [
 [
 0,
 1
 ]
 ],
 "8,8,15|4": [
 [
 0,
 1
 ]
 ],
 "8,8,15|5": [
 [
 0,
 1
 ]
 ],
 "8,8,9|0": [
 [
 0,
 1,
 2
 ]
 ],
 "8,8,9|1": [
 [
 0,
 1,
 2
 ]
 ],
 "8,8,9|2": [
 [
 0,
 1,
 2
 ]
 ],
 "8,8,9|3": [
 [
 0,
 1,
 2
 ]
 ],
 "8,8,9|4": [
 [
 0,
 1,
 2
 ]
 ],
 "8,8,9|5": [
 [
 0,
 1,
 2
 ]
 ],
 "8,9,14|0": [
 [
 0,
 1,
 2
 ],
 [
 1,
 2
 ]
 ],
 "8,9,14|1": [
 [
 0,
 1,
 2
 ],
 [
 1,
 2
 ]
 ],
 "8,9,14|2": [
 [
 0,
 1,
 2
 ],
 [
 1,
 2
 ]
 ],
 "8,9,14|3": [
 [
 0,
 1,
 2
 ],
 [
 1,
 2
 ]
 ],
 "8,9,14|4": [
 [
 0,
 1,
 2
 ],
 [
 1,
 2
 ]
 ],
 "8,9,14|5": [
 [
 0,
 1,
 2
 ],
 [
 1,
 2
 ]
 ],
 "8,9,15|0": [
 [
 0,
 1
 ],
 [
 0,
 1,
 2
 ]
 ],
 "8,9,15|1": [
 [
 0,
 1
 ],
 [
 0,
 1,
 2
 ]
 ],
 "8,9,15|2": [
 [
 0,
 1
 ],
 [
 0,
 1,
 2
 ]
 ],
 "8,9,15|3": [
 [
 0,
 1
 ],
 [
 0,
 1,
 2
 ]
 ],
 "8,9,15|4": [
 [
 0,
 1
 ],
 [
 0,
 1,
 2
 ]
 ],
 "8,9,15|5": [
 [
 0,
 1
 ],
 [
 0,
 1,
 2
 ]
 ],
 "8,9,9|0": [
 [
 0,
 1,
 2
 ]
 ],
 "8,9,9|1": [
 [
 0,
 1,
 2
 ]
 ],
 "8,9,9|2": [
 [
 0,
 1,
 2
 ]
 ],
 "8,9,9|3": [
 [
 0,
 1,
 2
 ]
 ],
 "8,9,9|4": [
 [
 0,
 1,
 2
 ]
 ],
 "8,9,9|5": [
 [
 0,
 1,
 2
 ]
 ],
 "9,14,14|0": [
 [
 1,
 2
 ]
 ],
 "9,14,14|1": [
 [
 1,
 2
 ]
 ],
 "9,14,14|2": [
 [
 1,
 2
 ]
 ],
 "9,14,14|3": [
 [
 1,
 2
 ]
 ],
 "9,14,14|4": [
 [
 1,
 2
 ]
 ],
 "9,14,14|5": [
 [
 1,
 2
 ]
 ],
 "9,14,15|0": [
 [
 0,
 1,
 2
 ],
 [
 1,
 2
 ]
 ],
 "9,14,15|1": [
 [
 0,
 1,
 2
 ],
 [
 1,
 2
 ]
 ],
 "9,14,15|2": [
 [
 0,
 1,
 2
 ],
 [
 1,
 2
 ]
 ],
 "9,14,15|3": [
 [
 0,
 1,
 2
 ],
 [
 1,
 2
 ]
 ],
 "9,14,15|4": [
 [
 0,
 1,
 2
 ],
 [
 1,
 2
 ]
 ],
 "9,14,15|5": [
 [
 0,
 1,
 2
 ],
 [
 1,
 2
 ]
 ],
 "9,9,14|0": [
 [
 1,
 2
 ]
 ],
 "9,9,14|1": [
 [
 1,
 2
 ]
 ],
 "9,9,14|2": [
 [
 1,
 2
 ]
 ],
 "9,9,14|3": [
 [
 1,
 2
 ]
 ],
 "9,9,14|4": [
 [
 1,
 2
 ]
 ],
 "9,9,14|5": [
 [
 1,
 2
 ]
 ]
 }

# first-loser residue class census over the 3,060 cap<=15 keys (r=3).
RESIDUE_CLASSES =  {
 "0": 210,
 "0,1": 660,
 "0,1,2": 525,
 "0,2": 750,
 "1": 140,
 "1,2": 600,
 "2": 175
 }
TWO_RESIDUE_KEYS = 2010

# keys containing a branch of the given size: (count, mixed among them).
BRANCH_STATS =  {
 "11": [
 660,
 0
 ],
 "12": [
 670,
 0
 ],
 "13": [
 676,
 0
 ],
 "14": [
 679,
 66
 ],
 "15": [
 680,
 58
 ],
 "8": [
 596,
 58
 ]
 }

SAMPLE_STRIDE = 32


# ---------------------------------------------------------------------------
# committed records
# ---------------------------------------------------------------------------

def load_records():
    """Committed packed sweep records for r=3, cap<=15.

    Committed as three line-aligned parts (63,288 records each) whose
    byte-exact join is the packed publication blob; per-part sha256
    and the joined sha256 are pinned constants.

    Packed publication format (one JSON array per line):
    [i, sv_mask, fl_mask, states]. atoms are NOT stored; they are a pure
    function of i through the canonical cap<=15 enumeration
    (direct_constrained below). determined == (popcount(sv_mask) == 1).
    """
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "output",
                           "js_cap15_r3.packed.jsonl.part1of3"), "rb") as f:
        b1 = f.read()
    with open(os.path.join(here, "output",
                           "js_cap15_r3.packed.jsonl.part2of3"), "rb") as f:
        b2 = f.read()
    with open(os.path.join(here, "output",
                           "js_cap15_r3.packed.jsonl.part3of3"), "rb") as f:
        b3 = f.read()
    if hashlib.sha256(b1).hexdigest() != COMMITTED_PACKED_PART1_SHA256:
        raise SystemExit("packed part1 sha256 mismatch")
    if hashlib.sha256(b2).hexdigest() != COMMITTED_PACKED_PART2_SHA256:
        raise SystemExit("packed part2 sha256 mismatch")
    if hashlib.sha256(b3).hexdigest() != COMMITTED_PACKED_PART3_SHA256:
        raise SystemExit("packed part3 sha256 mismatch")
    blob = b1 + b2 + b3
    sha = hashlib.sha256(blob).hexdigest()
    out = []
    for line in blob.decode().splitlines():
        line = line.strip()
        if not line:
            continue
        i, sv, fl, states = json.loads(line)
        survivors = [p for p in range(64) if (sv >> p) & 1]
        first_losers = [p for p in range(64) if (fl >> p) & 1]
        out.append({
            "i": i,
            "sv_mask": sv,
            "fl_mask": fl,
            "determined": len(survivors) == 1,
            "survivors": survivors,
            "first_losers": first_losers,
            "states": states,
        })
    return out, sha


# ---------------------------------------------------------------------------
# analysis over committed records + canonical enumeration
# ---------------------------------------------------------------------------

def analyze(profiles, records):
    byk = {}
    for i, atoms in enumerate(profiles):
        rec = records[i]
        byk.setdefault(key_of(atoms), []).append((atoms, rec))
    census = {
        "uniform_det": 0,
        "uniform_ndet": 0,
        "mixed_keys": [],
        "det_profiles": 0,
        "ndet_profiles": 0,
        "total_states": 0,
        "max_states": 0,
        "fl_violations": 0,
    }
    partitions = {}
    ndet_sets = {}
    det_surv_by_key = {}
    for k, items in byk.items():
        det = sum(1 for _, rec in items if rec["determined"])
        ndet = len(items) - det
        census["det_profiles"] += det
        census["ndet_profiles"] += ndet
        for _, rec in items:
            census["total_states"] += rec["states"]
            census["max_states"] = max(census["max_states"], rec["states"])
        if det == 0:
            census["uniform_ndet"] += 1
        elif ndet == 0:
            census["uniform_det"] += 1
        else:
            census["mixed_keys"].append(k)
            partitions[kstr(k)] = {"det": det, "ndet": ndet,
                                   "prof": len(items)}
            s = set()
            for atoms, rec in items:
                if not rec["determined"]:
                    s.add(tuple(rec["survivors"]))
                else:
                    det_surv_by_key.setdefault(kstr(k), set()).add(
                        tuple(rec["survivors"]))
                sizes = profile_sizes(atoms, 3)
                want = sorted(set(c % R for c in sizes))
                if sorted(set(rec["first_losers"])) != want:
                    census["fl_violations"] += 1
            ndet_sets[kstr(k)] = sorted([list(t) for t in s])
    census["keys"] = len(byk)
    census["mixed_keys"] = sorted(census["mixed_keys"])
    residue = {}
    for k in byk:
        residue[kstr(k)] = ",".join(map(str, sorted(set(
            c % R for c in k[0]))))
    return byk, census, partitions, ndet_sets, det_surv_by_key, residue


def residue_class_census(residue, mixed_keys):
    from collections import Counter
    # residue maps kstr(k) -> comma-joined residue class string
    cnt = Counter(residue.values())
    mixed_cnt = Counter(residue[kstr(k)] for k in mixed_keys)
    return cnt, mixed_cnt


# ---------------------------------------------------------------------------
# checks
# ---------------------------------------------------------------------------

def check(name, ok, note):
    return {"name": name, "ok": bool(ok), "note": note}


def d14_positions(profiles15):
    """Order-preserving subsequence positions of D_14 inside D_15
    (both regenerated deterministically by the same enumeration)."""
    p14 = direct_constrained(14)
    pos = {}
    j = 0
    for prof in p14:
        while profiles15[j] != prof:
            j += 1
        pos[j] = len(pos)
        j += 1
    return p14, pos


def assemble_audit():
    here = os.path.dirname(os.path.abspath(__file__))
    checks = []
    notes = []

    # -- enumeration -------------------------------------------------------
    fix_id, fix_trans, fix_cyc, orbits = burnside_fix_counts(CAP)
    ok = ((fix_id, fix_trans, fix_cyc, orbits)
          == (BURNSIDE_15["fix_id"], BURNSIDE_15["fix_trans"],
              BURNSIDE_15["fix_cyc"], BURNSIDE_15["orbits"]))
    checks.append(check("burnside_cap15", ok,
                        "fix(id,trans,cyc)=(%d,%d,%d) orbits=%d"
                        % (fix_id, fix_trans, fix_cyc, orbits)))
    profiles = direct_constrained(CAP)
    ok = len(profiles) == RECORDS_EXPECTED
    checks.append(check("enumeration_cap15", ok,
                        "len(D_15)=%d expected=%d" % (len(profiles),
                                                     RECORDS_EXPECTED)))

    # -- committed records --------------------------------------------------
    records, sha = load_records()
    ok = sha == COMMITTED_PACKED_SHA256 and len(records) == RECORDS_EXPECTED
    checks.append(check("committed_packed_sha256", ok,
                        "sha256=%s records=%d" % (sha, len(records))))
    bad = 0
    for n, rec in enumerate(records):
        if rec["i"] != n:
            bad += 1
        if rec["sv_mask"] >> R or rec["fl_mask"] >> R:
            bad += 1
        if rec["determined"] != (len(rec["survivors"]) == 1):
            bad += 1
        if rec["states"] < 1:
            bad += 1
    checks.append(check("committed_records_format", bad == 0,
                        "i-contiguity/bitwidth/determined/states violations=%d"
                        % bad))

    # -- analysis -----------------------------------------------------------
    byk, census, partitions, ndet_sets, det_surv, residue = analyze(
        profiles, records)
    ok = (census["keys"] == CENSUS_15["keys"]
          and census["uniform_det"] == CENSUS_15["uniform_det"]
          and census["uniform_ndet"] == CENSUS_15["uniform_ndet"]
          and census["det_profiles"] == CENSUS_15["det_profiles"]
          and census["ndet_profiles"] == CENSUS_15["ndet_profiles"]
          and census["total_states"] == CENSUS_15["total_states"]
          and census["max_states"] == CENSUS_15["max_states"])
    checks.append(check("census_totals", ok,
                        "keys=%d udet=%d undet=%d det_prof=%d "
                        "ndet_prof=%d states=%d max=%d"
                        % (census["keys"], census["uniform_det"],
                           census["uniform_ndet"], census["det_profiles"],
                           census["ndet_profiles"], census["total_states"],
                           census["max_states"])))

    mixed = census["mixed_keys"]
    mixed_list = [[list(k[0]), k[1]] for k in mixed]
    ok = (mixed_list == EXPECTED_FAILING_110_KEYS and len(mixed) == 110)
    checks.append(check("mixed_keys_are_H14_52_plus_58_new", ok,
                        "mixed=%d; equals theorem H14 52 + 58 new keys: %s"
                        % (len(mixed), ok)))
    ok = all(k in mixed_list for k in EXPECTED_FAILING_22_KEYS)
    checks.append(check("theorem_H_22_still_mixed", ok,
                        "all 22 theorem H keys remain mixed at cap<=15"))
    ok = all(k in mixed_list for k in EXPECTED_FAILING_52_KEYS)
    checks.append(check("h14_52_still_mixed", ok,
                        "all 52 theorem H14 keys remain mixed at cap<=15"))
    new_keys = [k for k in mixed_list if k not in EXPECTED_FAILING_52_KEYS]
    ok = (len(new_keys) == 58 and all(15 in k[0] for k in new_keys))
    checks.append(check("new_mixed_keys_have_size15", ok,
                        "58 new mixed keys, each containing a size-15 "
                        "branch: %s" % ok))

    ok = partitions == MIXED_PARTITION
    checks.append(check("mixed_partition", ok,
                        "per-key det/ndet/profile table equals the embedded "
                        "constant" if ok else "partition mismatch"))
    ok = ndet_sets == MIXED_NDET_SETS
    checks.append(check("mixed_ndet_sets", ok,
                        "possible survivor sets on the ndet side equal the "
                        "embedded constant"))
    ok = all(s == {(1,)} for s in det_surv.values())
    checks.append(check("mixed_det_survivors_uniform_P1", ok,
                        "det-side survivor set == {P_1} in all %d mixed keys"
                        % len(det_surv)))

    # sizes / structure of mixed keys
    ok = (all(min(k[0]) >= 2 for k in mixed) and
          all(max(k[0]) in (8, 9, 14, 15) for k in mixed) and
          all((8 in k[0]) or (9 in k[0]) or (14 in k[0])
              or (15 in k[0]) for k in mixed))
    checks.append(check("mixed_structure_sizes", ok,
                        "mixed sizes within [2,15]; max in {8,9,14,15}; "
                        "every mixed key contains a size-8/9/14/15 "
                        "branch"))

    # -- FL lemma -----------------------------------------------------------
    ok = census["fl_violations"] == 0
    checks.append(check("FL_lemma_cap15", ok,
                        "possible-first-loser set == {C_i mod 3} on all %d "
                        "profiles, violations=%d"
                        % (RECORDS_EXPECTED, census["fl_violations"])))

    # -- residue lens -------------------------------------------------------
    cnt, mixed_cnt = residue_class_census(residue, mixed)
    cls = {k: v for k, v in sorted(cnt.items())}
    ok = cls == RESIDUE_CLASSES
    checks.append(check("residue_class_census", ok,
                        "classes=%s" % json.dumps(cls, sort_keys=True)))
    two = sum(v for k, v in cnt.items() if len(k.split(",")) == 2)
    ok = two == TWO_RESIDUE_KEYS
    checks.append(check("two_residue_keys", ok,
                        "two-residue keys=%d expected=%d"
                        % (two, TWO_RESIDUE_KEYS)))
    # all one- and three-residue keys collapse
    non_two_mixed = [k for k in mixed
                     if len(residue[kstr(k)].split(",")) != 2]
    ok = len(non_two_mixed) == 0
    checks.append(check("non_two_residue_keys_collapse", ok,
                        "mixed keys outside the 2-residue class: %d"
                        % len(non_two_mixed)))
    ok = (mixed_cnt.get("0,2", 0) == 110
          and sum(mixed_cnt.values()) == 110)
    checks.append(check("mixed_residue_pair_02", ok,
                        "mixed residue census=%s"
                        % json.dumps(dict(mixed_cnt), sort_keys=True)))

    # -- branch size stats ---------------------------------------------------
    stats = {}
    for sz in (8, 11, 12, 13, 14, 15):
        ks = [k for k in byk if sz in k[0]]
        stats[str(sz)] = [len(ks), sum(1 for k in ks if k in mixed)]
    ok = stats == BRANCH_STATS
    checks.append(check("branch_size_stats", ok,
                        "size->(keys, mixed)=%s" % json.dumps(stats,
                                                              sort_keys=True)))

    # -- K0883 cross-artifact: records ---------------------------------------
    p14, pos = d14_positions(profiles)
    with open(os.path.join(here, K0883_R3_PACKED_P1_PATH), "rb") as f:
        kb1 = f.read()
    with open(os.path.join(here, K0883_R3_PACKED_P2_PATH), "rb") as f:
        kb2 = f.read()
    if hashlib.sha256(kb1).hexdigest() != K0883_R3_PACKED_PART1_SHA256:
        raise SystemExit("K0883 packed part1 sha256 mismatch")
    if hashlib.sha256(kb2).hexdigest() != K0883_R3_PACKED_PART2_SHA256:
        raise SystemExit("K0883 packed part2 sha256 mismatch")
    blob = kb1 + kb2
    ksha = hashlib.sha256(blob).hexdigest()
    pub = [json.loads(line) for line in blob.decode().splitlines() if line.strip()]
    rec_mism = 0
    for j15, k14 in pos.items():
        # the packed i field is the position in the producing enumeration:
        # j15 in D_15 (this experiment) vs k14 in D_14 (the K0883 file);
        # sv_mask / fl_mask / states must be identical for the same
        # canonical profile.
        rec = records[j15]
        if ([rec["i"], rec["sv_mask"], rec["fl_mask"], rec["states"]]
                != [j15, pub[k14][1], pub[k14][2], pub[k14][3]]
                or pub[k14][0] != k14):
            rec_mism += 1
    ok = (ksha == K0883_R3_PACKED_JOINED_SHA256 and rec_mism == 0
          and len(pub) == 123272 and len(pos) == 123272)
    checks.append(check("k0883_cross_records", ok,
                        "published K0883 r=3 packed sha256 ok=%s; %d/%d "
                        "records reproduced at the D_14 subsequence "
                        "positions, mismatches=%d"
                        % (ksha == K0883_R3_PACKED_JOINED_SHA256, len(pub),
                           len(pos), rec_mism)))

    # -- K0876 cross-artifact: audit partition ------------------------------
    with open(os.path.join(here, K0876_AUDIT_PATH), "rb") as f:
        ablob = f.read()
    asha = hashlib.sha256(ablob).hexdigest()
    ok = asha == K0876_AUDIT_SHA256
    checks.append(check("k0876_audit_sha256", ok,
                        "K0876 audit sha256=%s" % asha))
    a76 = json.loads(ablob.decode())
    fp = a76["sweeps"]["r3"]["failing_partitions"]
    part_mism = 0
    for kk, v in fp.items():
        mine = partitions.get(kk)
        if mine is None or mine["det"] != v["n_det"] or \
                mine["prof"] != v["profiles"]:
            part_mism += 1
    ok = part_mism == 0 and len(fp) == 22
    checks.append(check("k0876_audit_partition", ok,
                        "theorem-H 22-key r=3 partition equals K0876 "
                        "audit sweeps.r3.failing_partitions, "
                        "mismatches=%d/%d" % (part_mism, len(fp))))

    # -- K0883 cross-artifact: audit partition ------------------------------
    with open(os.path.join(here, K0883_AUDIT_PATH), "rb") as f:
        k83blob = f.read()
    k83sha = hashlib.sha256(k83blob).hexdigest()
    ok = k83sha == K0883_AUDIT_SHA256
    checks.append(check("k0883_audit_sha256", ok,
                        "K0883 audit sha256=%s" % k83sha))
    a83 = json.loads(k83blob.decode())
    fp83 = a83["mixed_partition"]
    part83_mism = 0
    for kk, v in fp83.items():
        mine = partitions.get(kk)
        if (mine is None or mine["det"] != v["det"]
                or mine["ndet"] != v["ndet"]
                or mine["prof"] != v["prof"]):
            part83_mism += 1
    ok = part83_mism == 0 and len(fp83) == 52
    checks.append(check("k0883_audit_partition", ok,
                        "theorem-H14 52-key r=3 partition equals the "
                        "K0883 audit mixed_partition, "
                        "mismatches=%d/%d" % (part83_mism, len(fp83))))

    # -- assemble ------------------------------------------------------------
    all_ok = all(c["ok"] for c in checks)
    audit = {
        "meta": {
            "date": "2026-11-16",
            "item": "K0886",
            "claim": ("cap<=15, r=3: non-collapsing keys are exactly "
                      "110 = theorem H14 52 + 58 new keys, each new key "
                      "containing a size-15 branch; the 14-generation of "
                      "new keys continues at 15, the gamma windows of "
                      "(14,14,15)/(14,15,15) extend to 0..9, and the "
                      "possible survivor set {0,1} appears on the "
                      "non-determined side for the first time"),
            "engine_provenance": (
                "verbatim region game / enumeration / Burnside / mask twin "
                "from the published K0883 verifier (which extends the "
                "K0876 packed-reading repair, commit c50f31f1); "
                "full-domain records produced by the committed JavaScript "
                "mask engine mask_engine_fast.js over the canonical "
                "cap<=15 enumeration; Python twin cross-validated live in "
                "every run"),
            "records_format": "packed [i, sv_mask, fl_mask, states]",
        },
        "burnside": {"fix_id": fix_id, "fix_trans": fix_trans,
                     "fix_cyc": fix_cyc, "orbits": orbits},
        "committed": {"records": len(records), "sha256_packed": sha,
                     "sha256_part1": COMMITTED_PACKED_PART1_SHA256,
                     "sha256_part2": COMMITTED_PACKED_PART2_SHA256,
                     "sha256_part3": COMMITTED_PACKED_PART3_SHA256},
        "census": census,
        "mixed_partition": partitions,
        "mixed_ndet_sets": ndet_sets,
        "residue_classes": cls,
        "mixed_residue": dict(sorted(mixed_cnt.items())),
        "branch_size_stats": stats,
        "k0883_cross": {
            "packed_part1_sha256": K0883_R3_PACKED_PART1_SHA256,
            "packed_part2_sha256": K0883_R3_PACKED_PART2_SHA256,
            "packed_sha256": ksha,
            "records_reproduced": len(pos),
            "record_mismatches": rec_mism,
        },
        "k0876_audit": {
            "audit_sha256": asha,
            "partition_keys": len(fp),
            "partition_mismatches": part_mism,
        },
        "k0883_audit": {
            "audit_sha256": k83sha,
            "partition_keys": len(fp83),
            "partition_mismatches": part83_mism,
        },
        "machine_checks": checks,
        "summary": {"all_ok": all_ok, "checks_total": len(checks)},
    }
    return audit


def serialize(audit):
    return json.dumps(audit, indent=1, sort_keys=True,
                      ensure_ascii=False) + "\n"


# ---------------------------------------------------------------------------
# live checks (engine re-computations; not part of the audit bytes)
# ---------------------------------------------------------------------------

def live_checks(audit):
    profiles = direct_constrained(CAP)
    pidx = {atoms: i for i, atoms in enumerate(profiles)}
    records, _ = load_records()
    rec = {r["i"]: r for r in records}

    # L1: full cap<=7 domain, verbatim == mask twin == committed JS
    profs7 = direct_constrained(7)
    mism = 0
    n = 0
    for atoms in profs7:
        idx15 = pidx[atoms]
        v1, s1 = region_verdict(atoms, 3, R, budget=20_000_000)
        v2, s2 = mask_verdict(atoms, 3, R, budget=20_000_000)
        j = rec[idx15]
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
          "JS records (verdicts and state counts) on %d verdicts (r=3)" % n)

    # L2: stratified cap<=15 sample, mask twin == committed JS records
    mism = 0
    n = 0
    for i in range(0, len(profiles), SAMPLE_STRIDE):
        atoms = profiles[i]
        v2, s2 = mask_verdict(atoms, 3, R, budget=50_000_000)
        j = rec[i]
        n += 1
        if verdict_triple(v2) != (j["determined"], j["survivors"],
                                 j["first_losers"]):
            mism += 1
        if s2 != j["states"]:
            mism += 1
    if mism != 0 or n != 5934:
        sys.stderr.write("LIVE FAIL: stratified sample %d mismatches / %d\n"
                         % (mism, n))
        sys.exit(1)
    print("LIVE OK: stratified cap<=15 sample (stride %d): mask twin == "
          "committed JS records on %d verdicts (verdicts and state counts)"
          % (SAMPLE_STRIDE, n))

    # L3: K0862 published 44 witnesses re-run with the verbatim engine
    wit_fail = 0
    js_cmp = 0
    js_mism = 0
    for kk, pair in K0862_WITNESSES.items():
        for tag, atoms_s in (("det", pair[0]), ("ndet", pair[1])):
            atoms = tuple(atoms_s)
            v, _ = region_verdict(atoms, 3, R, budget=50_000_000)
            if tag == "det":
                if not (v["determined"] and v["survivors"] == [1]):
                    wit_fail += 1
            else:
                if v["determined"] or sorted(v["survivors"]) not in \
                        ([0, 1, 2], [1, 2]):
                    wit_fail += 1
            idx = pidx.get(atoms)
            if idx is not None:
                j = rec[idx]
                js_cmp += 1
                if verdict_triple(v) != (j["determined"], j["survivors"],
                                          j["first_losers"]):
                    js_mism += 1
    if wit_fail != 0 or js_mism != 0 or js_cmp != 44:
        sys.stderr.write("LIVE FAIL: witnesses wit_fail=%d js_mism=%d "
                         "js_cmp=%d\n" % (wit_fail, js_mism, js_cmp))
        sys.exit(1)
    print("LIVE OK: all 44 K0862 published witnesses re-verified with the "
          "verbatim engine (%d also cross-checked against the committed "
          "JS records, %d mismatches)" % (js_cmp, js_mism))


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
        "remo_k_branch_cap15_boundary_audit.json",
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
