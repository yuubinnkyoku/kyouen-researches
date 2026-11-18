#!/usr/bin/env python3
"""Core library for K0937 (SIEVE-COMPOSITE-GEN / INV-TRACK).

Composition of PUBLISHED universal theorems only:
  K0931 STR2-U/V, K0933 S3/S4, K0934 LAD-GEN (first-stretch-w law +
  end-state census + watched criterion), K0935 WATCH-MAP. The LAD-GEN
  core below is copied verbatim from the published K0934/K0935/K0936
  verifiers; play_full() follows the K0928 Lemma P phase rule exactly.

New in this file (machine-derived, then anchored against engines):
  stretch_sim(w,h,n,a)  positional mini-engine for ONE stretch from
                        F(w,h;n) with the watched at distance a
  watchmap_ext(w,h,n,a) WATCH-MAP extended to the t=1 regime
                        (published watchmap covers t>=2 i.e. n>=2w+2)
  death_fast(w,h,n,a)   O(1) replica of the LAD-GEN elimination-set
                        test, incl. collapse and the (0,0,2,w+1)
                        exception; unlike the K0936 death_info it
                        reports held=w for block-1 deaths of collapse
                        stretches (engine truth, see T1MAP/DEATHFAST)
  track_gen(side,m)     unbounded pure-arithmetic tracker: runs from
                        the base state through stretches w=2,3,...
                        until the watched dies, the ladder regime ends
                        (t=0 endgame) or a domain exit
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PIN_UV = os.path.join(HERE, "..", "remo-pc-twin-laws-20261117",
                      "data", "pc_uv8000.json")
PIN_P = os.path.join(HERE, "..", "remo-pc-twin-laws-20261117",
                     "data", "pc_p8000.json")


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
#  research/experiments/watchmap-20261118/watchmap_verify.py,
#  research/experiments/remo-sieve7-uv-20261118/sieve7_verify.py)

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


# ------------- new: positional mini-engine for ONE stretch --------------

def stretch_sim(w, h, n, a):
    """Simulate the single stretch-w starting from the canonical circle
    F(w,h;n) (holdings [w]^(n-h)+[w+1]^h, pot=w, ptr at position 0) with
    the watched at position n-a. Plays phases while the pot stays w.

    Returns {"n2", "holdings" (end ptr-frame circle), "a2" (or None if
    the watched died), "phases", "died": None or {"phase", "held"},
    "collapse"}. Ground truth for T1MAP/DEATHFAST (independent of
    ladder_gen: it only shares the phase rule with play_full).
    """
    hold = [w] * (n - h) + [w + 1] * h
    active = list(range(n))
    ptr = 0
    pot = w
    watch = n - a
    phases = 0
    died = None
    collapse = None
    while pot == w and len(active) > 1:
        k = len(active)
        phases += 1
        q, r = divmod(pot, k)
        if q:
            for lab in active:
                hold[lab] += q
        for i in range(r):
            hold[active[(ptr + i) % k]] += 1
        L = (ptr + pot) % k
        loser = active[L]
        held = hold[loser]
        if loser == watch and died is None:
            died = {"phase": phases, "held": held}
        pot = held
        active.pop(L)
        ptr = L % len(active) if active else 0
        if pot == w + 2 and k == 2:
            collapse = True
    n2 = len(active)
    circle = active[ptr:] + active[:ptr] if active else []
    holdings = [hold[lab] for lab in circle]
    a2 = None
    if died is None and watch in circle:
        a2 = n2 - circle.index(watch)
    return {"n2": n2, "holdings": holdings, "a2": a2, "phases": phases,
            "died": died, "collapse": collapse}


# ------------- new: O(1) death test (LAD-GEN (d) without block lists) ----

def death_fast(w, h, n, a):
    """O(1) replica of the LAD-GEN elimination-set membership test with
    phase and held, incl. collapse (block-1 deaths keep w; the collapse
    breaking loser 0 keeps w+2) and the (h,r,t,a)=(0,0,2,w+1) exception.
    Valid for every t >= 1. Returns ("dies", {...}) / ("alive", None) /
    ("invalid", None).
    """
    t, r = divmod(n, w + 1)
    if t < 1 or h > w:
        return "invalid", None
    pos = n - a
    if not (0 <= pos < n):
        return "invalid", None
    J = t if r >= h else t - 1
    collapse = (t == 1 and r == 0 and h == 0)
    # block losers: positions j*(w+1)-1, 1 <= j <= J
    if pos >= w and (pos + 1) % (w + 1) == 0:
        j = (pos + 1) // (w + 1)
        if j <= J:
            return "dies", {"phase": j, "held": w}
    if collapse:
        if pos == 0:
            return "dies", {"phase": 2, "held": w + 2}
        return "alive", None
    if r < h:
        bl = n - r - 1
    elif r >= 1:
        bl = w - r
    else:                       # r == 0, h == 0, t >= 2
        bl = w + 1
    if pos == bl:
        return "dies", {"phase": J + 1, "held": w + 1}
    return "alive", None


# ------------- new: WATCH-MAP extended to t=1 ---------------------------

def watchmap_ext(w, h, n, a):
    """Surviving watched distance across the stretch-w boundary, valid
    for every t >= 1 (non-collapse, watched alive, 1 <= a <= w+1). For
    t >= 2 identical to the published watchmap (regression-checked);
    for t = 1 the same case formulas for the INV-relevant distances
    a in {h, h+1}, anchored by stretch_sim (T1MAP). Non-INV window
    distances can deviate at t=1 (recorded as observation).
    """
    t, r = divmod(n, w + 1)
    if t < 1 or h > w:
        return None
    if t == 1 and r == 0 and h == 0:
        return None                      # collapse: no map
    if r < h:
        n2 = n - t
        return (n2 - r + a) if a <= r else (a - r - 1)
    if r == 0:                           # h == 0, t >= 2
        return w + a - 1
    n2 = n - t - 1
    return (a + w - r) if a <= r else (a + w - r - 1)


def ladder_n2h2(w, h, n):
    t, r = divmod(n, w + 1)
    if t < 1 or h > w:
        return None
    if t == 1 and r == 0 and h == 0:
        return None
    if r < h:
        return n - t, h - 1 - r
    return n - t - 1, h + w - r


# ------------- new: unbounded pure-arithmetic tracker -------------------

def track_gen(side, m, step_cap=100000):
    """Trajectory of the watched from the base state through stretches
    2, 3, ... by pure arithmetic. V: F(2,1;m-1), a=1. U: F(2,0;m), a=1.
    Stops at the watched's death, at the first t=0 stretch (endgame:
    the ladder regime ends), at a collapse survivor exit, at a window
    violation, or at step_cap (paranoia).

    Returns {"steps", "status", "T0"}; each step records
    {w, h, n, a, t, r, exp_len, died, phase?, held?, n2?, h2?, a2?}.
    """
    if side == "V":
        w, h, n, a = 2, 1, m - 1, 1
        T0 = 2 * m + 1
    else:
        w, h, n, a = 2, 0, m, 1
        T0 = 2 * m + 2
    steps = []
    while len(steps) < step_cap:
        t, r = divmod(n, w + 1)
        if t < 1 or h > w:
            return {"steps": steps, "status": "endgame(w=%d)" % w, "T0": T0}
        if not (1 <= a <= w + 1):
            return {"steps": steps, "status": "window(w=%d)" % w, "T0": T0}
        st, dinf = death_fast(w, h, n, a)
        exp_len = 2 if (t == 1 and r == 0 and h == 0) else \
            ((t + 1) if r >= h else t)
        step = {"w": w, "h": h, "n": n, "a": a, "t": t, "r": r,
                "exp_len": exp_len, "died": st == "dies"}
        if st == "dies":
            step["phase"] = dinf["phase"]
            step["held"] = dinf["held"]
            steps.append(step)
            return {"steps": steps, "status": "died", "T0": T0}
        if t == 1 and r == 0 and h == 0:
            step["n2"] = step["h2"] = None
            steps.append(step)
            return {"steps": steps, "status": "collapse_exit(w=%d)" % w,
                    "T0": T0}
        n2h2 = ladder_n2h2(w, h, n)
        a2 = watchmap_ext(w, h, n, a)
        if a2 is None or n2h2 is None:
            steps.append(step)
            return {"steps": steps, "status": "no_map(w=%d)" % w, "T0": T0}
        n2, h2 = n2h2
        step["n2"], step["h2"], step["a2"] = n2, h2, a2
        steps.append(step)
        w, h, n, a = w + 1, h2, n2, a2
    return {"steps": steps, "status": "step_cap", "T0": T0}
