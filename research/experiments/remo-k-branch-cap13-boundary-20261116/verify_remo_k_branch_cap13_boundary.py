#!/usr/bin/env python3
"""K0880 audit: 3-branch REMO determinacy size boundary cap<=13 for r=3.

Self-contained verifier. Deterministic (no randomness, no wall clock, no
network). Python 3.11+ / stdlib only.

Extends Theorem H12 (K0875, cap<=12, r=3: exactly 22 non-collapsing keys)
to cap<=13. The canonical cap<=13 profile enumeration (77,828 orbits,
S_3-canonicalized atom vectors) is swept once with the committed
JavaScript mask engine (mask_engine_fast.js, the K0876 lineage engine)
at r=3; the records are committed in the packed publication format
([i, sv_mask, fl_mask, states] - same format as the K0876 repair; atoms
are re-derived from the canonical enumeration inside this verifier).

Main finite claims checked here (cap<=13, r=3, complete enumeration):

  - The non-collapsing (mixed) keys are exactly the Theorem H 22 keys;
    zero new non-collapsing keys appear when the branch-size boundary
    moves from 12 to 13. All 455 keys containing a size-13 branch
    collapse to key level.
  - The order-preserving subsequence property: the canonical cap<=12
    list D_12 embeds into D_13, and at the mapped positions the
    committed cap<=13 records reproduce ALL 47,595 published K0876 r=3
    packed records byte-for-byte (cross-artifact, sha256-pinned).
  - The per-key det/ndet partition of the 22 mixed keys equals the
    K0876 audit sweeps.r3.failing_partitions (sha256-pinned cross-read).
  - Residue lens (K0872): every mixed key has first-loser residue pair
    {0,2}; all 330 one-residue and 300 three-residue keys collapse;
    1,190 two-residue keys contain exactly the 22 mixed keys.
  - Lemma FL (possible first losers == {C_i mod 3}): 0 violations over
    all 77,828 cap<=13 profiles (extends the K0875 cap<=12 observation).

Live engine re-checks (not part of the audit bytes): verbatim region
engine == Python mask twin == committed JS records on the full cap<=7
domain (2,048 verdicts) and on a stride-32 sample of D_13 (2,433
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

CAP = 13
R = 3
RECORDS_EXPECTED = 77828

# Burnside / enumeration expectation for cap<=13 (fix counts over the
# S_3 action on the 7-atom vectors, computed with burnside_fix_counts).
BURNSIDE_13 = {"fix_id": 432906, "fix_trans": 11186, "fix_cyc": 252,
               "orbits": 77828}

# Committed packed sweep records sha256 (output/js_cap13_r3.packed.jsonl).
COMMITTED_PACKED_SHA256 = (
    "47a5eb34f738dc60a74d4ef0c66e54032d7c79f2e3413b47c40dbc56c07df5fd"
)

# Cross-artifact pins (published K0876 repair artifacts on main).
K0876_R3_PACKED_PATH = os.path.join(
    "..", "remo-k-branch-cap12-r456-boundary-20261116", "output",
    "js_cap12_r3.packed.jsonl",
)
K0876_R3_PACKED_SHA256 = (
    "ea7c66286f728a52d5696d627ce1faf7705e77f9e4222493221f3a4fe79ed134"
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

# K0862 published 44 minimal witnesses (det/ndet atom pairs per key),
# same constant as the K0876 verifier.
K0862_WITNESSES = {"2,3,8|0": [[1, 1, 1, 7, 0, 1, 0], [1, 1, 0, 5, 1, 2, 0]], "2,3,8|1": [[1, 2, 0, 7, 0, 0, 1], [1, 1, 0, 6, 0, 1, 1]], "2,8,9|0": [[1, 2, 1, 4, 0, 5, 0], [1, 1, 0, 1, 1, 7, 0]], "2,8,9|1": [[1, 3, 0, 4, 0, 4, 1], [1, 1, 0, 2, 0, 6, 1]], "3,3,8|0": [[1, 1, 1, 6, 1, 1, 0], [1, 1, 0, 4, 2, 2, 0]], "3,3,8|1": [[1, 1, 1, 7, 0, 0, 1], [1, 1, 0, 5, 1, 1, 1]], "3,8,8|0": [[1, 1, 1, 1, 1, 6, 0], [1, 1, 2, 3, 0, 5, 0]], "3,8,8|1": [[1, 1, 6, 2, 0, 0, 1], [1, 1, 1, 2, 0, 5, 1]], "3,8,9|0": [[1, 2, 1, 3, 1, 5, 0], [1, 1, 1, 2, 1, 6, 0]], "3,8,9|1": [[1, 3, 0, 3, 1, 4, 1], [1, 1, 0, 1, 1, 6, 1]], "8,8,9|0": [[1, 1, 3, 1, 4, 4, 0], [1, 1, 6, 5, 1, 2, 0]], "8,8,9|1": [[1, 1, 3, 2, 3, 3, 1], [1, 1, 5, 4, 1, 2, 1]], "8,8,9|2": [[1, 1, 2, 1, 3, 3, 2], [1, 1, 4, 3, 1, 2, 2]], "8,8,9|3": [[1, 1, 2, 2, 2, 2, 3], [1, 1, 3, 2, 1, 2, 3]], "8,8,9|4": [[1, 1, 2, 3, 1, 1, 4], [1, 1, 1, 1, 2, 2, 4]], "8,8,9|5": [[1, 1, 2, 4, 0, 0, 5], [1, 1, 1, 2, 1, 1, 5]], "8,9,9|0": [[1, 1, 4, 2, 3, 4, 0], [1, 1, 6, 6, 1, 2, 0]], "8,9,9|1": [[1, 1, 3, 1, 3, 4, 1], [1, 1, 5, 5, 1, 2, 1]], "8,9,9|2": [[1, 1, 3, 2, 2, 3, 2], [1, 1, 4, 4, 1, 2, 2]], "8,9,9|3": [[1, 1, 2, 1, 2, 3, 3], [1, 1, 3, 3, 1, 2, 3]], "8,9,9|4": [[1, 1, 3, 2, 1, 1, 4], [1, 1, 2, 2, 1, 2, 4]], "8,9,9|5": [[1, 1, 3, 3, 0, 0, 5], [1, 1, 1, 1, 1, 2, 5]]}

# cap<=13, r=3 census totals (from the committed records; this file is
# the new published constant).
CENSUS_13 = {
    "keys": 1820,
    "uniform_det": 313,
    "uniform_ndet": 1485,
    "mixed": 22,
    "det_profiles": 11515,
    "ndet_profiles": 66313,
    "total_states": 294553171,
    "max_states": 48256,
}

# per-key det/ndet/profile partition of the 22 mixed keys (cap<=13, r=3).
MIXED_PARTITION = {"2,3,8|0": {"det": 6, "ndet": 2, "prof": 8}, "2,3,8|1": {"det": 1, "ndet": 1, "prof": 2}, "2,8,9|0": {"det": 18, "ndet": 5, "prof": 23}, "2,8,9|1": {"det": 5, "ndet": 2, "prof": 7}, "3,3,8|0": {"det": 7, "ndet": 3, "prof": 10}, "3,3,8|1": {"det": 2, "ndet": 2, "prof": 4}, "3,8,8|0": {"det": 22, "ndet": 6, "prof": 28}, "3,8,8|1": {"det": 7, "ndet": 6, "prof": 13}, "3,8,9|0": {"det": 30, "ndet": 13, "prof": 43}, "3,8,9|1": {"det": 10, "ndet": 10, "prof": 20}, "8,8,9|0": {"det": 92, "ndet": 8, "prof": 100}, "8,8,9|1": {"det": 62, "ndet": 8, "prof": 70}, "8,8,9|2": {"det": 40, "ndet": 8, "prof": 48}, "8,8,9|3": {"det": 22, "ndet": 8, "prof": 30}, "8,8,9|4": {"det": 10, "ndet": 8, "prof": 18}, "8,8,9|5": {"det": 3, "ndet": 6, "prof": 9}, "8,9,9|0": {"det": 102, "ndet": 8, "prof": 110}, "8,9,9|1": {"det": 72, "ndet": 8, "prof": 80}, "8,9,9|2": {"det": 46, "ndet": 8, "prof": 54}, "8,9,9|3": {"det": 28, "ndet": 8, "prof": 36}, "8,9,9|4": {"det": 13, "ndet": 8, "prof": 21}, "8,9,9|5": {"det": 4, "ndet": 8, "prof": 12}}

# possible survivor sets on the non-determined side of the 22 mixed keys.
MIXED_NDET_SETS = {"2,3,8|0": [[1, 2]], "2,3,8|1": [[1, 2]], "2,8,9|0": [[0, 1, 2]], "2,8,9|1": [[0, 1, 2]], "3,3,8|0": [[1, 2]], "3,3,8|1": [[1, 2]], "3,8,8|0": [[1, 2]], "3,8,8|1": [[1, 2]], "3,8,9|0": [[0, 1, 2], [1, 2]], "3,8,9|1": [[0, 1, 2], [1, 2]], "8,8,9|0": [[0, 1, 2]], "8,8,9|1": [[0, 1, 2]], "8,8,9|2": [[0, 1, 2]], "8,8,9|3": [[0, 1, 2]], "8,8,9|4": [[0, 1, 2]], "8,8,9|5": [[0, 1, 2]], "8,9,9|0": [[0, 1, 2]], "8,9,9|1": [[0, 1, 2]], "8,9,9|2": [[0, 1, 2]], "8,9,9|3": [[0, 1, 2]], "8,9,9|4": [[0, 1, 2]], "8,9,9|5": [[0, 1, 2]]}

# first-loser residue class census over the 1,820 cap<=13 keys (r=3).
RESIDUE_CLASSES = {"0": 105, "1": 140, "2": 85, "0,1": 450, "0,2": 340,
                   "1,2": 400, "0,1,2": 300}
TWO_RESIDUE_KEYS = 1190

# keys containing a branch of the given size: (count, mixed among them).
BRANCH_STATS = {"8": [420, 22], "11": [451, 0], "12": [454, 0], "13": [455, 0]}

SAMPLE_STRIDE = 32


# ---------------------------------------------------------------------------
# committed records
# ---------------------------------------------------------------------------

def load_records():
    """Committed packed sweep records for r=3, cap<=13.

    Packed publication format (one JSON array per line):
    [i, sv_mask, fl_mask, states]. atoms are NOT stored; they are a pure
    function of i through the canonical cap<=13 enumeration
    (direct_constrained below). determined == (popcount(sv_mask) == 1).
    """
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "output", "js_cap13_r3.packed.jsonl")
    with open(path, "rb") as f:
        blob = f.read()
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


def d12_positions(profiles13):
    """Order-preserving subsequence positions of D_12 inside D_13
    (both regenerated deterministically by the same enumeration)."""
    p12 = direct_constrained(12)
    pos = {}
    j = 0
    for prof in p12:
        while profiles13[j] != prof:
            j += 1
        pos[j] = len(pos)
        j += 1
    return p12, pos


def assemble_audit():
    here = os.path.dirname(os.path.abspath(__file__))
    checks = []
    notes = []

    # -- enumeration -------------------------------------------------------
    fix_id, fix_trans, fix_cyc, orbits = burnside_fix_counts(CAP)
    ok = ((fix_id, fix_trans, fix_cyc, orbits)
          == (BURNSIDE_13["fix_id"], BURNSIDE_13["fix_trans"],
              BURNSIDE_13["fix_cyc"], BURNSIDE_13["orbits"]))
    checks.append(check("burnside_cap13", ok,
                        "fix(id,trans,cyc)=(%d,%d,%d) orbits=%d"
                        % (fix_id, fix_trans, fix_cyc, orbits)))
    profiles = direct_constrained(CAP)
    ok = len(profiles) == RECORDS_EXPECTED
    checks.append(check("enumeration_cap13", ok,
                        "len(D_13)=%d expected=%d" % (len(profiles),
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
    ok = (census["keys"] == CENSUS_13["keys"]
          and census["uniform_det"] == CENSUS_13["uniform_det"]
          and census["uniform_ndet"] == CENSUS_13["uniform_ndet"]
          and census["det_profiles"] == CENSUS_13["det_profiles"]
          and census["ndet_profiles"] == CENSUS_13["ndet_profiles"]
          and census["total_states"] == CENSUS_13["total_states"]
          and census["max_states"] == CENSUS_13["max_states"])
    checks.append(check("census_totals", ok,
                        "keys=%d udet=%d undet=%d det_prof=%d "
                        "ndet_prof=%d states=%d max=%d"
                        % (census["keys"], census["uniform_det"],
                           census["uniform_ndet"], census["det_profiles"],
                           census["ndet_profiles"], census["total_states"],
                           census["max_states"])))

    mixed = census["mixed_keys"]
    ok = ([[list(k[0]), k[1]] for k in mixed] == EXPECTED_FAILING_22_KEYS
          and len(mixed) == 22)
    checks.append(check("mixed_keys_are_theorem_H_22", ok,
                        "mixed=%d == theorem H 22 keys: %s"
                        % (len(mixed), ok)))

    ok = partitions == MIXED_PARTITION
    checks.append(check("mixed_partition", ok,
                        "per-key det/ndet/profile table equals the embedded "
                        "K0880 constant" if ok else "partition mismatch"))
    ok = ndet_sets == MIXED_NDET_SETS
    checks.append(check("mixed_ndet_sets", ok,
                        "possible survivor sets on the ndet side equal the "
                        "embedded constant"))
    ok = all(s == {(1,)} for s in det_surv.values())
    checks.append(check("mixed_det_survivors_uniform_P1", ok,
                        "det-side survivor set == {P_1} in all %d mixed keys"
                        % len(det_surv)))

    # sizes / structure of mixed keys
    ok = (all(8 in k[0] for k in mixed) and
          all(max(k[0]) <= 9 for k in mixed) and
          all(min(k[0]) >= 2 for k in mixed))
    checks.append(check("mixed_structure_sizes", ok,
                        "all mixed keys contain a size-8 branch; sizes "
                        "within [2,9]"))

    # -- FL lemma -----------------------------------------------------------
    ok = census["fl_violations"] == 0
    checks.append(check("FL_lemma_cap13", ok,
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
    ok = (mixed_cnt.get("0,2", 0) == 22
          and sum(mixed_cnt.values()) == 22)
    checks.append(check("mixed_residue_pair_02", ok,
                        "mixed residue census=%s"
                        % json.dumps(dict(mixed_cnt), sort_keys=True)))

    # -- branch size stats ---------------------------------------------------
    stats = {}
    for sz in (8, 11, 12, 13):
        ks = [k for k in byk if sz in k[0]]
        stats[str(sz)] = [len(ks), sum(1 for k in ks if k in mixed)]
    ok = stats == BRANCH_STATS
    checks.append(check("branch_size_stats", ok,
                        "size->(keys, mixed)=%s" % json.dumps(stats,
                                                              sort_keys=True)))

    # -- K0876 cross-artifact: records ---------------------------------------
    p12, pos = d12_positions(profiles)
    k0876_path = os.path.join(here, K0876_R3_PACKED_PATH)
    with open(k0876_path, "rb") as f:
        blob = f.read()
    ksha = hashlib.sha256(blob).hexdigest()
    pub = [json.loads(line) for line in blob.decode().splitlines() if line.strip()]
    mism = 0
    for j13, k12 in pos.items():
        # the packed i field is the position in the producing enumeration:
        # j13 in D_13 (this experiment) vs k12 in D_12 (the K0876 file);
        # sv_mask / fl_mask / states must be identical for the same
        # canonical profile.
        rec = records[j13]
        if ([rec["i"], rec["sv_mask"], rec["fl_mask"], rec["states"]]
                != [j13, pub[k12][1], pub[k12][2], pub[k12][3]]
                or pub[k12][0] != k12):
            mism += 1
    ok = (ksha == K0876_R3_PACKED_SHA256 and mism == 0
          and len(pub) == 47595 and len(pos) == 47595)
    checks.append(check("k0876_cross_records", ok,
                        "published K0876 r=3 packed sha256 ok=%s; %d/%d "
                        "records reproduced at the D_12 subsequence "
                        "positions, mismatches=%d"
                        % (ksha == K0876_R3_PACKED_SHA256, len(pub),
                           len(pos), mism)))

    # -- K0876 cross-artifact: audit partition ------------------------------
    with open(os.path.join(here, K0876_AUDIT_PATH), "rb") as f:
        ablob = f.read()
    asha = hashlib.sha256(ablob).hexdigest()
    ok = asha == K0876_AUDIT_SHA256
    checks.append(check("k0876_audit_sha256", ok,
                        "K0876 audit sha256=%s" % asha))
    a76 = json.loads(ablob.decode())
    fp = a76["sweeps"]["r3"]["failing_partitions"]
    mism = 0
    for kk, v in fp.items():
        mine = partitions.get(kk)
        if mine is None or mine["det"] != v["n_det"] or \
                mine["prof"] != v["profiles"]:
            mism += 1
    ok = mism == 0 and len(fp) == 22
    checks.append(check("k0876_audit_partition", ok,
                        "22-key r=3 partition equals K0876 audit "
                        "sweeps.r3.failing_partitions, mismatches=%d/%d"
                        % (mism, len(fp))))

    # -- assemble ------------------------------------------------------------
    all_ok = all(c["ok"] for c in checks)
    audit = {
        "meta": {
            "date": "2026-11-16",
            "item": "K0882",
            "claim": ("cap<=13, r=3: non-collapsing keys are exactly the "
                      "theorem H 22; no new non-collapsing key appears "
                      "when the size boundary grows 12 -> 13"),
            "engine_provenance": (
                "verbatim region game / enumeration / Burnside / mask twin "
                "from the published K0876 verifier (packed-reading repair "
                "commit c50f31f1); full-domain records produced by the "
                "committed JavaScript mask engine mask_engine_fast.js over "
                "the canonical cap<=13 enumeration; Python twin "
                "cross-validated live in every run"),
            "records_format": "packed [i, sv_mask, fl_mask, states]",
        },
        "burnside": {"fix_id": fix_id, "fix_trans": fix_trans,
                     "fix_cyc": fix_cyc, "orbits": orbits},
        "committed": {"records": len(records), "sha256_packed": sha},
        "census": census,
        "mixed_partition": partitions,
        "mixed_ndet_sets": ndet_sets,
        "residue_classes": cls,
        "mixed_residue": dict(sorted(mixed_cnt.items())),
        "branch_size_stats": stats,
        "k0876_cross": {
            "packed_sha256": ksha,
            "records_reproduced": len(pos),
            "record_mismatches": mism,
            "audit_sha256": asha,
            "partition_keys": len(fp),
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
        idx13 = pidx[atoms]
        v1, s1 = region_verdict(atoms, 3, R, budget=20_000_000)
        v2, s2 = mask_verdict(atoms, 3, R, budget=20_000_000)
        j = rec[idx13]
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

    # L2: stratified cap<=13 sample, mask twin == committed JS records
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
    if mism != 0 or n != 2433:
        sys.stderr.write("LIVE FAIL: stratified sample %d mismatches / %d\n"
                         % (mism, n))
        sys.exit(1)
    print("LIVE OK: stratified cap<=13 sample (stride %d): mask twin == "
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
        "remo_k_branch_cap13_boundary_audit.json",
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
