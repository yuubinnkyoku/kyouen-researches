#!/usr/bin/env python3
"""Verifier for K0943: closed-form ladder stretch states.

Core: sievegen_core.py is the byte-identical K0937 committed core
(sha256 a69f916c86ed02d5eeed3d5494bbb0f44f652d0d1e47e4c50bbc68bef1843499):
track_gen (pure-arithmetic tracker), stretch_sim (positional one-stretch
mini-engine), play_full (full-game engine), spf/isprime.

New universal claims of K0943 (paper proofs in report.md; anchored here):

HCAP: at every ladder stretch start F(w,h;n) (w>=2, t=n//(w+1)>=1, watch
  alive) of a V/U game, 0 <= h <= w-1 (V additionally h >= 1). Hence the
  LAD-GEN watch-death exception (h,r,t,a)=(0,0,2,w+1) is unreachable in
  V/U games (it needs a=w+1: V has a=h<=w-1, U has a=h+1<=w).

STATE-CF: with T = N = 2m+1 (V) / T = N-1 = 2m+2 (U), every such stretch
  start state satisfies
      h = (T - w) mod w        (V: in [1,w-1], U: in [0,w-1])
      n = (T - w - h) // w
  i.e. the whole (w,n,t,r,h) walk is O(1) arithmetic per stretch with no
  recursion. The same formulas hold at the t=0 endgame-entrance family
  state of prime-N games.

DS-CF: for odd composite N (p=spf(N), w*=p-1) the death-stretch state is
  the STATE-CF value at w*, the death dichotomy r=h-1 (V, breaking hot
  death, held w+1) / r=h (U, block cold death, held w) follows from the
  congruence N = h-r-1+s (mod w*+1), and the K0941 Theorem-B post-death
  states conserve T exactly (arithmetic check).

P2 (upgrades K0941 P2OBS observation to a theorem):
  U-side collapse death (t,h,r)=(1,0,0)  <=>  N = spf(N)^2
  V-side death state (n,t,r,h)=(p,1,0,1)  <=>  N = p^2

Checks (all deterministic; no time/random):
  COREPIN   sievegen_core.py sha256 pin.
  CFTRACK   m <= CF_BOUND both sides: every tracker step matches the
            closed form, HCAP, watch window 1<=a<=n, INV identity
            T=w*n+h+w, a=h (V)/h+1 (U); prime-N entrance (family state,
            incl. the w=2 base-direct cases) matches the closed form.
  DEATHCF   composite subset of the same range: status died, w*=spf-1,
            dichotomy r=h-1/h, held w+1/w, death phase t, post-death
            stone totals == T (three Theorem-B forms), and the U
            ambiguity statistic (w* | N-1 games all take h*=0).
  P2        both directions of the two equivalences, with counts and the
            exact p^2 lists; bijection counts equal on both sides.
  SIMDEATH  composite m <= SIM_BOUND plus every N=p^2 game with
            m <= SIM_SQUARE_BOUND, both sides: the positional mini-engine
            stretch_sim started from the CLOSED-FORM death state
            reproduces death (phase/held), n2, and the K0941 Theorem-B
            post-death holdings circle exactly.
  ENGINE    m <= ENGINE_BOUND both sides: fresh play_full engine; every
            ladder run start (pot 2..death width / entrance width) has
            n/holdings/watch position equal to the closed-form state;
            composite deaths have pot=w*, held w+1 (V) / w (U); prime
            games end with survivor == watch.
"""

import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import sievegen_core as core  # noqa: E402

CF_BOUND = 30000
ENGINE_BOUND = 400
SIM_BOUND = 400
SIM_SQUARE_BOUND = 30000
MAX_VIOL = 40

CORE_SHA = ("a69f916c86ed02d5eeed3d5494bbb0f44f652d0d1e4714c"
            "50bbc68bef1843499")


def canon(obj):
    return json.dumps(obj, sort_keys=True, indent=1, ensure_ascii=False) + "\n"


def game_N(side, m):
    return 2 * m + 1 if side == "V" else 2 * m + 3


def game_T(side, m):
    return 2 * m + 1 if side == "V" else 2 * m + 2


def cf_h(side, m, w):
    T = game_T(side, m)
    return (T - w) % w


def cf_n(side, m, w, h):
    T = game_T(side, m)
    return (T - w - h) // w


def base_state(side, m):
    # stretch-2 start state (K0937 INV-TRACK base)
    if side == "V":
        return 2, 1, m - 1, 1
    return 2, 0, m, 1


def expected_postdeath(side, w, h, n, t):
    """K0941 Theorem-B post-death state description and stone total."""
    if side == "V":
        return {"form": "Z", "M": w + 1, "K": n - t,
                "total": (w + 1) * (n - t + 1)}
    if t == 1 and h == 0:  # collapse (then r=0)
        return {"form": "Z", "M": w + 2, "K": w - 1,
                "total": (w + 2) * w}
    alpha = n - t - 1 - w
    return {"form": "E", "P": w + 1, "alpha": alpha, "beta": w,
            "total": (w + 1) * alpha + (w + 2) * w + (w + 1)}


def run_checks():
    checks = []
    res = {"all_ok": True, "checks": checks}

    def record(name, ok, info):
        entry = {"name": name, "ok": bool(ok)}
        entry.update(info)
        checks.append(entry)
        if not ok:
            res["all_ok"] = False

    # ---------------- COREPIN ----------------
    with open(os.path.join(HERE, "sievegen_core.py"), "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    record("COREPIN", sha == CORE_SHA, {"sha256": sha})

    cf = {"games": 0, "steps": 0, "entrances": 0,
          "h_cap_viol": [], "closed_form_viol": [], "window_viol": [],
          "inv_viol": [], "entrance_viol": [], "degenerate_v1": 0,
          "status_viol": [], "h_eq_w_seen": 0}
    dth = {"games": 0, "w_viol": [], "dich_viol": [], "held_viol": [],
           "phase_viol": [], "posttotal_viol": [], "u_ambig": 0,
           "u_ambig_n_eq_w1": 0, "u_ambig_n_ge_w2": 0}
    p2 = {"u_games": 0, "v_games": 0, "u_collapse": [], "v_state": [],
          "u_squares": [], "v_squares": [], "u_viol": [], "v_viol": [],
          "u_count_match": None}
    sim = {"games": 0, "viol": [], "collapse_checked": 0,
           "square_games": 0}
    eng = {"games": 0, "runs": 0, "state_viol": [], "death_viol": [],
           "prime_survivor_viol": [], "composite_games": 0,
           "prime_games": 0}

    T_viol = cf["closed_form_viol"]

    for side in ("V", "U"):
        for m in range(1, CF_BOUND + 1):
            N = game_N(side, m)
            T = game_T(side, m)
            tr = core.track_gen(side, m)
            cf["games"] += 1
            status = tr["status"]
            if not (status == "died" or status.startswith("endgame")):
                if len(cf["status_viol"]) < MAX_VIOL:
                    cf["status_viol"].append({"side": side, "m": m,
                                              "status": status})
                continue
            # ---- per-step closed form / HCAP / window / INV ----
            for st in tr["steps"]:
                w, h, n, a = st["w"], st["h"], st["n"], st["a"]
                t, r = st["t"], st["r"]
                cf["steps"] += 1
                bad = None
                if t != n // (w + 1) or r != n % (w + 1):
                    bad = "divmod"
                if h == w:
                    cf["h_eq_w_seen"] += 1
                if not (0 <= h <= w - 1):
                    if len(cf["h_cap_viol"]) < MAX_VIOL:
                        cf["h_cap_viol"].append(
                            {"side": side, "m": m, "w": w, "h": h})
                if side == "V" and h < 1:
                    if len(cf["h_cap_viol"]) < MAX_VIOL:
                        cf["h_cap_viol"].append(
                            {"side": side, "m": m, "w": w, "h": h})
                exp_a = h if side == "V" else h + 1
                if a != exp_a or not (1 <= a <= n):
                    if len(cf["window_viol"]) < MAX_VIOL:
                        cf["window_viol"].append(
                            {"side": side, "m": m, "w": w, "h": h,
                             "a": a, "n": n})
                if T != w * n + h + w:
                    if len(cf["inv_viol"]) < MAX_VIOL:
                        cf["inv_viol"].append(
                            {"side": side, "m": m, "w": w, "h": h,
                             "n": n, "T": T})
                if bad is None:
                    hcf = cf_h(side, m, w)
                    ncf = cf_n(side, m, w, hcf)
                    if h != hcf or n != ncf:
                        if len(T_viol) < MAX_VIOL:
                            T_viol.append({"side": side, "m": m, "w": w,
                                           "h": h, "n": n, "hcf": hcf,
                                           "ncf": ncf})
            # ---- composite death checks ----
            if status == "died":
                dth["games"] += 1
                st = tr["steps"][-1]
                w, h, n = st["w"], st["h"], st["n"]
                t, r = st["t"], st["r"]
                p = core.spf(N)
                if w != p - 1:
                    if len(dth["w_viol"]) < MAX_VIOL:
                        dth["w_viol"].append({"side": side, "m": m,
                                              "w": w, "spf": p})
                dich_ok = (r == h - 1) if side == "V" else (r == h)
                if not dich_ok:
                    if len(dth["dich_viol"]) < MAX_VIOL:
                        dth["dich_viol"].append({"side": side, "m": m,
                                                 "w": w, "h": h, "r": r})
                exp_held = w + 1 if side == "V" else w
                if st["held"] != exp_held:
                    if len(dth["held_viol"]) < MAX_VIOL:
                        dth["held_viol"].append({"side": side, "m": m,
                                                 "held": st["held"],
                                                 "exp": exp_held})
                if st.get("phase") != t:
                    if len(dth["phase_viol"]) < MAX_VIOL:
                        dth["phase_viol"].append({"side": side, "m": m,
                                                  "phase": st.get("phase"),
                                                  "t": t})
                pd = expected_postdeath(side, w, h, n, t)
                if pd["total"] != T:
                    if len(dth["posttotal_viol"]) < MAX_VIOL:
                        dth["posttotal_viol"].append(
                            {"side": side, "m": m, "total": pd["total"],
                             "T": T})
                if side == "U":
                    if (N - 1) % w == 0:
                        dth["u_ambig"] += 1
                        if n == w + 1:
                            dth["u_ambig_n_eq_w1"] += 1
                        else:
                            dth["u_ambig_n_ge_w2"] += 1
                # ---- P2 ----
                square = (N == p * p)
                if side == "U":
                    p2["u_games"] += 1
                    collapse = (t == 1 and h == 0 and r == 0)
                    if collapse != square:
                        if len(p2["u_viol"]) < MAX_VIOL:
                            p2["u_viol"].append({"m": m, "N": N,
                                                 "collapse": collapse,
                                                 "square": square})
                    if collapse:
                        p2["u_collapse"].append({"m": m, "N": N, "p": p})
                    if square:
                        p2["u_squares"].append({"m": m, "N": N, "p": p})
                else:
                    p2["v_games"] += 1
                    vstate = (n == p and t == 1 and r == 0 and h == 1)
                    if vstate != square:
                        if len(p2["v_viol"]) < MAX_VIOL:
                            p2["v_viol"].append({"m": m, "N": N,
                                                 "vstate": vstate,
                                                 "square": square})
                    if vstate:
                        p2["v_state"].append({"m": m, "N": N, "p": p})
                    if square:
                        p2["v_squares"].append({"m": m, "N": N, "p": p})
            else:
                # ---- prime-N entrance (family state) closed form ----
                if tr["steps"]:
                    last = tr["steps"][-1]
                    w2, h2, n2 = last["w"] + 1, last["h2"], last["n2"]
                else:
                    _, h2, n2, _ = base_state(side, m)
                    w2 = 2
                cf["entrances"] += 1
                hcf = cf_h(side, m, w2)
                ncf = cf_n(side, m, w2, hcf)
                fam_ok = ncf in (w2 - 1, w2)
                if side == "V":
                    fam_ok = fam_ok and 1 <= hcf <= min(ncf, w2)
                else:
                    fam_ok = fam_ok and 0 <= hcf <= min(ncf - 1, w2)
                degenerate = (side == "V" and m == 1)
                if degenerate:
                    cf["degenerate_v1"] += 1
                if h2 != hcf or n2 != ncf or not (fam_ok or degenerate):
                    if len(cf["entrance_viol"]) < MAX_VIOL:
                        cf["entrance_viol"].append(
                            {"side": side, "m": m, "w2": w2, "h2": h2,
                             "n2": n2, "hcf": hcf, "ncf": ncf,
                             "fam_ok": fam_ok, "degenerate": degenerate})

    p2["u_count_match"] = (len(p2["u_collapse"]) == len(p2["u_squares"])
                           and len(p2["v_state"]) == len(p2["v_squares"])
                           and len(p2["u_collapse"]) == len(p2["v_state"]))
    # expected square list
    exp_sq = []
    p = 3
    while p * p <= 2 * CF_BOUND + 3:
        if core.isprime(p):
            exp_sq.append(p)
        p += 2
    p2["expected_p_list_len"] = len(exp_sq)

    record("CFTRACK",
           not (cf["h_cap_viol"] or cf["closed_form_viol"]
                or cf["window_viol"] or cf["inv_viol"]
                or cf["entrance_viol"] or cf["status_viol"])
           and cf["h_eq_w_seen"] == 0,
           {k: cf[k] for k in ("games", "steps", "entrances",
                               "h_cap_viol", "closed_form_viol",
                               "window_viol", "inv_viol",
                               "entrance_viol", "status_viol",
                               "degenerate_v1", "h_eq_w_seen")})
    record("DEATHCF",
           not (dth["w_viol"] or dth["dich_viol"] or dth["held_viol"]
                or dth["phase_viol"] or dth["posttotal_viol"]),
           {k: dth[k] for k in dth if not isinstance(dth[k], list)}
           | {"w_viol": dth["w_viol"], "dich_viol": dth["dich_viol"],
              "held_viol": dth["held_viol"], "phase_viol": dth["phase_viol"],
              "posttotal_viol": dth["posttotal_viol"]})
    record("P2",
           not (p2["u_viol"] or p2["v_viol"]) and p2["u_count_match"]
           and len(p2["u_squares"]) == len(exp_sq)
           and len(p2["v_squares"]) == len(exp_sq),
           {"u_viol": p2["u_viol"], "v_viol": p2["v_viol"],
            "u_collapse_count": len(p2["u_collapse"]),
            "v_state_count": len(p2["v_state"]),
            "u_square_count": len(p2["u_squares"]),
            "v_square_count": len(p2["v_squares"]),
            "expected_p_list_len": len(exp_sq),
            "count_match": p2["u_count_match"],
            "u_collapse": p2["u_collapse"], "v_state": p2["v_state"]})

    # ---------------- SIMDEATH ----------------
    sim_targets = []
    for p in exp_sq:
        # every N = p^2 game within SIM_SQUARE_BOUND (first, so these
        # are counted as square games even when also <= SIM_BOUND)
        for side in ("V", "U"):
            if side == "V":
                m = (p * p - 1) // 2
            else:
                m = (p * p - 3) // 2
            if 1 <= m <= SIM_SQUARE_BOUND:
                sim_targets.append((side, m, True))
    for side in ("V", "U"):
        for m in range(1, SIM_BOUND + 1):
            N = game_N(side, m)
            if not core.isprime(N):
                sim_targets.append((side, m, False))
    seen = set()
    for side, m, is_sq in sim_targets:
        if (side, m) in seen:
            continue
        seen.add((side, m))
        N = game_N(side, m)
        T = game_T(side, m)
        p = core.spf(N)
        w = p - 1
        h = cf_h(side, m, w)
        n = cf_n(side, m, w, h)
        a = h if side == "V" else h + 1
        t, r = divmod(n, w + 1)
        sim["games"] += 1
        if is_sq:
            sim["square_games"] += 1
        if t == 1 and h == 0 and side == "U":
            sim["collapse_checked"] += 1
        out = core.stretch_sim(w, h, n, a)
        pd = expected_postdeath(side, w, h, n, t)
        exp_phases = 2 if (t == 1 and h == 0) else \
            ((t + 1) if r >= h else t)
        ok = True
        detail = {"side": side, "m": m, "w": w, "h": h, "n": n}
        if out["died"] is None:
            ok = False
            detail["why"] = "no death"
        else:
            if out["died"]["phase"] != t:
                ok = False
                detail["why"] = "phase"
            exp_held = w + 1 if side == "V" else w
            if out["died"]["held"] != exp_held:
                ok = False
                detail["why"] = "held"
        if pd["form"] == "Z":
            exp_hold = [pd["M"]] * pd["K"]
            if out["n2"] != pd["K"]:
                ok = False
                detail["why"] = "n2"
        else:
            exp_hold = [pd["P"]] * pd["alpha"] + [pd["P"] + 1] * pd["beta"]
            if out["n2"] != pd["alpha"] + pd["beta"]:
                ok = False
                detail["why"] = "n2"
        if out["holdings"] != exp_hold:
            ok = False
            detail["why"] = "holdings"
        if out["phases"] != exp_phases:
            ok = False
            detail["why"] = "phases"
        if not ok and len(sim["viol"]) < MAX_VIOL:
            sim["viol"].append(detail)
    record("SIMDEATH", not sim["viol"],
           {k: sim[k] for k in ("games", "square_games",
                                "collapse_checked", "viol")})

    # ---------------- ENGINE ----------------
    for side in ("V", "U"):
        for m in range(1, ENGINE_BOUND + 1):
            N = game_N(side, m)
            T = game_T(side, m)
            pot0 = 1 if side == "V" else 2
            watch = 0 if side == "V" else m - 1
            g = core.play_full(m, pot0, watch)
            tr = core.track_gen(side, m)
            eng["games"] += 1
            if core.isprime(N):
                eng["prime_games"] += 1
                if g["survivor"] != watch:
                    if len(eng["prime_survivor_viol"]) < MAX_VIOL:
                        eng["prime_survivor_viol"].append(
                            {"side": side, "m": m,
                             "survivor": g["survivor"]})
                w_lim = int(tr["status"].split("w=")[1].rstrip(")"))
            else:
                eng["composite_games"] += 1
                if g["death"] is None:
                    if len(eng["death_viol"]) < MAX_VIOL:
                        eng["death_viol"].append(
                            {"side": side, "m": m, "why": "no death"})
                    continue
                w_lim = tr["steps"][-1]["w"]
                exp_held = w_lim + 1 if side == "V" else w_lim
                if g["death"]["pot"] != w_lim or \
                        g["death"]["held"] != exp_held:
                    if len(eng["death_viol"]) < MAX_VIOL:
                        eng["death_viol"].append(
                            {"side": side, "m": m, "death": g["death"],
                             "w": w_lim, "exp_held": exp_held})
            for run in g["stretches"]:
                w = run["pot"]
                if w < 2 or w > w_lim:
                    continue
                eng["runs"] += 1
                h = cf_h(side, m, w)
                n = cf_n(side, m, w, h)
                a = h if side == "V" else h + 1
                exp_hold = [w] * (n - h) + [w + 1] * h
                ok = (run["n"] == n and run["holdings"] == exp_hold
                      and run["wpos"] == n - a)
                if not ok and len(eng["state_viol"]) < MAX_VIOL:
                    eng["state_viol"].append(
                        {"side": side, "m": m, "w": w, "n": run["n"],
                         "ncf": n, "hcf": h, "wpos": run["wpos"]})
    record("ENGINE",
           not (eng["state_viol"] or eng["death_viol"]
                or eng["prime_survivor_viol"]),
           {k: eng[k] for k in eng})

    res["bounds"] = {"CF_BOUND": CF_BOUND, "ENGINE_BOUND": ENGINE_BOUND,
                     "SIM_BOUND": SIM_BOUND,
                     "SIM_SQUARE_BOUND": SIM_SQUARE_BOUND}
    return res


def main():
    r1 = run_checks()
    r2 = run_checks()
    if canon(r1) != canon(r2):
        print("FATAL: nondeterministic run_checks", file=sys.stderr)
        sys.exit(1)
    sys.stdout.write(canon(r1))


if __name__ == "__main__":
    main()
