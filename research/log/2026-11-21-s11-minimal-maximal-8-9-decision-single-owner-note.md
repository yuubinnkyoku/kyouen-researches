# s_11 minimal-maximal decision (8/9-stone maximal safe sets on 11x11): single-owner declaration note

Date: 2026-11-21T07:22Z
Lane: standard-board minimal-maximal size s_n lane (K0026/K0312/K0147/K0148/K0149 family).
Declaration HEAD at write time: 2315f0d8a9d3231ec85021d3232a8ffd0e409400 (latest main at 07:18Z).
Not a continuation of any claimed lane; no prior declaration found for this target
(latest s_11-search record is the 2026-10-17 bounded advance inside K0148/K0149, incomplete).

## Declared work (first-published-priority)

This lane claims, to the exclusion of other parallel runs, the finite undetermined-value
question s_11 of the standard 11x11 q=4 kyouen board (currently 8 <= s_11 <= 10 by K0312
plus the K0320 10-stone maximal construction):

(a) **Independent census**: forbidden-quartet census of the 11x11 board (exact integer
    arithmetic, two independent implementations of the collinear/cocircular split),
    calibrated against the published exact values F_9 = 29,152 (3,156 + 25,996),
    F_10 = 54,441, F_11 = 95,670, F_12 = 158,426 (K0057 table). Publishing the
    unpublished D_11/C_11 split (collinear/cocircular quartet counts for n=11) if the
    two implementations agree.
(b) **Complete SAT encoding of "maximal safe with at most k stones"** on the n x n
    standard board: safety (at-most-3 per forbidden quartet), maximality (every empty
    cell covered by a curve holding >= 3 stones), |S| <= k cardinality. Controls:
    n=5,6,7 (published s_n = 5,6,7), n=9 both sides (s_9 = 9: k=9 SAT + k=8 UNSAT),
    and the K0320 n=11 10-stone witnesses must satisfy the k=10 CNF (positive control),
    plus a direct CNF-free brute-force cross-check for n <= 7.
(c) **Decision runs**: kissat 4.0.4 (pinned binary) on
    - (11, k=9): SAT -> s_11 <= 9 (witness published, independently verified by three
      systems: SAT-decode + two CNF-free geometry verifiers in Python and TypeScript/
      BigInt); UNSAT -> 9-stone exclusion.
    - (11, k=10): positive control (K0320 witness) — no minimality claim.
    - (11, k=8): if k=9 is SAT, decide 8 similarly; if k=9 is UNSAT the k=8 run decides
      whether s_11 = 8 or s_11 = 10 given K0312's 8 <= s_11.
    Honest cap-INDET records if a run does not finish; no absence claim from a timeout.
(d) **Publication**: experiment dir + records + research log + update of the K0312
    proposition (same-proposition status update), plus K0149 (monotonicity) and
    K0147/K0148 notes if the outcome changes their open questions; knowledge README
    bullet. K numbers triple-checked at push time (items dir, README heading, commits).

## Acceptance conditions (fail-closed)

1. Pins: kissat 4.0.4 linux-amd64, binary md5 3a5eba830aa6008a604fcc9bbe99a325
   (official rel-4.0.4 asset), F_n calibration targets exactly as in K0057.
2. Census split must match between the two implementations on n=9..12 totals before
   any CNF is built; F_11 must equal 95,670 exactly or the lane aborts.
3. All control runs (n=7 k=6 UNSAT / k=7 SAT; n=9 k=8 UNSAT / k=9 SAT; n=11 k=10 SAT
   with the K0320 witness checked literally against the CNF) must pass before any
   (11, k=8/9) verdict is claimed or pushed.
4. Every SAT witness is verified by three independent systems (python integer/Fraction
   geometry, TypeScript BigInt geometry, and satisfaction against the CNF clause list);
   every UNSAT claim records the full kissat log (conflicts, decisions, seconds) and a
   rerun bit-exact conflicts value.
5. Every push is fetch-back byte-verified against the pinned commit SHA; latest main is
   re-fetched immediately before each push; on fetch/push/conflict failure the
   situation is recorded and deferred to the next run, never forced.
6. Finite-machine scope only: no claims about s_n asymptotics, s_n for n >= 12, or
   monotonicity beyond what the s_11 outcome literally decides.

## Non-goals

- No claim about K_n (maximum safe size) for any n (n9-ge19 lane 21f8610464 owns K_9's
  upper bound; n10-ge20 witness lane is separate).
- No claim about the standard 11x11 game value classes (WIN8/residual lanes own those);
  this lane touches only the static extremal quantity s_11.
- No claim about fixed-width stabilization lengths (four-row q5/q6, three-row q4,
  five-row q7 lanes are all declared by others).
- No long-running server: all runs are local, time-capped per invocation, resumable.
