#!/usr/bin/env python3
"""Machine anchor for K0934 (LAD-GEN: universal first-stretch-w law of the
restricted ladder F(w,h;n), including the open class h >= 2, 1 <= r < h).

The closed forms checked here are PROVED in report.md (block induction +
breaking case analysis + end-state census); this script is the machine
anchor, not the proof.

Checks (each over the full grid w in 2..7, h in 0..w, n in w+1..155, i.e.
every residue r, every family):
  LG1  first-stretch length: t+1 phases if r >= h, t phases if r < h
       (n = (w+1)t + r); collapse case (t,r,h)=(1,0,0) has 2 phases.
  LG2  cold blocks j = 1..J (J = t if r >= h else t-1): deal positions
       (j-1)(w+1)..j(w+1)-2 (all front, w -> w+1) and eliminate position
       j(w+1)-1 (cold, held w).
  LG3  breaking phase: r < h -> ptr n-r-w-1, deal n-r-w-1..n-r-2, loser
       n-r-1 (hot, w+1); r >= h -> ptr n-r, deal last r positions + wrap
       0..w-1-r, loser w-r (r >= 1) resp. w+1 (r=0, h=0), hot, w+1;
       collapse (1,0,0): phase 2 has q=1, all -> w+2, loser holds w+2.
  LG4  end state: F(w+1, h2; n2) with pot w+1 and circle exactly
       [w+1]^(n2-h2) + [w+2]^h2, where
         r < h : n2 = n-t,     h2 = h-1-r
         r >= h: n2 = n-t-1,   h2 = h+w-r
       (h2 = (h-1-r) mod (w+1)); collapse: W_{w+2}(w-1).
  LG5  elimination set of the first stretch-w = {j(w+1)-1 : j <= J} plus
       the breaking loser; watched-at-n-a criterion: for n >= 2w+2 and
       1 <= a <= w+1 the watched dies iff a = r+1 (phase t; cold iff
       a >= h+1, hot-final iff a <= h), with the single exception
       (h,r,t,a) = (0,0,2,w+1) which dies hot at phase t+1.
  LG6  regression vs K0931 LAD-h0 (h=0): end state F(w+1,w-r; wt+r-1)
       for r >= 1, F(w+1,w; wt-1) for r=0,t>=2, collapse W_{w+2}(w-1).
  LG7  regression vs K0933 S4 (w=4): the four families' death table
       (W4/F(4,1) die iff 5|n, F(4,2)/F(4,3) die iff n=2 mod 5; cold /
       hot-final; death block t; first-stretch length (n-1)//5+1 resp.
       (n-3)//5+1 for watched families; survival-class breaking loser
       positions 4-r for h in {0,1}, n-1/n-2/1/0 for h in {2,3}).
  LG8  two-stretch handoff: the state after the first stretch is exactly
       F(w+1,h2;n2) in the new ptr frame, verified by running LAD-GEN's
       closed forms on the SECOND stretch (w'=w+1) against the direct
       continuation of the same simulation (grid w in 2..5, n <= 90).

All stdlib, deterministic. Run from the experiment directory:
    python3 ladder_gen_verify.py
Exit status 0 iff every check passes.
"""

import json
import os
import sys

W_MAX = 7
N_MAX = 155
W_HANDOFF = 5
N_HANDOFF = 90


# ---------------- simulator (K0928 Lemma P phase rule) ----------------

def simulate_first_stretches(w, h, n, stretches=1):
    """Play F(w,h;n) through the first `stretches` stretch-w runs.

    Returns a list of stretch records, each with:
      phases   list of dicts(start_ptr_label, dealt_labels, loser_label, held)
      circle   surviving labels in ptr-frame order at the stretch end
      endhold  holdings aligned with circle
      endpot   pot at the stretch end
    """
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


# ---------------- closed forms (proved; see report.md) ----------------

def ladder_gen(w, h, n):
    """Closed-form description of the first stretch-w of F(w,h;n).

    Returns dict(J, exp_len, blocks, break_phase, n2, h2, collapse, elim,
    loser) or None if out of domain (t < 1 or h > w).
    """
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
    """Closed form: does the watched at n-a die in the first stretch-w?

    Returns None if out of domain, else dict(dies, phase, held)."""
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


# ---------------- checks ----------------

class Ctx:
    def __init__(self):
        self.fails = []
        self.counts = {}

    def count(self, name, k=1):
        self.counts[name] = self.counts.get(name, 0) + k

    def fail(self, name, msg):
        self.fails.append(f"{name}: {msg}")


def check_game(ctx, w, h, n):
    recs = simulate_first_stretches(w, h, n, stretches=1)
    g = ladder_gen(w, h, n)
    if g is None:
        return
    ph = recs[0]["phases"]

    # LG1 length
    ctx.count("LG1")
    if len(ph) != g["exp_len"]:
        ctx.fail("LG1", f"w={w} h={h} n={n}: len {len(ph)} != {g['exp_len']}")
        return

    # LG2 cold blocks
    for j, b in enumerate(g["blocks"]):
        ctx.count("LG2")
        p = ph[j]
        if sorted(p["dealt"]) != sorted(b["deal"]) or \
           p["loser"] != b["loser"] or p["held"] != b["held"]:
            ctx.fail("LG2", f"w={w} h={h} n={n} block {j+1}: {p} vs {b}")
            return

    # LG3 breaking phase
    ctx.count("LG3")
    bp = g["break_phase"]
    p = ph[g["J"]]
    if g["collapse"]:
        if p["held"] != bp["held"] or len(p["dealt"]) != 0:
            # collapse: q=1 -> everyone +1, rem = pot%k = 0
            if p["held"] != w + 2 or p["loser"] != 0:
                ctx.fail("LG3", f"collapse w={w} n={n}: {p}")
                return
    else:
        if sorted(p["dealt"]) != sorted(bp["deal"]) or \
           p["loser"] != bp["loser"] or p["held"] != bp["held"] or \
           p["start_ptr"] != bp["ptr"] % n:
            ctx.fail("LG3", f"w={w} h={h} n={n}: {p} vs {bp}")
            return

    # LG4 end state
    ctx.count("LG4")
    r0 = recs[0]
    if g["collapse"]:
        if r0["endpot"] != w + 2 or len(r0["circle"]) != n - 2 or \
           any(x != w + 2 for x in r0["endhold"]):
            ctx.fail("LG4", f"collapse w={w} n={n}: {r0}")
            return
    else:
        exp = [w + 1] * (g["n2"] - g["h2"]) + [w + 2] * g["h2"]
        if r0["endpot"] != w + 1 or r0["endhold"] != exp:
            ctx.fail("LG4", f"w={w} h={h} n={n}: {r0['endhold']} != {exp}")
            return

    # LG5 elimination set + watched criterion
    ctx.count("LG5")
    elim = [p["loser"] for p in ph]
    if sorted(elim) != sorted(g["elim"]):
        ctx.fail("LG5", f"w={w} h={h} n={n}: elim {elim} vs {g['elim']}")
        return
    if n >= 2 * w + 2:
        for a in range(1, w + 2):
            ctx.count("LG5w")
            pos = n - a
            dies = pos in elim
            exp = watch_dies(w, h, n, a)
            if exp is None:
                continue
            if dies != exp["dies"]:
                ctx.fail("LG5", f"w={w} h={h} n={n} a={a}: dies {dies} != {exp['dies']}")
                return
            if dies:
                idx = elim.index(pos)
                if idx + 1 != exp["phase"] or ph[idx]["held"] != exp["held"]:
                    ctx.fail("LG5", f"w={w} h={h} n={n} a={a}: phase/held")
                    return

    # LG6 LAD-h0 regression (h=0)
    if h == 0:
        ctx.count("LG6")
        t, r = g["t"], g["r"]
        if g["collapse"]:
            if not (r0["endpot"] == w + 2 and len(r0["circle"]) == w - 1):
                ctx.fail("LG6", f"collapse w={w}")
                return
        elif r == 0:
            if g["n2"] != w * t - 1 or g["h2"] != w:
                ctx.fail("LG6", f"w={w} n={n} r=0: {g['n2']} {g['h2']}")
                return
        else:
            if g["n2"] != w * t + r - 1 or g["h2"] != w - r:
                ctx.fail("LG6", f"w={w} n={n} r={r}: {g['n2']} {g['h2']}")
                return



def check_handoff(ctx, w, h, n):
    """LG8: the end state of stretch 1 is exactly F(w+1,h2;n2); the closed
    forms then predict stretch 2 (w' = w+1) against the direct simulation."""
    recs = simulate_first_stretches(w, h, n, stretches=2)
    if len(recs) < 2:
        return
    g = ladder_gen(w, h, n)
    if g is None or g["collapse"]:
        return
    n2, h2 = g["n2"], g["h2"]
    w2 = w + 1
    circle = recs[0]["circle"]
    # closed form for stretch 2 in circle-frame
    g2 = ladder_gen(w2, h2, n2)
    if g2 is None:
        return
    # map circle-frame position -> label
    def lab(c):
        return circle[c % len(circle)]
    ph2 = recs[1]["phases"]
    ctx.count("LG8")
    if len(ph2) != g2["exp_len"]:
        ctx.fail("LG8", f"w={w} h={h} n={n}: s2 len {len(ph2)} != {g2['exp_len']}")
        return
    for j, b in enumerate(g2["blocks"]):
        ctx.count("LG8b")
        p = ph2[j]
        if p["loser"] != lab(b["loser"]) or p["held"] != b["held"]:
            ctx.fail("LG8", f"w={w} h={h} n={n} s2 block {j+1}: {p} vs {b}")
            return
    bp = g2["break_phase"]
    p = ph2[g2["J"]]
    if not g2["collapse"]:
        if p["loser"] != lab(bp["loser"]) or p["held"] != bp["held"]:
            ctx.fail("LG8", f"w={w} h={h} n={n} s2 break: {p} vs {bp}")
            return


def run_checks():
    ctx = Ctx()
    for w in range(2, W_MAX + 1):
        for h in range(0, w + 1):
            for n in range(w + 1, N_MAX + 1):
                check_game(ctx, w, h, n)
    for w in range(2, W_HANDOFF + 1):
        for h in range(0, w + 1):
            for n in range(w + 1, N_HANDOFF + 1):
                check_handoff(ctx, w, h, n)
    # LG7: S4 regression (K0933, w=4, n >= 11): death table + lengths
    #   family (h, a):  W4=(0,1)  F(4,1)=(1,1)  F(4,2)=(2,3)  F(4,3)=(3,3)
    #   death iff r = death_r; cold for h in {0,2}, hot-final for {1,3};
    #   death block t; watched length formula (n-a)//5+1 = death phase if
    #   the watched dies, else the full stretch length.
    for h, a, death_r, kind in [(0, 1, 0, "cold"), (1, 1, 0, "hot"),
                                (2, 3, 2, "cold"), (3, 3, 2, "hot")]:
        for n in range(11, N_MAX + 1):
            ctx.count("LG7")
            wd = watch_dies(4, h, n, a)
            if wd is None:
                continue
            t, r = divmod(n, 5)
            exp_dies = (r == death_r)
            if wd["dies"] != exp_dies:
                ctx.fail("LG7", f"h={h} a={a} n={n}: dies {wd['dies']} != {exp_dies} ({wd})")
                return
            g = ladder_gen(4, h, n)
            if exp_dies:
                if wd["phase"] != t or wd["held"] != (4 if kind == "cold" else 5):
                    ctx.fail("LG7", f"h={h} n={n}: phase/held {wd}")
                    return
                watched_len = wd["phase"]
            else:
                watched_len = g["exp_len"]
            if (n - a) // 5 + 1 != watched_len:
                ctx.fail("LG7", f"h={h} a={a} n={n}: len {(n-a)//5+1} != {watched_len}")
                return
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
