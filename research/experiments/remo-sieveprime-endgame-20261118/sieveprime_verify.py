#!/usr/bin/env python3
"""Machine anchor for K0939 (SIEVE-PRIME / END-SIEVE).

Universal prime-side closure of the SIEVE structure: the t = 0 endgame
reached by the watched (K0937 INV-TRACK tracker, prime N) is a DIVISOR
SIEVE.  Every phase state has the ptr-frame form E(P; alpha, beta) =
[P]^alpha + [P+1]^beta with the watched at position alpha (V) resp.
alpha-1 (U) and the stone identity N = P(k+1) + beta + s (s = 0 V,
1 U); the watched dies in a phase  <=>  the circle size k divides N
(END-SIEVE).  The endgame entry of a prime game is always a family
state n in {w-1, w} (ENTRY-LOC), and on the family the survival
verdict is exactly primality of N (END-SIEVE-IFF).  Hence SIEVE-PRIME:
N = 2m+1 prime => V(m) = 0, N = 2m+3 prime => U(m) = m-1, and the
twin laws LAW1/LAW2 (K0929) become universal iff theorems
(P(C) = 1 <=> C prime, C >= 2; P(C) = C-1 <=> C+1 prime, C >= 2).

Instruments (sievegen_core.py is the byte-identical K0937 copy):
  endgame_engine(w,h,n,a)  literal positional endgame engine (phase
                           rule of K0928 Lemma P), per-phase records
  emodel_replay(side,w,h,n) pure-arithmetic E-model replay with
                           per-phase identity + congruence self-checks

Checks:
  PIN        committed K0929 tables (sha256, format, P(1..40) anchor)
  REDRECON   committed U/V tables vs committed P table via proved RED
             (m <= 3999; fixes the 1-based list indexing of all pins)
  FAMILY     ALL family states (w <= 60: V n in {w-1,w}, 1<=h<=min(n,w),
             a=h; U 0<=h<=min(n-1,w), a=h+1): literal engine vs
             E-model; per-phase structure E(P;alpha,beta), watch
             position alpha / alpha-1, identity N=P(k+1)+beta+s,
             transition formulas, death <=> k|N; final survives <=> N
             prime (END-SIEVE-IFF at machine level)
  ENTRY      prime N, m <= 200000 both sides: tracker reaches the
             endgame (no death / collapse / window exit), entry is a
             family state with a = h / h+1 and N = w(n+1)+h(+1)
             (ENTRY-LOC), and the E-model replay survives
  PINREPRO   ALL m <= 8000 both sides: arithmetic prediction
             (tracker death, or endgame + E-model survival) equals
             primality of N AND the committed U/V pins (end-to-end
             reproduction of the K0929 tables from pure arithmetic)
  ENGINE     fresh python engine m <= 600 both sides: death None and
             survivor == watched  <=>  N prime; survivor verdict == pin
  PINSIEVE   committed tables, full iff: P(C)=1 <=> C prime (C=2..8000),
             P(C)=C-1 <=> C+1 prime, V(m)=0 <=> 2m+1 prime,
             U(m)=m-1 <=> 2m+3 prime (m <= 8000)

All stdlib, deterministic. Run from the experiment directory:
    python3 sieveprime_verify.py
Exit status 0 iff every check passes.
"""

import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from sievegen_core import play_full, track_gen, isprime  # noqa: E402

PIN_UV = os.path.join(HERE, "..", "remo-pc-twin-laws-20261117",
                      "data", "pc_uv8000.json")
PIN_P = os.path.join(HERE, "..", "remo-pc-twin-laws-20261117",
                     "data", "pc_p8000.json")
PIN_UV_SHA = "8a3b318bd26b8197c66fd55d79007654d2926a18af165132af8c194bc76d8ae2"
PIN_P_SHA = "58a414bc31fb6266cc2d0e10000436e50f396135847bab5a32163cffff0b975e"
P_PIN_1_40 = [0, 1, 1, 3, 1, 5, 1, 5, 5, 9, 1, 11, 1, 5, 7, 15, 1, 17, 1, 15,
              17, 21, 1, 21, 11, 15, 7, 27, 1, 29, 1, 27, 17, 21, 11, 35, 1,
              5, 7, 39]  # P(1)..P(40), committed pin (K0919/K0929)

MBIG = 200000       # ENTRY tracker range (N <= 400003)
M_REPRO = 8000       # PINREPRO range (covers the committed pin tables)
M_ENG = 600         # fresh python engine range
FAM_W = 60          # FAMILY literal-engine grid width


def spf_sieve(nmax):
    """Smallest-prime-factor table for 0..nmax."""
    tab = list(range(nmax + 1))
    for i in range(2, int(nmax ** 0.5) + 1):
        if tab[i] == i:
            for j in range(i * i, nmax + 1, i):
                if tab[j] == j:
                    tab[j] = i
    return tab


# ------------- endgame instruments ---------------------------------------

def endgame_engine(w, h, n, a):
    """Literal positional endgame engine from F(w,h;n) (holdings
    [w]^(n-h)+[w+1]^h, pot w, ptr 0, watched at position n-a).
    Plays the phase rule until one player remains or the watched dies.

    Returns (survives, records); records[i] = phase i+1 data:
    {k, P, alpha, beta, q, r, wpos, struct, watchpos, inv, died,
    kdivN, trans} where struct/watchpos/inv/trans flag the structural
    theorem at that phase and trans is None at the last phase.
    """
    hold = [w] * (n - h) + [w + 1] * h
    active = list(range(n))
    ptr = 0
    pot = w
    watch = n - a
    records = []
    while len(active) > 1:
        k = len(active)
        q, r = divmod(pot, k)
        circle = active[ptr:] + active[:ptr]
        holdings = [hold[lab] for lab in circle]
        alpha = holdings.index(pot + 1) if (pot + 1) in holdings else k
        beta = k - alpha
        rec = {"k": k, "P": pot, "alpha": alpha, "beta": beta,
               "q": q, "r": r}
        rec["struct"] = holdings == [pot] * alpha + [pot + 1] * beta
        rec["wpos"] = circle.index(watch) if watch in circle else None
        rec["inv"] = None
        rec["died"] = False
        rec["kdivN"] = None
        rec["trans"] = None
        records.append(rec)
        if q:
            for lab in active:
                hold[lab] += q
        for i in range(r):
            hold[active[(ptr + i) % k]] += 1
        L = (ptr + pot) % k
        loser = active[L]
        if loser == watch:
            rec["died"] = True
            return False, records
        # transition prediction for the next phase
        if r < alpha:
            rec["trans"] = (pot + q, alpha - r - 1, beta + r)
        else:
            rec["trans"] = (pot + q + 1, beta + 2 * alpha - r - 1, r - alpha)
        pot = hold[loser]
        active.pop(L)
        ptr = L % len(active) if active else 0
    return True, records


def emodel_replay(side, w, h, n):
    """Pure-arithmetic E-model replay of the endgame from a family
    entry F(w,h;n) (watched a=h for V, a=h+1 for U). Per phase the
    state is (P, alpha, beta); the identity N = P(k+1)+beta+s and the
    death congruence (death <=> k|N) are self-checked each phase.

    Returns (survives, fails) with fails a list of violation records.
    """
    fails = []
    if n <= 1:
        # n=1: the watched is the sole player (family entry, a=h(h+1)=n);
        # n=0: degenerate V(m=1) base, no circle at all. Both survive.
        return True, fails
    s = 0 if side == "V" else 1
    N = w * (n + 1) + h + s
    P, alpha, beta = w, n - h, h
    k = n
    while k > 1:
        if N != P * (k + 1) + beta + s:
            fails.append(["inv", side, w, h, n, P, alpha, beta, k])
        q, r = divmod(P, k)
        dies = (r == alpha) if side == "V" else (r == alpha - 1)
        if dies != (N % k == 0):
            fails.append(["cong", side, w, h, n, P, alpha, beta, k, r])
            return False, fails
        if dies:
            return False, fails
        if r < alpha:
            P, alpha, beta = P + q, alpha - r - 1, beta + r
        else:
            P, alpha, beta = P + q + 1, beta + 2 * alpha - r - 1, r - alpha
        k -= 1
    return True, fails


def family_states(side, w_hi):
    """Family entry states (w, n, h, a, N) for w = 2..w_hi."""
    out = []
    for w in range(2, w_hi + 1):
        for n in (w - 1, w):
            if side == "V":
                for h in range(1, min(n, w) + 1):
                    out.append((w, n, h, h, w * (n + 1) + h))
            else:
                for h in range(0, min(n - 1, w) + 1):
                    out.append((w, n, h, h + 1, w * (n + 1) + h + 1))
    return out


def tracker_entry(side, m):
    """Endgame entry state (w,h,n,a) of the tracker; base state if the
    tracker exits at w=2 with no recorded step."""
    tr = track_gen(side, m)
    steps = tr["steps"]
    if tr["status"].startswith("endgame"):
        if steps:
            last = steps[-1]
            return tr, (last["w"] + 1, last["h2"], last["n2"], last["a2"])
        if side == "V":
            return tr, (2, 1, m - 1, 1)
        return tr, (2, 0, m, 1)
    return tr, (None, None, None, None)


# ------------- checks ----------------------------------------------------

def run_checks():
    res = {}
    ok_all = True

    def put(name, ok, n=None, extra=None):
        nonlocal ok_all
        entry = {"ok": bool(ok)}
        if n is not None:
            entry["count"] = n
        if extra:
            entry.update(extra)
        res[name] = entry
        if not ok:
            ok_all = False

    # covers ENTRY (2m+3 <= 2*MBIG+3), PINREPRO and the U pins of
    # PINSIEVE (2m+3 <= 2*8000+3 for the committed m <= 8000 tables)
    SPF = spf_sieve(max(2 * MBIG + 4, 2 * M_REPRO + 4, 16004))

    def prime(n):
        return n >= 2 and SPF[n] == n

    # ---- PIN ----
    with open(PIN_UV, "rb") as f:
        uv_bytes = f.read()
    with open(PIN_P, "rb") as f:
        p_bytes = f.read()
    uv = json.loads(uv_bytes)
    pp = json.loads(p_bytes)
    pin_ok = (hashlib.sha256(uv_bytes).hexdigest() == PIN_UV_SHA
              and hashlib.sha256(p_bytes).hexdigest() == PIN_P_SHA
              and uv["M"] == 8000 and len(uv["U"]) == 8000
              and len(uv["V"]) == 8000
              and pp["N"] == 8000 and len(pp["P"]) == 8000
              and pp["P"][:40] == P_PIN_1_40)
    put("PIN", pin_ok, extra={
        "uv_sha256": hashlib.sha256(uv_bytes).hexdigest()[:8],
        "p_sha256": hashlib.sha256(p_bytes).hexdigest()[:8]})

    U_pin, V_pin, P_pin = uv["U"], uv["V"], pp["P"]
    # list indexing (K0929 commit): P_pin[i] = P(i+1), U_pin[i] = U(i+1),
    # V_pin[i] = V(i+1) (dummy entry at index 0), fixed by REDRECON.

    # ---- REDRECON (proved RED, K0928: P(2m+1)=1+2V, P(2m+2)=3+2U) ----
    bad = 0
    for m in range(1, 4000):
        if P_pin[2 * m + 1 - 1] != 1 + 2 * V_pin[m - 1]:
            bad += 1
        if P_pin[2 * m + 2 - 1] != 3 + 2 * U_pin[m - 1]:
            bad += 1
    put("REDRECON", bad == 0, n=2 * 3999, extra={"mismatches": bad})

    # ---- FAMILY (END-INV / END-SIEVE / END-SIEVE-IFF, literal engine) --
    fam = {"struct": [], "watchpos": [], "inv": [], "cong": [],
           "trans": [], "iff": [], "emodel": []}
    fam_n = 0
    fam_ph = 0
    fam_trans = 0
    s_of = {"V": 0, "U": 1}
    for side in ("V", "U"):
        s = s_of[side]
        for (w, n, h, a, N) in family_states(side, FAM_W):
            fam_n += 1
            surv, recs = endgame_engine(w, h, n, a)
            fam_ph += len(recs)
            for i, rec in enumerate(recs):
                if not rec["struct"]:
                    fam["struct"].append([side, w, n, h, i + 1])
                if rec["wpos"] is None or \
                        (rec["wpos"] != (rec["alpha"] if side == "V"
                                         else rec["alpha"] - 1)):
                    fam["watchpos"].append([side, w, n, h, i + 1, rec["wpos"],
                                             rec["alpha"]])
                if N != rec["P"] * (rec["k"] + 1) + rec["beta"] + s:
                    fam["inv"].append([side, w, n, h, i + 1])
                if rec["died"] != (N % rec["k"] == 0):
                    fam["cong"].append([side, w, n, h, i + 1, rec["k"],
                                        rec["r"], rec["alpha"]])
                if rec["trans"] is not None:
                    fam_trans += 1
                    if i + 1 < len(recs):
                        nxt = recs[i + 1]
                        if rec["trans"] != (nxt["P"], nxt["alpha"],
                                            nxt["beta"]):
                            fam["trans"].append([side, w, n, h, i + 1,
                                                 rec["trans"],
                                                 (nxt["P"], nxt["alpha"],
                                                  nxt["beta"])])
            if surv != prime(N):
                fam["iff"].append([side, w, n, h, N, surv])
            esurv, efails = emodel_replay(side, w, h, n)
            if esurv != surv or efails:
                fam["emodel"].append([side, w, n, h, N, surv, esurv,
                                      efails[:3]])
    put("FAMILY",
        not any(fam[x] for x in fam),
        n=fam_n,
        extra={"phases": fam_ph, "transition_checks": fam_trans,
               "struct_fails": len(fam["struct"]),
               "watchpos_fails": len(fam["watchpos"]),
               "inv_fails": len(fam["inv"]),
               "cong_fails": len(fam["cong"]),
               "trans_fails": len(fam["trans"]),
               "iff_fails": len(fam["iff"]),
               "emodel_fails": len(fam["emodel"]),
               "fails": (fam["struct"] + fam["watchpos"] + fam["inv"] +
                         fam["cong"] + fam["trans"] + fam["iff"] +
                         fam["emodel"])[:10],
               "fail_count": sum(len(fam[x]) for x in fam)})

    # ---- ENTRY (ENTRY-LOC + E-model survival, primes m <= MBIG) -------
    ent = []
    ent_n = 0
    ent_maxw = 0
    emodel_fails = 0
    for side in ("V", "U"):
        s = s_of[side]
        for m in range(1, MBIG + 1):
            if side == "V" and m == 1:
                # degenerate base F(2,1;0): no circle, trivial survival
                continue
            N = 2 * m + 1 if side == "V" else 2 * m + 3
            if not prime(N):
                continue
            ent_n += 1
            tr, (w, h, n, a) = tracker_entry(side, m)
            if not tr["status"].startswith("endgame"):
                ent.append(["status", side, m, N, tr["status"]])
                continue
            ent_maxw = max(ent_maxw, w)
            ok = (n in (w - 1, w))
            if side == "V":
                ok = ok and 1 <= h <= min(n, w) and a == h
            else:
                ok = ok and 0 <= h <= min(n - 1, w) and a == h + 1
            ok = ok and N == w * (n + 1) + h + s
            if not ok:
                ent.append(["entry", side, m, N, w, h, n, a])
                continue
            esurv, efails = emodel_replay(side, w, h, n)
            if not esurv or efails:
                emodel_fails += 1
                ent.append(["emodel", side, m, N, w, h, n,
                            esurv, efails[:3]])
    put("ENTRY", not ent, n=ent_n,
        extra={"max_entry_w": ent_maxw, "emodel_fails": emodel_fails,
               "fails": ent[:10], "fail_count": len(ent)})

    # ---- PINREPRO (all m <= 8000: arithmetic prediction vs pins) -------
    rep = []
    rep_n = 0
    for side in ("V", "U"):
        s = s_of[side]
        for m in range(1, M_REPRO + 1):
            N = 2 * m + 1 if side == "V" else 2 * m + 3
            rep_n += 1
            tr, (w, h, n, a) = tracker_entry(side, m)
            if tr["status"] == "died":
                pred = False
            elif tr["status"].startswith("endgame"):
                pred, _ = emodel_replay(side, w, h, n)
            else:
                rep.append(["status", side, m, N, tr["status"]])
                continue
            if pred != prime(N):
                rep.append(["prime", side, m, N, pred])
            if side == "V":
                if pred != (V_pin[m - 1] == 0):
                    rep.append(["pin", "V", m, N, pred, V_pin[m - 1]])
            else:
                if pred != (U_pin[m - 1] == m - 1):
                    rep.append(["pin", "U", m, N, pred, U_pin[m - 1]])
    put("PINREPRO", not rep, n=rep_n,
        extra={"fails": rep[:10], "fail_count": len(rep)})

    # ---- ENGINE (fresh python engine, m <= M_ENG) ----------------------
    eng = []
    eng_n = 0
    for side in ("V", "U"):
        pot0 = 1 if side == "V" else 2
        for m in range(1, M_ENG + 1):
            N = 2 * m + 1 if side == "V" else 2 * m + 3
            watch = 0 if side == "V" else m - 1
            rec = play_full(m, pot0, watch)
            eng_n += 1
            pr = prime(N)
            if (rec["death"] is None) != pr:
                eng.append(["death", side, m, N, rec["death"]])
            if (rec["survivor"] == watch) != pr:
                eng.append(["survivor", side, m, N, rec["survivor"]])
            if side == "V":
                if (V_pin[m - 1] == 0) != pr:
                    eng.append(["pinV", m, N, V_pin[m - 1]])
            else:
                if (U_pin[m - 1] == m - 1) != pr:
                    eng.append(["pinU", m, N, U_pin[m - 1]])
    put("ENGINE", not eng, n=eng_n,
        extra={"fails": eng[:10], "fail_count": len(eng)})

    # ---- PINSIEVE (committed tables, full iff) -------------------------
    law1 = 0
    law2 = 0
    lawv = 0
    lawu = 0
    for C in range(2, 8001):
        if (P_pin[C - 1] == 1) != prime(C):
            law1 += 1
        if (P_pin[C - 1] == C - 1) != prime(C + 1):
            law2 += 1
    for m in range(1, 8001):
        if (V_pin[m - 1] == 0) != prime(2 * m + 1):
            lawv += 1
        if (U_pin[m - 1] == m - 1) != prime(2 * m + 3):
            lawu += 1
    put("PINSIEVE", law1 == 0 and law2 == 0 and lawv == 0 and lawu == 0,
        n=8000 + 7999 + 16000,
        extra={"law1_violations": law1, "law2_violations": law2,
               "v_violations": lawv, "u_violations": lawu})

    return {"all_ok": ok_all, "checks": res}


def main():
    res1 = run_checks()
    res2 = run_checks()
    same = json.dumps(res1, sort_keys=True) == json.dumps(res2, sort_keys=True)
    print(json.dumps({"all_ok": bool(res1["all_ok"] and res2["all_ok"]
                                     and same),
                      "deterministic": same,
                      "checks": {k: v["ok"] for k, v in
                                 res1["checks"].items()}},
                     sort_keys=True))
    sys.exit(0 if (res1["all_ok"] and res2["all_ok"] and same) else 1)


if __name__ == "__main__":
    main()
