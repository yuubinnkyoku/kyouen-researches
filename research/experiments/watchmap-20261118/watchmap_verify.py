#!/usr/bin/env python3
"""Machine anchor for K0935 (WATCH-MAP: where a surviving watched position
lands in the next ladder state, and the death prediction it gives).

The LAD-GEN core (simulator + first-stretch closed forms) is copied
verbatim from the published K0934 verifier
(research/experiments/ladder-gen-20261118/ladder_gen_verify.py); the new
content is the watchmap() closed form and the WM1/WM2 checks below, PROVED
in report.md (segment bookkeeping on the LAD-GEN end-state census).

  WM1  watched map: for every F(w,h;n) with n >= 2w+2, 1 <= a <= w+1, if
       the watched position n-a survives the first stretch (per the proved
       LAD-GEN criterion (e), exception included), then its index in the
       end circle (the new ptr frame) is exactly n2 - a2 with
         r < h        : a <= r  ->  a2 = n2 - r + a     (front segment)
                        a >= r+2 ->  a2 = a - r - 1    (long segment)
         r >= h, r>=1 : a <= r  ->  a2 = a + w - r     (cold prefix)
                        a >= r+2 ->  a2 = a + w - r - 1
         r = h = 0    : a <= w  ->  a2 = w + a - 1     (a = w+1 is the
                        dead exception of LAD-GEN (e))
       where n2, h2 are the LAD-GEN end-state parameters.
  WM2  composition (the SIEVE bookkeeping primitive): with a2 from WM1,
       the watched dies in the SECOND stretch iff the position n2 - a2 is
       in the LAD-GEN elimination set of F(w+1, h2; n2), with the phase
       and holding of that elimination. Checked against the direct
       continuation of the same simulation (stretch 2 in the circle
       frame), for every grid point where stretch 2 is in the LAD-GEN
       domain (h2 <= w+1, n2 >= w+2).

Grid: w in 2..7, h in 0..w, n in w+1..155 (as K0934). All stdlib,
deterministic. Run from the experiment directory:
    python3 watchmap_verify.py
Exit status 0 iff every check passes.
"""

import json
import sys

W_MAX = 7
N_MAX = 155

# ---------------- core: copied verbatim from K0934 ladder_gen_verify.py --

def simulate_first_stretches(w, h, n, stretches=1):
    holdings = [w] * (n - h) + [w + 1] * h
    active = list(range(n))          # labels in ptr-frame order
    ptr = 0
    pot = w
    out = []
    cur = {"phases": []}
    stretch_pot = w
    while len(active) > 1 and len(out) < stretches:
        k = len(active)
        if pot != stretch_pot:
            cur["circle"] = active[ptr:] + active[:ptr]
            cur["endhold"] = [holdings[lab] for lab in cur["circle"]]
            cur["endpot"] = pot
            out.append(cur)
            stretch_pot = pot
            cur = {"phases": []}
            continue
        q, rem = divmod(pot, k)
        if q:
            for lab in active:
                holdings[lab] += q
        dealt = []
        for i in range(rem):
            lab = active[(ptr + i) % k]
            holdings[lab] += 1
            dealt.append(lab)
        L = (ptr + pot) % k
        loser = active[L]
        held = holdings[loser]
        cur["phases"].append({"start_ptr": active[ptr % k],
                              "dealt": dealt, "loser": loser, "held": held})
        pot = held
        active.pop(L)
        ptr = L % len(active) if active else 0
    if cur["phases"]:
        cur["circle"] = active[ptr:] + active[:ptr] if active else []
        cur["endhold"] = [holdings[lab] for lab in cur["circle"]]
        cur["endpot"] = pot
        out.append(cur)
    return out


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

# ---------------- new: WATCH-MAP closed form (proved; see report.md) ----

def watchmap(w, h, n, a):
    """New a-value of a watched position n-a that SURVIVES the first
    stretch-w. Returns None if out of domain or the watched dies."""
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

# ---------------- checks ------------------------------------------------

class Ctx:
    def __init__(self):
        self.fails = []
        self.counts = {}

    def count(self, name, k=1):
        self.counts[name] = self.counts.get(name, 0) + k

    def fail(self, name, msg):
        self.fails.append(f"{name}: {msg}")


def check_game(ctx, w, h, n):
    recs = simulate_first_stretches(w, h, n, stretches=2)
    if not recs:
        return
    g = ladder_gen(w, h, n)
    if g is None or g["collapse"]:
        return
    n2, h2 = g["n2"], g["h2"]
    circle = recs[0]["circle"]
    if len(circle) != n2:
        ctx.fail("WM0", f"w={w} h={h} n={n}: circle {len(circle)} != {n2}")
        return
    w2 = w + 1
    g2 = ladder_gen(w2, h2, n2)
    for a in range(1, w + 2):
        a2 = watchmap(w, h, n, a)
        pos = n - a
        if a2 is None:
            # must be dead in stretch 1 (or out of watched domain)
            if n >= 2 * w + 2 and pos in [p["loser"] for p in recs[0]["phases"]]:
                wd = watch_dies(w, h, n, a)
                if wd is None or not wd["dies"]:
                    ctx.fail("WM1", f"w={w} h={h} n={n} a={a}: "
                              "watchmap None but watched alive")
            continue
        ctx.count("WM1")
        if pos not in circle:
            ctx.fail("WM1", f"w={w} h={h} n={n} a={a}: watched not in circle")
            return
        idx = circle.index(pos)
        if n2 - idx != a2:
            ctx.fail("WM1", f"w={w} h={h} n={n} a={a}: "
                      f"a2 {n2-idx} != closed {a2}")
            return
        # WM2: death prediction for stretch 2
        if g2 is None or len(recs) < 2:
            continue
        ctx.count("WM2")
        pos2 = n2 - a2
        if pos2 < 0 or pos2 >= n2:
            ctx.fail("WM2", f"w={w} h={h} n={n} a={a}: pos2 {pos2} invalid")
            return
        pred_dies = pos2 in g2["elim"]
        los2 = [p["loser"] for p in recs[1]["phases"]]
        # losers of stretch 2 are labels; map circle index -> label
        sim_dies = circle[pos2] in los2
        if pred_dies != sim_dies:
            ctx.fail("WM2", f"w={w} h={h} n={n} a={a}: dies2 "
                      f"{pred_dies} != sim {sim_dies}")
            return
        if pred_dies:
            pred_phase = g2["elim"].index(pos2) + 1
            sim_phase = los2.index(circle[pos2]) + 1
            if pred_phase != sim_phase:
                ctx.fail("WM2", f"w={w} h={h} n={n} a={a}: phase2 "
                          f"{pred_phase} != {sim_phase}")
                return
            exp_held = (w2 if pos2 in [b["loser"] for b in g2["blocks"]]
                        else (w2 + 2 if g2["collapse"] else w2 + 1))
            if recs[1]["phases"][sim_phase - 1]["held"] != exp_held:
                ctx.fail("WM2", f"w={w} h={h} n={n} a={a}: held2 mismatch")
                return


def run_checks():
    ctx = Ctx()
    for w in range(2, W_MAX + 1):
        for h in range(0, w + 1):
            for n in range(w + 1, N_MAX + 1):
                check_game(ctx, w, h, n)
    return {"all_ok": not ctx.fails, "fails": ctx.fails[:20],
            "fail_count": len(ctx.fails), "counts": dict(sorted(ctx.counts.items()))}


def main():
    res1 = run_checks()
    res2 = run_checks()
    same = json.dumps(res1, sort_keys=True) == json.dumps(res2, sort_keys=True)
    print(json.dumps({"all_ok": res1["all_ok"] and same,
                      "fail_count": res1["fail_count"],
                      "deterministic": same,
                      "counts": res1["counts"]}, ensure_ascii=False,
                     sort_keys=True, indent=1))
    sys.exit(0 if (res1["all_ok"] and same) else 1)


if __name__ == "__main__":
    main()
