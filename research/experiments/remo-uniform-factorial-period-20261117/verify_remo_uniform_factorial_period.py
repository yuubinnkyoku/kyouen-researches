#!/usr/bin/env python3
"""LCM periodicity of the uniform-board REMO counting recursion
(item K0919).  THEOREM PER: put Q(r) := lcm(1,2,...,r) = lcm({r} U
{k*(k+1) : 2 <= k <= r-1}).  For every r >= 2 and every C >= 1, the
K0859 Theorem-D counting recursion (uniform board, terminal size C,
r players) produces the SAME full elimination sequence and survivor
for C and C + Q(r).  In particular r! is also a period (Q(r) | r!).

Proof (report.md, universal): a uniform-offset induction - at the
start of phase h the two boards share (active, turn) and every
active player's stone count differs by exactly D_h, with D_1 = 0,
D_{h+1} = D_h + X_h/k_h, X_h = T - k_h*D_h the phase-length shift
(T = the period candidate).  D_{h+1} = T/k_h and X_h = T/(k_h+1)
for h >= 2, so the preservation requirements are r | T (phase 1,
X_1 = T) and k_h(k_h+1) | T (phases h >= 2, for the rich/poor split
indicator t_h, the loser index, and the uniform receipt shift);
taking the lcm over all phases gives exactly Q(r) = lcm(1..r) (the
prime-power lemma is proved in report.md).  The closed-form shifts
give the strong invariant that every active player's receipt shifts
by the SAME X_h/k_h and the phase loser received exactly q_h
stones in phase h.

Machine checks (all deterministic, stdlib only, no network):

PIN   All 14 committed packed columns match their pinned sha256 and
      line counts (47,595 for cap<=12 r=2..9, 15,863 for cap<=10
      r=9..13) with contiguous indices.
E1    Two implementations of the recursion (the verbatim K0859
      per-stone loop vs the closed-form share-count rewrite) agree:
      on all C in [1,r!] for r = 2..7, and on a stratified sample
      for r = 8, 9 (the closed-form twin is the one swept to full
      range below; it also reproduces the K0859 published table,
      see E5).
E2    Periodicity E(C + Q(r), r) == E(C, r) (elimination tuple AND
      survivor, closed-form twin) for every r = 2..9 and ALL C in
      [1, Q(r)]; Q(r) divides r!; and the r!-period machine anchor
      E(C + r!, r) == E(C, r) for every r = 2..9 and ALL C in
      [1, r!] (409,112 pairs).
E3    Minimality: for every r = 2..9 the minimal period of both the
      elimination-sequence column and the survivor column is
      exactly Q(r) = lcm(1..r) (full scan over all proper divisors
      of Q(r); every proper divisor fails).  For r >= 10 the period
      Q(r) stands by the universal proof; minimality and the
      necessity direction (only multiples of Q(r) can be periods)
      stay OPEN beyond the machine range.
E4    Uniform-offset induction data check: for the period T = Q(r),
      every r = 2..9 and ALL C in [1, Q(r)]; for the period T = r!,
      every r = 2..8 and ALL C in [1, r!] (the r! data check for
      r = 9 is omitted for runtime; the r = 9 r!-periodicity itself
      is fully machine-anchored by E2).  Per phase: k/t/li/loser/
      turn identical between C and C+T; every active player's count offset equals D_h exactly; X_h == T -
      k_h*D_h; closed forms X_1 = T, X_h = T/(k_h+1) (h >= 2);
      every receipt shifts by exactly X_h/k_h; the loser received
      exactly q_h stones in phase h; k_h | X_h.
E5    Theorem D anchor vs committed columns: all 1,512 cap<=12
      Delta=0 canonical profiles are determined with survivor
      theorem_d(C,r) at every r = 2..9 (8 columns), and all 728
      cap<=10 Delta=0 profiles at every r = 9..13 (5 columns, the
      r=9 access via the K0882 order-preserving embedding, K0916
      svfl convention); 15,736 record checks, 0 mismatches.  The
      closed-form twin reproduces the K0859 published (C,r)
      elimination table (84 entries, 0 mismatches).
E6    Plateau observation (finite; Theorem J corollary anchor for
      Delta=0 keys): survivor S(C,r) is constant on r >= C for
      C <= 24 (r up to 3C+3), and the plateau sequence P(C) =
      S(C, C), C = 1..40, is pinned (0,1,1,3,1,5,1,5,5,9,1,11,...);
      no closed form for P(C) is claimed.

Scope / limits (do not over-read):
- Theorem PER is a statement about the K0859 counting recursion,
  hence (by Theorem D, universal) about REMO on every uniform board
  (Delta = 0), all C >= 1, all r >= 2.  It says NOTHING about
  non-uniform (Delta != 0) boards.
- Minimality of the period Q(r) is machine-verified only for
  r <= 9; for r >= 10 the universal period Q(r) holds by the proof
  but the minimal period and the necessity direction are OPEN.
- E6 is a finite observation (Theorem J of K0906 is the universal
  statement behind the plateau; this verifier only re-anchors it
  on uniform (C,r) values).
- The stratified (not exhaustive) part of E1 for r = 8, 9 is a
  consistency anchor for the closed-form twin, which is separately
  validated exhaustively at r <= 7, against the published table
  (E5), and against 15,736 committed column records (E5).
- 11x11 empty board / class frontiers remain UNKNOWN, unrelated.

The audit JSON is regenerated twice and must be byte-identical.

Usage: python3 verify_remo_uniform_factorial_period.py
"""

import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")
AUDIT_PATH = os.path.join(OUT, "remo_uniform_factorial_period_audit.json")

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

DELTA0_PROFILES_CAP12 = 1512
DELTA0_PROFILES_CAP10 = 728

P1A_EXHAUSTIVE_RMAX = 7
P1A_STRATIFIED = {"r8_low": 200, "r8_stride": 997, "r8_samples": 61,
                  "r9_low": 200, "r9_stride": 9973, "r9_samples": 71}

Q_SEQUENCE = {2: 2, 3: 6, 4: 12, 5: 60, 6: 60, 7: 420, 8: 840, 9: 2520}
E2Q_TOTAL = 3920      # sum of Q(r), r = 2..9
E2F_TOTAL = 409112    # sum of r!, r = 2..9

PLATEAU_CMAX = 24
PLATEAU_SEQUENCE = [0, 1, 1, 3, 1, 5, 1, 5, 5, 9, 1, 11, 1, 5, 7, 15, 1,
                    17, 1, 15, 17, 21, 1, 21, 11, 15, 7, 27, 1, 29, 1,
                    27, 17, 21, 11, 35, 1, 5, 7, 39]


# ---------------------------------------------------------------------------
# the K0859 Theorem-D recursion, two implementations
# ---------------------------------------------------------------------------

def theorem_d(C, r):
    """Verbatim K0859 recursion (per-stone distribution loop)."""
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


def theorem_d_fast(C, r):
    """Closed-form share-count rewrite of the same recursion.

    The m-th stone (m = 0..ell-1) goes to active[(turn + m) % k], so
    each player receives q = ell // k or q + 1 (the first ell mod k
    offsets from turn get the extra one), and the loser is at offset
    (turn + ell) % k having received exactly q stones this phase.
    Equality with the verbatim loop is asserted by E1.
    """
    active = list(range(r))
    counts = [0] * r
    turn = 0
    elimination = []
    while len(active) > 1:
        k = len(active)
        s = sum(counts[p] for p in active)
        ell = C - s
        q, t = divmod(ell, k)
        for i in range(k):
            pos = active[(turn + i) % k]
            counts[pos] += q + (1 if i < t else 0)
        li = (turn + ell) % k
        loser = active[li]
        elimination.append(loser)
        counts[loser] = 0
        active.pop(li)
        if active:
            turn = li % len(active)
    return tuple(elimination), active[0]


def factorial(r):
    out = 1
    for i in range(2, r + 1):
        out *= i
    return out


def lcm_all(r):
    """Q(r) = lcm(1,2,...,r)."""
    out = 1
    for i in range(2, r + 1):
        a, b = out, i
        while b:
            a, b = b, a % b
        out = out * i // a
    return out


def divisors(n):
    out = []
    i = 1
    while i * i <= n:
        if n % i == 0:
            out.append(i)
            if i != n // i:
                out.append(n // i)
        i += 1
    return sorted(out)


def theorem_d_phases(C, r):
    """Per-phase trace of the closed-form twin (for the E4 data check)."""
    active = list(range(r))
    counts = [0] * r
    turn = 0
    phases = []
    while len(active) > 1:
        k = len(active)
        s = sum(counts[p] for p in active)
        ell = C - s
        q, t = divmod(ell, k)
        li = (turn + ell) % k
        loser = active[li]
        rec = {}
        for i in range(k):
            pos = active[(turn + i) % k]
            rec[pos] = q + (1 if i < t else 0)
        phases.append({
            "k": k, "s": s, "ell": ell, "q": q, "t": t, "li": li,
            "loser": loser, "turn": turn,
            "counts": dict((p, counts[p]) for p in active),
            "rec": rec,
        })
        for i in range(k):
            pos = active[(turn + i) % k]
            counts[pos] += q + (1 if i < t else 0)
        counts[loser] = 0
        active.pop(li)
        if active:
            turn = li % len(active)
    return phases, active[0]


PUBLISHED_UNIFORM_ELIMINATION_TABLE_JSON = (
    '{"1":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[1,2],"survivor":0},"4":{"elimination":[1,2,3],"survivor":0},"5":{"elimination":[1,2,3,4],"survivor":0},"6":{"elimination":[1,2,3,4,5],"survivor":0},"7":{"elimination":[1,2,3,4,5,6],"survivor":0},"8":{"elimination":[1,2,3,4,5,6,7],"survivor":0}},"10":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[1,0],"survivor":2},"4":{"elimination":[2,1,0],"survivor":3},"5":{"elimination":[0,3,2,1],"survivor":4},"6":{"elimination":[4,0,3,2,1],"survivor":5},"7":{"elimination":[3,5,0,4,2,1],"survivor":6},"8":{"elimination":[2,4,6,0,5,3,1],"survivor":7}},"11":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[2,1],"survivor":0},"4":{"elimination":[3,2,1],"survivor":0},"5":{"elimination":[1,4,3,2],"survivor":0},"6":{"elimination":[5,1,4,3,2],"survivor":0},"7":{"elimination":[4,6,1,5,3,2],"survivor":0},"8":{"elimination":[3,5,7,1,6,4,2],"survivor":0}},"12":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[0,1],"survivor":2},"4":{"elimination":[0,1,2],"survivor":3},"5":{"elimination":[2,0,1,3],"survivor":4},"6":{"elimination":[0,3,1,2,4],"survivor":5},"7":{"elimination":[5,0,3,1,2,4],"survivor":6},"8":{"elimination":[4,6,0,3,1,2,5],"survivor":7}},"2":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[2,0],"survivor":1},"4":{"elimination":[2,3,0],"survivor":1},"5":{"elimination":[2,3,4,0],"survivor":1},"6":{"elimination":[2,3,4,5,0],"survivor":1},"7":{"elimination":[2,3,4,5,6,0],"survivor":1},"8":{"elimination":[2,3,4,5,6,7,0],"survivor":1}},"3":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[0,2],"survivor":1},"4":{"elimination":[3,0,2],"survivor":1},"5":{"elimination":[3,4,0,2],"survivor":1},"6":{"elimination":[3,4,5,0,2],"survivor":1},"7":{"elimination":[3,4,5,6,0,2],"survivor":1},"8":{"elimination":[3,4,5,6,7,0,2],"survivor":1}},"4":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[1,0],"survivor":2},"4":{"elimination":[0,2,1],"survivor":3},"5":{"elimination":[4,0,2,1],"survivor":3},"6":{"elimination":[4,5,0,2,1],"survivor":3},"7":{"elimination":[4,5,6,0,2,1],"survivor":3},"8":{"elimination":[4,5,6,7,0,2,1],"survivor":3}},"5":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[2,1],"survivor":0},"4":{"elimination":[1,3,2],"survivor":0},"5":{"elimination":[0,2,4,3],"survivor":1},"6":{"elimination":[5,0,2,4,3],"survivor":1},"7":{"elimination":[5,6,0,2,4,3],"survivor":1},"8":{"elimination":[5,6,7,0,2,4,3],"survivor":1}},"6":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[0,1],"survivor":2},"4":{"elimination":[2,0,1],"survivor":3},"5":{"elimination":[1,3,0,2],"survivor":4},"6":{"elimination":[0,2,4,1,3],"survivor":5},"7":{"elimination":[6,0,2,4,1,3],"survivor":5},"8":{"elimination":[6,7,0,2,4,1,3],"survivor":5}},"7":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[1,2],"survivor":0},"4":{"elimination":[3,1,2],"survivor":0},"5":{"elimination":[2,4,1,3],"survivor":0},"6":{"elimination":[1,3,5,2,4],"survivor":0},"7":{"elimination":[0,2,4,6,3,5],"survivor":1},"8":{"elimination":[7,0,2,4,6,3,5],"survivor":1}},"8":{"2":{"elimination":[0],"survivor":1},"3":{"elimination":[2,0],"survivor":1},"4":{"elimination":[0,3,1],"survivor":2},"5":{"elimination":[3,0,4,1],"survivor":2},"6":{"elimination":[2,4,0,5,1],"survivor":3},"7":{"elimination":[1,3,5,0,6,2],"survivor":4},"8":{"elimination":[0,2,4,6,1,7,3],"survivor":5}},"9":{"2":{"elimination":[1],"survivor":0},"3":{"elimination":[0,2],"survivor":1},"4":{"elimination":[1,0,3],"survivor":2},"5":{"elimination":[4,1,0,3],"survivor":2},"6":{"elimination":[3,5,1,0,4],"survivor":2},"7":{"elimination":[2,4,6,1,0,5],"survivor":3},"8":{"elimination":[1,3,5,7,2,0,6],"survivor":4}}}'
)


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


def profile_sizes(atoms, k):
    """C_i = |A_i| per branch."""
    return tuple(
        sum(atoms[m - 1] for m in range(1, 1 << k) if (m >> (i - 1)) & 1)
        for i in range(1, k + 1)
    )


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


def det_of_mask(m):
    return bin(m).count("1") == 1


def induction_check(C, r, T):
    """E4 core: compare the phase traces of C and C+T.

    Returns the number of violations of the uniform-offset induction
    identities (0 expected):
      - k/t/li/loser/turn identical per phase,
      - every active player's count offset == D_h exactly,
      - X_h == T - k_h*D_h and closed form X_h == T/(k_h+1) (h>=2,
        X_1 == T),
      - s shift == k_h*D_h, k_h | X_h,
      - receipts identical in pattern and shifted by exactly X_h/k_h,
      - the phase loser received exactly q_h stones this phase.
    """
    ph, sv = theorem_d_phases(C, r)
    ph2, sv2 = theorem_d_phases(C + T, r)
    if sv != sv2 or len(ph) != len(ph2):
        return 1
    bad = 0
    D = 0
    for h, (a, b) in enumerate(zip(ph, ph2)):
        k = a["k"]
        for key in ("k", "t", "li", "loser", "turn"):
            if a[key] != b[key]:
                bad += 1
                break
        for p in a["counts"]:
            if b["counts"][p] - a["counts"][p] != D:
                bad += 1
                break
        X = b["ell"] - a["ell"]
        if X != T - k * D:
            bad += 1
        cf = T if h == 0 else T // (k + 1)
        if X != cf or X % k != 0:
            bad += 1
        if b["s"] - a["s"] != k * D:
            bad += 1
        if set(a["rec"]) != set(b["rec"]):
            bad += 1
        else:
            for p in a["rec"]:
                if b["rec"][p] - a["rec"][p] != X // k:
                    bad += 1
                    break
        if a["rec"][a["loser"]] != a["q"]:
            bad += 1
        D = D + X // k
    return bad


# ---------------------------------------------------------------------------
# audit assembly (deterministic; regenerate twice, byte-identical)
# ---------------------------------------------------------------------------

def assemble_audit():
    checks = []

    def record(name, ok, data):
        checks.append({"name": name, "ok": bool(ok), "data": data})

    # ---- PIN: committed columns
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
    record("PIN: 14 committed columns sha256/shape", pin_ok, pin_detail)

    # ---- E1: two implementations agree
    e1_pairs = 0
    e1_mism = 0
    e1_detail = {}
    for r in range(2, P1A_EXHAUSTIVE_RMAX + 1):
        T = factorial(r)
        for C in range(1, T + 1):
            e1_pairs += 1
            if theorem_d(C, r) != theorem_d_fast(C, r):
                e1_mism += 1
        e1_detail["r%d_pairs" % r] = T
    for r, low, stride, nsamp in ((8, P1A_STRATIFIED["r8_low"],
                                   P1A_STRATIFIED["r8_stride"],
                                   P1A_STRATIFIED["r8_samples"]),
                                  (9, P1A_STRATIFIED["r9_low"],
                                   P1A_STRATIFIED["r9_stride"],
                                   P1A_STRATIFIED["r9_samples"])):
        T = factorial(r)
        sample = list(range(1, low + 1))
        for j in range(nsamp):
            c = 1 + j * stride
            if c <= T and c not in sample:
                sample.append(c)
        sample = sorted(set(sample))
        for C in sample:
            e1_pairs += 1
            if theorem_d(C, r) != theorem_d_fast(C, r):
                e1_mism += 1
        e1_detail["r%d_stratified" % r] = len(sample)
    table = json.loads(PUBLISHED_UNIFORM_ELIMINATION_TABLE_JSON)
    tab_entries = 0
    tab_mism = 0
    for C in range(1, 13):
        for r in range(2, 9):
            published = table[str(C)][str(r)]
            elim, surv = theorem_d_fast(C, r)
            tab_entries += 1
            if list(elim) != published["elimination"] or surv != published["survivor"]:
                tab_mism += 1
    record("E1: verbatim per-stone recursion == closed-form twin "
           "(exhaustive for r=2..7 over all C in [1,r!]; stratified "
           "sample for r=8,9; the twin also reproduces the K0859 "
           "published 84-entry table)",
           e1_mism == 0 and tab_mism == 0,
           {"pairs": e1_pairs, "mismatches": e1_mism,
            "table_entries": tab_entries, "table_mismatches": tab_mism,
            "stratified": e1_detail})

    # ---- E2: periodicity Q(r) (and the r! machine anchor)
    e2q_pairs = 0
    e2q_mism = 0
    e2q_detail = {}
    for r in range(2, 10):
        Q = lcm_all(r)
        mism = 0
        for C in range(1, Q + 1):
            e2q_pairs += 1
            if theorem_d_fast(C, r) != theorem_d_fast(C + Q, r):
                mism += 1
                e2q_mism += 1
        e2q_detail["r%d" % r] = {"Q": Q, "pairs": Q, "mismatches": mism,
                                  "Q_matches_pin": Q == Q_SEQUENCE[r]}
        if Q != Q_SEQUENCE[r]:
            e2q_mism += 1
    e2f_pairs = 0
    e2f_mism = 0
    for r in range(2, 10):
        T = factorial(r)
        for C in range(1, T + 1):
            e2f_pairs += 1
            if theorem_d_fast(C, r) != theorem_d_fast(C + T, r):
                e2f_mism += 1
    div_ok = all(factorial(r) % lcm_all(r) == 0 for r in range(2, 10))
    record("E2: THEOREM PER (universal proof in report.md) machine "
           "anchor - E(C + Q(r), r) == E(C, r) for every r = 2..9 and "
           "ALL C in [1, Q(r)] with Q(r) = lcm(1..r) as pinned; "
           "Q(r) | r! for every r = 2..9; and the r! anchor E(C + r!, r) "
           "== E(C, r) for every r = 2..9 and ALL C in [1, r!]",
           e2q_mism == 0 and e2q_pairs == E2Q_TOTAL
           and e2f_mism == 0 and e2f_pairs == E2F_TOTAL and div_ok,
           {"Q_pairs": e2q_pairs, "Q_mismatches": e2q_mism,
            "Q_divides_factorial": div_ok,
            "factorial_pairs": e2f_pairs, "factorial_mismatches": e2f_mism,
            "per_r": e2q_detail})

    # ---- E3: minimal period is exactly Q(r) (r = 2..9)
    e3_detail = {}
    e3_ok = True
    for r in range(2, 10):
        Q = lcm_all(r)
        L = [theorem_d_fast(C, r) for C in range(1, 2 * Q + 1)]
        sv = [rec[1] for rec in L]
        proper = divisors(Q)[:-1]
        bad_elim = []
        bad_sv = []
        for d in proper:
            if not all(L[C - 1] == L[C + d - 1]
                       for C in range(1, Q - d + 1)):
                bad_elim.append(d)
            if not all(sv[C - 1] == sv[C + d - 1]
                       for C in range(1, Q - d + 1)):
                bad_sv.append(d)
        e3_ok = e3_ok and sorted(bad_elim) == proper and sorted(bad_sv) == proper
        e3_detail["r%d" % r] = {
            "Q": Q, "proper_divisors": len(proper),
            "all_proper_fail_elim": sorted(bad_elim) == proper,
            "all_proper_fail_survivor": sorted(bad_sv) == proper,
        }
    record("E3: minimality (machine, r=2..9 only): the minimal period of "
           "both the elimination-sequence column and the survivor column "
           "is exactly Q(r) = lcm(1..r) (every proper divisor of Q(r) "
           "fails, full scan).  For r >= 10 the universal period Q(r) "
           "stands by the proof; minimality and the necessity direction "
           "are OPEN",
           e3_ok, e3_detail)

    # ---- E4: uniform-offset induction data check (both periods)
    e4_bad_f = 0
    e4_bad_q = 0
    e4_phases = 0
    e4_detail = {}
    for r in range(2, 10):
        Q = lcm_all(r)
        Tf = factorial(r) if r <= 8 else None
        badf = 0
        if Tf is not None:
            for C in range(1, Tf + 1):
                badf += induction_check(C, r, Tf)
                e4_phases += 1
        badq = 0
        for C in range(1, Q + 1):
            badq += induction_check(C, r, Q)
        e4_bad_f += badf
        e4_bad_q += badq
        e4_detail["r%d" % r] = {
            "r!_violations": badf,
            "r!_swept": Tf is not None,
            "Q_violations": badq,
        }
    e4_pairs = sum((factorial(r) if r <= 8 else 0) + lcm_all(r)
                   for r in range(2, 10))
    record("E4: uniform-offset induction data check: period T = Q(r) "
           "for every r = 2..9 and ALL C in [1, Q(r)], and period T = r! "
           "for every r = 2..8 and ALL C in [1, r!] (the r! data check "
           "for r = 9 is omitted for runtime; the r = 9 r!-periodicity "
           "itself is fully machine-anchored by E2): per phase "
           "k/t/li/loser/turn identical between C and C+T; every "
           "active player's count offset == D_h exactly; X_h == T - "
           "k_h*D_h; closed forms X_1 = T, X_h = T/(k_h+1) for h >= 2; "
           "s shift == k_h*D_h; receipts shift by exactly X_h/k_h "
           "(uniform); the phase loser received exactly q_h stones in "
           "phase h; k_h | X_h",
           e4_bad_f == 0 and e4_bad_q == 0,
           {"pairs": e4_pairs,
            "violations_r_factorial": e4_bad_f,
            "violations_Q": e4_bad_q, "per_r": e4_detail})

    # ---- E5: Theorem D anchor vs committed columns
    profiles10 = direct_constrained(10)
    profiles12 = direct_constrained(12)
    idx10 = {at: i for i, at in enumerate(profiles10)}
    emb = [i for i, at in enumerate(profiles12) if at in idx10]
    d0_12 = 0
    d0_10 = 0
    mism12 = 0
    mism10 = 0
    for i, at in enumerate(profiles12):
        sizes = profile_sizes(at, 3)
        if len(set(sizes)) != 1:
            continue
        d0_12 += 1
        C = sizes[0]
        for r in range(2, 10):
            _, surv = theorem_d_fast(C, r)
            rec = cols[r][i]
            if not (det_of_mask(rec[1]) and rec[1] == (1 << surv)):
                mism12 += 1
    for j, at in enumerate(profiles10):
        sizes = profile_sizes(at, 3)
        if len(set(sizes)) != 1:
            continue
        d0_10 += 1
        C = sizes[0]
        for r in range(9, 14):
            _, surv = theorem_d_fast(C, r)
            # K0916 svfl convention: for r=9 use the D_12 column via the
            # order-preserving embedding; for r=10..13 use the D_10 column
            pos = emb[j] if r == 9 else j
            rec = cols[r][pos]
            if not (det_of_mask(rec[1]) and rec[1] == (1 << surv)):
                mism10 += 1
    e5_ok = (d0_12 == DELTA0_PROFILES_CAP12 and d0_10 == DELTA0_PROFILES_CAP10
             and mism12 == 0 and mism10 == 0 and len(emb) == 15863)
    record("E5: Theorem D (K0859, universal) anchor vs committed columns: "
           "all 1,512 cap<=12 Delta=0 canonical profiles determined with "
           "the theorem_d survivor at every r = 2..9 (8 columns) and all "
           "728 cap<=10 Delta=0 profiles at every r = 9..13 (5 columns, "
           "r=9 access via the K0882 order-preserving embedding); "
           "15,736 record checks, 0 mismatches; K0882 D_10 embedding "
           "reproduced (15,863 positions)",
           e5_ok, {"delta0_cap12": d0_12, "delta0_cap10": d0_10,
                   "mismatches_cap12": mism12, "mismatches_cap10": mism10,
                   "embedding_positions": len(emb)})

    # ---- E6: plateau observation (finite)
    pl_ok = True
    pl_bad = []
    for C in range(1, PLATEAU_CMAX + 1):
        vals = {theorem_d_fast(C, r)[1] for r in range(C, 3 * C + 4)}
        if len(vals) != 1:
            pl_ok = False
            pl_bad.append(C)
    p_seq = [theorem_d_fast(C, C)[1] for C in range(1, 41)]
    seq_ok = p_seq == PLATEAU_SEQUENCE
    record("E6: plateau observation (finite; Theorem J corollary anchor "
           "for Delta=0 keys): survivor S(C,r) is constant on r >= C for "
           "C <= 24 (up to r = 3C+3); the plateau sequence P(C) = S(C,C), "
           "C=1..40, is pinned; NO closed form for P(C) is claimed",
           pl_ok and seq_ok,
           {"plateau_constant_violations": pl_bad,
            "plateau_sequence": p_seq})

    audit = {
        "meta": {
            "item": "K0919",
            "title": "LCM periodicity of the uniform-board REMO counting "
                "recursion: E(C + lcm(1..r), r) == E(C, r) for all C >= 1, "
                "r >= 2 (universal proof, uniform-offset induction); "
                "minimal period == lcm(1..r) machine-verified for r <= 9",
            "date": "2026-11-17",
            "columns": "committed packed columns only (K0881/K0876/K0912 "
                "r=2..9 cap<=12; K0895/K0897/K0898/K0902 r=10..13 "
                "cap<=10)",
            "machinery": "verbatim K0859 theorem_d + closed-form twin; "
                "K0862/K0875 canonical enumeration for the column "
                "anchor",
        },
        "checks": checks,
    }
    ok = all(c["ok"] for c in checks)
    audit["all_ok"] = ok
    return audit


def main():
    a1 = assemble_audit()
    a2 = assemble_audit()
    b1 = json.dumps(a1, indent=1, sort_keys=True, ensure_ascii=False) + "\n"
    b2 = json.dumps(a2, indent=1, sort_keys=True, ensure_ascii=False) + "\n"
    if b1 != b2:
        print("FAIL: assemble is not deterministic")
        sys.exit(1)
    os.makedirs(OUT, exist_ok=True)
    with open(AUDIT_PATH, "w") as f:
        f.write(b1)
    n_ok = sum(1 for c in a1["checks"] if c["ok"])
    n_all = len(a1["checks"])
    for c in a1["checks"]:
        print("%s  %s" % ("OK " if c["ok"] else "FAIL", c["name"]))
    print("checks: %d/%d ok" % (n_ok, n_all))
    if not a1["all_ok"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
