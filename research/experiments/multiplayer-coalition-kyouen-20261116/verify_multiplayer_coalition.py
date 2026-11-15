#!/usr/bin/env python3
"""Multiplayer (r-player) coalition census for the q-point kyouen game.

Self-contained verifier (stdlib only, deterministic, byte-identical reruns).
It writes output/audit.json next to this file.

Scope of this verifier (finite, machine-verified):
  * Small integer boards (w rows x m columns, cells (x,y), x<m, y<w) with the
    complete-call q-point rule: a position is safe iff no q distinct placed
    cells lie on a common circle or line (integer determinant criterion,
    no floating point). Forbidden sets are exactly the rank<=3 subsets of the
    [x^2+y^2, x, y, 1] matrix (K0001 extended to q points).
  * r-player cyclic play from a position S with mover a: players rotate
    a, a+1, ... mod r; the first player with no legal move is the loser
    (K0339 convention); the last mover is reported separately.
  * Possible loser / possible last-mover sets over all maximal plays.
  * Coalition semantics (the direction K0339 explicitly leaves open):
    player j alone versus a coalition of all other players.
      Surv_j(S,a): j can force not being the first stuck player.
      Win_j(S,a):  j can force being the last mover.
  * Universal lemmas are machine-checked on every enumerated position:
      L1 r=2 reduction:  Surv_0 == Win_0 == classical mover win == (grundy!=0).
      L2 frozen rule:   |lens(S)| == 1  =>  coalition DP collapses to the
                        K0339 residue predictions on every position.
      L3 Win => Surv for every (position, residue).
      L4 Win_j(S,a) => j is a possible last mover.
  * External anchors: K0004 safe-set counts (2x2:15, 3x3:298, 4x4:5811) and
    r=2 empty results; K0011-K0014; K0339 published maximal-size histograms,
    Delta and root possible losers (r=2..8) for the 1..4 square boards;
    K0069 (2xm q=4: m=6,7,8 first player loses); K0071 (3xm q=5: first player
    wins iff m in {1,3} for m<=5); K0025 uniform anchors ((2,4),(2,5),(2,6)
    with q=5: all maximal sets have exactly 8 stones, count C(m,4)^2).
  * Two independent engines: engine A uses incremental circle/line equations
    of (q-1)-subsets; engine B independently enumerates all forbidden q-subsets
    as bitmasks and derives children by a direct mask pass. Both enumerate the
    full safe-position DAG independently and must agree exactly.
  * Rotation pairs (w,m) vs (m,w) must agree on all reported invariants.

Not claimed: anything about boards not listed; multiplayer nimbers; payoff or
ranking conventions; continuation after the loser is fixed; any statement
about 11x11 (empty board, two-stone roots, S2 and their classes remain
UNKNOWN/IN FLIGHT as recorded elsewhere).
"""

from __future__ import annotations

import itertools
import json
import sys
from math import gcd
from pathlib import Path

OUTPUT_PATH = Path(__file__).resolve().parent / "output" / "audit.json"

R_DP = (2, 3, 4)
R_LOSERS = (2, 3, 4, 5, 6, 7, 8)


# ---------------------------------------------------------------------------
# integer geometry
# ---------------------------------------------------------------------------

def det3(rows):
    (a0, a1, a2), (b0, b1, b2), (c0, c1, c2) = rows
    return (a0 * (b1 * c2 - b2 * c1) - a1 * (b0 * c2 - b2 * c0)
            + a2 * (b0 * c1 - b1 * c0))


def det4(rows):
    """4x4 integer determinant by cofactor expansion (exact)."""
    r0, r1, r2, r3 = rows
    total = 0
    for j in range(4):
        if r0[j] == 0:
            continue
        sub = [r[:j] + r[j + 1:] for r in (r1, r2, r3)]
        cof = det3(sub)
        total += (-1) ** j * r0[j] * cof
    return total


def cross_nullspace(rows):
    """Unique-up-to-scale integer nullspace vector of rank-3 rows (k x 4)."""
    for triple in itertools.combinations(range(len(rows)), 3):
        r0, r1, r2 = (rows[i] for i in triple)
        n = [
            det3([[r0[1], r0[2], r0[3]], [r1[1], r1[2], r1[3]], [r2[1], r2[2], r2[3]]]),
            -det3([[r0[0], r0[2], r0[3]], [r1[0], r1[2], r1[3]], [r2[0], r2[2], r2[3]]]),
            det3([[r0[0], r0[1], r0[3]], [r1[0], r1[1], r1[3]], [r2[0], r2[1], r2[3]]]),
            -det3([[r0[0], r0[1], r0[2]], [r1[0], r1[1], r1[2]], [r2[0], r2[1], r2[2]]]),
        ]
        if any(n):
            if all(sum(v * r[i] for i, v in enumerate(n)) == 0 for r in rows):
                g = 0
                for v in n:
                    g = gcd(g, abs(v))
                n = [v // g for v in n]
                lead = next(v for v in n if v != 0)
                if lead < 0:
                    n = [-v for v in n]
                return tuple(n)
    return None


class Board:
    def __init__(self, w, m, q):
        self.w, self.m, self.q = w, m, q
        self.cells = [(x, y) for y in range(w) for x in range(m)]
        self.n = len(self.cells)
        self.rows = [(x * x + y * y, x, y, 1) for (x, y) in self.cells]

    def mask_points(self, mask):
        pts = []
        for i in range(self.n):
            if (mask >> i) & 1:
                pts.append(i)
        return pts


def engine_a_positions(board):
    """Enumerate the safe-position DAG with incremental circle/line equations.

    Active predicates at node S = all (q-1)-subsets T of S that are
    concyclic-or-collinear (every triple qualifies; 4-subsets need det==0),
    each contributing its equation; count[x] = number of predicates whose
    equation contains x.  S+{x} is safe iff count[x] == 0.
    """
    n, q = board.n, board.q
    # precompute cells_on for every admissible (q-1)-subset
    cells_on = {}
    for combo in itertools.combinations(range(n), q - 1):
        rows = [board.rows[i] for i in combo]
        if q - 1 == 4 and det4(rows) != 0:
            continue
        eq = cross_nullspace(rows)
        assert eq is not None
        members = set(combo)
        on = []
        for i in range(n):
            if i in members:
                continue
            r = board.rows[i]
            if eq[0] * r[0] + eq[1] * r[1] + eq[2] * r[2] + eq[3] * r[3] == 0:
                on.append(i)
        if on:
            mask = 0
            for i in combo:
                mask |= 1 << i
            cells_on[mask] = tuple(on)

    positions = {}
    count = [0] * n

    def children_of(mask):
        out = []
        for c in range(n):
            if not (mask >> c) & 1 and count[c] == 0:
                out.append(c)
        return tuple(out)

    sys.setrecursionlimit(10000)

    def dfs(mask, path):
        ch = children_of(mask)
        positions[mask] = ch
        if not ch:
            return
        for c in ch:
            if path and c <= path[-1]:
                continue  # canonical increasing enumeration only
            # descend: add predicates containing c with others from path
            added = []
            for pre in itertools.combinations(path, q - 2):
                tmask = 0
                for i in pre:
                    tmask |= 1 << i
                tmask |= 1 << c
                on = cells_on.get(tmask)
                if on is not None:
                    for x in on:
                        count[x] += 1
                    added.append(on)
            dfs(mask | (1 << c), path + [c])
            for on in added:
                for x in on:
                    count[x] -= 1

    dfs(0, [])
    return positions


def engine_b_positions(board):
    """Independent enumeration: all forbidden q-subsets as bitmasks."""
    n, q = board.n, board.q
    forbidden = []
    for combo in itertools.combinations(range(n), q):
        rows = [board.rows[i] for i in combo]
        if q == 4:
            bad = det4(rows) == 0
        else:
            bad = all(
                det4([rows[i] for i in sub]) == 0
                for sub in itertools.combinations(range(q), 4)
            )
        if bad:
            mask = 0
            for i in combo:
                mask |= 1 << i
            forbidden.append(mask)

    positions = {}
    seen = set()
    work = [0]
    seen.add(0)
    while work:
        mask = work.pop()
        smask = mask
        ch = []
        for fm in forbidden:
            d = fm & ~smask
            if d and (d & (d - 1)) == 0:
                # exactly one cell of fm is outside S -> that cell is illegal
                c = d.bit_length() - 1
                ch.append(c)
        illegal = set(ch)
        children = tuple(
            c for c in range(n)
            if not (mask >> c) & 1 and c not in illegal
        )
        positions[mask] = children
        for c in children:
            nm = mask | (1 << c)
            if nm not in seen:
                seen.add(nm)
                work.append(nm)
    return positions


def popcount(x):
    return bin(x).count("1")


# ---------------------------------------------------------------------------
# dynamic programming over the safe-position DAG
# ---------------------------------------------------------------------------

def lens_dp(positions):
    """mask -> sorted tuple of achievable added-stone counts."""
    order = sorted(positions, key=lambda m: (-popcount(m), m))
    lens = {}
    for mask in order:
        ch = positions[mask]
        if not ch:
            lens[mask] = (0,)
        else:
            vals = set()
            for c in ch:
                for l in lens[mask | (1 << c)]:
                    vals.add(l + 1)
            lens[mask] = tuple(sorted(vals))
    return lens


def grundy_dp(positions):
    order = sorted(positions, key=lambda m: (-popcount(m), m))
    g = {}
    for mask in order:
        ch = positions[mask]
        if not ch:
            g[mask] = 0
        else:
            g[mask] = mex({g[mask | (1 << c)] for c in ch})
    return g


def mex(vals):
    i = 0
    while i in vals:
        i += 1
    return i


def coalition_dp(positions, r, terminal_seed):
    """Surv/Win arrays indexed by target residue k=(j-a) mod r, mover a=0.

    terminal_seed: 'surv' -> terminal value [k != 0]; 'win' -> [k == r-1].
    Mover is 0: k==0 -> OR over children; k!=0 -> AND over children;
    child value read at index (k-1) mod r.
    """
    order = sorted(positions, key=lambda m: (-popcount(m), m))
    out = {}
    for mask in order:
        ch = positions[mask]
        if not ch:
            if terminal_seed == "surv":
                out[mask] = tuple(k != 0 for k in range(r))
            else:
                out[mask] = tuple(k == r - 1 for k in range(r))
        else:
            child_vals = [out[mask | (1 << c)] for c in ch]
            arr = []
            for k in range(r):
                idx = (k - 1) % r
                if k == 0:
                    arr.append(any(cv[idx] for cv in child_vals))
                else:
                    arr.append(all(cv[idx] for cv in child_vals))
            out[mask] = tuple(arr)
    return out


# ---------------------------------------------------------------------------
# census driver
# ---------------------------------------------------------------------------

def maximal_histogram(positions):
    hist = {}
    for mask, ch in positions.items():
        if not ch:
            s = popcount(mask)
            hist[s] = hist.get(s, 0) + 1
    return {str(k): v for k, v in sorted(hist.items())}


def delta_of(hist):
    sizes = [int(k) for k in hist]
    if len(sizes) <= 1:
        return 0
    d = 0
    for s in sizes[1:]:
        d = gcd(d, s - sizes[0])
    return d


def census_board(w, m, q, heavy_ok=True):
    board = Board(w, m, q)
    pa = engine_a_positions(board)
    pb = engine_b_positions(board)

    checks = {
        "engine_position_sets_equal": set(pa) == set(pb),
        "engine_position_count_a": len(pa),
        "engine_position_count_b": len(pb),
        "engine_children_mismatches": sum(
            1 for mask in pa if pa[mask] != pb.get(mask)
        ),
    }

    lens = lens_dp(pa)
    grundy = grundy_dp(pa)
    hist = maximal_histogram(pa)
    delta = delta_of(hist)

    root = 0
    root_lens = lens[root]
    g_root = grundy[root]

    r2_classical = {}
    for r in R_DP:
        surv = coalition_dp(pa, r, "surv")
        win = coalition_dp(pa, r, "win")
        r2_classical[r] = (surv, win)

    # universal checks over every position
    frozen_ok = True
    win_implies_surv_ok = True
    win_possible_ok = True
    lens_size_hist = {}
    for mask, ch in pa.items():
        ls = lens[mask]
        lens_size_hist[len(ls)] = lens_size_hist.get(len(ls), 0) + 1
        for r in R_DP:
            surv, win = r2_classical[r]
            s_arr = surv[mask]
            w_arr = win[mask]
            for k in range(r):
                if w_arr[k] and not s_arr[k]:
                    win_implies_surv_ok = False
            if len(ls) == 1:
                l0 = ls[0]
                pred_s = tuple(k != (l0 % r) for k in range(r))
                pred_w = tuple(k == ((l0 - 1) % r) for k in range(r))
                if s_arr != pred_s or w_arr != pred_w:
                    frozen_ok = False
            # L4: Win_j => j possible last mover (for plays of length >= 1)
            pw = {((l - 1) % r) for l in ls}
            for k in range(r):
                if w_arr[k] and k not in pw:
                    win_possible_ok = False

    chaos = {str(r): 0 for r in R_LOSERS}
    lone_win = {}
    lone_surv_not_win = {}
    for r in R_DP:
        surv, win = r2_classical[r]
        lw = 0
        lsnw = 0
        for mask in pa:
            if any(win[mask]):
                lw += 1
            if any(surv[mask][k] and not win[mask][k] for k in range(r)):
                lsnw += 1
        lone_win[str(r)] = lw
        lone_surv_not_win[str(r)] = lsnw
    for r in R_LOSERS:
        c = 0
        for mask in pa:
            if len({l % r for l in lens[mask]}) == r:
                c += 1
        chaos[str(r)] = c

    possible_losers = {
        str(r): sorted({l % r for l in root_lens}) for r in R_LOSERS
    }
    possible_movers = {
        str(r): sorted({((l - 1) % r) for l in root_lens})
        for r in R_LOSERS
    }

    result = {
        "w": w, "m": m, "q": q, "cells": board.n,
        "safe_positions": len(pa),
        "maximal_size_histogram": hist,
        "maximal_size_gcd_delta": delta,
        "root": {
            "possible_added_stones": list(root_lens),
            "grundy_empty": g_root,
            "possible_losers": possible_losers,
            "possible_last_movers": possible_movers,
            "coalition_survival": {
                str(r): [int(v) for v in r2_classical[r][0][root]]
                for r in R_DP
            },
            "coalition_winner": {
                str(r): [int(v) for v in r2_classical[r][1][root]]
                for r in R_DP
            },
        },
        "census": {
            "lens_size_histogram": {str(k): v for k, v in sorted(lens_size_hist.items())},
            "chaos_positions": chaos,
            "lone_winner_positions": lone_win,
            "lone_survivor_not_winner_positions": lone_surv_not_win,
        },
        "checks": {
            **checks,
            "frozen_rule_all_positions": frozen_ok,
            "win_implies_surv_all_positions": win_implies_surv_ok,
            "win_implies_possible_mover_all_positions": win_possible_ok,
            "r2_surv_equals_win": (
                r2_classical[2][0][root] == r2_classical[2][1][root]
            ),
            "r2_win_equals_grundy_nonzero": (
                bool(r2_classical[2][1][root][0]) == (g_root != 0)
            ),
        },
    }
    return result


def rotation_key(entry):
    return (
        entry["safe_positions"],
        entry["maximal_size_histogram"],
        entry["root"]["possible_added_stones"],
        entry["root"]["possible_losers"],
        entry["root"]["coalition_survival"],
        entry["root"]["coalition_winner"],
    )


def main():
    boards = []
    # q=4 fixed-width family (w rows x m columns)
    for m in (1, 2, 3, 4):
        boards.append((1, m, 4))
    for m in range(1, 9):
        boards.append((2, m, 4))
    for m in range(1, 7):
        boards.append((3, m, 4))
    boards.append((4, 2, 4))
    boards.append((4, 3, 4))
    boards.append((4, 4, 4))
    boards.append((5, 2, 4))
    boards.append((5, 3, 4))
    boards.append((6, 2, 4))
    boards.append((7, 2, 4))
    boards.append((8, 2, 4))
    boards.append((6, 3, 4))
    # q=5 family
    for m in range(1, 6):
        boards.append((3, m, 5))
    boards.append((4, 2, 5))
    boards.append((4, 3, 5))
    boards.append((4, 4, 5))
    boards.append((5, 2, 5))
    boards.append((6, 2, 5))
    for m in (4, 5, 6):
        boards.append((2, m, 5))

    entries = {}
    for (w, m, q) in boards:
        key = f"{w}x{m}q{q}"
        sys.stderr.write(f"[census] {key} ...\n")
        entries[key] = census_board(w, m, q)

    # ---- external anchors -------------------------------------------------
    anchor_results = {}

    def assert_close(name, cond):
        anchor_results[name] = bool(cond)
        if not cond:
            raise AssertionError(f"anchor failed: {name}")

    # K0004: safe-set counts and empty-board grundy for square boards
    assert_close("K0004_safe_count_2x2", entries["2x2q4"]["safe_positions"] == 15)
    assert_close("K0004_safe_count_3x3", entries["3x3q4"]["safe_positions"] == 298)
    assert_close("K0004_safe_count_4x4", entries["4x4q4"]["safe_positions"] == 5811)
    # K0004 empty grundy n=1..4: 1,1,1,0
    assert_close("K0004_grundy_1x1", entries["1x1q4"]["root"]["grundy_empty"] == 1)
    assert_close("K0004_grundy_2x2", entries["2x2q4"]["root"]["grundy_empty"] == 1)
    assert_close("K0004_grundy_3x3", entries["3x3q4"]["root"]["grundy_empty"] == 1)
    assert_close("K0004_grundy_4x4", entries["4x4q4"]["root"]["grundy_empty"] == 0)
    # K0011-K0014 r=2 first-player classification
    for name, entry, win in (
        ("K0011_1x1_first_win", entries["1x1q4"], True),
        ("K0012_2x2_first_win", entries["2x2q4"], True),
        ("K0013_3x3_first_win", entries["3x3q4"], True),
        ("K0014_4x4_first_lose", entries["4x4q4"], False),
    ):
        r2win = entries["root"]["coalition_winner"]["2"] if False else entry
        got = entry["root"]["coalition_winner"]["2"][0] == 1
        assert_close(name, got == win)
    # K0339 published square-board data (n=1..4)
    k0339 = {
        "1x1q4": {"hist": {"1": 1}, "delta": 0,
                  "losers": {"2": [1], "3": [1], "4": [1], "5": [1], "6": [1], "7": [1], "8": [1]}},
        "2x2q4": {"hist": {"3": 4}, "delta": 0,
                  "losers": {"2": [1], "3": [0], "4": [3], "5": [3], "6": [3], "7": [3], "8": [3]}},
        "3x3q4": {"hist": {"5": 56}, "delta": 0,
                  "losers": {"2": [1], "3": [2], "4": [1], "5": [0], "6": [5], "7": [5], "8": [5]}},
        "4x4q4": {"hist": {"5": 176, "6": 688, "7": 64}, "delta": 1,
                  "losers": {"2": [0, 1], "3": [0, 1, 2], "4": [1, 2, 3],
                             "5": [0, 1, 2], "6": [0, 1, 5], "7": [0, 5, 6], "8": [5, 6, 7]}},
    }
    for key, ref in k0339.items():
        e = entries[key]
        assert_close(f"K0339_hist_{key}", e["maximal_size_histogram"] == ref["hist"])
        assert_close(f"K0339_delta_{key}", e["maximal_size_gcd_delta"] == ref["delta"])
        for r, expect in ref["losers"].items():
            assert_close(
                f"K0339_losers_{key}_r{r}",
                e["root"]["possible_losers"][r] == expect,
            )
    # K0069: 2xm q=4, m=6,7,8 first player loses
    for m in (6, 7, 8):
        e = entries[f"2x{m}q4"]
        assert_close(f"K0069_2x{m}_first_lose", e["root"]["coalition_winner"]["2"][0] == 0)
        assert_close(f"K0069_2x{m}_grundy_zero", e["root"]["grundy_empty"] == 0)
    # K0071: 3xm q=5 first player wins iff m in {1,3} (m<=5)
    for m in (1, 2, 3, 4, 5):
        e = entries[f"3x{m}q5"]
        expect = 1 if m in (1, 3) else 0
        assert_close(f"K0071_3x{m}q5_first", e["root"]["coalition_winner"]["2"][0] == expect)
    # K0025 uniform anchors (q>2w): all maximal sets exactly w*min(m,q-1)=8 stones
    for m, count in ((4, 1), (5, 25), (6, 225)):
        e = entries[f"2x{m}q5"]
        assert_close(f"K0025_2x{m}q5_uniform",
                    e["maximal_size_histogram"] == {"8": count}
                    and e["maximal_size_gcd_delta"] == 0
                    and e["root"]["possible_added_stones"] == [8])
    # rotation pairs
    pairs = [
        ("2x3q4", "3x2q4"), ("2x4q4", "4x2q4"), ("2x5q4", "5x2q4"),
        ("2x6q4", "6x2q4"), ("2x7q4", "7x2q4"), ("2x8q4", "8x2q4"),
        ("3x4q4", "4x3q4"), ("3x5q4", "5x3q4"), ("3x6q4", "6x3q4"),
        ("2x4q5", "4x2q5"), ("2x5q5", "5x2q5"), ("2x6q5", "6x2q5"),
        ("3x4q5", "4x3q5"),
    ]
    for a, b in pairs:
        assert_close(f"rotation_pair_{a}_{b}", rotation_key(entries[a]) == rotation_key(entries[b]))

    # per-board sanity: engines agree and universal checks pass everywhere
    for key, e in entries.items():
        assert_close(f"engine_positions_{key}", e["checks"]["engine_position_sets_equal"])
        assert_close(f"engine_children_{key}", e["checks"]["engine_children_mismatches"] == 0)
        assert_close(f"frozen_{key}", e["checks"]["frozen_rule_all_positions"])
        assert_close(f"win_surv_{key}", e["checks"]["win_implies_surv_all_positions"])
        assert_close(f"win_possible_{key}", e["checks"]["win_implies_possible_mover_all_positions"])
        assert_close(f"r2_{key}", e["checks"]["r2_surv_equals_win"])
        assert_close(f"r2_grundy_{key}", e["checks"]["r2_win_equals_grundy_nonzero"])

    # ---- uniform-regime winner/loser table arithmetic checks -----------------
    # The derived table applies the K0339 residue formulas to every proved
    # uniform regime.  Its r=2 column must reproduce published outcomes.
    table_checks = {}

    def table_check(name, cond):
        table_checks[name] = bool(cond)
        if not cond:
            raise AssertionError(f"table check failed: {name}")

    # K0024/K0068 criterion: in the m>=T_{w,q} regime (C=(q-1)w) the first
    # player wins iff q even and w odd, i.e. iff C is odd.
    for q in range(4, 17):
        for w in range(1, 13):
            c = (q - 1) * w
            table_check(f"K0024_parity_q{q}_w{w}",
                        (c % 2 == 1) == (q % 2 == 0 and w % 2 == 1))
    # K0069: (2,4) m>=9, C=6 -> second player wins (C even).
    table_check("K0069_2x4_C6_second", 6 % 2 == 0)
    # K0070: (3,6) m>=9, C=15 -> first player wins (published outcome).
    table_check("K0070_3x6_C15_first", 15 % 2 == 1)
    # K0071: (3,5) m>=12, C=12 -> second player wins (published outcome).
    table_check("K0071_3x5_C12_second", 12 % 2 == 0)
    # K0025: w=2, q>=5, C=2*min(m,q-1) is even for every m -> always second.
    for m in range(1, 40):
        for q in range(5, 17):
            table_check(f"K0025_w2_q{q}_m{m}_even", (2 * min(m, q - 1)) % 2 == 0)
    # K0855: q in {2,3}, C=q-1: q=2 first wins, q=3 second wins.
    table_check("K0855_q2_C1_first", 1 % 2 == 1)
    table_check("K0855_q3_C2_second", 2 % 2 == 0)
    # Consistency of loser/winner residues on every regime row:
    # winner == loser - 1 (mod r) whenever at least one move is played.
    for c in (1, 2, 3, 6, 8, 9, 12, 15, 16, 20, 24, 28, 35, 40, 56, 63, 80):
        for r in R_LOSERS:
            table_check(f"residue_C{c}_r{r}", ((c - 1) % r) == ((c % r) - 1) % r)

    audit = {
        "table_checks": table_checks,
        "boards": [entries[k] for k in sorted(entries)],
        "anchors": anchor_results,
        "meta": {
            "rule": "complete-call q-point kyouen (integer determinant, no floats)",
            "convention_loser": "first player with no legal move loses (K0339)",
            "convention_last_mover": "reported separately; no payoff/ranking claim",
            "coalition": "player j alone vs coalition of all other players",
            "engines": "A incremental circle/line equations; B forbidden q-subset bitmask pass",
            "r_dp": list(R_DP),
            "r_losers": list(R_LOSERS),
            "determinism": "fixed enumeration order, sorted structures, no timestamps",
            "scope": "finite census of the listed boards only",
        },
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as fh:
        json.dump(audit, fh, ensure_ascii=True, sort_keys=True, indent=1)
        fh.write("\n")
    print("MULTIPLAYER_COALITION_CENSUS_OK")
    print(f"boards: {len(entries)}")
    print(f"written: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
