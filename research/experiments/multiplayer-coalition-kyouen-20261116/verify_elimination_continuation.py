#!/usr/bin/env python3
"""Elimination continuation rules after the first loser (K0339 open remark).

K0339 fixes the rules at "the first player without a legal move is the
loser and the game ends" and explicitly leaves open ("resolves to state in
the item text): continuation after removing the loser.  This verifier
formalizes two natural continuation rules and machine-checks three
universal statements about them.

Rules (both extend K0339 phase 1 verbatim: play rotates cyclically, the
player to move at a maximal safe position is stuck and eliminated first).

  Rule CASC (cascade, board unchanged): a stuck player is eliminated and
    the board is left unchanged; the next player in cyclic order moves.
  Rule REMO (stone removal): a stuck player is eliminated and all stones
    that player owns are removed from the board; play continues with the
    next player in cyclic order among the survivors.

  Theorem C (cascade ranking, universal).  Under CASC the full ranking is
  determined by the terminal length alone: if the play ends at a maximal
  position of size L, the elimination order is P_{L mod r}, P_{(L+1) mod r},
  ... (cyclic, consecutive), and the survivor is P_{(L-1) mod r}, i.e. the
  last mover.  Hence the possible-survivor set from any position S with
  mover a is exactly the possible last-mover set {(a+ell-1) mod r}, and
  coalition Win_j (K0858) coincides with "j can force sole survival".
  Strategy independence of the whole ranking is equivalent to r | Delta
  (K0339's condition, now for the ranking, not just the loser).

  Theorem D (removal determinism on uniform boards, universal).  If every
  maximal safe set has the same size C (Delta = 0), then under REMO the
  complete elimination sequence is independent of strategies and of the
  geometry: it is the output of an explicit count recursion in (C, r)
  (uniform_elimination below).  Phase lengths equal C minus current board
  size; the loser of a phase is the player to move when the board refills
  to C; all of the loser's stones are then removed.

  Counterexample (Delta != 0 sharpness; r | Delta does NOT suffice for
  REMO).  A synthetic downward-closed family with maximal sets of sizes 6
  and 9 (Delta = 3): with r = 3 the first loser is always P_0 (3 | 3, so
  K0339 fixes it), yet the survivor is P_2 for plays ending at the 6-set
  and P_1 for plays ending at the 9-set, so the ranking is
  strategy-dependent under REMO while CASC stays determined.

This script:
  1. brute-forces the full game tree of both rules on small uniform and
     non-uniform boards (r = 2..6) with ownership tracking (REMO),
  2. checks Theorem C per outcome, the possible-survivor = possible
     last-mover identity against recomputed lens data, and
     determinacy <==> r | Delta against the published census deltas,
  3. checks Theorem D: brute-force REMO outcome on uniform boards is the
     singleton predicted by the arithmetic recursion,
  4. checks the synthetic counterexample (first loser fixed, survivor
     strategy-dependent under REMO, determined under CASC),
  5. emits the geometry-free (C, r) elimination table for C = 1..12,
     r = 2..8, which instantiates every uniform regime by reading off
     its (C, r) (e.g. 2xm q=4 uniform boards m in {1,2,3,9..12}).

Deterministic: fixed enumeration order, sorted structures, no randomness,
no timestamps.  Scope: the theorems are proved for all finite downward-
closed placement games; the machine checks cover the listed boards.
Stone ownership is tracked only for REMO; CASC needs none.
"""

import importlib.util
import json
from math import gcd

from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE_PATH = HERE / "verify_multiplayer_coalition.py"
AUDIT_PATH = HERE / "output" / "audit.json"
OUTPUT_PATH = HERE / "output" / "elimination_continuation_audit.json"

_spec = importlib.util.spec_from_file_location("kmc_base", BASE_PATH)
base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(base)

Board = base.Board
engine_a_positions = base.engine_a_positions


# ---------------------------------------------------------------------------
# Rule semantics as full game-tree searches.
# ---------------------------------------------------------------------------

def cascade_outcomes(positions, r):
    """All possible (elimination order, survivor) under CASC from the root.

    positions: dict mask -> tuple of safe child cells.
    Returns a sorted tuple of (elim_tuple, survivor) pairs.
    """
    memo = {}

    def rec(placed, active, turn):
        if len(active) == 1:
            return (((), active[0]),)
        key = (placed, active, turn)
        if key in memo:
            return memo[key]
        children = positions[placed]
        if not children:
            loser = active[turn]
            rest = tuple(p for p in active if p != loser)
            sub = rec(placed, rest, turn % len(rest))
            out = tuple(((loser,) + e, s) for (e, s) in sub)
        else:
            outs = set()
            nturn = (turn + 1) % len(active)
            for c in children:
                for (e, s) in rec(placed | (1 << c), active, nturn):
                    outs.add((e, s))
            out = tuple(sorted(outs))
        memo[key] = out
        return out

    return rec(0, tuple(range(r)), 0)


def removal_outcomes(positions, r):
    """All possible (elimination order, survivor) under REMO from the root.

    owners are tracked per original player id (bitmasks over cells); the
    eliminated player's stones are removed from the board.
    """
    memo = {}

    def rec(placed, owners, active, turn):
        if len(active) == 1:
            return (((), active[0]),)
        key = (placed, owners, active, turn)
        if key in memo:
            return memo[key]
        children = positions[placed]
        if not children:
            loser = active[turn]
            rest = tuple(p for p in active if p != loser)
            ow = list(owners)
            ow[loser] = 0
            new_placed = placed & ~owners[loser]
            sub = rec(new_placed, tuple(ow), rest, turn % len(rest))
            out = tuple(((loser,) + e, s) for (e, s) in sub)
        else:
            outs = set()
            mover = active[turn]
            nturn = (turn + 1) % len(active)
            for c in children:
                ow = list(owners)
                ow[mover] |= 1 << c
                for (e, s) in rec(placed | (1 << c), tuple(ow), active, nturn):
                    outs.add((e, s))
            out = tuple(sorted(outs))
        memo[key] = out
        return out

    return rec(0, tuple(0 for _ in range(r)), tuple(range(r)), 0)


def uniform_elimination(C, r):
    """Theorem D arithmetic recursion: elimination order and survivor.

    Returns (elimination tuple, survivor) for a uniform board (all
    maximal safe sets have size C) with r players, P_0 to move first.
    Deterministic function of (C, r) only.
    """
    active = list(range(r))
    counts = [0] * r
    turn = 0
    elimination = []
    while len(active) > 1:
        k = len(active)
        s = sum(counts[p] for p in active)
        ell = C - s
        for m in range(ell):
            counts[active[(turn + m) % k]] += 1
        li = (turn + ell) % k
        loser = active[li]
        elimination.append(loser)
        counts[loser] = 0
        active.pop(li)
        if active:
            turn = li % len(active)
    return tuple(elimination), active[0]


def cascade_formula(L, r):
    """Theorem C prediction for a play ending at terminal size L."""
    j1 = L % r
    elim = tuple((j1 + t) % r for t in range(r - 1))
    surv = (L - 1) % r
    return elim, surv


def synthetic_family_positions():
    """Downward-closed family with maximal sets A (size 6) and B (size 9).

    Cells 0..5 encode x1..x6 (A), cells 6..11 encode y1..y6;
    B = {x1, x2, x3} U {y1..y6} = cells {0, 1, 2} U {6..11}.
    Delta = gcd(9 - 6) = 3.  Safe sets = subsets of A or of B.
    """
    A = (1 << 6) - 1
    B = (1 << 3) - 1 | (((1 << 6) - 1) << 6)
    safe = set()
    for mask in range(1 << 12):
        if mask & ~A == 0 or mask & ~B == 0:
            safe.add(mask)
    positions = {}
    for mask in safe:
        children = []
        for c in range(12):
            if not (mask >> c) & 1 and (mask | (1 << c)) in safe:
                children.append(c)
        positions[mask] = tuple(children)
    return positions, sorted(m for m in safe
                              if not positions[m]), 3  # positions, maximal, delta


def root_lens(positions):
    """Achievable root lengths (sizes of maximal positions)."""
    sizes = set()
    stack = [0]
    seen = {0}
    while stack:
        mask = stack.pop()
        ch = positions[mask]
        if not ch:
            sizes.add(bin(mask).count("1"))
        for c in ch:
            nxt = mask | (1 << c)
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return sorted(sizes)


def main():
    out = {"meta": {
        "script": "verify_elimination_continuation.py",
        "rules": {
            "CASC": "stuck player eliminated, board unchanged, next cyclic "
                    "survivor moves (Theorem C applies to all games)",
            "REMO": "stuck player eliminated and their stones removed, next "
                    "cyclic survivor moves (Theorem D applies when Delta=0)",
        },
        "claims": [
            "Theorem C: CASC ranking is determined by terminal length mod r; "
            "survivor = last mover; determinacy <==> r | Delta",
            "Theorem D: REMO on a Delta=0 board is fully determined by (C, r) "
            "via the count recursion",
            "Counterexample: Delta=3 family, r=3: first loser fixed (r|Delta) "
            "but REMO survivor is strategy-dependent; CASC stays determined",
        ],
        "deterministic": True,
        "scope": "theorems universal for finite downward-closed placement "
                 "games; machine checks cover the listed boards only",
    }}
    checks = []

    def check(name, cond, detail=None):
        checks.append({"name": name, "ok": bool(cond),
                       **({"detail": detail} if detail else {})})
        if not cond:
            print("FAIL:", name, detail or "")

    audit = json.loads(AUDIT_PATH.read_text())
    deltas = {(b["w"], b["m"], b["q"]): b["maximal_size_gcd_delta"]
              for b in audit["boards"]}
    histograms = {(b["w"], b["m"], b["q"]): b["maximal_size_histogram"]
                   for b in audit["boards"]}

    # ------------------------------------------------------------------
    # 1. CASC on uniform and non-uniform small boards.
    # ------------------------------------------------------------------
    casc = {}
    casc_boards = [
        (2, 2, 4), (2, 3, 4), (3, 3, 4), (2, 4, 4), (2, 5, 4), (2, 6, 4),
        (3, 4, 4), (2, 4, 5), (3, 2, 5),
    ]
    for (w, m, q) in casc_boards:
        board = Board(w, m, q)
        positions = engine_a_positions(board)
        lens = root_lens(positions)
        delta = deltas[(w, m, q)]
        key = f"{w}x{m}q{q}"
        casc[key] = {"maximal_sizes": lens, "delta": delta}
        for r in range(2, 7):
            outcomes = cascade_outcomes(positions, r)
            # structure: each outcome is the consecutive cyclic run
            for (elim, surv) in outcomes:
                j1 = elim[0]
                # structure: elimination is the consecutive cyclic run from j1
                ok_struct = elim == tuple((j1 + t) % r for t in range(r - 1))
                ok_struct = ok_struct and surv == (j1 - 1) % r
                check(f"casc_structure:{key}:r{r}", ok_struct,
                      {"elim": list(elim), "surv": surv})
            # first losers = possible losers (L mod r)
            possible_losers = sorted({L % r for L in lens})
            first_losers = sorted({elim[0] for (elim, _) in outcomes})
            check(f"casc_first_losers:{key}:r{r}",
                  first_losers == possible_losers,
                  {"first_losers": first_losers,
                   "possible_losers": possible_losers})
            # survivors = possible last movers
            possible_movers = sorted({(L - 1) % r for L in lens})
            survivors = sorted({surv for (_, surv) in outcomes})
            check(f"casc_survivors_are_last_movers:{key}:r{r}",
                  survivors == possible_movers,
                  {"survivors": survivors, "possible_last_movers": possible_movers})
            # per-outcome terminal-length consistency
            for (elim, surv) in outcomes:
                j1 = elim[0]
                if any(L % r == j1 and surv == (L - 1) % r for L in lens):
                    ok = True
                else:
                    ok = False
                check(f"casc_outcome_from_formula:{key}:r{r}:{j1}", ok,
                      {"elim": list(elim), "surv": surv})
            # determinacy <==> r | delta (delta 0 -> always determined)
            determined = len(outcomes) == 1
            expect_det = delta == 0 or delta % r == 0
            check(f"casc_determinacy_iff_r_divides_delta:{key}:r{r}",
                  determined == expect_det,
                  {"determined": determined, "delta": delta})
            casc[key][f"r{r}"] = {
                "n_outcomes": len(outcomes),
                "outcomes": [[list(e), s] for (e, s) in outcomes],
                "determined": determined,
            }
    out["cascade_boards"] = casc

    # ------------------------------------------------------------------
    # 2. REMO on uniform boards vs the Theorem D recursion.
    # ------------------------------------------------------------------
    remo = {}
    remo_boards = [
        (2, 2, 4, range(2, 7)),
        (2, 3, 4, range(2, 7)),
        (3, 2, 5, range(2, 6)),
        (2, 4, 5, range(2, 5)),
        (3, 3, 5, range(2, 4)),
    ]
    for (w, m, q, rrange) in remo_boards:
        board = Board(w, m, q)
        positions = engine_a_positions(board)
        lens = root_lens(positions)
        check(f"remo_uniform_board:{w}x{m}q{q}", len(lens) == 1,
              {"maximal_sizes": lens})
        C = lens[0]
        key = f"{w}x{m}q{q}"
        remo[key] = {"C": C}
        for r in rrange:
            outcomes = removal_outcomes(positions, r)
            pred_elim, pred_surv = uniform_elimination(C, r)
            determined = len(outcomes) == 1
            ok = determined and outcomes[0] == (pred_elim, pred_surv)
            check(f"remo_matches_recursion:{key}:r{r}", ok,
                  {"outcomes": [[list(e), s] for (e, s) in outcomes],
                   "predicted": [list(pred_elim), pred_surv]})
            # first loser agrees with K0339 frozen rule: C mod r
            check(f"remo_first_loser_frozen:{key}:r{r}",
                  determined and outcomes[0][0][0] == C % r,
                  {"first_loser": outcomes[0][0][0], "C mod r": C % r})
            remo[key][f"r{r}"] = {
                "n_outcomes": len(outcomes),
                "outcome": [list(outcomes[0][0]), outcomes[0][1]]
                if outcomes else None,
                "predicted": [list(pred_elim), pred_surv],
                "determined": determined,
            }
        # r=2: REMO and CASC coincide (only one elimination ever happens)
        o_casc = cascade_outcomes(positions, 2)
        o_remo = removal_outcomes(positions, 2)
        check(f"remo_equals_casc_r2:{key}", o_casc == o_remo,
              {"casc": [[list(e), s] for (e, s) in o_casc],
               "remo": [[list(e), s] for (e, s) in o_remo]})
    out["removal_uniform"] = remo

    # ------------------------------------------------------------------
    # 3. Synthetic counterexample: Delta = 3.
    # ------------------------------------------------------------------
    positions, maximal_masks, delta = synthetic_family_positions()
    synth = {"delta": delta, "maximal_sizes":
             sorted(bin(mm).count("1") for mm in maximal_masks)}
    check("synth_maximal_sizes", synth["maximal_sizes"] == [6, 9],
          {"sizes": synth["maximal_sizes"]})
    check("synth_delta", delta == 3, {"delta": delta})
    for r in (2, 3):
        casc_out = cascade_outcomes(positions, r)
        remo_out = removal_outcomes(positions, r)
        # first loser fixed <==> r | delta
        first_losers = sorted({elim[0] for (elim, _) in remo_out})
        expect_fixed = delta % r == 0
        check(f"synth_first_loser_fixed:r{r}",
              (len(first_losers) == 1) == expect_fixed,
              {"first_losers": first_losers, "expect_fixed": expect_fixed})
        if r == 3:
            # K0339: first loser always P_0
            check("synth_r3_first_loser_is_P0", first_losers == [0],
                  {"first_losers": first_losers})
            # CASC determined with survivor P_2 (final mover of both lengths)
            check("synth_r3_casc_determined", len(casc_out) == 1
                  and casc_out[0] == ((0, 1), 2),
                  {"casc": [[list(e), s] for (e, s) in casc_out]})
            # REMO NOT determined: survivor P_2 via the 6-set, P_1 via the 9-set
            survivors = sorted({s for (_, s) in remo_out})
            check("synth_r3_remo_undetermined", len(remo_out) == 2
                  and survivors == [1, 2],
                  {"remo": [[list(e), s] for (e, s) in remo_out]})
            # each REMO outcome has first loser P_0
            check("synth_r3_remo_outcomes_start_P0",
                  all(e[0] == 0 for (e, _) in remo_out),
                  {"remo": [[list(e), s] for (e, s) in remo_out]})
        synth[f"r{r}"] = {
            "casc": [[list(e), s] for (e, s) in casc_out],
            "remo": [[list(e), s] for (e, s) in remo_out],
        }
    out["synthetic_counterexample"] = synth

    # ------------------------------------------------------------------
    # 4. Geometry-free (C, r) elimination table (Theorem D recursion).
    # ------------------------------------------------------------------
    table = {}
    for C in range(1, 13):
        rows = {}
        for r in range(2, 9):
            elim, surv = uniform_elimination(C, r)
            rows[str(r)] = {"elimination": list(elim), "survivor": surv}
        table[str(C)] = rows
    out["uniform_elimination_table"] = table

    # spot-check the table against small uniform family boards; the m>=9
    # uniform family boards (C=6) are covered by Theorem D itself and by
    # the whole-board C=6 board 3x2 q5, so no brute force is needed there.
    for (w, m, q) in [(2, 1, 4), (2, 2, 4), (2, 3, 4)]:
        board = Board(w, m, q)
        positions = engine_a_positions(board)
        lens = root_lens(positions)
        if len(lens) != 1:
            continue
        C = lens[0]
        for r in range(2, 7):
            pred = uniform_elimination(C, r)
            o = removal_outcomes(positions, r)
            check(f"table_spot:{w}x{m}q{q}:r{r}",
                  o == (pred,) if len(o) == 1 else False,
                  {"C": C, "outcomes": [[list(e), s] for (e, s) in o],
                   "predicted": [list(pred[0]), pred[1]]})

    # ------------------------------------------------------------------
    # 5. Summary.
    # ------------------------------------------------------------------
    n_fail = sum(1 for c in checks if not c["ok"])
    out["checks"] = checks
    out["summary"] = {
        "n_checks": len(checks),
        "n_fail": n_fail,
        "all_ok": n_fail == 0,
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(out, indent=1, sort_keys=True,
                                       ensure_ascii=False) + "\n")
    print(f"checks: {len(checks)}  fail: {n_fail}")
    print("wrote", OUTPUT_PATH)
    return n_fail == 0


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
