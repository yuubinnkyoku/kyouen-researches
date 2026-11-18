#!/usr/bin/env python3
"""Independent verification of the z=6 two-token uniform closed form.

Provenance of every component (no component is taken from K0974's verifier):

- H6(y,x,r): the uniform claim table, derived INDEPENDENTLY in this session by
  normalizing the published proved slices K0938 (y=26), K0972 (y=35) and
  K0973 (y=36) into coordinates d = x-y, t = r-2y. It was fixed BEFORE the
  publication of K0974 was read.
- T26/P26, T35/P35, T36/P36: per-slice closed forms transcribed verbatim from
  the published items K0938/K0972/K0973 (proof anchors).
- k974_value(x,y,r): the K0974 published formula (T_y/P_y), transcribed from
  its report; used here only as the OBJECT of verification.
- h5: the K0873 z=5 full Grundy formula (verbatim published code).
- ordered/canonical: two independent direct recursion engines.
- Step engine: universal y-step verified on the (d, t, u, parity) atom grid
  derived in this session (u = d - t is invariant under A/B moves); this is a
  machine-checked full proof of the step for ALL y >= 27, ALL d >= 0,
  13 <= r < x+y+7, given the base slice y = 26 (K0938) and the induction
  hypotheses. Combined with the base, the uniform formula holds for all
  y >= 26 by induction (a second, structurally different proof of the
  conclusion K0974 reaches from the y=4 base via S-induction).

Determinism: the audit JSON is a pure function of the code; two cold runs
must be byte-identical. The verifier records its own SHA-256.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from functools import lru_cache

sys.setrecursionlimit(100000)


def mex(values):
    values = set(values)
    n = 0
    while n in values:
        n += 1
    return n


def O(r, a, b=None):
    return r >= a and (b is None or r <= b) and r % 2 == 1


def E(r, a, b=None):
    return r >= a and (b is None or r <= b) and r % 2 == 0


# --------------------------------------------------------------- K0873 (C-child)
def h5(x, y, r):
    """z=5 two-token full Grundy formula (verbatim published K0873 code)."""
    if r == 0:
        return 0
    s, d = x + y, x - y
    twos = {1, 3, 5}
    if d == 1 and y >= 2:
        twos.add(2 * y + 3)
    elif d == 5:
        twos.add(2 * y + 5)
    elif d == 6:
        twos.update({2 * y + 5, 2 * y + 7, 2 * y + 9, 2 * y + 11})
    elif d >= 7:
        twos.add(2 * y + 5)
    if r in twos:
        return 2
    if d == 0:
        one = E(r, 6, s + 2) if y >= 3 else False
    elif d == 1:
        one = (E(r, 6, s + 3) or r >= s + 4) if y >= 2 else r >= 4
    elif d == 2:
        one = E(r, 6, s) if y >= 2 else False
    elif d == 3:
        one = E(r, 6, s + 1) or r >= s + 2
    elif d == 4:
        one = E(r, 6, s)
    elif d == 5:
        one = E(r, 6, s - 1) or r >= s + 1
    elif d == 6:
        one = E(r, 6, s - 2)
    elif d % 2:
        one = E(r, 6, 2 * y + 4) or O(r, 2 * y + 7, s + 4) or r >= s + 6
    else:
        one = E(r, 6, 2 * y + 4) or O(r, 2 * y + 7, s + 5)
    return int(one)


# --------------------------------------------------------------- uniform claim
K_ODD = {0: 1, 1: 7, 2: 3, 3: 9, 4: 3, 5: 11, 6: 5, 7: 5}


def k_of(d):
    """Odd-r value-1 band upper end: O[7, 2y+k(d)]."""
    if d >= 8:
        return 5
    return K_ODD[d]


def h_even_of(d):
    """Odd-d even-r value-1 lower end: E[2y+h(d), ...] or none for even d<=6."""
    if d == 1:
        return 4
    if d in (3, 5):
        return 6
    return 8  # odd d >= 7


def H6(y, x, r):
    """UNIFORM CLAIM: z=6 two-token residual game, all y >= 26, x >= y, r >= 0.

    Independently normalized from published slices K0938/K0972/K0973.
    """
    if r == 0:
        return 0
    if r >= x + y + 7:
        return (x + y) & 1
    if r <= 12:
        if r in (1, 3, 5):
            return 2
        if r & 1:
            return int(r >= 7)
        return 0
    t = r - 2 * y
    d = x - y
    if r & 1:
        if t <= k_of(d):
            return 1
        if d == 0 and t == 3:
            return 2
        if d == 4 and t == 5:
            return 2
        if d == 7 and t in (7, 9, 11, 13):
            return 2
        if d >= 8 and t == 7:
            return 2
        return 0
    if d & 1:
        if t >= h_even_of(d):
            return 1
    else:
        if d >= 8 and 8 <= t <= d + 6:
            return 1
    return 0


def children6(y, x, r):
    """A/B/C option values for the z=6 slice at (y, x, r), y >= 27, r >= 1.

    Uses induction hypotheses only: A-child is claim(y, x-1, r-1) (inner
    x-induction), B-child is claim(y-1, x, r-1) (outer y-induction, slice
    y-1 >= 26), C-child is the K0873 formula. d = 0 collapses A into B.
    """
    d = x - y
    q = r - 1
    if d == 0:
        b = H6(y - 1, y, q)
        a = b
    else:
        a = H6(y, x - 1, q)
        b = H6(y - 1, x, q)
    c = 1 ^ h5(x, y, q)
    return (a, b, c)


# --------------------------------------------------------------- published anchors
def T26(x):
    res = {1, 3, 5}
    if x == 26:
        res.add(55)
    elif x == 30:
        res.add(57)
    elif x == 33:
        res.update({59, 61, 63, 65})
    elif x >= 34:
        res.add(59)
    return res


def P26(x, r):
    if x == 26:
        return O(r, 7, 53)
    if x == 27:
        return O(r, 7) or E(r, 56)
    if x == 28:
        return O(r, 7, 55)
    if x == 29:
        return O(r, 7) or E(r, 58)
    if x == 30:
        return O(r, 7, 55)
    if x == 31:
        return O(r, 7) or E(r, 58)
    if x == 32:
        return O(r, 7, 57)
    if x == 33:
        return O(r, 7, 57) or E(r, 60) or O(r, 67)
    if x % 2 == 0:
        return O(r, 7, 57) or E(r, 60, x + 32)
    return O(r, 7, 57) or E(r, 60) or O(r, x + 34)


def h26_closed(x, r):
    if r == 0:
        return 0
    if r in T26(x):
        return 2
    return int(P26(x, r))


def T35(x):
    res = {1, 3, 5}
    if x == 35:
        res.add(73)
    elif x == 39:
        res.add(75)
    elif x == 42:
        res.update({77, 79, 81, 83})
    elif x >= 43:
        res.add(77)
    return res


def P35(x, r):
    if x == 35:
        return O(r, 7, 71)
    if x == 36:
        return O(r, 7) or E(r, 74)
    if x == 37:
        return O(r, 7, 73)
    if x == 38:
        return O(r, 7) or E(r, 76)
    if x == 39:
        return O(r, 7, 73)
    if x == 40:
        return O(r, 7) or E(r, 76)
    if x == 41:
        return O(r, 7, 75)
    if x == 42:
        return O(r, 7, 75) or E(r, 78) or r >= 85
    if x == 43:
        return O(r, 7, 75) or E(r, 78, 84)
    if x % 2 == 0:
        return O(r, 7, 75) or E(r, 78) or r >= x + 43
    return O(r, 7, 75) or E(r, 78, x + 41)


def h35_closed(x, r):
    if r == 0:
        return 0
    if r in T35(x):
        return 2
    return int(P35(x, r))


def T36(x):
    res = {1, 3, 5}
    if x == 36:
        res.add(75)
    elif x == 40:
        res.add(77)
    elif x == 43:
        res.update({79, 81, 83, 85})
    elif x >= 44:
        res.add(79)
    return res


def P36(x, r):
    if x == 36:
        return O(r, 7, 73)
    if x == 37:
        return O(r, 7) or E(r, 76)
    if x == 38:
        return O(r, 7, 75)
    if x == 39:
        return O(r, 7) or E(r, 78)
    if x == 40:
        return O(r, 7, 75)
    if x == 41:
        return O(r, 7) or E(r, 78)
    if x == 42:
        return O(r, 7, 77)
    if x == 43:
        return O(r, 7, 77) or E(r, 80) or O(r, 87)
    if x == 44:
        return O(r, 7, 77) or E(r, 80, 86)
    if x % 2 == 0:
        return O(r, 7, 77) or E(r, 80, x + 42)
    return O(r, 7, 77) or E(r, 80) or O(r, x + 44)


def h36_closed(x, r):
    if r == 0:
        return 0
    if r in T36(x):
        return 2
    return int(P36(x, r))


# --------------------------------------------------------------- K0974 formula
def k974_T(x, y):
    res = {1, 3, 5}
    d = x - y
    if d == 0:
        res.add(2 * y + 3)
    elif d == 4:
        res.add(2 * y + 5)
    elif d == 7:
        res.update({2 * y + 7, 2 * y + 9, 2 * y + 11, 2 * y + 13})
    elif d >= 8:
        res.add(2 * y + 7)
    return res


def k974_P(x, y, r):
    d = x - y
    S = x + y
    if d == 0:
        return O(r, 7,  * y + 1)
    if d == 1:
        return O(r, 7) or E(r, 2 * y + 4)
    if d == 2:
        return O(r, 7, 2 * y + 3)
    if d == 3:
        return O(r, 7) or E(r, 2 * y + 6)
    if d == 4:
        return O(r, 7, 2 * y + 3)
    if d == 5:
        return O(r, 7) or E(r, 2 * y + 6)
    if d == 6:
        return O(r, 7, 2 * y + 5)
    if d % 2 == 1:
        return O(r, 7, 2 * y + 5) or E(r, 2 * y + 8) or O(r, S + 8)
    return O(r, 7, 2 * y + 5) or E(r, 2 * y + 8, S + 6)


def k974_value(x, y, r):
    if r == 0:
        return 0
    if r >= x + y + 7:
        return (x + y) & 1
    if r in k974_T(x, y):
        return 2
    return int(k974_P(x, y, r))


# --------------------------------------------------------------- direct engines
def make_engines():
    @lru_cache(None)
    def ordered(r, tokens, z):
        if r == 0:
            return 0
        children = []
        for i, value in enumerate(tokens):
            child = list(tokens)
            next_z = z
            if value >= 2:
                child[i] -= 1
            else:
                child.pop(i)
                next_z += 1
            children.append(ordered(r - 1, tuple(child), next_z))
        if z:
            children.append(1 ^ ordered(r - 1, tokens, z - 1))
        return mex(children)

    @lru_cache(None)
    def canonical(r, tokens, z):
        if r == 0:
            return 0
        children = []
        for i, value in enumerate(tokens):
            child = list(tokens)
            next_z = z
            if value >= 2:
                child[i] -= 1
            else:
                child.pop(i)
                next_z += 1
            children.append(canonical(r - 1, tuple(sorted(child, reverse=True)), next_z))
        if z:
            children.append(1 ^ canonical(r - 1, tokens, z - 1))
        return mex(children)

    return ordered, canonical


# --------------------------------------------------------------- step engine
def pick_y(t):
    """Smallest y >= 27 with r = 2y + t >= 13 (region-A representative)."""
    need = (13 - t + 1) // 2
    return max(27, need)


def eval_point(d, t):
    """Step check at one region-A point; returns (mex, claim, children, y).

    Asserts two-y invariance: children at (y, y+d, 2y+t) and at (y+1, y+1+d,
    2(y+1)+t) must agree, so the mex computation is y-independent.
    Returns (None, None, (ch1, ch2), y) on variance.
    """
    y = pick_y(t)
    x = y + d
    r = 2 * y + t
    ch1 = children6(y, x, r)
    ch2 = children6(y + 1, x + 1, r + 2)
    if ch1 != ch2:
        return None, None, (ch1, ch2), y
    return mex(ch1), H6(y, x, r), ch1, y


def verify_region_L(failures, counts):
    """r in 1..12: d-free low window (claim low branch reads no d; h5 children
    reduce to h5_low since every d-sensitive h5 threshold exceeds 2y-2 >= 50).
    Concrete check over d in 0..151 and y in {27,28,60}; the claim value must
    be d-constant per r.
    """
    for r in range(1, 13):
        for d in range(0, 152):
            for y in (27, 28, 60): 
                x = y + d
                m = mex(children6(y, x, r))
                cl = H6(y, x, r)
                counts["step_low_window"] += 1
                if m != cl:
                    failures.append(("low-step", d, r, y, m, cl))
        by_val = {}
        for d in range(0, 152):
            v = H6(101, 101 + d, r)
            counts["low_window_d_constancy"] += 1
            by_val.setdefault(v, []).append(d)
        if len(by_val) > 1:
            failures.append(("low-claim-d-dependent", r, {k: v[:5] for k, v in by_val.items()}))


def h5_low(rq):
    if rq == 0:
        return 0
    if rq in (1, 3, 5):
        return 2
    if rq % 2 == 0 and rq >= 6:
        return 1
    return 0


def verify_h5_low(failures, counts):
    """Every d-sensitive atom of h5 has a threshold >= 2y-2 >= 50 > 11, so
    h5(x,y,rq) = h5_low(rq) for all y >= 26, all d, rq <= 11. Finite scan
    corroborates the reduction over a d-window and several y.
    """
    for d in range(0, 3001):
        for y in (26, 27, 100, 850):
            for rq in range(0, 12):
                counts["h5_low_reduction"] += 1
                if h5(y + d, y, rq) != h5_low(rq):
                    failures.append(("h5-low", d, y, rq, h5(y + d, y, rq), h5_low(rq)))
                    return


def verify_transient_d(failures, counts):
    """Fixed d in 0..8: sweep t over all atom intervals covering
    (t <= d+6) x (region A via y choice). All parent and child claim/h5 atoms
    are t-vs-constant with constants in [-60, d+11], so the sweeps cover
    every t. Below-interval constancy is asserted per t-parity at three
    depths (incl. t = -10**9).
    """
    for d in range(0, 9):
        bt = set(range(-60, d + 12))
        bt |= set(K_ODD.values())
        bt.add(k_of(d + 1))
        for e in range(-4, 8):
            bt.add(d + e)
            bt.add(d + e + 1)
        for c in (3, 5, 7, 9, 11, 13):
            bt.add(c + 1)
            bt.add(c - 1)
        bt = sorted(bt)
        cap = d + 6
        # below interval (t < bt[0]): per-parity constancy + step check
        for parity in (0, 1):
            vals = []
            for t in (c for c in (bt[0] - 1, bt[0] - 2, bt[0] - 50, -(10 ** 9)) if c % 2 == parity):
                res = eval_point(d, t)
                counts["step_transient"] += 1
                if res[0] is None:
                    failures.append(("transient-yvar", d, t, res[2]))
                    continue
                vals.append((t, res[0], res[1]))
            if len(set((v[1], v[2]) for v in vals)) > 1:
                failures.append(("transient-below-not-constant", d, parity, vals))
            for t, m, cl in vals:
                if m != cl:
                    failures.append(("transient-step", d, t, m, cl))
        # singleton intervals
        for t in bt:
            if t <= cap:
                res = eval_point(d, t)
                counts["step_transient"] += 1
                if res[0] is None:
                    failures.append(("transient-yvar", d, t, res[2]))
                else:
                    m, cl, ch, y = res
                    if m != cl:
                        failures.append(("transient-step", d, t, m, cl, ch, y))


def verify_class_grid(failures, counts, dmin, dparity, label):
    """Classes (d >= dmin, d parity fixed): 2-D (t, u) box grid. All atoms
    (claim tables, child claim tables, h5) reduce to t-vs-const or u-vs-const
    with constants inside Gamma_t = [-40, 45) and Gamma_u = [-20, 14); u is
    invariant under A/B children (u_child = u), so a feasible box has a
    constant child pattern, asserted at up to 3 reps; every point of the
    class region (u >= -6 i.e. below tail, d >= dmin, r >= 13) lies in
    exactly one box.
    """
    gt = list(range(-40, 45))
    gu = list(range(-20, 14))
    t_iv = [(None, gt[0] - 1, "below")] + [(c, c, "singleton") for c in gt] + [(gt[-1] + 1, None, "above")]
    u_iv = [(c, c, "singleton") for c in gu] + [(gu[-1] + 1, None, "above")]
    for (t_lo, t_hi, tk) in t_iv:
        for (u_lo, u_hi, uk) in u_iv:
            if uk == "singleton" and u_lo < -6:
                continue  # tail zone (u <= -7): covered by K0832
            for parity in (0, 1):  # parity of r = parity of t
                reps = []
                if tk == "singleton":
                    tcands = [t_lo]
                elif tk == "below":
                    tcands = [c for c in (gt[0] - 1, gt[0] - 2, gt[0] - 200) if c % 2 == parity]
                else:
                    tcands = [c for c in (gt[-1] + 1, gt[-1] + 2, gt[-1] + 200) if c % 2 == parity]
                for t in tcands:
                    if uk == "singleton":
                        ucands = [u_lo]
                    else:
                        u0 = max(u_lo, -6, dmin - t)
                        if u0 % 2 != (dparity - t) % 2:
                            u0 += 1
                        ucands = [u0, u0 + 40]
                    for u in ucands:
                        if u < -6 or u < u_lo or (u_hi is not None and u > u_hi):
                            continue
                        d = t + u
                        if d < dmin or d % 2 != dparity:
                            if tk != "singleton":
                                u2 = max(u_lo, -6, dmin - t)
                                if u2 % 2 != (dparity - t) % 2:
                                    u2 += 1
                                if u2 >= -6 and (u_hi is None or u2 <= u_hi):
                                    d = t + u2
                                    u = u2
                                else:
                                    continue
                            else:
                                continue
                        if d < dmin or d % 2 != dparity or u < -6:
                            continue
                        reps.append((t, u))
                seen = set()
                for (t, u) in reps:
                    d = t + u
                    res = eval_point(d, t)
                    counts["step_class"] += 1
                    if res[0] is None:
                        failures.append(("class-yvar", label, t, u, res[2]))
                        continue
                    m, cl, ch, y = res
                    seen.add((m, cl))
                    if m != cl:
                        failures.append(("class-step", label, t, u, d, m, cl, ch, y))
                if len(seen) > 1:
                    failures.append(("class-box-not-constant", label, (t_lo, t_hi, tk), (u_lo, u_hi, uk), parity, sorted(seen)))
                if reps:
                    counts[f"boxes_{label}"] += 1


# --------------------------------------------------------------- main audit
def main():
    failures = []
    counts = {
        "step_low_window": 0,
        "low_window_d_constancy": 0,
        "h5_low_reduction": 0,
        "step_transient": 0,
        "step_class": 0,
        "boxes_d9_odd": 0,
        "boxes_d10_even": 0,
    }

    # (1) universal step proof (given base slice y=26 = K0938)
    verify_region_L(failures, counts)
    verify_h5_low(failures, counts)
    verify_transient_d(failures, counts)
    verify_class_grid(failures, counts, 9, 1, "d9_odd")
    verify_class_grid(failures, counts, 10, 0, "d10_even")

    # (2) base slice y=26 vs published K0938 closed forms
    n = 0
    for x in range(26, 1201):
        for r in range(0, x + 51):
            n += 1
            if H6(26, x, r) != h26_closed(x, r):
                failures.append(("base26_published", x, r, H6(26, x, r), h26_closed(x, r)))
    for x in (1300, 2000, 5000, 39000):
        for r in list(range(0, 120)) + list(range(x + 33, x + 52)):
            n += 1
            if H6(26, x, r) != h26_closed(x, r):
                failures.append(("base26_published_far", x, r))
    counts["base26_vs_K0938"] = n

    # (3) published slices y=35 (K0972), y=36 (K0973) vs closed forms
    n = 0
    for x in range(35, 1201):
        for r in range(0, x + 51):
            n += 1
            if H6(35, x, r) != h35_closed(x, r):
                failures.append(("slice35_published", x, r))
    for x in (1300, 2000, 5000, 39000):
        for r in list(range(0, 120)) + list(range(x + 33, x + 52)):
            n += 1
            if H6(35, x, r) != h35_closed(x, r):
                failures.append(("slice35_published_far", x, r))
    counts["slice35_vs_K0972"] = n
    n = 0
    for x in range(36, 1201):
        for r in range(0, x + 51):
            n += 1
            if H6(36, x, r) != h36_closed(x, r):
                failures.append(("slice36_published", x, r))
    for x in (1300, 2000, 5000, 39000):
        for r in list(range(0, 120)) + list(range(x + 33, x + 52)):
            n += 1
            if H6(36, x, r) != h36_closed(x, r):
                failures.append(("slice36_published_far", x, r))
    counts["slice36_vs_K0973"] = n

    # (4) independent H6 == K0974 published formula (equality of two
    # independently derived encodings), y >= 26 domain of my proof
    n = 0
    for y in list(range(26, 121, 7)) + [200, 500, 1000]:
        for d in range(0, 43):
            x = y + d
            for r in range(0, x + 64):
                n += 1
                if H6(y, x, r) != k974_value(x, y, r):
                    failures.append(("H6_vs_K0974", y, x, r, H6(y, x, r), k974_value(x, y, r)))
    for y in range(26, 42, 2):
        for d in (0, 1, 5, 8, 9, 11, 40):
            x = y + d
            for r in range(x + y + 7, x + y + 48):
                n += 1
                if H6(y, x, r) != k974_value(x, y, r):
                    failures.append(("H6_vs_K0974_tail", y, x, r))
    counts["H6_vs_K0974"] = n

    # (5) direct recursion vs the uniform claim, published AND unpublished
    # slices y=26..100 (y=37..100 never published before)
    ordered, canonical = make_engines()
    n = 0
    for y in range(26, 41):
        for d in range(0, 11):
            x = y + d
            for r in range(0, x + y + 10):
                v_o = ordered(r, (x, y), 6)
                v_c = canonical(r, (x, y), 6)
                n += 2
                if v_o != v_c:
                    failures.append(("engine_mismatch", y, x, r, v_o, v_c))
                if H6(y, x, r) != v_c:
                    failures.append(("direct26_40", y, x, r, v_c, H6(y, x, r)))
    for y in list(range(42, 57, 2)) + [60, 70, 80, 90, 100]:
        for d in range(0, 6):
            x = y + d
            for r in range(0, x + y + 10):
                v_c = canonical(r, (x, y), 6)
                n += 1
                if H6(y, x, r) != v_c:
                    failures.append(("direct42_100", y, x, r, v_c, H6(y, x, r)))
    for y in list(range(61, 101, 12)) + [97, 99]:
        for d in range(0, 4):
            x = y + d
            for r in range(0, x + y + 9):
                v_c = canonical(r, (x, y), 6)
                n += 1
                if H6(y, x, r) != v_c:
                    failures.append(("direct61_99", y, x, r, v_c, H6(y, x, r)))
    # wide-d spot checks (independent engines at large d, both below and at tail)
    for y in (26, 30, 34, 38):
        for d in range(40, 46):
            x = y + d
            for r in range(0, x + y + 12):
                v_c = canonical(r, (x, y), 6)
                n += 1
                if H6(y, x, r) != v_c:
                    failures.append(("direct_wide_d", y, x, r, v_c, H6(y, x, r)))
    counts["direct_vs_H6_y26_100"] = n

    # (6) direct recursion vs the published K0974 formula on its own
    # exclusive range y=4..25 (K0880..K0936 slice territory), independent engines
    n = 0
    for y in range(4, 26):
        for d in range(0, 9):
            x = y + d
            for r in range(0, x + y + 9):
                v = canonical(r, (x, y), 6)
                n += 1
                if k974_value(x, y, r) != v:
                    failures.append(("direct4_25_vs_K0974", y, x, r, v, k974_value(x, y, r)))
    for (x, y) in ((9, 4), (14, 7), (20, 12), (27, 18)):
        for r in range(0, 45):
            v_o = ordered(r, (x, y), 6)
            v_c = canonical(r, (x, y), 6)
            n += 2
            if v_o != v_c or k974_value(x, y, r) != v_o:
                failures.append(("direct4_25_ordered", x, y, r, v_o, v_c))
    counts["direct_vs_K0974_y4_25"] = n

    # (7) value-2 census via independent recursion vs the published T_y formula
    n = 0
    for y in range(4, 41):
        for d in range(0, 9):
            x = y + d
            twos = {r for r in range(1, x + y + 10) if canonical(r, (x, y), 6) == 2}
            n += 1
            if twos != k974_T(x, y):
                failures.append(("twos_census", y, x, sorted(twos), sorted(k974_T(x, y))))
    counts["twos_census_y4_40"] = n

    # (8) y=3 boundary check: published claim T_3(3) = {1,3,5,7,9} (the reason
    # the uniform formula starts at y=4)
    twos3 = sorted(r for r in range(1, 45) if canonical(r, (3, 3), 6) == 2)
    n = 1
    if twos3 != [1, 3, 5, 7, 9]:
        failures.append(("y3_boundary", twos3))
    counts["y3_boundary"] = n

    # (9) Theorem T parity bound audit at step representative points
    n = 0
    for d in range(0, 40):
        for t in list(range(-45, 46, 2)) + [7, 9, 11, 13]:
            if t > d + 6:
                continue
            res = eval_point(d, t)
            if res[0] is None:
                continue
            m, cl, ch, y = res
            x = y + d
            r = 2 * y + t
            n += 1
            if r & 1:
                if not set(ch) <= {0, 1}:
                    failures.append(("odd_parent_children_bound", x, y, r, ch))
            else:
                if m > 1:
                    failures.append(("even_parent_value_bound", x, y, r, m, ch))
    counts["theorem_T_bounds"] = n

    # (10) tail audit vs K0832 on samples
    n = 0
    for y in range(26, 44, 2):
        for d in (0, 1, 5, 8, 9, 11, 30, 41):
            x = y + d
            for r in range(x + y + 7, x + y + )
                n += 1
                if H6(y, x, r) != (x + y) & 1:
                    failures.append(("tail_parity", y, x, r))
    counts["tail_parity"] = n

    # ---------------------------------------------------------------- assembly
    with open(__file__, "rb") as fhv:
        verifier_sha = hashlib.sha256(fhv.read()).hexdigest()

    counts["total_examples"] = sum(v for v in counts.values())
    audit = {
        "audit_schema": "kyouen-z6-independent-uniform-audit-v1",
        "checks": {k: counts[k] for k in sorted(counts)},
        "failure_count": len(failures),
        "failures": failures[:25],
        "all_ok": len(failures) == 0,
        "provenance": {
            "H6_uniform_claim": "normalized independently from published slices K0938/K0972/K0973",
            "k974_formula": "transcribed from K0974 report (verification object)",
            "closed_form_anchors": "K0938 y=26, K0972 y=35, K0973 y=36",
            "h5": "K0873 verbatim",
            "universal_step": "(d,t,u) atom-grid induction, base y=26 (K0938), covers all y>=27, all d, 13<=r<x+y+7",
        },
        "verifier_sha256": verifier_sha,
    }
    out = json.dumps(audit, ensure_ascii=True, indent=2, sort_keys=True) + "\n"
    dest = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output", "audit.json")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", newline="\n") as fho:
        fho.write(out)
    print(json.dumps({k: counts[k] for k in sorted(counts)}, indent=None))
    print("failures:", len(failures))
    for f in failures[:25]:
        print("FAIL", f)
    print("all_ok:", len(failures) == 0)
    print("verifier_sha256:", verifier_sha)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
