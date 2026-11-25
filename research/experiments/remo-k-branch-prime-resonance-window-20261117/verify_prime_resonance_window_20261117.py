#!/usr/bin/env python3
"""K-prime-resonance-window (provisional item number, see report): THEOREM
PRW, the prime resonance window of the three-branch REMO determinacy.

For every canonical key K = (sizes, gamma) of the cap<=12 canonical
domain (47,595 profiles / 1,365 keys, K0875 Burnside machinery) whose
branch sizes all lie in {2,3,5,7,11} and which is NOT Delta=0 (94
keys: 43 with M = max C_i <= 10, 51 with M = 11), let m = min C_i and
M = max C_i.  THEOREM PRW (universal in r, all r >= 2):

    K is uniformly determined at r (every canonical profile of K
    determined)  <=>  r < m  or  r >= M.

Equivalently: on the resonance window [m, M-1] K is uniformly
NON-determined, and at NO r >= 2 is a prime-size key ever MIXED (for
every r, all profiles of K share one determinacy status).  The
survivor refinement pinned here (finite observation beyond the r=2..6
universality of G', K0864): every determined profile carries the
chain survivor; uniformly P_0 below the window (r < m), uniformly P_1
at/above the anchor (r >= M, Theorem J makes the r=M sv the value
for all r >= M).

Assembly (no new sweep; three committed elements + one universal
theorem):
(1) Theorem J (K0906, proved universal): per-profile det/sv are
    constant for r >= max(M,2); so the uniformly determined anchor
    column at r = M (committed r=2..9 columns for the 43 cap<=10
    keys since M <= 7; the committed K0920 r=11 focus column for the
    51 prime-11 keys) fixes det/sv for ALL r >= M.
(2) The fixed-point dichotomy side (r >= M) is Theorem PD (K0916)
    for the 43 cap<=10 keys and Theorem PD12 (K0920) for the 51
    prime-11 keys; PRW re-derives both sides independently from the
    raw committed columns below.
(3) The finite window r < M is completely covered by data: r=2..9
    from the 8 committed cap<=12 columns (K0881/K0876/K0912) and,
    for the 51 prime-11 keys, r=10 from the committed K0920 focus
    column (window top) and r=11 (anchor) from the r=11 focus
    column.  728 (key, r) pairs are checked in full (all profiles of
    the key in the column).
(4) Theorem E' (K0861) transfers every profile verdict to all
    realizing boards.

Complementarity pinned here (finite observations):
- EXO: the exotic11 pair (1,1,11)|0, (1,11,11)|0 is the exact
  ANTI-mirror: uniformly determined with survivor P_0 on ALL of
  r=2..10 (m=1 would put the whole range in the PRW window; instead
  it is determined there) and uniformly non-determined from r=M=11
  (sv mask 0b11), i.e. det <=> r < M.  Prime resonance is not a
  low-r tautology.
- COR: the 34 mixed keys of the cap<=12 r=9 boundary (K0893/K0912)
  re-derived from the raw r=9 column contain no all-prime-size key
  (0), consistent with "prime keys are never mixed".
- DORM: the K0916 dormancy-window shapes {2,3,4} / {2,..,6} are the
  m=5 / m=7 det-prefixes of PRW; the prime-11 dormancy prefixes are
  det exactly on [2, m-1] by m in {2,3,5,7} (statuses pinned).

Self-contained verifier (stdlib only, deterministic, no network, no
new machine columns).  Inputs: 10 sha256-pinned committed packed
columns (8 cap<=12 r=2..9 published in the K0881/K0876/K0912
experiment dirs + the 2 K0920 focus columns), all read-only.  The
Python mask twin is the verbatim K0912 machinery block (twin of
record via K0893).

Checked claims (audit JSON carries the tables):

PIN   10 input columns match pinned sha256 and line counts.
B     Burnside cap12 (261749,7805,203) -> 47595 orbits; 1365 keys;
      canonical enumeration re-derived.
TAX   94 prime keys (43 cap<=10 + 51 prime-11); m/M census
      {2,3:4, 2,5:6, 2,7:8, 2,11:10, 3,5:6, 3,7:9, 3,11:12,
      5,7:10, 5,11:15, 7,11:14}; 1664 prime profiles (393 + 1271);
      30 multisets with per-multiset profile counts pinned.
FOC   K0920 focus columns: 1619 records each, same index set,
      cover ALL profiles of the 51 prime-11 keys.
PRW   THEOREM: 728 (key, r) pairs (218 cap<=10 + 510 prime-11)
      checked in full against the law (det <=> r<m or r=M, ndet on
      [m, M-1]); 0 violations; 0 MIXED cells.
SV    all 266 det cases: sv uniform over the key's profiles AND ==
      chain record sv (0 mismatches); below-window sv mask == P_0
      (172 cases), anchor sv mask == P_1 (94 cases).
FL    fl == OR{1 << (C_i mod r)} on all 14,882 used records
      (Lemma FL redundant anchor, 0 violations).
J     cap<=10 keys: per-profile sv/det constant on r in [M, 9]
      (1,365 profile-column records, 0 mismatches) - the finite
      anchor of the Theorem-J side.
EXO   exotic11 anti-mirror (12 profiles x r=2..11): uniform det
      sv=P_0 on r=2..10, uniform ndet sv mask 0b11 at r=11.
COR   mixed keys of the r=9 boundary re-derived: exactly 34, none
      all-prime-size.
DORM  prime-11 dormancy prefixes by m pinned (m=2: none; m=3: {2};
      m=5: {2,3,4}; m=7: {2,..,6}); ndet elsewhere on r<=10.
P11S  K0920's graded dormancy series 90/273/273/704/704 (r=7..10
      full 1271) is exactly the cumulative profile count over keys
      with m <= r - the family grading is a superposition of
      per-key uniform statuses, no key is actually mixed.
LIVE  Python mask twin (independent implementation, verbatim block)
      recomputes 329 records (chain profile of every key at r=2,
      r=m, r=M, every prime-11 chain and lightest profile at the
      r=10 window top, lightest profile at r=m per key, all 12
      exotic11 profiles at r=10/11): verdict equality AND twin
      state count == engine states on every record.

Limits: universal in r only through Theorem J (K0906); sizes <= 12
(the {2,3,5,7,11} description is a finite set inside cap<=12 and
primality is NOT claimed as the mechanism); the r < M side is a
complete finite check, not a proof for sizes >= 13; the survivor
levels P_0/P_1 below/above the window are finite observations
beyond the r=2..6 universality of G' (K0864); mixed-free-ness of
prime keys at r > 11 follows from Theorem J + the uniform anchor
(det constant per profile, uniform at the anchor), stated as
assembly, not as an independent sweep; ranking determinacy and the
11x11 frontier are untouched (UNKNOWN).
"""

import hashlib
import json
import os
import sys

sys.setrecursionlimit(100000)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")
AUDIT_PATH = os.path.join(OUT, "prime_resonance_window_audit.json")
E = os.path.join(HERE, "..")

# committed cap<=12 packed columns r=2..9 (published: K0881 r=2,7,8 /
# K0876 r=3..6 / K0912 r=9)
COMMITTED_PINS = {
    # r: (path relative to research/experiments/, sha256, line count)
    2: ("remo-k-branch-cap12-r278-boundary-20261116/output/js_cap12_r2.packed.jsonl",
        "1fd9dbf4cb6699c26bab7f6b34a900f5877d3408603a02a2dd121ca71ef8e951", 47595),
    3: ("remo-k-branch-cap12-r456-boundary-20261116/output/js_cap12_r3.packed.jsonl",
        "ea7c66286f728a52d5696d627ce1faf7705e77f9e4222493221f3a4fe79ed134", 47595),
    4: ("remo-k-branch-cap12-r456-boundary-20261116/output/js_cap12_r4.packed.jsonl",
        "04caba43a7c0f7124db1ea81fcad4f170de04bd041699f6659e42f786e9a40b4", 47595),
    5: ("remo-k-branch-cap12-r456-boundary-20261116/output/js_cap12_r5.packed.jsonl",
        "c6dddad7a4ce39d3ebc8765187b0f16961720654918d74f54e608e12975ea693", 47595),
    6: ("remo-k-branch-cap12-r456-boundary-20261116/output/js_cap12_r6.packed.jsonl",
        "65f1cb32a9ecae6bd258056dfe8ab7c59d376d570f1d11c647b6823fd2467f1d", 47595),
    7: ("remo-k-branch-cap12-r278-boundary-20261116/output/js_cap12_r7.packed.jsonl",
        "50eb7c1ba41825dcbf726258cb2c6878a324d58bb17a708cb587d9d2b3b79c78", 47595),
    8: ("remo-k-branch-cap12-r278-boundary-20261116/output/js_cap12_r8.packed.jsonl",
        "0a884b490e28c281166754c1e82aaa73f7515580dea05b4ce023e8a1f079e8dc", 47595),
    9: ("remo-k-branch-cap12-r9-boundary-20261117/output/js_cap12_r9.packed.jsonl",
        "02e771cda84ae5178ee67a905cc9c2148e0c186790cf0562f569d9923110f32d", 47595),
}

# committed K0920 focus columns (prime-11 + exotic11 candidates,
# full profiles; published in the prime-dichotomy-cap12 experiment)
FOCUS_PINS = {
    # name: (path relative to research/experiments/, sha256, records, r)
    "r11_focus": ("remo-k-branch-prime-dichotomy-cap12-20261117/output/packed_r11_focus.jsonl",
                  "8daa1cfa634af48a511fcfb1c9389eda03c05fd2deee501829caf99235c2daeb", 1619, 11),
    "r10_focus": ("remo-k-branch-prime-dichotomy-cap12-20261117/output/packed_r10_focus.jsonl",
                  "3face607a59c559941bcb58d2b1bdaea05132c33a1af8a891ab254983a445ac1", 1619, 10),
}

PRIMES = (2, 3, 5, 7, 11)

EXPECTED = {
    "burnside": {"fix_id": 261749, "fix_trans": 7805, "fix_cyc": 203,
                 "orbits": 47595, "keys": 1365},
    "prime_keys": {"total": 94, "cap10": 43, "p11": 51},
    "mm_census": {"2,3": 4, "2,5": 6, "2,7": 8, "2,11": 10,
                  "3,5": 6, "3,7": 9, "3,11": 12,
                  "5,7": 10, "5,11": 15, "7,11": 14},
    "profiles": {"total": 1664, "cap10": 393, "p11": 1271},
    "multiset_profiles": {
        "2,2,3": 5, "2,2,5": 5, "2,2,7": 5, "2,2,11": 5, "2,3,3": 7,
        "2,3,5": 10, "2,3,7": 10, "2,3,11": 10, "2,5,5": 13,
        "2,5,7": 18, "2,5,11": 18, "2,7,7": 19, "2,7,11": 26,
        "2,11,11": 31, "3,3,5": 15, "3,3,7": 15, "3,3,11": 15,
        "3,5,5": 26, "3,5,7": 40, "3,5,11": 40, "3,7,7": 40,
        "3,7,11": 60, "3,11,11": 68, "5,5,7": 67, "5,5,11": 70,
        "5,7,7": 98, "5,7,11": 175, "5,11,11": 186, "7,7,11": 207,
        "7,11,11": 360},
    "pairs": {"total": 728, "cap10": 218, "p11": 510, "det": 266,
              "det_below_m": 172, "det_anchor": 94},
    "sv": {"below_m_mask": 1, "anchor_mask": 2},
    "fl": {"records": 14882, "violations": 0},
    "j_cap10": {"records": 1365, "mismatches": 0},
    "exo": {"profiles": 12, "det_through_r10": True, "sv10_mask": 1,
            "ndet_r11": True, "sv11_mask": 3},
    "cor": {"mixed_r9": 34, "allprime_mixed": 0},
    "p11_series": {2: 90, 3: 273, 4: 273, 5: 704, 6: 704, 7: 1271,
                   8: 1271, 9: 1271, 10: 1271},
    "dorm": {"m2_det_prefix": [], "m3_det_prefix": [2],
             "m5_det_prefix": [2, 3, 4], "m7_det_prefix": [2, 3, 4, 5, 6]},
    "live": {"records": 329, "mismatches": 0, "nodes_eq_states": True,
             "max_states": 9271},
}

EXOTIC11 = [((1, 1, 11), 0), ((1, 11, 11), 0)]

# ====PINNED====
# ---------------------------------------------------------------------------
# verbatim K0912 machinery block (K0875 enumeration / Burnside / Theorem D
# / mask twin; twin of record via K0893 - see file header)
# ---------------------------------------------------------------------------;
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
# helpers (this experiment)
# ---------------------------------------------------------------------------

def sha256_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def load_col(path):
    out = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                i, sv, fl, st = json.loads(line)
                out[i] = (sv, fl, st)
    return out


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

    # ---- load pinned columns
    cols = {}
    pin_ok = True
    pin_detail = {"committed": {}, "focus": {}}
    for r, (rel, sha, n) in sorted(COMMITTED_PINS.items()):
        p = os.path.normpath(os.path.join(E, rel))
        got = sha256_file(p)
        col = load_col(p)
        idx_ok = sorted(col) == list(range(n))
        pin_ok = pin_ok and got == sha and len(col) == n and idx_ok
        cols[r] = col
        pin_detail["committed"]["r%d" % r] = {
            "sha256": got, "lines": len(col), "index_contiguous": idx_ok}
    foc = {}
    for name, (rel, sha, n, rr) in sorted(FOCUS_PINS.items()):
        p = os.path.normpath(os.path.join(E, rel))
        got = sha256_file(p)
        col = load_col(p)
        idx_ok = len(col) == n
        pin_ok = pin_ok and got == sha and len(col) == n and idx_ok
        foc[name] = col
        pin_detail["focus"][name] = {"sha256": got, "lines": len(col),
                                     "r": rr, "indices_unique": idx_ok}
    record("PIN: 8 committed cap<=12 columns r=2..9 + 2 committed K0920 "
           "focus columns (r=10/11) sha256/shape", pin_ok, pin_detail)

    def col_for(r):
        if r <= 9:
            return cols[r]
        if r == 10:
            return foc["r10_focus"]
        if r == 11:
            return foc["r11_focus"]
        raise ValueError(r)

    # ---- B: Burnside vs direct enumeration
    fix_id, fix_trans, fix_cyc, orbits = burnside_fix_counts(12)
    b_ok = ((fix_id, fix_trans, fix_cyc, orbits) ==
            (EXPECTED["burnside"]["fix_id"], EXPECTED["burnside"]["fix_trans"],
             EXPECTED["burnside"]["fix_cyc"], EXPECTED["burnside"]["orbits"]))
    profiles = direct_constrained(12)
    b_ok = b_ok and len(profiles) == EXPECTED["burnside"]["orbits"]
    allkeys = {}
    for i, at in enumerate(profiles):
        allkeys.setdefault(key_of(at), []).append(i)
    b_ok = b_ok and len(allkeys) == EXPECTED["burnside"]["keys"]
    record("B: Burnside cap12 (261749,7805,203)->47595 orbits; 1365 keys",
           b_ok, {"fix": [fix_id, fix_trans, fix_cyc], "orbits": orbits,
                  "keys": len(allkeys)})

    # ---- TAX: the 94 prime keys
    prime_keys = sorted(k for k in allkeys
                        if len(set(k[0])) > 1
                        and all(s in PRIMES for s in k[0]))
    cap10 = [k for k in prime_keys if max(k[0]) <= 10]
    p11 = [k for k in prime_keys if max(k[0]) == 11]
    tax_ok = (len(prime_keys) == EXPECTED["prime_keys"]["total"] and
              len(cap10) == EXPECTED["prime_keys"]["cap10"] and
              len(p11) == EXPECTED["prime_keys"]["p11"])
    mm = {}
    for k in prime_keys:
        mm_key = "%d,%d" % (min(k[0]), max(k[0]))
        mm[mm_key] = mm.get(mm_key, 0) + 1
    tax_ok = tax_ok and mm == EXPECTED["mm_census"]
    prof_total = sum(len(allkeys[k]) for k in prime_keys)
    prof_cap10 = sum(len(allkeys[k]) for k in cap10)
    prof_p11 = sum(len(allkeys[k]) for k in p11)
    tax_ok = (tax_ok and
              prof_total == EXPECTED["profiles"]["total"] and
              prof_cap10 == EXPECTED["profiles"]["cap10"] and
              prof_p11 == EXPECTED["profiles"]["p11"])
    ms_prof = {}
    for k in prime_keys:
        ms = ",".join(map(str, sorted(k[0])))
        ms_prof[ms] = ms_prof.get(ms, 0) + len(allkeys[k])
    tax_ok = tax_ok and ms_prof == EXPECTED["multiset_profiles"]
    record("TAX: 94 prime keys (43 cap<=10 + 51 prime-11); m/M census; "
           "1664 = 393 + 1271 profiles; 30 multisets with per-multiset "
           "profile counts", tax_ok,
           {"keys": len(prime_keys), "cap10": len(cap10), "p11": len(p11),
            "mm_census": mm, "profiles": prof_total,
            "multiset_profiles": ms_prof})

    # ---- FOC: focus columns cover all prime-11 profiles
    foc_ok = (len(foc["r11_focus"]) == 1619 and
              len(foc["r10_focus"]) == 1619 and
              set(foc["r11_focus"]) == set(foc["r10_focus"]))
    n_cover = 0
    for k in p11:
        for i in allkeys[k]:
            if i in foc["r11_focus"] and i in foc["r10_focus"]:
                n_cover += 1
            else:
                foc_ok = False
    foc_ok = foc_ok and n_cover == EXPECTED["profiles"]["p11"]
    record("FOC: K0920 focus columns (1619 each, same index set) cover "
           "ALL 1271 profiles of the 51 prime-11 keys", foc_ok,
           {"covered": n_cover, "focus_records": len(foc["r11_focus"])})

    # ---- PRW: the resonance-window law, full check on r=2..M
    law_viol = 0
    mixed_cells = 0
    pairs = 0
    det_cases = 0
    det_below_m = 0
    det_anchor = 0
    key_rows = []
    class_tab = {}
    for k in prime_keys:
        m, M = min(k[0]), max(k[0])
        idxs = allkeys[k]
        row = {"key": kstr(k), "m": m, "M": M, "n_prof": len(idxs)}
        for r in range(2, M + 1):
            col = col_for(r)
            dets = [det_of_mask(col[i][0]) for i in idxs]
            n_det = sum(dets)
            status = ("det" if n_det == len(idxs) else
                      "ndet" if n_det == 0 else "mixed")
            if status == "mixed":
                mixed_cells += 1
            expect = "det" if (r < m or r == M) else "ndet"
            pairs += 1
            if status != expect:
                law_viol += 1
            if status == "det":
                det_cases += 1
                if r < m:
                    det_below_m += 1
                else:
                    det_anchor += 1
            cls = "%d,%d" % (m, M)
            if cls not in class_tab:
                class_tab[cls] = {"keys": 0, "profiles": 0,
                                  "cells": [], "det_prefix": [],
                                  "anchor_sv": sorted({col[i][0] for i in idxs})
                                  if status == "det" else None}
            class_tab[cls]["cells"].append([r, status])
            class_tab[cls]["keys"] = 0  # filled below
        key_rows.append(row)
    for cls in class_tab:
        class_tab[cls]["cells"].sort()
    for k in prime_keys:
        cls = "%d,%d" % (min(k[0]), max(k[0]))
        class_tab[cls]["keys"] += 1
        class_tab[cls]["profiles"] = class_tab[cls].get("profiles", 0) + \
            len(allkeys[k])
    # det prefix per class
    for cls, tab in class_tab.items():
        tab["det_prefix"] = [r for r, s in tab["cells"] if s == "det" and
                             r < int(cls.split(",")[0])]
    prw_ok = (law_viol == 0 and mixed_cells == 0 and
              pairs == EXPECTED["pairs"]["total"] and
              det_cases == EXPECTED["pairs"]["det"] and
              det_below_m == EXPECTED["pairs"]["det_below_m"] and
              det_anchor == EXPECTED["pairs"]["det_anchor"])
    cap10_pairs = sum(max(k[0]) - 1 for k in cap10)
    p11_pairs = sum(max(k[0]) - 1 for k in p11)
    prw_ok = prw_ok and cap10_pairs == EXPECTED["pairs"]["cap10"] and \
        p11_pairs == EXPECTED["pairs"]["p11"]
    record("PRW: THEOREM (94 prime keys x r=2..M, all profiles per "
           "column): det <=> r<m or r=M, uniformly ndet on [m,M-1]; "
           "728 cells (218 cap<=10 + 510 prime-11), 0 violations, "
           "0 MIXED cells", prw_ok,
           {"pairs": pairs, "cap10_pairs": cap10_pairs,
            "p11_pairs": p11_pairs, "violations": law_viol,
            "mixed": mixed_cells, "det_cases": det_cases,
            "det_below_m": det_below_m, "det_anchor": det_anchor,
            "classes": class_tab})

    # ---- SV: survivor refinement on det cases
    perms = branch_perms(3)
    atom2idx = {at: i for i, at in enumerate(profiles)}
    sv_bad = 0
    below_bad = 0
    anchor_bad = 0
    chain_states = {}
    for k in prime_keys:
        m, M = min(k[0]), max(k[0])
        rep = orbit_representative(chain_profile(k[0], k[1], 3), 3, perms)
        chi = atom2idx[rep]
        for r in list(range(2, m)) + [M]:
            col = col_for(r)
            svs = {col[i][0] for i in allkeys[k]}
            chain_sv = col[chi][0]
            if len(svs) != 1 or next(iter(svs)) != chain_sv or \
                    not det_of_mask(chain_sv):
                sv_bad += 1
            if r < m and chain_sv != EXPECTED["sv"]["below_m_mask"]:
                below_bad += 1
            if r == M and chain_sv != EXPECTED["sv"]["anchor_mask"]:
                anchor_bad += 1
        if M == 11:
            chain_states[kstr(k)] = {
                "states_r10": foc["r10_focus"][chi][2],
                "states_r11": foc["r11_focus"][chi][2],
                "sv_r11": foc["r11_focus"][chi][0]}
    sv_ok = (sv_bad == 0 and below_bad == 0 and anchor_bad == 0 and
             det_cases == EXPECTED["pairs"]["det"])
    record("SV: all 266 det cases carry the chain survivor, uniform "
           "over the key's profiles; sv mask == P_0 on the 172 "
           "below-window cells and == P_1 on the 94 anchor cells "
           "(finite observation beyond G' r=2..6 universality)",
           sv_ok, {"sv_chain_mismatches": sv_bad,
                   "below_m_mask_violations": below_bad,
                   "anchor_mask_violations": anchor_bad,
                   "prime11_chain_states": chain_states})

    # ---- FL: Lemma FL redundant anchor on all used records
    fl_viol = 0
    fl_n = 0
    for k in prime_keys:
        M = max(k[0])
        for r in range(2, M + 1):
            col = col_for(r)
            for i in allkeys[k]:
                sv, fl, st = col[i]
                expect = 0
                for c in set(profile_sizes(profiles[i], 3)):
                    expect |= 1 << (c % r)
                fl_n += 1
                if fl != expect:
                    fl_viol += 1
    fl_ok = (fl_viol == 0 and fl_n == EXPECTED["fl"]["records"])
    record("FL: first-losers == OR{1<<(C_i mod r)} on all 14882 used "
           "records (Lemma FL / Theorem J(ii), redundant anchor)", fl_ok,
           {"records": fl_n, "violations": fl_viol})

    # ---- J: Theorem-J finite anchor for the cap<=10 keys (sv/det
    # constant on r in [M, 9])
    j_bad = 0
    j_n = 0
    for k in cap10:
        M = max(k[0])
        base = cols[M]
        for r in range(M, 10):
            col = cols[r]
            for i in allkeys[k]:
                j_n += 1
                if col[i][0] != base[i][0]:
                    j_bad += 1
    j_ok = (j_bad == 0 and j_n == EXPECTED["j_cap10"]["records"])
    record("J: cap<=10 prime keys: per-profile sv constant on r in "
           "[M,9] across the committed columns (1365 profile-column "
           "records, 0 mismatches) - the finite anchor of the "
           "Theorem-J side (r >= M det/sv for ALL r then follows from "
           "Theorem J, K0906; the prime-11 anchor is the single r=11 "
           "focus column, J-extended by K0920's r=13 anchor)", j_ok,
           {"records": j_n, "mismatches": j_bad})

    # ---- EXO: exotic11 anti-mirror
    exo_ok = True
    exo_data = {}
    for k in EXOTIC11:
        idxs = allkeys[k]
        exo_ok = exo_ok and len(idxs) > 0
        for r in range(2, 10):
            col = cols[r]
            dets = {det_of_mask(col[i][0]) for i in idxs}
            svs = {col[i][0] for i in idxs}
            exo_ok = exo_ok and dets == {True} and svs == {1}
        sv10 = {foc["r10_focus"][i][0] for i in idxs}
        d10 = {det_of_mask(x) for x in sv10}
        exo_ok = exo_ok and d10 == {True} and sv10 == {EXPECTED["exo"]["sv10_mask"]}
        sv11 = {foc["r11_focus"][i][0] for i in idxs}
        d11 = {det_of_mask(x) for x in sv11}
        exo_ok = exo_ok and d11 == {False} and sv11 == {EXPECTED["exo"]["sv11_mask"]}
        exo_data[kstr(k)] = {"profiles": len(idxs),
                             "sv_r10": sorted(sv10), "sv_r11": sorted(sv11)}
    exo_ok = exo_ok and sum(len(allkeys[k]) for k in EXOTIC11) == \
        EXPECTED["exo"]["profiles"]
    record("EXO: exotic11 (1,1,11)|0,(1,11,11)|0 anti-mirror: uniformly "
           "det with survivor P_0 on ALL of r=2..10 (committed + focus) "
           "and uniformly ndet (sv mask 0b11) at r=11=M - prime "
           "resonance is not a low-r tautology (m=1 keys invert the "
           "window law)", exo_ok, exo_data)

    # ---- COR: mixed keys of the r=9 boundary contain no prime key
    mixed9 = []
    for k, idxs in allkeys.items():
        dets = {det_of_mask(cols[9][i][0]) for i in idxs}
        if len(dets) > 1:
            mixed9.append(k)
    allprime_mixed = [k for k in mixed9 if all(s in PRIMES for s in k[0])]
    cor_ok = (len(mixed9) == EXPECTED["cor"]["mixed_r9"] and
              len(allprime_mixed) == EXPECTED["cor"]["allprime_mixed"])
    record("COR: the 34 mixed keys of the cap<=12 r=9 boundary (K0893/"
           "K0912, re-derived from the raw r=9 column) contain no "
           "all-prime-size key - consistent with PRW's mixed-free "
           "regularity for prime keys", cor_ok,
           {"mixed_r9": len(mixed9), "allprime_mixed": len(allprime_mixed)})

    # ---- DORM: dormancy prefixes by m (prime-11)
    dorm_ok = True
    dorm_data = {}
    for mval, pin in sorted(EXPECTED["dorm"].items()):
        m = int(mval[1])
        pref_pin = pin
        ks = [k for k in p11 if min(k[0]) == m]
        pref = []
        for r in range(2, 11):
            col = col_for(r)
            stats = set()
            for k in ks:
                idxs = allkeys[k]
                dets = {det_of_mask(col[i][0]) for i in idxs}
                stats.add("det" if dets == {True} else
                          "ndet" if dets == {False} else "mixed")
            if stats == {"det"}:
                pref.append(r)
            elif stats != {"ndet"}:
                dorm_ok = False
        dorm_ok = dorm_ok and pref == pref_pin
        dorm_data["m=%d" % m] = {"keys": len(ks), "det_prefix": pref}
    record("DORM: prime-11 dormancy prefixes by m: m=2 none, m=3 {2}, "
           "m=5 {2,3,4}, m=7 {2,..,6}; uniformly ndet on the rest of "
           "r<=10; r=11 uniform det (K0916's two dormancy-window "
           "shapes are the m=5/m=7 prefixes)", dorm_ok, dorm_data)

    # ---- P11S: K0920 graded-dormancy series explained by the law
    series = {}
    for r in range(2, 11):
        series[r] = sum(len(allkeys[k]) for k in p11 if min(k[0]) <= r)
    s_ok = series == EXPECTED["p11_series"]
    record("P11S: K0920's graded prime-11 dormancy series "
           "(90/273/273/704/704 and the r=7..10 full count) is exactly "
           "the cumulative profile count over keys with m <= r - the "
           "'family mixed' grading is the superposition of per-key "
           "uniform statuses (PRW), no key is actually mixed", s_ok,
           {"derived_ndet_by_r": series})

    # ---- LIVE: Python mask twin recomputation (independent)
    live_bad = 0
    live_n = 0
    nodes_eq = 0

    def twin_check(i, rr, col):
        nonlocal live_bad, live_n, nodes_eq
        sv, fl, st = col[i]
        verdict, nodes = mask_verdict(list(profiles[i]), 3, rr,
                                      budget=50_000_000)
        ok = (verdict["determined"] == det_of_mask(sv) and
              verdict["survivors"] == mask_bits(sv) and
              verdict["first_losers"] == mask_bits(fl))
        live_n += 1
        if nodes == st:
            nodes_eq += 1
        if not ok:
            live_bad += 1

    live_set = set()
    for k in prime_keys:
        m, M = min(k[0]), max(k[0])
        rep = orbit_representative(chain_profile(k[0], k[1], 3), 3, perms)
        chi = atom2idx[rep]
        for r in {2, m, M}:
            live_set.add((chi, r, M))
        light_m = min(allkeys[k], key=lambda i: (cols[m][i][2], i))
        live_set.add((light_m, m, M))
        if M == 11:
            light10 = min(allkeys[k],
                          key=lambda i: (foc["r10_focus"][i][2], i))
            live_set.add((chi, 10, M))
            live_set.add((light10, 10, M))
    for k in EXOTIC11:
        for i in allkeys[k]:
            live_set.add((i, 10, 11))
            live_set.add((i, 11, 11))
    max_states = 0
    for i, r, M in sorted(live_set):
        col = col_for(r)
        max_states = max(max_states, col[i][2])
        twin_check(i, r, col)
    live_ok = (live_bad == 0 and
               live_n == EXPECTED["live"]["records"] and
               (nodes_eq == live_n) == EXPECTED["live"]["nodes_eq_states"]
               and max_states == EXPECTED["live"]["max_states"])
    record("LIVE: Python mask twin (independent implementation, "
           "verbatim K0912 block) recomputes 329 records (chain of "
           "every key at r=2/m/M, prime-11 chain + lightest at the "
           "r=10 window top, lightest at r=m per key, all 12 exotic11 "
           "profiles at r=10/11): verdict equality on every record "
           "AND twin state count == engine states on every record "
           "(max states 9271)", live_ok,
           {"records": live_n, "mismatches": live_bad,
            "nodes_eq_states": nodes_eq, "max_states": max_states})

    all_ok = all(c["ok"] for c in checks)
    return {"all_ok": all_ok, "checks": checks,
            "keys": key_rows,
            "meta": {
                "theorem": "prime resonance window (PRW), cap<=12",
                "assembly": "Theorem J (K0906) + Theorem PD (K0916) / "
                            "PD12 (K0920) + committed columns r=2..9 "
                            "(K0881/K0876/K0912) + K0920 focus columns "
                            "r=10/11; Theorem E' (K0861) transfers",
                "engine": "mask_engine_fast2.js sha256 "
                          "b904760e109e9adf1689b91e7dcbb1aa530704af"
                          "322ee7808e2304d0377586de (source of the "
                          "committed columns; no new columns here)",
                "columns_committed": sorted(COMMITTED_PINS),
                "columns_focus": sorted(FOCUS_PINS)}}


def main():
    audit1 = assemble_audit()
    audit2 = assemble_audit()
    b1 = json.dumps(audit1, sort_keys=True, indent=1)
    b2 = json.dumps(audit2, sort_keys=True, indent=1)
    if b1 != b2:
        print("FATAL: assemble not deterministic")
        sys.exit(2)
    os.makedirs(OUT, exist_ok=True)
    with open(AUDIT_PATH, "w") as f:
        json.dump(audit1, f, indent=1, sort_keys=True)
        f.write("\n")
    n_ok = sum(1 for c in audit1["checks"] if c["ok"])
    n_all = len(audit1["checks"])
    for c in audit1["checks"]:
        print("%s  %s" % ("OK " if c["ok"] else "FAIL", c["name"]))
    print("checks: %d/%d ok" % (n_ok, n_all))
    if not audit1["all_ok"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
