#!/usr/bin/env python3
"""K1227 (provisional): independent partial cross-verification of the K0893
r=9 packed sweep records against a fresh re-computation with the K0864
verbatim Python engine, plus the K0869-lineage / K0862-lineage canonical
enumeration-order divergence record.

Self-contained verifier. Deterministic (no randomness, no wall clock, no
network). Python 3.11+ / stdlib only.

Context. K0893 published the cap<=10 r=9 full sweep as packed records
    [i, sv_mask, fl_mask, states]
whose index i refers to the K0862-lineage canonical enumeration
(direct_constrained, nesting v0,v1,v3,v2,v4,v5,v6). K0869's r=8 compact
records use a DIFFERENT canonical enumeration order (enumerate_profiles
with nesting a0,a1,a2,a3,a4,a5,a6 then max-size filter). Both enumerate
the same 15863-profile orbit set; they agree on the first 125 canonical
profiles and diverge from index 125 onward. Per-index joins across the
two lineages are therefore invalid without the atoms->index mapping
(this was initially misread as a verdict disagreement: comparing the
same i across lineages yields ~80% mismatch; no verdict disagreement
exists once profiles are matched by atoms).

This experiment re-computed r=9 verdicts for 6457 of the 15863 canonical
cap<=10 profiles with the K0864 verbatim region-game engine (independent
process, committed as output/r9_python_partial_verdicts.jsonl in the
K0869-lineage index order, atoms re-derivable from i) and compares every
snapshot record against the K0893 committed packed records under the
enumeration-order bijection phi (their_i -> my_i).

Checked claims:

C1  Burnside(10) fix counts (84494, 3478, 125) -> 15863 orbits; both
    enumerations produce 15863 profiles with identical profile SETS.
C2  The two canonical enumeration orders agree on profiles 0..124 and
    differ from index 125 onward; phi is a bijection with
    phi[k] - k == 0 for k < 125 (as DATA: the divergence point).
C3  Snapshot integrity: unique K0869-lineage indices, well-formed
    verdict fields, sha256 == pinned, count == 6457.
C4  Packed integrity: 15863 records, index-complete, masks/states
    well-formed, sha256 == pinned (byte-verified against the committed
    K0893 file research/experiments/remo-k-branch-cap10-r9-boundary-
    20261117/output/js_cap10_r9.packed.jsonl).
C5  CROSS-CHECK (the substance): for every snapshot record, the
    phi-mapped packed record has identical survivor set, identical
    first-loser set, identical determined flag. Expected: 6457/6457
    matches, 0 mismatches in each of the three fields.
C6  Pinned state-count witnesses: 13 snapshot profiles re-run live with
    the verbatim engine; (survivors, first_losers, states) must equal
    BOTH the pinned constants AND the phi-mapped packed record's
    (sv_mask, fl_mask, states) including the state count.
C7  Live engine binding: the first 12 snapshot profiles re-run live
    with the verbatim engine and compared field-by-field with the
    snapshot records (binds the committed snapshot to the engine code
    path, deterministically, fast).
C8  Snapshot anchors: FL residue lemma (first_losers == residues of
    sizes mod 9) holds on all snapshot records (K0864 proved FL
    universally; redundant anchor); Delta=0 profiles in the snapshot
    (267) all have determined survivor == Theorem D recursion at r=9.
C9  K0893 pinned census re-derived from the packed records under the
    K0862-lineage enumeration: key census 57/336/322 residue classes,
    98 uniformly determined / 583 uniformly non-determined / 34 mixed
    keys, the exact 34-key failing list, per-key partition table,
    max_states 363630. (Independent re-analysis of the committed bytes.)

Scope / limits (do not over-read):
- The cross-check is PARTIAL: 6457 of 15863 profiles (about 41%). It
  confirms agreement on everything it covers; it is not a re-proof of
  K0893 (whose own verifier covers the full domain differently).
- Order-determinacy fields are NOT cross-checked (the JS mask engine
  does not reproduce elimination orders; K0893 records the same limit).
- No r, cap, or board claim changes: all K0893/K0869 claims stand as
  published. This item adds an independent partial verification and
  an interoperability rule (joins across packed/compact generations
  must be by atoms or via an explicit index mapping, never by raw i).
- 11x11 empty board / class frontiers remain UNKNOWN.
"""

import hashlib
import json
import os
import sys

sys.setrecursionlimit(100000)

R = 9
CAP = 10
N_PROFILES = 15863
N_SNAPSHOT = 6457

# pinned digests (committed files this verifier binds together)
PINNED_SNAPSHOT_SHA256 = {"expected": "f8fffc4602e3efa62ccf7d726c53a87f6f6bc7614dc90a610db8da9f65640e06"}
PINNED_PACKED_SHA256 = {"expected": "a2bb16bc8d03f341704d902f0a50ce4352b14ad08043cbced54b8e8f83b9973b"}

# pinned 13 (my_i, sv_mask, fl_mask, states) witnesses computed with the
# verbatim engine in an independent process (see README)
PINNED_STATES_WITNESSES = [
    [120, 378, 162, 30612], [121, 362, 146, 6260], [122, 42, 33, 5327],
    [123, 288, 66, 36594], [124, 314, 98, 8562], [125, 3, 6, 26],
    [126, 2, 12, 66], [127, 14, 24, 125], [128, 10, 48, 197],
    [129, 58, 96, 300], [130, 42, 192, 410], [131, 58, 384, 555],
    [132, 184, 257, 715],
]

# K0893 published pinned constants (verbatim from
# verify_remo_k_branch_cap10_r9_boundary.py R9_SWEEP / R9_PARTITIONS /
# K0872_R9_PREFILTER) re-derived here from the committed packed bytes.
K0893_FAILING_KEYS = [[[6, 6, 8], 0], [[6, 6, 8], 1], [[6, 6, 8], 2], [[6, 6, 8], 3], [[6, 6, 8], 4], [[6, 6, 9], 0], [[6, 6, 9], 1], [[6, 6, 9], 2], [[6, 6, 9], 3], [[6, 8, 8], 0], [[6, 8, 8], 1], [[6, 8, 8], 2], [[6, 8, 8], 3], [[6, 8, 8], 4], [[6, 8, 9], 0], [[6, 8, 9], 1], [[6, 8, 9], 2], [[6, 8, 9], 3], [[6, 9, 9], 0], [[6, 9, 9], 1], [[6, 9, 9], 2], [[6, 9, 9], 3], [[8, 8, 9], 0], [[8, 8, 9], 1], [[8, 8, 9], 2], [[8, 8, 9], 3], [[8, 8, 9], 4], [[8, 8, 9], 5], [[8, 9, 9], 0], [[8, 9, 9], 1], [[8, 9, 9], 2], [[8, 9, 9], 3], [[8, 9, 9], 4], [[8, 9, 9], 5]]
K0893_PARTITIONS = {"6,6,8|0": [48, 3, 51], "6,6,8|1": [30, 3, 33], "6,6,8|2": [16, 3, 19], "6,6,8|3": [7, 3, 10], "6,6,8|4": [2, 2, 4], "6,6,9|0": [40, 14, 54], "6,6,9|1": [22, 12, 34], "6,6,9|2": [10, 10, 20], "6,6,9|3": [3, 7, 10], "6,8,8|0": [63, 3, 66], "6,8,8|1": [42, 3, 45], "6,8,8|2": [24, 3, 27], "6,8,8|3": [13, 3, 16], "6,8,8|4": [4, 3, 7], "6,8,9|0": [95, 25, 120], "6,8,9|1": [53, 25, 78], "6,8,9|2": [24, 23, 47], "6,8,9|3": [6, 19, 25], "6,9,9|0": [64, 14, 78], "6,9,9|1": [40, 14, 54], "6,9,9|2": [19, 14, 33], "6,9,9|3": [6, 14, 20], "8,8,9|0": [92, 8, 100], "8,8,9|1": [62, 8, 70], "8,8,9|2": [40, 8, 48], "8,8,9|3": [22, 8, 30], "8,8,9|4": [10, 8, 18], "8,8,9|5": [3, 6, 9], "8,9,9|0": [102, 8, 110], "8,9,9|1": [72, 8, 80], "8,9,9|2": [46, 8, 54], "8,9,9|3": [28, 8, 36], "8,9,9|4": [13, 8, 21], "8,9,9|5": [4, 8, 12]}
K0893_CENSUS = {"single_residue": 57, "two_residue": 336, "three_residue": 322,
                "uniformly_determined": 98, "uniformly_ndet": 583, "mixed": 34,
                "max_states": 363630}

# ---------------------------------------------------------------------------
# verbatim engine block: K0864 region game (via the K0869 published verifier)
# ---------------------------------------------------------------------------


class Budget(Exception):
    pass


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
    return tuple(
        sum(atoms[m - 1] for m in range(1, 1 << k) if (m >> (i - 1)) & 1)
        for i in range(1, k + 1)
    )


def check_profile(atoms, k):
    for i in range(1, k + 1):
        assert atoms[(1 << (i - 1)) - 1] >= 1, "singleton atom must be nonempty"
    return profile_sizes(atoms, k)


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


# ---------------------------------------------------------------------------
# enumeration A: K0869-lineage canonical order (enumerate_profiles with the
# max-size filter inlined as safe pruning; emitted sequence identical to the
# verbatim enumerate_profiles(3*cap)+filter -- filter fate is rep-invariant
# and pruning only removes candidates whose partial branch sizes already
# exceed cap; validated offline against the verbatim construction).
# ---------------------------------------------------------------------------


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


# branch incidence: atom index -> branches it feeds (k=3)
_ATOM_BRANCHES = [
    (0,), (1,), (0, 1), (2,), (0, 2), (1, 2), (0, 1, 2),
]


def enumerate_A_pruned(cap, k=3):
    """K0869-lineage canonical order, pruned verbatim-equivalent traversal.

    Same atom-index nesting order and value order as the K0869 verifier's
    enumerate_profiles (rec over atom indices 0..6 with singleton lower
    bound 1 at indices 0,1,3), same first-occurrence dedup by orbit
    representative; candidates whose partial branch sizes already
    exceed cap are pruned (they can never pass the max-size filter, and
    no kept profile can share a representative with a pruned candidate
    because sizes are representative-invariant).
    """
    perms = branch_perms(k)
    seen = set()
    profiles = []
    atoms = [0] * ((1 << k) - 1)
    partial = [0] * k  # partial per-branch sizes
    singles = {0, 1, 3}

    def rec(idx):
        if idx == (1 << k) - 1:
            rep = orbit_representative(tuple(atoms), k, perms)
            if rep not in seen:
                seen.add(rep)
                profiles.append(rep)
            return
        lo = 1 if idx in singles else 0
        branches = _ATOM_BRANCHES[idx]
        # total already placed bounds the remaining atoms below:
        # every remaining branch size only grows. upper bound via 3*cap
        # is not needed: prune a value as soon as any fed branch
        # exceeds cap.
        for v in range(lo, 3 * cap + 1):
            ok = True
            for b in branches:
                if partial[b] + v > cap:
                    ok = False
                    break
            if not ok:
                break
            atoms[idx] = v
            for b in branches:
                partial[b] += v
            rec(idx + 1)
            for b in branches:
                partial[b] -= v
        atoms[idx] = 0

    rec(0)
    # the verbatim filter keeps max(branch sizes) <= cap; the pruned
    # traversal only ever extends branches up to cap, so no final
    # filter is needed - but assert the invariant anyway.
    for rep in profiles:
        assert max(profile_sizes(rep, k)) <= cap
    return profiles


# ---------------------------------------------------------------------------
# enumeration B: K0862-lineage canonical order (verbatim direct_constrained,
# as published inside the K0893 verifier)
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# verifier
# ---------------------------------------------------------------------------


def sha256_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def load_snapshot(path):
    out = {}
    for line in open(path, "r", encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        assert rec["i"] not in out, "duplicate snapshot index"
        out[rec["i"]] = rec
    return out


def load_packed(path):
    out = {}
    for line in open(path, "r", encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        i, sv, fl, states = json.loads(line)
        assert i not in out, "duplicate packed index"
        assert 0 <= sv < (1 << R) and 0 <= fl < (1 << R)
        assert states > 0
        out[i] = (sv, fl, states)
    return out


def build_checks():
    checks = []

    def record(name, ok, data):
        checks.append({"name": name, "ok": bool(ok), "data": data})

    here = os.path.dirname(os.path.abspath(__file__))
    snap_path = os.path.join(here, "output", "r9_python_partial_verdicts.jsonl")
    # packed records: committed K0893 file, referenced relative to repo root
    packed_candidates = [
        os.path.join(here, "..",
                     "remo-k-branch-cap10-r9-boundary-20261117",
                     "output", "js_cap10_r9.packed.jsonl"),
        os.path.join(here, "input", "js_cap10_r9.packed.jsonl"),
    ]
    packed_path = next((p for p in packed_candidates if os.path.exists(p)), None)
    assert packed_path is not None, "K0893 packed records not found"

    # ---- C1: Burnside + two enumerations + set equality
    fi, ft, fc, orbits = burnside_fix_counts(CAP)
    profA = enumerate_A_pruned(CAP)
    profB = direct_constrained(CAP)
    set_eq = set(profA) == set(profB)
    record(
        "C1 Burnside(10) (fix %d/%d/%d -> %d orbits) == enumeration A "
        "(K0869-lineage, pruned verbatim-equivalent traversal, %d) == "
        "enumeration B (K0862-lineage direct_constrained, %d) with "
        "identical profile SETS" % (fi, ft, fc, orbits, len(profA), len(profB)),
        orbits == len(profA) == len(profB) == N_PROFILES and set_eq,
        {"orbits": orbits, "len_A": len(profA), "len_B": len(profB),
         "sets_equal": set_eq},
    )

    # ---- C2: first divergence point 125 (data); phi bijection
    smA = {a: i for i, a in enumerate(profA)}
    phi = [smA[a] for a in profB]     # phi[their_i] = my_i
    inv = {phi[t]: t for t in range(len(phi))}
    agree_prefix = 0
    while agree_prefix < N_PROFILES and phi[agree_prefix] == agree_prefix:
        agree_prefix += 1
    # number of indices where the offset changes
    offsets = [phi[t] - t for t in range(len(phi))]
    n_changes = sum(1 for t in range(1, len(offsets))
                    if offsets[t] != offsets[t - 1])
    record(
        "C2 enumeration-order divergence (DATA): the two published "
        "canonical enumerations agree on indices 0..%d and diverge from "
        "index %d onward (%d offset-change points); phi is a bijection "
        "[their_i -> my_i] over all %d profiles" % (
            agree_prefix - 1, agree_prefix, n_changes, len(phi)),
        agree_prefix == 125 and len(inv) == N_PROFILES
        and sorted(phi) == list(range(N_PROFILES)),
        {"agree_prefix": agree_prefix, "offset_change_points": n_changes},
    )

    # ---- C3: snapshot integrity
    snap = load_snapshot(snap_path)
    h = sha256_file(snap_path)
    ok_fields = all(
        isinstance(rec["i"], int) and 0 <= rec["i"] < N_PROFILES
        and isinstance(rec["d"], bool) and isinstance(rec["od"], bool)
        and rec["d"] == (len(rec["s"]) == 1)
        and sorted(set(rec["s"])) == rec["s"]
        and sorted(set(rec["fl"])) == rec["fl"]
        and all(0 <= p < R for p in rec["s"] + rec["fl"])
        for rec in snap.values())
    # atoms re-derivation: snapshot indices must map to real profiles
    ok_atoms = all(tuple(profA[i]) is not None for i in snap)
    record(
        "C3 snapshot integrity: %d unique K0869-lineage-indexed records, "
        "well-formed verdict fields, sha256 %s" % (
            len(snap), h[:16]),
        len(snap) == N_SNAPSHOT and ok_fields and ok_atoms
        and h == PINNED_SNAPSHOT_SHA256["expected"],
        {"records": len(snap), "sha256": h},
    )

    # ---- C4: packed integrity
    packed = load_packed(packed_path)
    hp = sha256_file(packed_path)
    idx_ok = sorted(packed) == list(range(N_PROFILES))
    record(
        "C4 K0893 packed integrity: 15863 records, index-complete, "
        "masks/states well-formed, sha256 %s (byte-verified against the "
        "committed K0893 publication)" % hp[:16],
        len(packed) == N_PROFILES and idx_ok and hp == PINNED_PACKED_SHA256["expected"],
        {"records": len(packed), "sha256": hp},
    )

    # ---- C5: THE cross-check
    m_sv = m_fl = m_det = 0
    n_cmp = 0
    for my_i, rec in snap.items():
        t = inv[my_i]
        sv, fl, states = packed[t]
        n_cmp += 1
        if rec["s"] != [p for p in range(R) if (sv >> p) & 1]:
            m_sv += 1
        if rec["fl"] != [p for p in range(R) if (fl >> p) & 1]:
            m_fl += 1
        if rec["d"] != (bin(sv).count("1") == 1):
            m_det += 1
    record(
        "C5 CROSS-CHECK: all %d snapshot records (fresh K0864 verbatim "
        "Python engine, independent process) agree with the phi-mapped "
        "K0893 packed records on survivors / first losers / determined "
        "(mismatches %d/%d/%d)" % (n_cmp, m_sv, m_fl, m_det),
        n_cmp == N_SNAPSHOT and m_sv == 0 and m_fl == 0 and m_det == 0,
        {"compared": n_cmp, "sv_mismatch": m_sv, "fl_mismatch": m_fl,
         "det_mismatch": m_det},
    )

    # ---- C6: pinned states witnesses (live verbatim engine)
    fail6 = 0
    for my_i, sv_w, fl_w, st_w in PINNED_STATES_WITNESSES:
        atoms = profA[my_i]
        v, states = region_verdict(atoms, 3, R, budget=20_000_000)
        sv_m = sum(1 << p for p in v["survivors"])
        fl_m = sum(1 << p for p in v["first_losers"])
        t = inv[my_i]
        sv_p, fl_p, st_p = packed[t]
        if not (v is not None and sv_m == sv_w == sv_p and fl_m == fl_w == fl_p
                and states == st_w == st_p):
            fail6 += 1
    record(
        "C6 pinned state-count witnesses: 13 snapshot profiles re-run "
        "live with the verbatim engine; (survivors, first_losers, states) "
        "equal the pinned constants AND the phi-mapped packed records "
        "including the reachable-state count (%d failures)" % fail6,
        fail6 == 0,
        {"witnesses": len(PINNED_STATES_WITNESSES), "failures": fail6},
    )

    # ---- C7: live engine binding on first 12 snapshot records
    fail7 = 0
    sample = sorted(snap)[:12]
    for my_i in sample:
        atoms = profA[my_i]
        v, _ = region_verdict(atoms, 3, R, budget=20_000_000)
        rec = snap[my_i]
        if not (v["determined"] == rec["d"]
                and v["survivors"] == rec["s"]
                and v["first_losers"] == rec["fl"]
                and v["order_determined"] == rec["od"]
                and (v["orders"][0] if v["order_determined"] else None) == rec["o0"]):
            fail7 += 1
    record(
        "C7 live engine binding: first 12 snapshot records re-run with "
        "the verbatim engine match all committed fields incl. order "
        "fields (%d failures)" % fail7,
        fail7 == 0,
        {"sample": len(sample), "failures": fail7},
    )

    # ---- C8: snapshot anchors (FL residues + Delta=0 Theorem D)
    fl_v = 0
    d0 = d0m = 0
    for my_i, rec in snap.items():
        sizes = profile_sizes(profA[my_i], 3)
        if rec["fl"] != sorted({c % R for c in sizes}):
            fl_v += 1
        if len(set(sizes)) == 1:
            d0 += 1
            _, surv = theorem_d(sizes[0], R)
            if not (rec["d"] and rec["s"] == [surv]):
                d0m += 1
    record(
        "C8 snapshot anchors: Lemma FL residues hold on all %d snapshot "
        "records (%d violations; K0864 proved FL universally - redundant "
        "anchor); the %d Delta=0 profiles in the snapshot all have "
        "determined survivor == Theorem D recursion at r=9 (%d mismatches)"
        % (len(snap), fl_v, d0, d0m),
        fl_v == 0 and d0m == 0,
        {"fl_violations": fl_v, "delta0_profiles": d0, "delta0_mismatches": d0m},
    )

    # ---- C9: K0893 census re-derived from packed bytes under enumeration B
    byk = {}
    for i, atoms in enumerate(profB):
        byk.setdefault(key_of(atoms), []).append(i)
    assert len(byk) == 715
    failing = sorted(k for k, rs in byk.items()
                     if len({bin(packed[i][0]).count("1") == 1 for i in rs}) > 1)
    failing_list = sorted([[list(k[0]), k[1]] for k in failing])
    part = {}
    for k in failing:
        rs = byk[k]
        ndet = sum(1 for i in rs if bin(packed[i][0]).count("1") != 1)
        part[kstr(k)] = [len(rs) - ndet, ndet, len(rs)]
    part_ok = all(part.get(kk) == v for kk, v in K0893_PARTITIONS.items())
    uni_det = sum(1 for k, rs in byk.items()
                  if {bin(packed[i][0]).count("1") == 1 for i in rs} == {True})
    uni_ndet = sum(1 for k, rs in byk.items()
                   if {bin(packed[i][0]).count("1") == 1 for i in rs} == {False})
    census = {}
    for k in byk:
        n = len({c % R for c in k[0]})
        census[str(n)] = census.get(str(n), 0) + 1
    max_states = max(v[2] for v in packed.values())
    record(
        "C9 K0893 pinned census re-derived from the committed packed "
        "bytes under the K0862-lineage enumeration: failing keys exactly "
        "the published %d-key set; all 34 partition rows match; census "
        "%s; uniformly determined %d / non-determined %d / mixed %d; "
        "max_states %d" % (
            len(K0893_FAILING_KEYS),
            "/".join(str(census.get(k, "?")) for k in ("1", "2", "3")),
            uni_det, uni_ndet, len(failing_list), max_states),
        failing_list == sorted(K0893_FAILING_KEYS) and part_ok
        and len(part) == len(K0893_PARTITIONS)
        and census == {"1": K0893_CENSUS["single_residue"],
                       "2": K0893_CENSUS["two_residue"],
                       "3": K0893_CENSUS["three_residue"]}
        and uni_det == K0893_CENSUS["uniformly_determined"]
        and uni_ndet == K0893_CENSUS["uniformly_ndet"]
        and len(failing_list) == K0893_CENSUS["mixed"]
        and max_states == K0893_CENSUS["max_states"],
        {"failing": len(failing_list), "uniformly_determined": uni_det,
         "uniformly_ndet": uni_ndet,
         "residue_census": census, "max_states": max_states},
    )

    return checks


def run():
    checks = build_checks()
    audit = {
        "meta": {
            "item": "K1227-provisional",
            "title": "Independent partial cross-verification of the "
                     "K0893 r=9 packed records with the K0864 verbatim "
                     "engine + K0869/K0862 enumeration-order divergence "
                     "record",
            "date": "2026-11-22",
            "snapshot_records": N_SNAPSHOT,
            "domain": "cap<=10 3-branch REMO r=9, 15863 canonical "
                      "profiles (partial snapshot %d / 15863)" % N_SNAPSHOT,
        },
        "machine_checks": checks,
        "summary": {
            "all_ok": all(c["ok"] for c in checks),
            "checks_total": len(checks),
        },
    }
    blob = json.dumps(audit, sort_keys=True, ensure_ascii=False, indent=1) + "\n"
    here = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(here, "output", "crosscheck_r9_partial_audit.json")
    committed = None
    if os.path.exists(out_path):
        with open(out_path, "r", encoding="utf-8") as f:
            committed = f.read()
    if committed is not None:
        if committed != blob:
            sys.stderr.write("FATAL: regenerated audit differs from "
                             "committed file\n")
            sys.exit(1)
        print("audit byte-identical")
    else:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(blob)
        print("wrote audit")
    print("AUDIT PASSED" if audit["summary"]["all_ok"] else "AUDIT FAILED")
    for c in checks:
        print("  [%s] %s" % ("ok" if c["ok"] else "NG", c["name"]))
    if not audit["summary"]["all_ok"]:
        sys.exit(1)


if __name__ == "__main__":
    run()
