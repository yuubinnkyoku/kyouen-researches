# s_12 / s_13 constructive upper bounds (10-stone maximal safe witness on 12x12, 11-stone on 13x13): single-owner declaration note

Date: 2026-11-21T13:59Z
Lane: standard-board minimal-maximal size s_n lane (K0026/K0320/K0312/K0147/K0148/K0149 family), constructive upper-bound side for n=12 and n=13.
Declaration HEAD at write time: 2ca0ef3be0ef7de4473e70aba03dca3410ae9461 (latest main at 13:58Z).
Not a continuation of any claimed lane. The s_11 decision is owned by the a45a626d lane
(s11-minimal-maximal-8-9-decision, 8 <= s_11 <= 10); no prior declaration found for any
s_12/s_13 upper-witness target (search of research/log: no s_12/cross-board/minimal-maximal
declaration other than the s_11 one and the K0320 n-1 constructive family, which publishes
s_12 <= 11 and s_13 <= 12 without claiming the lane).

## Declared work (first-published-priority)

This lane claims, to the exclusion of other parallel runs, the constructive upper-bound
question for s_12 and s_13 of the standard q=4 kyouen board (currently s_12 <= 11 and
s_13 <= 12 by the K0320 n-1 constructions):

(a) **Independent census** of the 12x12 and 13x13 forbidden-quartet structure (exact
    integer arithmetic; maximal-line and 4+-point-circle enumeration, C(m,4)
    decomposition), calibrated against the published K0057 values F_12 = 158,426
    (D = 17,154 + C = 141,272; lines 326, circles 34,031) and F_13 = 252,362
    (D = 27,340 + C = 225,022).
(b) **Exhaustive local nets around the published K0320 witnesses**: complete
    remove-1/add-0 and remove-2/add-1 enumeration on 12x12 around the 11-stone witness
    (target: a 10-stone maximal safe set in that neighborhood) and on 13x13 around the
    12-stone witness (target: 11 stones). Exact scans of the stated neighborhood; any
    negative outcome is recorded as a failed neighborhood search, never as nonexistence.
(c) **Stochastic local search (SLS) witness hunt**: 10-stone maximal safe sets on 12x12
    and 11-stone on 13x13, incremental-delta objective (safety violations + uncovered
    empty cells), seeded from transplanted published witnesses and from random restarts.
    This sandbox has no C compiler and kissat 4.0.4 cannot be built; **no UNSAT,
    nonexistence, or lower-bound claim is in scope from this lane, ever**.
(d) **Cross-board transplant diagnostics**: canonical placements (translations fitting in
    the larger board, D4 images) of the published K0320 witnesses on larger boards, with
    per-cell uncovered reports; recorded as finite observations (both outcomes are new
    facts: transfer vs non-transfer of maximality). This subitem does not claim the s_n
    upper/lower question for the host boards; it only records the transplant tables.
(e) **Publication**: experiment dir + scripts + machine-readable records, a K item per
    genuine new constructive bound, research log, knowledge README bullet; K numbers
    triple-checked at push time (items dir, README heading, recent commits).

## Acceptance conditions (fail-closed)

1. Census must reproduce all published anchors (F/D/C for n=12 and n=13) before any
   hunting; a mismatch aborts the lane.
2. Every claimed witness is verified by two independent verifier implementations
   (Python exact Fraction/integer-determinant geometry; a second Node/BigInt
   implementation with independent code path) AND receives a full empty-point
   certificate (per empty cell: an attacking stone triple and the curve coefficients),
   published in machine-readable JSON.
3. Constructive-upper-bound-only wording: each new witness is stated as s_n <= k on the
   stated board, explicitly not as equality; no lower bound, no monotonicity, no
   asymptotic claim, no s_n = k reading of any finite search.
4. Local nets and transplant tables are finite scans of the stated neighborhoods with
   recorded task sizes; negatives are labeled as such, not as absence proofs.
5. Every push is fetch-back byte-verified against the pinned commit SHA; latest main is
   re-fetched immediately before each push; on fetch/push/conflict failure the situation
   is recorded and deferred to the next run, never forced.
6. Finite-machine scope only; moves/evaluations/restart counts are not verdicts.

## Non-goals

- No s_11 work of any kind (owned by the a45a626d lane).
- No lower-bound/UNSAT machinery and therefore no s_12/s_13 lower bounds from this lane.
- No witness hunting beyond n=13 in this session; n >= 14 appears only inside the
  transplant diagnostics as recorded observations (no n >= 14 upper-bound claims).
- No claims about K_n (maximum safe size), no standard 11x11 game-value claims
  (WIN8/residual lanes own those).
- No fixed-width stabilization lengths (four-row/five-row/seven-row/three-row lanes are
  declared by others).
- No long-running server: all runs are local, time-capped per invocation, resumable.
