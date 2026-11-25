#!/usr/bin/env python3
"""High-r completion of the 2xm q=4 family root coalition characterization.

Extends the published family root table (m=1..12, r=2..8, pushed with the
multiplayer-coalition census) to r=2..16 and machine-checks two universal
short-play theorems that close the whole family for every r >= 7:

  Theorem A (short-play targeting).  Let S be a position whose achievable
  play lengths are Lambda(S) and suppose max Lambda(S) < r.  Then the set of
  force-targetable players equals the set of possible losers
  { L mod r : L in Lambda(S) }.
  Proof.  (<=) Fix L in Lambda(S), a realizing play pi, and j = L mod r.
  Since L < r, the movers of pi are exactly P_0, ..., P_{L-1} and the victim
  P_j = P_L never moves in pi, so every move of pi is a coalition move;
  following pi ends the game at length L with P_j to move, so j loses.
  (=>) If j is not a possible loser then no play ends with j losing, so j
  survives under any strategy.

  Theorem B (short-play solo win).  Under the same hypothesis, and assuming
  safety is hereditary (every subset of a safe position is safe, hence every
  safe position is reachable from the root), player j alone can force being
  the last mover iff j = min(Lambda) - 1 and every safe position with
  min(Lambda) - 1 stones admits a one-move extension to a maximal (terminal)
  position.  In particular the root solo-win set is identical for every
  r > max Lambda(S).
  Proof.  See report.md, section "High-r completion".

For the 2xm q=4 family every board has max achievable root length 6
(m in {1,2,3}: C=2,3,4; m=4: {4,5}; m=5..8: {5,6}; m>=9: C=6 by K0069),
so r >= 7 puts every board in the short-play regime and the two theorems
determine the whole family root characterization for all r >= 7:
  - targeted = { L mod r : L in Lambda },
  - solo win = { min(Lambda) - 1 } iff the one-move-extension predicate
    holds (machine-checked false for m=4..8, true for uniform boards,
    where it recovers the frozen-collapse winner P_{(C-1) mod r}).

This script:
  1. recomputes r=2..8 and cross-checks against the published census audit
     (output/audit.json, family_2xm_q4_root rows),
  2. computes r=9..16 (new finite data),
  3. checks Theorems A and B and the structural constraints
     (Win => possible last mover; Win => Surv; targeted => possible loser)
     for every r in 2..16,
  4. evaluates the Theorem-B predicate directly on the position graph
     (independent of any coalition DP) and records a failing witness
     position for each non-uniform board.

Deterministic: fixed enumeration order, sorted structures, no randomness,
no timestamps.  Scope: the theorems are proved for all r > max Lambda; the
machine checks cover the family for r <= 16.
"""

import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE_PATH = HERE / "verify_multiplayer_coalition.py"
AUDIT_PATH = HERE / "output" / "audit.json"
OUTPUT_PATH = HERE / "output" / "family_high_r_audit.json"

R_LOW, R_HIGH = 2, 16
R_SHORT = 7  # every family board has max achievable length 6 < 7

_spec = importlib.util.spec_from_file_location("kmc_base", BASE_PATH)
base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(base)

Board = base.Board
engine_a_positions = base.engine_a_positions
coalition_dp = base.coalition_dp
lens_dp = base.lens_dp
popcount = base.popcount


def cells_of(mask, board):
    return [board.cells[i] for i in range(board.n) if mask >> i & 1]


def main():
    published = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
    pub_rows = published["family_2xm_q4_root"]["rows"]
    pub_by_m = {row["m"]: row for row in pub_rows}

    checks = {}

    def check(name, cond):
        checks[name] = bool(cond)
        if not cond:
            raise AssertionError(f"check failed: {name}")

    boards = []
    for m in range(1, 13):
        board = Board(2, m, 4)
        pa = engine_a_positions(board)
        lens = lens_dp(pa)
        lam = list(lens[0])
        l_min, l_max = min(lam), max(lam)

        hist = {}
        for mask, ch in pa.items():
            if not ch:
                s = popcount(mask)
                hist[s] = hist.get(s, 0) + 1
        uniform = len(hist) == 1
        c_uniform = next(iter(hist)) if uniform else None

        # ---- Theorem B predicate, evaluated directly on the position graph
        j0 = l_min - 1
        j0_masks = [mask for mask in sorted(pa) if popcount(mask) == j0]
        # no terminal of size j0 can exist (its size would be < l_min)
        check(f"no_terminal_size{j0}_2x{m}", all(pa[mask] for mask in j0_masks))
        pred_win = True
        pred_witness = None
        for mask in j0_masks:
            if not any(not pa[mask | (1 << cell)] for cell in pa[mask]):
                pred_win = False
                if pred_witness is None:
                    pred_witness = sorted(cells_of(mask, board))
                break
        expected_short_win = [j0] if pred_win else []

        # ---- coalition DP for r = 2..16
        win_by_r, targ_by_r = {}, {}
        for r in range(R_LOW, R_HIGH + 1):
            surv = coalition_dp(pa, r, "surv")
            win = coalition_dp(pa, r, "win")
            win_by_r[str(r)] = [k for k in range(r) if win[0][k]]
            targ_by_r[str(r)] = [k for k in range(r) if not surv[0][k]]

        # ---- cross-check r=2..8 against the published census audit
        pub = pub_by_m[m]
        for r in range(2, 9):
            check(f"published_win_2x{m}_r{r}",
                  win_by_r[str(r)] == pub["root_win_by_r"][str(r)])
            check(f"published_targ_2x{m}_r{r}",
                  targ_by_r[str(r)] == pub["root_targeted_by_r"][str(r)])

        # ---- structural constraints for every r
        for r in range(R_LOW, R_HIGH + 1):
            possible_losers = {L % r for L in lam}
            possible_movers = {(L - 1) % r for L in lam}
            check(f"L4_win_subset_movers_2x{m}_r{r}",
                  set(win_by_r[str(r)]) <= possible_movers)
            check(f"targ_subset_possible_2x{m}_r{r}",
                  set(targ_by_r[str(r)]) <= possible_losers)

        # ---- Theorems A and B in the short-play regime r=7..16
        for r in range(R_SHORT, R_HIGH + 1):
            check(f"short_regime_2x{m}_r{r}", r > l_max)
            check(f"theoremA_targeted_2x{m}_r{r}",
                  targ_by_r[str(r)] == sorted({L % r for L in lam}))
            check(f"theoremB_win_2x{m}_r{r}",
                  win_by_r[str(r)] == [j % r for j in expected_short_win])
            # in the short regime the solo winner j0 = l_min - 1 satisfies
            # j0 < l_min, so it is never a possible loser (Theorem B + A)
            check(f"short_win_losers_disjoint_2x{m}_r{r}",
                  not (set(win_by_r[str(r)]) & {L % r for L in lam}))
        indep = {frozenset(win_by_r[str(r)]) for r in range(R_SHORT, R_HIGH + 1)}
        check(f"win_r_independent_2x{m}", len(indep) == 1)

        # ---- explicit frozen arrays for uniform boards, r=7..16
        if uniform:
            for r in range(R_SHORT, R_HIGH + 1):
                check(f"frozen_win_2x{m}_r{r}",
                      win_by_r[str(r)] == [(c_uniform - 1) % r])
                check(f"frozen_targ_2x{m}_r{r}",
                      targ_by_r[str(r)] == [c_uniform % r])
            check(f"uniform_predicate_2x{m}", pred_win is True)

        boards.append({
            "m": m,
            "uniform": uniform,
            "C": c_uniform,
            "achievable_lengths": lam,
            "min_length": l_min,
            "max_length": l_max,
            "solo_win_candidate": j0,
            "solo_win_predicate": bool(pred_win),
            "solo_win_witness": pred_witness,
            "root_win_by_r": win_by_r,
            "root_targeted_by_r": targ_by_r,
        })

    audit = {
        "boards": boards,
        "checks": checks,
        "meta": {
            "family": "2xm q=4, m=1..12, r=2..16",
            "theorem_a": (
                "if max achievable play length < r then force-targetable set "
                "= possible losers {L mod r}; proved in report.md"
            ),
            "theorem_b": (
                "under the same hypothesis and hereditary safety, solo "
                "forced last-mover win iff j = min(Lambda)-1 and every safe "
                "j-stone position has a one-move terminal extension; the "
                "solo-win set is r-independent for r > max(Lambda)"
            ),
            "short_regime_r": list(range(R_SHORT, R_HIGH + 1)),
            "published_crosscheck": "output/audit.json family_2xm_q4_root r=2..8",
            "engines": "A only; coalition DP identical to the census verifier",
            "determinism": "fixed enumeration order, sorted structures, no timestamps",
            "scope": (
                "finite machine check of the family for r<=16; theorems A/B "
                "are proved for all r > max achievable length, so the family "
                "root characterization holds for every r >= 7"
            ),
        },
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as fh:
        json.dump(audit, fh, ensure_ascii=True, sort_keys=True, indent=1)
        fh.write("\n")
    print("FAMILY_HIGH_R_OK")
    print(f"boards: {len(boards)}")
    print(f"checks: {len(checks)}")
    print(f"written: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
