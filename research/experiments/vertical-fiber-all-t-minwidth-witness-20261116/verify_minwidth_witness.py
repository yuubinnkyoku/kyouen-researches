#!/usr/bin/env python3
"""Independent audit of the minimum-width G=3 witness family.

The all-t theorem gives the lower bound w >= ceil((cap+2)/t).
This script checks a residue-sensitive witness attaining that width.
It deliberately uses the original occupancy-game mex recursion.
"""
from __future__ import annotations

import json
import math
import hashlib
from pathlib import Path
from functools import lru_cache


def make_witness(t: int, cap: int):
    if t < 2 or cap < 2 * t:
        raise ValueError("requires t >= 2 and cap >= 2t")
    mu, r = divmod(cap - 2 * t, t)
    m = t + 1
    occ = [t, t - 1] + [m] * mu

    if r == 0:
        # The one unused fiber is empty; it supplies an X-token.
        width = mu + 3
    elif 1 <= r <= t - 2:
        # This residual fiber itself supplies the X-token.
        occ.append(r)
        width = mu + 3
    else:
        # r=t-1 supplies another z-token, so an empty fiber is needed for X.
        occ.append(t - 1)
        width = mu + 4

    occ = tuple(sorted(occ, reverse=True))
    if width != math.ceil((cap + 2) / t):
        raise AssertionError(("width formula", t, cap, width))
    if len(occ) > width:
        raise AssertionError(("too many occupied fibers", t, cap, width, occ))
    return m, width, occ, mu, r


def exact_original_grundy(t: int, width: int, m: int, cap: int, start):
    """Canonical occupancy-multiset recursion for the original game."""
    @lru_cache(maxsize=None)
    def G(st):
        used = sum(min(c, t) for c in st)
        options = set()

        # Add a stone in a previously empty fiber.
        if len(st) < width and used < cap:
            child = tuple(sorted(st + (1,), reverse=True))
            options.add(G(child))

        # Add a stone in an occupied fiber.
        for i, c in enumerate(st):
            if c < m:
                child_list = list(st)
                child_list[i] += 1
                child = tuple(sorted(child_list, reverse=True))
                if sum(min(v, t) for v in child) <= cap:
                    options.add(G(child))

        g = 0
        while g in options:
            g += 1
        return g

    value = G(tuple(sorted(start, reverse=True)))
    return value, G.cache_info().currsize


def exact_max_from_empty(t: int, width: int, m: int, cap: int):
    """Exhaust all safe canonical states reachable from the empty position."""
    memo = {}

    def G(st):
        if st in memo:
            return memo[st]
        used = sum(min(c, t) for c in st)
        options = set()
        if len(st) < width and used < cap:
            options.add(G(tuple(sorted(st + (1,), reverse=True))))
        for i, c in enumerate(st):
            if c < m:
                child_list = list(st)
                child_list[i] += 1
                child = tuple(sorted(child_list, reverse=True))
                if sum(min(v, t) for v in child) <= cap:
                    options.add(G(child))
        g = 0
        while g in options:
            g += 1
        memo[st] = g
        return g

    G(())
    return max(memo.values()), len(memo)


def audit():
    checks = 0
    total_states = 0
    failures = []
    residue_counts = {"r=0": 0, "1<=r<=t-2": 0, "r=t-1": 0}

    for t in range(2, 17):
        for mu in range(0, 6):
            for r in range(t):
                cap = 2 * t + mu * t + r
                m, width, occ, mu2, r2 = make_witness(t, cap)
                used = sum(min(c, t) for c in occ)
                empty = width - len(occ)
                z = sum(c == t - 1 for c in occ)
                X = [t - 1 - c for c in occ if c < t - 1]
                X.extend([t - 1] * empty)
                R = cap - used

                structural_ok = (
                    R == 1
                    and used == cap - 1
                    and z >= 1
                    and len(X) >= 1
                    and sum((m - c) % 2 for c in occ if c >= t) % 2 == 1
                )
                value, nstates = exact_original_grundy(t, width, m, cap, occ)
                checks += 1
                total_states += nstates

                if r == 0:
                    residue_counts["r=0"] += 1
                elif r == t - 1:
                    residue_counts["r=t-1"] += 1
                else:
                    residue_counts["1<=r<=t-2"] += 1

                if not structural_ok or value != 3:
                    failures.append({
                        "t": t, "cap": cap, "mu": mu, "r": r,
                        "width": width, "occupancy": list(occ),
                        "R": R, "X": X, "z": z,
                        "structural_ok": structural_ok,
                        "G": value, "states": nstates,
                    })

    # A small explicit regression: the old construction unnecessarily
    # reserved an empty fiber for r=1, although (5,4,1) already works.
    t, cap = 5, 11
    m, width, occ, mu, r = make_witness(t, cap)
    regression_value, regression_states = exact_original_grundy(
        t, width, m, cap, occ
    )

    minimality_checks = 0
    minimality_failures = []
    minimality_states = 0
    for t0 in range(2, 7):
        for mu0 in range(0, 3):
            for r0 in range(t0):
                cap0 = 2 * t0 + mu0 * t0 + r0
                _, w0, _, _, _ = make_witness(t0, cap0)
                max_g, nstates = exact_max_from_empty(t0, w0 - 1, t0 + 1, cap0)
                minimality_checks += 1
                minimality_states += nstates
                if max_g > 1:
                    minimality_failures.append({
                        "t": t0, "cap": cap0, "width": w0 - 1,
                        "max_G": max_g, "states": nstates,
                    })

    return {
        "schema": "vertical-fiber-minwidth-witness-audit-v1",
        "range": {
            "t": [2, 16],
            "mu": [0, 5],
            "r": "0..t-1",
            "m": "t+1",
            "cap": "2t+mu*t+r",
        },
        "checks": checks,
        "total_original_game_states_visited": total_states,
        "residue_case_counts": residue_counts,
        "failures": failures,
        "minimality_boundary_checks": minimality_checks,
        "minimality_boundary_states": minimality_states,
        "minimality_boundary_failures": minimality_failures,
        "pass": not failures and not minimality_failures and checks == 810 and minimality_checks == 60,
        "minimal_width_formula": "ceil((cap+2)/t)",
        "regression_example": {
            "t": t, "m": m, "cap": cap, "q": cap + 1,
            "width": width, "occupancy": list(occ),
            "used_capacity": sum(min(c, t) for c in occ),
            "empty_fibers": width - len(occ),
            "G": regression_value,
            "states_visited": regression_states,
            "residue": r,
        },
        "proof_boundary": (
            "The finite audit checks the witness family only. "
            "The lower bound on width follows from the all-t regime lemma "
            "q>=t*w => max G<=1; the construction is proved by the R=1 "
            "residual mex H=mex{0,1}=2 and one saturated odd chain."
        ),
    }


if __name__ == "__main__":
    result = audit()
    result["verifier_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    if not result["pass"]:
        raise SystemExit(1)
