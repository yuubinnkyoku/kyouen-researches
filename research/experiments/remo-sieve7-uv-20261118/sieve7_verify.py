#!/usr/bin/env python3
"""Machine anchor for K0936 (SIEVE7-U/V: stretch-5/6 watched tracking by
composition, the spf = 7 instance of the SIEVE structure, and the twin
laws on all 57 + 57 classes mod 210).

Composition of PUBLISHED universal theorems only:
  K0931 STR2-U/V (stretch-2), K0933 S3/S4 (stretch-3/4 start states and
  death tables), K0934 LAD-GEN (universal first-stretch-w law + end-state
  census + watched criterion (e)), K0935 WATCH-MAP (surviving watched
  position across the stretch boundary). The LAD-GEN core below is copied
  verbatim from the published K0934/K0935 verifiers; the play() engine
  follows the K0928 Lemma P phase rule exactly as in the published
  K0932/K0933 verifiers.

The uniform tracker starts at F(2,1;m-1) (V) resp. F(2,0;m) (U) with the
watched at distance a=1 and iterates LAD-GEN + WATCH-MAP through
stretch-6 by pure arithmetic on (w, h, n, a) - no simulation.

Checks:
  PIN        committed K0929 tables (sha256, format, P(1..40) anchor)
  REDRECON   committed U/V tables vs committed P table via proved RED
             (m <= 3999, i.e. every C <= 8000 covered by the P table)
  FRESHPIN   fresh survivors == committed U/V tables (m = 1..700)
  CANON      engine stretch-entry states (pots 2..6, first occurrence)
             are exactly the canonical F(w,h;n) circles predicted by the
             tracker: n, holdings [w]^(n-h)+[w+1]^h, watched at n-a,
             run length (m = 60..700)
  TRK        tracker death/survival == engine, incl. held, phase within
             the stretch and death pot (m = 60..700)
  S3REG      tracker stretch-4 entry == published K0933 S3 closed forms
             (s5u_case / s5v_case) (m = 60..700)
  K935TBL    tracker stretch-5 entry == published K0935 w=4 tables
             (a2 / h2 / n2 as functions of h4, r4) (m = 60..700, domain)
  SV7EDGE    finite exhaustive region 3 <= m < 60 (both sides, domain
             classes): no stretch-5 death, stretch-6 death
             <=> 7 | (2m+s) and 2m+s > 7, held 7 (V) / 6 (U);
             non-domain m die at stretch 2 or 4 (SIEVE3/SIEVE5 regression)
  SV7        composition region m = 60..700 (domain classes): tracker
             valid through stretch-6, no stretch-5 death, stretch-6
             death <=> 7 | (2m+s) (automatically composite there), hot
             (V, held 7) / cold (U, held 6) death, phase = n3 // 7
  CLASS      the 32-row class table (side x m mod 30 domain classes):
             affine forms n4 = 15j+c4, n2 = 12j+c2, n3 = 10j+c3,
             t5 = 2j+e5, per-class constants (h4, r4, h2, a2, r5, h3, a3)
             consistent with the K0935 tables, exactly one death residue
             j = rho (mod 7) equal to the residue of 7 | 2(30j+c)+s, and
             engine agreement for every j in 2..16
  TWIN210    committed P table C <= 8000: LAW1 (odd C, 3 or 5 or 7 | C):
             P(C) = 1 <=> C prime; LAW2 (even C, 3 or 5 or 7 | C+1):
             P(C) = C-1 <=> C+1 prime; 57 + 57 residue classes mod 210,
             of which 8 + 8 are new for spf = 7
  SIEVEOBS   machine observation (NOT part of the theorem): m = 1..700,
             the watched dies at pot spf(2m+s)-1 holding spf (V) /
             spf-1 (U) iff 2m+s composite, survives (is the survivor)
             iff 2m+s prime; every watched death pot is even

All stdlib, deterministic. Run from the experiment directory:
    python3 sieve7_verify.py
Exit status 0 iff every check passes.

The SIEVE7 statement for m >= 60 is PROVED by composition (each stretch
step is a published universal theorem; the per-class arithmetic is the
CLASS table, every row machine-verified against the tracker and the
engine). The region 3 <= m < 60 is covered by the exhaustive finite check
SV7EDGE. The spf >= 11 part of SIEVE remains a CONJECTURE; SIEVEOBS is
observation only.
"""

import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PIN_UV = os.path.join(HERE, "..", "remo-pc-twin-laws-20261117",
                      "data", "pc_uv8000.json")
PIN_P = os.path.join(HERE, "..", "remo-pc-twin-laws-20261117",
                     "data", "pc_p8000.json")
PIN_UV_SHA = "8a3b318bd26b8197c66fd55d79007654d2926a18af165132af8c194bc76d8ae2"
PIN_P_SHA = "58a414bc31fb6266cc2d0e10000436e50f396135847bab5a32163cffff0b975e"
P_PIN_1_40 = [0, 1, 1, 3, 1, 5, 1, 5, 5, 9, 1, 11, 1, 5, 7, 15, 1, 17, 1, 15,
              17, 21, 1, 21, 11, 15, 7, 27, 1, 29, 1, 27, 17, 21, 11, 35, 1,
              5, 7, 39]  # P(1)..P(40), committed pin (K0919/K0929)

M0 = 60          # composition region: m >= M0 <=> j >= 2 in every class
M_FRESH = 700    # fresh simulation range
J_HI = 16        # class-table range: m = 30j + c <= 509 <= M_FRESH


def spf(n):
    if n < 2:
        return n
    d = 2
    while d * d <= n:
        if n % d == 0:
            return d
        d += 1
    return n


def isprime(n):
    return n >= 2 and spf(n) == n


# ------------- LAD-GEN core: verbatim from the published K0934/K0935 ----
# (research/experiments/ladder-gen-20261118/ladder_gen_verify.py,
#  research/experiments/watchmap-20261118/watchmap_verify.py)

def ladder_gen(w, h, n):
    t, r = divmod(n, w + 1)
    if t < 1 or h > w:
        return None
    J = t if r >= h else t - 1
    collapse = (t == 1 and r == 0 and h == 0)
    exp_len = 2 if collapse else ((t + 1) if r >= h else t)
    blocks = []
    eliminated = set()
    for j in range(1, J + 1):
        deal = [p for p in range((j - 1) * (w + 1), j * (w + 1) - 1)
                if p not in eliminated]
        blocks.append({"deal": deal, "loser": j * (w + 1) - 1, "held": w})
        eliminated.add(j * (w + 1) - 1)
    if collapse:
        break_phase = {"ptr": 0, "deal": None, "loser": 0, "held": w + 2,
                       "q": 1}
        loser = 0
        n2 = h2 = None
    elif r < h:
        deal = [p for p in range(n - r - w - 1, n - r - 1) if p not in eliminated]
        break_phase = {"ptr": n - r - w - 1, "deal": deal,
                       "loser": n - r - 1, "held": w + 1, "q": 0}
        loser = n - r - 1
        n2 = n - t
        h2 = h - 1 - r
    else:
        deal = [p for p in range(n - r, n)] + \
               [p for p in range(0, w - r) if p not in eliminated]
        bl = w - r if r >= 1 else w + 1
        break_phase = {"ptr": n - r, "deal": deal, "loser": bl,
                       "held": w + 1, "q": 0}
        loser = bl
        n2 = n - t - 1
        h2 = h + w - r
    elim = [b["loser"] for b in blocks] + [loser]
    return {"t": t, "r": r, "J": J, "exp_len": exp_len, "blocks": blocks,
            "break_phase": break_phase, "n2": n2, "h2": h2,
            "collapse": collapse, "elim": elim}


def watch_dies(w, h, n, a):
    g = ladder_gen(w, h, n)
    if g is None or n < 2 * w + 2 or not (1 <= a <= w + 1):
        return None
    t, r = g["t"], g["r"]
    exception = (h == 0 and r == 0 and t == 2 and a == w + 1)
    if exception:
        return {"dies": True, "phase": t + 1, "held": w + 1}
    if a == r + 1:
        return {"dies": True, "phase": t,
                "held": w if a >= h + 1 else w + 1}
    return {"dies": False, "phase": None, "held": None}


def watchmap(w, h, n, a):
    g = ladder_gen(w, h, n)
    if g is None or g["collapse"] or n < 2 * w + 2 or not (1 <= a <= w + 1):
        return None
    wd = watch_dies(w, h, n, a)
    if wd is None or wd["dies"]:
        return None
    t, r = g["t"], g["r"]
    n2 = g["n2"]
    if r < h:
        return (n2 - r + a) if a <= r else (a - r - 1)
    if r == 0:            # h = 0, t >= 2 (collapse excluded above)
        return w + a - 1  # a <= w; a = w+1 is the dead exception
    return (a + w - r) if a <= r else (a + w - r - 1)


# ------------- U/V game engine (K0928 Lemma P phase rule) --------------
# Same rule as the published K0932/K0933 play(): deal pot stones one each
# from ptr, loser = active[(ptr+pot) % k] (post-deal), the loser's
# post-deal holding becomes the new pot, ptr = loser's slot after removal.

def play_full(m, pot0, watch):
    """Play U(m) (pot0=2, watch=m-1) or V(m) (pot0=1, watch=0).

    Returns {"survivor", "death", "stretches"} where stretches is the list
    of maximal constant-pot runs, each recorded BEFORE its first phase:
    {"pot", "n", "holdings" (ptr-frame circle), "wpos", "phases"}, and
    death is None or {"pot", "held", "phase"} for the FIRST phase whose
    loser is the watched label ("phase" = 1-based index within its run).
    """
    holdings = [2] * m
    active = list(range(m))
    ptr = 0
    pot = pot0
    prev_pot = None
    stretches = []
    death = None
    while len(active) > 1:
        k = len(active)
        if pot != prev_pot:
            circle = active[ptr:] + active[:ptr]
            stretches.append({
                "pot": pot, "n": k,
                "holdings": [holdings[lab] for lab in circle],
                "wpos": circle.index(watch) if watch in circle else None,
                "phases": 0})
            prev_pot = pot
        cur = stretches[-1]
        cur["phases"] += 1
        q, r = divmod(pot, k)
        if q:
            for lab in active:
                holdings[lab] += q
        for i in range(r):
            holdings[active[(ptr + i) % k]] += 1
        L = (ptr + pot) % k
        loser = active[L]
        held = holdings[loser]
        if loser == watch and death is None:
            death = {"pot": pot, "held": held, "phase": cur["phases"]}
        pot = held
        active.pop(L)
        ptr = L % len(active) if active else 0
    return {"survivor": active[0] if active else watch,
            "stretches": stretches, "death": death}


# ------------- uniform tracker (composition of published theorems) ------

def death_info(w, h, n, a, g):
    """LAD-GEN (d): elimination-set membership of the watched position."""
    pos = n - a
    if not (0 <= pos < n):
        return "invalid", None
    if pos in g["elim"]:
        phase = g["elim"].index(pos) + 1
        if g["collapse"]:
            held = w + 2
        elif pos in [b["loser"] for b in g["blocks"]]:
            held = w
        else:
            held = w + 1
        return "dies", {"phase": phase, "held": held}
    return "alive", None


def track(side, m, max_w=6):
    """Pure-arithmetic trajectory of the watched through stretches 2..6.

    V: starts at F(2,1;m-1), watched at a=1 (the state after the single
    pot-1 phase). U: starts at F(2,0;m), watched at a=1.
    Each step applies LAD-GEN (elim-set test, cross-checked against the
    published monitor criterion (e) wherever it applies) and, on survival,
    WATCH-MAP. Returns {"steps", "status"}: "died", "survived" (through
    stretch max_w) or a domain-exit string.
    """
    if side == "V":
        w, h, n, a = 2, 1, m - 1, 1
    else:
        w, h, n, a = 2, 0, m, 1
    steps = []
    while True:
        g = ladder_gen(w, h, n)
        if g is None:
            return {"steps": steps, "status": "ladgen_none(w=%d)" % w}
        st, dinf = death_info(w, h, n, a, g)
        wd = watch_dies(w, h, n, a)
        if wd is not None and wd["dies"] != (st == "dies"):
            return {"steps": steps, "status": "monitor_mismatch(w=%d)" % w}
        if st == "dies" and wd is not None and \
                (wd["phase"] != dinf["phase"] or wd["held"] != dinf["held"]):
            return {"steps": steps,
                    "status": "monitor_detail_mismatch(w=%d)" % w}
        step = {"w": w, "h": h, "n": n, "a": a, "t": g["t"], "r": g["r"],
                "exp_len": g["exp_len"], "died": st == "dies"}
        if st == "dies":
            step["phase"] = dinf["phase"]
            step["held"] = dinf["held"]
            steps.append(step)
            return {"steps": steps, "status": "died"}
        if w >= max_w:
            steps.append(step)
            return {"steps": steps, "status": "survived"}
        if g["collapse"]:
            steps.append(step)
            return {"steps": steps, "status": "collapse_exit(w=%d)" % w}
        a2 = watchmap(w, h, n, a)
        if a2 is None:
            steps.append(step)
            return {"steps": steps, "status": "no_watchmap(w=%d)" % w}
        step["n2"], step["h2"], step["a2"] = g["n2"], g["h2"], a2
        steps.append(step)
        w, h, n, a = w + 1, g["h2"], g["n2"], a2


# ------------- published closed forms (K0933) for regression ------------

def s5u_case(m):
    """(sub, n4, wpos, h) for m % 3 != 0 (U side, stretch-4 start)."""
    if m % 3 == 1:
        q = (m - 1) // 3
        if q % 2 == 0:
            k = q // 2
            return (1, 3 * k, 3 * k - 1, 0)
        k = (q - 1) // 2
        return (2, 3 * k + 1, 3 * k - 2, 2)
    q = (m - 2) // 3
    if q % 2 == 0:
        k = q // 2
        return (3, 3 * k, 3 * k - 3, 2)
    k = (q - 1) // 2
    return (4, 3 * k + 2, 3 * k + 1, 0)


def s5v_case(m):
    """(sub, n4, wpos, h) for m % 3 != 1 (V side, stretch-4 start)."""
    if m % 3 == 0:
        q = m // 3
        if q % 2 == 1:
            k = (q - 1) // 2
            return (1, 3 * k, 3 * k - 3, 3)
        k = q // 2 - 1
        return (2, 3 * k + 2, 3 * k + 1, 1)
    q = (m - 2) // 3
    if q % 2 == 0:
        k = q // 2
        return (3, 3 * k, 3 * k - 1, 1)
    k = (q - 1) // 2
    return (4, 3 * k + 1, 3 * k - 2, 3)


# K0935 published w=4 tables (stretch-5 entry from the stretch-4 start):
# family h4 -> a2 given r4 = n4 mod 5 (death residues absent), then h2.
K935_A2 = {0: {1: 4, 2: 3, 3: 2, 4: 1},        # W4 / F(4,1): a2 = 5 - r
           1: {1: 4, 2: 3, 3: 2, 4: 1},
           2: {0: 2, 1: 1, 3: 4, 4: 3},        # F(4,2) / F(4,3)
           3: {0: 2, 1: 1, 3: 4, 4: 3}}


def k935_h2(h4, r4):
    if h4 == 0:
        return 4 - r4
    if h4 == 1:
        return 5 - r4
    if h4 == 2:
        return 1 - r4 if r4 <= 1 else 6 - r4
    return 2 - r4 if r4 <= 1 else 7 - r4


def in_domain(side, m):
    """Watched survives stretch-2 and stretch-4 (SIEVE3/SIEVE5 classes)."""
    if side == "V":
        return m % 3 != 1 and m % 5 != 2
    return m % 3 != 0 and m % 5 != 1


def side_params(side):
    """(pot0, watch label, offset s with N = 2m + s)."""
    if side == "V":
        return 1, 0, 1
    return 2, None, 3  # watch label = m - 1


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

    # ---- fresh simulations + inline CANON/TRK (compact storage) ----
    recs = {}          # (side, m) -> compact engine record
    canon_fails, trk_fails = [], []
    canon_n = trk_n = 0
    for side in ("U", "V"):
        pot0, _, s = side_params(side)
        for m in range(1, M_FRESH + 1):
            watch = m - 1 if side == "U" else 0
            rec = play_full(m, pot0, watch)
            compact = {
                "survivor": rec["survivor"],
                "death": None if rec["death"] is None else
                [rec["death"]["pot"], rec["death"]["held"],
                 rec["death"]["phase"]],
                "st": {}}
            for st in rec["stretches"]:
                if st["pot"] not in compact["st"]:
                    compact["st"][st["pot"]] = [st["n"], st["wpos"],
                                                st["phases"]]
            recs[(side, m)] = compact
            if m < M0:
                continue
            # tracker comparison (CANON + TRK)
            tr = track(side, m)
            if tr["status"] not in ("died", "survived"):
                trk_fails.append([side, m, tr["status"]])
                continue
            trk_n += 1
            eng = compact["st"]
            for step in tr["steps"]:
                w = step["w"]
                if w not in eng:
                    trk_fails.append([side, m, "no engine stretch", w])
                    continue
                n_e, wpos_e, ph_e = eng[w]
                canon_n += 1
                if n_e != step["n"]:
                    canon_fails.append([side, m, w, "n", n_e, step["n"]])
                    continue
                if wpos_e != step["n"] - step["a"]:
                    canon_fails.append([side, m, w, "wpos", wpos_e,
                                        step["n"] - step["a"]])
                    continue
                # holdings pattern (from the transient full record)
                full = next(st for st in rec["stretches"] if st["pot"] == w)
                expect_hold = [w] * (step["n"] - step["h"]) + \
                    [w + 1] * step["h"]
                if full["holdings"] != expect_hold:
                    canon_fails.append([side, m, w, "holdings"])
                    continue
                if step["died"]:
                    hot = step["held"] in (w + 1, w + 2)
                    want = step["phase"] if hot else step["exp_len"]
                else:
                    want = step["exp_len"]
                if ph_e != want:
                    trk_fails.append([side, m, w, "len", ph_e, want])
            d = compact["death"]
            if tr["status"] == "died":
                last = tr["steps"][-1]
                if not d or d[0] != last["w"] or d[1] != last["held"] or \
                        d[2] != last["phase"]:
                    trk_fails.append([side, m, "death", d,
                                      last["w"], last["held"],
                                      last["phase"]])
            else:
                if d and d[0] <= 6:
                    trk_fails.append([side, m, "late death", d[0]])
    put("CANON", not canon_fails, n=canon_n,
        extra={"fails": canon_fails[:10],
               "fail_count": len(canon_fails)})
    put("TRK", not trk_fails, n=trk_n,
        extra={"fails": trk_fails[:10], "fail_count": len(trk_fails)})

    # ---- FRESHPIN ----
    bad = 0
    for side, tab in (("U", U_pin), ("V", V_pin)):
        for m in range(1, M_FRESH + 1):
            if recs[(side, m)]["survivor"] != tab[m - 1]:
                bad += 1
    put("FRESHPIN", bad == 0, n=2 * M_FRESH, extra={"mismatches": bad})

    # ---- S3REG (tracker reproduces the published K0933 S3 closed forms) --
    fails = []
    n_chk = 0
    for side, case_fn in (("U", s5u_case), ("V", s5v_case)):
        for m in range(M0, M_FRESH + 1):
            tr = track(side, m)
            step4 = [st for st in tr["steps"] if st["w"] == 4]
            if not step4:
                continue  # died at stretch 2/3 (non-SIEVE3 classes)
            n_chk += 1
            _, n4, wpos, h4 = case_fn(m)
            st = step4[0]
            if st["n"] != n4 or st["h"] != h4 or \
                    st["n"] - st["a"] != wpos:
                fails.append([side, m, [st["n"], st["h"], st["a"]],
                              [n4, h4, n4 - wpos]])
    put("S3REG", not fails, n=n_chk,
        extra={"fails": fails[:10], "fail_count": len(fails)})

    # ---- K935TBL (tracker stretch-5 entry == published w=4 tables) ----
    fails = []
    n_chk = 0
    for side in ("U", "V"):
        for m in range(M0, M_FRESH + 1):
            if not in_domain(side, m):
                continue
            tr = track(side, m)
            steps = {st["w"]: st for st in tr["steps"]}
            if 4 not in steps or "a2" not in steps[4] or 5 not in steps:
                fails.append([side, m, "no stretch-5 entry"])
                continue
            n_chk += 1
            s4, s5e = steps[4], steps[5]
            h4, r4 = s4["h"], s4["r"]
            if r4 not in K935_A2[h4]:
                fails.append([side, m, "death residue in domain?", h4, r4])
                continue
            exp_n2 = s4["n"] - s4["t"] - (1 if r4 >= h4 else 0)
            if K935_A2[h4][r4] != s5e["a"] or \
                    k935_h2(h4, r4) != s5e["h"] or s5e["n"] != exp_n2:
                fails.append([side, m, h4, r4, s5e["a"], s5e["h"], s5e["n"]])
    put("K935TBL", not fails, n=n_chk,
        extra={"fails": fails[:10], "fail_count": len(fails)})

    # ---- SV7EDGE (finite exhaustive region 3 <= m < M0) ----
    fails = []
    n_dom = 0
    death6 = 0
    for side in ("U", "V"):
        _, _, s = side_params(side)
        for m in range(3, M0):
            N = 2 * m + s
            d = recs[(side, m)]["death"]
            if in_domain(side, m):
                n_dom += 1
                if d and d[0] == 5:
                    fails.append([side, m, "stretch-5 death"])
                    continue
                want6 = (N % 7 == 0 and N > 7)
                got6 = bool(d and d[0] == 6)
                if want6 != got6:
                    fails.append([side, m, N, d])
                    continue
                if got6:
                    death6 += 1
                    if d[1] != (7 if side == "V" else 6):
                        fails.append([side, m, "held", d[1]])
            else:
                # SIEVE3/SIEVE5 edge regression: dies at stretch 2 or 4
                if not (d and d[0] in (2, 4)):
                    fails.append([side, m, "non-domain", d])
    put("SV7EDGE", not fails, n=n_dom,
        extra={"fails": fails[:10], "fail_count": len(fails),
               "stretch6_deaths": death6})

    # ---- SV7 (composition region, domain classes) ----
    fails = []
    n_dom = 0
    death6 = surv6 = 0
    for side in ("U", "V"):
        _, _, s = side_params(side)
        for m in range(M0, M_FRESH + 1):
            if not in_domain(side, m):
                continue
            n_dom += 1
            tr = track(side, m)
            if tr["status"] not in ("died", "survived"):
                fails.append([side, m, tr["status"]])
                continue
            if any(st["died"] and st["w"] == 5 for st in tr["steps"]):
                fails.append([side, m, "stretch-5 death (tracker)"])
                continue
            want6 = (2 * m + s) % 7 == 0
            tr_died6 = (tr["status"] == "died" and
                        tr["steps"][-1]["w"] == 6)
            if want6 != tr_died6:
                fails.append([side, m, "congruence", want6, tr_died6])
                continue
            if tr_died6:
                death6 += 1
                last = tr["steps"][-1]
                if last["held"] != (7 if side == "V" else 6):
                    fails.append([side, m, "held", last["held"]])
                if side == "V" and last["a"] > last["h"]:
                    fails.append([side, m, "V death not hot"])
                if side == "U" and last["a"] <= last["h"]:
                    fails.append([side, m, "U death not cold"])
                if last["phase"] != last["n"] // 7:
                    fails.append([side, m, "phase", last["phase"],
                                  last["n"] // 7])
            else:
                surv6 += 1
                if tr["status"] == "died":
                    fails.append([side, m, "died below 6?",
                                  tr["steps"][-1]["w"]])
    put("SV7", not fails, n=n_dom,
        extra={"fails": fails[:10], "fail_count": len(fails),
               "stretch6_deaths": death6, "stretch6_survivals": surv6})

    # ---- CLASS (the 32-row table) ----
    fails = []
    rows = []
    case_names = {"U": {1: "A-I", 4: "A-II", 2: "B-III", 5: "B-IV"},
                  "V": {3: "V-A1", 0: "V-A2", 2: "V-B1", 5: "V-B2"}}
    for side in ("U", "V"):
        _, _, s = side_params(side)
        for c in range(30):
            if not in_domain(side, c):
                continue
            js = list(range(2, J_HI + 1))
            feats = {}
            aborted = False
            for j in js:
                m = 30 * j + c
                tr = track(side, m)
                if tr["status"] not in ("died", "survived"):
                    fails.append([side, c, j, tr["status"]])
                    aborted = True
                    break
                steps = {st["w"]: st for st in tr["steps"]}
                if 4 not in steps or 5 not in steps or 6 not in steps:
                    fails.append([side, c, j, "missing step"])
                    aborted = True
                    break
                s4, s5e, s6 = steps[4], steps[5], steps[6]
                if s4["died"] or s5e["died"]:
                    fails.append([side, c, j, "early death in domain"])
                    aborted = True
                    break
                d6 = (tr["status"] == "died")
                last = tr["steps"][-1]
                feats[j] = {
                    "n4": s4["n"], "h4": s4["h"], "r4": s4["r"],
                    "n2": s5e["n"], "h2": s5e["h"], "a2": s5e["a"],
                    "r5": s5e["r"], "t5": s5e["t"],
                    "n3": s6["n"], "h3": s6["h"], "a3": s6["a"],
                    "died6": d6,
                    "held": last["held"] if d6 else None,
                    "phase": last["phase"] if d6 else None}
            if aborted:
                continue

            def fit(key, slope):
                c0 = feats[2][key] - slope * 2
                for j in js:
                    if feats[j][key] != slope * j + c0:
                        return None
                return c0
            c4 = fit("n4", 15)
            c2 = fit("n2", 12)
            c3 = fit("n3", 10)
            e5 = fit("t5", 2)
            if c4 is None or c2 is None or c3 is None or e5 is None:
                fails.append([side, c, "affine"])
                continue
            consts = {}
            bad_const = False
            for key in ("h4", "r4", "h2", "a2", "r5", "h3", "a3"):
                vals = {feats[j][key] for j in js}
                if len(vals) != 1:
                    fails.append([side, c, "const", key, sorted(vals)])
                    bad_const = True
                    break
                consts[key] = vals.pop()
            if bad_const:
                continue
            # invariants tying the row to the published tables
            if consts["r4"] != c4 % 5 or consts["r5"] != c2 % 6:
                fails.append([side, c, "residue invariants", consts])
                continue
            if consts["r4"] not in K935_A2[consts["h4"]] or \
                    K935_A2[consts["h4"]][consts["r4"]] != consts["a2"] or \
                    k935_h2(consts["h4"], consts["r4"]) != consts["h2"]:
                fails.append([side, c, "k935 mismatch", consts])
                continue
            if not (1 <= consts["a2"] <= 6 and 1 <= consts["a3"] <= 7):
                fails.append([side, c, "watch range", consts])
                continue
            if side == "V" and consts["a3"] > consts["h3"]:
                fails.append([side, c, "V death not hot (class)", consts])
                continue
            if side == "U" and consts["a3"] <= consts["h3"]:
                fails.append([side, c, "U death not cold (class)", consts])
                continue
            # death residue mod 7
            dset = {j for j in js if feats[j]["died6"]}
            rho_set = {j % 7 for j in dset}
            if len(rho_set) > 1:
                fails.append([side, c, "death residue", sorted(rho_set)])
                continue
            rho = rho_set.pop() if dset else None
            exp_rho = None
            for jj in range(7):
                if (2 * (30 * jj + c) + s) % 7 == 0:
                    exp_rho = jj
                    break
            if rho != exp_rho or (dset !=
                                  {j for j in js if j % 7 == rho}):
                fails.append([side, c, "rho", rho, exp_rho, sorted(dset)])
                continue
            helds = {feats[j]["held"] for j in dset}
            if len(helds) != 1 or helds != {7 if side == "V" else 6}:
                fails.append([side, c, "held", sorted(helds)])
                continue
            # engine agreement for every j (m <= 509 <= M_FRESH)
            for j in js:
                m = 30 * j + c
                d = recs[(side, m)]["death"]
                f = feats[j]
                if f["died6"] != bool(d and d[0] == 6):
                    fails.append([side, c, j, "engine death", d])
                    break
                if f["died6"] and (d[1] != f["held"] or
                                   d[2] != f["phase"]):
                    fails.append([side, c, j, "engine detail", d,
                                  f["held"], f["phase"]])
                    break
            else:
                m6 = 30 * 2 + c
                rows.append({
                    "side": side, "c": c,
                    "case": case_names[side][m6 % 6], "m5": c % 5,
                    "n4": c4, "h4": consts["h4"], "r4": consts["r4"],
                    "n2": c2, "h2": consts["h2"], "a2": consts["a2"],
                    "r5": consts["r5"], "t5": e5,
                    "n3": c3, "h3": consts["h3"], "a3": consts["a3"],
                    "rho": rho,
                    "held": 7 if side == "V" else 6})
    expect_rows = 2 * 16
    rows.sort(key=lambda r: (r["side"], r["c"]))
    put("CLASS", not fails and len(rows) == expect_rows, n=len(rows),
        extra={"fails": fails[:10], "fail_count": len(fails),
               "expected_rows": expect_rows, "rows": rows})

    # ---- TWIN210 (twin laws on all 57 + 57 classes, committed P table) --
    law1_bad = []
    law1_res = set()
    law1_new = set()
    n1 = 0
    for C in range(3, 8001, 2):
        if C % 3 and C % 5 and C % 7:
            continue
        n1 += 1
        law1_res.add(C % 210)
        if C % 7 == 0 and C % 3 and C % 5:
            law1_new.add(C % 210)
        if (P_pin[C - 1] == 1) != isprime(C):
            law1_bad.append(C)
    law2_bad = []
    law2_res = set()
    law2_new = set()
    n2c = 0
    for C in range(2, 8001, 2):
        Cp = C + 1
        if Cp % 3 and Cp % 5 and Cp % 7:
            continue
        n2c += 1
        law2_res.add(C % 210)
        if Cp % 7 == 0 and Cp % 3 and Cp % 5:
            law2_new.add(C % 210)
        if (P_pin[C - 1] == C - 1) != isprime(Cp):
            law2_bad.append(C)
    exp_law1 = sorted(r for r in range(210)
                      if r % 2 == 1 and (r % 3 == 0 or r % 5 == 0
                                         or r % 7 == 0))
    exp_law2 = sorted(r for r in range(210)
                      if r % 2 == 0 and ((r + 1) % 3 == 0 or
                                         (r + 1) % 5 == 0 or
                                         (r + 1) % 7 == 0))
    exp_new1 = sorted(r for r in range(210)
                      if r % 2 == 1 and r % 7 == 0 and r % 3 and r % 5)
    exp_new2 = sorted((r - 1) % 210 for r in exp_new1)
    twin_ok = (not law1_bad and not law2_bad
               and sorted(law1_res) == exp_law1
               and sorted(law2_res) == exp_law2
               and len(exp_law1) == 57 and len(exp_law2) == 57
               and sorted(law1_new) == exp_new1 and len(exp_new1) == 8
               and sorted(law2_new) == exp_new2 and len(exp_new2) == 8)
    put("TWIN210", twin_ok, n=n1 + n2c,
        extra={"law1_violations": len(law1_bad),
               "law2_violations": len(law2_bad),
               "law1_classes": len(exp_law1),
               "law2_classes": len(exp_law2),
               "law1_new_classes": exp_new1,
               "law2_new_classes": exp_new2})

    # ---- SIEVEOBS (machine observation; spf >= 11 is conjecture) -------
    fails = []
    n_chk = 0
    odd_deaths = 0
    for side in ("U", "V"):
        _, _, s = side_params(side)
        watch0 = (lambda mm: mm - 1) if side == "U" else (lambda mm: 0)
        for m in range(1, M_FRESH + 1):
            N = 2 * m + s
            rec = recs[(side, m)]
            d = rec["death"]
            if d and d[0] % 2 == 1:
                odd_deaths += 1
            n_chk += 1
            if isprime(N):
                if d is not None or rec["survivor"] != watch0(m):
                    fails.append([side, m, N, d, rec["survivor"]])
            else:
                p = spf(N)
                if not d or d[0] != p - 1 or \
                        d[1] != (p if side == "V" else p - 1):
                    fails.append([side, m, N, d])
    put("SIEVEOBS", not fails and odd_deaths == 0, n=n_chk,
        extra={"fails": fails[:5], "fail_count": len(fails),
               "odd_pot_deaths": odd_deaths})

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
