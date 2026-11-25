#!/usr/bin/env python3
"""Final verifier for the all-t pure-fiber Grundy max theorem.

V0: labeled occupancy-vector engine vs multiset engine (independent implementations).
V1: multiset engine vs decomposition G = x XOR H(R;X;z) (excess-coordinate residual).
V2: state-max vs closed-form max formula.
V3: universal bound max <= 3.
V4: Theorem-T parity structure: H <= 1 at even R, H <= 2 at odd R, and
    option sets at even R never contain both 0 and 1 (box audit).
V5: explicit witness families achieve the claimed maxima.
V6: regime closed form: R >= L-1  =>  H = (L-n) mod 2.
Writes the JSON audit to stdout on completion.
"""
import sys, json
from functools import lru_cache
from itertools import product as iproduct

sys.setrecursionlimit(1000000)

def engine_values(t, w, m, cap):
    @lru_cache(maxsize=None)
    def G(st):
        ch = set()
        used = sum(min(c, t) for c in st)
        if len(st) < w and used < cap:
            ch.add(tuple(sorted(st + (1,), reverse=True)))
        for i in range(len(st)):
            if st[i] < m:
                new = list(st); new[i] += 1
                nt = tuple(sorted(new, reverse=True))
                if sum(min(c, t) for c in nt) <= cap:
                    ch.add(nt)
        vals = {G(c) for c in ch}
        g = 0
        while g in vals: g += 1
        return g
    states = {()}
    frontier = [()]
    while frontier:
        nf = []
        for st in frontier:
            used = sum(min(c, t) for c in st)
            if len(st) < w and used < cap:
                hi = st[0] if st else m
                vmax = min(hi, m)
                if cap - used < t:
                    vmax = min(vmax, cap - used)
                for v in range(1, vmax + 1):
                    nt = tuple(sorted(st + (v,), reverse=True))
                    if sum(min(c, t) for c in nt) <= cap and nt not in states:
                        states.add(nt); nf.append(nt)
        frontier = nf
    return {st: G(st) for st in states}

def labeled_engine_values(t, w, m, cap):
    """Occupancy vectors (c_1..c_w), moves increment one coordinate."""
    safe = lambda c: sum(min(v, t) for v in c) <= cap
    memo = {}
    def G(c):
        if c in memo: return memo[c]
        vals = set()
        for i in range(w):
            if c[i] < m:
                nc = list(c); nc[i] += 1
                if safe(nc):
                    vals.add(G(tuple(nc)))
        g = 0
        while g in vals: g += 1
        memo[c] = g
        return g
    states = [c for c in iproduct(range(0, m + 1), repeat=w) if safe(c)]
    for c in states: G(c)
    return {c: G(c) for c in states}

def make_H(kap):
    memo = {}
    def H(R, X, z):
        key = (R, X, z)
        if key in memo: return memo[key]
        cands = set()
        if R >= 1:
            for x in set(X):
                nx = list(X)
                if x >= 2:
                    nx.remove(x); nx.append(x - 1); nx.sort()
                    cands.add(H(R - 1, tuple(nx), z))
                else:
                    nx.remove(1); nx.sort()
                    cands.add(H(R - 1, tuple(nx), z + 1))
            if z >= 1:
                cands.add(kap ^ H(R - 1, X, z - 1))
        g = 0
        while g in cands: g += 1
        memo[key] = g
        return g
    return H

def state_of(t, w, m, cap, st):
    """decomposition state (x, R, X, z) of occupancy-multiset st."""
    M = min(t, m)
    x = 0; R = cap; X = []; z = 0
    for c in st:
        if c >= t:
            R -= t; x ^= (m - c) % 2
        elif c <= M - 1:
            R -= c
            e = (M - 1) - c
            if e == 0: z += 1
            else: X.append(e)
        else:
            R -= c
    for _ in range(w - len(st)):
        e = M - 1
        if e == 0: z += 1
        else: X.append(e)
    return x, R, tuple(sorted(X, reverse=True)), z

def max_formula(t, w, m, cap):
    if cap == 0: return 0
    p = (m - min(t, m)) % 2
    if p == 0 or cap >= t * w - 1:
        return 1
    return min(3, cap // t + 1)

def gen_multisets(maxpart, maxsize):
    results = {()}
    frontier = [()]
    while frontier:
        nf = []
        for ms in frontier:
            lo = ms[-1] if ms else maxpart
            if len(ms) < maxsize:
                for p_ in range(1, lo + 1):
                    nm = tuple(sorted(ms + (p_,), reverse=True))
                    if nm not in results:
                        results.add(nm); nf.append(nm)
        frontier = nf
    return sorted(results)

def main():
    out = {"V0": {"checks": 0, "mismatches": 0},
           "V1": {"checks": 0, "mismatches": 0},
           "V2": {"checks": 0, "mismatches": []},
           "V3": {"checks": 0, "violations": []},
           "V4": {"states": 0, "parity_violations": 0, "even_option_01_violations": 0, "sup_H": 0},
           "V5": {"checks": 0, "failures": []},
           "V6": {"checks": 0, "mismatches": 0}}
    Hs = {}
    def getH(kap):
        return Hs.setdefault(kap, make_H(kap))

    # ---- V0: labeled vs multiset on a subgrid ----
    for t in (2, 3, 4):
        for w in (1, 2, 3):
            for m in (3, 4, 5):
                if m < 2: continue
                for cap in range(1, min(t * w, 10) + 1):
                    mv = engine_values(t, w, m, cap)
                    lv = labeled_engine_values(t, w, m, cap)
                    for c, g in lv.items():
                        ms = tuple(sorted([v for v in c if v > 0], reverse=True))
                        out["V0"]["checks"] += 1
                        if ms not in mv or mv[ms] != g:
                            out["V0"]["mismatches"] += 1
                            if out["V0"]["mismatches"] <= 5:
                                print("V0 MISMATCH", t, w, m, cap, c, g, mv.get(ms), flush=True)

    # ---- V1/V2/V3: full grid ----
    grid = 0
    for t in (2, 3, 4, 5, 6):
        for w in (1, 2, 3, 4, 5):
            for m in (2, 3, 4, 5, 6, 7, 8, 9):
                for cap in range(0, min(t * w, 20) + 1):
                    grid += 1
                    vals = engine_values(t, w, m, cap)
                    H = getH((m - min(t, m)) % 2)
                    for st, g in vals.items():
                        x, R, X, z = state_of(t, w, m, cap, st)
                        out["V1"]["checks"] += 1
                        if (x ^ H(R, X, z)) != g:
                            out["V1"]["mismatches"] += 1
                            if out["V1"]["mismatches"] <= 5:
                                print("V1 MISMATCH", t, w, m, cap, st, g, x ^ H(R, X, z), flush=True)
                    mx = max(vals.values())
                    pred = max_formula(t, w, m, cap)
                    out["V2"]["checks"] += 1
                    if mx != pred:
                        out["V2"]["mismatches"].append([t, w, m, cap, mx, pred])
                    out["V3"]["checks"] += 1
                    if mx > 3:
                        out["V3"]["violations"].append([t, w, m, cap, mx])
    out["grid_points"] = grid

    # ---- V4: Theorem-T structure audit over a box (kap=1) ----
    H1 = getH(1)
    allX = gen_multisets(5, 6)
    for X in allX:
        for z in range(0, 8):
            for R in range(0, 13):
                v = H1(R, X, z)
                out["V4"]["states"] += 1
                out["V4"]["sup_H"] = max(out["V4"]["sup_H"], v)
                if R % 2 == 0 and v > 1: out["V4"]["parity_violations"] += 1
                if R % 2 == 1 and v > 2: out["V4"]["parity_violations"] += 1
                if R % 2 == 0 and R >= 2:
                    opts = set()
                    for xx in set(X):
                        nx = list(X)
                        if xx >= 2:
                            nx.remove(xx); nx.append(xx - 1); nx.sort()
                            opts.add(H1(R - 1, tuple(nx), z))
                        else:
                            nx.remove(1); nx.sort()
                            opts.add(H1(R - 1, tuple(nx), z + 1))
                    if z >= 1:
                        opts.add(1 ^ H1(R - 1, X, z - 1))
                    if 0 in opts and 1 in opts:
                        out["V4"]["even_option_01_violations"] += 1

    # ---- V5: witness families ----
    # G=3 witnesses: cap >= 2t, p=1: m=t+1. Position: chains/full-chains/z/empty/fillers.
    def witness3(t, cap, w):
        m = t + 1
        # consumption target: cap - 1 (R = 1)
        # base: chain(level t) [t], z(level t-1) [t-1], empty [0]
        # remainder k = cap - 1 - (2t - 1) = cap - 2t  filled with full-chains (t each, value 0)
        # and one level-j token (j in 1..t-2) or extra z-tokens (t-1) or empties (0).
        k = cap - 2 * t
        # base: chain (level t) + z-token (level t-1); at least one fiber must stay
        # empty (its excess token M-1 = t-1 supplies the X-token of the H=2 witness).
        parts = [t, t - 1]
        rem = k
        while rem >= t and len(parts) < w - 1:
            parts.append(m)  # full chain: consumption t, value-0 contribution
            rem -= t
        if rem > 0:
            if 1 <= rem <= t - 2:
                if len(parts) >= w - 1: return None
                parts.append(rem)  # level-j token (extra X-token)
            elif rem == t - 1:
                if len(parts) >= w - 1: return None
                parts.append(t - 1)  # extra z-token
            else:
                return None
        if len(parts) > w - 1:
            return None
        # recompute R: total consumption must be cap - 1
        cons = sum(min(p_, t) for p_ in parts)
        if cons != cap - 1: return None
        return m, tuple(sorted(parts, reverse=True))
    for t in (2, 3, 4, 5, 6):
        for cap in range(2 * t, min(2 * t + 6, 5 * t) + 1):
            for w in range(3, 6):
                wit = witness3(t, cap, w)
                if wit is None: continue
                m, st = wit
                if len(st) > w: continue
                vals = engine_values(t, w, m, cap)
                out["V5"]["checks"] += 1
                if vals.get(st) != 3:
                    out["V5"]["failures"].append(["G3", t, cap, w, list(st), vals.get(st)])
    # G=2 witnesses: t <= cap <= 2t-2, p=1: m=t+1: position: z(level t-1) + level-j token (j=cap-t), w>=2
    for t in (2, 3, 4, 5, 6):
        for cap in range(t, 2 * t - 1):
            m = t + 1
            j = cap - t
            parts = [t - 1] + ([j] if j >= 1 else [])
            w = 2
            st = tuple(sorted(parts, reverse=True))
            vals = engine_values(t, w, m, cap)
            out["V5"]["checks"] += 1
            if vals.get(st) != 2:
                out["V5"]["failures"].append(["G2", t, cap, w, list(st), vals.get(st)])
    # G=2 witness at cap=2t-1: two z-tokens + one empty fiber (w=3)
    for t in (2, 3, 4, 5, 6):
        cap = 2 * t - 1
        m = t + 1
        parts = [t - 1, t - 1]
        w = 3
        st = tuple(sorted(parts, reverse=True))
        vals = engine_values(t, w, m, cap)
        out["V5"]["checks"] += 1
        if vals.get(st) != 2:
            out["V5"]["failures"].append(["G2b", t, cap, w, list(st), vals.get(st)])
    # G=1 witness: 1 <= cap <= t-1, any p: single token at level cap-1
    for t in (2, 3, 4, 5, 6):
        for cap in range(1, t):
            for p_, m in ((0, t + 2), (1, t + 1)):
                w = 1
                st = (cap - 1,) if cap >= 2 else ()
                vals = engine_values(t, w, m, cap)
                out["V5"]["checks"] += 1
                if max(vals.values()) != 1:
                    out["V5"]["failures"].append(["G1", t, cap, m, "max!=1", max(vals.values())])

    # ---- V6: regime closed form ----
    for X in allX:
        for z in range(0, 7):
            for R in range(0, 12):
                L = sum(X) + len(X) + z
                n = len(X) + z
                if R >= L - 1 and (L > 0 or R >= 0):
                    out["V6"]["checks"] += 1
                    if H1(R, X, z) != (L - n) % 2:
                        out["V6"]["mismatches"] += 1
    print(json.dumps(out, ensure_ascii=False))

if __name__ == "__main__":
    main()
