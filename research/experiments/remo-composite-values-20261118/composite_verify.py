#!/usr/bin/env python3
"""Machine anchor for K0941 (composite-N values of the watched game).

The K0937/K0939 closure determined the PRIME side completely
(SIEVE-PRIME: N prime => V(m)=0 / U(m)=m-1).  This experiment closes
the COMPOSITE side: for odd composite N the watched never reaches the
t=0 endgame (LADDER-ONLY, THM-A), dies at ladder stretch
w = spf(N)-1 in a breaking (V) resp. block (U) phase (death
dichotomy, THM-B), the post-death circle is a uniform state
Z(w+1, n-t)  (V)  resp. an E-state  E(w+1; n-t-1-w, w)  (U,
non-collapse)  or  Z(w+2, w-1)  (U collapse), the death-stretch
frame->label map is the LAD-GEN composition (THM-D), and the survivor
of an E/uniform game is the Josephus-type recursion sigma_E/sigma_Z
(THM-C).  Hence V(m)/U(m) for composite N = frame[sigma] is pure
arithmetic, and combined with SIEVE-PRIME ALL m >= 1 values are
arithmetic (COMPOSITE-VALUES).

Instruments (sievegen_core.py is the byte-identical K0937 copy):
  predict(side, m)          pure-arithmetic value for ALL m >= 1
  predict_composite(side,m) composite branch with intermediate info
  sigma_E / sigma_Z         survivor frame position of E/uniform games
  death_frame(side,m,steps,death)  death-stretch frame + post-death
                            entry state (label map composition)

Checks:
  PIN        committed K0929 tables (sha256, format, P(1..40) anchor)
  DEATH      ALL composite m <= 8000 both sides: tracker status
             'died', death stretch w == spf(N)-1, V: r == h-1 and
             held == w+1 (breaking), U: r == h and held == w (block)
  FULLREPRO  ALL m <= 8000 both sides (16000 games): arithmetic
             prediction == committed pin value (composite branch =
             new arithmetic, prime branch = SIEVE-PRIME)
  STRUCT     composite m <= 1500 both sides (2141 games): literal
             positional engine vs THM-B/D: post-death ptr-frame circle
             labels == composed frame, holdings/pot == entry state,
             final survivor == frame[sigma] (THM-C)
  EGAME      literal engine vs sigma_E/sigma_Z on general E-states
             E(P;alpha,beta) and uniform states Z(M,K) (k <= 50,
             P,M grid) - anchors THM-C beyond family/post-death states
  ENGINE     fresh python engine m <= 600 both sides (1200 games):
             survivor label == predict(side, m) for ALL m (prime and
             composite)
  P2OBS      machine observations on N = p^2 games, composite
             m <= 8000: U collapse death (t=h=r=0) <=> N == spf(N)^2
             (29 games each way); V N=p^2 death step (n,t,r,h) ==
             (p,1,0,1); U N=p^2 death step (t,h,r) == (1,0,0)

All stdlib, deterministic. Run from the experiment directory:
    python3 composite_verify.py
Exit status 0 iff every check passes.
"""

import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from sievegen_core import play_full, track_gen, isprime, spf  # noqa: E402
from composite_core import (predict, predict_composite,  # noqa: E402
                            sigma_E, sigma_Z, death_frame)

PIN_UV = os.path.join(HERE, "..", "remo-pc-twin-laws-20261117",
                      "data", "pc_uv8000.json")
PIN_P = os.path.join(HERE, "..", "remo-pc-twin-laws-20261117",
                     "data", "pc_p8000.json")
PIN_UV_SHA = "8a3b318bd26b8197c66fd55d79007654d2926a18af165132af8c194bc76d8ae2"
PIN_P_SHA = "58a414bc31fb6266cc2d0e10000436e50f396135847bab5a32163cffff0b975e"
P_PIN_1_40 = [0, 1, 1, 3, 1, 5, 1, 5, 5, 9, 1, 11, 1, 5, 7, 15, 1, 17, 1, 15,
              17, 21, 1, 21, 11, 15, 7, 27, 1, 29, 1, 27, 17, 21, 11, 35, 1,
              5, 7, 39]  # P(1)..P(40), committed pin (K0919/K0929)

M_BIG = 8000        # DEATH / FULLREPRO / P2OBS range (committed pins)
M_STRUCT = 1500     # STRUCT literal-engine range
M_ENG = 600         # fresh python engine range
EGAME_K = 50        # EGAME grid: k <= 50


# ------------- literal engines -------------------------------------------

def engine_phases(m, pot0, watch):
    """Literal positional engine (K0928 Lemma P phase rule). Returns
    (phases, survivor); phases[i] = dict(k, pot, loser, held, circle
    (ptr-frame labels BEFORE the deal), holdings (BEFORE the deal))."""
    holdings = {lab: 2 for lab in range(m)}
    active = list(range(m))
    ptr = 0
    pot = pot0
    phases = []
    while len(active) > 1:
        k = len(active)
        pre_circle = active[ptr:] + active[:ptr]
        pre_hold = [holdings[lab] for lab in pre_circle]
        q, r = divmod(pot, k)
        if q:
            for lab in active:
                holdings[lab] += q
        for i in range(r):
            holdings[active[(ptr + i) % k]] += 1
        L = (ptr + pot) % k
        loser = active[L]
        held = holdings[loser]
        phases.append({"k": k, "pot": pot, "loser": loser, "held": held,
                      "circle": pre_circle, "holdings": pre_hold})
        pot = held
        active.pop(L)
        ptr = L % len(active) if active else 0
    return phases, active[0]


def state_engine(holdings, pot):
    """Literal engine on an explicit ptr-frame state (labels 0..k-1).
    Returns the surviving label."""
    active = list(range(len(holdings)))
    hold = list(holdings)
    ptr = 0
    while len(active) > 1:
        k = len(active)
        q, r = divmod(pot, k)
        if q:
            for i in range(k):
                hold[i] += q
        for i in range(r):
            hold[(ptr + i) % k] += 1
        L = (ptr + pot) % k
        pot = hold[L]
        active.pop(L)
        hold.pop(L)
        ptr = L % len(active) if active else 0
    return active[0]


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
    U_pin, V_pin = uv["U"], uv["V"]

    # ---- DEATH (LADDER-ONLY + death dichotomy, all composite m) --------
    dth = []
    dth_n = 0
    for side in ("V", "U"):
        for m in range(1, M_BIG + 1):
            N = 2 * m + 1 if side == "V" else 2 * m + 3
            if isprime(N):
                continue
            dth_n += 1
            tr = track_gen(side, m)
            if tr["status"] != "died":
                dth.append(["status", side, m, N, tr["status"]])
                continue
            d = tr["steps"][-1]
            w, n, t, r, h = d["w"], d["n"], d["t"], d["r"], d["h"]
            if w != spf(N) - 1:
                dth.append(["w", side, m, N, w, spf(N) - 1])
            if side == "V":
                if r != h - 1 or d["held"] != w + 1:
                    dth.append(["V", side, m, N, r, h, d["held"], w])
            else:
                if r != h or d["held"] != w:
                    dth.append(["U", side, m, N, r, h, d["held"], w])
    put("DEATH", not dth, n=dth_n,
        extra={"fails": dth[:10], "fail_count": len(dth)})

    # ---- FULLREPRO (all 16000 values: arithmetic vs pins) --------------
    rep = []
    rep_n = 0
    for side in ("V", "U"):
        for m in range(1, M_BIG + 1):
            rep_n += 1
            val = predict(side, m)
            pin = V_pin[m - 1] if side == "V" else U_pin[m - 1]
            if val != pin:
                rep.append([side, m, val, pin])
    put("FULLREPRO", not rep, n=rep_n,
        extra={"fails": rep[:10], "fail_count": len(rep)})

    # ---- STRUCT (literal engine vs THM-B/C/D, composite m <= 1500) -----
    struct = []
    struct_n = 0
    for side in ("V", "U"):
        pot0 = 1 if side == "V" else 2
        watch = 0 if side == "V" else None
        for m in range(1, M_STRUCT + 1):
            N = 2 * m + 1 if side == "V" else 2 * m + 3
            if isprime(N):
                continue
            struct_n += 1
            if watch is None:
                watch = m - 1
            val, info = predict_composite(side, m)
            if val is None:
                struct.append(["nodied", side, m, N, info["status"]])
                continue
            death = info["death"]
            w_d = death["w"]
            phases, survivor = engine_phases(m, pot0, watch)
            di = next(i for i, p in enumerate(phases)
                      if p["loser"] == watch)
            if side == "V":
                bj = di + 1
            else:
                bj = di + 1
                while bj < len(phases) and phases[bj]["pot"] <= w_d:
                    bj += 1
            tr = track_gen(side, m)
            frame, entry = death_frame(side, m, tr["steps"],
                                      tr["steps"][-1])
            if bj < len(phases):
                rec = phases[bj]
                eng_circle = rec["circle"]
                eng_hold = rec["holdings"]
                eng_pot = rec["pot"]
            else:
                eng_circle = [survivor]
                eng_hold = None
                eng_pot = None
            if eng_circle != frame:
                struct.append(["frame", side, m, len(eng_circle),
                               len(frame)])
            if entry[0] == "Z":
                _, M, K = entry
                if eng_hold is not None and any(x != M
                                                for x in eng_hold):
                    struct.append(["Zhold", side, m, M,
                                   eng_hold[:12]])
                if eng_pot is not None and eng_pot != M:
                    struct.append(["Zpot", side, m, M, eng_pot])
                if len(frame) != K:
                    struct.append(["Zlen", side, m, K, len(frame)])
            else:
                _, P, al, be = entry
                want = [P] * al + [P + 1] * be
                if eng_hold is not None and eng_hold != want:
                    struct.append(["Ehold", side, m, (P, al, be),
                                   eng_hold[:14]])
                if eng_pot is not None and eng_pot != P:
                    struct.append(["Epot", side, m, P, eng_pot])
            if survivor != frame[info["sigma"]]:
                struct.append(["surv", side, m, survivor,
                               frame[info["sigma"]], info["sigma"]])
    put("STRUCT", not struct, n=struct_n,
        extra={"fails": struct[:10], "fail_count": len(struct)})

    # ---- EGAME (general E / uniform states vs sigma) -------------------
    eg = []
    eg_n = 0
    for P in (3, 7, 12, 25, 60, 120):
        for k in range(2, EGAME_K + 1):
            for alpha in range(0, k + 1):
                beta = k - alpha
                eg_n += 1
                hold = [P] * alpha + [P + 1] * beta
                surv = state_engine(hold, P)
                if surv != sigma_E(P, alpha, beta):
                    eg.append(["E", P, alpha, beta, surv,
                               sigma_E(P, alpha, beta)])
    for M in (2, 3, 5, 9, 20, 47):
        for K in range(1, EGAME_K + 1):
            eg_n += 1
            hold = [M] * K
            surv = state_engine(hold, M)
            if surv != sigma_Z(M, K):
                eg.append(["Z", M, K, surv, sigma_Z(M, K)])
    put("EGAME", not eg, n=eg_n,
        extra={"fails": eg[:10], "fail_count": len(eg)})

    # ---- ENGINE (fresh python engine, m <= M_ENG, exact survivor) ------
    eng = []
    eng_n = 0
    for side in ("V", "U"):
        pot0 = 1 if side == "V" else 2
        for m in range(1, M_ENG + 1):
            watch = 0 if side == "V" else m - 1
            eng_n += 1
            rec = play_full(m, pot0, watch)
            if rec["survivor"] != predict(side, m):
                eng.append([side, m, rec["survivor"], predict(side, m)])
    put("ENGINE", not eng, n=eng_n,
        extra={"fails": eng[:10], "fail_count": len(eng)})

    # ---- P2OBS (N = p^2 observations) -----------------------------------
    p2 = []
    col = 0
    p2u = 0
    p2v = 0
    for side in ("V", "U"):
        for m in range(1, M_BIG + 1):
            N = 2 * m + 1 if side == "V" else 2 * m + 3
            if isprime(N):
                continue
            tr = track_gen(side, m)
            d = tr["steps"][-1]
            t, r, h, n = d["t"], d["r"], d["h"], d["n"]
            isp2 = (N == spf(N) ** 2)
            if side == "U":
                if t == 1 and h == 0 and r == 0:
                    col += 1
                    if not isp2:
                        p2.append(["col-not-p2", m, N])
                if isp2:
                    p2u += 1
                    if not (t == 1 and h == 0 and r == 0):
                        p2.append(["p2-not-col", m, N, (t, h, r)])
            else:
                if isp2:
                    p2v += 1
                    if (n, t, r, h) != (spf(N), 1, 0, 1):
                        p2.append(["Vp2", m, N, (n, t, r, h)])
    put("P2OBS", not p2,
        extra={"collapse_deaths": col, "u_p2_games": p2u,
               "v_p2_games": p2v,
               "fails": p2[:10], "fail_count": len(p2)})

    return {"all_ok": ok_all, "checks": res}


def main():
    res1 = run_checks()
    res2 = run_checks()
    same = json.dumps(res1, sort_keys=True) == json.dumps(res2,
                                                         sort_keys=True)
    print(json.dumps({"all_ok": bool(res1["all_ok"] and res2["all_ok"]
                                     and same),
                      "deterministic": same,
                      "checks": {k: v["ok"] for k, v in
                                 res1["checks"].items()}},
                     sort_keys=True))
    sys.exit(0 if (res1["all_ok"] and res2["all_ok"] and same) else 1)


if __name__ == "__main__":
    main()
