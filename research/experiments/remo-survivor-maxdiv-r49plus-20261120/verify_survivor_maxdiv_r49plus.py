#!/usr/bin/env python3
"""Maximal-proper-divisor (maxdiv) reduction for the SURVIVOR-column
minimal period of the K0859 Theorem-D uniform-board counting recursion
E(C,r), plus the r = 49..150 machine extension at maxdiv granularity
(fast lane, follows K0925 THEOREM S32 and K1145 THEOREM S48).

LEMMA RED (universal, proved in report.md as a corollary of the
K0922 LEMMA DIV): for every r >= 2, the survivor column
C -> S(C,r) = survivor(E(C,r)) has minimal period exactly Q(r) =
lcm(1..r) IF AND ONLY IF for every prime p <= r the maximal proper
divisor Q(r)/p is rejected by some witness C (S(C+Q/p,r) != S(C,r)).
The full proper-divisor sweep of K0925/K1145 (1,548,272 divisors at
r = 48) collapses to pi(r) <= 35 checks.

Positive direction is K0925 THEOREM W+ (universal, every C >= 1),
necessity direction via LEMMA DIV + LEMMA RED.  The published
full-sweep conclusion (survivor minimal period = Q(r), r = 2..48)
is therefore EXTENDED to r = 2..150 machine-wise, with the maxdiv
fragment observed to hold with witness <= r-1 on every swept pair
(the K0926 window form).

Machine checks (deterministic, stdlib only, no network, no clock in
the audit, per-r checkpoints in output/ck/, --no-cache forces full
recomputation, audit assembled twice per invocation and compared
byte-for-byte):

C0    maxdiv-covering anchor: for r = 2..36, every proper divisor
      d of Q(r) (factorization-enumerated) divides at least one
      maximal proper divisor Q(r)/p (p prime <= r).  Machine anchor
      of the one-line covering argument in LEMMA RED's proof.
C1    brute-force equivalence anchor: for r = 2..24 the K0925 W5
      full-divisor minimal-witness sweep (independent
      reimplementation, window [1,150] fallback [151,1500]) and the
      maxdiv-only sweep agree on the per-r "every proper divisor
      rejected" verdict; the maxdiv subset witnesses match the full
      sweep exactly.
C2    TWIN anchor at the new range: verbatim per-stone K0859
      recursion == closed-form twin (full (elim, survivor) pair)
      == survivor_fast, r grid in [49,150], C in [1,60]
      (900 pairs; trust boundary as in K1145 S4).
C3    published-value pins (r = 2..48): (a) the maxdiv table
      reproduces the K0922 audit M5 [w_elim,w_sv] values for
      d = Q/p, r = 10..16 (as transcribed in the K0925 verifier);
      (b) the per-r maxdiv witness maximum is <= the published
      full-divisor maximum everywhere (K0925 audit r = 2..32,
      K1145 r = 33..48), with equality except r in
      {19,20,21,22,27,28} where the published maximum sits at a
      NON-maximal divisor (machine-recorded exception list).
C4    the main sweep: for r = 49..150 and every prime p <= r, the
      maximal proper divisor Q(r)/p is rejected by a witness C
      (ascending from C=1, window [1,150], fallback [151,1500],
      fail-closed if none).  Per-r aggregates (max, argmax prime,
      h*(Q/p,r) closed form, h*-class, histogram) and the compact
      per-(r,p) witness table (sha256-pinned inside the audit,
      published as output/maxdiv_witness_table.txt).  Witness
      <= r-1 checked on every pair.  Conclusion via W+ and
      DIV+RED: survivor minimal period = Q(r), r = 2..150.
C5    positive period anchors at the new range: S(C+Q(r),r) ==
      S(C,r) for ten r in [49,150], C in [1,50] plus anchors
      {Q-1, Q+1, Q+5, 2Q-1} (machine anchor; the universal proof
      is K0925 W+ / K1154).
C6    equal-Q block minimal-witness-map identity r = 2..150:
      inside every equal-Q block the (p -> minimal witness) map is
      identical across the block (K1145 observation extended to
      maxdiv granularity and r <= 150); adjacent-block control
      pairs have differing maps.
C7    reject-vector non-identity (observation, negative): for
      same-block groups {17,18}, {37,38,39,40}, {89,90}, {113,120}
      the FULL reject vectors (C in [1,60]) of different r in the
      group DIFFER for some primes (the K1145 identity is exactly
      at the minimal-witness level), while their minimal witnesses
      agree.

Trust boundary: all witness comparisons at huge C rest on the
published closed-form survivor_fast (pinned to the verbatim
per-stone recursion at small C by TWIN here and by the K0925/K1145
TWIN checks), on the positive/necessity reduction (K0919 PER,
K0925 W+, K0922 DIV, LEMMA RED proved in report.md), and on the
machine sweeps here.  The SURVIVOR-side universal necessity
(bounded-witness conjecture for ALL r) stays OPEN.
"""

import hashlib
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")
CK = os.path.join(OUT, "ck")

R_MIN = 2
R_MAX = 150
R_COV = 36            # C0 range
R_BRUTE = 24         # C1 range
TWIN_GRID = [49, 55, 60, 67, 74, 81, 89, 97, 104, 113, 120,
             128, 135, 143, 150]
TWIN_CMAX = 60
POS_GRID = [49, 60, 72, 84, 96, 108, 120, 132, 144, 150]
POS_CMAX = 50
SURV_WINDOW = 150
SURV_FALLBACK = 1500
W_VEC = 60           # C7 reject-vector window

# ---------------------------------------------------------------------------
# the K0859 Theorem-D recursion: verbatim, closed-form twin, survivor-only
# (verbatim copies of the K0922/K0925 verifier implementations)
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
    """Closed-form share-count rewrite of the same recursion."""
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


def survivor_fast(C, r):
    """Survivor only (same dynamics as theorem_d_fast)."""
    active = list(range(r))
    counts = [0] * r
    turn = 0
    while len(active) > 1:
        k = len(active)
        s = sum(counts[p] for p in active)
        ell = C - s
        q, t = divmod(ell, k)
        for i in range(k):
            pos = active[(turn + i) % k]
            counts[pos] += q + (1 if i < t else 0)
        li = (turn + ell) % k
        counts[active[li]] = 0
        active.pop(li)
        if active:
            turn = li % len(active)
    return active[0]

# ---------------------------------------------------------------------------
# arithmetic (verbatim K0925 helpers where applicable)
# ---------------------------------------------------------------------------

def sha256_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def lcm_all(r):
    out = 1
    for i in range(2, r + 1):
        a, b = out, i
        while b:
            a, b = b, a % b
        out = out * i // a
    return out


def primes_upto(r):
    """Sieve of Eratosthenes, deterministic."""
    sieve = [True] * (r + 1)
    out = []
    for i in range(2, r + 1):
        if sieve[i]:
            out.append(i)
            for j in range(i * i, r + 1, i):
                sieve[j] = False
    return out


def v_p(n, p):
    out = 0
    while n % p == 0:
        n //= p
        out += 1
    return out


def hstar_qp(Q, p, r):
    """Closed form of h*(Q/p) (verbatim K0925 W6): 1 if
    v_p(r) == v_p(Q) (M_1 fails), else r+1 - max{k <= r-1 :
    v_p(k(k+1)) == v_p(Q)}."""
    vq = v_p(Q, p)
    if v_p(r, p) == vq:
        return 1
    best = None
    for k in range(2, r):
        if v_p(k * (k + 1), p) == vq:
            best = k
    return None if best is None else r + 1 - best


def q_factorization(r):
    """Q(r) = prod p^e_p with e_p = max{a : p^a <= r}."""
    fac = {}
    for p in primes_upto(r):
        e = 0
        pk = p
        while pk <= r:
            e += 1
            pk *= p
        fac[p] = e
    return fac


def divisors_from_factorization(fac):
    out = [1]
    for p, e in sorted(fac.items()):
        pk = 1
        nxt = []
        for a in range(e + 1):
            nxt.extend(d * pk for d in out)
            pk *= p
        out = nxt
    return sorted(out)


# ---------------------------------------------------------------------------
# sweeps and checkpoints
# ---------------------------------------------------------------------------

def witness_for(d, r):
    """Minimal witness C for the survivor-column comparand d
    (ascending, window [1,SURV_WINDOW] then fallback); None if
    unwitnessed (fail-closed upstream)."""
    for C in range(1, SURV_WINDOW + 1):
        if survivor_fast(C, r) != survivor_fast(C + d, r):
            return C
    for C in range(SURV_WINDOW + 1, SURV_FALLBACK + 1):
        if survivor_fast(C, r) != survivor_fast(C + d, r):
            return C
    return None


def ck_path(name):
    return os.path.join(CK, "%s.json" % name)


def load_ck(name):
    p = ck_path(name)
    if os.path.exists(p):
        with open(p) as f:
            return json.load(f)
    return None


def save_ck(name, obj):
    os.makedirs(CK, exist_ok=True)
    with open(ck_path(name), "w") as f:
        json.dump(obj, f, indent=1, sort_keys=True)
    return obj


_ROW_MEMO = {}


def sweep_row(r, no_cache):
    """Per-r maxdiv sweep row: primes, minimal witnesses, hstar
    (verbatim K0925 W6 closed form), h*-class (1 if v_p(r) ==
    v_p(Q(r)) i.e. M_1 fails, else 2).  Memoized per invocation;
    `no_cache` ignores the on-disk checkpoint on first touch and
    recomputes (the memo still dedupes in-process consumers)."""
    if r in _ROW_MEMO:
        return _ROW_MEMO[r]
    ck = load_ck("sw_r%d" % r)
    if ck is not None and not no_cache:
        _ROW_MEMO[r] = ck
        return ck
    Q = lcm_all(r)
    ps = primes_upto(r)
    w = []
    hs = []
    hc = []
    for p in ps:
        w.append(witness_for(Q // p, r))
        hs.append(hstar_qp(Q, p, r))
        hc.append(1 if v_p(r, p) == v_p(Q, p) else 2)
    row = {"r": r, "Q": str(Q), "primes": ps, "w": w, "hstar": hs,
           "hclass": hc, "unwitnessed": sum(1 for x in w if x is None)}
    save_ck("sw_r%d" % r, row)
    _ROW_MEMO[r] = row
    return row


def build_table(no_cache):
    """The compact per-(r,p) witness table for r = 2..150
    (deterministic; sha256 pinned inside the audit; published as
    output/maxdiv_witness_table.txt)."""
    lines = ["# witness per prime p (ascending = primes_upto(r)): "
             "minimal C rejecting Q(r)/p, window [1,150] then "
             "[151,1500], fail-closed"]
    for r in range(R_MIN, R_MAX + 1):
        row = sweep_row(r, no_cache)
        lines.append("r=%d %s" % (r, " ".join(str(x) for x in row["w"])))
    return "\n".join(lines) + "\n"


def maxdiv_sweep(r):
    """Per-prime minimal witnesses for the maximal proper divisors
    Q(r)/p of one r; returns dict p -> witness (None = unwitnessed).
    Used by C1 as an independent second code path (no sw_* rows)."""
    Q = lcm_all(r)
    out = {}
    for p in primes_upto(r):
        out[p] = witness_for(Q // p, r)
    return out


# ---------------------------------------------------------------------------
# checks
# ---------------------------------------------------------------------------

def compute_c0(no_cache):
    ck = load_ck("c0")
    if ck is not None and not no_cache:
        return ck
    data = {}
    ok = True
    total = 0
    for r in range(R_MIN, R_COV + 1):
        Q = lcm_all(r)
        fac = q_factorization(r)
        proper = divisors_from_factorization(fac)[:-1]  # excludes Q
        maxdivs = [Q // p for p in primes_upto(r)]
        bad = 0
        for d in proper:
            if not any(m % d == 0 for m in maxdivs):
                bad += 1
        data["r%d" % r] = {"proper": len(proper),
                           "maxdiv": len(maxdivs), "uncovered": bad}
        total += len(proper)
        if bad:
            ok = False
    data["total_proper"] = total
    data["ok"] = ok
    return save_ck("c0", data)


def compute_c1(no_cache):
    ck = load_ck("c1")
    if ck is not None and not no_cache:
        return ck
    data = {}
    ok = True
    for r in range(R_MIN, R_BRUTE + 1):
        Q = lcm_all(r)
        fac = q_factorization(r)
        proper = divisors_from_factorization(fac)[:-1]
        unwit_full = 0
        wit_max_full = 0
        maxdiv_wit = {}
        for d in proper:
            w = witness_for(d, r)
            if w is None:
                unwit_full += 1
            else:
                wit_max_full = max(wit_max_full, w)
            if Q % d == 0 and (Q // d) in primes_upto(r):
                maxdiv_wit[Q // d] = w
        md = maxdiv_sweep(r)   # independent code path
        unwit_md = sum(1 for w in md.values() if w is None)
        match = all(maxdiv_wit[p] == md[p] for p in md)
        verdict_full = (unwit_full == 0)
        verdict_md = (unwit_md == 0)
        data["r%d" % r] = {"proper": len(proper),
                            "unwit_full": unwit_full,
                            "unwit_maxdiv": unwit_md,
                            "wit_max_full": wit_max_full,
                            "wit_max_maxdiv": max([w for w in md.values()
                                                   if w is not None]),
                            "maxdiv_subset_match": match,
                            "verdicts_agree": verdict_full == verdict_md}
        if not (match and verdict_full == verdict_md and verdict_md):
            ok = False
    data["ok"] = ok
    return save_ck("c1", data)


def compute_c2(no_cache):
    ck = load_ck("c2")
    if ck is not None and not no_cache:
        return ck
    pairs = 0
    mism = 0
    per_r = {}
    for r in TWIN_GRID:
        bad = 0
        for C in range(1, TWIN_CMAX + 1):
            e1, s1 = theorem_d(C, r)
            e2, s2 = theorem_d_fast(C, r)
            s3 = survivor_fast(C, r)
            pairs += 1
            if e1 != e2 or s1 != s2 or s1 != s3:
                bad += 1
                mism += 1
        per_r["r%d" % r] = {"pairs": TWIN_CMAX, "mismatch": bad}
    data = {"grid": TWIN_GRID, "cmax": TWIN_CMAX, "pairs": pairs,
            "mismatch": mism, "per_r": per_r,
            "ok": mism == 0}
    return save_ck("c2", data)


# published pins ------------------------------------------------------------

# K0922 audit M5 [w_elim, w_sv] for d = Q/p (transcribed in the K0925
# verifier as K0922_QP); w_elim = 1 is universal (K0925 W+).
K0922_QP_SV = {
    10: {1260: 4, 360: 4, 504: 1, 840: 6},
    11: {13860: 4, 2520: 10, 3960: 2, 5544: 1, 9240: 3},
    12: {13860: 4, 2520: 10, 3960: 2, 5544: 1, 9240: 3},
    13: {120120: 3, 180180: 4, 27720: 9, 32760: 9, 51480: 5, 72072: 3},
    14: {120120: 3, 180180: 4, 27720: 9, 32760: 9, 51480: 5, 72072: 3},
    15: {120120: 3, 180180: 4, 27720: 9, 32760: 9, 51480: 5, 72072: 3},
    16: {102960: 3, 144144: 1, 240240: 6, 360360: 8, 55440: 5, 65520: 7},
}

# Per-r published survivor witness maxima over ALL proper divisors:
# K0925 (r = 2..32, audit remo_uniform_witness_theorem_audit.json, W5)
# and K1145 (r = 33..48, report table).
PUBLISHED_WIT_MAX = {2: 1, 3: 1, 4: 2, 5: 3, 6: 3, 7: 3, 8: 6, 9: 6,
                     10: 6, 11: 10, 12: 10, 13: 9, 14: 9, 15: 9, 16: 8,
                     17: 12, 18: 12, 19: 9, 20: 9, 21: 9, 22: 9,
                     23: 8, 24: 8, 25: 20, 26: 20, 27: 18, 28: 18,
                     29: 28, 30: 28, 31: 27, 32: 25,
                     33: 25, 34: 25, 35: 25, 36: 25, 37: 35, 38: 35,
                     39: 35, 40: 35, 41: 29, 42: 29, 43: 30, 44: 30,
                     45: 30, 46: 30, 47: 39, 48: 39}

# r where the published full-divisor maximum strictly exceeds the
# maxdiv maximum (machine-recorded exceptions, discovered here).
PIN_EXCEPTIONS = [19, 20, 21, 22, 27, 28]

R_PIN_LO = 2
R_PIN_HI = 48


def compute_c3(no_cache):
    ck = load_ck("c3")
    if ck is not None and not no_cache:
        return ck
    data = {"qp_pins": {}, "wit_max_cmp": {}}
    ok = True
    for r in range(R_PIN_LO, R_PIN_HI + 1):
        row = sweep_row(r, no_cache)
        wdict = dict(zip(row["primes"], row["w"]))
        wit_max_md = max(row["w"])
        pub = PUBLISHED_WIT_MAX[r]
        if wit_max_md > pub:
            ok = False
        equal = (wit_max_md == pub)
        expect_equal = r not in PIN_EXCEPTIONS
        if equal != expect_equal:
            ok = False
        data["wit_max_cmp"]["r%d" % r] = {
            "maxdiv": wit_max_md, "published": pub, "equal": equal}
        if r in K0922_QP_SV:
            Q = lcm_all(r)
            qpok = True
            for d, w_sv in K0922_QP_SV[r].items():
                p = Q // d
                w_elim = 1 if (theorem_d_fast(1, r)[0]
                               != theorem_d_fast(1 + d, r)[0]) else None
                if wdict[p] != w_sv or w_elim != 1:
                    qpok = False
            data["qp_pins"]["r%d" % r] = qpok
            if not qpok:
                ok = False
    data["ok"] = ok
    return save_ck("c3", data)


def compute_c4(no_cache):
    ck = load_ck("c4")
    if ck is not None and not no_cache:
        return ck
    per_r = {}
    ok = True
    wit_leq = 0
    pairs = 0
    hist = {}
    for r in range(49, R_MAX + 1):
        row = sweep_row(r, no_cache)
        pairs += len(row["primes"])
        unwit = row["unwitnessed"]
        if unwit:
            ok = False
        rmax = None
        argmax_p = None
        argmax_hs = None
        argmax_hc = None
        for p, w, hs, hc in zip(row["primes"], row["w"],
                                row["hstar"], row["hclass"]):
            if w is None:
                continue
            hist[w] = hist.get(w, 0) + 1
            if w > r - 1:
                ok = False
            else:
                wit_leq += 1
            if rmax is None or w > rmax:
                rmax = w
                argmax_p = p
                argmax_hs = hs
                argmax_hc = hc
        per_r["r%d" % r] = {
            "Q": row["Q"], "pairs": len(row["primes"]),
            "unwitnessed": unwit, "wit_max": rmax,
            "wit_argmax_p": argmax_p,
            "wit_argmax_hstar": argmax_hs,
            "wit_argmax_hclass": argmax_hc}
    unw = sum(v["unwitnessed"] for v in per_r.values())
    data = {"r_range": [49, R_MAX], "pairs": pairs,
            "wit_leq_r_minus_1": wit_leq, "unwitnessed": unw,
            "per_r": per_r,
            "hist": {str(k): v for k, v in sorted(hist.items())},
            "ok": ok}
    return save_ck("c4", data)


def compute_c5(no_cache):
    ck = load_ck("c5")
    if ck is not None and not no_cache:
        return ck
    per_r = {}
    comps = 0
    bad = 0
    for r in POS_GRID:
        Q = lcm_all(r)
        cs = list(range(1, POS_CMAX + 1)) + [Q - 1, Q + 1, Q + 5, 2 * Q - 1]
        b = 0
        for C in cs:
            comps += 1
            if survivor_fast(C, r) != survivor_fast(C + Q, r):
                b += 1
                bad += 1
        per_r["r%d" % r] = {"comparisons": len(cs), "bad": b}
    data = {"grid": POS_GRID, "cmax": POS_CMAX, "comparisons": comps,
            "bad": bad, "per_r": per_r, "ok": bad == 0}
    return save_ck("c5", data)


def equal_q_blocks(rmax):
    blocks = []
    cur = [R_MIN]
    curQ = lcm_all(R_MIN)
    for r in range(R_MIN + 1, rmax + 1):
        Q = lcm_all(r)
        if Q == curQ:
            cur.append(r)
        else:
            blocks.append(cur)
            cur = [r]
            curQ = Q
    blocks.append(cur)
    return blocks


def compute_c6(no_cache):
    ck = load_ck("c6")
    if ck is not None and not no_cache:
        return ck
    rows = {r: sweep_row(r, no_cache) for r in range(R_MIN, R_MAX + 1)}
    blocks = equal_q_blocks(R_MAX)
    info = []
    ok = True
    for blk in blocks:
        if len(blk) < 2:
            continue
        ref = rows[blk[0]]
        same = True
        for r in blk[1:]:
            o = rows[r]
            if o["primes"] != ref["primes"] or o["w"] != ref["w"]:
                same = False
        ok = ok and same
        info.append({"block": blk, "identical_map": same,
                     "shared_primes": len(ref["primes"])})
    ctrl = []
    for i in range(len(blocks) - 1):
        a, b = blocks[i][-1], blocks[i + 1][0]
        ra, rb = rows[a], rows[b]
        differ = (ra["primes"] != rb["primes"]) or (ra["w"] != rb["w"])
        if not differ:
            ok = False
        ctrl.append({"pair": [a, b], "differ": differ})
    data = {"blocks_multi": info, "controls": ctrl,
            "n_blocks": len(blocks),
            "n_blocks_multi": len(info), "ok": ok}
    return save_ck("c6", data)


C7_PAIRS = [(17, 18), (37, 38, 39, 40), (89, 90), (113, 120)]


def compute_c7(no_cache):
    ck = load_ck("c7")
    if ck is not None and not no_cache:
        return ck
    res = []
    for grp in C7_PAIRS:
        a = grp[0]
        Q = lcm_all(a)
        ps = sorted(primes_upto(grp[-1]))
        diffs = []
        agree_wit = True
        for p in ps:
            T = Q // p
            vecs = {}
            for r in grp:
                vecs[r] = tuple(
                    1 if survivor_fast(C + T, r) != survivor_fast(C, r)
                    else 0 for C in range(1, W_VEC + 1))
            ref = vecs[grp[0]]
            mindiff = None
            for r in grp[1:]:
                if vecs[r] != ref and mindiff is None:
                    for C in range(1, W_VEC + 1):
                        if vecs[r][C - 1] != ref[C - 1]:
                            mindiff = C
                            break
            if mindiff is not None:
                diffs.append({"p": p, "first_vector_diff_C": mindiff})
            row = sweep_row(a, no_cache)
            pidx = row["primes"].index(p)
            ws = [sweep_row(r, no_cache)
                  ["w"][row["primes"].index(p)] for r in grp]
            if len(set(ws)) != 1:
                agree_wit = False
        res.append({"group": grp, "vector_diffs": diffs,
                    "minimal_witnesses_agree": agree_wit,
                    "n_vector_diff_primes": len(diffs)})
    data = {"groups": res,
            "ok": all(g["minimal_witnesses_agree"] for g in res)}
    return save_ck("c7", data)


# ---------------------------------------------------------------------------
# audit assembly (twice per invocation, byte-identical)
# ---------------------------------------------------------------------------

CHECKS = [
    ("C0", "maxdiv-covering anchor r=2..36: every proper divisor of "
           "Q(r) divides some maximal proper divisor Q(r)/p",
     compute_c0),
    ("C1", "brute-force equivalence r=2..24: K0925-W5-style full-divisor "
           "sweep vs maxdiv-only sweep verdicts and witnesses agree",
     compute_c1),
    ("C2", "TWIN anchor: verbatim per-stone K0859 recursion == "
           "closed-form twin == survivor_fast, r grid in [49,150], "
           "C in [1,60]",
     compute_c2),
    ("C3", "published-value pins: K0922 [w_elim,w_sv] d=Q/p table "
           "(r=10..16) and K0925/K1145 per-r witness maxima (r=2..48)",
     compute_c3),
    ("C4", "maxdiv sweep r=49..150: every maximal proper divisor Q(r)/p "
           "rejected by a witness C<=150 (fallback 1500), witness <= r-1",
     compute_c4),
    ("C5", "positive period anchors r grid in [49,150]: "
           "S(C+Q(r),r) == S(C,r)",
     compute_c5),
    ("C6", "equal-Q block minimal-witness-map identity r=2..150 "
           "(observation, K1145 extension)",
     compute_c6),
    ("C7", "reject-vector non-identity within equal-Q blocks "
           "(observation, negative: K1145 identity is exactly at the "
           "minimal-witness level)",
     compute_c7),
]


def assemble(no_cache):
    checks = []
    for name, desc, fn in CHECKS:
        data = fn(no_cache)
        checks.append({"name": "%s: %s" % (name, desc),
                       "ok": bool(data["ok"]), "data": data})
    audit = {
        "title": ("REMO survivor column, maximal-proper-divisor reduction "
                  "(LEMMA RED) and the r = 49..150 maxdiv sweep "
                  "(fast lane; follows K0925 S32, K1145 S48)"),
        "date": "2026-11-20",
        "item": "K1163",
        "follows": ("K0859 (Theorem D recursion); K0919 (THEOREM PER); "
                    "K0922 (LEMMA DIV); K0925 (THEOREM W+, S32); "
                    "K0926 (E6U plateau, window form); K0928; "
                    "K1145 (THEOREM S48); K1154 (E-side necessity, "
                    "PNE)"),
        "checks": checks,
        "maxdiv_witness_table": {
            "path": "output/maxdiv_witness_table.txt",
            "format": ("one line per r: 'r=<r> w_2 w_3 w_5 ...' with "
                       "primes ascending (primes_upto(r)); w = minimal "
                       "witness C rejecting Q(r)/p (window [1,150] then "
                       "[151,1500], fail-closed); same sweep rows as the "
                       "checks"),
            "sha256": sha256_text(build_table(no_cache)),
            "rows": R_MAX - R_MIN + 1,
        },
        "all_ok": all(c["ok"] for c in checks),
    }
    return json.dumps(audit, indent=1, sort_keys=True) + "\n"


def main():
    args = sys.argv[1:]
    no_cache = "--no-cache" in args
    os.makedirs(OUT, exist_ok=True)
    t0 = time.time()
    a = assemble(no_cache)
    b = assemble(False)
    if a != b:
        sys.stderr.write("AUDIT ASSEMBLY NOT BYTE-IDENTICAL\n")
        sys.exit(1)
    with open(os.path.join(OUT, "audit.json"), "w") as f:
        f.write(a)
    with open(os.path.join(OUT, "maxdiv_witness_table.txt"), "w") as f:
        f.write(build_table(False))
    n_ok = 0
    for c in json.loads(a)["checks"]:
        print("CHECK", c["name"].split(":")[0], "OK" if c["ok"] else "FAIL")
        n_ok += 1 if c["ok"] else 0
    print("STATUS: COMPLETE checks:%d ok:%d all_ok:%s elapsed:%.1fs"
          % (len(json.loads(a)["checks"]), n_ok,
             json.loads(a)["all_ok"], time.time() - t0))
    sys.exit(0 if json.loads(a)["all_ok"] else 1)


if __name__ == "__main__":
    main()
