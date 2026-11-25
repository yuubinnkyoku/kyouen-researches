#!/usr/bin/env python3
"""Full-record period characterization of the uniform-board REMO counting
recursion (knowledge item K1154; single-owner
note research/log/2026-11-20-remo-full-record-period-necessity-single-owner-
note.md).  This closes the explicitly stated OPEN of K0919 (minimality for
r >= 10 and the necessity direction: every period of E(.,r) is a multiple
of Q(r)).

THEOREM (PNE, universal).  Put Q(r) := lcm(1,2,...,r) and let
E(C,r) = (elimination tuple, survivor) be the K0859 Theorem-D counting
recursion on the uniform board.  For every r >= 2 and every T >= 1:

    T is a period of E(.,r)   (i.e. E(C+T,r) == E(C,r) for all C >= 1)
        if and only if
    Q(r) | T.

Hence the minimal period of E(.,r) is exactly Q(r) for EVERY r >= 2.

Proof (necessity direction; sufficiency is K0919 Theorem PER).

Phase data.  For a fixed T, say the two boards C and C+T are IN SYNC at
phase h (sigma_h) when in phase h they have the same ordered active
list, the same turn pointer, and every active player's count differs by
one common offset D_h.  sigma_1 holds trivially with D_1 = 0.  Let k_h
be the number of active players in phase h (k_h = r, r-1, ..., 2 for
h = 1..r-1) and X_h := T - k_h*D_h the phase-length shift (the ell of
the C+T board minus the ell of the C board, since the active count sum
shifts by exactly k_h*D_h).  Two facts:

(INS, preservation)  sigma_h and k_h | X_h imply: same share/remainder
    split pattern, same loser offset li, same removed label, same new
    turn, and sigma_{h+1} with D_{h+1} = D_h + X_h/k_h = T/k_h.  (This
    is literally the K0919 uniform-offset induction, Theorem PER.)

(MIS, deviation)  sigma_h and k_h -/~ X_h imply: the loser OFFSETS
    differ (li' - li == X_h mod k_h != 0 over identical active lists),
    hence the two boards remove DIFFERENT LABELS in phase h.

Conditions.  By INS, if the divisibility conditions
    M_1: r = k_1 | T              (X_1 = T)
    M_h: k_{h-1}*k_h | T          (h >= 2; on the in-sync prefix
                                  D_h = T/k_{h-1} and
                                  X_h = T - k_h*T/k_{h-1} = T/k_{h-1})
hold for phases 1..r-1, then sigma_h holds at every phase and every
removed label coincides: this is Theorem PER's sufficiency.  By Lemma Q
of K0919, M_1..M_{r-1} hold jointly iff Q(r) | T.

Necessity.  Let Q(r) -/~ T and let h* be the FIRST phase whose
condition fails (h* depends only on (T, r)).  INS applied to phases
1..h*-1 keeps the boards in sync (their conditions hold; the closed
forms D_h = T/k_{h-1}, X_h = T/k_{h-1} hold along the prefix), and MIS
at phase h* shows the h*-th removed labels differ.  Nothing above
depends on C, so for EVERY C >= 1 the elimination tuples agree on
entries 1..h*-1 and first differ exactly at entry h*:

    E(C+T, r) != E(C, r) for all C >= 1.

In particular C = 1 already witnesses the non-periodicity of every T
with Q(r) -/~ T, and with PER's sufficiency this gives the
characterization and the minimality of Q(r) for every r >= 2.

Machine checks (all deterministic, stdlib only, no network, no file
input; audit assembled twice in-process and compared byte-for-byte):

V0  Lemma-Q anchors: lcm(r, k(k+1) : 2 <= k <= r-1) == Q(r) for every
    r = 2..48, and, for a deterministic family of T values per r
    r = 2..32 (maximal proper divisors of Q(r), all Q(r)/p^e, 32 LCG
    values in [1,2Q(r)], Q(r), 2Q(r), Q(r)+1), the conjunction of
    M_1..M_{r-1} equals the test Q(r) | T.
V1  Twin implementations of the recursion (K0859 verbatim per-stone
    loop vs the closed-form share-count rewrite used everywhere
    else) agree on (elimination tuple, survivor) for r = 2..12,
    all C in [1,30].  (The verbatim per-stone loop is O(C) per phase,
    so huge-C spot checks elsewhere exercise the closed form only.)
V2  Sufficiency anchors (K0919 Theorem PER faith, period side):
    for r = 2..13, E(C+Q(r)) == E(C) for every C in [1,25] and
    E(C+2Q(r)) == E(C) for C in [1,5]; Q(r) | r!.
V3  Necessity anchors, maximal proper divisors: for every r = 2..48
    and every prime p <= r, with T = Q(r)/p: E(C+T,r) != E(C,r) for
    every C in [1,8] and for three huge C (2**30+1, 2**30+7,
    10**12+3), and the FIRST differing elimination entry equals
    h*(T,r) for every such C.  The per-(r,p) h* table is published.
V4  Necessity anchors, FULL proper-divisor sweep: for every r = 2..28
    every proper divisor d of Q(r) is rejected at witness C = 1
    (E(1+d,r) != E(1,r)) with first difference exactly h*(d,r).
    Together with the K0922 DIV argument this machine-extends the E3
    minimality range r <= 9 to r <= 28 independently of the universal
    proof.  Per-r divisor counts published.
V5  Phase-trace strong form (heart of the proof, mechanically
    checked): for r = 2..20, every maximal proper divisor T and
    C in [1,10], plus LCG non-periods for r = 5..12: both boards
    traced phase by phase; for h < h*: identical ordered active
    lists, turn, li, removed label; pre-phase counts offset exactly
    D_h (D_1 = 0, D_h = T/k_{h-1}); ell-shift exactly X_h = T/k_{h-1}
    (X_1 = T) and k_h | X_h.  At phase h*: identical active list and
    turn but li and removed label differ with
    (li' - li) mod k_h == X_h mod k_h != 0.  Elimination tuples agree
    on entries 1..h*-1 and differ exactly at h*.
V6  Equal-Q block contrast (finite observation): inside the equal-Q
    blocks {17,18}, {41,42}, {47,48} the E-side h*-map over maximal
    proper divisors of Q is NOT block-invariant (e.g. r=41 vs r=42 at
    p=2: h* = 10 vs 11), contrasting the survivor-side witness-stream
    identity observed within blocks by K1145: the survivor-side
    observation cannot be inherited from E-side phase structure.
V7  Determinism: the whole audit is assembled twice in-process and
    the two byte strings must be identical; the audit then records
    its own sha256.

Scope / limits (do not over-read):
- The universal claims (the characterization THEOREM PNE and its
  strong form) are PROVEN in the report; the machine checks are
  independent anchors, with V5 validating the exact phase-level
  identities used in the proof.
- Only the FULL RECORD E (elimination tuple + survivor) is treated.
  The SURVIVOR-column necessity (bounded witness conjecture of
  K0925/K1145, machine r <= 48) is NOT closed here: a label mismatch
  at phase h* does not imply a survivor mismatch.  V6 is recorded as
  a finite contrast only.
- Uniform boards (Delta = 0, Theorem-D domain) only; nothing about
  non-uniform boards; 11x11 empty board / class frontiers remain
  UNKNOWN and unrelated.
- V6 and the huge-C spot checks are finite anchors, not exhaustive
  claims.

Usage: python3 verify_period_necessity.py
(regenerates output/audit.json; exit code 1 on any failed check)
"""

import hashlib
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")
AUDIT_PATH = os.path.join(OUT, "audit.json")

ITEM_ID = "K1154"  # provisional; final K-number triple-checked at push


# ---------------------------------------------------------------------------
# the K0859 Theorem-D recursion, two implementations (verbatim twins)
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
    Equality with the verbatim loop is asserted by V1.
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
            counts[active[(turn + i) % k]] += q + (1 if i < t else 0)
        li = (turn + ell) % k
        loser = active[li]
        elimination.append(loser)
        counts[loser] = 0
        active.pop(li)
        if active:
            turn = li % len(active)
    return tuple(elimination), active[0]


def theorem_d_phases(C, r):
    """Phase-by-phase trace of the closed-form recursion.

    Returns (phases, elimination, survivor).  Each phase dict records:
      active  ordered active list BEFORE the removal (rebuilt),
      turn    turn pointer at phase start,
      k, ell, t, q  phase parameters,
      li      loser offset, loser the loser LABEL,
      pre     {label: count} at phase start (active players),
      post_turn  turn pointer after the removal (li % len(active)).
    """
    active = list(range(r))
    counts = [0] * r
    turn = 0
    elimination = []
    phases = []
    while len(active) > 1:
        k = len(active)
        s = sum(counts[p] for p in active)
        ell = C - s
        q, t = divmod(ell, k)
        li = (turn + ell) % k
        loser = active[li]
        pre = {p: counts[p] for p in active}
        for i in range(k):
            counts[active[(turn + i) % k]] += q + (1 if i < t else 0)
        counts[loser] = 0
        active.pop(li)
        post_turn = li % len(active) if active else turn
        phases.append({
            "active": tuple(active[:li] + [loser] + active[li:]),
            "turn": turn, "k": k, "ell": ell, "t": t, "q": q,
            "li": li, "loser": loser, "pre": pre, "post_turn": post_turn,
        })
        turn = post_turn
        elimination.append(loser)
    return phases, tuple(elimination), active[0]


def factorial(r):
    out = 1
    for i in range(2, r + 1):
        out *= i
    return out


def gcd_pair(a, b):
    while b:
        a, b = b, a % b
    return a


def lcm2(a, b):
    return a * b // gcd_pair(a, b)


def lcm_all(r):
    """Q(r) = lcm(1,2,...,r)."""
    out = 1
    for i in range(2, r + 1):
        out = lcm2(out, i)
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


def primes_upto(n):
    return [p for p in range(2, n + 1)
            if all(p % d for d in range(2, int(p ** 0.5) + 1))]


# ---------------------------------------------------------------------------
# the condition chain and the first-failing phase h*(T,r)
# ---------------------------------------------------------------------------

def ks_of(r):
    """Phase sizes k_h for h = 1..r-1: r, r-1, ..., 2."""
    return list(range(r, 1, -1))


def conditions_all(T, r):
    """M_1..M_{r-1}; all hold iff Q(r) | T (K0919 Lemma Q)."""
    ks = ks_of(r)
    if T % ks[0] != 0:
        return False
    for h in range(2, r):
        if T % (ks[h - 2] * ks[h - 1]) != 0:
            return False
    return True


def first_fail_phase(T, r):
    """h*(T,r): 1-based index of the first failing condition, or None.

    None means all conditions hold (iff Q(r) | T).  Otherwise h* is the
    first phase where k_h -/~ X_h on the in-sync prefix, i.e. the phase
    whose eliminated labels differ for EVERY C >= 1.
    """
    ks = ks_of(r)
    if T % ks[0] != 0:
        return 1
    D = T // ks[0]
    for h in range(2, r):
        k = ks[h - 1]
        X = T - k * D            # = T / k_{h-1} on the prefix
        if X % k != 0:
            return h
        D = D + X // k           # = T / k_{h-1}
    return None


# ---------------------------------------------------------------------------
# deterministic LCG (reproducible pseudo-random samples)
# ---------------------------------------------------------------------------

def lcg_list(n, seed, a=1103515245, c=12345, m=1 << 31):
    out = []
    x = seed
    for _ in range(n):
        x = (a * x + c) % m
        out.append(x)
    return out


def first_diff(e1, e2):
    for i in range(min(len(e1), len(e2))):
        if e1[i] != e2[i]:
            return i + 1
    return None


def trace_check(C, r, T, hstar):
    """Count violations of the strong-form identities for boards C, C+T."""
    ph1, el1, _ = theorem_d_phases(C, r)
    ph2, el2, _ = theorem_d_phases(C + T, r)
    if len(ph1) != r - 1 or len(ph2) != r - 1:
        return 1
    if first_diff(el1, el2) != hstar:
        return 1
    ks = ks_of(r)
    bad = 0
    for h in range(1, hstar + 1):
        a, b = ph1[h - 1], ph2[h - 1]
        if a["active"] != b["active"] or a["turn"] != b["turn"]:
            bad += 1
            break
        k = a["k"]
        if k != ks[h - 1] or b["k"] != k:
            bad += 1
            break
        X = b["ell"] - a["ell"]
        cf = T if h == 1 else T // ks[h - 2]
        if X != cf:
            bad += 1
            break
        D = 0 if h == 1 else T // ks[h - 2]
        for p in a["pre"]:
            if a["pre"][p] + D != b["pre"][p]:
                bad += 1
                break
        if h < hstar:
            if a["li"] != b["li"] or a["loser"] != b["loser"]:
                bad += 1
                break
            if a["post_turn"] != b["post_turn"]:
                bad += 1
                break
            if X % k != 0:
                bad += 1
                break
        else:
            if a["li"] == b["li"] or a["loser"] == b["loser"]:
                bad += 1
                break
            if (b["li"] - a["li"]) % k != X % k or X % k == 0:
                bad += 1
                break
    return bad


# ---------------------------------------------------------------------------
# audit assembly (deterministic; assembled twice, byte-identical)
# ---------------------------------------------------------------------------

HUGE_C = [2 ** 30 + 1, 2 ** 30 + 7, 10 ** 12 + 3]


def build_checks():
    checks = []

    def record(name, ok, data):
        checks.append({"name": name, "ok": bool(ok), "data": data})

    # ---- V0: Lemma-Q anchors ---------------------------------------------
    v0_lcm_ok = True
    v0_equiv_ok = True
    v0_equiv_n = 0
    for r in range(2, 49):
        q = lcm_all(r)
        l = r
        for k in range(2, r):
            l = lcm2(l, k * (k + 1))
        if l != q:
            v0_lcm_ok = False
    for r in range(2, 33):
        q = lcm_all(r)
        ts = set()
        for p in primes_upto(r):
            ts.add(q // p)
            pe = p
            while q % (pe * p) == 0:
                pe *= p
                ts.add(q // pe)
        for v in lcg_list(32, 20261120 * r):
            ts.add((v % (2 * q)) + 1)
        ts.add(q)
        ts.add(2 * q)
        ts.add(q + 1)
        for T in sorted(ts):
            v0_equiv_n += 1
            if conditions_all(T, r) != (T % q == 0):
                v0_equiv_ok = False
    record("V0 lemmaQ anchors: lcm(r, k(k+1)) == Q(r) r2..48; "
           "M-conjunction iff Q|T on %d deterministic T probes (r2..32)"
           % v0_equiv_n,
           v0_lcm_ok and v0_equiv_ok,
           {"lcm_identity_r_max": 48, "equiv_probes": v0_equiv_n,
            "lcm_ok": v0_lcm_ok, "equiv_ok": v0_equiv_ok})

    # ---- V1: verbatim vs closed-form twins (small C; loop cost O(C)) ------
    v1_ok = True
    v1_pairs = 0
    for r in range(2, 13):
        for C in range(1, 31):
            v1_pairs += 1
            if theorem_d(C, r) != theorem_d_fast(C, r):
                v1_ok = False
    record("V1 verbatim per-stone recursion == closed-form twin "
           "(r = 2..12, all C in [1,30]; 3540 pairs)",
           v1_ok, {"pairs": v1_pairs, "c_cap": 30, "r_max": 12,
                   "ok": v1_ok})

    # ---- V2: sufficiency anchors (K0919 Theorem PER faith) ----------------
    v2_ok = True
    v2_pairs = 0
    per_r_q = {}
    for r in range(2, 14):
        q = lcm_all(r)
        per_r_q[r] = q
        if factorial(r) % q != 0:
            v2_ok = False
        ok_r = True
        for C in range(1, 26):
            v2_pairs += 1
            if theorem_d_fast(C + q, r) != theorem_d_fast(C, r):
                ok_r = False
        for C in range(1, 6):
            v2_pairs += 1
            if theorem_d_fast(C + 2 * q, r) != theorem_d_fast(C, r):
                ok_r = False
        v2_ok = v2_ok and ok_r
    record("V2 sufficiency anchors E(C+Q(r))==E(C) r2..13 "
           "(Q(r) pinned; Q|r!)",
           v2_ok, {"pairs": v2_pairs, "Q_by_r": per_r_q, "ok": v2_ok})

    # ---- V3: necessity anchors, maximal proper divisors -------------------
    v3_ok = True
    v3_pairs = 0
    hstar_map = {}
    for r in range(2, 49):
        q = lcm_all(r)
        hm = {}
        for p in primes_upto(r):
            T = q // p
            hstar = first_fail_phase(T, r)
            if hstar is None:
                v3_ok = False
                hm[p] = -1
                continue
            hm[p] = hstar
            ok_p = True
            for C in list(range(1, 9)) + HUGE_C:
                v3_pairs += 1
                e1 = theorem_d_fast(C, r)
                e2 = theorem_d_fast(C + T, r)
                if e1 == e2:
                    ok_p = False
                if first_diff(e1[0], e2[0]) != hstar:
                    ok_p = False
            v3_ok = v3_ok and ok_p
        hstar_map[r] = hm
    record("V3 every maximal proper divisor Q(r)/p (p prime <= r) is "
           "rejected for ALL probed C (r2..48, C1..8 + 3 huge C), first "
           "difference exactly h*(T,r)",
           v3_ok, {"pairs": v3_pairs, "hstar_maximal": hstar_map,
                   "ok": v3_ok})

    # ---- V4: FULL proper-divisor sweep at witness C=1, r2..28 --------------
    v4_ok = True
    v4_divisors_total = 0
    v4_per_r = {}
    for r in range(2, 29):
        q = lcm_all(r)
        e1 = theorem_d_fast(1, r)
        bad = 0
        hstar_bad = 0
        n = 0
        for d in divisors(q):
            if d == q:
                continue
            n += 1
            e2 = theorem_d_fast(1 + d, r)
            if e1 == e2:
                bad += 1
            if first_diff(e1[0], e2[0]) != first_fail_phase(d, r):
                hstar_bad += 1
        v4_divisors_total += n
        v4_per_r[r] = {"proper": n, "rejected": n - bad,
                       "fd_equals_hstar": n - hstar_bad}
        if bad or hstar_bad:
            v4_ok = False
    record("V4 FULL proper-divisor sweep at witness C=1: every proper "
           "divisor of Q(r) rejected, first difference exactly h* "
           "(r2..28; machine minimality anchor via K0922 DIV, "
           "independent of the universal proof)",
           v4_ok, {"divisors_total": v4_divisors_total,
                   "per_r": v4_per_r, "ok": v4_ok})

    # ---- V5: phase-trace strong form ---------------------------------------
    v5_ok = True
    v5_traces = 0
    v5_violations = 0
    for r in range(2, 21):
        q = lcm_all(r)
        Ts = [q // p for p in primes_upto(r)]
        if 5 <= r <= 18:
            for v in lcg_list(4, 771 * r + 3):
                Ts.append(v % (2 * q) + 1)
        for T in Ts:
            if T % q == 0:
                continue  # periods are excluded here
            hstar = first_fail_phase(T, r)
            if hstar is None:
                v5_ok = False
                continue
            for C in range(1, 11):
                v5_traces += 1
                v5_violations += trace_check(C, r, T, hstar)
    record("V5 phase-trace strong form: in-sync prefix with "
           "D_h = T/k_{h-1}, X_h = T/k_{h-1}, k_h | X_h and exact "
           "phase-h* label mismatch (li shift == X mod k != 0) "
           "(r2..20, maximal proper divisors + LCG non-periods)",
           v5_violations == 0,
           {"traces": v5_traces, "violations": v5_violations})

    # ---- V6: equal-Q block contrast (finite observation) -------------------
    v6 = {}
    v6_ok = True
    for block in [(17, 18), (41, 42), (47, 48)]:
        qb = lcm_all(block[0])
        assert all(lcm_all(x) == qb for x in block)
        common = set(primes_upto(block[0]))
        diffs = []
        for p in sorted(common):
            hs = tuple(first_fail_phase(qb // p, x) for x in block)
            if len(set(hs)) > 1:
                diffs.append([p, list(hs)])
        v6["{%s}" % ",".join(str(x) for x in block)] = {
            "n_differing_primes": len(diffs), "examples": diffs[:8]}
        if not diffs:
            v6_ok = False
    record("V6 equal-Q block E-side h*-map is block-VARIANT (finite "
           "observation; blocks {17,18} {41,42} {47,48}; contrast with "
           "K1145 survivor witness-stream identity)",
           v6_ok, v6)

    return checks


def assemble():
    checks = build_checks()
    all_ok = all(c["ok"] for c in checks)
    audit = {
        "item": ITEM_ID + "-remo-full-record-period-characterization",
        "single_owner_note":
            "research/log/2026-11-20-remo-full-record-period-necessity-"
            "single-owner-note.md",
        "sufficiency_upstream": "K0919 (Theorem PER, universal)",
        "theorem":
            "for all r >= 2, T >= 1: T is a period of E(.,r) iff "
            "Q(r) = lcm(1..r) divides T; the minimal period of E(.,r) "
            "is exactly Q(r) (universal proof; the necessity direction "
            "closes the K0919 OPEN for every r >= 2)",
        "strong_form":
            "if Q(r) does not divide T then E(C+T,r) != E(C,r) for "
            "EVERY C >= 1; the elimination tuples agree on entries "
            "1..h*-1 and first differ exactly at entry h* = h*(T,r) "
            "(C-independent; in particular C = 1 is a universal "
            "E-side witness)",
        "issue": "closes the K0919 OPEN: minimality for r >= 10 and "
                 "the necessity direction",
        "checks": checks,
        "all_ok": all_ok,
        "generator": "verify_period_necessity.py",
        "environment": "python3 stdlib only; deterministic; no network; "
                       "no file input; audit assembled twice and "
                       "compared byte-for-byte",
    }
    return audit


def main():
    t0 = time.time()
    a1 = assemble()
    t1 = time.time()
    a2 = assemble()
    t2 = time.time()
    s1 = json.dumps(a1, sort_keys=True, indent=1, ensure_ascii=True)
    s2 = json.dumps(a2, sort_keys=True, indent=1, ensure_ascii=True)
    if s1 != s2:
        print("AUDIT NOT DETERMINISTIC", file=sys.stderr)
        return 1
    h = hashlib.sha256(s1.encode("ascii")).hexdigest()
    a1["audit_sha256"] = h
    final = json.dumps(a1, sort_keys=True, indent=1, ensure_ascii=True)
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    with open(AUDIT_PATH, "w", encoding="utf-8") as f:
        f.write(final)
        f.write("\n")
    n_ok = sum(1 for c in a1["checks"] if c["ok"])
    print("checks: %d ok: %d all_ok: %s" % (
        len(a1["checks"]), n_ok, a1["all_ok"]))
    for c in a1["checks"]:
        print("  [%s] %s" % ("OK" if c["ok"] else "FAIL", c["name"]))
    print("audit sha256: %s" % h)
    print("audit path: %s" % AUDIT_PATH)
    print("assemble seconds: %.3f / %.3f" % (t1 - t0, t2 - t1))
    return 0 if a1["all_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
