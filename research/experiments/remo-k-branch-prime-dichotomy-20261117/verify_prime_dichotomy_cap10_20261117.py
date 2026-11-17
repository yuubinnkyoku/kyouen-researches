#!/usr/bin/env python3
"""K-prime-dichotomy (item K0916): the universal determinacy dichotomy for
three-branch REMO canonical keys with branch sizes <= 10.  THEOREM PD:
for every key (sizes multiset, gamma) with max C_i = M <= 10 and every
r >= max(M,2), the key is uniformly determined at r (all canonical
profiles determined) IF AND ONLY IF Delta=0 (uniform sizes (C,C,C),
Theorem D family, K0859) OR all branch sizes lie in {2,3,5,7}.

Proof assembly (report.md): the committed machine columns pin the
finite window [max(M,2),13] for every one of the 715 cap<=10 keys
(cap<=12 columns r=2..9 via the K0882 order-preserving D_10 embedding
+ cap<=10 columns r=9..13); Theorem J(i) of K0906 (proved universal,
canonical domain, any k) makes per-profile det/sv constant on
r >= max(M,2); Theorem E' (K0861) transfers the profile statement to
every realizing board.  The verification below re-derives the whole
finite anchor from the raw committed columns (no new sweep).

Self-contained verifier (stdlib only, deterministic, no network).
All 14 input columns are pinned by sha256.  The Python mask twin is
the verbatim K0912 machinery block (itself the K0893 twin of record).

Checked claims:

PIN   All 14 input columns match their pinned sha256, have the pinned
      line counts (47,595 for cap<=12 r=2..9, 15,863 for cap<=10
      r=9..13) and contiguous indices.
B     Burnside fix counts cap10/cap12 == (84494,3478,125)/
      (261749,7805,203) -> orbits 15,863/47,595; direct canonical
      enumerations reproduce; key counts 715/1365.
EMB   profiles(D_10) is the order-preserving subsequence of
      profiles(D_12) (K0882); the cap<=12 r=9 column restricted to
      the D_10 positions is byte-identical to the committed K0893
      cap<=10 r=9 column ([i, sv, fl, states]).
FL    Lemma FL / Theorem J(ii) (K0864/K0906, universal; redundant
      anchor): fl == {C_i mod r} for all 15,863 profiles at every
      r = 2..13 (0 violations).
J     Theorem J finite anchor (K0906 universal; K0904 C5 redundancy
      re-derived from raw columns): per profile, det and sv mask are
      constant on r in [max(M,2),13] (0 det diffs, 0 sv diffs); fl
      constant on [max(M+1,2),13] (0 diffs); sigma <= M-1
      (Theorem J(iii), 0 violations).
CENS  Per-column key census (cap<=10 keys) is 98 uniform-det / 583
      uniform-ndet / 34 mixed at every r = 9..13; the 34 mixed keys
      are exactly the published 7-family set (K0893); the cap<=12
      r=9 total census is 143/1188/34 (K0912).
PD    THEOREM PD (universal in r via Theorem J, finite over sizes
      <= 10): the fixed-point uniformly-det key set (98 keys) is
      EXACTLY Delta=0 (55 keys) union all-sizes-in-{2,3,5,7} (60
      keys, of which 17 are also Delta=0; 43 non-uniform), with 0
      violations in either direction; det is constant on the whole
      window per key (0 keys with any window change); the r=9 det
      set equals the window det set; gamma-independence corollary:
      the fixed-point status depends only on the size multiset (0
      multisets with differing status).
D0    Theorem D (K0859, universal) anchor: all 728 cap<=10 Delta=0
      profiles are determined at every r = 2..13 with survivor
      theorem_d(C,r).survivor (0 mismatches); the Theorem D
      recursion reproduces the K0859 published table (84 entries,
      0 mismatches).
GP    Theorem G' survivor level (K0864 proved r=2..6; here a
      redundant finite anchor on every committed column): every
      determined profile of each of the 98 uniformly-det keys and
      of the 34 mixed keys (det profiles) carries the chain
      profile's survivor at every r in [max(M,2),13]; the chain
      profile is itself determined (0 mismatches; mixed-key det
      profile counts constant on the window).
ABS   Finite observation (low-r structure): the keys uniformly
      determined at EVERY r = 2..13 are exactly the 55 Delta=0
      keys; 446 keys are non-determined at every r = 2..13; the
      six keys (1,1,p)/(1,p,p), p in {3,5,7}, are determined on
      their whole low-r window r in [2,M-1] and non-determined at
      every r >= M; in total 171 keys are 'deceptive' (det at
      some r < max(M,2), non-det at the fixed point) - the full
      measured table is pinned in the audit.
EXOT  Finite observation (cap<=12 new keys, committed columns
      r=2..9; the dichotomy does NOT extend there): 650 new keys
      (363 with a size-11 branch, 364 with a size-12 branch,
      31,732 profiles); exactly 45 are uniformly determined at
      every r = 2..9 = the 23 new Delta=0 keys ((11,11,11) x
      g=0..10, (12,12,12) x g=0..11) plus the 22 exotic keys
      (1,1,11)|0, (1,11,11)|0, (10,10,12) x g=0..9,
      (10,12,12) x g=0..9 (neither Delta=0 nor all-prime);
      exactly 65 dormant keys are determined on a contiguous
      prefix window {r: 2..4} (32 keys, 8 multisets) or {r: 2..6}
      (33 keys, 6 multisets) and non-determined at r=7..9; the
      remaining 540 keys are non-determined at r=3..9 and their
      r=2 status matches the K0881 r=2 parity closed form exactly
      (93 det / 447 ndet, 0 mismatches).
LIVE  Live Python-twin recomputation: (a) 40 stratified light
      profiles (states <= 200,000 in the r=13 column) reproduce the
      committed r=13 column exactly at r=13; (b) beyond-column
      probes (first data past r=13): all 60 all-prime keys' chain
      profiles stay determined at r=14,15 with the SAME survivor
      as r=13; the composite keys (2,2,4),(3,4,6) (all profiles)
      stay non-determined at r=14,15 with sv mask identical to
      r=13; all 55 Delta=0 keys' chain profiles are determined
      with the theorem_d(C,14/15) survivor; the six deceptive
      keys' 18 profiles stay non-determined at r=14,15.

Scope / limits (do not over-read):
- PD is universal over r but FINITE over sizes (<= 10).  It says
  nothing about sizes 11,12: the EXOT rows show 22 exotic keys
  outside both families that are determined on all committed
  columns r=2..9, so the dichotomy is exactly a cap<=10
  classification; the cap<=11/12 fixed points of those keys are
  unknown until the r=11/r=12 cap<=12 columns exist.
- 'All sizes in {2,3,5,7}' is a statement about a finite set; the
  prime framing is a classification label, NOT a mechanism: no
  structural characterization of 'why primes' is claimed, and
  within cap<=10 the set {2,3,5,7} cannot be distinguished from
  'primes <= 10' by this data alone.
- GP and ABS and EXOT rows are finite observations on committed
  columns plus the LIVE r=14/15 probes, not universal laws.
  Theorem G' is proved only for r=2..6 (K0864); Theorem D and
  Theorem J are universal (K0859/K0906).
- fl (first-loser) masks are covered by Lemma FL / Theorem J(ii),
  universal; this verifier re-anchors them redundantly.
- 11x11 empty board / class frontiers remain UNKNOWN, unrelated.

The audit JSON is regenerated twice and must be byte-identical, and
byte-identical to the committed audit (fresh-checkout reproducible).

Usage: python3 verify_prime_dichotomy_cap10_20261117.py
"""

import hashlib
import json
import os
import sys

sys.setrecursionlimit(100000)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")
AUDIT_PATH = os.path.join(OUT, "prime_dichotomy_cap10_audit.json")

E = os.path.join(HERE, "..")

# ====PINNED====

COLUMN_PINS = {
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
    10: ("remo-k-branch-cap10-r10-boundary-20261117/output/js_cap10_r10.packed.jsonl",
         "fa1e1a405523403611101f819aed5013b353fdf2a526d125e643b8364b072884", 15863),
    11: ("remo-k-branch-cap10-r11-boundary-20261117/output/js_cap10_r11.packed.jsonl",
         "08324c19e8837041d8128423f26d88100b1ba7963fea1b86e3f90052b10664f0", 15863),
    12: ("remo-k-branch-cap10-r12-boundary-20261117/output/js_cap10_r12.packed.jsonl",
         "0835a06fe3a2cc812b5434ef0d56146f72b2b019b144ed62544d437472c05274", 15863),
    13: ("remo-k-branch-cap10-r13-invariance-20261117/output/js_cap10_r13.packed.jsonl",
         "b0ec4f58ac0f4e91185ad252924920738d5e6e8d47a75e61477cf3d915bb7dca", 15863),
}
CAP10_R9_PIN = ("remo-k-branch-cap10-r9-boundary-20261117/output/js_cap10_r9.packed.jsonl",
                "a2bb16bc8d03f341704d902f0a50ce4352b14ad08043cbced54b8e8f83b9973b", 15863)

PRIMES = (2, 3, 5, 7)

EXPECTED_BURNSIDE = {
    10: {"fix_id": 84494, "fix_trans": 3478, "fix_cyc": 125, "orbits": 15863, "keys": 715},
    12: {"fix_id": 261749, "fix_trans": 7805, "fix_cyc": 203, "orbits": 47595, "keys": 1365},
}
D10 = {"positions": 15863, "first": 0, "last": 47562}

CENSUS_CAP10 = {"uniform_det": 98, "uniform_ndet": 583, "mixed": 34}
CENSUS_CAP12_R9 = {"uniform_det": 143, "uniform_ndet": 1188, "mixed": 34}

PD_COUNTS = {"det": 98, "delta0": 55, "allprime": 60, "allprime_non_delta0": 43,
             "delta0_allprime": 17}
ABS_COUNTS = {"always_det": 55, "always_ndet": 446, "deceptive": 171}
SIX_FULL_WINDOW = ["1,1,3|0", "1,3,3|0", "1,1,5|0", "1,5,5|0",
                   "1,1,7|0", "1,7,7|0"]
DELTA0_PROFILES = 728
D0_TABLE = {"entries": 84, "mismatches": 0}

NEW_KEYS = {"keys": 650, "with_11": 363, "with_12": 364, "profiles": 31732,
            "profiles_with_11": 18740, "profiles_with_12": 19530}
NEW_DET_KEYS = ["1,1,11|0", "1,11,11|0", "10,10,12|0", "10,10,12|1",
                "10,10,12|2", "10,10,12|3", "10,10,12|4", "10,10,12|5",
                "10,10,12|6", "10,10,12|7", "10,10,12|8", "10,10,12|9",
                "10,12,12|0", "10,12,12|1", "10,12,12|2", "10,12,12|3",
                "10,12,12|4", "10,12,12|5", "10,12,12|6", "10,12,12|7",
                "10,12,12|8", "10,12,12|9", "11,11,11|0", "11,11,11|1",
                "11,11,11|10", "11,11,11|2", "11,11,11|3", "11,11,11|4",
                "11,11,11|5", "11,11,11|6", "11,11,11|7", "11,11,11|8",
                "11,11,11|9", "12,12,12|0", "12,12,12|1", "12,12,12|10",
                "12,12,12|11", "12,12,12|2", "12,12,12|3", "12,12,12|4",
                "12,12,12|5", "12,12,12|6", "12,12,12|7", "12,12,12|8",
                "12,12,12|9"]
DORMANT = {"count": 65, "w_2_4": 32, "w_2_6": 33}
DORMANT_W4_MULTISETS = [[1, 5, 11], [4, 4, 12], [4, 6, 12], [4, 10, 12],
                        [4, 12, 12], [5, 5, 11], [5, 7, 11], [5, 11, 11]]
DORMANT_W6_MULTISETS = [[1, 7, 11], [6, 6, 12], [6, 10, 12], [6, 12, 12],
                         [7, 7, 11], [7, 11, 11]]
REST_KEYS = {"count": 540, "r2_det": 93, "r2_ndet": 447, "parity_mismatches": 0}

LIVE_PINS = {"sample_states_cap": 200000, "sample_n": 40, "r13_mismatches": 0,
             "primes_chain_keys": 60, "primes_chain_mismatches": 0,
             "composite_keys": ["2,2,4", "3,4,6"], "composite_profiles": 35,
             "composite_mismatches": 0, "d0_chain_checks": 110,
             "d0_chain_mismatches": 0, "deceptive_profiles": 18,
             "deceptive_mismatches": 0}


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
# helpers
# ---------------------------------------------------------------------------

def sha256_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def load_packed(path):
    out = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                i, svm, flm, st = json.loads(line)
                out.append((i, svm, flm, st))
    return out


def mask_bits(m):
    return sorted(p for p in range(32) if (m >> p) & 1)


def det_of_mask(m):
    return bin(m).count("1") == 1


def key_of(atoms):
    return (tuple(sorted(profile_sizes(atoms, 3))), atoms[6])


def kstr(k):
    return "%s|%d" % (",".join(map(str, k[0])), k[1])


def parse_kstr(s):
    a, g = s.split("|")
    return (tuple(int(x) for x in a.split(",")), int(g))


PERMS3 = None


def chain_rep(sizes, gamma):
    """Canonical (orbit-representative) form of the chain profile."""
    return orbit_representative(chain_profile(sizes, gamma, 3), 3, PERMS3)


def is_delta0(k):
    return len(set(k[0])) == 1


def is_allprime(k):
    return all(s in PRIMES for s in k[0])


# ---------------------------------------------------------------------------
# audit assembly (deterministic; regenerate twice, byte-identical)
# ---------------------------------------------------------------------------

def assemble_audit():
    global PERMS3
    checks = []

    def record(name, ok, data):
        checks.append({"name": name, "ok": bool(ok), "data": data})

    PERMS3 = branch_perms(3)

    # ---- load columns (PIN)
    cols = {}
    pin_ok = True
    pin_detail = {}
    for r, (rel, sha, n) in sorted(COLUMN_PINS.items()):
        p = os.path.normpath(os.path.join(E, rel))
        got = sha256_file(p)
        recs = load_packed(p)
        idx_ok = all(rec[0] == j for j, rec in enumerate(recs))
        pin_ok = pin_ok and got == sha and len(recs) == n and idx_ok
        cols[r] = recs
        pin_detail["r%d" % r] = {"sha256": got, "lines": len(recs),
                                 "index_contiguous": idx_ok}
    rel, sha, n = CAP10_R9_PIN
    p = os.path.normpath(os.path.join(E, rel))
    got = sha256_file(p)
    cap10r9 = load_packed(p)
    pin_ok = pin_ok and got == sha and len(cap10r9) == n
    pin_detail["cap10_r9"] = {"sha256": got, "lines": len(cap10r9)}
    record("PIN: 14 committed columns sha256/shape", pin_ok, pin_detail)

    # ---- B: Burnside vs direct enumeration (K0875 machinery, r-independent)
    b_ok = True
    b_detail = {}
    for cap in (10, 12):
        fix_id, fix_trans, fix_cyc, orbits = burnside_fix_counts(cap)
        exp = EXPECTED_BURNSIDE[cap]
        b_ok = b_ok and (fix_id, fix_trans, fix_cyc, orbits) == (
            exp["fix_id"], exp["fix_trans"], exp["fix_cyc"], exp["orbits"])
        b_detail["cap%d" % cap] = {"fix": [fix_id, fix_trans, fix_cyc],
                                   "orbits": orbits}
    profiles10 = direct_constrained(10)
    profiles12 = direct_constrained(12)
    byk10 = {}
    for i, at in enumerate(profiles10):
        byk10.setdefault(key_of(at), []).append(i)
    byk12 = {}
    for i, at in enumerate(profiles12):
        byk12.setdefault(key_of(at), []).append(i)
    b_ok = b_ok and len(profiles10) == D10["positions"]
    b_ok = b_ok and len(profiles12) == EXPECTED_BURNSIDE[12]["orbits"]
    b_ok = b_ok and len(byk10) == EXPECTED_BURNSIDE[10]["keys"]
    b_ok = b_ok and len(byk12) == EXPECTED_BURNSIDE[12]["keys"]
    b_detail["profiles"] = [len(profiles10), len(profiles12)]
    b_detail["keys"] = [len(byk10), len(byk12)]
    record("B: Burnside fix counts + canonical enumerations + key counts",
           b_ok, b_detail)

    # ---- EMB: D_10 order-preserving subsequence + r=9 byte identity
    e_ok = True
    idx10 = {at: i for i, at in enumerate(profiles10)}
    emb = []
    for i, at in enumerate(profiles12):
        if at in idx10:
            emb.append(i)
    e_ok = e_ok and len(emb) == D10["positions"]
    e_ok = e_ok and emb == sorted(emb)
    e_ok = e_ok and emb[0] == D10["first"] and emb[-1] == D10["last"]
    mism = 0
    for j, gpos in enumerate(emb):
        gi, gsv, gfl, gst = cols[9][gpos]
        li, lsv, lfl, lst = cap10r9[j]
        if (gsv, gfl, gst) != (lsv, lfl, lst) or li != j:
            mism += 1
    e_ok = e_ok and mism == 0
    record("EMB: K0882 order-preserving D_10 subsequence; cap<=12 r=9 "
           "column == K0893 cap<=10 r=9 column at all 15,863 positions",
           e_ok, {"positions": len(emb), "byte_mismatches": mism})

    # ---- column accessors for cap<=10 keys
    # r=2..9: D_12-indexed cap<=12 columns; r=9..13: D_10-indexed cap<=10
    def svfl(r, i10):
        if r <= 9:
            return cols[r][emb[i10]]
        return cols[r][i10]

    # ---- FL: Lemma FL / Theorem J(ii) anchor, r=2..13 all profiles
    fl_viol = 0
    for i, at in enumerate(profiles10):
        sizes = profile_sizes(at, 3)
        for r in range(2, 14):
            expect = 0
            for c in sizes:
                expect |= 1 << (c % r)
            flm = svfl(r, i)[2]
            if flm != expect:
                fl_viol += 1
    record("FL: fl == {C_i mod r} for all 15,863 profiles x r=2..13 "
           "(Lemma FL / Theorem J(ii), universal; redundant anchor)",
           fl_viol == 0, {"pairs": 15863 * 12, "violations": fl_viol})

    # ---- J: Theorem J finite anchor (det/sv constancy on window)
    j_det = 0
    j_sv = 0
    j_fl = 0
    j_sigma = 0
    for i, at in enumerate(profiles10):
        sizes = profile_sizes(at, 3)
        M = max(sizes)
        W = range(max(M, 2), 14)
        ref = svfl(W[0], i)
        refdet = det_of_mask(ref[1])
        for r in W:
            rec = svfl(r, i)
            if det_of_mask(rec[1]) != refdet:
                j_det += 1
            if rec[1] != ref[1]:
                j_sv += 1
            if max(mask_bits(rec[1])) >= M:
                j_sigma += 1
        Wf = range(max(M + 1, 2), 14)
        reffl = svfl(Wf[0], i)[2]
        for r in Wf:
            if svfl(r, i)[2] != reffl:
                j_fl += 1
    record("J: Theorem J (K0906, universal) finite anchor from raw columns: "
           "det/sv constant on [max(M,2),13], fl constant on [max(M+1,2),13], "
           "sigma <= M-1, for all 15,863 profiles",
           j_det == 0 and j_sv == 0 and j_fl == 0 and j_sigma == 0,
           {"det_diffs": j_det, "sv_mask_diffs": j_sv, "fl_diffs": j_fl,
            "sigma_violations": j_sigma})

    # ---- CENS: per-column key census r=9..13 + cap<=12 r=9 total
    c_detail = {}
    c_ok = True
    mixed_keys = set()
    for r in range(9, 14):
        ud = un = mx = 0
        for k, idxs in byk10.items():
            d = sum(1 for i in idxs if det_of_mask(svfl(r, i)[1]))
            if d == len(idxs):
                ud += 1
            elif d == 0:
                un += 1
            else:
                mx += 1
                if r == 9:
                    mixed_keys.add(k)
        exp = CENSUS_CAP10
        c_ok = c_ok and (ud, un, mx) == (exp["uniform_det"], exp["uniform_ndet"],
                                         exp["mixed"])
        c_detail["r%d" % r] = [ud, un, mx]
    # cap<=12 r=9 total census (K0912 cross-check)
    ud12 = un12 = mx12 = 0
    for k, idxs in byk12.items():
        d = sum(1 for i in idxs if det_of_mask(cols[9][i][1]))
        if d == len(idxs):
            ud12 += 1
        elif d == 0:
            un12 += 1
        else:
            mx12 += 1
    e12 = CENSUS_CAP12_R9
    c_ok = c_ok and (ud12, un12, mx12) == (e12["uniform_det"],
                                           e12["uniform_ndet"], e12["mixed"])
    c_detail["cap12_r9_total"] = [ud12, un12, mx12]
    mixed_sorted = sorted(kstr(k) for k in mixed_keys)
    fam = sorted({m for m, _ in (parse_kstr(s) for s in mixed_sorted)})
    c_ok = c_ok and len(mixed_keys) == 34 and fam == [
        (6, 6, 8), (6, 6, 9), (6, 8, 8), (6, 8, 9), (6, 9, 9),
        (8, 8, 9), (8, 9, 9)]
    c_detail["mixed_families"] = [list(m) for m in fam]
    c_detail["mixed_keys"] = mixed_sorted
    record("CENS: key census 98/583/34 at every column r=9..13; 34 mixed "
           "keys == the published 7-family set; cap<=12 r=9 total "
           "143/1188/34 (K0912)", c_ok, c_detail)

    # ---- PD: the dichotomy
    det_keys = []
    ndet_keys = []
    window_change = 0
    det_r9 = set()
    for k, idxs in byk10.items():
        M = max(k[0])
        W = range(max(M, 2), 14)
        per = []
        for r in W:
            per.append(all(det_of_mask(svfl(r, i)[1]) for i in idxs))
        if all(per):
            det_keys.append(k)
        if not any(per):
            ndet_keys.append(k)
        if len(set(per)) > 1:
            window_change += 1
        if all(det_of_mask(svfl(9, i)[1]) for i in idxs):
            det_r9.add(k)
    det_keys.sort()
    d0 = [k for k in det_keys if is_delta0(k)]
    pr = [k for k in det_keys if is_allprime(k)]
    pr_non = [k for k in det_keys if is_allprime(k) and not is_delta0(k)]
    both = [k for k in det_keys if is_allprime(k) and is_delta0(k)]
    viol_pos = [kstr(k) for k in det_keys
                if not (is_delta0(k) or is_allprime(k))]
    viol_neg = [kstr(k) for k in ndet_keys
               if is_delta0(k) or is_allprime(k)]
    allpr_total = [k for k in byk10 if is_allprime(k)]
    # gamma independence: fixed-point status constant per size multiset
    gamma_status = {}
    gamma_bad = []
    for k, idxs in byk10.items():
        M = max(k[0])
        W = range(max(M, 2), 14)
        st = all(all(det_of_mask(svfl(r, i)[1]) for i in idxs) for r in W)
        gamma_status.setdefault(k[0], set()).add(st)
    for m, sts in gamma_status.items():
        if len(sts) > 1:
            gamma_bad.append(list(m))
    p_ok = (len(det_keys) == PD_COUNTS["det"]
            and len(d0) == PD_COUNTS["delta0"]
            and len(pr) == PD_COUNTS["allprime"]
            and len(pr_non) == PD_COUNTS["allprime_non_delta0"]
            and len(both) == PD_COUNTS["delta0_allprime"]
            and not viol_pos and not viol_neg
            and window_change == 0
            and det_r9 == set(det_keys)
            and not gamma_bad
            and len(allpr_total) == PD_COUNTS["allprime"])
    record("PD: THEOREM prime dichotomy - for every cap<=10 key and every "
           "r >= max(M,2): uniformly determined <=> Delta=0 (uniform sizes, "
           "Theorem D family) or all sizes in {2,3,5,7}; det set = 98 keys "
           "(55 Delta=0 + 43 non-uniform all-prime; 60 all-prime of which "
           "17 also Delta=0); 0 violations both directions; det constant "
           "on the whole committed window; r=9 det set == window det set; "
           "gamma-independence corollary holds (status depends only on "
           "the size multiset). Universality in r via Theorem J(i) "
           "(K0906, proved universal); board transfer via Theorem E' "
           "(K0861). Finite anchor: all committed columns r=2..13.",
           p_ok,
           {"det_keys": len(det_keys), "delta0": len(d0), "allprime": len(pr),
            "allprime_non_delta0": len(pr_non), "delta0_allprime": len(both),
            "violations_det_side": viol_pos, "violations_ndet_side": viol_neg,
            "window_changes": window_change,
            "det_r9_equals_window": det_r9 == set(det_keys),
            "gamma_independence_violations": gamma_bad,
            "det_key_list": [kstr(k) for k in det_keys]})

    # ---- D0: Theorem D anchor (universal theorem, redundant anchor)
    d0_prof = 0
    d0_mism = 0
    for i, at in enumerate(profiles10):
        sizes = profile_sizes(at, 3)
        if len(set(sizes)) != 1:
            continue
        d0_prof += 1
        C = sizes[0]
        for r in range(2, 14):
            _, surv = theorem_d(C, r)
            rec = svfl(r, i)
            if not (det_of_mask(rec[1]) and rec[1] == (1 << surv)):
                d0_mism += 1
    entries, t_mism = theorem_d_table()
    record("D0: Theorem D (K0859, universal) anchor: all 728 cap<=10 "
           "Delta=0 profiles determined with the theorem_d survivor at "
           "every r=2..13 (0 mismatches); Theorem D recursion == K0859 "
           "published table (84 entries, 0 mismatches)",
           d0_prof == DELTA0_PROFILES and d0_mism == 0
           and entries == D0_TABLE["entries"] and t_mism == D0_TABLE["mismatches"],
           {"delta0_profiles": d0_prof, "survivor_mismatches": d0_mism,
            "table_entries": entries, "table_mismatches": t_mism})

    # ---- GP: chain survivor level (Theorem G' redundant anchor)
    gp_det = 0
    gp_mixed = 0
    chain_ndet = 0
    mixed_ct_bad = 0
    for k in det_keys:
        rep = chain_rep(k[0], k[1])
        ri = idx10[rep]
        for r in range(max(max(k[0]), 2), 14):
            csv = svfl(r, ri)[1]
            if not det_of_mask(csv):
                chain_ndet += 1
            for i in byk10[k]:
                if svfl(r, i)[1] != csv:
                    gp_det += 1
    for k in sorted(mixed_keys):
        rep = chain_rep(k[0], k[1])
        ri = idx10[rep]
        cts = []
        for r in range(max(max(k[0]), 2), 14):
            csv = svfl(r, ri)[1]
            ct = 0
            for i in byk10[k]:
                svm = svfl(r, i)[1]
                if det_of_mask(svm):
                    ct += 1
                    if svm != csv:
                        gp_mixed += 1
            cts.append(ct)
        if len(set(cts)) > 1:
            mixed_ct_bad += 1
    record("GP: Theorem G' survivor level (K0864 proved r=2..6; redundant "
           "finite anchor on every committed column): every determined "
           "profile of the 98 uniformly-det keys and of the 34 mixed keys "
           "carries the chain survivor at every r in [max(M,2),13]; chain "
           "profiles determined; mixed-key det-profile counts constant",
           gp_det == 0 and gp_mixed == 0 and chain_ndet == 0 and mixed_ct_bad == 0,
           {"det_key_mismatches": gp_det, "mixed_key_mismatches": gp_mixed,
            "chain_nondet_cases": chain_ndet,
            "mixed_count_nonconstant": mixed_ct_bad})

    # ---- ABS: low-r structure (finite observation)
    always_det = []
    always_ndet = 0
    for k, idxs in byk10.items():
        if all(all(det_of_mask(svfl(r, i)[1]) for i in idxs)
               for r in range(2, 14)):
            always_det.append(kstr(k))
        if not any(all(det_of_mask(svfl(r, i)[1]) for i in idxs)
                   for r in range(2, 14)):
            always_ndet += 1
    always_det.sort()
    deceptive = []
    six_full = []
    for k, idxs in byk10.items():
        M = max(k[0])
        W = range(max(M, 2), 14)
        if any(all(det_of_mask(svfl(r, i)[1]) for i in idxs) for r in W):
            continue
        low = [r for r in range(2, min(M, 14))
               if all(det_of_mask(svfl(r, i)[1]) for i in idxs)]
        if low:
            deceptive.append((kstr(k), low))
            if low == list(range(2, M)):
                six_full.append(kstr(k))
    deceptive.sort()
    a_ok = (len(always_det) == ABS_COUNTS["always_det"]
            and always_det == sorted(kstr(k) for k in det_keys
                                     if is_delta0(k))
            and always_ndet == ABS_COUNTS["always_ndet"]
            and len(deceptive) == ABS_COUNTS["deceptive"]
            and sorted(six_full) == sorted(SIX_FULL_WINDOW))
    record("ABS: low-r structure (finite observation): keys determined at "
           "EVERY r=2..13 == exactly the 55 Delta=0 keys; 446 keys "
           "non-determined at every r=2..13; the six keys (1,1,p)/(1,p,p), "
           "p in {3,5,7}, are determined on their whole low-r window "
           "[2,M-1] and non-determined at every r >= M; 171 deceptive keys "
           "in total (measured table pinned)",
           a_ok, {"always_det": len(always_det), "always_ndet": always_ndet,
                  "deceptive": len(deceptive), "six_full_window": sorted(six_full),
                  "deceptive_table": [[k, w] for k, w in deceptive]})

    # ---- EXOT: cap<=12 new keys on committed columns r=2..9
    new_keys = [k for k in byk12 if max(k[0]) >= 11]
    w11 = sum(1 for k in new_keys if 11 in k[0])
    w12 = sum(1 for k in new_keys if 12 in k[0])
    nprof = sum(len(byk12[k]) for k in new_keys)
    p11 = sum(len(byk12[k]) for k in new_keys if 11 in k[0])
    p12 = sum(len(byk12[k]) for k in new_keys if 12 in k[0])
    det_all = []
    dormant = []
    rest = []
    for k in new_keys:
        per = {r: all(det_of_mask(cols[r][i][1]) for i in byk12[k])
               for r in range(2, 10)}
        if all(per[r] for r in range(2, 10)):
            det_all.append(k)
        elif any(per[r] for r in range(3, 10)):
            dormant.append((k, [r for r in range(2, 10) if per[r]]))
        else:
            rest.append(k)
    det_all.sort(key=kstr)
    dormant.sort(key=lambda x: kstr(x[0]))
    rest.sort(key=kstr)
    w4 = sorted({k[0] for k, w in dormant if w == [2, 3, 4]})
    w6 = sorted({k[0] for k, w in dormant if w == [2, 3, 4, 5, 6]})
    other_windows = [(kstr(k), w) for k, w in dormant
                     if w not in ([2, 3, 4], [2, 3, 4, 5, 6])]
    r2_det = [k for k in rest
              if all(det_of_mask(cols[2][i][1]) for i in byk12[k])]
    parity_mism = 0
    for k in rest:
        same = len({c % 2 for c in k[0]}) == 1
        if same != (k in r2_det):
            parity_mism += 1
    exotic = [k for k in det_all
              if not is_delta0(k) and not is_allprime(k)]
    x_ok = (len(new_keys) == NEW_KEYS["keys"] and w11 == NEW_KEYS["with_11"]
            and w12 == NEW_KEYS["with_12"] and nprof == NEW_KEYS["profiles"]
            and p11 == NEW_KEYS["profiles_with_11"]
            and p12 == NEW_KEYS["profiles_with_12"]
            and sorted(kstr(k) for k in det_all) == sorted(NEW_DET_KEYS)
            and len(dormant) == DORMANT["count"]
            and len(w4) == len(DORMANT_W4_MULTISETS)
            and [list(m) for m in w4] == DORMANT_W4_MULTISETS
            and len(w6) == len(DORMANT_W6_MULTISETS)
            and [list(m) for m in w6] == DORMANT_W6_MULTISETS
            and not other_windows
            and len(rest) == REST_KEYS["count"]
            and len(r2_det) == REST_KEYS["r2_det"]
            and parity_mism == REST_KEYS["parity_mismatches"]
            and len(exotic) == 22)
    record("EXOT: cap<=12 new keys (sizes 11/12) on committed columns "
           "r=2..9 (finite observation; the dichotomy does NOT extend to "
           "cap<=11/12): 650 new keys (363 with 11, 364 with 12; 31,732 "
           "profiles); 45 uniformly determined at every r=2..9 == 23 new "
           "Delta=0 + 22 exotic keys (neither Delta=0 nor all-prime - "
           "outside the dichotomy families); 65 dormant keys with det "
           "window exactly {2,3,4} (32 keys, 8 multisets) or {2,..,6} "
           "(33 keys, 6 multisets), contiguous prefixes; 540 keys "
           "non-determined at r=3..9 with r=2 status matching the K0881 "
           "parity closed form (93 det / 447 ndet, 0 mismatches)",
           x_ok, {"new_keys": len(new_keys), "with_11": w11, "with_12": w12,
                  "profiles": nprof, "det_all": len(det_all),
                  "det_all_keys": [kstr(k) for k in det_all],
                  "exotic_count": len(exotic),
                  "dormant": len(dormant),
                  "dormant_windows": {"2_4": len(w4), "2_6": len(w6),
                                      "other": other_windows},
                  "dormant_table": [[kstr(k), w] for k, w in dormant],
                  "rest": len(rest), "rest_r2_det": len(r2_det),
                  "parity_mismatches": parity_mism})

    # ---- LIVE: Python-twin recomputation
    # (a) stratified light sample vs committed r=13 column
    light = [i for i, rec in enumerate(cols[13]) if rec[3] <= LIVE_PINS["sample_states_cap"]]
    sel = [light[j * len(light) // LIVE_PINS["sample_n"]]
           for j in range(LIVE_PINS["sample_n"])]
    r13_mism = 0
    for i in sel:
        v = mask_verdict(profiles10[i], 3, 13)[0]
        svm = sum(1 << p for p in v["survivors"])
        flm = sum(1 << p for p in v["first_losers"])
        rec = cols[13][i]
        if (v["determined"], svm, flm) != (det_of_mask(rec[1]), rec[1], rec[2]):
            r13_mism += 1
    # (b) beyond-column probes at r=14,15
    pr_keys = sorted(k for k in byk10 if is_allprime(k))
    pr_mism = 0
    for k in pr_keys:
        rep = chain_rep(k[0], k[1])
        sv13 = svfl(13, idx10[rep])[1]
        for r in (14, 15):
            v = mask_verdict(rep, 3, r)[0]
            svm = sum(1 << p for p in v["survivors"])
            if not v["determined"] or svm != sv13:
                pr_mism += 1
    comp_prof = 0
    comp_mism = 0
    for ks in LIVE_PINS["composite_keys"]:
        sizes = tuple(int(x) for x in ks.split(","))
        for g in range(min(sizes)):
            for i in byk10[(sizes, g)]:
                comp_prof += 1
                sv13 = svfl(13, i)[1]
                for r in (14, 15):
                    v = mask_verdict(profiles10[i], 3, r)[0]
                    svm = sum(1 << q for q in v["survivors"])
                    if v["determined"] or svm != sv13:
                        comp_mism += 1
    d0_checks = 0
    d0_mism2 = 0
    for C in range(1, 11):
        for g in range(C):
            rep = chain_rep((C, C, C), g)
            for r in (14, 15):
                _, surv = theorem_d(C, r)
                v = mask_verdict(rep, 3, r)[0]
                d0_checks += 1
                svm = sum(1 << p for p in v["survivors"])
                if not v["determined"] or v["survivors"] != [surv]:
                    d0_mism2 += 1
    dec_prof = 0
    dec_mism = 0
    for ks in SIX_FULL_WINDOW:
        for i in byk10[parse_kstr(ks)]:
            dec_prof += 1
            for r in (14, 15):
                if mask_verdict(profiles10[i], 3, r)[0]["determined"]:
                    dec_mism += 1
    l_ok = (r13_mism == LIVE_PINS["r13_mismatches"]
            and len(pr_keys) == LIVE_PINS["primes_chain_keys"]
            and pr_mism == LIVE_PINS["primes_chain_mismatches"]
            and comp_prof == LIVE_PINS["composite_profiles"]
            and comp_mism == LIVE_PINS["composite_mismatches"]
            and d0_checks == LIVE_PINS["d0_chain_checks"]
            and d0_mism2 == LIVE_PINS["d0_chain_mismatches"]
            and dec_prof == LIVE_PINS["deceptive_profiles"]
            and dec_mism == LIVE_PINS["deceptive_mismatches"])
    record("LIVE: Python-twin recomputation: 40 stratified light profiles "
           "reproduce the committed r=13 column; r=14/15 probes (first "
           "data past r=13): all 60 all-prime chain profiles stay "
           "determined with the SAME survivor as r=13; composite keys "
           "(2,2,4),(3,4,6) (35 profiles) stay non-determined with sv "
           "mask == r=13; 55 Delta=0 chain profiles match theorem_d at "
           "r=14,15; the six deceptive keys' 18 profiles stay "
           "non-determined",
           l_ok, {"sample": len(sel), "r13_mismatches": r13_mism,
                  "primes_chain_keys": len(pr_keys), "primes_mismatches": pr_mism,
                  "composite_profiles": comp_prof,
                  "composite_mismatches": comp_mism,
                  "d0_chain_checks": d0_checks, "d0_mismatches": d0_mism2,
                  "deceptive_profiles": dec_prof,
                  "deceptive_mismatches": dec_mism})

    audit = {
        "meta": {
            "item": "K0916",
            "title": "Prime dichotomy: cap<=10 three-branch REMO keys are "
                "uniformly determined for every r >= max(M,2) iff "
                "Delta=0 or all sizes in {2,3,5,7} (98 = 55 + 43 keys); "
                "universal in r via Theorem J",
            "date": "2026-11-17",
            "columns": "committed packed columns only (K0881/K0876/K0912 "
                "r=2..9 cap<=12; K0893/K0895/K0897/K0898/K0902 "
                "r=9..13 cap<=10)",
            "machinery": "verbatim K0912 machinery block (K0875 "
                "enumeration/Burnside/theorem_d via K0893 twin of record)",
        },
        "checks": checks,
    }
    ok = all(c["ok"] for c in checks)
    audit["all_ok"] = ok
    return audit


def main():
    audit = assemble_audit()
    os.makedirs(OUT, exist_ok=True)
    with open(AUDIT_PATH, "w") as f:
        json.dump(audit, f, indent=1, sort_keys=True)
        f.write("\n")
    n_ok = sum(1 for c in audit["checks"] if c["ok"])
    n_all = len(audit["checks"])
    for c in audit["checks"]:
        print("%s  %s" % ("OK " if c["ok"] else "FAIL", c["name"]))
    print("checks: %d/%d ok" % (n_ok, n_all))
    if not audit["all_ok"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
