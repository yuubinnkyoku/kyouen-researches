#!/usr/bin/env python3
"""Machine anchor for K0937 (SIEVE-COMPOSITE-GEN / INV-TRACK).

Universal composite-side closure of the SIEVE structure: for EVERY m and
both sides the watched's stretch-w entry state is F(w,h;n) with watched
distance a = h (V) resp. a = h + 1 (U) (invariant INV), hence the watched
dies at a stretch iff (w+1) | N.  For composite N = 2m+s the death lands
exactly at stretch spf(N)-1 (V hot, held spf; U cold, held spf-1; phase
t = n//(w+1) of that stretch).  Prime-side: the watched survives every
t >= 1 stretch; the only remaining gap is the t = 0 endgame (conjecture
SIEVE-PRIME, machine-verified here to m <= 2600 by fresh engines).

Instruments (see sievegen_core.py):
  published core (verbatim):  ladder_gen, watch_dies, watchmap, play_full
  new, anchored here:         stretch_sim (positional one-stretch engine),
                              watchmap_ext (WATCH-MAP extended to t = 1,
                              INV-relevant window), death_fast (O(1)
                              elimination test incl. collapse + exception),
                              track_gen (unbounded pure-arithmetic tracker)

Checks:
  PIN        committed K0929 tables (sha256, format, P(1..40) anchor)
  REDRECON   committed U/V tables vs committed P table via proved RED
             (m <= 3999, i.e. every C <= 8000 covered by the P table)
  T1MAP      t=1 grids (w=2..11): INV-relevant distances a in {h, h+1}
             survive with the SAME WATCH-MAP formulas (census F(w+1,h2;n2),
             a2 map, run length); all window a: death semantics, census
             and run length; collapse grids vs engine truth;
             non-INV t=1 map deviations are counted as OBSERVATION
  T2REG      t >= 2: watchmap_ext == published watchmap for every alive
             non-collapse window case (w=2..7, n <= 5(w+1))
  DEATHFAST  death_fast == LAD-GEN death_info on all non-collapse grids
             (w=2..7, n <= 5(w+1), all window a); == watch_dies verdicts
             and details wherever the published monitor applies
  INVGEN     m = 1..200000 both sides, pure-arithmetic tracker: INV
             (a = h / h+1) and the stone identity T = wn+h+w at EVERY
             stretch entry; composite N -> death at stretch spf(N)-1,
             held spf (V, hot breaking, phase = t = exp_len) resp.
             spf-1 (U, cold block, phase = t), and (w+1) | N there;
             prime N -> no tracker death (endgame exit)
  FRESHPIN   fresh engine survivors == committed U/V tables (m <= 2600)
  CANON      engine stretch-entry states (all pots, first occurrence) are
             exactly the tracker's F(w,h;n) circles: n, holdings
             [w]^(n-h)+[w+1]^h, watched at n-a, run length (m <= 2600,
             incl. t=1 stretches and the death stretch)
  TRK        tracker death == engine death (pot, held, phase); no engine
             death <=> no tracker death; prime N: engine survivor ==
             watched (endgame survival, N <= 5203) (m <= 2600)
  SV7REG     engine-level K0936 regression: m in [60,700] domain classes,
             no stretch-5 death, stretch-6 death <=> 7 | (2m+s)
  TWINCOMP   committed P table C <= 8000: every odd composite C has
             P(C) != 1 and every even C with C+1 composite has
             P(C) != C-1 (the theorem's RED-implied predictions, 0
             violations); prime-side equalities as finite observation

All stdlib, deterministic. Run from the experiment directory:
    python3 sievegen_verify.py
Exit status 0 iff every check passes.
"""

import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from sievegen_core import (  # noqa: E402
    ladder_gen, watch_dies, watchmap, play_full, stretch_sim,
    death_fast, watchmap_ext, track_gen, spf, isprime)

PIN_UV = os.path.join(HERE, "..", "remo-pc-twin-laws-20261117",
                      "data", "pc_uv8000.json")
PIN_P = os.path.join(HERE, "..", "remo-pc-twin-laws-20261117",
                     "data", "pc_p8000.json")
PIN_UV_SHA = "8a3b318bd26b8197c66fd55d79007654d2926a18af165132af8c194bc76d8ae2"
PIN_P_SHA = "58a414bc31fb6266cc2d0e10000436e50f396135847bab5a32163cffff0b975e"
P_PIN_1_40 = [0, 1, 1, 3, 1, 5, 1, 5, 5, 9, 1, 11, 1, 5, 7, 15, 1, 17, 1, 15,
              17, 21, 1, 21, 11, 15, 7, 27, 1, 29, 1, 27, 17, 21, 11, 35, 1,
              5, 7, 39]  # P(1)..P(40), committed pin (K0919/K0929)

MBIG = 200000       # INVGEN tracker range (N <= 400003, spf <= 631)
M_FRESH = 2600      # fresh engine range (N <= 5203, spf <= 71)
T1_WHI = 11         # T1MAP t=1 grid width
DF_WHI = 7          # DEATHFAST / T2REG grid width
DF_NFAC = 5         # n <= DF_NFAC*(w+1)


def spf_sieve(nmax):
    """Smallest-prime-factor table for 0..nmax."""
    tab = list(range(nmax + 1))
    for i in range(2, int(nmax ** 0.5) + 1):
        if tab[i] == i:
            for j in range(i * i, nmax + 1, i):
                if tab[j] == j:
                    tab[j] = i
    return tab


def side_params(side):
    """(pot0, watch label fn, offset s with N = 2m + s)."""
    if side == "V":
        return 1, (lambda m: 0), 1
    return 2, (lambda m: m - 1), 3


def in_domain(side, m):
    """K0936 domain (watched survives stretch-2 and stretch-4)."""
    if side == "V":
        return m % 3 != 1 and m % 5 != 2
    return m % 3 != 0 and m % 5 != 1


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

    U_pin, V_pin, P_pin = uv["U"], uv["V"], pp["P"]

    # ---- REDRECON (proved RED, K0928: P(2m+1)=1+2V, P(2m+2)=3+2U) ----
    bad = 0
    for m in range(1, 4000):
        if P_pin[2 * m + 1 - 1] != 1 + 2 * V_pin[m - 1]:
            bad += 1
        if P_pin[2 * m + 2 - 1] != 3 + 2 * U_pin[m - 1]:
            bad += 1
    put("REDRECON", bad == 0, n=2 * 3999, extra={"mismatches": bad})

    # ---- T1MAP (t=1 regime) --------------------------------------------
    fails = []
    inv_n = 0           # INV-relevant grids fully verified
    win_n = 0           # all-window grids: death/census/length
    dev_n = 0           # OBSERVATION: non-INV a2 deviations at t=1
    for w in range(2, T1_WHI + 1):
        for h in range(0, w + 1):
            for n in range(w + 1, 2 * w + 2):        # t = 1
                g = ladder_gen(w, h, n)
                if g is None:
                    continue
                for a in range(1, w + 2):
                    if a > n:
                        continue
                    st, dinf = death_fast(w, h, n, a)
                    sim = stretch_sim(w, h, n, a)
                    win_n += 1
                    # death semantics for every window a
                    if (st == "dies") != (sim["died"] is not None):
                        fails.append(["t1-death", w, h, n, a])
                        continue
                    if st == "dies":
                        if sim["died"]["phase"] != dinf["phase"] or \
                                sim["died"]["held"] != dinf["held"]:
                            fails.append(["t1-death-detail", w, h, n, a])
                        continue
                    if g["collapse"]:
                        continue
                    # census + run length for every surviving window a
                    n2e, h2e = g["n2"], g["h2"]
                    if sim["n2"] != n2e or \
                            sim["holdings"] != [w + 1] * (n2e - h2e) + \
                            [w + 2] * h2e or \
                            sim["phases"] != g["exp_len"]:
                        fails.append(["t1-census", w, h, n, a])
                        continue
                    a2f = watchmap_ext(w, h, n, a)
                    if a in (h, h + 1):
                        inv_n += 1
                        if a2f != sim["a2"]:
                            fails.append(["t1-inv-map", w, h, n, a,
                                          a2f, sim["a2"]])
                    elif a2f != sim["a2"]:
                        dev_n += 1
    # collapse grids vs engine truth (block-1 deaths keep w)
    coll_n = 0
    for w in range(2, T1_WHI + 1):
        n = w + 1
        for a in range(1, w + 2):
            st, dinf = death_fast(w, 0, n, a)
            sim = stretch_sim(w, 0, n, a)
            coll_n += 1
            ok = (st == "dies") == (sim["died"] is not None)
            if ok and st == "dies":
                ok = sim["died"]["phase"] == dinf["phase"] and \
                    sim["died"]["held"] == dinf["held"]
            if not ok:
                fails.append(["t1-collapse", w, n, a])
    put("T1MAP", not fails,
        extra={"inv_relevant_grids": inv_n, "window_grids": win_n,
               "collapse_grids": coll_n, "noninv_t1_map_deviations": dev_n,
               "fails": fails[:10], "fail_count": len(fails)})

    # ---- T2REG (t >= 2: extension == published watchmap) ----------------
    fails = []
    n_chk = 0
    for w in range(2, DF_WHI + 1):
        for h in range(0, w + 1):
            for n in range(2 * w + 2, DF_NFAC * (w + 1)):
                g = ladder_gen(w, h, n)
                if g is None or g["collapse"]:
                    continue
                for a in range(1, w + 2):
                    wd = watch_dies(w, h, n, a)
                    if wd is None or wd["dies"]:
                        continue
                    n_chk += 1
                    if watchmap_ext(w, h, n, a) != watchmap(w, h, n, a):
                        fails.append([w, h, n, a])
    put("T2REG", not fails, n=n_chk,
        extra={"fails": fails[:10], "fail_count": len(fails)})

    # ---- DEATHFAST (O(1) test == LAD-GEN elim semantics) ----------------
    fails = []
    n_chk = 0
    for w in range(2, DF_WHI + 1):
        for h in range(0, w + 1):
            for n in range(w + 1, DF_NFAC * (w + 1)):
                g = ladder_gen(w, h, n)
                if g is None or g["collapse"]:
                    continue
                for a in range(1, w + 2):
                    st, dinf = death_fast(w, h, n, a)
                    pos = n - a
                    if pos in g["elim"]:
                        exp = ("dies", {
                            "phase": g["elim"].index(pos) + 1,
                            "held": w if pos in
                            [b["loser"] for b in g["blocks"]] else w + 1})
                    else:
                        exp = ("alive", None)
                    n_chk += 1
                    if (st, dinf) != exp:
                        fails.append([w, h, n, a, [st, dinf], exp])
                        continue
                    # published monitor agreement in its window
                    wd = watch_dies(w, h, n, a)
                    if wd is not None:
                        if wd["dies"] != (st == "dies"):
                            fails.append(["wd-verdict", w, h, n, a])
                        elif st == "dies" and (wd["phase"] != dinf["phase"]
                                               or wd["held"] != dinf["held"]):
                            fails.append(["wd-detail", w, h, n, a])
    put("DEATHFAST", not fails, n=n_chk,
        extra={"fails": fails[:10], "fail_count": len(fails)})

    # ---- INVGEN (pure-arithmetic law, m <= MBIG both sides) -------------
    SPF = spf_sieve(2 * MBIG + 4)
    fails = []
    n_games = 0
    n_died = n_end = 0
    max_stretch = 0
    max_spf = 0
    n_inv_steps = 0
    for side in ("V", "U"):
        for m in range(1, MBIG + 1):
            N = 2 * m + (1 if side == "V" else 3)
            tr = track_gen(side, m)
            n_games += 1
            for stp in tr["steps"]:
                w, h, n, a = stp["w"], stp["h"], stp["n"], stp["a"]
                n_inv_steps += 1
                if side == "V":
                    if a != h:
                        fails.append(["inv", side, m, stp])
                        break
                else:
                    if a != h + 1:
                        fails.append(["inv", side, m, stp])
                        break
                if w * n + h + w != tr["T0"]:
                    fails.append(["T", side, m, stp])
                    break
            if tr["status"] == "died":
                n_died += 1
                last = tr["steps"][-1]
                p = SPF[N]
                max_spf = max(max_spf, p)
                max_stretch = max(max_stretch, last["w"])
                if p == N or last["w"] != p - 1 or \
                        last["held"] != (p if side == "V" else p - 1) or \
                        last["phase"] != last["t"] or \
                        N % (last["w"] + 1) != 0:
                    fails.append(["death-law", side, m, N, p, last])
            elif tr["status"].startswith("endgame"):
                n_end += 1
                if SPF[N] != N:
                    fails.append(["endgame-composite", side, m, N])
            else:
                fails.append(["status", side, m, tr["status"]])
    put("INVGEN", not fails, n=n_games,
        extra={"died": n_died, "endgame_exits": n_end,
               "inv_steps": n_inv_steps,
               "max_death_stretch": max_stretch,
               "max_spf": max_spf,
               "fails": fails[:10], "fail_count": len(fails)})

    # ---- fresh engines (m <= M_FRESH) + CANON / TRK / SV7REG ------------
    recs = {}
    canon_fails, trk_fails = [], []
    canon_n = trk_n = 0
    for side in ("U", "V"):
        pot0, watchf, s = side_params(side)
        for m in range(1, M_FRESH + 1):
            watch = watchf(m)
            rec = play_full(m, pot0, watch)
            st_by_pot = {}
            for st in rec["stretches"]:
                if st["pot"] not in st_by_pot:
                    st_by_pot[st["pot"]] = st
            recs[(side, m)] = {"survivor": rec["survivor"],
                               "death": rec["death"],
                               "st": st_by_pot}
            trk_n += 1
            tr = track_gen(side, m)
            # CANON: every tracker entry == engine stretch record
            for stp in tr["steps"]:
                w = stp["w"]
                if w not in st_by_pot:
                    trk_fails.append([side, m, "no engine stretch", w])
                    continue
                eng = st_by_pot[w]
                canon_n += 1
                if eng["n"] != stp["n"]:
                    canon_fails.append([side, m, w, "n", eng["n"], stp["n"]])
                    continue
                if eng["wpos"] != stp["n"] - stp["a"]:
                    canon_fails.append([side, m, w, "wpos", eng["wpos"],
                                        stp["n"] - stp["a"]])
                    continue
                exp_hold = [w] * (stp["n"] - stp["h"]) + [w + 1] * stp["h"]
                if eng["holdings"] != exp_hold:
                    canon_fails.append([side, m, w, "holdings"])
                    continue
                if stp["died"]:
                    hot = stp["held"] in (w + 1, w + 2)
                    want = stp["phase"] if hot else stp["exp_len"]
                else:
                    want = stp["exp_len"]
                if eng["phases"] != want:
                    trk_fails.append([side, m, w, "len", eng["phases"], want])
            # TRK: death agreement
            d = rec["death"]
            if tr["status"] == "died":
                last = tr["steps"][-1]
                if not d or d["pot"] != last["w"] or \
                        d["held"] != last["held"] or \
                        d["phase"] != last["phase"]:
                    trk_fails.append([side, m, "death", d,
                                      last["w"], last["held"], last["phase"]])
            else:
                if d is not None:
                    trk_fails.append([side, m, "engine-death-only", d])
                N = 2 * m + s
                if SPF[N] == N and rec["survivor"] != watch:
                    trk_fails.append([side, m, "prime-nonsurvivor",
                                      rec["survivor"]])
    put("CANON", not canon_fails, n=canon_n,
        extra={"fails": canon_fails[:10], "fail_count": len(canon_fails)})
    put("TRK", not trk_fails, n=trk_n,
        extra={"fails": trk_fails[:10], "fail_count": len(trk_fails)})

    # ---- FRESHPIN ----
    bad = 0
    for side, tab in (("U", U_pin), ("V", V_pin)):
        for m in range(1, M_FRESH + 1):
            if recs[(side, m)]["survivor"] != tab[m - 1]:
                bad += 1
    put("FRESHPIN", bad == 0, n=2 * M_FRESH, extra={"mismatches": bad})

    # ---- SIEVEOBS-GEN (engine-level spf law, m <= M_FRESH) --------------
    fails = []
    n_chk = 0
    n_comp = 0
    for side in ("U", "V"):
        _, _, s = side_params(side)
        watch0 = (lambda mm: mm - 1) if side == "U" else (lambda mm: 0)
        for m in range(1, M_FRESH + 1):
            N = 2 * m + s
            d = recs[(side, m)]["death"]
            n_chk += 1
            if SPF[N] == N:
                if d is not None or recs[(side, m)]["survivor"] != watch0(m):
                    fails.append([side, m, N, d, recs[(side, m)]["survivor"]])
            else:
                n_comp += 1
                p = SPF[N]
                if not d or d["pot"] != p - 1 or \
                        d["held"] != (p if side == "V" else p - 1):
                    fails.append([side, m, N, d])
    put("SIEVEOBSGEN", not fails, n=n_chk,
        extra={"composite_games": n_comp,
               "fails": fails[:10], "fail_count": len(fails)})

    # ---- SV7REG (K0936 regression, engine level) ------------------------
    fails = []
    n_chk = 0
    for side in ("U", "V"):
        _, _, s = side_params(side)
        for m in range(60, 701):
            if not in_domain(side, m):
                continue
            N = 2 * m + s
            d = recs[(side, m)]["death"]
            n_chk += 1
            if d is not None and d["pot"] == 5:
                fails.append(["stretch5-death", side, m])
            six = d is not None and d["pot"] == 6
            if six != (N % 7 == 0):
                fails.append(["stretch6", side, m, N, d])
    put("SV7REG", not fails, n=n_chk,
        extra={"fails": fails[:10], "fail_count": len(fails)})

    # ---- TWINCOMP (committed P table: composite directions) -------------
    law1_bad, law2_bad = [], []
    n1 = n2c = 0
    prime1_ok = prime2_ok = 0
    for C in range(3, 8001, 2):                 # odd C: LAW1 direction
        pC = SPF[C]
        if pC == C:
            if P_pin[C - 1] == 1:
                prime1_ok += 1
            continue
        n1 += 1
        if P_pin[C - 1] == 1:
            law1_bad.append(C)
    for C in range(2, 8000, 2):                 # even C: LAW2 direction
        Cp = C + 1
        if SPF[Cp] == Cp:
            if P_pin[C - 1] == C - 1:
                prime2_ok += 1
            continue
        if Cp < 9:                              # C+1 in {3,5,7} prime pins
            continue
        n2c += 1
        if P_pin[C - 1] == C - 1:
            law2_bad.append(C)
    put("TWINCOMP", not law1_bad and not law2_bad,
        n=n1 + n2c,
        extra={"law1_composites": n1, "law2_composites": n2c,
               "law1_violations": len(law1_bad),
               "law2_violations": len(law2_bad),
               "prime_obs_law1": prime1_ok, "prime_obs_law2": prime2_ok})

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
