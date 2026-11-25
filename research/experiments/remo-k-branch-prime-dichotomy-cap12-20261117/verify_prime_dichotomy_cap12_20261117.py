#!/usr/bin/env python3
"""K-prime-dichotomy-cap12 (item K0920): the fixed point of the three-
branch REMO determinacy dichotomy at branch sizes <= 12.  THEOREM PD12:
for every canonical key (sizes multiset, gamma) with max C_i = M <= 12,
the key is uniformly determined at r (all canonical profiles
determined) for ALL r >= max(M,2)  IF AND ONLY IF  Delta=0 (uniform
sizes (C,C,C)|gamma, Theorem D family, K0859) OR all branch sizes lie
in {2,3,5,7,11}.

Assembly: (1) Theorem J(i) of K0906 (proved universal, canonical
domain) makes per-profile det/sv constant on r >= max(M,2), so a
single r = M column per key decides the fixed point; (2) the cap<=10
part (715 keys, 98 det) is Theorem PD of K0916; (3) this experiment
adds the 650 new keys: full r=11 focus column for the 64 candidate
keys (all 1619 profiles), Theorem-D machine anchors for (12,12,12),
and cheapest-profile witness scans at r=11/r=12 for the 576
non-prime non-Delta=0 keys; (4) Theorem E' (K0861) transfers to every
realizing board.

Sub-results pinned here (finite observations, not universal claims):
- prime-11 keys (51 non-Delta=0 + (11,11,11)xG) awaken exactly at
  r=M: dormancy is graded below M (mixed r=2..6, uniform-ndet r=7..10)
  and uniform-det at r=11 with chain survivor P_1 (G' finite anchor).
- exotic11 keys (1,1,11)|0,(1,11,11)|0 are deceptive: det on the
  whole low-r window r=2..10, flipping to uniform-ndet exactly at
  r=M=11.  The K0916 deception family (1,1,p),(1,p,p) extends from
  p in {3,5,7} to p=11 (6 -> 8 keys).
- exotic12 keys (10,10,12),(10,12,12) x G=0..9 are determined on all
  their 1425 profiles at r=2..9 and det at r=10, but flip BELOW the
  Theorem-J window already at r=11 = M-1 (sub-window flip; first such
  cohort) and are non-determined at r=12 = M (dichotomy side).
- Theorem J r=13 constancy anchor (15 records) and Lemma FL on all
  4445 new records.

Self-contained verifier (stdlib only, deterministic, no network).
Inputs: 8 committed cap<=12 packed columns r=2..9 (sha256-pinned,
published in the K0881/K0876/K0912 experiment dirs) + 11 new packed
columns committed in this experiment's output/ (packed single source
[i, sv_mask, fl_mask, states]; atoms are a pure function of the
canonical index via the Burnside enumeration).  The Python mask twin
is the verbatim K0912 machinery block (K0893 twin of record).

Checked claims (see audit JSON for full tables):

PIN   19 input columns match pinned sha256 and line counts.
B     Burnside cap12 (261749,7805,203) -> 47595 orbits; 1365 keys,
      650 new keys, 31732 new profiles.
TAX   650 = 23 Delta=0 + 51 prime-nD0 + 2 exotic11 + 20 exotic12
      + 222 others11 + 332 others12 (partition, definitions only).
FOC   focus columns cover ALL profiles of the 64 candidate keys.
S1    62 prime-11 keys uniformly det at r=11, survivors == chain
      survivor == P_1 (G' finite anchor, 0 mismatches).
S2    exotic11 uniformly NON-det at r=11 (sv mask 0b11).
O1    r=10 focus: 13 uniform-det / 51 uniform-ndet / 0 mixed.
EX11  exotic11 det on r=2..10 (12 profiles x 9 columns), flip at M.
P11   prime-11 dormancy series pinned (r=2..10).
D0C   Delta=0 profiles det with Theorem-D survivor on committed
      r=2..9 (both 336 + 448 profiles) and focus r=10/r=11.
D0    (12,12,12) cheapest anchors det, Theorem-D survivor P_11 at
      r=12 / P_10 at r=11.
EX12  exotic12 all-profiles det at r=2..9; cheapest det at r=10;
      cheapest NON-det at r=11 (sub-window flip) and r=12.
N1/N2 witness scans: all witnesses NON-det; every witness IS the
      cheapest profile (states@r9 asc, canon tiebreak) re-derived
      from the committed r=9 column (0 selection violations).
C1    coverage 64+222+352+12 == 650 keys; gamma-independence of the
      fixed point (144 multisets, 0 mixed).
PD12  det set == Delta=0 U all-prime on the 650 new keys (74 det /
      576 witness, both-direction violations 0); combined with the
      98 cap<=10 det keys of K0916 the cap<=12 dichotomy closes at
      172 det keys among 1365.
FL1   fl == OR{1 << (C_i mod r)} on all 4445 new records.
J13   15 r=13 anchor records sv-identical to their r=11/r=12 sources.
LIVE  Python mask twin recomputes 1007 witness/probe/anchor records
      plus focus samples: verdict equality (0 mismatches).

Limits: universal in r only via Theorem J (K0906); sizes <= 12;
primality as a mechanism is NOT claimed ({2,3,5,7,11} is a finite
set description inside cap<=12); G' universality beyond r=6 and the
graded dormancy / sub-window flip observations are finite data;
ranking determinacy and the 11x11 frontier are untouched (UNKNOWN).
"""

import json
import os
import sys
import hashlib
# ==== pinned constants (this experiment) ====

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")
AUDIT_PATH = os.path.join(OUT, "prime_dichotomy_cap12_audit.json")

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

# new machine columns committed with this experiment (packed single
# source: [canonical index, sv_mask, fl_mask, states]; atoms are a pure
# function of the canonical index via the Burnside enumeration).
# names: (file in output/, sha256, record count, r)
NEW_PINS = {
    "r11_focus": ("packed_r11_focus.jsonl",
        "8daa1cfa634af48a511fcfb1c9389eda03c05fd2deee501829caf99235c2daeb", 1619, 11),
    "r10_focus": ("packed_r10_focus.jsonl",
        "3face607a59c559941bcb58d2b1bdaea05132c33a1af8a891ab254983a445ac1", 1619, 10),
    "r12_witness": ("packed_r12_witness.jsonl",
        "73b9b0a0c59ca0f58dc12ebc9ee396b57ae72c7a4c1632486868565657cd6fe4", 352, 12),
    "r11_witness": ("packed_r11_witness.jsonl",
        "651ac851c4ea1326ae14e3da73154d4411fff66b03937c64af7f883c02a18ff3", 222, 11),
    "r12_d0anchor": ("packed_r12_d0anchor.jsonl",
        "2ff4dc5cc56c8beb2509371c231553b001894f7795372f58e1c8e26786ebc5f6", 12, 12),
    "ex12_r10": ("packed_ex12_r10.jsonl",
        "bfc7fafee9e842db30094a15f1b310e04af8b119c408791acfc0c49d2af48708", 20, 10),
    "ex12_r11": ("packed_ex12_r11.jsonl",
        "b42cb9825983d8f2ea8b811777b51bdc268260bc69cc40e7283dd06cc059c35d", 20, 11),
    "others12_r11": ("packed_others12_r11.jsonl",
        "26ee9f4515ac137bce29f3aaa03b8454347aa8cd414a74f393f920041b8671a6", 332, 11),
    "others11_r10": ("packed_others11_r10.jsonl",
        "bc5080e0952c22add374eddd8ef36c3ee98747322efc547a07c034bccf624cba", 222, 10),
    "d0_r11": ("packed_d0_r11.jsonl",
        "ec7001cfa110c522b661d8adbf7708a28fe98a06351ec3922ab46cc647db871c", 12, 11),
    "j13_anchor": ("packed_j13_anchor.jsonl",
        "888e6397d9e7d1c9658d814618591e9721575935305c9396667a3b79433fa8a0", 15, 13),
}

PRIMES = (2, 3, 5, 7, 11)

EXPECTED_BURNSIDE = {"fix_id": 261749, "fix_trans": 7805, "fix_cyc": 203,
                     "orbits": 47595, "keys": 1365,
                     "new_keys": 650, "new_profiles": 31732}

TAXONOMY = {"delta0": 23, "prime_non_delta0": 51, "exotic11": 2,
            "exotic12": 20, "others11": 222, "others12": 332, "total": 650}

FOCUS = {"keys": 64, "records": 1619, "prime11_keys": 62,
         "prime11_profiles": 1607, "exotic11_profiles": 12,
         "d0_11_keys": 11, "d0_11_profiles": 336}

S1_PINS = {"uniform_det_keys": 62, "chain_survivor": 1}
S2_PINS = {"exotic11_sv_mask": 3}
O1_PINS = {"det10": 13, "ndet10": 51, "mixed10": 0}
P11_DORMANCY = {"profiles": 1271,
                "ndet_by_r": {2: 90, 3: 273, 4: 273, 5: 704, 6: 704,
                              7: 1271, 8: 1271, 9: 1271, 10: 1271}}
D0_PINS = {"d0_11_profiles": 336, "d0_12_profiles": 448,
           "d0_12_keys": 12, "r12_survivor": 11, "r11_survivor": 10}
EX12_PINS = {"keys": 20, "profiles": 1425, "r10_det": 20,
             "r11_ndet": 20, "r12_ndet": 20}
PD12_PINS = {"det_new": 74, "ndet_new": 576, "delta0": 23, "allprime": 62,
             "overlap": 11, "cap10_det": 98, "combined_det": 172}
LIVE_PINS = {"states_cap": 100000, "extra_per_key": 2,
             "records": 1710, "mismatches": 0,
             "nodes_eq_states": True}
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

LIVE_COLS = ["r12_witness", "r11_witness", "r12_d0anchor", "ex12_r10",
             "ex12_r11", "others12_r11", "others11_r10", "d0_r11",
             "j13_anchor"]


def assemble_audit():
    global PERMS3
    checks = []

    def record(name, ok, data):
        checks.append({"name": name, "ok": bool(ok), "data": data})

    PERMS3 = branch_perms(3)

    # ---- load committed columns (PIN part 1)
    cols = {}
    pin_ok = True
    pin_detail = {"committed": {}, "new": {}}
    for r, (rel, sha, n) in sorted(COMMITTED_PINS.items()):
        p = os.path.normpath(os.path.join(E, rel))
        got = sha256_file(p)
        recs = load_packed(p)
        idx_ok = all(rec[0] == j for j, rec in enumerate(recs))
        pin_ok = pin_ok and got == sha and len(recs) == n and idx_ok
        cols[r] = {rec[0]: (rec[1], rec[2], rec[3]) for rec in recs}
        pin_detail["committed"]["r%d" % r] = {
            "sha256": got, "lines": len(recs), "index_contiguous": idx_ok}

    # ---- load new columns (PIN part 2)
    new = {}
    for name, (fn, sha, n, rr) in sorted(NEW_PINS.items()):
        p = os.path.join(OUT, fn)
        got = sha256_file(p)
        recs = load_packed(p)
        idx_ok = len({rec[0] for rec in recs}) == len(recs)
        pin_ok = pin_ok and got == sha and len(recs) == n and idx_ok
        new[name] = {rec[0]: (rec[1], rec[2], rec[3]) for rec in recs}
        pin_detail["new"][name] = {"sha256": got, "lines": len(recs),
                                   "r": rr, "indices_unique": idx_ok}
    record("PIN: 8 committed + 11 new columns sha256/shape", pin_ok,
           pin_detail)

    # ---- B: Burnside vs direct enumeration (K0875 machinery, r-independent)
    fix_id, fix_trans, fix_cyc, orbits = burnside_fix_counts(12)
    b_ok = ((fix_id, fix_trans, fix_cyc, orbits) ==
            (EXPECTED_BURNSIDE["fix_id"], EXPECTED_BURNSIDE["fix_trans"],
             EXPECTED_BURNSIDE["fix_cyc"], EXPECTED_BURNSIDE["orbits"]))
    profiles = direct_constrained(12)
    b_ok = b_ok and len(profiles) == EXPECTED_BURNSIDE["orbits"]
    atom2idx = {at: i for i, at in enumerate(profiles)}
    newkeys = {}
    allkeys = {}
    for i, at in enumerate(profiles):
        k = key_of(at)
        allkeys.setdefault(k, []).append(i)
        if max(k[0]) >= 11:
            newkeys.setdefault(k, []).append(i)
    b_ok = b_ok and len(allkeys) == EXPECTED_BURNSIDE["keys"]
    b_ok = b_ok and len(newkeys) == EXPECTED_BURNSIDE["new_keys"]
    b_ok = b_ok and (sum(len(v) for v in newkeys.values()) ==
                     EXPECTED_BURNSIDE["new_profiles"])
    record("B: Burnside cap12 (261749,7805,203)->47595 orbits; "
           "1365 keys / 650 new keys / 31732 new profiles", b_ok,
           {"fix": [fix_id, fix_trans, fix_cyc], "orbits": orbits,
            "keys": len(allkeys), "new_keys": len(newkeys),
            "new_profiles": sum(len(v) for v in newkeys.values())})

    # ---- taxonomy of the 650 new keys
    def is_delta0(k):
        return k[0][0] == k[0][1] == k[0][2]

    def is_allprime(k):
        return all(s in PRIMES for s in k[0])

    cls = {"delta0": [], "prime_non_delta0": [], "exotic11": [],
           "exotic12": [], "others11": [], "others12": []}
    for k in newkeys:
        if is_delta0(k):
            cls["delta0"].append(k)
        elif is_allprime(k):
            cls["prime_non_delta0"].append(k)
        elif k in (((1, 1, 11), 0), ((1, 11, 11), 0)):
            cls["exotic11"].append(k)
        elif k[0] in ((10, 10, 12), (10, 12, 12)):
            cls["exotic12"].append(k)
        elif max(k[0]) == 11:
            cls["others11"].append(k)
        else:
            cls["others12"].append(k)
    tax_ok = all(len(cls[c]) == TAXONOMY[c] for c in cls)
    tax_ok = tax_ok and sum(len(cls[c]) for c in cls) == TAXONOMY["total"]
    d0_11 = [k for k in cls["delta0"] if k[0] == (11, 11, 11)]
    d0_12 = [k for k in cls["delta0"] if k[0] == (12, 12, 12)]
    tax_ok = tax_ok and len(d0_11) == FOCUS["d0_11_keys"]
    tax_ok = tax_ok and len(d0_12) == D0_PINS["d0_12_keys"]
    tax_ok = tax_ok and sum(len(newkeys[k]) for k in d0_11) == \
        FOCUS["d0_11_profiles"]
    tax_ok = tax_ok and sum(len(newkeys[k]) for k in d0_12) == \
        D0_PINS["d0_12_profiles"]
    record("TAX: 650 = 23 d0 + 51 prime-nD0 + 2 exotic11 + 20 exotic12 "
           "+ 222 others11 + 332 others12", tax_ok,
           {c: len(cls[c]) for c in cls})

    # ---- focus columns cover ALL profiles of the 64 keys
    prime11 = cls["prime_non_delta0"] + d0_11
    exotic11 = cls["exotic11"]
    focus_keys = prime11 + exotic11
    A11 = new["r11_focus"]
    A10 = new["r10_focus"]
    foc_ok = len(A11) == FOCUS["records"] and len(A10) == FOCUS["records"]
    foc_ok = foc_ok and set(A11) == set(A10)
    got_keys = {}
    for i in A11:
        got_keys.setdefault(key_of(profiles[i]), []).append(i)
    foc_ok = foc_ok and len(got_keys) == FOCUS["keys"]
    foc_ok = foc_ok and set(got_keys) == set(focus_keys)
    for k in focus_keys:
        foc_ok = foc_ok and sorted(got_keys[k]) == sorted(newkeys[k])
    n_prime = sum(len(got_keys[k]) for k in prime11)
    n_ex = sum(len(got_keys[k]) for k in exotic11)
    foc_ok = foc_ok and n_prime == FOCUS["prime11_profiles"]
    foc_ok = foc_ok and n_ex == FOCUS["exotic11_profiles"]
    record("FOC: r=11/r=10 focus columns cover ALL profiles of the 64 "
           "keys (1619 = 1607 prime-11 + 12 exotic11)", foc_ok,
           {"keys": len(got_keys), "prime11_profiles": n_prime,
            "exotic11_profiles": n_ex})

    # ---- S1: prime-11 uniformly determined at r=11, chain survivor P_1
    det_keys_11 = [k for k in got_keys
                   if all(det_of_mask(A11[i][0]) for i in got_keys[k])]
    s1_ok = set(det_keys_11) == set(prime11)
    chain_of = {}
    for k in focus_keys:
        chains = [i for i in newkeys[k]
                  if profiles[i][2] == 0 and profiles[i][4] == 0
                  and profiles[i][5] == 0]
        if len(chains) != 1:
            s1_ok = False
            break
        chain_of[k] = chains[0]
    g_mism = 0
    chain_survivors = {}
    for k in prime11:
        ci = chain_of[k]
        sv_bits = mask_bits(A11[ci][0])
        chain_survivors[kstr(k)] = sv_bits
        if len(sv_bits) != 1:
            s1_ok = False
        for i in got_keys[k]:
            if mask_bits(A11[i][0]) != sv_bits:
                g_mism += 1
    s1_ok = s1_ok and g_mism == 0
    s1_ok = s1_ok and all(v == [S1_PINS["chain_survivor"]]
                           for v in chain_survivors.values())
    s1_ok = s1_ok and len(chain_survivors) == S1_PINS["uniform_det_keys"]
    record("S1: 62 prime-11 keys (incl (11,11,11)xG) UNIFORM_DET at r=11 "
           "with chain survivor P_1 (G' finite anchor)", s1_ok,
           {"uniform_det_keys": len(det_keys_11), "chain_survivor": 1,
            "profile_survivor_mismatches": g_mism,
            "chain_survivors": chain_survivors})

    # ---- S2: exotic11 uniformly NON-determined at r=11
    ex_sv = sorted({A11[i][0] for k in exotic11 for i in got_keys[k]})
    s2_ok = (all(not det_of_mask(A11[i][0])
                 for k in exotic11 for i in got_keys[k])
             and len(ex_sv) == 1 and ex_sv[0] == S2_PINS["exotic11_sv_mask"])
    record("S2: exotic11 (1,1,11)|0,(1,11,11)|0 UNIFORM_NDET at r=11 "
           "(sv mask 0b11)", s2_ok,
           {"keys": [kstr(k) for k in exotic11], "sv_masks": ex_sv})

    # ---- O1: r=10 focus classification (below-M structure)
    det10 = [k for k in got_keys
             if all(det_of_mask(A10[i][0]) for i in got_keys[k])]
    ndet10 = [k for k in got_keys
              if all(not det_of_mask(A10[i][0]) for i in got_keys[k])]
    mixed10 = [k for k in got_keys
               if k not in det10 and k not in ndet10]
    o1_ok = (len(det10) == O1_PINS["det10"] and
             len(ndet10) == O1_PINS["ndet10"] and
             len(mixed10) == O1_PINS["mixed10"] and
             set(det10) == set(d0_11) | set(exotic11) and
             set(ndet10) == set(cls["prime_non_delta0"]))
    record("O1: r=10 focus = 13 uniform-det (11 d0_11 + 2 exotic11) / "
           "51 uniform-ndet (prime-11 dormant) / 0 mixed", o1_ok,
           {"det10": len(det10), "ndet10": len(ndet10),
            "mixed10": len(mixed10)})

    # ---- D1/EX11: exotic11 deception window [2, M-1] closed at r=M
    d1_bad = 0
    for k in exotic11:
        for i in got_keys[k]:
            for rr in range(2, 11):
                col = cols[rr] if rr <= 9 else A10
                if not det_of_mask(col[i][0]):
                    d1_bad += 1
    d1_ok = d1_bad == 0
    ex11_data = {"profiles": FOCUS["exotic11_profiles"],
                 "det_columns_r2_r10": 9, "violations": d1_bad,
                 "family": "(1,1,p),(1,p,p) p in {3,5,7} (K0916) + p=11"}
    record("EX11: exotic11 deceptive window r=2..10 (12 profiles x 9 "
           "columns all det), flip to uniform-ndet exactly at r=M=11; "
           "deception family extends to p=11 (6->8 keys)", d1_ok, ex11_data)

    # ---- P11: prime-11 dormancy structure below M (finite observation)
    dorm = {}
    p11_ok = True
    for rr in range(2, 11):
        col = cols[rr] if rr <= 9 else A10
        n_ndet = sum(1 for k in cls["prime_non_delta0"]
                     for i in newkeys[k] if not det_of_mask(col[i][0]))
        dorm["r%d" % rr] = n_ndet
        if n_ndet != P11_DORMANCY["ndet_by_r"][rr]:
            p11_ok = False
    n_prof = sum(len(newkeys[k]) for k in cls["prime_non_delta0"])
    p11_ok = p11_ok and n_prof == P11_DORMANCY["profiles"]
    record("P11: prime-11 dormancy is graded below M: mixed at r=2..6 "
           "(90/273/273/704/704 of 1271 ndet), uniform-ndet at r=7..10, "
           "uniform-det at r=11=M (onset at M)", p11_ok,
           {"ndet_by_r": dorm, "profiles": n_prof})

    # ---- D0C: Delta=0 anchors on committed columns (Theorem D redundant)
    d0c_bad = 0
    d0c_n = 0
    for C, group in ((11, d0_11), (12, d0_12)):
        for rr in range(2, 10):
            surv = theorem_d(C, rr)[1]
            for k in group:
                for i in newkeys[k]:
                    sv = cols[rr][i][0]
                    d0c_n += 1
                    if (not det_of_mask(sv) or
                            (sv & -sv) != (1 << surv)):
                        d0c_bad += 1
    # (11,11,11) at r=10 and r=11 (focus)
    for rr, col in ((10, A10), (11, A11)):
        surv = theorem_d(11, rr)[1]
        for k in d0_11:
            for i in newkeys[k]:
                sv = col[i][0]
                d0c_n += 1
                if (not det_of_mask(sv) or (sv & -sv) != (1 << surv)):
                    d0c_bad += 1
    d0c_ok = d0c_bad == 0
    record("D0C: Delta=0 profiles det with Theorem-D survivor on "
           "committed r=2..9 (both (11,11,11) and (12,12,12)) and "
           "focus r=10/r=11 ((11,11,11))", d0c_ok,
           {"profile_columns": d0c_n, "violations": d0c_bad})

    # ---- D0: (12,12,12) anchors at r=12 / r=11 (Theorem D machine anchors)
    D12 = new["r12_d0anchor"]
    D11 = new["d0_r11"]
    surv12 = theorem_d(12, 12)[1]
    surv11_ = theorem_d(12, 11)[1]
    d0_ok = (len(D12) == D0_PINS["d0_12_keys"] and
             len(D11) == D0_PINS["d0_12_keys"])
    for i, (sv, fl, st) in D12.items():
        if key_of(profiles[i])[0] != (12, 12, 12):
            d0_ok = False
        if not det_of_mask(sv) or mask_bits(sv) != [surv12]:
            d0_ok = False
    for i, (sv, fl, st) in D11.items():
        if key_of(profiles[i])[0] != (12, 12, 12):
            d0_ok = False
        if not det_of_mask(sv) or mask_bits(sv) != [surv11_]:
            d0_ok = False
    d0_ok = d0_ok and surv12 == D0_PINS["r12_survivor"]
    d0_ok = d0_ok and surv11_ == D0_PINS["r11_survivor"]
    record("D0: (12,12,12)xG=0..11 cheapest anchors det with Theorem-D "
           "survivor P_11 at r=12 / P_10 at r=11 (full uniformity of "
           "Delta=0 rests on Theorem D, universal)", d0_ok,
           {"r12_survivor": surv12, "r11_survivor": surv11_,
            "anchors": len(D12) + len(D11)})

    # ---- EX12: exotic12 sub-M flip (det r=2..10, ndet at r=11=M-1, r=12=M)
    E10 = new["ex12_r10"]
    E11 = new["ex12_r11"]
    W12 = new["r12_witness"]
    ex12_keys = cls["exotic12"]
    ex12_ok = len(ex12_keys) == EX12_PINS["keys"]
    n_ex12_prof = sum(len(newkeys[k]) for k in ex12_keys)
    ex12_ok = ex12_ok and n_ex12_prof == EX12_PINS["profiles"]
    bad_low = 0
    for rr in range(2, 10):
        for k in ex12_keys:
            for i in newkeys[k]:
                if not det_of_mask(cols[rr][i][0]):
                    bad_low += 1
    ex12_ok = ex12_ok and bad_low == 0
    det10c = sum(1 for i, (sv, fl, st) in E10.items() if det_of_mask(sv))
    ndet11c = sum(1 for i, (sv, fl, st) in E11.items()
                  if not det_of_mask(sv))
    ndet12c = sum(1 for i, (sv, fl, st) in W12.items()
                  if key_of(profiles[i])[0] in ((10, 10, 12), (10, 12, 12))
                  and not det_of_mask(sv))
    ex12_ok = (ex12_ok and det10c == EX12_PINS["r10_det"] and
               ndet11c == EX12_PINS["r11_ndet"] and
               ndet12c == EX12_PINS["r12_ndet"])
    record("EX12: exotic12 (10,10,12),(10,12,12)xG=0..9: all 1425 "
           "profiles det on committed r=2..9; cheapest det at r=10; "
           "cheapest NON-det at r=11 (=M-1, sub-window flip) and r=12 "
           "(=M, dichotomy side)", ex12_ok,
           {"keys": len(ex12_keys), "profiles": n_ex12_prof,
            "committed_violations": bad_low, "r10_det": det10c,
            "r11_ndet": ndet11c, "r12_ndet": ndet12c})

    # ---- witness scans: cheapest-profile selection re-derived
    packed9_states = {i: cols[9][i][2] for i in cols[9]}

    def cheapest(k):
        return min(newkeys[k], key=lambda i: (packed9_states[i], i))

    W11 = new["r11_witness"]
    n1_ok = len(W12) == 352 and len(W11) == 222
    sel_bad = 0
    for name, col, keyset in (("r12", W12, cls["exotic12"] + cls["others12"]),
                               ("r11", W11, cls["others11"])):
        got_ks = {key_of(profiles[i]) for i in col}
        if got_ks != set(keyset) or len(col) != len(keyset):
            n1_ok = False
        for i, (sv, fl, st) in col.items():
            if det_of_mask(sv):
                n1_ok = False
            if i != cheapest(key_of(profiles[i])):
                sel_bad += 1
    n1_ok = n1_ok and sel_bad == 0
    record("N1/N2: witness scans r=12 (352 = 20 exotic12 + 332 others12) "
           "and r=11 (222 others11): every witness NON-det and every "
           "witness IS the cheapest profile (states@r9 asc, canon "
           "tiebreak) re-derived from the committed r=9 column", n1_ok,
           {"selection_violations": sel_bad,
            "r12_ndet": sum(1 for v in W12.values() if not det_of_mask(v[0])),
            "r11_ndet": sum(1 for v in W11.values() if not det_of_mask(v[0]))})

    # ---- C1: key coverage and gamma-independence
    covered = set(got_keys) | {key_of(profiles[i]) for i in W12} | \
        {key_of(profiles[i]) for i in W11} | \
        {key_of(profiles[i]) for i in D12}
    c1_ok = covered == set(newkeys) and len(covered) == 650
    bym = {}
    fixed_status = {}
    for k in newkeys:
        if k in prime11:
            fixed_status[k] = "det"
        elif k in got_keys:  # exotic11
            fixed_status[k] = "ndet"
        elif any(i in W11 for i in newkeys[k]):  # others11 witness
            fixed_status[k] = "ndet"
        elif any(i in W12 for i in newkeys[k]):  # exotic12/others12
            fixed_status[k] = "ndet"
        elif any(i in D12 for i in newkeys[k]):  # d0_12 anchors
            fixed_status[k] = "det"
        else:
            fixed_status[k] = "UNCOVERED"
            c1_ok = False
        bym.setdefault(k[0], set()).add(fixed_status[k])
    mixed_m = [m for m, s in bym.items() if len(s) != 1]
    c1_ok = c1_ok and len(mixed_m) == 0 and len(bym) == 144
    record("C1: 64 focus + 222 + 352 + 12 anchor keys == 650 distinct "
           "new keys exactly; fixed-point status is gamma-independent "
           "(144 multisets, 0 mixed)", c1_ok,
           {"covered": len(covered), "multisets": len(bym),
            "gamma_mixed_multisets": len(mixed_m)})

    # ---- PD12: the cap<=12 dichotomy on the 650 new keys
    pd_set = set(k for k in newkeys
                 if is_delta0(k) or is_allprime(k))
    det_side = set(k for k in newkeys if fixed_status[k] == "det")
    pd_ok = det_side == pd_set
    pd_ok = pd_ok and len(pd_set) == PD12_PINS["det_new"]
    pd_ok = pd_ok and 650 - len(pd_set) == PD12_PINS["ndet_new"]
    pd_ok = pd_ok and len(cls["delta0"]) == PD12_PINS["delta0"]
    n_allprime = sum(1 for k in newkeys if is_allprime(k))
    pd_ok = pd_ok and n_allprime == PD12_PINS["allprime"]
    pd_ok = pd_ok and sum(1 for k in newkeys
                          if is_allprime(k) and is_delta0(k)) == \
        PD12_PINS["overlap"]
    pd_ok = pd_ok and (PD12_PINS["cap10_det"] + PD12_PINS["det_new"] ==
                       PD12_PINS["combined_det"])
    det_table = sorted(
        ({"key": kstr(k),
         "class": ("delta0" if is_delta0(k) else
                   ("prime" if is_allprime(k) else "other")),
         "survivor": mask_bits(new["r11_focus"][chain_of[k]][0])[0]
         if k in got_keys else
         (D0_PINS["r12_survivor"] if k[0] == (12, 12, 12) else None)}
        for k in det_side), key=lambda e: e["key"])
    ndet_table = sorted(
        ({"key": kstr(k),
          "witness_canon": (min(i for i in W11 if key_of(profiles[i]) == k)
                            if any(i in W11 for i in newkeys[k]) else
                            (min(i for i in W12 if key_of(profiles[i]) == k)
                             if any(i in W12 for i in newkeys[k]) else
                             min(i for i in newkeys[k])))}
         for k in newkeys if fixed_status[k] == "ndet"),
        key=lambda e: e["key"])
    record("PD12: THEOREM (cap<=12 fixed point, 650 new keys): "
           "uniformly det at r >= max(M,2) <=> Delta=0 or all sizes in "
           "{2,3,5,7,11}; det 74 = 23 d0 + 51 prime (62 all-prime incl "
           "11 overlap), witness side 576; combined with K0916 "
           "(98 cap<=10 det keys) the cap<=12 dichotomy closes at "
           "172 det keys; Theorem J (K0906) extends each r=M column to "
           "all r >= max(M,2); Theorem E' (K0861) transfers to boards",
           pd_ok,
           {"det_new": len(det_side), "ndet_new": 650 - len(det_side),
            "both_direction_violations": len(det_side ^ pd_set),
            "det_keys": det_table, "ndet_witnesses": ndet_table})

    # ---- FL1: lemma FL on all 4445 new records
    fl_viol = 0
    fl_n = 0
    for name, (fn, sha, n, rr) in sorted(NEW_PINS.items()):
        col = new[name]
        for i, (sv, fl, st) in col.items():
            expect = 0
            for c in set(profile_sizes(profiles[i], 3)):
                expect |= 1 << (c % rr)
            fl_n += 1
            if fl != expect:
                fl_viol += 1
    record("FL1: first-losers == OR{1<<(C_i mod r)} on all 4445 new "
           "records (r=10/11/12/13 columns)", fl_viol == 0,
           {"records": fl_n, "violations": fl_viol})

    # ---- J13: Theorem J constancy anchor at r=13
    J13 = new["j13_anchor"]
    j_bad = 0
    j_src = {}
    for i, (sv13, fl13, st13) in J13.items():
        src = None
        for col, rr in ((W12, 12), (W11, 11), (A11, 11)):
            if i in col:
                src = col[i]
                j_src["%d" % i] = rr
                break
        if src is None:
            j_bad += 1
            j_src["%d" % i] = "none"
            continue
        if src[0] != sv13:
            j_bad += 1
    record("J13: 15 r=13 anchor records (10 witnesses + 5 prime-11 "
           "light) have sv mask identical to their r=11/r=12 source "
           "records (Theorem J finite anchor beyond the window)",
           j_bad == 0, {"mismatches": j_bad, "sources": j_src})

    # ---- LIVE: Python mask twin recomputation (independent implementation)
    live_bad = 0
    live_n = 0
    nodes_eq = 0
    nodes_total = 0

    def twin_check(i, rr, sv, fl, st):
        nonlocal live_bad, live_n, nodes_eq, nodes_total
        verdict, nodes = mask_verdict(list(profiles[i]), 3, rr,
                                      budget=50_000_000)
        ok = (verdict["determined"] == det_of_mask(sv) and
              verdict["survivors"] == mask_bits(sv) and
              verdict["first_losers"] == mask_bits(fl))
        live_n += 1
        nodes_total += 1
        if nodes == st:
            nodes_eq += 1
        if not ok:
            live_bad += 1

    for name in LIVE_COLS:
        rr = NEW_PINS[name][3]
        for i, (sv, fl, st) in sorted(new[name].items()):
            twin_check(i, rr, sv, fl, st)
    for col, rr in ((A11, 11), (A10, 10)):
        sel = set()
        for k in exotic11:
            sel |= set(newkeys[k])
        for k in d0_11:
            sel |= {i for i in newkeys[k] if col[i][2] <= LIVE_PINS["states_cap"]}
        for k in cls["prime_non_delta0"]:
            sel.add(chain_of[k])
            light = sorted((i for i in newkeys[k]
                            if col[i][2] <= LIVE_PINS["states_cap"]),
                           key=lambda i: (col[i][2], i))
            sel |= set(light[:LIVE_PINS["extra_per_key"]])
        for i in sorted(sel):
            sv, fl, st = col[i]
            twin_check(i, rr, sv, fl, st)
    live_ok = (live_bad == LIVE_PINS["mismatches"] and
               live_n == LIVE_PINS["records"] and
               (nodes_eq == live_n) == LIVE_PINS["nodes_eq_states"])
    record("LIVE: Python mask twin (independent implementation, "
           "verbatim K0912 block) recomputes every witness/probe/anchor "
           "record (1007) plus focus samples (exotic11 all, d0_11 and "
           "prime-11 under the states cap with chain records): verdict "
           "equality on all 1710 records AND twin state count == "
           "engine states on every record", live_ok,
           {"records": live_n, "mismatches": live_bad,
            "nodes_eq_states": nodes_eq, "states_cap":
            LIVE_PINS["states_cap"]})

    all_ok = all(c["ok"] for c in checks)
    return {"all_ok": all_ok, "checks": checks,
            "meta": {"theorem": "prime dichotomy cap<=12 (PD12)",
                     "engine": "mask_engine_fast2.js sha256 "
                               "b904760e109e9adf1689b91e7dcbb1aa530704af322ee7808e2304d0377586de",
                     "columns_committed": sorted(COMMITTED_PINS),
                     "columns_new": sorted(NEW_PINS)}}


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
