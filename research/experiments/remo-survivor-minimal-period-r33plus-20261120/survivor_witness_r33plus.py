#!/usr/bin/env python3
"""REMO survivor-column minimal period, r = 33..48 extension of the
K0925 small-witness sweep (THEOREM S32 -> S48), K1143.

Declared lane: research/log/2026-11-20-remo-survivor-witness-r33plus-
single-owner-note.md (single owner, fast lane).

Context (published, K0859/K0919/K0922/K0924/K0925).  For the uniform
board counting recursion E(C,r) (K0859 Theorem D), with Q(r) =
lcm(1..r):

  * THEOREM W+ (K0925, universal, every C >= 1): elim(E(C+d,r)) ==
    elim(E(C,r)) iff Q(r) | d; hence S(C+Q(r),r) == S(C,r) for all C,
    i.e. Q(r) is a period of the survivor column (the survivor is a
    function of the run, which the elim tuple pins).
  * LEMMA DIV (K0922, universal, column-generic): every period of a
    periodic column divides Q(r); so the survivor column's minimal
    period is a divisor of Q(r).
  * Therefore the survivor column's minimal period is exactly Q(r)
    iff every PROPER divisor d of Q(r) is rejected by at least one
    witness C with S(C+d,r) != S(C,r).

K0925 THEOREM S32 did this for r = 2..32 (72,397 proper divisors,
all witnessed with C <= 150, fallback [151,1500] never used).  This
experiment extends the SAME method to r = 33..48 (1,548,272 proper
divisors enumerated from the factorization of Q(r), since trial
division to sqrt(Q(48)) ~ 2.1e10 is not feasible).

SURVIVOR dynamics: verbatim survivor_fast of the K0925 verifier
(closed-form share-count rewrite of the K0859 recursion; the
K0925 TWIN check already pinned it to the per-stone verbatim
recursion).

Machine checks (deterministic, stdlib only, no network; per-(check,r)
checkpoints in output/; --no-cache forces recomputation; --budget=N
seconds stops at a shard boundary with resumable progress; the audit
is assembled twice and required byte-identical):

S0    DIVISOR ENUMERATION: for r = 2..20 the factorization-based
      divisor list equals trial-division divisors(Q(r)) exactly
      (multiset and sorted order); for r = 33..48 the factorization
      exponent pattern of Q(r) matches the analytic pattern
      e_p = max{a : p^a <= r}.
S1    K0925 REPRODUCTION PINS: for r = 17..32 the sweep recomputes
      (proper, unwitnessed, wit_max_sv, wit_argmax_over_Q,
      sv_C1_same) and all five must equal the K0925 published audit
      values verbatim (audit sha256 b3733ed5..., check W5 data).
S2    THE MAIN SWEEP (r = 33..48): every proper divisor d of Q(r) is
      rejected by a witness C in [1,150] (fallback [151,1500]),
      witness minimal ascending, exact same search semantics as
      K0925 W5; aggregates per r plus a chained sha256 pinning the
      exact per-divisor witness stream "d w" (sorted ascending d,
      chunked, restart-safe).
S3    POSITIVE PERIOD ANCHOR: for each r = 33..48 and C in [1,1500]
      plus anchors C in {Q-1, Q+1, Q+5, 2Q-1}:
      S(C+Q(r),r) == S(C,r) (machine anchor of the positive
      direction; the universal proof is K0925 THEOREM W+).
S4    TWIN ANCHOR at the new range: for r = 33..48 and C in [1,150]
      the verbatim per-stone K0859 recursion, its closed-form twin
      and the swept survivor_fast all agree on the full
      (elimination, survivor) pair; K0925 TWIN already pinned the
      dynamics for r = 2..24 (C in [1,200] plus anchors).

With all checks green and LEMMA DIV, the survivor column's minimal
period is exactly Q(r) for every r = 33..48 (machine determination,
same trust boundary as K0925 THEOREM S32; combined with K0925 the
swept range is r = 2..48).  The universal survivor statement
(bounded-witness conjecture) stays OPEN.  Nothing here concerns
non-uniform boards or the 11x11 empty board.
"""

import hashlib
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")

R_PINS = list(range(17, 33))             # S1 range (K0925 published)
R_MAIN = list(range(33, 49))             # S2 range (new)
SURV_WINDOW = 150
SURV_FALLBACK = 1500
SHARD = 16384                            # S2 divisor shard for resume

# K0925 published audit (research/experiments/remo-uniform-witness-
# theorem-20261117/output/remo_uniform_witness_theorem_audit.json,
# sha256 b3733ed5f6d8db88e60fb6c3ac5379d94677cd091bc50b21909adcd259e99390)
# check W5 data values for r = 17..32, verbatim.
K0925_W5_PINS = {
    17: {"proper": 479, "sv_C1_same": 227, "unwitnessed": 0,
         "wit_argmax_over_Q": 17, "wit_max_sv": 12},
    18: {"proper": 479, "sv_C1_same": 227, "unwitnessed": 0,
         "wit_argmax_over_Q": 17, "wit_max_sv": 12},
    19: {"proper": 959, "sv_C1_same": 438, "unwitnessed": 0,
         "wit_argmax_over_Q": 209, "wit_max_sv": 9},
    20: {"proper": 959, "sv_C1_same": 438, "unwitnessed": 0,
         "wit_argmax_over_Q": 209, "wit_max_sv": 9},
    21: {"proper": 959, "sv_C1_same": 438, "unwitnessed": 0,
         "wit_argmax_over_Q": 209, "wit_max_sv": 9},
    22: {"proper": 959, "sv_C1_same": 438, "unwitnessed": 0,
         "wit_argmax_over_Q": 209, "wit_max_sv": 9},
    23: {"proper": 1919, "sv_C1_same": 860, "unwitnessed": 0,
         "wit_argmax_over_Q": 163438, "wit_max_sv": 8},
    24: {"proper": 1919, "sv_C1_same": 860, "unwitnessed": 0,
         "wit_argmax_over_Q": 163438, "wit_max_sv": 8},
    25: {"proper": 2879, "sv_C1_same": 1348, "unwitnessed": 0,
         "wit_argmax_over_Q": 5, "wit_max_sv": 20},
    26: {"proper": 2879, "sv_C1_same": 1348, "unwitnessed": 0,
         "wit_argmax_over_Q": 5, "wit_max_sv": 20},
    27: {"proper": 3839, "sv_C1_same": 1888, "unwitnessed": 0,
         "wit_argmax_over_Q": 15, "wit_max_sv": 18},
    28: {"proper": 3839, "sv_C1_same": 1888, "unwitnessed": 0,
         "wit_argmax_over_Q": 15, "wit_max_sv": 18},
    29: {"proper": 7679, "sv_C1_same": 3725, "unwitnessed": 0,
         "wit_argmax_over_Q": 29, "wit_max_sv": 28},
    30: {"proper": 7679, "sv_C1_same": 3725, "unwitnessed": 0,
         "wit_argmax_over_Q": 29, "wit_max_sv": 28},
    31: {"proper": 15359, "sv_C1_same": 7317, "unwitnessed": 0,
         "wit_argmax_over_Q": 29, "wit_max_sv": 27},
    32: {"proper": 18431, "sv_C1_same": 9146, "unwitnessed": 0,
         "wit_argmax_over_Q": 29, "wit_max_sv": 25},
}


# ---------------------------------------------------------------------------
# the survivor dynamics: verbatim K0925 survivor_fast (closed-form
# share-count rewrite of the K0859 Theorem-D recursion)
# ---------------------------------------------------------------------------

def survivor_fast(C, r):
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
        loser = active[li]
        counts[loser] = 0
        active.pop(li)
        if active:
            turn = li % len(active)
    return active[0]


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
    """Closed-form share-count rewrite (same dynamics)."""
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


# ---------------------------------------------------------------------------
# arithmetic
# ---------------------------------------------------------------------------

def lcm_all(r):
    out = 1
    for i in range(2, r + 1):
        a = out
        b = i
        while b:
            a, b = b, a % b
        out = out * i // a
    return out


def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def prime_power_exponents(r):
    """(p, e) with p prime <= r, e = max{a : p^a <= r}: the
    factorization of Q(r) = lcm(1..r)."""
    fac = []
    for p in range(2, r + 1):
        if not is_prime(p):
            continue
        e = 0
        pp = p
        while pp <= r:
            e += 1
            pp *= p
        fac.append((p, e))
    return fac


def divisors_from_factors(fac):
    divs = [1]
    for p, e in fac:
        divs = [d * p ** i for d in divs for i in range(e + 1)]
    divs.sort()
    return divs


def divisors_trial(n):
    out = []
    i = 1
    while i * i <= n:
        if n % i == 0:
            out.append(i)
            if i != n // i:
                out.append(n // i)
        i += 1
    return sorted(out)


def proper_divisors(r, Q=None):
    """Sorted proper divisors of Q(r) (all divisors except Q)."""
    if Q is None:
        Q = lcm_all(r)
    divs = divisors_from_factors(prime_power_exponents(r))
    assert divs[-1] == Q, "factorization/lcm disagreement"
    return divs[:-1]


# ---------------------------------------------------------------------------
# witness search (K0925 W5 semantics: minimal ascending C, window
# [1,150], fallback [151,1500]) with a cache of the small-C column
# ---------------------------------------------------------------------------

class SCache:
    def __init__(self, r):
        self.r = r
        # 1-based small column values C = 1..SURV_FALLBACK
        self.vals = [survivor_fast(C, r)
                     for C in range(0, SURV_FALLBACK + 1)]

    def small(self, C):
        return self.vals[C]

    def big(self, X):
        return survivor_fast(X, self.r)


def witness(cache, d, counter):
    """Minimal witness C in [1,150] (fallback [151,1500]) or None;
    counts every simulation in counter[0]."""
    counter[0] += 1
    if cache.big(1 + d) != cache.small(1):
        return 1, False
    for C in range(2, SURV_WINDOW + 1):
        counter[0] += 1
        if cache.big(C + d) != cache.small(C):
            return C, False
    for C in range(SURV_WINDOW + 1, SURV_FALLBACK + 1):
        counter[0] += 1
        if cache.big(C + d) != cache.small(C):
            return C, True
    return None, None


# ---------------------------------------------------------------------------
# checkpoints
# ---------------------------------------------------------------------------

def _path(name):
    return os.path.join(OUT, name)


def load_json(name, no_cache):
    if no_cache:
        return None
    p = _path(name)
    if os.path.exists(p):
        with open(p) as f:
            return json.load(f)
    return None


def save_json(name, obj):
    os.makedirs(OUT, exist_ok=True)
    tmp = _path(name + ".tmp")
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=1, sort_keys=True, ensure_ascii=False)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, _path(name))


def ck_name(tag, r):
    return "sv33ck_%s_r%d.json" % (tag, r)


def prog_name(tag, r):
    return "sv33prog_%s_r%d.json" % (tag, r)


# ---------------------------------------------------------------------------
# the resumable sweep (S2 and S1 share this machinery)
# ---------------------------------------------------------------------------

def sweep_resumable(tag, r, divs, no_cache, deadline):
    """Sweep one r over sorted proper divisors in shards, resumable at
    shard boundaries; chained chunk hashes pin the full witness
    stream restart-safe.  Returns (agg, None) or (None, shard_index)."""
    progname = prog_name(tag, r)
    prog = load_json(progname, no_cache)
    cache = None
    agg = None
    chunk_hashes = None
    start_shard = 0
    if prog is not None:
        agg = prog["agg"]
        chunk_hashes = prog["chunk_hashes"]
        start_shard = prog["shard_done"]
        cache = SCache(r)          # rebuilt cheaply on resume
    else:
        agg = {"proper": len(divs), "n_wit_C1": 0, "fallback_count": 0,
               "unwitnessed": 0, "unwitnessed_first": None,
               "wit_max_sv": 0, "wit_argmax_d": None, "hist": {},
               "n_sims": 0}
        chunk_hashes = []
    n_shards = (len(divs) + SHARD - 1) // SHARD
    Q = lcm_all(r)
    for si in range(start_shard, n_shards):
        if deadline is not None and time.time() + est_shard_sec(r) \
                > deadline:
            save_json(progname, {"shard_done": si,
                                 "chunk_hashes": chunk_hashes,
                                 "agg": agg,
                                 "elapsed_note": "budget stop"})
            return None, si
        if cache is None:
            cache = SCache(r)
        chunk = hashlib.sha256()
        lo = si * SHARD
        hi = min(lo + SHARD, len(divs))
        for i in range(lo, hi):
            d = divs[i]
            counter = [0]
            w, fb = witness(cache, d, counter)
            agg["n_sims"] += counter[0]
            chunk.update(("%d %s\n" % (d,
                                      "NONE" if w is None else w))
                         .encode())
            if w is None:
                agg["unwitnessed"] += 1
                if agg["unwitnessed_first"] is None:
                    agg["unwitnessed_first"] = d
                continue
            if fb:
                agg["fallback_count"] += 1
            agg["hist"][str(w)] = agg["hist"].get(str(w), 0) + 1
            if w == 1:
                agg["n_wit_C1"] += 1
            if w > agg["wit_max_sv"]:
                agg["wit_max_sv"] = w
                agg["wit_argmax_d"] = d
        chunk_hashes.append(chunk.hexdigest())
        save_json(progname, {"shard_done": si + 1,
                             "chunk_hashes": chunk_hashes,
                             "agg": agg})
    # finalize
    agg["r"] = r
    agg["Q"] = str(Q)
    agg["sv_C1_same"] = agg["proper"] - agg["unwitnessed"] - \
        agg["n_wit_C1"]
    agg["wit_argmax_over_Q"] = (Q // agg["wit_argmax_d"]
                                 if agg["wit_argmax_d"] else None)
    stream = hashlib.sha256()
    for i, h in enumerate(chunk_hashes):
        stream.update(("%d:%s\n" % (i, h)).encode())
    agg["stream_sha256"] = stream.hexdigest()
    agg["chunk_hashes"] = chunk_hashes
    os.makedirs(OUT, exist_ok=True)
    if os.path.exists(_path(progname)):
        os.remove(_path(progname))
    return agg, None


def est_shard_sec(r):
    """Conservative shard-cost estimate for deadline checks
    (seconds; observed per divisor is 127-241 us at r = 33..48, so
    this is roughly 2x the measured worst case)."""
    return 0.0003 * SHARD + 0.000005 * SHARD * r


# ---------------------------------------------------------------------------
# check computations
# ---------------------------------------------------------------------------

def compute_s0(no_cache):
    """Factorization vs trial division for r = 2..20 and the analytic
    exponent pattern for r = 33..48."""
    eq_small = True
    det = {}
    for r in range(2, 21):
        Q = lcm_all(r)
        a = divisors_from_factors(prime_power_exponents(r))
        b = divisors_trial(Q)
        eq = (a == b) and (a[-1] == Q)
        det["r%d" % r] = {"equal": eq, "n": len(a)}
        eq_small = eq_small and eq
    exp_pat = True
    for r in R_MAIN:
        fac = prime_power_exponents(r)
        ok = all(p ** e <= r < p ** (e + 1) for p, e in fac)
        ok = ok and len(fac) == sum(1 for p in range(2, r + 1)
                                    if is_prime(p))
        n_div = 1
        for p, e in fac:
            n_div *= e + 1
        det["r%d" % r] = {"pattern_ok": ok, "n_primes": len(fac),
                          "tau_Q": n_div}
        exp_pat = exp_pat and ok
    return {"small_equal": eq_small, "exp_pattern": exp_pat,
            "detail": det}, eq_small and exp_pat


def compute_s1(no_cache, deadline):
    """K0925 reproduction pins r = 17..32."""
    out = {}
    ok = True
    for r in R_PINS:
        ck = load_json(ck_name("s1", r), no_cache)
        if ck is None:
            agg, stopped = sweep_resumable("s1", r,
                                           proper_divisors(r),
                                           no_cache, deadline)
            if agg is None:
                return None, ("s1", r, stopped)
            pin = K0925_W5_PINS[r]
            match = (agg["proper"] == pin["proper"] and
                     agg["unwitnessed"] == pin["unwitnessed"] and
                     agg["wit_max_sv"] == pin["wit_max_sv"] and
                     agg["wit_argmax_over_Q"] ==
                     pin["wit_argmax_over_Q"] and
                     agg["sv_C1_same"] == pin["sv_C1_same"])
            ck = {"r": r, "proper": agg["proper"],
                  "unwitnessed": agg["unwitnessed"],
                  "wit_max_sv": agg["wit_max_sv"],
                  "wit_argmax_over_Q": agg["wit_argmax_over_Q"],
                  "sv_C1_same": agg["sv_C1_same"],
                  "pin_match": bool(match),
                  "stream_sha256": agg["stream_sha256"]}
            save_json(ck_name("s1", r), ck)
        out["r%d" % r] = ck
        ok = ok and ck["pin_match"]
    return out, ok


def compute_s2(no_cache, deadline):
    """The main sweep r = 33..48."""
    out = {}
    ok = True
    for r in R_MAIN:
        ck = load_json(ck_name("s2", r), no_cache)
        if ck is None:
            agg, stopped = sweep_resumable("s2", r,
                                           proper_divisors(r),
                                           no_cache, deadline)
            if agg is None:
                return None, ("s2", r, stopped)
            ck = agg
            save_json(ck_name("s2", r), ck)
        out["r%d" % r] = ck
        ok = ok and ck["unwitnessed"] == 0
    return out, ok


def compute_s3(no_cache, deadline):
    """Positive period anchors for r = 33..48."""
    out = {}
    ok = True
    for r in R_MAIN:
        ck = load_json(ck_name("s3", r), no_cache)
        if ck is None:
            Q = lcm_all(r)
            cs = list(range(1, SURV_FALLBACK + 1)) + \
                [Q - 1, Q + 1, Q + 5, 2 * Q - 1]
            bad = 0
            for C in cs:
                if deadline is not None and time.time() > deadline:
                    return None, ("s3", r, C)
                if survivor_fast(C, r) != survivor_fast(C + Q, r):
                    bad += 1
            ck = {"r": r, "Q": str(Q), "anchors": len(cs),
                  "per_bad": bad}
            save_json(ck_name("s3", r), ck)
        out["r%d" % r] = ck
        ok = ok and ck["per_bad"] == 0
    return out, ok


def compute_s4(no_cache, deadline):
    """TWIN anchor at the new r values: the swept survivor_fast
    dynamics equal the verbatim per-stone K0859 recursion (and its
    closed-form twin) for r = 33..48, C in [1,150]."""
    out = {}
    ok = True
    for r in R_MAIN:
        ck = load_json(ck_name("s4", r), no_cache)
        if ck is None:
            pairs = 0
            bad = 0
            for C in range(1, SURV_WINDOW + 1):
                if deadline is not None and time.time() > deadline:
                    return None, ("s4", r, C)
                td = theorem_d(C, r)
                tdf = theorem_d_fast(C, r)
                pairs += 1
                if td != tdf or td[1] != survivor_fast(C, r):
                    bad += 1
            ck = {"r": r, "pairs": pairs, "mismatches": bad}
            save_json(ck_name("s4", r), ck)
        out["r%d" % r] = ck
        ok = ok and ck["mismatches"] == 0
    return out, ok


# ---------------------------------------------------------------------------
# audit assembly (deterministic; regenerate twice, byte-identical)
# ---------------------------------------------------------------------------

def assemble_audit(no_cache, deadline=None):
    checks = []

    def record(name, ok, data):
        checks.append({"name": name, "ok": bool(ok), "data": data})

    s0, s0_ok = compute_s0(no_cache)
    record("S0: divisor enumeration from the factorization of Q(r) == "
           "trial-division divisors for r = 2..20 (exact multiset and "
           "sorted order), analytic exponent pattern e_p = "
           "max{a : p^a <= r} holds for r = 33..48", s0_ok, s0)

    s1, s1_stop = compute_s1(no_cache, deadline)
    if s1 is None:
        return None, s1_stop
    record("S1: K0925 REPRODUCTION PINS r = 17..32: recomputed "
           "(proper, unwitnessed, wit_max_sv, wit_argmax_over_Q, "
           "sv_C1_same) equal the published K0925 audit values "
           "verbatim (audit sha256 b3733ed5...); the r = 2..32 "
           "sweep semantics are reproduced exactly by this "
           "implementation", s1_stop, s1)

    s2, s2_stop = compute_s2(no_cache, deadline)
    if s2 is None:
        return None, s2_stop
    record("S2: SURVIVOR minimality extension (machine, r = 33..48): "
           "every proper divisor of Q(r) is rejected as a "
           "survivor-column period by a witness C <= 150 (fallback "
           "window [151,1500]); with K0922 LEMMA DIV the survivor "
           "column's minimal period is exactly Q(r) for r = 33..48; "
           "per-divisor witness stream pinned by chained sha256",
           s2_stop, s2)

    s3, s3_stop = compute_s3(no_cache, deadline)
    if s3 is None:
        return None, s3_stop
    record("S3: POSITIVE period anchor r = 33..48: S(C+Q(r),r) == "
           "S(C,r) for C in [1,1500] plus anchors "
           "{Q-1,Q+1,Q+5,2Q-1} (machine anchor; the universal proof "
           "is K0925 THEOREM W+)", s3_stop, s3)

    s4, s4_stop = compute_s4(no_cache, deadline)
    if s4 is None:
        return None, s4_stop
    record("S4: TWIN anchor at the new range: the swept "
           "survivor_fast dynamics match the verbatim per-stone "
           "K0859 recursion (full (elim, survivor) pair via the "
           "closed-form twin theorem_d_fast) for r = 33..48 and "
           "C in [1,150]; the K0925 TWIN check already pinned the "
           "dynamics for r = 2..24, C = [1,200] plus anchors",
           s4_stop, s4)

    audit = {
        "item": "K1143",
        "title": "Survivor-column minimal period exactly Q(r) for "
                 "r = 33..48 by small witnesses (every proper divisor "
                 "rejected), extending K0925 theorem S32 to S48; "
                 "r = 2..32 reproduction pinned verbatim",
        "date": "2026-11-20",
        "follows": "K0919 (THEOREM PER), K0922 (LEMMA DIV), K0925 "
                   "(THEOREM S32, THEOREM W+, published audit pins)",
        "checks": checks,
    }
    audit["all_ok"] = all(c["ok"] for c in checks)
    return audit, None


def main():
    no_cache = "--no-cache" in sys.argv
    budget = None
    for a in sys.argv:
        if a.startswith("--budget="):
            budget = int(a.split("=", 1)[1])
    t_start = time.time()
    deadline = t_start + budget if budget else None
    audit, stopped = assemble_audit(no_cache, deadline)
    if audit is None:
        tag, r, info = stopped
        print("STATUS: INCOMPLETE %s r=%s at %s (rerun to resume)"
              % (tag, r, info))
        return 0
    a1 = audit
    # second assemble for determinism (checkpoints make it cheap);
    # with --no-cache the sweep is recomputed in full.
    a2, stopped2 = assemble_audit(no_cache, None)
    if a2 is None:
        print("FAIL: second assemble incomplete")
        return 1
    b1 = json.dumps(a1, indent=1, sort_keys=True,
                    ensure_ascii=False) + "\n"
    b2 = json.dumps(a2, indent=1, sort_keys=True,
                    ensure_ascii=False) + "\n"
    if b1 != b2:
        print("FAIL: assemble is not deterministic")
        return 1
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "audit.json"), "w") as f:
        f.write(b1)
    for c in a1["checks"]:
        print("%s  %s" % ("OK " if c["ok"] else "FAIL",
                          c["name"][:110]))
    print("STATUS: COMPLETE checks:%d all_ok:%s elapsed:%.1fs"
          % (len(a1["checks"]), a1["all_ok"],
             time.time() - t_start))
    return 0 if a1["all_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
